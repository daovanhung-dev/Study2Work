from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID

import app.modules.shared.api_18_operations.view as operation_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.shared.api_18_operations.query import FIND_NOTIFICATION_OPERATION
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

OPERATION_ID = UUID("c29dfe4f-1668-4a2c-8fc8-396f41d82163")
SUBMITTED_AT = datetime(2026, 10, 25, 8, 0, tzinfo=UTC)
UPDATED_AT = datetime(2026, 10, 25, 8, 15, tzinfo=UTC)
TRACE_ID = "a03f8cb9-7316-4b14-9d89-11121a6a2640"


class FakeSession:
    """Theo dõi rollback và đảm bảo API GET không commit dữ liệu."""

    def __init__(self) -> None:
        """Khởi tạo bộ đếm transaction cho request giả lập."""

        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Ghi nhận nếu luồng đọc vô tình commit transaction."""

        self.commit_count += 1

    def rollback(self) -> None:
        """Ghi nhận rollback sau lỗi query hoặc mapping."""

        self.rollback_count += 1


def operation_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection Operation notification hợp lệ hoặc có chủ đích bị ghi đè."""

    return {
        "id": OPERATION_ID,
        "owner_id": 1001,
        "submitted_at": SUBMITTED_AT,
        "updated_at": UPDATED_AT,
        "status": "QUEUED",
        **overrides,
    }


@pytest.fixture
def operation_client(client: TestClient, monkeypatch: pytest.MonkeyPatch):
    """Cấp HTTP client, DB giả và JWT claims có thể đổi theo từng ca kiểm thử."""

    session = FakeSession()
    state: dict[str, Any] = {
        "row": operation_row(),
        "query_error": False,
        "roles": ["STUDENT"],
        "subject": "1001",
    }
    calls: list[tuple[str, dict[str, Any]]] = []

    def fake_query_one(
        db: FakeSession,
        query: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Lưu SQL bindings rồi trả hàng giả hoặc lỗi database đã cấu hình."""

        assert db is session
        calls.append((query, dict(params or {})))
        if state["query_error"]:
            raise SQLAlchemyError("private database detail")
        return state["row"]

    def fake_get_db():
        """Yield session giả cho dependency database của HTTP request."""

        yield session

    def fake_decode_access_token(_token: str) -> dict[str, Any]:
        """Trả JWT subject và roles có thể cấu hình trong test."""

        return {"sub": state["subject"], "roles": state["roles"]}

    previous_db_override = client.app.dependency_overrides.get(get_db)
    client.app.dependency_overrides[get_db] = fake_get_db
    monkeypatch.setattr(operation_view, "query_one", fake_query_one)
    monkeypatch.setattr(auth_utils, "decode_access_token", fake_decode_access_token)
    try:
        yield client, session, state, calls
    finally:
        if previous_db_override is None:
            client.app.dependency_overrides.pop(get_db, None)
        else:
            client.app.dependency_overrides[get_db] = previous_db_override


def get_operation(client: TestClient, operation_id: str = str(OPERATION_ID)):
    """Gọi GET API #18 với Bearer token và trace ID cố định."""

    return client.get(
        f"/api/v1/operations/{operation_id}",
        headers={"Authorization": "Bearer valid-token", "X-Trace-Id": TRACE_ID},
    )


@pytest.mark.parametrize("role", ["STUDENT", "MENTOR", "ADMIN"])
def test_get_operation_allows_documented_roles_and_binds_owner(
    operation_client,
    role: str,
) -> None:
    """Cho phép các role trong sơ đồ AC nhưng chỉ query operation của caller."""

    client, session, state, calls = operation_client
    state["roles"] = [role]

    response = get_operation(client)

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["businessCode"] == "DESIGN_OPERATION_RETRIEVED"
    assert payload["data"] == {
        "id": str(OPERATION_ID),
        "kind": "NOTIFICATION_DISPATCH",
        "status": "QUEUED",
        "owner_id": 1001,
        "submitted_at": "2026-10-25T08:00:00Z",
        "updated_at": "2026-10-25T08:15:00Z",
    }
    assert payload["meta"] == {}
    assert payload["traceId"] == TRACE_ID
    assert response.headers["X-Trace-Id"] == TRACE_ID
    assert calls == [
        (
            FIND_NOTIFICATION_OPERATION,
            {"operation_id": OPERATION_ID, "owner_id": 1001},
        )
    ]
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_operation_rejects_missing_bearer_before_query(operation_client) -> None:
    """Trả 401 và không truy vấn DB khi thiếu Bearer header."""

    client, _session, _state, calls = operation_client

    response = client.get(f"/api/v1/operations/{OPERATION_ID}")

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert calls == []


def test_get_operation_rejects_unlisted_role_before_query(operation_client) -> None:
    """Trả 403 trước DB access khi token có role ngoài sơ đồ AC."""

    client, _session, state, calls = operation_client
    state["roles"] = ["GUEST"]

    response = get_operation(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert calls == []


def test_get_operation_rejects_malformed_uuid_before_query(operation_client) -> None:
    """Map malformed UUID path thành 404 catalog sau khi xác thực caller."""

    client, _session, _state, calls = operation_client

    response = get_operation(client, "not-a-uuid")

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert calls == []


def test_get_operation_returns_404_for_missing_or_non_owned_operation(
    operation_client,
) -> None:
    """Ẩn operation vắng mặt hoặc không thuộc caller theo owner-bound query hiện tại."""

    client, _session, state, calls = operation_client
    state["row"] = None

    response = get_operation(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert calls == [
        (
            FIND_NOTIFICATION_OPERATION,
            {"operation_id": OPERATION_ID, "owner_id": 1001},
        )
    ]


def test_get_operation_maps_query_error_to_safe_500(operation_client) -> None:
    """Rollback và trả lỗi nội bộ an toàn khi truy vấn operation thất bại."""

    client, session, state, calls = operation_client
    state["query_error"] = True

    response = get_operation(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private database detail" not in response.text
    assert len(calls) == 1
    assert session.rollback_count == 1
