from __future__ import annotations

from typing import Any

from app.core.database import query_many, query_one
from app.modules.guest.courses.models import SORT_FIELDS
from sqlalchemy.orm import Session

SORT_COLUMNS = {
    "id": "c.id",
    "name": "c.name",
    "price": "c.price",
    "created_at": "c.created_at",
}

LIST_PUBLISHED_COURSES = """
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
ORDER BY {order_by}
LIMIT :limit OFFSET :offset
"""

COUNT_PUBLISHED_COURSES = """
SELECT
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE m.id IS NULL) AS missing_mentor_count
FROM courses AS c
LEFT JOIN users AS m ON m.id = c.mentor_id
WHERE c.status = :status
"""


def build_order_by(sort: str | None) -> str:
    """Map validated sort input to a static SQL ORDER BY expression."""

    if sort is None:
        return "c.created_at DESC, c.id ASC"

    field, direction = sort.split(":")
    if field not in SORT_FIELDS or field not in SORT_COLUMNS:
        raise ValueError("sort field không được hỗ trợ.")

    column = SORT_COLUMNS[field]
    direction_sql = direction.upper()
    if field == "id":
        return f"{column} {direction_sql}"
    return f"{column} {direction_sql}, c.id ASC"


def find_published_courses(
    db: Session,
    *,
    page: int,
    size: int,
    sort: str | None,
) -> list[dict[str, Any]]:
    """Return one page of published courses with their mentor projection."""

    offset = (page - 1) * size
    query = LIST_PUBLISHED_COURSES.format(order_by=build_order_by(sort))
    return query_many(
        db,
        query,
        {
            "status": "PUBLISHED",
            "limit": size,
            "offset": offset,
        },
    )


def count_published_courses(db: Session) -> dict[str, Any]:
    """Return the total and mentor-integrity count for published courses."""

    return query_one(
        db,
        COUNT_PUBLISHED_COURSES,
        {"status": "PUBLISHED"},
    ) or {"total": 0, "missing_mentor_count": 0}
