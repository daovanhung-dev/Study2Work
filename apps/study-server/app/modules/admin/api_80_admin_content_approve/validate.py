"""Xác thực ADMIN và path signed-int64 của API #80."""

from __future__ import annotations

import re

from app.core.responses import ErrorDetail, error_response
from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1
_SIGNED_INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+\Z")


def parse_admin_content_approval_id(value: str) -> int | None:
    """Trả Content ID signed-int64 hoặc None nếu path sai format/vượt miền."""

    if len(value) > 20 or _SIGNED_INTEGER_PATTERN.fullmatch(value) is None:
        return None
    content_id = int(value)
    if not INT64_MIN <= content_id <= INT64_MAX:
        return None
    return content_id


def validate_admin_content_approval_request(
    authorization: str | None,
    content_id_value: str,
    *,
    trace_id: str,
) -> tuple[int, int] | JSONResponse:
    """Yêu cầu role ADMIN trước path parse; trả Content ID và actor user ID."""

    authentication = validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Content approval could not be completed.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    actor_user_id, _roles = authentication

    content_id = parse_admin_content_approval_id(content_id_value)
    if content_id is None:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Dữ liệu đầu vào không hợp lệ.",
            trace_id=trace_id,
            errors=[
                ErrorDetail(
                    field="content_id",
                    code="INT_PARSING",
                    message="Input should be a valid signed 64-bit integer",
                )
            ],
        )

    return content_id, actor_user_id
