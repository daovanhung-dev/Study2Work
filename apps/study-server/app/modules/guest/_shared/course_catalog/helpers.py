from __future__ import annotations

from decimal import Decimal
from typing import Any

from app.core.responses import ApiError
from app.modules.guest._shared.course_catalog.constants import (
    SORT_COLUMNS,
    SORT_DIRECTIONS,
    SORT_FIELDS,
)
from app.modules.guest._shared.course_catalog.models import Course, MentorSummary


def normalize_sort(value: str | None) -> str | None:
    """Validate and normalize one public ``field:direction`` sort expression."""

    if value is None:
        return None

    parts = value.split(":")
    if len(parts) != 2:
        raise ValueError("sort phải có định dạng field:direction.")

    field, direction = parts
    if field not in SORT_FIELDS:
        raise ValueError("sort field không được hỗ trợ.")
    if direction not in SORT_DIRECTIONS:
        raise ValueError("sort direction không được hỗ trợ.")
    return f"{field}:{direction}"


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


def map_course(row: dict[str, Any]) -> Course:
    """Map one joined course row to the shared public course contract."""

    mentor_id = row.get("mentor_id")
    mentor_name = row.get("mentor_full_name")
    if mentor_id is None or mentor_name is None:
        raise ValueError("Published course is missing a mentor.")

    return Course(
        id=row.get("id"),
        title=row.get("title"),
        description=row.get("description"),
        thumbnail_url=row.get("thumbnail_url"),
        price=decimal_string(row.get("price")),
        status=row.get("status"),
        mentor=MentorSummary(
            id=mentor_id,
            full_name=mentor_name,
            avatar_url=row.get("mentor_avatar_url"),
        ),
    )


def decimal_string(value: Any) -> str:
    """Serialize a numeric course price without floating-point conversion."""

    if value is None:
        raise ValueError("Course price is missing.")
    return format(Decimal(str(value)), "f")


def course_internal_error(trace_id: str) -> ApiError:
    """Build the shared safe error for course read failures."""

    return ApiError(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Courses could not be retrieved.",
        trace_id=trace_id,
    )
