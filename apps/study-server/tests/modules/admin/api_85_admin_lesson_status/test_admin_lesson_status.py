"""HTTP tests cho Admin Lesson status API #85."""

from __future__ import annotations

from typing import Any

import app.modules.admin.api_85_admin_lesson_status.view as lesson_status_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.admin.api_85_admin_lesson_status.query import (
    INSERT_ADMIN_LESSON_STATUS_AUDIT,
    LOCK_ADMIN_LESSON_STATUS,
    UPDATE_ADMIN_LESSON_STATUS,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Đếm transaction calls và giả lập commit failure cho API #85."""

    def __init__(self, *, fail_commit: bool = False) -> None:
        """Khởi tạo bộ đếm transaction và tùy chọn lỗi commit."""

        self.commit_count = 0
        self.rollback_count = 0
        self.fail_commit = fail_commit

    def commit(self) -> None:
        """Ghi nhận commit hoặc phát sinh lỗi DB đã cấu hình."""

        self.commit_count += 1
        if self.fail_commit:
            raise SQLAlchemyError("sensitive commit detail")

    def rollback(self) -> None:
        """Ghi nhận rollback khi API lỗi hoặc không tìm thấy Lesson."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả session giả cho TestClient."""

    def dependency():
        """Yield session test cho dependency get_db."""

        yield session

    return dependency


def allow_admin_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Cài decoder giả trả JWT Admin hoặc role test được chỉ định."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": roles or ["ADMIN"]},
    )


def lesson_row(status: str = "PUBLISHED", **overrides: Any) -> dict[str, Any]:
    """Tạo projection Lesson theo aliases của API #09."""

    return {
        "id": 501,
        "course_id": 42,
        "title": "Giới thiệu khóa học",
        "content": "Nội dung bài học",
        "video_url": "https://cdn.example.test/lessons/501.mp4",
        "order": 2,
        "status": status,
        **overrides,
    }


def patch_lesson_status(
    client: TestClient,
    lesson_id: str = "501",
    *,
    target_status: str = "PUBLISHED",
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi HTTP PATCH API #85 với raw path, target status và Authorization."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.patch(
        f"/api/v1/admin/lessons/{lesson_id}/status",
        headers=headers,
        json={"status": target_status},
    )


def install_status_queries(
    monkeypatch: pytest.MonkeyPatch,
    *,
    current: Any = ...,
    updated: Any = ...,
    fail_lock: bool = False,
    fail_update: bool = False,
    fail_audit: bool = False,
) -> tuple[list[tuple[str, dict[str, Any]]], list[dict[str, Any]]]:
    """Cài DB doubles, giữ query order/bindings và audit insert parameters."""

    current_row = lesson_row("DRAFT") if current is ... else current
    updated_row = lesson_row() if updated is ... else updated
    queries: list[tuple[str, dict[str, Any]]] = []
    audit_rows: list[dict[str, Any]] = []

    def query_one(_db, query, params):
        """Trả Lesson row lock hoặc projection sau UPDATE."""

        bound = dict(params)
        queries.append((query, bound))
        if query == LOCK_ADMIN_LESSON_STATUS:
            if fail_lock:
                raise SQLAlchemyError("sensitive lock detail")
            return current_row
        if query == UPDATE_ADMIN_LESSON_STATUS:
            if fail_update:
                raise SQLAlchemyError("sensitive update detail")
            return updated_row
        raise AssertionError(f"Unexpected query: {query}")

    def execute_query(_db, query, params):
        """Ghi nhận audit insert hoặc giả lập lỗi khi append log."""

        assert query == INSERT_ADMIN_LESSON_STATUS_AUDIT
        if fail_audit:
            raise SQLAlchemyError("sensitive audit detail")
        audit_rows.append(dict(params))

    monkeypatch.setattr(lesson_status_view, "query_one", query_one)
    monkeypatch.setattr(lesson_status_view, "execute_query", execute_query)
    return queries, audit_rows


