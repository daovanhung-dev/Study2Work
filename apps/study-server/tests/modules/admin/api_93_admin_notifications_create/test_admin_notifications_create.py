from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID

import app.modules.admin.api_93_admin_notifications_create.view as notification_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.admin.api_93_admin_notifications_create.query import (
    FIND_ADMIN_NOTIFICATION_RECIPIENTS,
    INSERT_ADMIN_NOTIFICATION,
    INSERT_ADMIN_NOTIFICATION_DELIVERY,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError, SQLAlchemyError

CREATED_AT = datetime(2026, 10, 26, 9, 45, tzinfo=UTC)
_DEFAULT = object()


class FakeSession:
    """Session giả để kiểm tra transaction của API #93."""

    def __init__(self, *, commit_error: SQLAlchemyError | None = None) -> None:
        """Khởi tạo bộ đếm và lỗi commit tùy chọn."""

        self.commit_count = 0
        self.rollback_count = 0
        self.commit_error = commit_error

    def commit(self) -> None:
        """Ghi nhận commit hoặc phát lỗi đã cấu hình."""

        self.commit_count += 1
        if self.commit_error is not None:
            raise self.commit_error

    def rollback(self) -> None:
        """Ghi nhận rollback khi batch không thể được chấp nhận."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo FastAPI dependency override trả session giả."""

    def dependency():
        """Yield session giả cho request hiện tại."""

        yield session

    return dependency


def allow_admin_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Cấp access JWT giả có Admin subject số cho TestClient."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": roles or ["ADMIN"]},
    )


def request_body(**overrides: Any) -> dict[str, Any]:
    """Tạo body explicit-recipient hợp lệ theo catalog và local fallback."""

    return {
        "recipients": [2002, 2001],
        "title": "Thông báo lịch học",
        "content": "Lịch học được cập nhật.",
        "channels": ["PUSH", "EMAIL"],
        **overrides,
    }


