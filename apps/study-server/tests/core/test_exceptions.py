import json

import pytest
from app.core.middleware import (
    http_exception_handler,
    request_validation_exception_handler,
    unhandled_exception_handler,
)
from app.core.trace import TRACE_HEADER
from app.main import create_app
from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient
from starlette.exceptions import HTTPException
from starlette.requests import Request

TRACE_ID = "00000000-0000-0000-0000-000000000001"


def test_create_app_registers_http_exception_handler() -> None:
    """Kiểm tra HTTP 404 do router phát sinh được chuẩn hóa bởi handler đã đăng ký trong app."""
    with TestClient(create_app()) as client:
        response = client.get("/missing", headers={TRACE_HEADER: TRACE_ID})

    assert response.status_code == 404
    assert response.headers[TRACE_HEADER] == TRACE_ID
    assert response.json()["businessCode"] == "HTTP_ERROR"
    assert response.json()["traceId"] == TRACE_ID


def make_request(path: str) -> Request:
    """Tạo đối tượng Request Starlette giả cho đường dẫn được truyền vào và gắn trace ID kiểm thử
    vào request.state."""
    request = Request(
        {
            "type": "http",
            "method": "GET",
            "scheme": "http",
            "server": ("testserver", 80),
            "client": ("testclient", 50000),
            "root_path": "",
            "path": path,
            "raw_path": path.encode(),
            "query_string": b"",
            "headers": [],
        }
    )
    request.state.trace_id = TRACE_ID
    return request


@pytest.mark.asyncio
async def test_http_exception_is_serialized_through_api_error() -> None:
    """Kiểm tra HTTPException được chuyển qua handler ApiError, giữ status và trace header nhưng
    không làm lộ detail tùy ý."""
    response = await http_exception_handler(
        make_request("/missing"),
        HTTPException(status_code=404, detail="private router detail"),
    )
    payload = json.loads(response.body)

    assert response.status_code == 404
    assert response.headers[TRACE_HEADER] == TRACE_ID
    assert payload == {
        "success": False,
        "businessCode": "HTTP_ERROR",
        "message": "Yêu cầu không thể được xử lý.",
        "data": {},
        "meta": {},
        "traceId": TRACE_ID,
    }
    assert "private router detail" not in response.body.decode()


@pytest.mark.asyncio
async def test_request_validation_becomes_api_error_with_field_errors() -> None:
    """Kiểm tra lỗi validation của request thành HTTP 422 với business code chuẩn và tên trường
    được đặt trong meta.fieldErrors."""
    response = await request_validation_exception_handler(
        make_request("/api/v1/categories"),
        RequestValidationError(
            [
                {
                    "type": "string_type",
                    "loc": ("query", "locale"),
                    "msg": "Input should be a valid string",
                    "input": 123,
                }
            ]
        ),
    )
    payload = json.loads(response.body)

    assert response.status_code == 422
    assert response.headers[TRACE_HEADER] == TRACE_ID
    assert payload["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert payload["meta"]["fieldErrors"] == [
        {
            "field": "locale",
            "code": "STRING_TYPE",
            "message": "Input should be a valid string",
        }
    ]


@pytest.mark.asyncio
async def test_unhandled_exception_becomes_safe_api_error() -> None:
    """Kiểm tra exception không xử lý được được ghi log nội bộ nhưng client chỉ nhận envelope lỗi
    an toàn cùng trace ID."""
    response = await unhandled_exception_handler(
        make_request("/internal"),
        RuntimeError("database password must not leak"),
    )
    payload = json.loads(response.body)

    assert response.status_code == 500
    assert response.headers[TRACE_HEADER] == TRACE_ID
    assert payload["businessCode"] == "INTERNAL_SERVER_ERROR"
    assert payload["message"] == "Đã xảy ra lỗi nội bộ hệ thống."
    assert "database password must not leak" not in response.body.decode()
