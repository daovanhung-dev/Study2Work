from __future__ import annotations

import logging
from typing import Any

from app.core.responses import ApiError, success_response
from app.modules.guest.api_09_courses_curriculum.models import (
    Lesson,
    LessonPage,
    Pagination,
)
from app.modules.guest.api_09_courses_curriculum.query import (
    find_published_course,
    find_published_lessons,
)
from app.modules.guest.api_09_courses_curriculum.validate import parse_course_id
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


def _internal_error(trace_id: str) -> ApiError:
    """Build the standard 500 error when database query or mapping fails."""
    return ApiError(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Curriculum could not be retrieved.",
        trace_id=trace_id,
    )


# API #09 get_course_curriculum
def get_course_curriculum(
    *,
    course_id_raw: str | int,
    db: Session,
    trace_id: str,
) -> dict[str, Any]:
    """Return the ordered list of published lessons in a published course."""
    # DD 1.2: Validate course_id path segment; invalid formats map to 404 per DD #09.
    try:
        course_id = parse_course_id(course_id_raw)
    except ValueError as exc:
        raise _course_not_found_error(trace_id) from exc
    # DD 2.1 & 2.2: Course visibility gate (Q1).
    try:
        course = find_published_course(db, course_id=course_id)
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Course lookup failed; trace_id=%s", trace_id)
        raise _internal_error(trace_id) from exc
    if course is None:
        raise _course_not_found_error(trace_id)
    # DD 3.1 & 3.2: Query published lessons (Q2).
    try:
        rows = find_published_lessons(db, course_id=course_id)
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Curriculum lookup failed; trace_id=%s", trace_id)
        raise _internal_error(trace_id) from exc
    # DD 4.1 & 4.2: Map lessons and build LessonPage response.
    try:
        items = [Lesson.model_validate(row) for row in rows]
        total = len(items)
        page = LessonPage(
            items=items,
            pagination=Pagination(
                page=1,
                size=total,
                total=total,
                total_pages=1 if total > 0 else 0,
            ),
        )
    except ValidationError as exc:
        logger.exception("Curriculum mapping failed; trace_id=%s", trace_id)
        raise _internal_error(trace_id) from exc
    # DD 5.1: Return canonical success response envelope.
    message = "Curriculum retrieved." if total else "No published lessons."
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message=message,
        trace_id=trace_id,
        data=page.model_dump(mode="json"),
    )
