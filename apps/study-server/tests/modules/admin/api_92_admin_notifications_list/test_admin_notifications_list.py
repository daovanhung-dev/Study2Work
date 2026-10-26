from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import app.modules.admin.api_92_admin_notifications_list.view as notifications_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError, SQLAlchemyError


class FakeSession:
    """Session giả dùng để xác minh API #92 chỉ đọc và rollback khi lỗi."""

    def __init__(self) -> None:
        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Đếm commit nếu route vô tình ghi dữ liệu."""

        self.commit_count += 1

    def rollback(self) -> None:
        """Đếm rollback khi query hoặc projection lỗi."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả fake session cho TestClient."""

    def dependency():
        """Yield session giả trong một HTTP request."""

        yield session

    return dependency


def allow_admin_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Thay decoder để cấp JWT Admin có subject số ổn định trong test."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": roles or ["ADMIN"]},
    )


def notification_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection Notification theo legacy row và delivery aggregate."""

    return {
        "id": 501,
        "title": "Thông báo lịch học",
        "content": "Lịch học được cập nhật.",
        "channels": ["EMAIL", "PUSH"],
        "status": "QUEUED",
        "created_at": datetime(2026, 10, 26, 8, 30, tzinfo=UTC),
        **overrides,
    }


def install_query_rows(
    monkeypatch: pytest.MonkeyPatch,
    *,
    rows: list[dict[str, Any]] | None = None,
    total: int | None = None,
    failure: tuple[str, SQLAlchemyError] | None = None,
) -> list[tuple[str, dict[str, Any]]]:
    """Cài query doubles và ghi nhận câu SQL cùng bindings theo thứ tự gọi."""

    result_rows = [notification_row()] if rows is None else rows
    result_total = len(result_rows) if total is None else total
    captured: list[tuple[str, dict[str, Any]]] = []

    def query_one(_db, query, params):
        """Trả count giả hoặc phát lỗi được cấu hình cho count query."""

        captured.append((query, dict(params)))
        if query != notifications_view.COUNT_ADMIN_NOTIFICATIONS:
            raise AssertionError("unexpected count query")
        if failure is not None and failure[0] == "count":
            raise failure[1]
        return {"total": result_total}

    def query_many(_db, query, params):
        """Trả trang giả hoặc phát lỗi được cấu hình cho list query."""

        captured.append((query, dict(params)))
        if query != notifications_view.LIST_ADMIN_NOTIFICATIONS:
            raise AssertionError("unexpected list query")
        if failure is not None and failure[0] == "list":
            raise failure[1]
        return result_rows

    monkeypatch.setattr(notifications_view, "query_one", query_one)
    monkeypatch.setattr(notifications_view, "query_many", query_many)
    return captured


def get_notifications_response(
    client: TestClient,
    *,
    authorization: str | None = "Bearer valid-admin-token",
    params: dict[str, str] | None = None,
):
    """Gửi HTTP GET API #92 với query/header tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.get("/api/v1/admin/notifications", headers=headers, params=params or {})


