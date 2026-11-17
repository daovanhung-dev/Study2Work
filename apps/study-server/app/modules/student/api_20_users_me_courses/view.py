from __future__ import annotations

import logging
import math
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.shared.course_catalog.constants import DEFAULT_SIZE
from app.modules.student.api_20_users_me_courses.models import CourseSummary, CourseSummaryPage, Pagination
from app.modules.student.api_20_users_me_courses.query import COUNT_USER_COURSES, LIST_USER_COURSES
from app.modules.student.api_20_users_me_courses.validate import validate_courses_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def get_user_courses(*, authorization: str | None, page_raw: str | None, status_filter: str | None, db: Session, trace_id: str) -> dict[str, Any] | JSONResponse:
    validated = validate_courses_request(authorization, page_raw, status_filter, trace_id=trace_id)
    if isinstance(validated, JSONResponse):
        return validated
    user_id, page, status_value = validated
    try:
        params = {"user_id": user_id, "status": status_value}
        count = query_one(db, COUNT_USER_COURSES, params)
        total = int((count or {}).get("total", 0))
        rows = query_many(db, LIST_USER_COURSES, {**params, "limit": DEFAULT_SIZE, "offset": (page - 1) * DEFAULT_SIZE})
        result = CourseSummaryPage(
            items=[CourseSummary.model_validate(row) for row in rows],
            pagination=Pagination(page=page, size=DEFAULT_SIZE, total=total, total_pages=math.ceil(total / DEFAULT_SIZE) if total else 0),
        )
    except (SQLAlchemyError, ValidationError, TypeError):
        db.rollback()
        logger.exception("Course list query failed; trace_id=%s", trace_id)
        return error_response(status_code=500, business_code="DESIGN_INTERNAL_ERROR", message="Courses could not be retrieved.", trace_id=trace_id)
    return success_response(business_code="DESIGN_RESOURCE_RETRIEVED", message="Courses retrieved.", trace_id=trace_id, data=result.model_dump(mode="json"))
