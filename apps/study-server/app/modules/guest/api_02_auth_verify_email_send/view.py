from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.responses import error_response, success_response
from app.modules.guest.api_02_auth_verify_email_send.models import VerifyEmailSendRequest
from app.modules.guest.api_02_auth_verify_email_send.validate import validate_verify_email_request
from app.service.email.provider import VerificationEmailProvider
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


# API #02 auth_verify_email_send
def send_verification_email(
    *,
    user_data: VerifyEmailSendRequest,
    raw_payload: Mapping[str, Any],
    provider: VerificationEmailProvider,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Gửi yêu cầu user ID, email và trace ID qua VerificationEmailProvider mà không mở database
    session. Lỗi provider được log nội bộ rồi chuyển thành error_response an toàn; kết quả chấp nhận
    được ánh xạ thành business response, kèm reason nếu provider có trả."""

    validated_user_data = validate_verify_email_request(
        user_data,
        raw_payload=raw_payload,
        trace_id=trace_id,
    )
    if isinstance(validated_user_data, JSONResponse):
        return validated_user_data
    user_data = validated_user_data

    try:
        dispatch_result = provider.dispatch(
            user_id=user_data.user_id,
            email=str(user_data.email),
            trace_id=trace_id,
        )
    except Exception:
        logger.error(
            "Verification email dispatch failed; trace_id=%s user_id=%s",
            trace_id,
            user_data.user_id,
        )
        return error_response(
            status_code=500,
            business_code="DESIGN_INTERNAL_ERROR",
            message="Không thể chấp nhận yêu cầu gửi email xác thực.",
            trace_id=trace_id,
        )

    data: dict[str, str] = {"status": dispatch_result.status}
    if dispatch_result.reason is not None:
        data["reason"] = dispatch_result.reason

    return success_response(
        business_code="DESIGN_OPERATION_ACCEPTED",
        message="Yêu cầu gửi email xác thực đã được chấp nhận.",
        trace_id=trace_id,
        data=data,
    )
