"""Opaque refresh-token helpers."""

from __future__ import annotations

import hashlib
import hmac
import secrets
from typing import Any

from app.core.config import get_settings
from app.core.security.exceptions import TokenError


def generate_refresh_token() -> str:
    """Generate a cryptographically secure refresh token."""

    return secrets.token_urlsafe(48)


def hash_refresh_token(token: str) -> str:
    """Hash a refresh token before storing it in the database."""

    pepper = _get_refresh_token_pepper()

    return hmac.new(
        pepper.encode("utf-8"),
        token.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def compare_refresh_token(
    token: str,
    stored_hash: str,
) -> bool:
    """Check whether a refresh token matches its stored hash."""

    token_hash = hash_refresh_token(token)

    return hmac.compare_digest(
        token_hash,
        stored_hash,
    )


def _get_refresh_token_pepper() -> str:
    settings = get_settings()

    pepper = _secret_value(
        settings.refresh_token_pepper,
    )

    if not pepper:
        raise TokenError(
            "Refresh token pepper chưa được cấu hình"
        )

    return pepper


def _secret_value(value: Any) -> str | None:
    if value is None:
        return None

    if hasattr(value, "get_secret_value"):
        return value.get_secret_value()

    return str(value)
