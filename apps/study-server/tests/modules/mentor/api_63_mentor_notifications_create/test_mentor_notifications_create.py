from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID

import app.modules.mentor.api_63_mentor_notifications_create.view as notification_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.mentor.api_63_mentor_notifications_create.query import (
    FIND_COMMON_MENTOR_COURSE_FOR_RECIPIENTS,
    INSERT_NOTIFICATION,
    INSERT_NOTIFICATION_DELIVERY,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError, SQLAlchemyError

CREATED_AT = datetime(2026, 10, 25, 10, 30, tzinfo=UTC)


class FakeSession:
    """Theo dõi commit/rollback và mô phỏng lỗi commit của API #63."""

    def __init__(self, *, commit_error: bool = False) -> None:
        """Khởi tạo bộ đếm transaction và cờ lỗi commit."""
        self.commit_count = 0
        self.rollback_count = 0
        self.commit_error = commit_error

    def commit(self) -> None:
        """Ghi nhận commit hoặc mô phỏng database unavailable khi commit."""
        self.commit_count += 1
        if self.commit_error:
            raise OperationalError("commit", {}, RuntimeError("private DB error"))

    def rollback(self) -> None:
        """Ghi nhận rollback khi scope, persistence hoặc projection thất bại."""
        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo FastAPI dependency override dùng FakeSession."""

    def dependency():
        """Yield session giả lập cho request đang kiểm thử."""
        yield session

    return dependency


def allow_mentor_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Thay decoder để trả numeric Mentor principal cho test HTTP."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "1001", "roles": roles or ["MENTOR"]},
    )


def request_body(**overrides: Any) -> dict[str, Any]:
    """Tạo body API #63 hợp lệ theo catalog và local CSV fallback."""

    return {
        "recipients": "2001,2002",
        "title": "Thong bao lop hoc",
        "content": 123,
        "channels": "PUSH,EMAIL",
        **overrides,
    }


def scope_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection xác nhận toàn bộ recipients cùng thuộc một course."""

    return {"course_id": 101, "matched_count": 2, **overrides}


def notification_row(notification_id: int = 30001) -> dict[str, Any]:
    """Tạo projection Notification insert hợp lệ."""

    return {"id": notification_id, "created_at": CREATED_AT}


def delivery_row(delivery_id: int = 40001) -> dict[str, int]:
    """Tạo projection delivery outbox insert hợp lệ."""

    return {"id": delivery_id}


def post_notification(
    client: TestClient,
    *,
    body: dict[str, Any] | None = None,
    authorization: str | None = "Bearer valid-token",
):
    """Gửi POST API #63 qua TestClient với body và Bearer mặc định."""

    headers = {} if authorization is None else {"Authorization": authorization}
    return client.post(
        "/api/v1/mentor/notifications",
        json=body or request_body(),
        headers=headers,
    )


def successful_query_one(captured: list[tuple[str, dict[str, Any]]]):
    """Tạo query fake tuần tự cho scope, Notification rows và delivery outbox."""

    notification_ids = iter([30001, 30002])
    delivery_ids = iter([40001, 40002, 40003, 40004])

    def query_one(_db, query: str, params: dict[str, Any]):
        """Lưu query/bindings và trả projection phù hợp với từng SQL constant."""

        captured.append((query, params))
        if query == FIND_COMMON_MENTOR_COURSE_FOR_RECIPIENTS:
            return scope_row(matched_count=len(params["recipient_ids"]))
        if query == INSERT_NOTIFICATION:
            return notification_row(next(notification_ids))
        if query == INSERT_NOTIFICATION_DELIVERY:
            return delivery_row(next(delivery_ids))
        raise AssertionError(f"Unexpected SQL constant: {query}")

    return query_one


def test_create_notification_queues_all_recipients_and_channels(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 202 Operation sau khi lưu Notification/outbox theo đúng thứ tự."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: list[tuple[str, dict[str, Any]]] = []
    monkeypatch.setattr(notification_view, "query_one", successful_query_one(captured))

    response = post_notification(
        client,
        body=request_body(
            recipients=" 2002,2001,2002 ",
            channels="PUSH,EMAIL,PUSH",
        ),
    )

    assert response.status_code == 202
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_OPERATION_ACCEPTED"
    assert payload["data"]["kind"] == "NOTIFICATION_DISPATCH"
    assert payload["data"]["status"] == "QUEUED"
    assert UUID(payload["data"]["id"])
    assert payload["data"]["owner_id"] == 1001
    assert payload["data"]["submitted_at"] == "2026-10-25T10:30:00Z"
    assert payload["data"]["updated_at"] == payload["data"]["submitted_at"]
    assert "completed_at" not in payload["data"]
    assert "result" not in payload["data"]
    assert payload["meta"]["notification_ids"] == [30001, 30002]
    assert response.headers["X-Trace-Id"] == payload["traceId"]

    assert [query for query, _params in captured] == [
        FIND_COMMON_MENTOR_COURSE_FOR_RECIPIENTS,
        INSERT_NOTIFICATION,
        INSERT_NOTIFICATION_DELIVERY,
        INSERT_NOTIFICATION_DELIVERY,
        INSERT_NOTIFICATION,
        INSERT_NOTIFICATION_DELIVERY,
        INSERT_NOTIFICATION_DELIVERY,
    ]
    assert captured[0][1] == {
        "mentor_id": 1001,
        "recipient_ids": [2002, 2001],
        "recipient_count": 2,
    }
    inserted_notifications = [
        params for query, params in captured if query == INSERT_NOTIFICATION
    ]
    assert [params["user_id"] for params in inserted_notifications] == [2002, 2001]
    assert all(params["sender_id"] == 1001 for params in inserted_notifications)
    assert all(params["content"] == "123" for params in inserted_notifications)
    assert len({params["operation_id"] for params in inserted_notifications}) == 1
    inserted_deliveries = [
        params for query, params in captured if query == INSERT_NOTIFICATION_DELIVERY
    ]
    assert [(item["notification_id"], item["channel"]) for item in inserted_deliveries] == [
        (30001, "PUSH"),
        (30001, "EMAIL"),
        (30002, "PUSH"),
        (30002, "EMAIL"),
    ]
    assert "e.status = 'ACTIVE'" in captured[0][0]
    assert "u.role = 'STUDENT'" in captured[0][0]
    assert "c.mentor_id = :mentor_id" in captured[0][0]
    assert "HAVING COUNT(DISTINCT u.id) = :recipient_count" in captured[0][0]
    assert session.commit_count == 1
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    "recipients",
    ["", "abc", "0", "-1", "1,,2", "9223372036854775808"],
)
def test_create_notification_rejects_invalid_recipient_csv_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    recipients: str,
) -> None:
    """Map recipient CSV parse failures to catalog 422 without a database query."""

    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        notification_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    response = post_notification(client, body=request_body(recipients=recipients))

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0]["field"] == "recipients"
    assert response.json()["data"] is None


