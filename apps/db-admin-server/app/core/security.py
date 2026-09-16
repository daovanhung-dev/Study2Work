"""Local/OIDC authentication and server-side DB Admin permission checks."""

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
    user_id: str | None = None
    username: str | None = None
    is_root: bool = False
    must_change_password: bool = False
    targets: frozenset[str] = frozenset()
    schema_bindings: tuple[dict[str, str], ...] = ()


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
    permissions = set(_string_set(claims.get("permissions"))) | set(
        _string_set(claims.get("scope"))
    )
    roles = _string_set(claims.get("roles"))
    is_root = bool(claims.get("isRoot", claims.get("is_root", False)))
    if "DB_ADMIN" in roles:
        permissions |= frozenset({"db_admin:read", "db_admin:write", "db_admin:sql"})
    if is_root:
        permissions.add("db_admin:manage")
    bindings: list[dict[str, str]] = []
    raw_bindings = claims.get("schemaBindings", claims.get("schema_bindings", []))
    if isinstance(raw_bindings, list):
        for item in raw_bindings:
            if not isinstance(item, dict):
                continue
            database = item.get("database") or item.get("databaseTarget")
            schema = item.get("schema") or item.get("schemaName")
            if isinstance(database, str) and isinstance(schema, str):
                bindings.append({"database": database, "schema": schema})
    return Principal(
        subject=subject,
        permissions=frozenset(permissions),
        roles=roles,
        claims=claims,
        user_id=str(claims.get("userId")) if claims.get("userId") else None,
        username=claims.get("username") if isinstance(claims.get("username"), str) else None,
        is_root=is_root,
        must_change_password=bool(claims.get("mustChangePassword", False)),
        targets=_string_set(claims.get("targets")),
        schema_bindings=tuple(bindings),
    )


@lru_cache(maxsize=1)
def _jwks_client(url: str) -> PyJWKClient:
    return PyJWKClient(url, cache_jwk_set=True, lifespan=300, timeout=5)


def _dev_principal() -> Principal:
    return Principal(
        subject="local-dev-admin",
        permissions=frozenset(
            {"db_admin:read", "db_admin:write", "db_admin:sql", "db_admin:manage"}
        ),
        roles=frozenset({"DB_ADMIN"}),
        claims={"sub": "local-dev-admin", "roles": ["DB_ADMIN"]},
        is_root=True,
    )


def _decode_local_token(token: str, settings: Any) -> Principal | None:
    secret = settings.local_jwt_secret
    if not settings.local_auth_enabled or secret is None:
        return None
    try:
        claims = jwt.decode(
            token,
            secret.get_secret_value(),
            algorithms=["HS256"],
            issuer=settings.jwt_issuer,
            audience=settings.jwt_audience,
            options={"require": ["sub", "exp", "iss", "aud"]},
        )
        return _principal_from_claims(dict(claims))
    except Exception as exc:
        logger.debug("Local DB Admin token rejected: %s", type(exc).__name__)
        return None


def authenticate(
    request: Request,
    authorization: str | None = AuthorizationHeader,
) -> Principal:
    settings = getattr(request.app.state, "settings", None) or get_settings()
    if not authorization or not authorization.lower().startswith("bearer "):
        if settings.dev_auth:
            return _dev_principal()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )
    token = authorization[7:].strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )
    local_principal = _decode_local_token(token, settings)
    if local_principal is not None:
        resources = getattr(request.app.state, "resources", None)
        if resources is not None and local_principal.user_id is not None:
            try:
                if not resources.access.is_active(
                    local_principal, request.headers.get("X-Trace-Id", "auth")
                ):
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid identity"
                    )
            except HTTPException:
                raise
            except Exception as exc:
                logger.warning("DB Admin local account check failed: %s", type(exc).__name__)
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid identity"
                ) from exc
        request.state.principal = local_principal
        return local_principal
    if settings.dev_auth:
        return _dev_principal()
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
        if principal.must_change_password:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Password change required"
            )
        if permission not in principal.permissions:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        return principal

    return dependency


def require_root(principal: Principal = PrincipalDependency) -> Principal:
    if principal.must_change_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Password change required"
        )
    if not principal.is_root:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    return principal
