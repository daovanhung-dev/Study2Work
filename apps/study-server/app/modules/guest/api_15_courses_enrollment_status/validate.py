"""Kiểm tra và chuẩn hóa dữ liệu đầu vào cho API #15 kiểm tra trạng thái ghi danh."""

from __future__ import annotations

import logging

from app.core.security.access_token import decode_access_token
from app.utils.validate import extract_bearer_token, validate_access_claims
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def validate_course_id(course_id: int) -> int:
    """Xác thực course_id nhận từ path đảm bảo là số nguyên hợp lệ."""

    if not isinstance(course_id, int):
        raise ValueError("course_id must be an integer.")
    return course_id


def resolve_optional_user_id(
    authorization: str | None,
    *,
    trace_id: str,
) -> int | None:
    """Trích xuất và giải mã user_id từ header Authorization nếu được cung cấp."""

    if not authorization:
        return None

    try:
        token = extract_bearer_token(authorization)
        claims = decode_access_token(token)
        if isinstance(claims, JSONResponse):
            return None
        user_id, _ = validate_access_claims(claims)
        return user_id
    except Exception:
        logger.debug("Optional token validation ignored; trace_id=%s", trace_id)
        return None
