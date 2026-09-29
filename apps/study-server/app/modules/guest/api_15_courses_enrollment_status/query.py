"""Parameterized SQL for the course enrollment status endpoint."""

from __future__ import annotations

from typing import Any

from app.core.database import query_one
from sqlalchemy.orm import Session

FIND_COURSE = """
SELECT
    c.id,
    c.status
FROM courses AS c
WHERE c.id = :course_id
LIMIT 1
"""

FIND_USER_ENROLLMENT = """
SELECT
    e.id,
    e.user_id,
    e.course_id,
    e.status,
    e.enrolled_at,
    e.completed_at
FROM enrollments AS e
WHERE e.course_id = :course_id
  AND e.user_id = :user_id
ORDER BY e.id DESC
LIMIT 1
"""

FIND_ANY_ENROLLMENT_BY_COURSE = """
SELECT
    e.id,
    e.user_id,
    e.course_id,
    e.status,
    e.enrolled_at,
    e.completed_at
FROM enrollments AS e
WHERE e.course_id = :course_id
ORDER BY e.id DESC
LIMIT 1
"""


def find_course_by_id(
    db: Session,
    *,
    course_id: int
    ) -> dict[str, Any] | None:
    """Return course row if it exists."""
    return query_one(db, FIND_COURSE, {"course_id": course_id})


def find_enrollment(
    db: Session,
    *,
    course_id: int,
    user_id: int | None = None,
) -> dict[str, Any] | None:
    """Find enrollment for a specific user, or fallback to course scope."""
    if user_id is not None:
        return query_one(db, FIND_USER_ENROLLMENT, {"course_id": course_id, "user_id": user_id})
    return query_one(db, FIND_ANY_ENROLLMENT_BY_COURSE, {"course_id": course_id})