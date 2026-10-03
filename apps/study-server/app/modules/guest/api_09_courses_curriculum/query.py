from __future__ import annotations

from typing import Any

from app.core.database import query_many, query_one
from sqlalchemy.orm import Session

CHECK_PUBLISHED_COURSE = """
SELECT
    c.id,
    c.status
FROM courses AS c
WHERE c.id = :course_id AND c.status = :status
"""
LIST_PUBLISHED_LESSONS = """
SELECT
    l.id,
    l.course_id,
    l.name AS title,
    l.content,
    l.video_url,
    l.sort_order AS "order",
    l.status
FROM lessons AS l
WHERE l.course_id = :course_id AND l.status = :status
ORDER BY l.sort_order ASC, l.id ASC
"""


def find_published_course(
    db: Session,
    *,
    course_id: int,
) -> dict[str, Any] | None:
    """Return the course record if it exists and is published."""
    return query_one(
        db,
        CHECK_PUBLISHED_COURSE,
        {
            "course_id": course_id,
            "status": "PUBLISHED",
        },
    )


def find_published_lessons(
    db: Session,
    *,
    course_id: int,
) -> list[dict[str, Any]]:
    """Return all published lessons of a course ordered by sort_order and id."""
    return query_many(
        db,
        LIST_PUBLISHED_LESSONS,
        {
            "course_id": course_id,
            "status": "PUBLISHED",
        },
    )
