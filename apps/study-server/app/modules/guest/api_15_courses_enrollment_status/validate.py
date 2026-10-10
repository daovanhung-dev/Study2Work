"""Kiểm tra và chuẩn hóa dữ liệu yêu cầu cho API #15 kiểm tra trạng thái enrollment."""

from __future__ import annotations

import logging

from app.core.responses import ErrorDetail, error_response
from app.core.security.access_token import decode_access_token
from app.utils.validate import extract_bearer_token, validate_access_claims
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def validate_enrollment_status_request(
    course_id: int,
    authorization: str | None,
    *,
    trace_id: str,
) -> tuple[int, int | None] | JSONResponse:
    """Kiểm tra course_id là số nguyên dương và giải mã tùy chọn token Bearer để lấy user_id."""

    if course_id <= 0:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Dữ liệu đầu vào không hợp lệ.",
            trace_id=trace_id,
            errors=[
                ErrorDetail(
                    field="course_id",
                    code="GREATER_THAN",
                    message="Input should be greater than 0",
                )
            ],
        )

    user_id: int | None = None
    if authorization:
        try:
            token = extract_bearer_token(authorization)
            claims = decode_access_token(token)
            if not isinstance(claims, JSONResponse):
                user_id, _ = validate_access_claims(claims)
        except (ValueError, Exception):
            logger.debug("Optional token validation failed; trace_id=%s", trace_id)

    return course_id, user_id

