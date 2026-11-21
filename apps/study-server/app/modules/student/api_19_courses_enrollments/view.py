from __future__ import annotations

import logging
from decimal import Decimal
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.student.api_19_courses_enrollments.models import Enrollment
from app.modules.student.api_19_courses_enrollments.query import (
    FIND_ACTIVE_ENROLLMENT,
    FIND_PAID_ORDER,
    INSERT_ENROLLMENT,
    INSERT_INITIAL_LESSON_PROGRESS,
    LOCK_ENROLLMENT_COURSE,
)
from app.modules.student.api_19_courses_enrollments.validate import validate_enrollment_request
from pydantic import ValidationError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def create_enrollment(*, authorization: str | None, course_id_raw: str, payload: Any, db: Session, trace_id: str) -> dict[str, Any] | JSONResponse:
    validated = validate_enrollment_request(authorization, course_id_raw, payload, trace_id=trace_id)
    if isinstance(validated, JSONResponse):
        return validated
    user_id, course_id = validated
    try:
        course = query_one(db, LOCK_ENROLLMENT_COURSE, {"course_id": course_id})
        if course is None or str(course.get("status", "")).upper() != "PUBLISHED":
            db.rollback()
            return error_response(status_code=404, business_code="DESIGN_RESOURCE_NOT_FOUND", message="Course not found.", trace_id=trace_id)
        if query_one(db, FIND_ACTIVE_ENROLLMENT, {"user_id": user_id, "course_id": course_id}) is not None:
            db.rollback()
            return error_response(status_code=409, business_code="DESIGN_STATE_CONFLICT", message="Student is already enrolled.", trace_id=trace_id)
        if course.get("price") is not None and Decimal(str(course["price"])) > 0:
            paid_order = query_one(db, FIND_PAID_ORDER, {"user_id": user_id, "course_id": course_id})
            if paid_order is None:
                db.rollback()
                return error_response(status_code=409, business_code="DESIGN_STATE_CONFLICT", message="A paid Order is required.", trace_id=trace_id)
        enrollment_row = query_one(db, INSERT_ENROLLMENT, {"user_id": user_id, "course_id": course_id})
        if enrollment_row is None:
            db.rollback()
            return _internal_error(trace_id)
        db.execute(text(INSERT_INITIAL_LESSON_PROGRESS), {"user_id": user_id, "course_id": course_id})
        enrollment = Enrollment.model_validate(enrollment_row)
        db.commit()
    except (SQLAlchemyError, ValidationError, TypeError):
        db.rollback()
        logger.exception("Create enrollment failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    return success_response(business_code="DESIGN_RESOURCE_CREATED", message="Enrollment created.", trace_id=trace_id, data=enrollment.model_dump(mode="json"))


def _internal_error(trace_id: str) -> JSONResponse:
    return error_response(status_code=500, business_code="DESIGN_INTERNAL_ERROR", message="Enrollment could not be created.", trace_id=trace_id)
