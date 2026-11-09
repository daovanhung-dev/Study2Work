"""Kiểm tra và chuẩn hóa dữ liệu đầu vào cho API #28."""

from __future__ import annotations

from app.core.responses import error_response
from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse

MAX_INT64 = 9_223_372_036_854_775_807


def validate_quiz_id(quiz_id_raw: str | int, *, trace_id: str) -> int | JSONResponse:
    """Kiểm tra và chuyển đổi quiz_id từ path parameter thành số nguyên int64 dương."""
    try:
        parsed_id = int(quiz_id_raw)
    except (TypeError, ValueError):
        return quiz_not_found(trace_id, message="Quiz not found")

    if parsed_id <= 0 or parsed_id > MAX_INT64:
        return quiz_not_found(trace_id, message="Quiz not found")

    return parsed_id


def validate_quiz_detail_request(
    *,
    authorization: str | None,
    quiz_id_raw: str | int,
    trace_id: str,
) -> tuple[int, int] | JSONResponse:
    """Xác thực Bearer token Student và kiểm tra tính hợp lệ của path quiz_id."""
    auth_result = validate_current_user_request(authorization, trace_id=trace_id)
    if isinstance(auth_result, JSONResponse):
        return auth_result
    user_id, _ = auth_result

    validated_quiz_id = validate_quiz_id(quiz_id_raw, trace_id=trace_id)
    if isinstance(validated_quiz_id, JSONResponse):
        return validated_quiz_id

    return user_id, validated_quiz_id


def quiz_not_found(
    trace_id: str,
    *,
    message: str = "Quiz not found",
) -> JSONResponse:
    """Tạo response lỗi 404 chuẩn khi không tìm thấy quiz."""
    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message=message,
        trace_id=trace_id,
    )

