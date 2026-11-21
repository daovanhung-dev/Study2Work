"""HTTP tests cho API #86 xóa mềm Lesson trong Admin."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import app.modules.admin.api_86_admin_lesson_delete.view as delete_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.admin.api_86_admin_lesson_delete.query import (
    CHECK_ADMIN_LESSON_DELETE_DEPENDENCIES,
    LOCK_ADMIN_LESSON_FOR_DELETE,
    SOFT_DELETE_ADMIN_LESSON,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

_UNSET = object()


class FakeSession:
    """Session giả để kiểm tra commit và rollback API #86."""

    def __init__(self, *, fail_commit: bool = False) -> None:
        """Khởi tạo bộ đếm transaction và tùy chọn lỗi commit."""

        self.commit_count = 0
        self.rollback_count = 0
        self.fail_commit = fail_commit

    def commit(self) -> None:
        """Ghi nhận commit hoặc giả lập lỗi DB đã cấu hình."""

        self.commit_count += 1
        if self.fail_commit:
            raise SQLAlchemyError("sensitive commit detail")

    def rollback(self) -> None:
        """Ghi nhận rollback của nhánh lỗi."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả session giả cho TestClient."""

    def dependency():
        """Cung cấp session giả cho một HTTP request."""

        yield session

    return dependency


def allow_admin_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Cài decoder giả trả principal Admin hoặc role do test chọn."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": roles or ["ADMIN"]},
    )


def delete_request(
    client: TestClient,
    lesson_id: str,
    *,
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi HTTP DELETE API #86 với raw path và Authorization tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.request(
        "DELETE",
        f"/api/v1/admin/lessons/{lesson_id}",
        headers=headers,
    )