def post_notification(
    client: TestClient,
    *,
    body: Any = _DEFAULT,
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi POST API #93 với JSON hoặc raw bytes và Bearer tùy chọn."""

    headers = {} if authorization is None else {"Authorization": authorization}
    if body is _DEFAULT:
        body = request_body()
    if isinstance(body, bytes):
        return client.post(
            "/api/v1/admin/notifications",
            headers={**headers, "Content-Type": "application/json"},
            content=body,
        )
    return client.post("/api/v1/admin/notifications", headers=headers, json=body)


def install_create_queries(
    monkeypatch: pytest.MonkeyPatch,
    *,
    recipient_rows: list[dict[str, Any]] | None = None,
    notification_rows: list[dict[str, Any]] | None = None,
    bad_delivery: bool = False,
    failing_query: str | None = None,
    failure: SQLAlchemyError | None = None,
) -> list[tuple[str, dict[str, Any]]]:
    """Cài query doubles, lưu SQL/bindings và mô phỏng projection/lỗi persistence."""

    captured: list[tuple[str, dict[str, Any]]] = []
    selected_recipient_rows = recipient_rows
    selected_notification_rows = iter(
        notification_rows
        or [
            {"id": 31001, "created_at": CREATED_AT},
            {"id": 31002, "created_at": CREATED_AT},
        ]
    )
    next_delivery_id = 41001
    delivery_call_count = 0

    def query_many(_db, query: str, params: dict[str, Any]):
        """Trả đúng recipient projection hoặc phát lỗi query được cấu hình."""

        captured.append((query, dict(params)))
        if query != FIND_ADMIN_NOTIFICATION_RECIPIENTS:
            raise AssertionError("unexpected query_many SQL")
        if query == failing_query:
            raise failure or SQLAlchemyError("private recipient query detail")
        return (
            selected_recipient_rows
            if selected_recipient_rows is not None
            else [{"id": user_id} for user_id in sorted(params["recipient_ids"])]
        )

    def query_one(_db, query: str, params: dict[str, Any]):
        """Trả insert projection theo SQL constant hoặc phát lỗi đã cấu hình."""

        nonlocal next_delivery_id, delivery_call_count
        captured.append((query, dict(params)))
        if query == failing_query:
            raise failure or SQLAlchemyError("private insert query detail")
        if query == INSERT_ADMIN_NOTIFICATION:
            return next(selected_notification_rows)
        if query == INSERT_ADMIN_NOTIFICATION_DELIVERY:
            delivery_call_count += 1
            if bad_delivery:
                return {"id": "invalid"}
            delivery_id = next_delivery_id
            next_delivery_id += 1
            return {"id": delivery_id}
        raise AssertionError("unexpected query_one SQL")

    monkeypatch.setattr(notification_view, "query_many", query_many)
    monkeypatch.setattr(notification_view, "query_one", query_one)
    return captured


def test_create_admin_notification_fans_out_and_returns_direct_notification(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Ghi recipient/channel fan-out atomically và trả Notification cùng batch metadata."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_create_queries(monkeypatch)

    response = post_notification(client)

    assert response.status_code == 202
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_OPERATION_ACCEPTED"
    assert payload["data"] == {
        "id": 31001,
        "title": "Thông báo lịch học",
        "content": "Lịch học được cập nhật.",
        "channels": ["PUSH", "EMAIL"],
        "status": "QUEUED",
        "created_at": "2026-10-26T09:45:00Z",
    }
    assert UUID(payload["meta"]["operation_id"])
    assert payload["meta"]["notification_ids"] == [31001, 31002]
    assert response.headers["X-Trace-Id"] == payload["traceId"]

    assert [query for query, _params in captured] == [
        FIND_ADMIN_NOTIFICATION_RECIPIENTS,
        INSERT_ADMIN_NOTIFICATION,
        INSERT_ADMIN_NOTIFICATION_DELIVERY,
        INSERT_ADMIN_NOTIFICATION_DELIVERY,
        INSERT_ADMIN_NOTIFICATION,
        INSERT_ADMIN_NOTIFICATION_DELIVERY,
        INSERT_ADMIN_NOTIFICATION_DELIVERY,
    ]
    assert captured[0][1] == {"recipient_ids": [2002, 2001]}
    inserted_notifications = [
        params for query, params in captured if query == INSERT_ADMIN_NOTIFICATION
    ]
    assert [params["user_id"] for params in inserted_notifications] == [2002, 2001]
    assert all(params["sender_id"] == 9001 for params in inserted_notifications)
    assert all(params["title"] == "Thông báo lịch học" for params in inserted_notifications)
    assert all(params["content"] == "Lịch học được cập nhật." for params in inserted_notifications)
    assert len({params["operation_id"] for params in inserted_notifications}) == 1
    inserted_deliveries = [
        params for query, params in captured if query == INSERT_ADMIN_NOTIFICATION_DELIVERY
    ]
    assert [(item["notification_id"], item["channel"]) for item in inserted_deliveries] == [
        (31001, "PUSH"),
        (31001, "EMAIL"),
        (31002, "PUSH"),
        (31002, "EMAIL"),
    ]
    assert "user_id" not in payload["data"]
    assert session.commit_count == 1
    assert session.rollback_count == 0


def test_create_admin_notification_authenticates_before_body_or_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Missing token/wrong role được trả trước khi body sai được parse hay query DB."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)

    def fail_query(*_args, **_kwargs):
        """Phát lỗi nếu một request chưa qua auth chạm tới database."""

        raise AssertionError("database query must not run")

    monkeypatch.setattr(notification_view, "query_many", fail_query)
    missing_token = post_notification(client, body=b"{", authorization=None)
    assert missing_token.status_code == 401
    assert missing_token.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"

    allow_admin_token(monkeypatch, roles=["STUDENT"])
    wrong_role = post_notification(client, body=b"{")
    assert wrong_role.status_code == 403
    assert wrong_role.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert session.commit_count == 0
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    ("body", "field"),
    [
        (b"{", "body"),
        ({"title": "T", "content": "C", "channels": ["PUSH"]}, "recipients"),
        (request_body(recipients=[]), "recipients"),
        (request_body(recipients=None), "recipients"),
        (request_body(recipients=[2001, 2001]), "recipients"),
        (request_body(recipients=[True]), "recipients.0"),
        (request_body(recipients=[2**63]), "recipients"),
        (request_body(segment="ALL_LEARNERS"), "segment"),
        (request_body(title="  "), "title"),
        (request_body(title="T" * 201), "title"),
        (request_body(content="\n\t"), "content"),
        (request_body(channels=[]), "channels"),
        (request_body(channels=["SMS"]), "channels"),
        (request_body(channels=["PUSH", "PUSH"]), "channels"),
        (request_body(action="SEND"), "action"),
    ],
)
def test_create_admin_notification_rejects_invalid_body_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    body: Any,
    field: str,
) -> None:
    """Map malformed, unsupported or DERIVED-invalid body fields to catalog 422."""

    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Phát lỗi nếu validator không dừng trước truy vấn recipients."""

        raise AssertionError("validation must finish before database query")

    monkeypatch.setattr(notification_view, "query_many", fail_query)
    response = post_notification(client, body=body)

    assert response.status_code == 422
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert payload["data"] is None
    assert payload["meta"]["fieldErrors"][0]["field"] == field


def test_create_admin_notification_rejects_unknown_recipients_without_leaking_ids(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả lỗi validation tổng quát nếu users query không tìm thấy đủ IDs."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_create_queries(monkeypatch, recipient_rows=[{"id": 2001}])

    response = post_notification(client)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0]["code"] == "RECIPIENT_NOT_FOUND"
    assert "2002" not in response.text
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize(
    ("error", "expected_status", "expected_code"),
    [
        (
            OperationalError("select", {}, RuntimeError("private offline detail")),
            503,
            "DESIGN_DEPENDENCY_UNAVAILABLE",
        ),
        (SQLAlchemyError("private query detail"), 500, "DESIGN_INTERNAL_ERROR"),
    ],
)
def test_create_admin_notification_maps_recipient_query_failures_safely(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    error: SQLAlchemyError,
    expected_status: int,
    expected_code: str,
) -> None:
    """Map DB connection failure to 503 and other recipient query errors to 500."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_create_queries(
        monkeypatch,
        failing_query=FIND_ADMIN_NOTIFICATION_RECIPIENTS,
        failure=error,
    )

    response = post_notification(client)

    assert response.status_code == expected_status
    assert response.json()["businessCode"] == expected_code
    assert "private" not in response.text
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize(
    ("failing_query", "failure", "bad_delivery", "commit_error"),
    [
        (INSERT_ADMIN_NOTIFICATION, SQLAlchemyError("private insert"), False, None),
        (None, None, True, None),
        (
            INSERT_ADMIN_NOTIFICATION_DELIVERY,
            OperationalError("insert", {}, RuntimeError()),
            False,
            None,
        ),
        (None, None, False, SQLAlchemyError("private commit")),
    ],
)
def test_create_admin_notification_rolls_back_partial_batch_failures(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    failing_query: str | None,
    failure: SQLAlchemyError | None,
    bad_delivery: bool,
    commit_error: SQLAlchemyError | None,
) -> None:
    """Rollback một batch nếu insert, outbox projection hoặc commit không thành công."""

    session = FakeSession(commit_error=commit_error)
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_create_queries(
        monkeypatch,
        failing_query=failing_query,
        failure=failure,
        bad_delivery=bad_delivery,
    )

    response = post_notification(client)

    expected_status = 503 if isinstance(failure, OperationalError) else 500
    assert response.status_code == expected_status
    assert response.json()["businessCode"] in {
        "DESIGN_INTERNAL_ERROR",
        "DESIGN_DEPENDENCY_UNAVAILABLE",
    }
    assert "private" not in response.text
    assert session.commit_count == (1 if commit_error is not None else 0)
    assert session.rollback_count == 1


