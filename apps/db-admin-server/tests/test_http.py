from __future__ import annotations

from fastapi.testclient import TestClient


def test_health_is_available_without_database_connection(client: TestClient) -> None:
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["businessCode"] == "DB_ADMIN_HEALTH_LIVE"
    assert response.headers["X-Trace-Id"]


def test_admin_route_requires_database_only_after_auth(client: TestClient) -> None:
    response = client.post("/api/v1/admin/sql/validate", json={"sql": "SELECT 1"})
    assert response.status_code == 200
    assert response.json()["data"]["classification"] == "read_only"


def test_ddl_preview_returns_confirmation_token(client: TestClient) -> None:
    response = client.post(
        "/api/v1/admin/ddl/preview",
        json={"kind": "schema", "operation": "create", "object_name": "analytics"},
    )

    assert response.status_code == 200
    assert response.json()["data"]["confirmationToken"]


def test_row_mutation_requires_server_confirmation(client: TestClient) -> None:
    response = client.post(
        "/api/v1/admin/tables/public/events/rows",
        json={"values": {"id": 1}},
    )

    assert response.status_code == 409
    assert response.json()["businessCode"] == "DB_ADMIN_CONFIRMATION_INVALID"


def test_row_preview_returns_confirmation_token(client: TestClient) -> None:
    response = client.post(
        "/api/v1/admin/tables/public/events/rows/preview",
        json={"operation": "delete", "primary_key": {"id": 1}},
    )

    assert response.status_code == 200
    assert response.json()["data"]["confirmationToken"]
