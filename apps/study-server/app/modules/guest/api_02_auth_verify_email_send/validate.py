"""Kiểm tra dữ liệu yêu cầu gửi email xác minh API #2."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.core.responses import ErrorDetail, error_response
from app.modules.guest.api_02_auth_verify_email_send.models import VerifyEmailSendRequest
from app.utils.validate import normalize_email
from starlette.responses import JSONResponse


def validate_verify_email_request(
    user_data: VerifyEmailSendRequest,
    *,
    raw_payload: Mapping[str, Any],
    trace_id: str,
) -> VerifyEmailSendRequest | JSONResponse:
    """Kiểm tra user_id nguyên nghiêm ngặt và email.

    Trả dữ liệu đã chuẩn hóa hoặc response lỗi HTTP 422.
    """

    errors: list[ErrorDetail] = []
    if type(raw_payload.get("user_id")) is not int:
        errors.append(
            ErrorDetail(
                field="user_id",
                code="INT_TYPE",
                message="Input should be a valid integer.",
            )
        )

    email = user_data.email
    try:
        email = normalize_email(email)
    except ValueError as exc:
        errors.append(ErrorDetail(field="email", code="VALUE_ERROR", message=str(exc)))

    if errors:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Dữ liệu đầu vào không hợp lệ.",
            trace_id=trace_id,
            errors=errors,
        )
    return user_data.model_copy(update={"email": email})
