"""Xác thực truy cập Mentor và query fields của API #46."""

from __future__ import annotations

import app.utils.auth as auth_utils
from app.core.responses import ErrorDetail, error_response
from app.modules.mentor.api_46_mentor_courses.models import MentorCourseQuery
from starlette.responses import JSONResponse

COURSE_STATUS_VALUES = frozenset({"DRAFT", "PUBLISHED"})


def validate_mentor_request(
    authorization: str | None,
    *,
    trace_id: str,
) -> int | JSONResponse:
    """Dùng auth guard chung với role MENTOR và trả mentor ID trước khi query."""
    authentication = auth_utils.validate_current_user_request(
        authorization,
        role="MENTOR",
        trace_id=trace_id,
        internal_error_message="Mentor courses could not be retrieved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    mentor_id, _roles = authentication
    return mentor_id


def validate_mentor_courses_query(
    mentor_query: MentorCourseQuery,
    *,
    trace_id: str,
) -> MentorCourseQuery | JSONResponse:
    """Kiểm tra status enum và giới hạn pagination theo pattern danh sách course API #6."""
    errors: list[ErrorDetail] = []
    if mentor_query.status is not None and mentor_query.status not in COURSE_STATUS_VALUES:
        errors.append(
            ErrorDetail(
                field="status",
                code="VALUE_ERROR",
                message="Input should be 'DRAFT' or 'PUBLISHED'",
            )
        )
    if mentor_query.page < 1:
        errors.append(
            ErrorDetail(
                field="page",
                code="GREATER_THAN_EQUAL",
                message="Input should be greater than or equal to 1",
            )
        )
    if mentor_query.size < 1:
        errors.append(
            ErrorDetail(
                field="size",
                code="GREATER_THAN_EQUAL",
                message="Input should be greater than or equal to 1",
            )
        )
    elif mentor_query.size > 100:
        errors.append(
            ErrorDetail(
                field="size",
                code="LESS_THAN_EQUAL",
                message="Input should be less than or equal to 100",
            )
        )

    if errors:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Dữ liệu đầu vào không hợp lệ.",
            trace_id=trace_id,
            errors=errors,
        )
    return mentor_query
