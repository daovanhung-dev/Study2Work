"""HTTP tests cho API #77 soft-delete course trong Admin."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import app.modules.admin.api_77_admin_course_delete.view as delete_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.admin.api_77_admin_course_delete.query import (
    CHECK_ADMIN_COURSE_DELETE_DEPENDENCIES,
    LOCK_ADMIN_COURSE_FOR_DELETE,
    SOFT_DELETE_ADMIN_COURSE,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

_UNSET = object()


class FakeSession:
    """Session giả để kiểm tra commit/rollback API #77."""

    def __init__(self, *, fail_commit: bool = False) -> None:
        """Khởi tạo bộ đếm transaction với tùy chọn lỗi commit."""

        self.commit_count = 0
        self.rollback_count = 0
        self.fail_commit = fail_commit

    def commit(self) -> None:
        """Ghi nhận commit hoặc phát sinh lỗi DB đã cấu hình."""

        self.commit_count += 1
        if self.fail_commit:
            raise SQLAlchemyError("sensitive commit detail")

    def rollback(self) -> None:
        """Ghi nhận rollback của nhánh lỗi."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override cấp fake session cho TestClient."""

    def dependency():
        """Yield fake session cho dependency get_db."""

        yield session

    return dependency


def allow_admin_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Cài decoder giả trả claim ADMIN hoặc role được test yêu cầu."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": roles or ["ADMIN"]},
    )


def delete_request(
    client: TestClient,
    course_id: str,
    *,
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi HTTP DELETE API #77 với raw path và Authorization tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.request(
        "DELETE",
        f"/api/v1/admin/courses/{course_id}",
        headers=headers,
    )


