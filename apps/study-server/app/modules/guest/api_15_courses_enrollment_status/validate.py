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


def resolve_student_user_id(
    authorization: str | None,
    *,
    trace_id: str,
) -> int | JSONResponse:
    """Resolve the authenticated Student identity; never query enrollment by course alone."""

    if not authorization:
        return _not_found(trace_id)

    authentication = validate_current_user_request(
        authorization,
        role="STUDENT",
        trace_id=trace_id,
    )
    if isinstance(authentication, JSONResponse):
        logger.debug("Enrollment identity could not be resolved; trace_id=%s", trace_id)
        return _not_found(trace_id)

    return authentication[0]


def _not_found(trace_id: str) -> JSONResponse:
    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Enrollment status not found.",
        trace_id=trace_id,
    )
