from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID

import app.modules.mentor.api_64_mentor_notification_status.view as notification_status_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.main import app
from app.modules.mentor.api_64_mentor_notification_status.query import (
    FIND_NOTIFICATION_STATUS,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

NOTIFICATION_ID = 5005
OPERATION_ID = UUID("c29dfe4f-1668-4a2c-8fc8-396f41d82163")
SUBMITTED_AT = datetime(2026, 10, 25, 8, 0, tzinfo=UTC)
UPDATED_AT = datetime(2026, 10, 25, 8, 15, tzinfo=UTC)
TRACE_ID = "a03f8cb9-7316-4b14-9d89-11121a6a2640"


class FakeSession:
    """Theo dõi các thao tác transaction để xác nhận GET không ghi dữ liệu."""

    def __init__(self) -> None:
        """Khởi tạo bộ đếm commit/rollback của session giả."""

        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Ghi nhận commit nếu luồng API vô tình gọi mutation transaction."""

        self.commit_count += 1

    def rollback(self) -> None:
        """Ghi nhận rollback sau lỗi query hoặc projection."""

        self.rollback_count += 1


def notification_row(
    *,
    queued_count: int = 2,
    sent_count: int = 0,
    failed_count: int = 0,
    delivery_count: int | None = None,
    **overrides: Any,
) -> dict[str, Any]:
    """Tạo projection notification/outbox hợp lệ hoặc có chủ đích bị lỗi."""

    count = delivery_count
    if count is None:
        count = queued_count + sent_count + failed_count
    row: dict[str, Any] = {
        "notification_id": NOTIFICATION_ID,
        "operation_id": OPERATION_ID,
        "sender_id": 1001,
        "submitted_at": SUBMITTED_AT,
        "delivery_count": count,
        "queued_count": queued_count,
        "sent_count": sent_count,
        "failed_count": failed_count,
        "updated_at": UPDATED_AT,
    }
    row.update(overrides)
    return row


@pytest.fixture
def notification_client(monkeypatch: pytest.MonkeyPatch):
    """Tạo HTTP client, fake DB session và query state có thể điều khiển."""

    session = FakeSession()
    state: dict[str, Any] = {
        "row": notification_row(),
        "query_error": False,
        "roles": ["MENTOR"],
        "subject": "1001",
    }
    calls: list[tuple[str, dict[str, Any]]] = []

    def fake_query_one(
        db: FakeSession,
        query: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Ghi nhận query binding rồi trả hàng giả hoặc lỗi DB đã cấu hình."""

        assert db is session
        calls.append((query, dict(params or {})))
        if state["query_error"]:
            raise SQLAlchemyError("private database detail")
        return state["row"]

    def fake_get_db():
        """Yield fake session cho request API #64."""

        yield session

    def fake_decode_access_token(_token: str) -> dict[str, Any]:
        """Trả claim JWT có thể cấu hình để kiểm tra role và principal."""

        return {"sub": state["subject"], "roles": state["roles"]}

    monkeypatch.setattr(notification_status_view, "query_one", fake_query_one)
    monkeypatch.setattr(auth_utils, "decode_access_token", fake_decode_access_token)
    app.dependency_overrides[get_db] = fake_get_db
    try:
        with TestClient(app) as client:
            yield client, session, state, calls
    finally:
        app.dependency_overrides.pop(get_db, None)


def get_status(client: TestClient, notification_id: str = str(NOTIFICATION_ID)):
    """Gọi API #64 bằng Bearer Mentor và trace ID cố định cho assertion."""

    return client.get(
        f"/api/v1/mentor/notifications/{notification_id}/status",
        headers={"Authorization": "Bearer mentor-token", "X-Trace-Id": TRACE_ID},
    )


@pytest.mark.parametrize(
    ("queued_count", "sent_count", "failed_count", "expected_status"),
    [
        (2, 0, 0, "QUEUED"),
        (0, 2, 0, "SENT"),
        (0, 0, 2, "FAILED"),
        (1, 1, 0, "QUEUED"),
        (0, 1, 1, "FAILED"),
    ],
)
def test_get_notification_status_maps_local_channel_states(
    notification_client,
    queued_count: int,
    sent_count: int,
    failed_count: int,
    expected_status: str,
) -> None:
    """Ánh xạ queued/sent/failed và trường hợp nhiều channel vào Operation.status."""

    client, session, state, calls = notification_client
    state["row"] = notification_row(
        queued_count=queued_count,
        sent_count=sent_count,
        failed_count=failed_count,
    )

    response = get_status(client)

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert body["data"] == {
        "id": str(OPERATION_ID),
        "kind": "NOTIFICATION_DISPATCH",
        "status": expected_status,
        "owner_id": 1001,
        "submitted_at": "2026-10-25T08:00:00Z",
        "updated_at": "2026-10-25T08:15:00Z",
    }
    assert body["meta"] == {}
    assert body["traceId"] == TRACE_ID
    assert response.headers["X-Trace-Id"] == TRACE_ID
    assert calls == [(FIND_NOTIFICATION_STATUS, {"notification_id": NOTIFICATION_ID})]
    assert session.commit_count == 0


def test_missing_bearer_is_rejected_before_query(notification_client) -> None:
    """Trả 401 trước khi đọc notification khi thiếu Bearer header."""

    client, _session, _state, calls = notification_client

    response = client.get(f"/api/v1/mentor/notifications/{NOTIFICATION_ID}/status")

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert calls == []


def test_non_mentor_role_is_rejected_before_query(notification_client) -> None:
    """Trả 403 trước DB access khi token hợp lệ nhưng không có role Mentor."""

    client, _session, state, calls = notification_client
    state["roles"] = ["STUDENT"]

    response = get_status(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert calls == []


@pytest.mark.parametrize("path_id", ["abc", "9223372036854775808", "-9223372036854775809"])
def test_malformed_or_out_of_range_path_uses_catalog_404(
    notification_client,
    path_id: str,
) -> None:
    """Map malformed và signed-int64 overflow path vào 404 catalog, không 422."""

    client, _session, _state, calls = notification_client

    response = get_status(client, path_id)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert calls == []


def test_missing_notification_returns_404(notification_client) -> None:
    """Trả 404 khi query không có notification row tương ứng với path ID."""

    client, session, state, _calls = notification_client
    state["row"] = None

    response = get_status(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert session.commit_count == 0


def test_notification_owned_by_another_mentor_returns_403(notification_client) -> None:
    """Không trả Operation hoặc delivery metadata cho sender Mentor khác."""

    client, _session, state, _calls = notification_client
    state["row"] = notification_row(sender_id=2002)

    response = get_status(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert response.json()["data"] is None


@pytest.mark.parametrize(
    "overrides",
    [
        {"operation_id": None},
        {
            "delivery_count": 0,
            "queued_count": 0,
            "sent_count": 0,
            "failed_count": 0,
            "updated_at": None,
        },
    ],
)
def test_notification_without_dispatch_rows_returns_404(
    notification_client,
    overrides: dict[str, Any],
) -> None:
    """Trả 404 khi legacy notification chưa có Operation hoặc delivery outbox."""

    client, _session, state, _calls = notification_client
    state["row"] = notification_row(**overrides)

    response = get_status(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_query_failure_returns_safe_500(notification_client) -> None:
    """Ánh xạ lỗi SQLAlchemy thành 500 an toàn theo catalog, không lộ chi tiết."""

    client, session, state, _calls = notification_client
    state["query_error"] = True

    response = get_status(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private database detail" not in response.text
    assert session.rollback_count == 1


@pytest.mark.parametrize(
    "overrides",
    [
        {"queued_count": -1, "delivery_count": 2},
        {"queued_count": 1, "sent_count": 0, "failed_count": 0, "delivery_count": 2},
        {"sender_id": "1001"},
        {"operation_id": "c29dfe4f-1668-4a2c-8fc8-396f41d82163"},
        {"updated_at": None},
        {"notification_id": 5006},
    ],
)
def test_invalid_query_projection_returns_safe_500(
    notification_client,
    overrides: dict[str, Any],
) -> None:
    """Từ chối count, owner, UUID, timestamp hoặc notification projection sai."""

    client, session, state, _calls = notification_client
    state["row"] = notification_row(**overrides)

    response = get_status(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert session.rollback_count == 1


def test_openapi_preserves_int64_path_exact_catalog_errors_and_no_body() -> None:
    """Xác nhận OpenAPI khai báo raw path là int64 và không tự thêm 422/body."""

    schema = app.openapi()
    operation = schema["paths"][
        "/api/v1/mentor/notifications/{notification_id}/status"
    ]["get"]
    path_parameter = next(
        parameter for parameter in operation["parameters"] if parameter["name"] == "notification_id"
    )
    authorization_parameter = next(
        parameter for parameter in operation["parameters"] if parameter["name"] == "Authorization"
    )

    assert path_parameter["schema"] == {"type": "integer", "format": "int64"}
    assert authorization_parameter["in"] == "header"
    assert authorization_parameter["required"] is False
    assert authorization_parameter["schema"] == {"type": "string"}
    assert set(operation["responses"]) == {"200", "401", "403", "404", "500"}
    assert "requestBody" not in operation
