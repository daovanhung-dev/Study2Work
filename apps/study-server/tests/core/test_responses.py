import json

from app.core.responses import INTERNAL_ERROR_MESSAGE, ApiError, ErrorDetail, success_response
from app.core.trace import reset_trace_id, set_trace_id
from starlette.responses import JSONResponse


def test_success_response_uses_canonical_envelope() -> None:
    """Xác nhận success_response trả đủ sáu khóa envelope chuẩn cùng data, meta và trace ID."""
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
    """Xác nhận success_response mặc định data là None và meta là object rỗng."""
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


def test_api_error_returns_json_response_with_canonical_envelope_and_field_errors() -> None:
    """Xác nhận ApiError trả JSONResponse trực tiếp và đặt lỗi trường dưới meta.fieldErrors."""
    response = ApiError(
        status_code=422,
        business_code="VALIDATION_ERROR",
        message="Invalid",
        trace_id="trace-id",
        data={"source": "query"},
        meta={"page": 1},
        errors=[ErrorDetail(field="email", code="INVALID_EMAIL", message="Invalid email")],
    )

    assert isinstance(response, JSONResponse)
    assert response.status_code == 422
    assert response.headers["X-Trace-Id"] == "trace-id"
    body = json.loads(response.body)
    assert body == {
        "success": False,
        "businessCode": "VALIDATION_ERROR",
        "message": "Invalid",
        "data": {"source": "query"},
        "meta": {
            "page": 1,
            "fieldErrors": [
                {"field": "email", "code": "INVALID_EMAIL", "message": "Invalid email"},
            ],
        },
        "traceId": "trace-id",
    }


def test_api_error_preserves_http_headers_and_sets_trace_header() -> None:
    """Xác nhận ApiError giữ header HTTP bổ sung và đặt trace ID do factory chọn."""
    response = ApiError(
        status_code=401,
        business_code="AUTH_REQUIRED",
        headers={"WWW-Authenticate": "Bearer", "X-Trace-Id": "caller-value"},
        trace_id="trace-id",
    )

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"
    assert response.headers["X-Trace-Id"] == "trace-id"
    assert json.loads(response.body)["data"] == {}


def test_internal_api_error_uses_current_trace_and_safe_defaults() -> None:
    """Xác nhận lỗi mặc định dùng message an toàn và trace ID trong ContextVar hiện tại."""
    trace_id = "00000000-0000-0000-0000-000000000001"
    token = set_trace_id(trace_id)
    try:
        response = ApiError()
    finally:
        reset_trace_id(token)

    assert response.status_code == 500
    assert response.headers["X-Trace-Id"] == trace_id
    assert json.loads(response.body) == {
        "success": False,
        "businessCode": "INTERNAL_SERVER_ERROR",
        "message": INTERNAL_ERROR_MESSAGE,
        "data": {},
        "meta": {},
        "traceId": trace_id,
    }


def test_internal_api_error_generates_trace_without_request_context() -> None:
    """Xác nhận ApiError sinh trace ID UUID khi không có request context."""
    response = ApiError()
    trace_id = response.headers["X-Trace-Id"]

    assert trace_id
    assert len(trace_id) == 36
    assert json.loads(response.body)["traceId"] == trace_id
