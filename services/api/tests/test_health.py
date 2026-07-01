from __future__ import annotations

from uuid import UUID

from fastapi.testclient import TestClient
from tests.conftest import make_test_client


def test_health_returns_standard_envelope() -> None:
    with make_test_client() as client:
        response = client.get("/api/v1/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "SYSTEM-HEALTH-SUCCESS"
    assert payload["message"] == "Service is healthy."
    assert UUID(payload["traceId"])
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert payload["data"] == {
        "status": "ok",
        "service": "study2work-api",
        "version": "0.1.0",
        "environment": "test",
    }


def test_health_accepts_valid_upstream_trace_id() -> None:
    trace_id = "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a"

    with make_test_client() as client:
        response = client.get("/api/v1/health", headers={"X-Trace-Id": trace_id})

    payload = response.json()
    assert payload["traceId"] == trace_id
    assert response.headers["X-Trace-Id"] == trace_id


def test_health_replaces_invalid_upstream_trace_id() -> None:
    with make_test_client() as client:
        response = client.get("/api/v1/health", headers={"X-Trace-Id": "not-a-uuid"})

    payload = response.json()
    assert payload["traceId"] != "not-a-uuid"
    assert UUID(payload["traceId"])


def test_client_fixture_type() -> None:
    assert isinstance(make_test_client(), TestClient)
