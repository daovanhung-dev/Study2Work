"""Password, JWT and opaque-token primitives shared by API modules."""

from __future__ import annotations

import hashlib
import hmac
import secrets
from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
from typing import Any, Literal, Protocol
from uuid import uuid4

import bcrypt
import jwt
from argon2 import PasswordHasher as Argon2PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError
from jwt.exceptions import InvalidTokenError

from app.core.config import get_settings

ACCESS_TOKEN = "access"
REFRESH_TOKEN = "refresh"
PASSWORD_ALGORITHM: Literal["ARGON2ID"] = "ARGON2ID"
PasswordAlgorithm = Literal["ARGON2ID", "BCRYPT"]

_argon2_hasher = Argon2PasswordHasher(
    time_cost=3,
    memory_cost=64 * 1024,
    parallelism=1,
)


class TokenKeyProvider(Protocol):
    """Interface for a local static key store or a JWKS-backed provider."""

    def get_verification_key(self, *, key_id: str | None) -> str | bytes:
        """Return the public verification key for a JWT ``kid``."""


JwksKeyProvider = TokenKeyProvider


class TokenError(Exception):
    """Raised when a token cannot be trusted or has the wrong token type."""


class PasswordHasher:
    """Hash new passwords with Argon2id and verify supported legacy hashes."""

    @staticmethod
    def hash(
        password: str,
        algorithm: PasswordAlgorithm = PASSWORD_ALGORITHM,
    ) -> str:
        if algorithm == "ARGON2ID":
            return _argon2_hasher.hash(password)
        if algorithm == "BCRYPT":
            return bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt(),
            ).decode("utf-8")
        raise ValueError(f"Unsupported password algorithm: {algorithm}")

    @staticmethod
    def verify(
        password: str,
        hashed_password: str,
        algorithm: str | None = None,
    ) -> bool:
        normalized_algorithm = (algorithm or "").upper()
        detected_algorithm = password_algorithm_for_hash(hashed_password)
        selected_algorithm = normalized_algorithm or detected_algorithm

        if selected_algorithm == "ARGON2ID":
            try:
                return _argon2_hasher.verify(hashed_password, password)
            except (VerifyMismatchError, VerificationError, InvalidHashError):
                return False

        if selected_algorithm == "BCRYPT":
            try:
                return bcrypt.checkpw(
                    password.encode("utf-8"),
                    hashed_password.encode("utf-8"),
                )
            except (ValueError, TypeError):
                return False

        return False


def password_algorithm_for_hash(hashed_password: str) -> PasswordAlgorithm | None:
    """Detect a supported password hash format without verifying it."""

    if hashed_password.startswith("$argon2"):
        return "ARGON2ID"
    if hashed_password.startswith(("$2a$", "$2b$", "$2y$")):
        return "BCRYPT"
    return None


def needs_password_rehash(
    hashed_password: str,
    algorithm: str | None = None,
) -> bool:
    """Return whether a verified password should be upgraded to Argon2id."""

    normalized_algorithm = (algorithm or "").upper()
    detected_algorithm = password_algorithm_for_hash(hashed_password)
    selected_algorithm = normalized_algorithm or detected_algorithm

    if selected_algorithm == "ARGON2ID":
        try:
            return _argon2_hasher.check_needs_rehash(hashed_password)
        except (InvalidHashError, TypeError):
            return True
    return selected_algorithm != "ARGON2ID"


def hash_password(password: str) -> str:
    """Hash a new application password with the canonical Argon2id policy."""

    return PasswordHasher.hash(password)


def verify_password(
    password: str,
    hashed_password: str,
    algorithm: str | None = None,
) -> bool:
    """Return whether a plaintext password matches a stored hash."""

    return PasswordHasher.verify(password, hashed_password, algorithm)


def _settings_secret(value: Any) -> str | None:
    if value is None:
        return None
    return value.get_secret_value() if hasattr(value, "get_secret_value") else str(value)


def _signing_key() -> str:
    config = get_settings()
    if config.jwt_algorithm == "ES256":
        private_key = _settings_secret(config.jwt_private_key)
        if not private_key:
            raise TokenError("JWT private key chưa được cấu hình")
        return private_key

    secret_key = _settings_secret(config.jwt_secret_key)
    if not secret_key:
        raise TokenError("JWT secret key chưa được cấu hình")
    return secret_key


def _verification_key(
    token: str,
    key_provider: TokenKeyProvider | None,
) -> str | bytes:
    config = get_settings()
    if key_provider is not None:
        try:
            header = jwt.get_unverified_header(token)
            return key_provider.get_verification_key(key_id=header.get("kid"))
        except (InvalidTokenError, KeyError, TypeError) as exc:
            raise TokenError("Không lấy được khóa xác thực token") from exc

    if config.jwt_algorithm == "ES256":
        if not config.jwt_public_key:
            raise TokenError("JWT public key chưa được cấu hình")
        return config.jwt_public_key

    secret_key = _settings_secret(config.jwt_secret_key)
    if not secret_key:
        raise TokenError("JWT secret key chưa được cấu hình")
    return secret_key


