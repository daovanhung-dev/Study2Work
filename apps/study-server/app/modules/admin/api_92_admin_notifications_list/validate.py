"""Xác thực Admin và chuẩn hóa raw query của API #92."""

from __future__ import annotations

import re

from app.core.responses import ErrorDetail, error_response
from app.modules.admin.api_92_admin_notifications_list.models import (
    AdminNotificationsQuery,
)
from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse

INT32_MIN = -(2**31)
INT32_MAX = 2**31 - 1
_SIGNED_INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+\Z")


def _parse_int32(value: str) -> int | None:
    """Parse page text thành số nguyên signed-int32 hoặc trả None nếu sai miền."""

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


def _invalid_page(trace_id: str, *, message: str) -> JSONResponse:
    """Dựng lỗi validation cục bộ khi page không phải số nguyên dương int32."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Dữ liệu đầu vào không hợp lệ.",
        trace_id=trace_id,
        errors=[
            ErrorDetail(
                field="page",
                code="INT_PARSING",
                message=message,
            )
        ],
    )


def validate_admin_notifications_request(
    authorization: str | None,
    *,
    status_value: str | None,
    channel_value: str | None,
    page_value: str | None,
    trace_id: str,
) -> AdminNotificationsQuery | JSONResponse:
    """Yêu cầu role ADMIN trước khi parse page và giữ nguyên filter text."""

    # Xác thực Bearer/JWT và role ADMIN trước mọi kiểm tra query hoặc database.
    authentication = validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Notifications could not be retrieved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication

    # Áp dụng page mặc định theo đề xuất danh sách và kiểm tra miền int32 dương.
    page = 1 if page_value is None else _parse_int32(page_value)
    if page is None:
        return _invalid_page(
            trace_id,
            message="Input should be a valid signed 32-bit integer",
        )
    if page < 1:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Dữ liệu đầu vào không hợp lệ.",
            trace_id=trace_id,
            errors=[
                ErrorDetail(
                    field="page",
                    code="GREATER_THAN_EQUAL",
                    message="Input should be greater than or equal to 1",
                )
            ],
        )

    # Không chuẩn hóa enum chưa được khai báo; DB so sánh đúng chuỗi nhận được.
    return AdminNotificationsQuery(
        status=status_value,
        channel=channel_value,
        page=page,
    )
