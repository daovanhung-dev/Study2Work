"""Xác thực Admin và parse Quiz ID cho API #91."""

from __future__ import annotations

import re

from app.core.responses import error_response
from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse

MAX_INT64 = 2**63 - 1
_POSITIVE_INTEGER_PATTERN = re.compile(r"[0-9]+\Z")


def parse_admin_quiz_statistics_id(value: str) -> int | None:
    """Parse Quiz ID dương thuộc miền signed-int64 từ raw path text."""

    # Giới hạn độ dài và chỉ nhận chữ số trước khi chuyển đổi kiểu.
    if len(value) > 19 or _POSITIVE_INTEGER_PATTERN.fullmatch(value) is None:
        return None
    quiz_id = int(value)
    return quiz_id if 1 <= quiz_id <= MAX_INT64 else None


def validate_admin_quiz_statistics_request(
    authorization: str | None,
    quiz_id_value: str,
    *,
    trace_id: str,
) -> int | JSONResponse:
    """Yêu cầu role ADMIN trước khi parse path hoặc truy cập database."""

    # Dùng guard chung để giữ xử lý Bearer/JWT và role nhất quán toàn Study.
    authentication = validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Quiz statistics could not be retrieved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication

    # Ánh xạ path sai về 404 để không thêm business code ngoài catalog #91.
    quiz_id = parse_admin_quiz_statistics_id(quiz_id_value)
    if quiz_id is None:
        return error_response(
            status_code=404,
            business_code="DESIGN_RESOURCE_NOT_FOUND",
            message="Quiz not found.",
            trace_id=trace_id,
        )
    return quiz_id