@pytest.mark.parametrize("channels", ["", "SMS", "PUSH,", "EMAIL, SMS"])
def test_create_notification_rejects_invalid_channel_csv_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    channels: str,
) -> None:
    """Map empty, malformed or unsupported channel tokens to catalog 422."""

    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        notification_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    response = post_notification(client, body=request_body(channels=channels))

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0]["field"] == "channels"


@pytest.mark.parametrize("authorization", [None, "Basic token", "Bearer"])
def test_create_notification_rejects_invalid_auth_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
) -> None:
    """Map missing or malformed Bearer credentials to 401 before all queries."""

    monkeypatch.setattr(
        notification_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    response = post_notification(client, authorization=authorization)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert response.json()["data"] is None


def test_create_notification_rejects_non_mentor_role_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map a Student principal to 403 without reading recipient data."""

    allow_mentor_token(monkeypatch, roles=["STUDENT"])
    monkeypatch.setattr(
        notification_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    response = post_notification(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"


def test_create_notification_denies_recipients_without_common_owned_course(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối toàn bộ recipient set khi không có common ACTIVE owned roster."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: list[tuple[str, dict[str, Any]]] = []
    monkeypatch.setattr(
        notification_view,
        "query_one",
        lambda _db, query, params: captured.append((query, params)) or None,
    )

    response = post_notification(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert captured == [
        (
            FIND_COMMON_MENTOR_COURSE_FOR_RECIPIENTS,
            {"mentor_id": 1001, "recipient_ids": [2001, 2002], "recipient_count": 2},
        )
    ]
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_create_notification_returns_503_for_database_unavailable(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map connection loss during scope lookup to catalog 503 and rollback."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        notification_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            OperationalError("scope", {}, RuntimeError("private DB error"))
        ),
    )

    response = post_notification(client)

    assert response.status_code == 503
    assert response.json()["businessCode"] == "DESIGN_DEPENDENCY_UNAVAILABLE"
    assert "private DB error" not in response.text
    assert session.rollback_count == 1


def test_create_notification_returns_500_for_unexpected_query_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map non-connection SQL failures to safe catalog 500."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        notification_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(SQLAlchemyError("private query")),
    )

    response = post_notification(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private query" not in response.text
    assert session.rollback_count == 1


def test_create_notification_rolls_back_when_delivery_projection_is_invalid(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Rollback Notification inserts when an outbox insert has an invalid projection."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    calls = 0

    def query_one(_db, query: str, _params: dict[str, Any]):
        """Trả scope và notification hợp lệ nhưng delivery row sai shape."""

        nonlocal calls
        calls += 1
        if query == FIND_COMMON_MENTOR_COURSE_FOR_RECIPIENTS:
            return scope_row()
        if query == INSERT_NOTIFICATION:
            return notification_row()
        if query == INSERT_NOTIFICATION_DELIVERY:
            return {"id": "invalid"}
        raise AssertionError(f"Unexpected SQL constant: {query}")

    monkeypatch.setattr(notification_view, "query_one", query_one)

    response = post_notification(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert calls == 3
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_create_notification_returns_503_when_commit_fails(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Rollback and avoid 202 when the durable outbox transaction cannot commit."""

    session = FakeSession(commit_error=True)
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured: list[tuple[str, dict[str, Any]]] = []
    monkeypatch.setattr(notification_view, "query_one", successful_query_one(captured))

    response = post_notification(client)

    assert response.status_code == 503
    assert response.json()["businessCode"] == "DESIGN_DEPENDENCY_UNAVAILABLE"
    assert response.json()["data"] is None
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_create_notification_maps_malformed_scope_projection_to_500(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Treat malformed ownership/count projection as an internal integrity failure."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        notification_view,
        "query_one",
        lambda *_args, **_kwargs: {"course_id": True, "matched_count": 2},
    )

    response = post_notification(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1


def test_create_notification_rejects_body_type_and_title_limit(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Use FastAPI request validation for direct int64 type and DDL title bound."""

    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        notification_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    string_content = post_notification(client, body=request_body(content="123"))
    long_title = post_notification(client, body=request_body(title="x" * 201))

    assert string_content.status_code == 422
    assert string_content.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert long_title.status_code == 422
    assert long_title.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"


def test_create_notification_openapi_preserves_catalog_body_and_operation(
    client: TestClient,
) -> None:
    """Expose JSON fields and int64 content with a 202 Operation response schema."""

    openapi = client.app.openapi()
    operation = openapi["paths"]["/api/v1/mentor/notifications"]["post"]
    request_schema = operation["requestBody"]["content"]["application/json"]["schema"]
    response_schema = operation["responses"]["202"]["content"]["application/json"]["schema"]
    request_model = openapi["components"]["schemas"][request_schema["$ref"].split("/")[-1]]

    assert request_model["required"] == ["recipients", "title", "content", "channels"]
    assert request_model["properties"]["content"]["type"] == "integer"
    assert request_model["properties"]["content"]["format"] == "int64"
    assert response_schema["$ref"].endswith("CreateNotificationEnvelope")
