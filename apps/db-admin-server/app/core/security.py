"""OIDC/JWKS authentication and server-side DB Admin permission checks."""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

import jwt
from fastapi import Depends, Header, HTTPException, Request, status
from jwt import PyJWKClient

from app.core.config import get_settings

logger = logging.getLogger("db_admin.auth")
AuthorizationHeader = Header(default=None)


@dataclass(frozen=True)
class Principal:
    subject: str
    permissions: frozenset[str]
    roles: frozenset[str]
    claims: dict[str, Any]


def _string_set(value: object) -> frozenset[str]:
    if isinstance(value, str):
        return frozenset(item for item in value.split() if item)
    if isinstance(value, list):
        return frozenset(str(item) for item in value if isinstance(item, str) and item)
    return frozenset()


def _principal_from_claims(claims: dict[str, Any]) -> Principal:
    subject = claims.get("sub")
    if not isinstance(subject, str) or not subject:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid identity")
    permissions = _string_set(claims.get("permissions")) | _string_set(claims.get("scope"))
    roles = _string_set(claims.get("roles"))
    if "DB_ADMIN" in roles:
        permissions |= frozenset({"db_admin:read", "db_admin:write", "db_admin:sql"})
    return Principal(subject=subject, permissions=permissions, roles=roles, claims=claims)


@lru_cache(maxsize=1)
def _jwks_client(url: str) -> PyJWKClient:
    return PyJWKClient(url, cache_jwk_set=True, lifespan=300, timeout=5)


def _dev_principal() -> Principal:
    return Principal(
        subject="local-dev-admin",
        permissions=frozenset({"db_admin:read", "db_admin:write", "db_admin:sql"}),
        roles=frozenset({"DB_ADMIN"}),
        claims={"sub": "local-dev-admin", "roles": ["DB_ADMIN"]},
    )


def authenticate(
    request: Request,
    authorization: str | None = AuthorizationHeader,
) -> Principal:
    settings = getattr(request.app.state, "settings", None) or get_settings()
    if settings.dev_auth:
        return _dev_principal()
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )
    token = authorization[7:].strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )
    try:
        client = _jwks_client(settings.jwks_url or "")
        signing_key = client.get_signing_key_from_jwt(token)
        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=settings.jwt_algorithms,
            issuer=settings.jwt_issuer,
            audience=settings.jwt_audience,
            options={"require": ["sub", "exp"]},
        )
        principal = _principal_from_claims(dict(claims))
        request.state.principal = principal
        return principal
    except HTTPException:
        raise
    except Exception as exc:
        logger.warning("DB Admin authentication failed: %s", type(exc).__name__)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid identity"
        ) from exc


PrincipalDependency = Depends(authenticate)


def require_permission(permission: str) -> Callable[..., Principal]:
    def dependency(principal: Principal = PrincipalDependency) -> Principal:
        if permission not in principal.permissions:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        return principal

    return dependency
