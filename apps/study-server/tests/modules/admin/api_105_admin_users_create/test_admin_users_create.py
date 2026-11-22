"""HTTP regression tests for the Admin user-create API #105."""

from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any

import app.modules.admin.api_105_admin_users_create.view as users_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.admin.api_105_admin_users_create.query import (
    CHECK_ADMIN_USER_EMAIL,
    INSERT_ADMIN_USER,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class FakeSession:
    """Session giả theo dõi transaction trong test HTTP."""

    def __init__(self, *, fail_commit: bool = False) -> None:
        self.commit_count = 0
        self.rollback_count = 0
        self.fail_commit = fail_commit

    def commit(self) -> None:
        """Đếm commit hoặc phát sinh lỗi database theo cấu hình test."""

        self.commit_count += 1
        if self.fail_commit:
            raise SQLAlchemyError("private commit detail $argon2id$test-hash")

    def rollback(self) -> None:
        """Đếm rollback của transaction cần hủy."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả session giả cho TestClient."""

    def dependency():
        """Yield session giả trong một request."""

        yield session

    return dependency


def allow_admin_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """Cấp token test với role ADMIN cho shared guard."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": ["ADMIN"]},
    )


def post_user(
    client: TestClient,
    *,
    body: Any | None = None,
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi HTTP POST API #105 với body hoặc Authorization có thể tùy chỉnh."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    if body is None:
        body = {
            "full_name": "Mai Nguyen",
            "email": "mai@example.com",
            "password": "initial secret",
            "role": "STUDENT",
        }
    if isinstance(body, bytes):
        return client.post("/api/v1/admin/users", headers=headers, content=body)
    return client.post("/api/v1/admin/users", headers=headers, json=body)


def install_queries(
    monkeypatch: pytest.MonkeyPatch,
    *,
    role: str = "STUDENT",
    duplicate: bool = False,
    failing_query: str | None = None,
    invalid_profile: bool = False,
    unique_race: bool = False,
) -> tuple[list[tuple[str, dict[str, Any]]], list[str]]:
    """Cài query/hash doubles để kiểm tra insert, projection và credential."""

    captured: list[tuple[str, dict[str, Any]]] = []
    hashed_passwords: list[str] = []

    def query_one(_db, query, params):
        """Trả kết quả giả theo SQL và giữ lại bind parameters để assert."""

        captured.append((query, dict(params)))
        if query == failing_query:
            raise SQLAlchemyError("private query detail")
        if query == CHECK_ADMIN_USER_EMAIL:
            if duplicate:
                return {"id": 17}
            return None
        if query == INSERT_ADMIN_USER:
            if unique_race:
                origin = SimpleNamespace(diag=SimpleNamespace(constraint_name="users_email_key"))
                raise IntegrityError("insert", dict(params), origin)
            row = {
                "id": 4901,
                "full_name": params["full_name"],
                "email": params["email"],
                "role": role,
                "avatar_url": None,
                "phone": None,
                "status": "SUSPENDED" if invalid_profile else "ACTIVE",
                "created_at": datetime(2026, 1, 2, tzinfo=UTC),
                "updated_at": datetime(2026, 1, 2, tzinfo=UTC),
            }
            return row
        raise AssertionError("unexpected SQL query")

    def hash_password(password: str) -> str:
        """Capture plaintext only inside the test and return a fake Argon2 string."""

        hashed_passwords.append(password)
        return "$argon2id$test-hash"

    monkeypatch.setattr(users_view, "query_one", query_one)
    monkeypatch.setattr(users_view, "hash_password", hash_password)
    return captured, hashed_passwords


@pytest.mark.parametrize("role", ["STUDENT", "MENTOR", "ADMIN"])
def test_create_admin_user_persists_selected_role_and_returns_safe_profile(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    role: str,
) -> None:
    """Tạo ACTIVE user cho từng role được duyệt và không trả credential."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured, hashed_passwords = install_queries(monkeypatch, role=role)

    response = post_user(
        client,
        body={
            "full_name": "  Mai Nguyen  ",
            "email": "  mai@example.com  ",
            "password": " initial secret ",
            "role": role,
        },
    )

    assert response.status_code == 201, response.text
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_CREATED"
    assert payload["data"]["full_name"] == "Mai Nguyen"
    assert payload["data"]["email"] == "mai@example.com"
    assert payload["data"]["role"] == role
    assert payload["data"]["status"] == "ACTIVE"
    assert "password" not in payload["data"]
    assert "password_hash" not in payload["data"]
    assert [query for query, _ in captured] == [CHECK_ADMIN_USER_EMAIL, INSERT_ADMIN_USER]
    assert captured[0][1] == {"email": "mai@example.com"}
    assert captured[1][1] == {
        "full_name": "Mai Nguyen",
        "email": "mai@example.com",
        "password_hash": "$argon2id$test-hash",
        "role": role,
    }
    assert hashed_passwords == [" initial secret "]
    assert session.commit_count == 1
    assert session.rollback_count == 0
    assert response.headers["X-Trace-Id"] == payload["traceId"]


def test_create_admin_user_authenticates_before_parsing_or_querying(
    client: TestClient,
) -> None:
    """Body JSON sai không được parse hoặc đưa tới database trước Admin guard."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)

    response = post_user(client, body=b"{", authorization=None)

    assert response.status_code == 401
    assert session.commit_count == 0
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    "body",
    [
        {"full_name": "Mai", "email": "mai@example.com", "password": "secret", "role": "TEACHER"},
        {"full_name": "  ", "email": "mai@example.com", "password": "secret", "role": "STUDENT"},
        {"full_name": "Mai", "email": "not-an-email", "password": "secret", "role": "STUDENT"},
        {"full_name": "Mai", "email": "mai@example.com", "password": "   ", "role": "STUDENT"},
        {
            "full_name": "Mai",
            "email": "mai@example.com",
            "password": "secret",
            "role": "STUDENT",
            "extra": "x",
        },
    ],
)
def test_create_admin_user_rejects_invalid_body_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    body: dict[str, Any],
) -> None:
    """Từ chối role ngoài allowlist, input rỗng và field thừa trước SQL."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured, hashed_passwords = install_queries(monkeypatch)

    response = post_user(client, body=body)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert captured == []
    assert hashed_passwords == []
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_create_admin_user_returns_conflict_without_hashing_duplicate_email(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Email đã tồn tại trả 409, không băm password và rollback transaction đọc."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured, hashed_passwords = install_queries(monkeypatch, duplicate=True)

    response = post_user(client)

    assert response.status_code == 409
    assert response.json()["businessCode"] == "DESIGN_STATE_CONFLICT"
    assert [query for query, _ in captured] == [CHECK_ADMIN_USER_EMAIL]
    assert hashed_passwords == []
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_create_admin_user_maps_email_unique_race_to_conflict(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Unique constraint race giữa kiểm tra và insert cũng trả conflict."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured, _ = install_queries(monkeypatch, unique_race=True)

    response = post_user(client)

    assert response.status_code == 409
    assert response.json()["businessCode"] == "DESIGN_STATE_CONFLICT"
    assert [query for query, _ in captured] == [CHECK_ADMIN_USER_EMAIL, INSERT_ADMIN_USER]
    assert session.rollback_count == 1


def test_create_admin_user_rolls_back_invalid_insert_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Không commit khi row mới không khớp role/status đã yêu cầu."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_queries(monkeypatch, invalid_profile=True)

    response = post_user(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private" not in response.text
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize("failure", ["query", "commit"])
def test_create_admin_user_rolls_back_database_failures_safely(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    failure: str,
) -> None:
    """Database query/commit failure trả 500 an toàn sau rollback."""

    session = FakeSession(fail_commit=failure == "commit")
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_queries(
        monkeypatch,
        failing_query=CHECK_ADMIN_USER_EMAIL if failure == "query" else None,
    )

    response = post_user(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private" not in response.text
    assert "private" not in caplog.text
    assert "$argon2id$test-hash" not in caplog.text
    assert session.commit_count == (1 if failure == "commit" else 0)
    assert session.rollback_count == 1


def test_create_admin_user_openapi_documents_request_roles_and_errors(client: TestClient) -> None:
    """OpenAPI mô tả request role, response created và lỗi conflict/auth."""

    operation = client.app.openapi()["paths"]["/api/v1/admin/users"]["post"]
    request_schema = operation["requestBody"]["content"]["application/json"]["schema"]

    assert request_schema["required"] == ["full_name", "email", "password", "role"]
    assert request_schema["properties"]["role"]["enum"] == ["STUDENT", "MENTOR", "ADMIN"]
    assert "201" in operation["responses"]
    assert "401" in operation["responses"]
    assert "403" in operation["responses"]
    assert "409" in operation["responses"]
