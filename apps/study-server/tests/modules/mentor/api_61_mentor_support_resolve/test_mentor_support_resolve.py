from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import app.modules.mentor.api_61_mentor_support_resolve.view as resolve_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.mentor.api_59_mentor_support_request_detail.query import (
    LIST_MENTOR_SUPPORT_REQUEST_MESSAGES,
)
from app.modules.mentor.api_61_mentor_support_resolve.query import (
    LOCK_MENTOR_SUPPORT_REQUEST_FOR_RESOLVE,
    UPDATE_MENTOR_SUPPORT_REQUEST_RESOLVED,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Theo dõi commit và rollback của mutation API #61."""

    def __init__(self, *, commit_error: bool = False) -> None:
        """Khởi tạo bộ đếm giao dịch và lỗi commit tùy chọn."""
        self.commit_count = 0
        self.rollback_count = 0
        self.commit_error = commit_error

    def commit(self) -> None:
        """Ghi nhận commit sau khi response projection hợp lệ."""
        self.commit_count += 1
        if self.commit_error:
            raise SQLAlchemyError("private commit detail")

    def rollback(self) -> None:
        """Ghi nhận rollback khi request không hoàn tất."""
        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency cung cấp fake session cho HTTP request."""

    def dependency():
        """Yield session giả lập."""
        yield session

    return dependency


def allow_mentor_token(monkeypatch: pytest.MonkeyPatch, *, roles: list[str] | None = None) -> None:
    """Thay JWT decoder bằng principal Mentor numeric dùng trong test."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "1001", "roles": roles or ["MENTOR"]},
    )


def request_row(**overrides: Any) -> dict[str, Any]:
    """Tạo parent projection hợp lệ cho SupportRequest và các FK cha."""

    return {
        "id": 59001,
        "course_id": 120,
        "parent_course_id": 120,
        "mentor_id": 1001,
        "student_id": 2042,
        "status": "OPEN",
        "created_at": datetime(2026, 10, 24, 8, 20, tzinfo=UTC),
        "resolved_at": None,
        "student_user_id": 2042,
        "student_full_name": "Nguyễn An",
        "student_avatar_url": None,
        **overrides,
    }


def thread_row(**overrides: Any) -> dict[str, Any]:
    """Tạo một message hợp lệ trong full thread projection."""

    return {
        "request_id": 59001,
        "course_id": 120,
        "parent_course_id": 120,
        "mentor_id": 1001,
        "message_id": 90002,
        "author_id": 1001,
        "author_user_id": 1001,
        "author_role": "MENTOR",
        "author_full_name": "Trần Mentor",
        "author_avatar_url": None,
        "content": "Mình đã gửi hướng dẫn xử lý.",
        "message_created_at": datetime(2026, 10, 25, 9, 0, tzinfo=UTC),
        "linked_upload_id": None,
        "attachment_id": None,
        "attachment_name": None,
        "attachment_url": None,
        "attachment_content_type": None,
        "attachment_size_bytes": None,
        "attachment_status": None,
        **overrides,
    }


def patch_resolve(
    client: TestClient,
    *,
    request_id: str = "59001",
    authorization: str | None = "Bearer valid-token",
):
    """Gửi PATCH API #61 với path và Bearer token mặc định."""

    headers = {} if authorization is None else {"Authorization": authorization}
    return client.patch(f"/api/v1/mentor/support/{request_id}/resolve", headers=headers)


