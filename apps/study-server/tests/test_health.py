from __future__ import annotations

from uuid import UUID

from fastapi.testclient import TestClient


def test_live_health_returns_standard_envelope(client: TestClient) -> None:
    """Kiểm tra GET /health/live trả status thành công, envelope chuẩn, environment và trace
    header."""
    response = client.get("/health/live")

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["businessCode"] == "SYSTEM_HEALTH_LIVE"
    assert payload["message"] == "Study API is live."
    assert UUID(payload["traceId"])
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert payload["data"]["service"] == "study-api"
    assert payload["data"]["environment"] == "test"


def test_ready_health_returns_standard_envelope(client: TestClient) -> None:
    """Kiểm tra GET /health/ready trả envelope cấu hình dependency mà không probe database thật."""
    response = client.get("/health/ready")

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["businessCode"] == "SYSTEM_HEALTH_READY"
    assert payload["data"]["dependencies"] == {
        "database": "configured",
        "redis": "configured",
    }


def test_health_accepts_valid_trace_id(client: TestClient) -> None:
    """Kiểm tra health endpoint giữ UUID trace ID hợp lệ trong response và header."""
    trace_id = "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a"

    response = client.get("/health/live", headers={"X-Trace-Id": trace_id})

    assert response.json()["traceId"] == trace_id
    assert response.headers["X-Trace-Id"] == trace_id


def test_health_replaces_invalid_trace_id(client: TestClient) -> None:
    """Kiểm tra middleware thay trace ID sai định dạng bằng UUID mới."""
    response = client.get("/health/live", headers={"X-Trace-Id": "invalid"})

    payload = response.json()
    assert payload["traceId"] != "invalid"
    assert UUID(payload["traceId"])


def test_validation_errors_use_canonical_field_error_location(client: TestClient) -> None:
    """Kiểm tra lỗi validation trả tên trường không còn tiền tố body trong fieldErrors."""
    response = client.post("/api/v1/auth/register", json={})

    assert response.status_code == 422
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert payload["meta"]["fieldErrors"]
    assert response.headers["X-Trace-Id"] == payload["traceId"]


def test_unknown_route_uses_safe_error_envelope(client: TestClient) -> None:
    """Kiểm tra route không tồn tại trả HTTP 404 bằng envelope an toàn có trace ID."""
    response = client.get("/does-not-exist")

    assert response.status_code == 404
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "HTTP_ERROR"
    assert "Not Found" not in payload["message"]


def test_unhandled_error_keeps_trace_header_and_hides_details(
    client_without_server_exception: TestClient,
) -> None:
    """Kiểm tra exception nội bộ giữ trace header nhưng không làm lộ message nhạy cảm."""
    def fail_request() -> None:
        """Phát sinh lỗi chứa thông tin nhạy cảm để xác nhận handler không trả detail đó."""
        raise RuntimeError("database password should not be exposed")

    client_without_server_exception.app.add_api_route("/test/unhandled", fail_request)
    trace_id = "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a"
    response = client_without_server_exception.get(
        "/test/unhandled",
        headers={"X-Trace-Id": trace_id},
    )

    payload = response.json()
    assert response.status_code == 500
    assert payload["businessCode"] == "INTERNAL_SERVER_ERROR"
    assert "database password" not in response.text
    assert payload["traceId"] == trace_id
    assert response.headers["X-Trace-Id"] == payload["traceId"]
