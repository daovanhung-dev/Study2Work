"""Business orchestration for the course resources endpoint."""

from __future__ import annotations

import logging
from typing import Any

from app.core.responses import error_response, success_response
from app.modules.guest.api_11_courses_resources.models import ResourceItem
from app.modules.guest.api_11_courses_resources.query import (
    find_course_resources,
    find_published_course,
)
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


# API #11 courses_resources
def get_course_resources(
    *,
    course_id: int,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Return resources for a published course."""

    try:
        course = find_published_course(db, course_id=course_id)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Course visibility check failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if course is None:
        return _not_found_error(trace_id)

    try:
        rows = find_course_resources(db, course_id=course_id)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Course resources query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if not rows:
        return _not_found_error(trace_id)

    try:
        first_row = rows[0]
        resource = ResourceItem(
            id=first_row["id"],
            name=first_row["name"],
            type=first_row["resource_type"],  # map resource_type -> type
            url=first_row["url"],
            lesson_id=first_row["lesson_id"],
        )
    except (ValidationError, KeyError):
        logger.exception("Resource mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Resource retrieved.",
        trace_id=trace_id,
        data=resource.model_dump(mode="json"),
    )


def _not_found_error(trace_id: str) -> JSONResponse:
    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Published course or resource not found.",
        trace_id=trace_id,
    )


def _internal_error(trace_id: str) -> JSONResponse:
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Resources could not be retrieved.",
        trace_id=trace_id,
    )