@pytest.mark.parametrize("status_value", ["OPEN", "IN_PROGRESS", "WAITING_LEARNER"])
def test_resolve_transitions_active_status_and_returns_full_thread(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    status_value: str,
) -> None:
    """Mọi active state được resolve và trả cùng full thread projection."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    resolved_at = datetime(2026, 10, 25, 9, 30, tzinfo=UTC)
    one_calls: list[tuple[str, dict[str, Any]]] = []
    many_calls: list[tuple[str, dict[str, Any]]] = []

    def query_one(_db, query, params):
        one_calls.append((query, params))
        if query == LOCK_MENTOR_SUPPORT_REQUEST_FOR_RESOLVE:
            return request_row(status=status_value)
        assert query == UPDATE_MENTOR_SUPPORT_REQUEST_RESOLVED
        return {"id": 59001, "status": "RESOLVED", "resolved_at": resolved_at}

    def query_many(_db, query, params):
        many_calls.append((query, params))
        assert query == LIST_MENTOR_SUPPORT_REQUEST_MESSAGES
        return [thread_row()]

    monkeypatch.setattr(resolve_view, "query_one", query_one)
    monkeypatch.setattr(resolve_view, "query_many", query_many)

    response = patch_resolve(client)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_UPDATED"
    assert payload["data"]["status"] == "RESOLVED"
    assert payload["data"]["resolved_at"] == "2026-10-25T09:30:00Z"
    assert payload["data"]["messages"][0]["content"] == "Mình đã gửi hướng dẫn xử lý."
    assert payload["data"]["messages"][0]["attachments"] == []
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert one_calls == [
        (LOCK_MENTOR_SUPPORT_REQUEST_FOR_RESOLVE, {"request_id": 59001}),
        (
            UPDATE_MENTOR_SUPPORT_REQUEST_RESOLVED,
            {"request_id": 59001, "mentor_id": 1001},
        ),
    ]
    assert many_calls == [
        (LIST_MENTOR_SUPPORT_REQUEST_MESSAGES, {"request_id": 59001, "mentor_id": 1001})
    ]
    assert session.commit_count == 1
    assert session.rollback_count == 0


def test_resolve_is_idempotent_for_resolved_request_and_skips_update(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Request đã RESOLVED trả success và giữ nguyên resolved_at."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    original_time = datetime(2026, 10, 24, 12, 0, tzinfo=UTC)
    one_calls: list[str] = []

    def query_one(_db, query, _params):
        one_calls.append(query)
        assert query == LOCK_MENTOR_SUPPORT_REQUEST_FOR_RESOLVE
        return request_row(status="RESOLVED", resolved_at=original_time)

    monkeypatch.setattr(resolve_view, "query_one", query_one)
    monkeypatch.setattr(
        resolve_view,
        "query_many",
        lambda _db, query, _params: (
            [thread_row()] if query == LIST_MENTOR_SUPPORT_REQUEST_MESSAGES else pytest.fail()
        ),
    )

    response = patch_resolve(client)

    assert response.status_code == 200
    assert response.json()["data"]["resolved_at"] == "2026-10-24T12:00:00Z"
    assert one_calls == [LOCK_MENTOR_SUPPORT_REQUEST_FOR_RESOLVE]
    assert session.commit_count == 1
    assert session.rollback_count == 0


def test_resolve_rejects_cancelled_state_without_update(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """CANCELLED là state terminal không được đổi sang RESOLVED."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    calls: list[str] = []

    def query_one(_db, query, _params):
        calls.append(query)
        return request_row(status="CANCELLED")

    monkeypatch.setattr(resolve_view, "query_one", query_one)

    response = patch_resolve(client)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["data"] is None
    assert calls == [LOCK_MENTOR_SUPPORT_REQUEST_FOR_RESOLVE]
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize(
    ("row", "expected_status", "expected_code"),
    [
        (None, 404, "DESIGN_RESOURCE_NOT_FOUND"),
        (request_row(mentor_id=2002), 403, "DESIGN_ACCESS_DENIED"),
    ],
)
def test_resolve_classifies_missing_and_other_owner(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    row: dict[str, Any] | None,
    expected_status: int,
    expected_code: str,
) -> None:
    """Request không tồn tại trả 404, request ngoài owner scope trả 403."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(resolve_view, "query_one", lambda *_args, **_kwargs: row)

    response = patch_resolve(client)

    assert response.status_code == expected_status
    assert response.json()["businessCode"] == expected_code
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_resolve_rechecks_concurrent_resolved_state_and_keeps_timestamp(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Conditional update miss re-reads a concurrently resolved request idempotently."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    original_time = datetime(2026, 10, 25, 8, 0, tzinfo=UTC)
    lookup_count = 0

    def query_one(_db, query, _params):
        nonlocal lookup_count
        if query == UPDATE_MENTOR_SUPPORT_REQUEST_RESOLVED:
            return None
        assert query == LOCK_MENTOR_SUPPORT_REQUEST_FOR_RESOLVE
        lookup_count += 1
        if lookup_count == 1:
            return request_row()
        return request_row(status="RESOLVED", resolved_at=original_time)

    monkeypatch.setattr(resolve_view, "query_one", query_one)
    monkeypatch.setattr(resolve_view, "query_many", lambda *_args: [thread_row()])

    response = patch_resolve(client)

    assert response.status_code == 200
    assert response.json()["data"]["resolved_at"] == "2026-10-25T08:00:00Z"
    assert session.commit_count == 1
    assert session.rollback_count == 0


def test_resolve_rejects_invalid_path_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Malformed and overflow signed-int64 paths use catalog 422 without DB access."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        resolve_view,
        "query_one",
        lambda *_args, **_kwargs: pytest.fail("database queried for invalid path"),
    )

    for invalid_id in ("abc", str(2**63)):
        response = patch_resolve(client, request_id=invalid_id)
        assert response.status_code == 422
        assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_resolve_authenticates_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Missing token and wrong role stop before any database query."""

    monkeypatch.setattr(
        resolve_view,
        "query_one",
        lambda *_args, **_kwargs: pytest.fail("database queried before Mentor auth"),
    )
    response = patch_resolve(client, authorization=None)
    assert response.status_code == 401

    allow_mentor_token(monkeypatch, roles=["STUDENT"])
    response = patch_resolve(client)
    assert response.status_code == 403


