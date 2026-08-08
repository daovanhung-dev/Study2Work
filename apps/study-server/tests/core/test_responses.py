import pytest
from app.core.responses import (
    ApiError,
    ApiResponse,
    ErrorDetail,
    error_payload,
    error_response,
    success_response,
)


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
    response = error_response(
        business_code="VALIDATION_ERROR",
        message="Invalid",
        trace_id="trace-id",
        errors=[
            ErrorDetail(field="email", code="INVALID_EMAIL", message="Invalid email"),
        ],
    )

    assert response["meta"] == {
        "fieldErrors": [
            {"field": "email", "code": "INVALID_EMAIL", "message": "Invalid email"},
        ],
    }
    assert "errors" not in response


def test_legacy_error_payload_preserves_top_level_errors() -> None:
    response = error_payload(
        business_code="VALIDATION_ERROR",
        message="Invalid",
        trace_id="trace-id",
        errors=[ErrorDetail(code="INVALID_EMAIL", message="Invalid email")],
    )

    assert response["errors"] == [
        {"field": None, "code": "INVALID_EMAIL", "message": "Invalid email"},
    ]


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
