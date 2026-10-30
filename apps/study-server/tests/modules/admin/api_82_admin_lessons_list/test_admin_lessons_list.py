from __future__ import annotations

from typing import Any

import app.modules.admin.api_82_admin_lessons_list.view as lessons_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Session giả để xác nhận API #82 chỉ đọc và rollback lỗi."""

    def __init__(self) -> None:
        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Đếm commit nếu API vô tình ghi dữ liệu."""

        self.commit_count += 1

    def rollback(self) -> None:
        """Đếm rollback khi truy vấn hoặc ánh xạ thất bại."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả fake session cho TestClient."""

    def dependency():
        """Cung cấp session giả cho một HTTP request."""

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


def lesson_row(**overrides: Any) -> dict[str, Any]:
    """Tạo Lesson projection theo các cột legacy `lessons` đã chọn."""

    return {
        "id": 501,
        "course_id": 42,
        "title": "Giới thiệu khóa học",
        "content": "Nội dung bài học",
        "video_url": "https://cdn.example.test/lessons/501.mp4",
        "order": 1,
        "status": "DRAFT",
        **overrides,
    }


def install_query_rows(
    monkeypatch: pytest.MonkeyPatch,
    *,
    rows: list[dict[str, Any]] | None = None,
) -> list[tuple[str, dict[str, Any]]]:
    """Cài query double và ghi lại SQL cùng bind parameters."""

    result_rows = [lesson_row()] if rows is None else rows
    captured: list[tuple[str, dict[str, Any]]] = []

    def query_many(_db, query, params):
        """Trả các row giả và lưu truy vấn được gọi."""

        captured.append((query, dict(params)))
        if query != lessons_view.LIST_ADMIN_LESSONS:
            raise AssertionError("unexpected lesson query")
        return result_rows

    monkeypatch.setattr(lessons_view, "query_many", query_many)
    return captured


def get_lessons_response(
    client: TestClient,
    *,
    authorization: str | None = "Bearer valid-admin-token",
    params: dict[str, str] | None = None,
):
    """Gửi HTTP GET API #82 với query/header tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.get("/api/v1/admin/lessons", headers=headers, params=params or {})


def test_get_admin_lessons_returns_lesson_collection_and_preserves_optional_nulls(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả Lesson[] đang hoạt động và giữ content/video null như API #09."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_query_rows(
        monkeypatch,
        rows=[lesson_row(content=None, video_url=None)],
    )

    response = get_lessons_response(client)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"] == [
        {
            "id": 501,
            "course_id": 42,
            "title": "Giới thiệu khóa học",
            "content": None,
            "video_url": None,
            "order": 1,
            "status": "DRAFT",
        }
    ]
    assert payload["traceId"] == response.headers["X-Trace-Id"]
    assert captured[0][1] == {"course_id": None, "status": None}
    assert "PUBLISHED" not in captured[0][0]
    assert "l.status IS DISTINCT FROM 'DELETED'" in captured[0][0]
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_admin_lessons_applies_exact_course_and_status_filters(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Bind chính xác bộ lọc course/status, không thêm điều kiện hiển thị công khai."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_query_rows(monkeypatch, rows=[lesson_row(status="SUSPENDED")])

    response = get_lessons_response(client, params={"course": "00042", "status": "SUSPENDED"})

    assert response.status_code == 200
    assert response.json()["data"][0]["status"] == "SUSPENDED"
    assert captured[0][1] == {"course_id": 42, "status": "SUSPENDED"}
    assert "l.course_id = :course_id" in captured[0][0]
    assert "l.status = :status" in captured[0][0]
    assert "l.status IS DISTINCT FROM 'DELETED'" in captured[0][0]
    assert "PUBLISHED" not in captured[0][0]
    assert session.commit_count == 0


def test_get_admin_lessons_returns_empty_collection_without_not_found(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Collection không có row vẫn trả 200 với data rỗng."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_query_rows(monkeypatch, rows=[])

    response = get_lessons_response(client)

    assert response.status_code == 200
    assert response.json()["data"] == []
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert session.commit_count == 0


def test_get_admin_lessons_checks_auth_before_invalid_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Thiếu token trả 401 trước khi parse course/type hoặc chạy query."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    query_calls: list[bool] = []
    monkeypatch.setattr(
        lessons_view,
        "query_many",
        lambda *_args, **_kwargs: query_calls.append(True),
    )

    response = get_lessons_response(
        client,
        authorization=None,
        params={"course": "not-an-id", "type": "video"},
    )

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert query_calls == []


def test_get_admin_lessons_denies_non_admin_before_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Role không phải ADMIN trả 403 trước khi query danh sách."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch, roles=["STUDENT"])
    query_calls: list[bool] = []
    monkeypatch.setattr(
        lessons_view,
        "query_many",
        lambda *_args, **_kwargs: query_calls.append(True),
    )

    response = get_lessons_response(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert query_calls == []


@pytest.mark.parametrize(
    "course",
    ["not-an-id", "9223372036854775808", "-9223372036854775809"],
)
def test_get_admin_lessons_rejects_invalid_int64_course_filter(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    course: str,
) -> None:
    """Course sai định dạng hoặc vượt miền int64 trả lỗi validation DESIGN."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    query_calls: list[bool] = []
    monkeypatch.setattr(
        lessons_view,
        "query_many",
        lambda *_args, **_kwargs: query_calls.append(True),
    )

    response = get_lessons_response(client, params={"course": course})

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0]["field"] == "course"
    assert query_calls == []


