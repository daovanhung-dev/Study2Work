from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import app.modules.admin.api_94_admin_notifications_update.view as notification_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.admin.api_94_admin_notifications_update.query import (
    LOCK_ADMIN_NOTIFICATION,
    LOCK_ADMIN_NOTIFICATION_DELIVERIES,
    UPDATE_ADMIN_NOTIFICATION,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

CREATED_AT = datetime(2026, 10, 26, 9, 45, tzinfo=UTC)


class FakeSession:
    """Session giả để kiểm tra transaction của API #94."""

    def __init__(self, *, commit_error: SQLAlchemyError | None = None) -> None:
        """Khởi tạo bộ đếm transaction và lỗi commit tùy chọn."""

        self.commit_count = 0
        self.rollback_count = 0
        self.commit_error = commit_error

    def commit(self) -> None:
        """Ghi nhận commit hoặc phát lỗi đã cấu hình."""

        self.commit_count += 1
        if self.commit_error is not None:
            raise self.commit_error

    def rollback(self) -> None:
        """Ghi nhận rollback sau lỗi hoặc request không đủ điều kiện."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả session giả cho TestClient."""

    def dependency():
        """Yield session giả trong một HTTP request."""

        yield session

    return dependency


def allow_admin_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Cấp access JWT giả có subject số theo shared ADMIN guard."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": roles or ["ADMIN"]},
    )


def request_body(**overrides: Any) -> dict[str, Any]:
    """Tạo body update title/content hợp lệ theo local fallback API #94."""

    return {"title": "Lịch học mới", "content": "Nội dung được cập nhật.", **overrides}


