"""Business orchestration for the course enrollment status endpoint."""

from __future__ import annotations

import logging
from typing import Any

from app.core.responses import ApiError, success_response
from app.core.security import decode_access_token
from app.modules.guest.api_15_courses_enrollment_status.models import (
    EnrollmentStatusResponse,
)
from app.modules.guest.api_15_courses_enrollment_status.query import (
    find_course_by_id,
    find_enrollment,
)
from app.utils.validate import extract_bearer_token, validate_access_claims
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


# API #15 courses_enrollment_status
def get_enrollment_status(
    *,
    course_id: int,
    authorization: str | None = None,
    db: Session,
    trace_id: str,
) -> dict[str, Any]:
    """Check enrollment status for a course."""

    user_id: int | None = None
    if authorization:
        try:
            token = extract_bearer_token(authorization)
            claims = decode_access_token(token)
            user_id, _ = validate_access_claims(claims)
        except ApiError:
            logger.debug("Optional token validation failed; trace_id=%s", trace_id)

    try:
        course = find_course_by_id(db, course_id=course_id)
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Course lookup failed; trace_id=%s", trace_id)
        raise _internal_error(trace_id) from exc

    if course is None:
        raise _not_found_error(trace_id)

    try:
        enrollment_row = find_enrollment(db, course_id=course_id, user_id=user_id)
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Enrollment lookup failed; trace_id=%s", trace_id)
        raise _internal_error(trace_id) from exc

    if enrollment_row is None:
        raise _not_found_error(trace_id)

    try:
        data = EnrollmentStatusResponse.model_validate(enrollment_row)
    except ValidationError as exc:
        logger.exception("Enrollment mapping failed; trace_id=%s", trace_id)
        raise _internal_error(trace_id) from exc

    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Enrollment status retrieved.",
        trace_id=trace_id,
        data=data.model_dump(mode="json"),
    )


def _not_found_error(trace_id: str) -> ApiError:
    return ApiError(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Enrollment status not found.",
        trace_id=trace_id,
    )


def _internal_error(trace_id: str) -> ApiError:
    return ApiError(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Enrollment status could not be retrieved.",
        trace_id=trace_id,
    )