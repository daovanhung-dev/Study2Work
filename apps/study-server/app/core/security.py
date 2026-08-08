from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

import bcrypt
import jwt
from argon2 import PasswordHasher as Argon2PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError
from jwt.exceptions import InvalidTokenError

from app.core.config import settings


ACCESS_TOKEN = "access"
REFRESH_TOKEN = "refresh"

_argon2_hasher = Argon2PasswordHasher()


class TokenError(Exception):
    """Raised when a JWT cannot be trusted or does not match the expected type."""


class PasswordHasher:
    @staticmethod
    def hash(password: str) -> str:
        """Hash new application passwords with bcrypt.

        The existing project registration flow stores the algorithm as BCRYPT,
        so this remains the write algorithm for backward compatibility.
        """
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")

    @staticmethod
    def verify(
        password: str,
        hashed_password: str,
        algorithm: str | None = None,
    ) -> bool:
        normalized_algorithm = (algorithm or "").upper()

        if normalized_algorithm == "ARGON2ID" or hashed_password.startswith("$argon2"):
            try:
                return _argon2_hasher.verify(hashed_password, password)
            except (VerifyMismatchError, VerificationError, InvalidHashError):
                return False

        if normalized_algorithm in {"", "BCRYPT"} or hashed_password.startswith(("$2a$", "$2b$", "$2y$")):
            try:
                return bcrypt.checkpw(
                    password.encode("utf-8"),
                    hashed_password.encode("utf-8"),
                )
            except (ValueError, TypeError):
                return False

        return False


def hash_password(password: str) -> str:
    """Hash a plaintext password with the application's password hasher."""
    return PasswordHasher.hash(password)


def verify_password(
    password: str,
    hashed_password: str,
    algorithm: str | None = None,
) -> bool:
    """Return whether a plaintext password matches a stored password hash."""
    return PasswordHasher.verify(password, hashed_password, algorithm)


def _create_token(
    *,
    subject: str,
    token_type: str,
    expires_delta: timedelta,
    claims: dict[str, Any] | None = None,
) -> str:
    now = datetime.now(UTC)
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "jti": str(uuid4()),
        "iat": now,
        "exp": now + expires_delta,
        "iss": settings.JWT_ISSUER,
    }

    if claims:
        # Reserved JWT claims cannot be overwritten by caller-provided data.
        for key, value in claims.items():
            if key not in {"sub", "type", "jti", "iat", "exp", "iss"}:
                payload[key] = value

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY.get_secret_value(),
        algorithm=settings.JWT_ALGORITHM,
    )


def create_access_token(
    *,
    user_id: str,
    roles: list[str] | None = None,
) -> str:
    return _create_token(
        subject=user_id,
        token_type=ACCESS_TOKEN,
        expires_delta=timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
        claims={"roles": roles or []},
    )


def create_refresh_token(*, user_id: str) -> str:
    return _create_token(
        subject=user_id,
        token_type=REFRESH_TOKEN,
        expires_delta=timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS),
    )


def decode_token(
    token: str,
    *,
    expected_type: str,
) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY.get_secret_value(),
            algorithms=[settings.JWT_ALGORITHM],
            issuer=settings.JWT_ISSUER,
            options={
                "require": ["sub", "type", "jti", "iat", "exp", "iss"],
            },
        )
    except InvalidTokenError as exc:
        raise TokenError("Token không hợp lệ hoặc đã hết hạn") from exc

    if payload.get("type") != expected_type:
        raise TokenError("Sai loại token")

    subject = payload.get("sub")
    if not isinstance(subject, str) or not subject:
        raise TokenError("Token thiếu subject hợp lệ")

    return payload


def decode_access_token(token: str) -> dict[str, Any]:
    return decode_token(token, expected_type=ACCESS_TOKEN)


def decode_refresh_token(token: str) -> dict[str, Any]:
    return decode_token(token, expected_type=REFRESH_TOKEN)
