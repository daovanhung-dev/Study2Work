"""Kiểm tra và chuẩn hóa dữ liệu đầu vào cho API #30."""

from __future__ import annotations

from app.core.responses import error_response
from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse

MAX_INT64 = 9_223_372_036_854_775_807


def validate_attempt_id(
    attempt_id_raw: str | int,
    *,
    trace_id: str,
) -> int | JSONResponse:
    """Kiểm tra và chuyển đổi attempt_id từ path parameter thành số nguyên int64 dương."""
    try:
        parsed_id = int(attempt_id_raw)
    except (TypeError, ValueError):
        return validation_error(trace_id, message="Invalid attempt_id")

    if parsed_id <= 0 or parsed_id > MAX_INT64:
        return validation_error(trace_id, message="Invalid attempt_id")

    return parsed_id


def validate_question_id(
    question_id_raw: int,
    *,
    trace_id: str,
) -> int | JSONResponse:
    """Kiểm tra question_id trong request body là số nguyên int64 dương hợp lệ."""
    if not isinstance(question_id_raw, int) or question_id_raw <= 0 or question_id_raw > MAX_INT64:
        return validation_error(trace_id, message="Invalid question_id")

    return question_id_raw


def validate_save_answer_request(
    *,
    authorization: str | None,
    attempt_id_raw: str | int,
    question_id_raw: int,
    trace_id: str,
) -> tuple[int, int, int] | JSONResponse:
    """Xác thực Bearer token Student và kiểm tra tính hợp lệ của path và body ID."""
    auth_result = validate_current_user_request(authorization, trace_id=trace_id)
    if isinstance(auth_result, JSONResponse):
        return auth_result
    user_id, _ = auth_result

    validated_attempt_id = validate_attempt_id(attempt_id_raw, trace_id=trace_id)
    if isinstance(validated_attempt_id, JSONResponse):
        return validated_attempt_id

    validated_question_id = validate_question_id(question_id_raw, trace_id=trace_id)
    if isinstance(validated_question_id, JSONResponse):
        return validated_question_id

    return user_id, validated_attempt_id, validated_question_id


def validation_error(
    trace_id: str,
    *,
    message: str = "Validation failed",
) -> JSONResponse:
    """Tạo response lỗi 422 chuẩn khi tham số path hoặc body không hợp lệ."""
    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message=message,
        trace_id=trace_id,
    )


def resource_not_found(
    trace_id: str,
    *,
    message: str = "Resource not found",
) -> JSONResponse:
    """Tạo response lỗi 404 chuẩn khi không tìm thấy attempt hoặc question."""
    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message=message,
        trace_id=trace_id,
    )


def access_denied(
    trace_id: str,
    *,
    message: str = "Access denied",
) -> JSONResponse:
    """Tạo response lỗi 403 chuẩn khi quyền truy cập bị từ chối."""
    return error_response(
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message=message,
        trace_id=trace_id,
    )

