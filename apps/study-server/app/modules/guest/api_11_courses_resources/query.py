"""Parameterized SQL for the course resources endpoint."""

from __future__ import annotations

from typing import Any

from app.core.database import query_many, query_one
from sqlalchemy.orm import Session

FIND_PUBLISHED_COURSE = """
SELECT
    c.id,
    c.status
FROM courses AS c
WHERE c.id = :course_id
  AND c.status = 'PUBLISHED'
LIMIT 1
"""

FIND_COURSE_RESOURCES = """
SELECT
    r.id,
    r.lesson_id,
    r.name,
    r.resource_type,
    r.url
FROM lessons AS l
INNER JOIN resources AS r ON r.lesson_id = l.id
WHERE l.course_id = :course_id
ORDER BY r.id ASC
"""


def find_published_course(
    db: Session,
    *,
    course_id: int
    ) -> dict[str, Any] | None:
    """Return course if it exists and is published."""

    return query_one(db, FIND_PUBLISHED_COURSE, {"course_id": course_id})


def find_course_resources(
    db: Session,
    *,
    course_id: int
    ) -> list[dict[str, Any]]:
    """Return all resources linked to lessons in the course."""
    
    return query_many(db, FIND_COURSE_RESOURCES, {"course_id": course_id})