@pytest.mark.parametrize("target_status", ["PUBLISHED", "SUSPENDED"])
def test_patch_admin_lesson_status_updates_and_audits_atomically(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    target_status: str,
) -> None:
    """Đổi status, append actor/old/new và trả Lesson trước commit."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    queries, audit_rows = install_status_queries(
        monkeypatch,
        updated=lesson_row(target_status),
    )

    response = patch_lesson_status(client, target_status=target_status)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_UPDATED"
    assert payload["data"] == lesson_row(target_status)
    assert payload["meta"] == {}
    assert payload["traceId"] == response.headers["X-Trace-Id"]
    assert [query for query, _ in queries] == [
        LOCK_ADMIN_LESSON_STATUS,
        UPDATE_ADMIN_LESSON_STATUS,
    ]
    assert queries[0][1] == {"lesson_id": 501}
    assert queries[1][1] == {"lesson_id": 501, "status": target_status}
    assert audit_rows == [
        {
            "lesson_id": 501,
            "actor_user_id": 9001,
            "previous_status": "DRAFT",
            "new_status": target_status,
        }
    ]
    assert session.commit_count == 1
    assert session.rollback_count == 0

    update_sql = queries[1][0]
    assert "status = :status" in update_sql
    assert "status IS DISTINCT FROM 'DELETED'" in queries[0][0]
    assert "status IS DISTINCT FROM 'DELETED'" in update_sql
    assert "updated_at = CURRENT_TIMESTAMP" in update_sql
    assert "name =" not in update_sql
    assert "course_id =" not in update_sql


def test_patch_admin_lesson_status_same_value_is_noop_without_duplicate_audit(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Status hiện tại được trả lại mà không UPDATE hoặc tạo audit trùng."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    queries, audit_rows = install_status_queries(
        monkeypatch,
        current=lesson_row("PUBLISHED"),
    )

    response = patch_lesson_status(client, target_status="PUBLISHED")

    assert response.status_code == 200
    assert response.json()["data"] == lesson_row("PUBLISHED")
    assert [query for query, _ in queries] == [LOCK_ADMIN_LESSON_STATUS]
    assert audit_rows == []
    assert session.commit_count == 1
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    ("authorization", "roles", "expected_status", "expected_code"),
    [
        (None, None, 401, "DESIGN_AUTHENTICATION_REQUIRED"),
        ("Bearer valid-token", ["STUDENT"], 403, "DESIGN_ACCESS_DENIED"),
    ],
)
def test_patch_admin_lesson_status_checks_auth_before_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
    roles: list[str] | None,
    expected_status: int,
    expected_code: str,
) -> None:
    """Credential thiếu hoặc role sai trả lỗi mà không khóa Lesson."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    if roles is not None:
        allow_admin_token(monkeypatch, roles=roles)

    def fail_query(*_args, **_kwargs):
        """Làm test thất bại nếu DB được gọi trước authorization."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(lesson_status_view, "query_one", fail_query)

    response = patch_lesson_status(client, authorization=authorization)

    assert response.status_code == expected_status
    assert response.json()["businessCode"] == expected_code
    assert response.json()["data"] is None


@pytest.mark.parametrize(
    "lesson_id",
    ["not-an-id", "9223372036854775808", "-9223372036854775809", "1" * 21],
)
def test_patch_admin_lesson_status_maps_invalid_int64_to_422(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    lesson_id: str,
) -> None:
    """Map path sai/out-of-range thành 422 và không gọi database."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Làm test thất bại nếu path sai vẫn khóa Lesson."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(lesson_status_view, "query_one", fail_query)

    response = patch_lesson_status(client, lesson_id)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["data"] is None
    assert response.json()["meta"]["fieldErrors"][0]["field"] == "lesson_id"