def deleted_lesson_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection UPDATE RETURNING gồm Lesson ID và timestamp."""

    return {
        "id": 501,
        "deleted_at": datetime(2026, 10, 26, 10, 30),
        **overrides,
    }


def install_delete_queries(
    monkeypatch: pytest.MonkeyPatch,
    *,
    lock_row: Any = _UNSET,
    dependency_row: Any = _UNSET,
    deleted_row: Any = _UNSET,
    fail_query: str | None = None,
) -> list[tuple[str, dict[str, Any]]]:
    """Ghi lại SQL/bindings và mô phỏng query result hoặc lỗi DB."""

    captured: list[tuple[str, dict[str, Any]]] = []
    results = {
        LOCK_ADMIN_LESSON_FOR_DELETE: (
            {"id": 501, "status": "PUBLISHED"} if lock_row is _UNSET else lock_row
        ),
        CHECK_ADMIN_LESSON_DELETE_DEPENDENCIES: (
            {"has_progress": False, "has_resources": False, "has_uploads": False}
            if dependency_row is _UNSET
            else dependency_row
        ),
        SOFT_DELETE_ADMIN_LESSON: (
            deleted_lesson_row() if deleted_row is _UNSET else deleted_row
        ),
    }

    def query_one(_db: Any, query: str, params: dict[str, Any]) -> Any:
        """Ghi statement và trả row đã cấu hình hoặc database failure."""

        captured.append((query, dict(params)))
        if query == fail_query:
            raise SQLAlchemyError("sensitive query detail")
        if query not in results:
            raise AssertionError("unexpected query")
        return results[query]

    monkeypatch.setattr(delete_view, "query_one", query_one)
    return captured


def test_delete_soft_marks_lesson_and_returns_database_timestamp(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Ghi marker DELETED, giữ dependency/audit rows và trả timestamp DB."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_delete_queries(monkeypatch)

    response = delete_request(client, "501")

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_DELETED"
    assert payload["data"] == {
        "id": 501,
        "status": "deleted",
        "deleted_at": "2026-10-26T10:30:00",
    }
    assert payload["meta"] == {}
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert captured == [
        (LOCK_ADMIN_LESSON_FOR_DELETE, {"lesson_id": 501}),
        (CHECK_ADMIN_LESSON_DELETE_DEPENDENCIES, {"lesson_id": 501}),
        (SOFT_DELETE_ADMIN_LESSON, {"lesson_id": 501}),
    ]
    assert "status = 'DELETED'" in SOFT_DELETE_ADMIN_LESSON
    assert "updated_at = CURRENT_TIMESTAMP" in SOFT_DELETE_ADMIN_LESSON
    assert "DELETE FROM" not in SOFT_DELETE_ADMIN_LESSON.upper()
    assert "lesson_status_audit_logs" not in SOFT_DELETE_ADMIN_LESSON
    assert session.commit_count == 1
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    "dependency_row",
    [
        {"has_progress": True, "has_resources": False, "has_uploads": False},
        {"has_progress": False, "has_resources": True, "has_uploads": False},
        {"has_progress": False, "has_resources": False, "has_uploads": True},
    ],
)
def test_delete_blocks_lesson_with_progress_or_linked_resources(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    dependency_row: dict[str, bool],
) -> None:
    """Trả catalog 422 và không mutation khi có progress/reference."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_delete_queries(monkeypatch, dependency_row=dependency_row)

    response = delete_request(client, "501")

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["data"] is None
    assert len(captured) == 2
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_delete_returns_not_found_for_missing_or_already_deleted_lesson(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map Lesson không có trong tập chưa xóa sang catalog 404."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_delete_queries(monkeypatch, lock_row=None)

    response = delete_request(client, "501")

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert response.json()["data"] is None
    assert captured == [(LOCK_ADMIN_LESSON_FOR_DELETE, {"lesson_id": 501})]
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize("lesson_id", ["abc", str(2**63), str(-(2**63) - 1)])
def test_delete_rejects_malformed_or_out_of_range_int64_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    lesson_id: str,
) -> None:
    """Map raw path không phải signed-int64 sang catalog 422 trước query."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_delete_queries(monkeypatch)

    response = delete_request(client, lesson_id)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert captured == []
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_delete_requires_authentication_and_admin_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối thiếu token hoặc role không phải ADMIN trước mọi truy vấn."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    captured = install_delete_queries(monkeypatch)

    no_token = delete_request(client, "501", authorization=None)
    allow_admin_token(monkeypatch, roles=["STUDENT"])
    wrong_role = delete_request(client, "501")

    assert no_token.status_code == 401
    assert no_token.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert wrong_role.status_code == 403
    assert wrong_role.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert captured == []
    assert session.commit_count == 0
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    "failed_query",
    [
        LOCK_ADMIN_LESSON_FOR_DELETE,
        CHECK_ADMIN_LESSON_DELETE_DEPENDENCIES,
        SOFT_DELETE_ADMIN_LESSON,
    ],
)
def test_delete_rolls_back_query_failures_without_database_details(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    failed_query: str,
) -> None:
    """Trả lỗi 500 an toàn và rollback khi một query thất bại."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_delete_queries(monkeypatch, fail_query=failed_query)

    response = delete_request(client, "501")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "sensitive query detail" not in response.text
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_delete_rolls_back_malformed_lock_dependency_and_result_projections(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối row sai shape, dependency type sai hoặc thiếu timestamp."""

    cases = [
        {"lock_row": {"id": "501", "status": "PUBLISHED"}},
        {"dependency_row": {"has_progress": 0, "has_resources": False, "has_uploads": False}},
        {"deleted_row": {"id": 501, "deleted_at": None}},
    ]
    for case in cases:
        session = FakeSession()
        client.app.dependency_overrides[get_db] = override_db(session)
        allow_admin_token(monkeypatch)
        install_delete_queries(monkeypatch, **case)

        response = delete_request(client, "501")

        assert response.status_code == 500
        assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
        assert session.commit_count == 0
        assert session.rollback_count == 1


def test_delete_rolls_back_when_commit_fails(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Rollback và ẩn database detail nếu transaction commit thất bại."""

    session = FakeSession(fail_commit=True)
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_delete_queries(monkeypatch)

    response = delete_request(client, "501")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "sensitive commit detail" not in response.text
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_delete_openapi_has_int64_path_catalog_errors_and_no_body(
    client: TestClient,
) -> None:
    """Xác nhận OpenAPI mô tả đúng DELETE path-only theo catalog."""

    operation = client.app.openapi()["paths"]["/api/v1/admin/lessons/{lesson_id}"]["delete"]
    parameters = {item["name"]: item for item in operation["parameters"]}

    assert parameters["lesson_id"]["in"] == "path"
    assert parameters["lesson_id"]["schema"] == {"type": "integer", "format": "int64"}
    assert parameters["Authorization"]["in"] == "header"
    assert "requestBody" not in operation
    assert set(operation["responses"]) >= {"200", "401", "403", "404", "422", "500"}

