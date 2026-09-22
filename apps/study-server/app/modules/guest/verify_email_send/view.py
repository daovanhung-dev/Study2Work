from __future__ import annotations

import logging
from typing import Any

from app.core.responses import ApiError, success_response
from app.modules.guest.verify_email_send.models import VerifyEmailSendRequest
from app.service.email.provider import VerificationEmailProvider

logger = logging.getLogger(__name__)


def send_verification_email(
    *,
    user_data: VerifyEmailSendRequest,
    provider: VerificationEmailProvider,
    trace_id: str,
) -> dict[str, Any]:
    """Accept a verification-email dispatch through the provider boundary."""

    try:
        dispatch_result = provider.dispatch(
            user_id=user_data.user_id,
            email=str(user_data.email),
            trace_id=trace_id,
        )
    except Exception as exc:
        logger.error(
            "Verification email dispatch failed; trace_id=%s user_id=%s",
            trace_id,
            user_data.user_id,
        )
        raise ApiError(
            status_code=500,
            business_code="DESIGN_INTERNAL_ERROR",
            message="Không thể chấp nhận yêu cầu gửi email xác thực.",
            trace_id=trace_id,
        ) from exc

    data: dict[str, str] = {"status": dispatch_result.status}
    if dispatch_result.reason is not None:
        data["reason"] = dispatch_result.reason

    return success_response(
        business_code="DESIGN_OPERATION_ACCEPTED",
        message="Yêu cầu gửi email xác thực đã được chấp nhận.",
        trace_id=trace_id,
        data=data,
    )