def test_get_admin_lessons_accepts_signed_int64_lower_bound(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Giá trị signed-int64 âm hợp lệ được bind mà không thêm positive-ID rule."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_query_rows(monkeypatch, rows=[])

    response = get_lessons_response(client, params={"course": "-9223372036854775808"})

    assert response.status_code == 200
    assert captured[0][1]["course_id"] == -(2**63)


def test_get_admin_lessons_rejects_unmapped_type_filter_before_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Không âm thầm bỏ qua type khi các schema hiện tại không có Lesson type."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    query_calls: list[bool] = []
    monkeypatch.setattr(
        lessons_view,
        "query_many",
        lambda *_args, **_kwargs: query_calls.append(True),
    )

    response = get_lessons_response(client, params={"type": "video"})

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0] == {
        "field": "type",
        "code": "UNSUPPORTED_FILTER",
        "message": "Lesson type filter is not supported by the available schema.",
    }
    assert query_calls == []


@pytest.mark.parametrize(
    "override",
    [
        {"course_id": None},
        {"order": None},
        {"status": None},
    ],
)
def test_get_admin_lessons_rejects_null_required_lesson_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    override: dict[str, Any],
) -> None:
    """Không bỏ row hoặc bịa default nếu required Lesson field trong DDL candidate bị null."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_query_rows(monkeypatch, rows=[lesson_row(**override)])

    response = get_lessons_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert session.rollback_count == 1


def test_get_admin_lessons_maps_query_failure_to_safe_error_and_rolls_back(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Query failure trả lỗi an toàn và rollback read transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Phát sinh lỗi SQLAlchemy để kiểm tra error boundary."""

        raise SQLAlchemyError("private database detail")

    monkeypatch.setattr(lessons_view, "query_many", fail_query)

    response = get_lessons_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert "private database detail" not in response.text
    assert session.rollback_count == 1


def test_admin_lessons_openapi_keeps_catalog_queries_and_documents_derived_422(
    client: TestClient,
) -> None:
    """OpenAPI khai báo ba query trực tiếp, Authorization và status code cục bộ."""

    schema = client.app.openapi()
    path = "/api/v1/admin/lessons"
    operation = schema["paths"][path]["get"]
    parameters = {
        (parameter["name"], parameter["in"]): parameter
        for parameter in operation["parameters"]
    }

    assert set(parameters) == {
        ("course", "query"),
        ("status", "query"),
        ("type", "query"),
        ("Authorization", "header"),
    }
    assert parameters[("course", "query")]["schema"]["type"] == "integer"
    assert parameters[("course", "query")]["schema"]["format"] == "int64"
    assert "requestBody" not in operation
    assert sorted(operation["responses"]) == ["200", "401", "403", "422", "500"]
    assert "/api/v1/courses/{course_id}/curriculum" in schema["paths"]
    assert "/api/v1/admin/content/pending" in schema["paths"]
    assert "/api/v1/admin/lessons/{lesson_id}" in schema["paths"]
    assert "get" in schema["paths"]["/api/v1/admin/lessons/{lesson_id}"]

