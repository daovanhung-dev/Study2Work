"""Xác thực quyền Admin và query parameters cho API #97."""

from __future__ import annotations

import re

from app.core.responses import ErrorDetail, error_response
from app.modules.admin.api_97_admin_discussions_reported.models import (
    AdminReportedDiscussionsQuery,
)
from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse

INT32_MIN = -(2**31)
INT32_MAX = 2**31 - 1
_SIGNED_INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+\Z")


def _parse_int32(value: str) -> int | None:
    """Parse chuỗi thành signed-int32 mà không chuyển chuỗi quá lớn sang int."""

    if _SIGNED_INTEGER_PATTERN.fullmatch(value) is None:
        return None

    negative = value.startswith("-")
    digits = value.lstrip("+-").lstrip("0") or "0"
    if len(digits) > 10:
        return None

    parsed = int(digits)
    if negative:
        parsed = -parsed
    return parsed if INT32_MIN <= parsed <= INT32_MAX else None


def _invalid_page(trace_id: str, *, code: str, message: str) -> JSONResponse:
    """Dựng lỗi 422 DERIVED cho page không phải số nguyên dương int32."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Dữ liệu đầu vào không hợp lệ.",
        trace_id=trace_id,
        errors=[ErrorDetail(field="page", code=code, message=message)],
    )


def validate_admin_reported_discussions_request(
    authorization: str | None,
    *,
    reason_value: str | None,
    severity_value: str | None,
    page_value: str | None,
    trace_id: str,
) -> AdminReportedDiscussionsQuery | JSONResponse:
    """Yêu cầu role ADMIN trước khi parse page và giữ nguyên filter text."""

    # Xác thực JWT/Admin trước mọi kiểm tra query hoặc database.
    authentication = validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Reported discussions could not be retrieved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication

    # Áp dụng default page 1 và giới hạn dương trong miền signed-int32.
    page = 1 if page_value is None else _parse_int32(page_value)
    if page is None:
        return _invalid_page(
            trace_id,
            code="INT_PARSING",
            message="Input should be a valid signed 32-bit integer",
        )
    if page < 1:
        return _invalid_page(
            trace_id,
            code="GREATER_THAN_EQUAL",
            message="Input should be greater than or equal to 1",
        )

    # Không tự đặt taxonomy; hai filter được DB so sánh exact-match.
    return AdminReportedDiscussionsQuery(
        reason=reason_value,
        severity=severity_value,
        page=page,
    )
