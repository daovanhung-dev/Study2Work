"""Chuẩn hóa và kiểm tra dữ liệu đầu vào cho API #11 lấy tài nguyên khóa học."""

from __future__ import annotations

from app.core.responses import error_response
from starlette.responses import JSONResponse


def validate_course_id(
    course_id: int,
    *,
    trace_id: str,
) -> int | JSONResponse:
    """Xác thực course_id từ path segment đảm bảo là số nguyên dương hợp lệ."""

    if not isinstance(course_id, int) or course_id <= 0:
        return error_response(
            status_code=404,
            business_code="DESIGN_RESOURCE_NOT_FOUND",
            message="Published course or resource not found.",
            trace_id=trace_id,
        )
    return course_id
