"""Kiểm tra và chuẩn hóa dữ liệu đầu vào cho API #27."""

from __future__ import annotations

from app.core.responses import error_response
from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse

MAX_INT64 = 9_223_372_036_854_775_807


def validate_lesson_id(lesson_id_raw: str | int, *, trace_id: str) -> int | JSONResponse:
    """Kiểm tra và chuyển đổi lesson_id từ path parameter thành số nguyên int64 dương."""
    try:
        parsed_id = int(lesson_id_raw)
    except (TypeError, ValueError):
        return lesson_not_found(trace_id, message="Current lesson not found")

    if parsed_id <= 0 or parsed_id > MAX_INT64:
        return lesson_not_found(trace_id, message="Current lesson not found")

    return parsed_id


def validate_next_lesson_request(
    *,
    authorization: str | None,
    lesson_id_raw: str | int,
    trace_id: str,
) -> tuple[int, int] | JSONResponse:
    """Xác thực Bearer token Student và kiểm tra tính hợp lệ của path lesson_id."""
    auth_result = validate_current_user_request(authorization, trace_id=trace_id)
    if isinstance(auth_result, JSONResponse):
        return auth_result
    user_id, _ = auth_result

    validated_lesson_id = validate_lesson_id(lesson_id_raw, trace_id=trace_id)
    if isinstance(validated_lesson_id, JSONResponse):
        return validated_lesson_id

    return user_id, validated_lesson_id


def lesson_not_found(
    trace_id: str,
    *,
    message: str = "Lesson not found",
) -> JSONResponse:
    """Tạo response lỗi 404 chuẩn khi không tìm thấy bài học hiện tại hoặc bài học tiếp theo."""
    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message=message,
        trace_id=trace_id,
    )
