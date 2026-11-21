"""Xác thực ADMIN và signed-int64 lesson_id cho API #85."""

from __future__ import annotations

import re

from app.core.responses import ErrorDetail, error_response
from app.modules.admin.api_85_admin_lesson_status.models import AdminLessonStatusRequest
from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1
_SIGNED_INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+\Z")


def validate_admin_lesson_status_request(
    authorization: str | None,
    lesson_id_value: str,
    lesson_data: AdminLessonStatusRequest,
    *,
    trace_id: str,
) -> tuple[int, int] | JSONResponse:
    """Yêu cầu ADMIN rồi validate path; trả lesson ID và actor user ID."""

    authentication = validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Lesson status could not be updated.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    actor_user_id, _roles = authentication

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

    return lesson_id, actor_user_id