def _create_token(
    *,
    subject: str,
    token_type: str,
    expires_delta: timedelta,
    claims: Mapping[str, Any] | None = None,
    include_audience: bool = True,
) -> str:
    config = get_settings()
    now = datetime.now(UTC)
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "jti": str(uuid4()),
        "iat": now,
        "exp": now + expires_delta,
        "iss": config.jwt_issuer,
    }
    if include_audience:
        payload["aud"] = config.jwt_audience

    reserved_claims = {"sub", "type", "jti", "iat", "exp", "iss", "aud"}
    for key, value in (claims or {}).items():
        if key not in reserved_claims:
            payload[key] = value

    return jwt.encode(
        payload,
        _signing_key(),
        algorithm=config.jwt_algorithm,
    )


def create_access_token(
    *,
    user_id: str,
    roles: list[str] | None = None,
    claims: Mapping[str, Any] | None = None,
) -> str:
    """Create a canonical access token for a subject."""

    token_claims = dict(claims or {})
    token_claims.setdefault("roles", roles or [])
    return _create_token(
        subject=user_id,
        token_type=ACCESS_TOKEN,
        expires_delta=timedelta(minutes=get_settings().jwt_access_token_expire_minutes),
        claims=token_claims,
    )


def create_refresh_token(*, user_id: str) -> str:
    """Create the legacy JWT refresh token used by the current auth module.

    New Identity code should use ``generate_refresh_token`` and persist only
    ``hash_refresh_token``.  This wrapper remains temporarily for compatibility
    with the existing module until its session schema is available.
    """

    return _create_token(
        subject=user_id,
        token_type=REFRESH_TOKEN,
        expires_delta=timedelta(days=get_settings().jwt_refresh_token_expire_days),
        include_audience=False,
    )


def decode_token(
    token: str,
    *,
    expected_type: str,
    key_provider: TokenKeyProvider | None = None,
    require_audience: bool = True,
) -> dict[str, Any]:
    """Decode and strictly validate a JWT."""

    config = get_settings()
    required_claims = ["sub", "type", "jti", "iat", "exp", "iss"]
    decode_options: dict[str, Any] = {
        "require": required_claims,
    }
    decode_kwargs: dict[str, Any] = {
        "algorithms": [config.jwt_algorithm],
        "issuer": config.jwt_issuer,
        "options": decode_options,
    }
    if require_audience:
        required_claims.append("aud")
        decode_kwargs["audience"] = config.jwt_audience
    else:
        decode_options["verify_aud"] = False

    try:
        payload = jwt.decode(
            token,
            _verification_key(token, key_provider),
            **decode_kwargs,
        )
    except (InvalidTokenError, TokenError, TypeError, ValueError) as exc:
        raise TokenError("Token không hợp lệ hoặc đã hết hạn") from exc

    if payload.get("type") != expected_type:
        raise TokenError("Sai loại token")

    subject = payload.get("sub")
    if not isinstance(subject, str) or not subject:
        raise TokenError("Token thiếu subject hợp lệ")

    return payload


def decode_access_token(
    token: str,
    *,
    key_provider: TokenKeyProvider | None = None,
) -> dict[str, Any]:
    return decode_token(
        token,
        expected_type=ACCESS_TOKEN,
        key_provider=key_provider,
    )


def decode_refresh_token(
    token: str,
    *,
    key_provider: TokenKeyProvider | None = None,
) -> dict[str, Any]:
    """Decode a legacy JWT refresh token without requiring an audience claim."""

    return decode_token(
        token,
        expected_type=REFRESH_TOKEN,
        key_provider=key_provider,
        require_audience=False,
    )


def generate_refresh_token() -> str:
    """Generate an opaque refresh token with no embedded user information."""

    return secrets.token_urlsafe(48)


def hash_refresh_token(token: str, pepper: str | None = None) -> str:
    """Return the keyed SHA-256 digest used for refresh-token persistence."""

    config = get_settings()
    configured_pepper = pepper or _settings_secret(config.refresh_token_pepper)
    if configured_pepper is None:
        configured_pepper = _settings_secret(config.jwt_secret_key)
    if not configured_pepper:
        raise TokenError("Refresh token pepper chưa được cấu hình")

    return hmac.new(
        configured_pepper.encode("utf-8"),
        token.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def compare_token_hash(expected: str, actual: str) -> bool:
    """Compare token digests in constant time."""

    return hmac.compare_digest(expected, actual)
