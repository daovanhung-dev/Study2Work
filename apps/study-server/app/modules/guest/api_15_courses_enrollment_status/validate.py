"""Kiểm tra và chuẩn hóa dữ liệu đầu vào cho API #15 kiểm tra trạng thái ghi danh."""

from __future__ import annotations

import logging

from app.core.responses import error_response
from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def validate_course_id(
    course_id: int,
    *,
    trace_id: str,
) -> int | JSONResponse:
    """Xác thực course_id nhận từ path đảm bảo là số nguyên dương hợp lệ."""

    if not isinstance(course_id, int) or course_id <= 0:
        return error_response(
            status_code=404,
            business_code="DESIGN_RESOURCE_NOT_FOUND",
            message="Enrollment status not found.",
            trace_id=trace_id,
        )
    return course_id


def resolve_optional_user_id(
    authorization: str | None,
    *,
    trace_id: str,
) -> int | None:
    """Trích xuất và giải mã user_id từ header Authorization nếu được cung cấp."""

    if not authorization:
        return None

    authentication = validate_current_user_request(
        authorization,
        trace_id=trace_id,
    )
    if isinstance(authentication, JSONResponse):
        logger.debug("Optional token validation ignored; trace_id=%s", trace_id)
        return None

    user_id, _roles = authentication
    return user_id
