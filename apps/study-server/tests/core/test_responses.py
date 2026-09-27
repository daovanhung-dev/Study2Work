import pytest
from app.core.responses import (
    INTERNAL_ERROR_MESSAGE,
    ApiError,
    ApiResponse,
    ErrorDetail,
    error_response,
    success_response,
)
from app.core.trace import reset_trace_id, set_trace_id


def test_success_response_uses_canonical_envelope() -> None:
    response = success_response(
        business_code="COURSE_LOADED",
        message="Loaded",
        trace_id="trace-id",
        data={"id": "course-1"},
    )

    assert response == {
        "success": True,
        "businessCode": "COURSE_LOADED",
        "message": "Loaded",
        "data": {"id": "course-1"},
        "meta": {},
        "traceId": "trace-id",
    }


def test_error_response_puts_field_errors_in_canonical_meta() -> None:
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


def test_internal_api_error_uses_current_trace_and_safe_defaults() -> None:
    trace_id = "00000000-0000-0000-0000-000000000001"
    token = set_trace_id(trace_id)
    try:
        error = ApiError.internal()
    finally:
        reset_trace_id(token)

    assert error.status_code == 500
    assert error.business_code == "INTERNAL_SERVER_ERROR"
    assert error.message == INTERNAL_ERROR_MESSAGE
    assert error.trace_id == trace_id


def test_internal_api_error_generates_trace_without_request_context() -> None:
    error = ApiError.internal()

    assert error.trace_id
    assert len(error.trace_id) == 36


def test_api_response_raise_error_uses_controlled_exception() -> None:
    response = ApiResponse(
        business_code="RESOURCE_NOT_FOUND",
        message="Not found",
        trace_id="trace-id",
        status_code=404,
    )

    with pytest.raises(ApiError) as error:
        response.raise_error()

    assert error.value.status_code == 404
    assert error.value.business_code == "RESOURCE_NOT_FOUND"
