"""Standalone smoke test using SQLite, without requiring PostgreSQL."""

import os
from uuid import uuid4

os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

from fastapi.testclient import TestClient  # noqa: E402

from app.core.database import engine  # noqa: E402
from app.main import app  # noqa: E402


DDL = """
CREATE TABLE auth_credentials (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    password_algorithm TEXT NOT NULL,
    password_login_enabled BOOLEAN NOT NULL,
    must_change_password BOOLEAN NOT NULL,
    failed_login_attempts INTEGER NOT NULL,
    locked_until TIMESTAMP NULL,
    password_changed_at TIMESTAMP NULL,
    last_login_at TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
)
"""


def run() -> None:
    with engine.begin() as connection:
        connection.exec_driver_sql(DDL)

    client = TestClient(app)

    assert client.get("/").status_code == 200
    assert client.get("/api/v1/hello").status_code == 200
    assert client.get("/api/v1/test/db").status_code == 200

    response = client.post(
        "/api/v1/register",
        json={"user_id": str(uuid4()), "password": "Password@123"},
    )
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["success"] is True, payload
    assert "password_hash" not in payload["data"]

    invalid = client.post(
        "/api/v1/register",
        json={"user_id": "not-a-uuid", "password": "123"},
    )
    assert invalid.status_code == 422, invalid.text

    print("Smoke test passed")


if __name__ == "__main__":
    run()
