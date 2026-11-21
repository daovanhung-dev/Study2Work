"""Xác thực ADMIN, path int64 và target status candidate của API #76."""

from __future__ import annotations

import re

from app.core.responses import ErrorDetail, error_response
from app.modules.admin.api_76_admin_course_status.models import AdminCourseStatusRequest
from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1
_SIGNED_INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+\Z")


def parse_admin_course_status_id(value: str) -> int | None:
    """Trả signed-int64 course ID hoặc None khi path sai định dạng/vượt miền."""

    if len(value) > 20 or _SIGNED_INTEGER_PATTERN.fullmatch(value) is None:
        return None
    course_id = int(value)
    if not INT64_MIN <= course_id <= INT64_MAX:
        return None
    return course_id


def validate_admin_course_status_request(
    authorization: str | None,
    course_id_value: str,
    course_data: AdminCourseStatusRequest,
    *,
    trace_id: str,
) -> tuple[int, int] | JSONResponse:
    """Yêu cầu ADMIN rồi validate path; trả course ID và actor user ID."""

    authentication = validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Course status could not be updated.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    actor_user_id, _roles = authentication

    course_id = parse_admin_course_status_id(course_id_value)
    if course_id is None:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Dữ liệu đầu vào không hợp lệ.",
            trace_id=trace_id,
            errors=[
                ErrorDetail(
                    field="course_id",
                    code="INT_PARSING",
                    message="Input should be a valid signed 64-bit integer",
                )
            ],
        )

    return course_id, actor_user_id
