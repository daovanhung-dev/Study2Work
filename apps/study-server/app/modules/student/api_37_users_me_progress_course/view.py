from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.student.api_37_users_me_progress_course.models import CourseProgress
from app.modules.student.api_37_users_me_progress_course.query import COURSE_LESSON_PROGRESS
from app.modules.student.api_37_users_me_progress_course.validate import validate_course_progress_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def get_course_progress(*, authorization: str | None, course_id_raw: str, db: Session, trace_id: str) -> dict[str, Any] | JSONResponse:
    validated = validate_course_progress_request(authorization, course_id_raw, trace_id=trace_id)
    if isinstance(validated, JSONResponse):
        return validated
    user_id, course_id = validated
    try:
        row = query_one(db, COURSE_LESSON_PROGRESS, {"course_id": course_id, "user_id": user_id})
        if row is None:
            return error_response(status_code=404, business_code="DESIGN_RESOURCE_NOT_FOUND", message="Course progress not found.", trace_id=trace_id)
        completed = int(row["completed_lessons"])
        total = int(row["total_lessons"])
        progress = int(completed * 100 / total) if total else 0
        data = CourseProgress(course_id=course_id, completed_lessons=completed, total_lessons=total, progress_percent=progress, has_content=total > 0)
    except (SQLAlchemyError, ValidationError, KeyError, TypeError):
        db.rollback()
        logger.exception("Course progress query failed; trace_id=%s", trace_id)
        return error_response(status_code=500, business_code="DESIGN_INTERNAL_ERROR", message="Course progress could not be retrieved.", trace_id=trace_id)
    return success_response(business_code="DESIGN_RESOURCE_RETRIEVED", message="Course progress retrieved.", trace_id=trace_id, data=data.model_dump(mode="json"))