@pytest.mark.parametrize(
    "body",
    [
        {},
        {"status": "ARCHIVED"},
        {"status": ""},
        {"status": 4},
        {"status": "PUBLISHED", "reason": "extra"},
    ],
)
def test_patch_admin_lesson_status_rejects_invalid_body_without_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    body: dict[str, Any],
) -> None:
    """Từ chối body thiếu/thừa field, sai type hoặc status ngoài candidate enum."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Làm test thất bại nếu body sai vẫn khóa Lesson."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(lesson_status_view, "query_one", fail_query)
    response = client.patch(
        "/api/v1/admin/lessons/501/status",
        headers={"Authorization": "Bearer valid-admin-token"},
        json=body,
    )

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["data"] is None


def test_patch_admin_lesson_status_returns_not_found_when_lock_is_empty(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Lesson không có trả catalog 404 và không thực hiện UPDATE/audit."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    queries, audit_rows = install_status_queries(monkeypatch, current=None)

    response = patch_lesson_status(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert response.json()["data"] is None
    assert [query for query, _ in queries] == [LOCK_ADMIN_LESSON_STATUS]
    assert audit_rows == []
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize(
    "current",
    [
        {},
        lesson_row(id="501"),
        lesson_row(status=4),
    ],
)
def test_patch_admin_lesson_status_rejects_malformed_locked_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    current: dict[str, Any],
) -> None:
    """Malformed lock identity/status returns safe 500 without attempting mutation."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    queries, audit_rows = install_status_queries(monkeypatch, current=current)

    response = patch_lesson_status(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert [query for query, _ in queries] == [LOCK_ADMIN_LESSON_STATUS]
    assert audit_rows == []
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize(
    ("failure", "expected_queries", "expected_audits"),
    [
        ("lock", [LOCK_ADMIN_LESSON_STATUS], 0),
        ("update", [LOCK_ADMIN_LESSON_STATUS, UPDATE_ADMIN_LESSON_STATUS], 0),
        ("audit", [LOCK_ADMIN_LESSON_STATUS, UPDATE_ADMIN_LESSON_STATUS], 0),
    ],
)
def test_patch_admin_lesson_status_rolls_back_query_and_audit_failures(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    failure: str,
    expected_queries: list[str],
    expected_audits: int,
) -> None:
    """Lock, UPDATE hoặc audit failure trả lỗi an toàn và rollback transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    queries, audit_rows = install_status_queries(
        monkeypatch,
        fail_lock=failure == "lock",
        fail_update=failure == "update",
        fail_audit=failure == "audit",
    )

    response = patch_lesson_status(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert "sensitive" not in response.text
    assert [query for query, _ in queries] == expected_queries
    assert len(audit_rows) == expected_audits
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize(
    "updated",
    [
        None,
        {},
        lesson_row(id="501"),
        lesson_row(status="DRAFT"),
        lesson_row(course_id=None),
    ],
)
def test_patch_admin_lesson_status_rejects_missing_or_invalid_update_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    updated: Any,
) -> None:
    """UPDATE projection thiếu row hoặc không thỏa Lesson contract thì rollback."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    queries, audit_rows = install_status_queries(monkeypatch, updated=updated)

    response = patch_lesson_status(client)

    expected_status = 404 if updated is None else 500
    expected_code = (
        "DESIGN_RESOURCE_NOT_FOUND" if updated is None else "DESIGN_INTERNAL_ERROR"
    )
    assert response.status_code == expected_status
    assert response.json()["businessCode"] == expected_code
    assert response.json()["data"] is None
    assert audit_rows == []
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_patch_admin_lesson_status_rolls_back_when_commit_fails(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Commit failure sau UPDATE và audit trả 500 an toàn, không lộ SQL detail."""

    session = FakeSession(fail_commit=True)
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    _queries, audit_rows = install_status_queries(monkeypatch)

    response = patch_lesson_status(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert "sensitive" not in response.text
    assert len(audit_rows) == 1
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_patch_admin_lesson_status_openapi_describes_body_and_catalog_errors(
    client: TestClient,
) -> None:
    """OpenAPI công bố PATCH, body status và tập error codes catalog."""

    operation = client.app.openapi()["paths"][
        "/api/v1/admin/lessons/{lesson_id}/status"
    ]["patch"]

    assert operation["requestBody"]["required"] is True
    assert operation["responses"]["200"]["description"] == "Successful Response"
    for code in ("401", "403", "404", "422", "500"):
        assert code in operation["responses"]
