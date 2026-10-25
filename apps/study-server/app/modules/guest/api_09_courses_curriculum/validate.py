"""Kiểm tra và chuẩn hóa dữ liệu đầu vào cho API #9 curriculum."""

from __future__ import annotations

from app.core.responses import error_response
from app.utils.validate import parse_integer
from starlette.responses import JSONResponse


def validate_course_id(
    course_id_raw: str | int,
    *,
    trace_id: str,
) -> int | JSONResponse:
    """Kiểm tra và chuyển đổi course_id từ path parameter thành số nguyên.

    Nếu giá trị không hợp lệ hoặc không thể chuyển đổi thành int, trả về error_response
    với mã HTTP 404 và business code DESIGN_RESOURCE_NOT_FOUND theo DD #09.
    """
    parsed_course_id = parse_integer(course_id_raw)
    if parsed_course_id is None:
        return _course_not_found_error(trace_id)
    return parsed_course_id


def parse_course_id(
    course_id_raw: str | int,
    *,
    trace_id: str,
) -> int | JSONResponse:
    """Hàm tương thích hỗ trợ gọi parse_course_id."""
    return validate_course_id(course_id_raw, trace_id=trace_id)


def _course_not_found_error(trace_id: str) -> JSONResponse:
    """Tạo phản hồi 404 chuẩn khi course_id không hợp lệ hoặc không tìm thấy."""
    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Published course not found.",
        trace_id=trace_id,
    )
