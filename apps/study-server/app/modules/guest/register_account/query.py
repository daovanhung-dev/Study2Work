from __future__ import annotations

from typing import Any

from app.core.database import query_one
from sqlalchemy.orm import Session

CHECK_DUPLICATE = "SELECT id FROM users WHERE email = :email"
INSERT_USER = """
INSERT INTO users (
    full_name,
    email,
    password_hash,
    role,
    avatar_url,
    phone,
    created_at,
    updated_at
)
VALUES (
    :full_name,
    :email,
    :password_hash,
    'STUDENT',
    NULL,
    NULL,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
)
RETURNING
    id,
    full_name,
    email,
    role,
    avatar_url,
    phone,
    status,
    created_at,
    updated_at
"""


def find_user_by_email(
    db: Session,
    email: str,
) -> dict[str, Any] | None:
    """Return the existing user ID for an email, if present."""

    return query_one(db, CHECK_DUPLICATE, {"email": email})


def insert_user(
    db: Session,
    *,
    full_name: str,
    email: str,
    password_hash: str,
) -> dict[str, Any] | None:
    """Insert one account and return its public profile fields."""

    return query_one(
        db,
        INSERT_USER,
        {
            "full_name": full_name,
            "email": email,
            "password_hash": password_hash,
        },
    )