def deleted_course_row(**overrides: Any) -> dict[str, Any]:
    """Tạo UPDATE RETURNING row gồm course ID và timestamp đã persist."""

    return {
        "id": 1001,
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
    """Cài query double, ghi SQL/bindings và mô phỏng từng nhánh DB."""

    captured: list[tuple[str, dict[str, Any]]] = []
    results = {
        LOCK_ADMIN_COURSE_FOR_DELETE: {"id": 1001} if lock_row is _UNSET else lock_row,
        CHECK_ADMIN_COURSE_DELETE_DEPENDENCIES: (
            {"has_enrollments": False, "has_content": False}
            if dependency_row is _UNSET
            else dependency_row
        ),
        SOFT_DELETE_ADMIN_COURSE: (
            deleted_course_row() if deleted_row is _UNSET else deleted_row
        ),
    }

    def query_one(_db: Any, query: str, params: dict[str, Any]) -> Any:
        """Ghi statement/bindings rồi trả kết quả hoặc database failure cấu hình."""

        captured.append((query, dict(params)))
        if query == fail_query:
            raise SQLAlchemyError("sensitive query detail")
        if query not in results:
            raise AssertionError("unexpected query")
        return results[query]

    monkeypatch.setattr(delete_view, "query_one", query_one)
    return captured


def test_delete_soft_marks_course_and_returns_database_timestamp(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Ghi status marker, giữ dependency rows và trả updated_at từ DB."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_delete_queries(monkeypatch)

    response = delete_request(client, "1001")

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_DELETED"
    assert payload["data"] == {
        "id": 1001,
        "status": "deleted",
        "deleted_at": "2026-10-26T10:30:00",
    }
    assert payload["meta"] == {}
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert captured == [
        (LOCK_ADMIN_COURSE_FOR_DELETE, {"course_id": 1001}),
        (CHECK_ADMIN_COURSE_DELETE_DEPENDENCIES, {"course_id": 1001}),
        (SOFT_DELETE_ADMIN_COURSE, {"course_id": 1001}),
    ]
    assert "status = 'DELETED'" in SOFT_DELETE_ADMIN_COURSE
    assert "updated_at = CURRENT_TIMESTAMP" in SOFT_DELETE_ADMIN_COURSE
    assert "DELETE FROM" not in SOFT_DELETE_ADMIN_COURSE.upper()
    assert "course_status_audit_logs" not in SOFT_DELETE_ADMIN_COURSE
    assert session.commit_count == 1
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    "dependency_row",
    [
        {"has_enrollments": True, "has_content": False},
        {"has_enrollments": False, "has_content": True},
        {"has_enrollments": True, "has_content": True},
    ],
)
def test_delete_blocks_course_with_enrollment_or_content(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    dependency_row: dict[str, bool],
) -> None:
    """Trả catalog 422 và không mutation nếu policy candidate tìm thấy dependency."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_delete_queries(monkeypatch, dependency_row=dependency_row)

    response = delete_request(client, "1001")

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["data"] is None
    assert len(captured) == 2
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_delete_returns_not_found_for_missing_or_already_deleted_course(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map no-row lock result sang catalog 404 mà không chạy dependency query."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_delete_queries(monkeypatch, lock_row=None)

    response = delete_request(client, "1001")

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert response.json()["data"] is None
    assert captured == [(LOCK_ADMIN_COURSE_FOR_DELETE, {"course_id": 1001})]
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize("course_id", ["abc", str(2**63), str(-(2**63) - 1)])
def test_delete_rejects_malformed_or_out_of_range_int64_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    course_id: str,
) -> None:
    """Map raw path sai format/range thành 422 trước query."""

    allow_admin_token(monkeypatch)
    captured = install_delete_queries(monkeypatch)

    response = delete_request(client, course_id)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["data"] is None
    assert captured == []


def test_delete_requires_authentication_before_database_access(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 401 khi thiếu Bearer JWT và không query course."""

    captured = install_delete_queries(monkeypatch)

    response = delete_request(client, "1001", authorization=None)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert captured == []


def test_delete_requires_admin_role_before_database_access(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 403 cho JWT không có ADMIN role và không query course."""

    allow_admin_token(monkeypatch, roles=["MENTOR"])
    captured = install_delete_queries(monkeypatch)

    response = delete_request(client, "1001")

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert captured == []


@pytest.mark.parametrize(
    ("query_to_fail", "expected_calls"),
    [
        (LOCK_ADMIN_COURSE_FOR_DELETE, 1),
        (CHECK_ADMIN_COURSE_DELETE_DEPENDENCIES, 2),
        (SOFT_DELETE_ADMIN_COURSE, 3),
    ],
)
def test_delete_rolls_back_query_failures_without_exposing_database_detail(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    query_to_fail: str,
    expected_calls: int,
) -> None:
    """Rollback từng lỗi query và không phản chiếu chi tiết database."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_delete_queries(monkeypatch, fail_query=query_to_fail)

    response = delete_request(client, "1001")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "sensitive query detail" not in response.text
    assert len(captured) == expected_calls
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize(
    ("lock_row", "dependency_row", "deleted_row"),
    [
        ({"id": "1001"}, None, None),
        ({"id": 1001}, {"has_enrollments": 0, "has_content": False}, None),
        ({"id": 1001}, {"has_enrollments": False, "has_content": False}, {"id": 1001}),
        (
            {"id": 1001},
            {"has_enrollments": False, "has_content": False},
            deleted_course_row(id=1002),
        ),
        (
            {"id": 1001},
            {"has_enrollments": False, "has_content": False},
            deleted_course_row(deleted_at="not-a-timestamp"),
        ),
    ],
)
def test_delete_rolls_back_malformed_database_projections(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    lock_row: Any,
    dependency_row: Any,
    deleted_row: Any,
) -> None:
    """Không commit khi lock, dependency hoặc DeleteResult projection sai kiểu."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_delete_queries(
        monkeypatch,
        lock_row=lock_row,
        dependency_row=dependency_row,
        deleted_row=deleted_row,
    )

    response = delete_request(client, "1001")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_delete_rolls_back_failed_commit(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Rollback commit failure và chỉ trả lỗi hệ thống an toàn."""

    session = FakeSession(fail_commit=True)
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_delete_queries(monkeypatch)

    response = delete_request(client, "1001")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "sensitive commit detail" not in response.text
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_delete_openapi_has_path_header_errors_and_no_request_body(client: TestClient) -> None:
    """Khai báo đúng DeleteResult, path int64, auth header và catalog errors."""

    openapi = client.app.openapi()
    operation = openapi["paths"]["/api/v1/admin/courses/{course_id}"]["delete"]

    assert "requestBody" not in operation
    parameters = {item["name"]: item for item in operation["parameters"]}
    assert parameters["course_id"]["schema"] == {"type": "integer", "format": "int64"}
    assert parameters["Authorization"]["in"] == "header"
    assert parameters["Authorization"]["required"] is True
    assert set(operation["responses"]) == {"200", "401", "403", "404", "422", "500"}
    envelope_ref = operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"]
    envelope_name = envelope_ref.rsplit("/", 1)[-1]
    envelope = openapi["components"]["schemas"][envelope_name]
    result_ref = envelope["properties"]["data"]["$ref"]
    result_name = result_ref.rsplit("/", 1)[-1]
    result_schema = openapi["components"]["schemas"][result_name]
    assert set(result_schema["properties"]) == {"id", "status", "deleted_at"}
    assert result_schema["properties"]["status"]["const"] == "deleted"
