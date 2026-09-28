import inspect

from app.core.responses import (
    INTERNAL_ERROR_MESSAGE,
    ApiError,
    ErrorDetail,
    _ApiError,
    error_response,
    success_response,
)
from app.core.trace import reset_trace_id, set_trace_id


def test_success_response_uses_canonical_envelope() -> None:
    """Kiểm tra success_response trả đủ sáu khóa chuẩn, giữ data/meta được cung cấp và gắn trace ID
    tương ứng."""
    response = success_response(
        business_code="COURSE_LOADED",
        message="Loaded",
        trace_id="trace-id",
        data={"id": "course-1"},
        meta={"page": 1},
    )

    assert response == {
        "success": True,
        "businessCode": "COURSE_LOADED",
        "message": "Loaded",
        "data": {"id": "course-1"},
        "meta": {"page": 1},
        "traceId": "trace-id",
    }


def test_success_response_defaults_data_and_meta() -> None:
    """Kiểm tra success_response dùng data=None và meta rỗng khi caller bỏ hai tham số tùy chọn."""
    response = success_response(
        business_code="RESOURCE_LOADED",
        message="Loaded",
        trace_id="trace-id",
    )

    assert response == {
        "success": True,
        "businessCode": "RESOURCE_LOADED",
        "message": "Loaded",
        "data": None,
        "meta": {},
        "traceId": "trace-id",
    }


def test_error_response_puts_field_errors_in_canonical_meta() -> None:
    """Kiểm tra error_response đặt danh sách ErrorDetail đã tuần tự hóa dưới meta.fieldErrors mà
    vẫn giữ envelope lỗi chuẩn."""
    error = ApiError(
        status_code=422,
        business_code="VALIDATION_ERROR",
        message="Invalid",
        trace_id="trace-id",
        data={"source": "query"},
        meta={"page": 1},
        errors=[
            ErrorDetail(field="email", code="INVALID_EMAIL", message="Invalid email"),
        ],
    )
    response = error_response(error)

    assert response["success"] is False
    assert response["businessCode"] == "VALIDATION_ERROR"
    assert response["message"] == "Invalid"
    assert response["data"] == {"source": "query"}
    assert response["traceId"] == "trace-id"
    assert response["meta"] == {
        "page": 1,
        "fieldErrors": [
            {"field": "email", "code": "INVALID_EMAIL", "message": "Invalid email"},
        ],
    }
    assert "errors" not in response


def test_api_error_is_a_factory_for_private_exception_instances() -> None:
    """Kiểm tra ApiError là function factory và mỗi lần gọi tạo instance exception nội bộ
    _ApiError."""
    error = ApiError(
        status_code=409,
        business_code="RESOURCE_CONFLICT",
        message="Conflict",
        trace_id="trace-id",
    )

    assert inspect.isfunction(ApiError)
    assert isinstance(error, _ApiError)
    assert error.status_code == 409
    assert error.business_code == "RESOURCE_CONFLICT"
    assert error.message == "Conflict"
    assert error.trace_id == "trace-id"


def test_internal_api_error_uses_current_trace_and_safe_defaults() -> None:
    """Kiểm tra ApiError không tham số dùng HTTP 500, business code/message mặc định an toàn và lấy
    trace ID từ ContextVar hiện tại."""
    trace_id = "00000000-0000-0000-0000-000000000001"
    token = set_trace_id(trace_id)
    try:
        error = ApiError()
    finally:
        reset_trace_id(token)

    assert error.status_code == 500
    assert error.business_code == "INTERNAL_SERVER_ERROR"
    assert error.message == INTERNAL_ERROR_MESSAGE
    assert error.trace_id == trace_id


def test_internal_api_error_generates_trace_without_request_context() -> None:
    """Kiểm tra ApiError vẫn tạo trace ID hợp lệ khi không có Request hay ContextVar trace đang
    hoạt động."""
    error = ApiError()

    assert error.trace_id
    assert len(error.trace_id) == 36
