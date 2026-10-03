from __future__ import annotations

from typing import Any

from app.core.database import query_one
from sqlalchemy.orm import Session

FIND_PUBLISHED_COURSE_DETAIL = """
SELECT
    c.id,
    c.name AS title,
    c.description,
    c.thumbnail_url,
    c.price,
    c.status,
    m.id AS mentor_id,
    m.full_name AS mentor_full_name,
    m.avatar_url AS mentor_avatar_url
FROM courses AS c
LEFT JOIN users AS m ON m.id = c.mentor_id
WHERE c.id = :course_id AND c.status = :status
"""


def find_published_course_detail(
    db: Session,
    *,
    course_id: int,
) -> dict[str, Any] | None:
    """Return one published course record with its mentor projection."""
    return query_one(
        db,
        FIND_PUBLISHED_COURSE_DETAIL,
        {
            "course_id": course_id,
            "status": "PUBLISHED",
        },
    )