def test_resolve_rolls_back_database_and_projection_failures(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """DB/thread mapping failure returns safe 500 and rolls back the pending update."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    resolved_at = datetime(2026, 10, 25, 9, 30, tzinfo=UTC)

    def query_one(_db, query, _params):
        if query == LOCK_MENTOR_SUPPORT_REQUEST_FOR_RESOLVE:
            return request_row()
        assert query == UPDATE_MENTOR_SUPPORT_REQUEST_RESOLVED
        return {"id": 59001, "status": "RESOLVED", "resolved_at": resolved_at}

    monkeypatch.setattr(resolve_view, "query_one", query_one)
    monkeypatch.setattr(
        resolve_view,
        "query_many",
        lambda *_args: (_ for _ in ()).throw(SQLAlchemyError("private query detail")),
    )

    response = patch_resolve(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private query detail" not in response.text
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_resolve_rolls_back_commit_failure_safely(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Commit failure is hidden from the client and triggers rollback."""

    session = FakeSession(commit_error=True)
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    resolved_at = datetime(2026, 10, 25, 9, 30, tzinfo=UTC)

    def query_one(_db, query, _params):
        if query == LOCK_MENTOR_SUPPORT_REQUEST_FOR_RESOLVE:
            return request_row()
        assert query == UPDATE_MENTOR_SUPPORT_REQUEST_RESOLVED
        return {"id": 59001, "status": "RESOLVED", "resolved_at": resolved_at}

    monkeypatch.setattr(resolve_view, "query_one", query_one)
    monkeypatch.setattr(resolve_view, "query_many", lambda *_args: [thread_row()])

    response = patch_resolve(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private commit detail" not in response.text
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_resolve_openapi_has_patch_int64_path_and_no_body(client: TestClient) -> None:
    """OpenAPI exposes PATCH, signed-int64 path and no request body for API #61."""

    operation = client.app.openapi()["paths"][
        "/api/v1/mentor/support/{request_id}/resolve"
    ]["patch"]
    path_parameter = next(item for item in operation["parameters"] if item["name"] == "request_id")

    assert path_parameter["schema"]["type"] == "integer"
    assert path_parameter["schema"]["format"] == "int64"
    assert "requestBody" not in operation
