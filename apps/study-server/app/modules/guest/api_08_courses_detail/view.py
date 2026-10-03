from __future__ import annotations

import logging
from decimal import InvalidOperation
from typing import Any

from app.core.responses import ApiError, success_response
from app.modules.guest._shared.course_catalog.helpers import (
    course_internal_error,
    map_course,
)
from app.modules.guest._shared.course_catalog.models import CoursePage, Pagination
from app.modules.guest.api_08_courses_detail.query import find_published_course_detail
from app.modules.guest.api_08_courses_detail.validate import parse_course_id
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def _course_not_found_error(trace_id: str) -> ApiError:
    """Build the standard 404 error when a course is not found or not published."""
    return ApiError(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Published course not found.",
        trace_id=trace_id,
    )


# API #08 get_course_detail
def get_course_detail(
    *,
    course_id_raw: str | int,
    db: Session,
    trace_id: str,
) -> dict[str, Any]:
    """Return the detailed view of one published course."""

    # DD 1.2: Validate course_id path segment; invalid formats are mapped to 404 per DD #08.
    try:
        course_id = parse_course_id(course_id_raw)
    except ValueError as exc:
        raise _course_not_found_error(trace_id) from exc

    # DD 2.1: Query published course detail joined with mentor.
    try:
        row = find_published_course_detail(db, course_id=course_id)
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Course detail lookup failed; trace_id=%s", trace_id)
        raise course_internal_error(trace_id) from exc

    # DD 3.2: Return 404 if course does not exist or is not in PUBLISHED status.
    if row is None:
        raise _course_not_found_error(trace_id)

    # DD 4.1 & 4.2: Map course fields and construct singleton CoursePage response.
    try:
        item = map_course(row)
        page = CoursePage(
            items=[item],
            pagination=Pagination(
                page=1,
                size=1,
                total=1,
                total_pages=1,
            ),
        )
    except (InvalidOperation, TypeError, ValueError, ValidationError) as exc:
        logger.exception("Course detail mapping failed; trace_id=%s", trace_id)
        raise course_internal_error(trace_id) from exc

    # DD 5.1: Return canonical success response envelope.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Course retrieved.",
        trace_id=trace_id,
        data=page.model_dump(mode="json"),
    )
