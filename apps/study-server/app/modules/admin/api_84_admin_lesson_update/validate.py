"""Xác thực Admin và signed-int64 lesson_id theo fallback API #84."""

from __future__ import annotations

import re

from app.core.responses import ErrorDetail, error_response
from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1
_SIGNED_INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+\Z")


def validate_admin_lesson_update_request(
    authorization: str | None,
    lesson_id_value: str,
    *,
    trace_id: str,
) -> int | JSONResponse:
    """Yêu cầu ADMIN rồi parse lesson_id; lỗi path dùng 422 của catalog PUT."""

    authentication = validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Lesson could not be updated.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication

    _admin_id, _roles = authentication
    if (
        len(lesson_id_value) > 20
        or _SIGNED_INTEGER_PATTERN.fullmatch(lesson_id_value) is None
    ):
        lesson_id = None
    else:
        parsed_id = int(lesson_id_value)
        lesson_id = parsed_id if INT64_MIN <= parsed_id <= INT64_MAX else None

    if lesson_id is None:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Dữ liệu đầu vào không hợp lệ.",
            trace_id=trace_id,
            errors=[
                ErrorDetail(
                    field="lesson_id",
                    code="INT_PARSING",
                    message="Input should be a valid signed 64-bit integer",
                )
            ],
        )

    return lesson_id
