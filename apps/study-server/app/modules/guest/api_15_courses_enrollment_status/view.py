"""Business orchestration for the course enrollment status endpoint."""

from __future__ import annotations

import logging
from typing import Any

from app.core.responses import error_response, success_response
from app.modules.guest.api_15_courses_enrollment_status.models import (
    EnrollmentStatusResponse,
)
from app.modules.guest.api_15_courses_enrollment_status.query import (
    find_course_by_id,
    find_enrollment,
)
from app.modules.guest.api_15_courses_enrollment_status.validate import (
    validate_enrollment_status_request,
)
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


# API #15 courses_enrollment_status
def get_enrollment_status(
    *,
    course_id: int,
    authorization: str | None = None,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Check enrollment status for a course."""

    validation = validate_enrollment_status_request(
        course_id=course_id,
        authorization=authorization,
        trace_id=trace_id,
    )
    if isinstance(validation, JSONResponse):
        return validation
    valid_course_id, user_id = validation

    try:
        course = find_course_by_id(db, course_id=valid_course_id)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Course lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if course is None:
        return _not_found_error(trace_id)

    try:
        enrollment_row = find_enrollment(db, course_id=course_id, user_id=user_id)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Enrollment lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if enrollment_row is None:
        return _not_found_error(trace_id)

    try:
        data = EnrollmentStatusResponse.model_validate(enrollment_row)
    except ValidationError:
        logger.exception("Enrollment mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Enrollment status retrieved.",
        trace_id=trace_id,
        data=data.model_dump(mode="json"),
    )


def _not_found_error(trace_id: str) -> JSONResponse:
    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Enrollment status not found.",
        trace_id=trace_id,
    )


def _internal_error(trace_id: str) -> JSONResponse:
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Enrollment status could not be retrieved.",
        trace_id=trace_id,
    )