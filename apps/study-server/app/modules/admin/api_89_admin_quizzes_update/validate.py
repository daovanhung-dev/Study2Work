"""Xác thực quyền Admin, quiz ID và request proposal của API #89."""

from __future__ import annotations

import re

from app.core.responses import ErrorDetail, error_response
from app.modules.admin.api_88_admin_quizzes_create.models import CreateAdminQuizInput
from app.modules.admin.api_88_admin_quizzes_create.validate import (
    validate_create_admin_quiz_request,
)
from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse

MAX_INT64 = 2**63 - 1
_POSITIVE_INTEGER_PATTERN = re.compile(r"[0-9]+\Z")


def parse_admin_quiz_id(value: str) -> int | None:
    """Parse a positive signed-int64 Quiz ID without accepting non-decimal path text."""

    if len(value) > 19 or _POSITIVE_INTEGER_PATTERN.fullmatch(value) is None:
        return None
    quiz_id = int(value)
    return quiz_id if 1 <= quiz_id <= MAX_INT64 else None


def validate_admin_quiz_update_request(
    authorization: str | None,
    quiz_id_value: str,
    raw_body: bytes,
    *,
    trace_id: str,
) -> tuple[int, CreateAdminQuizInput] | JSONResponse:
    """Require ADMIN before parsing path/body and reuse the current #88 nested request proposal."""

    authentication = validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Quiz could not be updated.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication

    quiz_id = parse_admin_quiz_id(quiz_id_value)
    if quiz_id is None:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Dữ liệu đầu vào không hợp lệ.",
            trace_id=trace_id,
            errors=[
                ErrorDetail(
                    field="quiz_id",
                    code="INT_PARSING",
                    message="Input should be a positive signed 64-bit integer",
                )
            ],
        )

    request = validate_create_admin_quiz_request(raw_body, trace_id=trace_id)
    if isinstance(request, JSONResponse):
        return request
    return quiz_id, request
