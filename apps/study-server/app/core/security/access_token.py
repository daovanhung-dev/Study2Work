"""JWT access-token creation and verification."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

import jwt
from jwt.exceptions import InvalidTokenError

from app.core.config import get_settings
from app.core.security.exceptions import TokenError


ACCESS_TOKEN_TYPE = "access"

RESERVED_CLAIMS = {
    "sub",
    "type",
    "jti",
    "iat",
    "exp",
    "iss",
    "aud",
}


def create_access_token(
    *,
    user_id: str,
    roles: list[str] | None = None,
    claims: Mapping[str, Any] | None = None,
) -> str:
    """Create a signed JWT access token."""

    settings = get_settings()
    now = datetime.now(UTC)

    payload: dict[str, Any] = {
        "sub": user_id,
        "type": ACCESS_TOKEN_TYPE,
        "roles": roles or [],
        "jti": str(uuid4()),
        "iat": now,
        "exp": now
        + timedelta(
            minutes=settings.jwt_access_token_expire_minutes,
        ),
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
    }

    _add_custom_claims(
        payload=payload,
        claims=claims,
    )

    return jwt.encode(
        payload,
        _get_signing_key(),
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(
    token: str,
) -> dict[str, Any]:
    """Decode and validate an access token."""

    settings = get_settings()

    try:
        payload = jwt.decode(
            token,
            _get_verification_key(),
            algorithms=[settings.jwt_algorithm],
            issuer=settings.jwt_issuer,
            audience=settings.jwt_audience,
            options={
                "require": [
                    "sub",
                    "type",
                    "jti",
                    "iat",
                    "exp",
                    "iss",
                    "aud",
                ],
            },
        )
    except (
        InvalidTokenError,
        TokenError,
        TypeError,
        ValueError,
    ) as exc:
        raise TokenError(
            "Token không hợp lệ hoặc đã hết hạn"
        ) from exc

    if payload.get("type") != ACCESS_TOKEN_TYPE:
        raise TokenError("Sai loại token")

    user_id = payload.get("sub")

    if not isinstance(user_id, str) or not user_id:
        raise TokenError("Token thiếu user_id hợp lệ")

    return payload


def _add_custom_claims(
    *,
    payload: dict[str, Any],
    claims: Mapping[str, Any] | None,
) -> None:
    if not claims:
        return

    for key, value in claims.items():
        if key not in RESERVED_CLAIMS:
            payload[key] = value


def _get_signing_key() -> str:
    settings = get_settings()

    if settings.jwt_algorithm == "ES256":
        private_key = _secret_value(settings.jwt_private_key)

        if not private_key:
            raise TokenError(
                "JWT private key chưa được cấu hình"
            )

        return private_key

    secret_key = _secret_value(settings.jwt_secret_key)

    if not secret_key:
        raise TokenError(
            "JWT secret key chưa được cấu hình"
        )

    return secret_key


def _get_verification_key() -> str:
    settings = get_settings()

    if settings.jwt_algorithm == "ES256":
        public_key = _secret_value(settings.jwt_public_key)

        if not public_key:
            raise TokenError(
                "JWT public key chưa được cấu hình"
            )

        return public_key

    secret_key = _secret_value(settings.jwt_secret_key)

    if not secret_key:
        raise TokenError(
            "JWT secret key chưa được cấu hình"
        )

    return secret_key


def _secret_value(value: Any) -> str | None:
    if value is None:
        return None

    if hasattr(value, "get_secret_value"):
        return value.get_secret_value()

    return str(value)
