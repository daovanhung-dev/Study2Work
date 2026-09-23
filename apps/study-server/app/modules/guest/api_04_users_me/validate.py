"""Pure request-header and JWT-claim validation for API #4."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def extract_bearer_token(authorization: str | None) -> str:
    """Extract one opaque JWT value from an Authorization header."""

    if authorization is None:
        raise ValueError("Authorization header is required")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise ValueError("Authorization header must use Bearer scheme")

    return parts[1]


def validate_access_claims(claims: Mapping[str, Any]) -> tuple[int, list[str]]:
    """Validate the current JWT claim shape and return normalized values."""

    subject = claims.get("sub")
    if not isinstance(subject, str) or not subject:
        raise ValueError("JWT subject is missing")

    try:
        user_id = int(subject)
    except ValueError as exc:
        raise ValueError("JWT subject is not a numeric user ID") from exc

    if user_id <= 0:
        raise ValueError("JWT subject is not a positive user ID")

    raw_roles = claims.get("roles")
    if not isinstance(raw_roles, list) or not raw_roles:
        raise ValueError("JWT roles are missing")

    if not all(isinstance(role, str) and role.strip() for role in raw_roles):
        raise ValueError("JWT roles are invalid")

    roles = [role.strip().upper() for role in raw_roles]
    return user_id, roles
