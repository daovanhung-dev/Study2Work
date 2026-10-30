from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import app.modules.admin.api_95_admin_notifications_delete.view as notification_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.admin.api_95_admin_notifications_delete.query import (
    DELETE_ADMIN_NOTIFICATION,
    LOCK_ADMIN_NOTIFICATION_DELIVERIES_FOR_DELETE,
    LOCK_ADMIN_NOTIFICATION_FOR_DELETE,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

DELETED_AT = datetime(2026, 10, 26, 10, 15, tzinfo=UTC)
_UNSET = object()


class FakeSession:
    """Session giả để kiểm tra transaction của API #95."""

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


def delete_notification(
    client: TestClient,
    *,
    notification_id: str = "501",
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi DELETE API #95 chỉ với path và header tùy chọn."""

    headers = {} if authorization is None else {"Authorization": authorization}
    return client.delete(f"/api/v1/admin/notifications/{notification_id}", headers=headers)


def install_delete_queries(
    monkeypatch: pytest.MonkeyPatch,
    *,
    notification_row: Any = _UNSET,
    delivery_rows: Any = _UNSET,
    deleted_row: Any = _UNSET,
    failing_query: str | None = None,
) -> list[tuple[str, dict[str, Any]]]:
    """Cài query doubles, lưu thứ tự SQL/bindings và mô phỏng lỗi query."""

    current = {"id": 501} if notification_row is _UNSET else notification_row
    deliveries = (
        [
            {"notification_id": 501, "channel": "EMAIL", "status": "QUEUED"},
            {"notification_id": 501, "channel": "PUSH", "status": "QUEUED"},
        ]
        if delivery_rows is _UNSET
        else delivery_rows
    )
    deleted = {"id": 501, "deleted_at": DELETED_AT} if deleted_row is _UNSET else deleted_row
    captured: list[tuple[str, dict[str, Any]]] = []

    def query_one(_db, query: str, params: dict[str, Any]):
        """Trả locked/deleted row hoặc phát lỗi query được cấu hình."""

        captured.append((query, dict(params)))
        if query == failing_query:
            raise SQLAlchemyError("private notification delete detail")
        if query == LOCK_ADMIN_NOTIFICATION_FOR_DELETE:
            return current
        if query == DELETE_ADMIN_NOTIFICATION:
            return deleted
        raise AssertionError("unexpected query_one SQL")

    def query_many(_db, query: str, params: dict[str, Any]):
        """Trả locked deliveries hoặc phát lỗi query được cấu hình."""

        captured.append((query, dict(params)))
        if query == failing_query:
            raise SQLAlchemyError("private delivery query detail")
        if query != LOCK_ADMIN_NOTIFICATION_DELIVERIES_FOR_DELETE:
            raise AssertionError("unexpected query_many SQL")
        return deliveries

    monkeypatch.setattr(notification_view, "query_one", query_one)
    monkeypatch.setattr(notification_view, "query_many", query_many)
    return captured


def test_delete_admin_notification_deletes_only_queued_row_and_returns_delete_result(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Khóa theo thứ tự parent/delivery rồi trả DeleteResult từ DELETE RETURNING."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_delete_queries(monkeypatch)

    response = delete_notification(client, notification_id="501")

    assert response.status_code == 200
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_DELETED"
    assert response.json()["data"] == {
        "id": 501,
        "status": "deleted",
        "deleted_at": DELETED_AT.isoformat().replace("+00:00", "Z"),
    }
    assert [query for query, _ in captured] == [
        LOCK_ADMIN_NOTIFICATION_FOR_DELETE,
        LOCK_ADMIN_NOTIFICATION_DELIVERIES_FOR_DELETE,
        DELETE_ADMIN_NOTIFICATION,
    ]
    assert all(params == {"notification_id": 501} for _, params in captured)
    assert session.commit_count == 1
    assert session.rollback_count == 0


def test_delete_admin_notification_returns_not_found_without_delivery_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 404 nếu parent không tồn tại và không đọc child rows."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_delete_queries(monkeypatch, notification_row=None)

    response = delete_notification(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert [query for query, _ in captured] == [LOCK_ADMIN_NOTIFICATION_FOR_DELETE]
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize(
    "delivery_rows",
    [
        [],
        [{"notification_id": 501, "channel": "EMAIL", "status": "SENT"}],
        [{"notification_id": 501, "channel": "EMAIL", "status": "FAILED"}],
    ],
)
def test_delete_admin_notification_rejects_missing_or_started_delivery(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    delivery_rows: list[dict[str, Any]],
) -> None:
    """Không xóa nếu không có delivery hoặc có delivery không còn QUEUED."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_delete_queries(monkeypatch, delivery_rows=delivery_rows)

    response = delete_notification(client)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert [query for query, _ in captured] == [
        LOCK_ADMIN_NOTIFICATION_FOR_DELETE,
        LOCK_ADMIN_NOTIFICATION_DELIVERIES_FOR_DELETE,
    ]
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize("notification_id", ["0", "x", "9223372036854775808", "9" * 100])
def test_delete_admin_notification_rejects_invalid_int64_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    notification_id: str,
) -> None:
    """Từ chối path ID sai hoặc ngoài signed-int64 trước mọi query."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_delete_queries(monkeypatch)

    response = delete_notification(client, notification_id=notification_id)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert captured == []
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_delete_admin_notification_authenticates_before_path_or_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Auth lỗi giữ precedence trước path sai và không truy vấn database."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    captured = install_delete_queries(monkeypatch)

    response = delete_notification(client, notification_id="not-an-id", authorization=None)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert captured == []
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_delete_admin_notification_forbids_non_admin_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Role khác ADMIN bị từ chối trước resource lookup."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch, roles=["MENTOR"])
    captured = install_delete_queries(monkeypatch)

    response = delete_notification(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert captured == []
    assert session.commit_count == 0
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    ("notification_row", "delivery_rows", "deleted_row"),
    [
        ({"id": "501"}, [], {"id": 501, "deleted_at": DELETED_AT}),
        ({"id": 501}, [{"notification_id": 502, "channel": "EMAIL", "status": "QUEUED"}], None),
        ({"id": 501}, [{"notification_id": 501, "channel": "SMS", "status": "QUEUED"}], None),
        (
            {"id": 501},
            [{"notification_id": 501, "channel": "EMAIL", "status": "QUEUED"}],
            {"id": 502, "deleted_at": DELETED_AT},
        ),
        (
            {"id": 501},
            [{"notification_id": 501, "channel": "EMAIL", "status": "QUEUED"}],
            {"id": 501, "deleted_at": "not-a-timestamp"},
        ),
    ],
)
def test_delete_admin_notification_rolls_back_malformed_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    notification_row: Any,
    delivery_rows: Any,
    deleted_row: Any,
) -> None:
    """Không commit projection sai; lỗi 500 không lộ chi tiết DB."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_delete_queries(
        monkeypatch,
        notification_row=notification_row,
        delivery_rows=delivery_rows,
        deleted_row=deleted_row,
    )

    response = delete_notification(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "not-a-timestamp" not in response.text
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize(
    "failing_query",
    [
        LOCK_ADMIN_NOTIFICATION_FOR_DELETE,
        LOCK_ADMIN_NOTIFICATION_DELIVERIES_FOR_DELETE,
        DELETE_ADMIN_NOTIFICATION,
    ],
)
def test_delete_admin_notification_rolls_back_query_failures_safely(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    failing_query: str,
) -> None:
    """Query lỗi trả 500 an toàn và rollback transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_delete_queries(monkeypatch, failing_query=failing_query)

    response = delete_notification(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private notification delete detail" not in response.text
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_delete_admin_notification_rolls_back_commit_failure(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Commit lỗi hoàn tác parent delete và cascade trong transaction giả."""

    session = FakeSession(commit_error=SQLAlchemyError("private commit detail"))
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_delete_queries(monkeypatch)

    response = delete_notification(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private commit detail" not in response.text
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_delete_admin_notification_openapi_has_catalog_contract_and_no_body(
    client: TestClient,
) -> None:
    """OpenAPI giữ path/header, exact errors, DeleteResult và không có body/query."""

    openapi = client.app.openapi()
    path = "/api/v1/admin/notifications/{notification_id}"
    operation = openapi["paths"][path]["delete"]

    assert "requestBody" not in operation
    assert operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"].endswith(
        "DeleteAdminNotificationEnvelope"
    )
    assert {
        "name": "notification_id",
        "in": "path",
        "required": True,
        "schema": {
            "type": "integer",
            "format": "int64",
            "minimum": 1,
            "maximum": 9223372036854775807,
        },
    } in operation["parameters"]
    assert {
        "name": "Authorization",
        "in": "header",
        "required": True,
        "schema": {"type": "string"},
    } in operation["parameters"]
    assert all(parameter["in"] != "query" for parameter in operation["parameters"])
    assert set(operation["responses"]) == {"200", "401", "403", "404", "422", "500"}
    assert operation["responses"]["200"]["description"] == "Successful Response"
    assert {
        code: operation["responses"][code]["description"]
        for code in ("401", "403", "404", "422", "500")
    } == {
        "401": "DESIGN_AUTHENTICATION_REQUIRED",
        "403": "DESIGN_ACCESS_DENIED",
        "404": "DESIGN_RESOURCE_NOT_FOUND",
        "422": "DESIGN_VALIDATION_ERROR",
        "500": "DESIGN_INTERNAL_ERROR",
    }
    envelope_schema_name = operation["responses"]["200"]["content"]["application/json"]["schema"][
        "$ref"
    ].rsplit("/", maxsplit=1)[-1]
    data_schema = openapi["components"]["schemas"][envelope_schema_name]["properties"]["data"]
    delete_result_ref = data_schema["$ref"]
    delete_result_name = delete_result_ref.rsplit("/", maxsplit=1)[-1]
    assert (
        openapi["components"]["schemas"][delete_result_name]["properties"]["status"]["const"]
        == "deleted"
    )

    api_paths = {key for key in openapi["paths"] if key.startswith("/api/v1/")}
    operation_count = sum(
        1
        for key in api_paths
        for method in openapi["paths"][key]
        if method in {"get", "post", "put", "patch", "delete"}
    )
    assert len(api_paths) == 57
    assert operation_count == 68
