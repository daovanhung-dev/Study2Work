"""Xác thực Admin và raw path int64 cho API #77."""

from __future__ import annotations

import re

from app.core.responses import ErrorDetail, error_response
from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1
_SIGNED_INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+\Z")


def parse_admin_course_delete_id(value: str) -> int | None:
    """Trả course ID signed-int64 hoặc None nếu raw path sai format/range."""

    if len(value) > 20 or _SIGNED_INTEGER_PATTERN.fullmatch(value) is None:
        return None
    course_id = int(value)
    if not INT64_MIN <= course_id <= INT64_MAX:
        return None
    return course_id


def validate_admin_course_delete_request(
    authorization: str | None,
    course_id_value: str,
    *,
    trace_id: str,
) -> int | JSONResponse:
    """Yêu cầu ADMIN trước khi parse course ID hoặc truy cập database."""

    authentication = validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Course could not be deleted.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication

    course_id = parse_admin_course_delete_id(course_id_value)
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
    return course_id
