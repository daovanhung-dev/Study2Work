from __future__ import annotations

from typing import Any

from app.core.database import query_many, query_one
from app.modules.guest._shared.course_catalog.constants import DEFAULT_SIZE
from app.modules.guest._shared.course_catalog.helpers import build_order_by
from sqlalchemy.orm import Session

LIST_SEARCHED_COURSES = """
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
WHERE c.status = :status
  AND (:q_pattern IS NULL OR LOWER(c.name) LIKE :q_pattern)
ORDER BY {order_by}
LIMIT :limit OFFSET :offset
"""

COUNT_SEARCHED_COURSES = """
SELECT
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE m.id IS NULL) AS missing_mentor_count
FROM courses AS c
LEFT JOIN users AS m ON m.id = c.mentor_id
WHERE c.status = :status
  AND (:q_pattern IS NULL OR LOWER(c.name) LIKE :q_pattern)
"""


def find_published_courses_search(
    db: Session,
    *,
    q: str | None,
    page: int,
    sort: str | None,
) -> list[dict[str, Any]]:
    """Return one fixed-size page of published courses matching ``q``."""

    offset = (page - 1) * DEFAULT_SIZE
    query = LIST_SEARCHED_COURSES.format(order_by=build_order_by(sort))
    return query_many(
        db,
        query,
        {
            "status": "PUBLISHED",
            "q_pattern": f"%{q}%" if q else None,
            "limit": DEFAULT_SIZE,
            "offset": offset,
        },
    )


def count_published_courses_search(
    db: Session,
    *,
    q: str | None,
) -> dict[str, Any]:
    """Return matching-course count and mentor-integrity count."""

    return query_one(
        db,
        COUNT_SEARCHED_COURSES,
        {
            "status": "PUBLISHED",
            "q_pattern": f"%{q}%" if q else None,
        },
    ) or {"total": 0, "missing_mentor_count": 0}