def put_notification(
    client: TestClient,
    *,
    notification_id: str = "501",
    body: Any = None,
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi PUT API #94 với JSON/raw bytes và Bearer tùy chọn."""

    headers = {} if authorization is None else {"Authorization": authorization}
    if body is None:
        body = request_body()
    if isinstance(body, bytes):
        return client.put(
            f"/api/v1/admin/notifications/{notification_id}",
            headers={**headers, "Content-Type": "application/json"},
            content=body,
        )
    return client.put(
        f"/api/v1/admin/notifications/{notification_id}",
        headers=headers,
        json=body,
    )


def install_update_queries(
    monkeypatch: pytest.MonkeyPatch,
    *,
    notification_row: dict[str, Any] | None = None,
    delivery_rows: list[dict[str, Any]] | None = None,
    updated_row: dict[str, Any] | None = None,
    failing_query: str | None = None,
) -> list[tuple[str, dict[str, Any]]]:
    """Cài query doubles, lưu thứ tự SQL/bindings và mô phỏng lỗi persistence."""

    current = notification_row or {
        "id": 501,
        "title": "Tiêu đề cũ",
        "content": "Nội dung cũ",
        "created_at": CREATED_AT,
    }
    deliveries = (
        [
            {"notification_id": 501, "channel": "EMAIL", "status": "QUEUED"},
            {"notification_id": 501, "channel": "PUSH", "status": "QUEUED"},
        ]
        if delivery_rows is None
        else delivery_rows
    )
    updated = updated_row or {
        "id": 501,
        "title": "Lịch học mới",
        "content": "Nội dung được cập nhật.",
        "created_at": CREATED_AT,
    }
    captured: list[tuple[str, dict[str, Any]]] = []

    def query_one(_db, query: str, params: dict[str, Any]):
        """Trả locked/updated row hoặc phát lỗi query được cấu hình."""

        captured.append((query, dict(params)))
        if query == failing_query:
            raise SQLAlchemyError("private notification query detail")
        if query == LOCK_ADMIN_NOTIFICATION:
            return current
        if query == UPDATE_ADMIN_NOTIFICATION:
            return updated
        raise AssertionError("unexpected query_one SQL")

    def query_many(_db, query: str, params: dict[str, Any]):
        """Trả locked delivery rows hoặc phát lỗi query được cấu hình."""

        captured.append((query, dict(params)))
        if query == failing_query:
            raise SQLAlchemyError("private delivery query detail")
        if query != LOCK_ADMIN_NOTIFICATION_DELIVERIES:
            raise AssertionError("unexpected query_many SQL")
        return deliveries

    monkeypatch.setattr(notification_view, "query_one", query_one)
    monkeypatch.setattr(notification_view, "query_many", query_many)
    return captured


def test_update_admin_notification_updates_text_and_preserves_delivery_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Khóa parent/delivery, cập nhật text và trả Notification QUEUED."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_update_queries(monkeypatch)

    response = put_notification(client)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_UPDATED"
    assert payload["data"] == {
        "id": 501,
        "title": "Lịch học mới",
        "content": "Nội dung được cập nhật.",
        "channels": ["EMAIL", "PUSH"],
        "status": "QUEUED",
        "created_at": "2026-10-26T09:45:00Z",
    }
    assert payload["traceId"] == response.headers["X-Trace-Id"]
    assert [query for query, _params in captured] == [
        LOCK_ADMIN_NOTIFICATION,
        LOCK_ADMIN_NOTIFICATION_DELIVERIES,
        UPDATE_ADMIN_NOTIFICATION,
    ]
    assert [params for _query, params in captured] == [
        {"notification_id": 501},
        {"notification_id": 501},
        {
            "notification_id": 501,
            "title": "Lịch học mới",
            "content": "Nội dung được cập nhật.",
        },
    ]
    assert "FOR UPDATE OF n" in LOCK_ADMIN_NOTIFICATION
    assert "FOR UPDATE OF d" in LOCK_ADMIN_NOTIFICATION_DELIVERIES
    assert "SET title = :title" in UPDATE_ADMIN_NOTIFICATION
    assert "content = :content" in UPDATE_ADMIN_NOTIFICATION
    assert "user_id" not in UPDATE_ADMIN_NOTIFICATION
    assert "sender_id" not in UPDATE_ADMIN_NOTIFICATION
    assert "created_at =" not in UPDATE_ADMIN_NOTIFICATION
    assert session.commit_count == 1
    assert session.rollback_count == 0


def test_update_admin_notification_authenticates_before_path_body_or_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Auth 401/403 được ưu tiên trên path/body lỗi và không chạm DB."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    query_calls = 0

    def unexpected_query(*_args, **_kwargs):
        """Phát hiện truy vấn trước khi role được xác thực."""

        nonlocal query_calls
        query_calls += 1
        raise AssertionError("database must not be queried")

    monkeypatch.setattr(notification_view, "query_one", unexpected_query)
    monkeypatch.setattr(notification_view, "query_many", unexpected_query)

    unauthenticated = put_notification(
        client,
        notification_id="bad-id",
        body=b"not-json",
        authorization=None,
    )
    allow_admin_token(monkeypatch, roles=["MENTOR"])
    forbidden = put_notification(
        client,
        notification_id="bad-id",
        body=b"not-json",
    )

    assert unauthenticated.status_code == 401
    assert unauthenticated.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert forbidden.status_code == 403
    assert forbidden.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert query_calls == 0
    assert session.commit_count == 0


@pytest.mark.parametrize(
    ("notification_id", "body", "field"),
    [
        ("0", request_body(), "notification_id"),
        ("9223372036854775808", request_body(), "notification_id"),
        ("9" * 5000, request_body(), "notification_id"),
        ("501", b"not-json", "body"),
        ("501", {"title": "x", "content": "y", "channels": ["EMAIL"]}, "channels"),
        ("501", {"title": "   ", "content": "y"}, "title"),
        ("501", {"title": "x", "content": "  "}, "content"),
        ("501", {"title": "x" * 201, "content": "y"}, "title"),
    ],
)
def test_update_admin_notification_rejects_invalid_input_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    notification_id: str,
    body: Any,
    field: str,
) -> None:
    """Reject path/body fallback violations before executing SQL."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    query_calls = 0

    def unexpected_query(*_args, **_kwargs):
        """Phát hiện query trước khi request được xác thực."""

        nonlocal query_calls
        query_calls += 1
        raise AssertionError("database must not be queried")

    monkeypatch.setattr(notification_view, "query_one", unexpected_query)
    monkeypatch.setattr(notification_view, "query_many", unexpected_query)

    response = put_notification(client, notification_id=notification_id, body=body)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0]["field"] == field
    assert query_calls == 0
    assert session.commit_count == 0


def test_update_admin_notification_returns_not_found_without_update(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 404 khi notification không tồn tại."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured: list[tuple[str, dict[str, Any]]] = []

    def missing_notification(_db, query: str, params: dict[str, Any]):
        """Ghi nhận lookup notification và giả lập target không có."""

        captured.append((query, dict(params)))
        assert query == LOCK_ADMIN_NOTIFICATION
        return None

    monkeypatch.setattr(notification_view, "query_one", missing_notification)
    monkeypatch.setattr(
        notification_view,
        "query_many",
        lambda *_args: pytest.fail("delivery query must not run for missing notification"),
    )

    response = put_notification(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert captured == [(LOCK_ADMIN_NOTIFICATION, {"notification_id": 501})]
    assert session.commit_count == 0


@pytest.mark.parametrize(
    "delivery_rows",
    [
        [],
        [{"notification_id": 501, "channel": "EMAIL", "status": "SENT"}],
        [{"notification_id": 501, "channel": "EMAIL", "status": "FAILED"}],
    ],
)
def test_update_admin_notification_rejects_missing_or_started_delivery(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    delivery_rows: list[dict[str, Any]],
) -> None:
    """Không cập nhật khi thiếu outbox row hoặc delivery không còn QUEUED."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_update_queries(monkeypatch, delivery_rows=delivery_rows)

    response = put_notification(client)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert [query for query, _params in captured] == [
        LOCK_ADMIN_NOTIFICATION,
        LOCK_ADMIN_NOTIFICATION_DELIVERIES,
    ]
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize(
    "failing_query",
    [LOCK_ADMIN_NOTIFICATION, LOCK_ADMIN_NOTIFICATION_DELIVERIES, UPDATE_ADMIN_NOTIFICATION],
)
def test_update_admin_notification_rolls_back_database_failures_safely(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    failing_query: str,
) -> None:
    """Rollback và trả error 500 không phản chiếu chi tiết query."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_update_queries(monkeypatch, failing_query=failing_query)

    response = put_notification(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private notification query detail" not in response.text
    assert "private delivery query detail" not in response.text
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_update_admin_notification_rolls_back_commit_failure(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Commit failure chuyển thành catalog 500 sau khi rollback."""

    session = FakeSession(commit_error=SQLAlchemyError("private commit detail"))
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_update_queries(monkeypatch)

    response = put_notification(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private commit detail" not in response.text
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_update_admin_notification_rejects_malformed_update_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Rollback nếu UPDATE RETURNING không khớp notification được khóa."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_update_queries(monkeypatch, updated_row={"id": 502})

    response = put_notification(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_update_admin_notification_openapi_declares_path_body_and_catalog_errors(
    client: TestClient,
) -> None:
    """OpenAPI ghi route #94, fallback strict body và đúng catalog errors."""

    paths = client.app.openapi()["paths"]
    api_paths = {path: value for path, value in paths.items() if path.startswith("/api/v1/")}
    operation_count = sum(
        method in {"get", "post", "put", "patch", "delete"}
        for item in api_paths.values()
        for method in item
    )
    assert len(api_paths) == 57
    assert operation_count == 68

    operation = paths["/api/v1/admin/notifications/{notification_id}"]["put"]
    assert {item["name"] for item in operation["parameters"]} == {
        "notification_id",
        "Authorization",
    }
    path_parameter = next(
        item for item in operation["parameters"] if item["name"] == "notification_id"
    )
    assert path_parameter["schema"] == {
        "type": "integer",
        "minimum": 1,
        "format": "int64",
    }
    assert set(operation["responses"]) == {"200", "401", "403", "404", "422", "500"}
    assert operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"].endswith(
        "/UpdateAdminNotificationEnvelope"
    )
    body_schema = operation["requestBody"]["content"]["application/json"]["schema"]
    assert body_schema["required"] == ["title", "content"]
    assert body_schema["additionalProperties"] is False
    assert set(body_schema["properties"]) == {"title", "content"}
    assert body_schema["properties"]["title"]["maxLength"] == 200
