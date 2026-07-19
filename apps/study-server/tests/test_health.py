from __future__ import annotations

from uuid import UUID

from fastapi.testclient import TestClient


def test_live_health_returns_standard_envelope(client: TestClient) -> None:
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
    trace_id = "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a"

    response = client.get("/health/live", headers={"X-Trace-Id": trace_id})

    assert response.json()["traceId"] == trace_id
    assert response.headers["X-Trace-Id"] == trace_id


def test_health_replaces_invalid_trace_id(client: TestClient) -> None:
    response = client.get("/health/live", headers={"X-Trace-Id": "invalid"})

    payload = response.json()
    assert payload["traceId"] != "invalid"
    assert UUID(payload["traceId"])