def test_create_admin_notification_rejects_malformed_insert_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Rollback khi DB projection không trả notification ID/timestamp hợp lệ."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_create_queries(
        monkeypatch, notification_rows=[{"id": "31001", "created_at": CREATED_AT}]
    )

    response = post_notification(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_create_admin_notification_openapi_declares_direct_contract_and_fallbacks(
    client: TestClient,
) -> None:
    """Kiểm tra POST route, body direct fields, exact errors và operation counts."""

    paths = client.app.openapi()["paths"]
    api_paths = {path: value for path, value in paths.items() if path.startswith("/api/v1/")}
    operation_count = sum(
        method in {"get", "post", "put", "patch", "delete"}
        for item in api_paths.values()
        for method in item
    )
    assert len(api_paths) == 57
    assert operation_count == 68

    operation = paths["/api/v1/admin/notifications"]["post"]
    assert {item["name"] for item in operation["parameters"]} == {"Authorization"}
    assert set(operation["responses"]) == {"202", "401", "403", "422", "500", "503"}
    assert operation["responses"]["202"]["content"]["application/json"]["schema"]["$ref"].endswith(
        "/CreateAdminNotificationEnvelope"
    )

    body_schema = operation["requestBody"]["content"]["application/json"]["schema"]
    assert set(body_schema["required"]) == {"title", "content", "channels"}
    assert set(body_schema["properties"]) == {
        "recipients",
        "segment",
        "title",
        "content",
        "channels",
    }
    assert body_schema["properties"]["recipients"]["items"] == {
        "type": "integer",
        "format": "int64",
        "minimum": 1,
    }
    assert body_schema["properties"]["channels"]["items"]["enum"] == ["PUSH", "EMAIL"]