def test_get_admin_notifications_returns_page_and_is_read_only(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả Page<Notification>, timestamps và status/channel từ local aggregate."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_query_rows(monkeypatch, rows=[notification_row()], total=21)

    response = get_notifications_response(client)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"]["pagination"] == {
        "page": 1,
        "size": 20,
        "total": 21,
        "total_pages": 2,
    }
    assert payload["data"]["items"] == [
        {
            "id": 501,
            "title": "Thông báo lịch học",
            "content": "Lịch học được cập nhật.",
            "channels": ["EMAIL", "PUSH"],
            "status": "QUEUED",
            "created_at": "2026-10-26T08:30:00Z",
        }
    ]
    assert captured[0][1] == {"status": None, "channel": None}
    assert captured[1][1] == {
        "status": None,
        "channel": None,
        "limit": 20,
        "offset": 0,
    }
    assert "FROM notification_deliveries AS d" in captured[0][0]
    assert "FROM notification_deliveries AS d" in captured[1][0]
    assert "ORDER BY n.created_at DESC, n.id DESC" in captured[1][0]
    assert "n.user_id" not in captured[1][0]
    assert "n.sender_id" not in captured[1][0]
    assert "n.is_read" not in captured[1][0]
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_admin_notifications_applies_exact_filters_and_page_offset(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Bind nguyên status/channel và tính offset cho page thứ hai."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_query_rows(monkeypatch, rows=[notification_row(id=502)], total=30)

    response = get_notifications_response(
        client,
        params={"status": " queued ", "channel": "push", "page": "2"},
    )

    assert response.status_code == 200
    assert response.json()["data"]["pagination"] == {
        "page": 2,
        "size": 20,
        "total": 30,
        "total_pages": 2,
    }
    assert captured[0][1] == {"status": " queued ", "channel": "push"}
    assert captured[1][1] == {
        "status": " queued ",
        "channel": "push",
        "limit": 20,
        "offset": 20,
    }
    assert "n.status = :status" in captured[0][0]
    assert "n.status = :status" in captured[1][0]
    assert ":channel = ANY(n.channels)" in captured[0][0]
    assert ":channel = ANY(n.channels)" in captured[1][0]


@pytest.mark.parametrize(
    "page",
    ["0", "-1", "1.5", "invalid", "2147483648"],
)
def test_get_admin_notifications_rejects_invalid_page_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    page: str,
) -> None:
    """Trả 422 cho page không dương/int32 trước khi gọi query."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    query_calls = 0

    def unexpected_query(*_args, **_kwargs):
        """Đánh dấu lỗi nếu validation gọi database."""

        nonlocal query_calls
        query_calls += 1
        raise AssertionError("database must not be queried")

    monkeypatch.setattr(notifications_view, "query_one", unexpected_query)
    monkeypatch.setattr(notifications_view, "query_many", unexpected_query)

    response = get_notifications_response(client, params={"page": page})

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0]["field"] == "page"
    assert query_calls == 0
    assert session.commit_count == 0


def test_get_admin_notifications_authenticates_before_invalid_page(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Role sai được trả 403 trước khi kiểm tra page hoặc truy vấn database."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch, roles=["STUDENT"])

    response = get_notifications_response(client, params={"page": "invalid"})

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_admin_notifications_requires_bearer_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Thiếu Bearer token trả 401 và không gọi query."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    query_calls = 0

    def unexpected_query(*_args, **_kwargs):
        """Đánh dấu lỗi nếu unauthenticated request chạm database."""

        nonlocal query_calls
        query_calls += 1
        raise AssertionError("database must not be queried")

    monkeypatch.setattr(notifications_view, "query_one", unexpected_query)
    monkeypatch.setattr(notifications_view, "query_many", unexpected_query)

    response = get_notifications_response(client, authorization=None)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert query_calls == 0
    assert session.rollback_count == 0


def test_get_admin_notifications_returns_empty_page_without_not_found(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Empty result và page ngoài phạm vi dữ liệu đều là Page rỗng HTTP 200."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_query_rows(monkeypatch, rows=[], total=0)

    response = get_notifications_response(client)

    assert response.status_code == 200
    assert response.json()["data"] == {
        "items": [],
        "pagination": {"page": 1, "size": 20, "total": 0, "total_pages": 0},
    }
    assert response.json()["message"] == "No notifications found."
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    "row",
    [
        notification_row(channels=[]),
        notification_row(channels=["SMS"]),
        notification_row(channels=["PUSH", "PUSH"]),
        notification_row(status="SCHEDULED"),
        notification_row(created_at="2026-10-26T08:30:00Z"),
        notification_row(id=0),
    ],
)
def test_get_admin_notifications_rejects_invalid_projection_safely(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    row: dict[str, Any],
) -> None:
    """Malformed status/channel/required projection maps to safe 500 and rollback."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_query_rows(monkeypatch, rows=[row], total=1)

    response = get_notifications_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "Thông báo lịch học" not in response.text if row.get("title") else True
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_admin_notifications_rejects_malformed_count(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Count projection không hợp lệ không tạo pagination response."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_query_rows(monkeypatch)

    def malformed_count(_db, query, params):
        """Trả total sai kiểu để kiểm tra error mapping."""

        captured.append((query, dict(params)))
        return {"total": "1"}

    monkeypatch.setattr(notifications_view, "query_one", malformed_count)

    response = get_notifications_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize(
    ("failure", "expected_status", "expected_code"),
    [
        (
            ("count", OperationalError("SELECT", {}, RuntimeError("offline"))),
            503,
            "DESIGN_DEPENDENCY_UNAVAILABLE",
        ),
        (("list", SQLAlchemyError("query failed")), 500, "DESIGN_INTERNAL_ERROR"),
    ],
)
def test_get_admin_notifications_maps_database_failures_safely(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    failure: tuple[str, SQLAlchemyError],
    expected_status: int,
    expected_code: str,
) -> None:
    """Database unavailable maps 503; other SQL errors map 500 without leaking detail."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_query_rows(monkeypatch, failure=failure)

    response = get_notifications_response(client)

    assert response.status_code == expected_status
    assert response.json()["businessCode"] == expected_code
    assert "query failed" not in response.text
    assert "offline" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_admin_notifications_openapi_declares_query_and_catalog_errors(
    client: TestClient,
) -> None:
    """OpenAPI khai báo query int32, Page response và các lỗi catalog cùng 422 DERIVED."""

    paths = client.app.openapi()["paths"]
    api_paths = {path: value for path, value in paths.items() if path.startswith("/api/v1/")}
    operation_count = sum(
        method in {"get", "post", "put", "patch", "delete"}
        for item in api_paths.values()
        for method in item
    )
    assert len(api_paths) == 57
    assert operation_count == 68

    operation = paths["/api/v1/admin/notifications"]["get"]
    parameters = {parameter["name"]: parameter for parameter in operation["parameters"]}

    assert set(parameters) == {"Authorization", "channel", "page", "status"}
    assert parameters["page"]["schema"] == {
        "type": "integer",
        "format": "int32",
        "minimum": 1,
        "maximum": 2147483647,
        "default": 1,
    }
    assert operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"].endswith(
        "GetAdminNotificationsEnvelope"
    )
    assert set(operation["responses"]) == {"200", "401", "403", "422", "500", "503"}
