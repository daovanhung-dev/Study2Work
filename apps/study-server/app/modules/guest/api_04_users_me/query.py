"""Parameterized SQL for the current-user profile endpoint."""

from __future__ import annotations

from typing import Any

from app.core.database import query_one
from sqlalchemy.orm import Session

CURRENT_USER_PROFILE = """
SELECT
    u.id,
    u.full_name,
    u.email,
    u.role,
    u.avatar_url,
    u.phone,
    u.status,
    u.created_at,
    u.updated_at
FROM users AS u
WHERE u.id = :user_id
LIMIT 1
"""


def find_current_user(
    db: Session,
    *,
    user_id: int,
) -> dict[str, Any] | None:
    """Return only the public profile columns for one authenticated user."""

    return query_one(db, CURRENT_USER_PROFILE, {"user_id": user_id})
