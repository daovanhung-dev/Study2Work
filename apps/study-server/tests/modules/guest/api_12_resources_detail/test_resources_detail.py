"""Kiểm thử HTTP, validation, query và error mapping của API #12."""

from __future__ import annotations

from typing import Any

import app.modules.guest.api_12_resources_detail.view as resource_view
import pytest
from app.core.database import get_db
from app.modules.guest.api_12_resources_detail.query import (
    PUBLISHED_PARENT_COURSE,
    RESOURCE_BY_ID,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Theo dõi rollback của API read-only mà không mở kết nối database thật."""

    def __init__(self) -> None:
        """Khởi tạo bộ đếm rollback cho một request kiểm thử."""

        self.rollback_count = 0

    def rollback(self) -> None:
        """Tăng bộ đếm khi view kết thúc transaction lỗi."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency database trả cùng FakeSession trong request."""

    def dependency():
        """Yield Session giả cho FastAPI dependency injection."""

        yield session

    return dependency


def make_resource(*, lesson_id: int | None = 101) -> dict[str, Any]:
    """Tạo row resource hợp lệ giống kết quả RESOURCE_BY_ID."""

    return {
        "id": 9001,
        "lesson_id": lesson_id,
        "name": "Course reference PDF",
        "type": "DOCUMENT",
        "url": "https://cdn.example.test/resources/9001.pdf",
        "visibility": "MUST_BE_IGNORED",
    }


def test_resource_detail_returns_source_backed_fields_without_auth_or_visibility(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra resource thuộc course published trả direct URL và loại visibility khỏi response."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        resource_view,
        "find_resource",
        lambda db, *, resource_id: make_resource(),
    )
    monkeypatch.setattr(
        resource_view,
        "find_published_parent_course",
        lambda db, *, lesson_id: {
            "lesson_id": lesson_id,
            "course_id": 7,
            "course_status": "PUBLISHED",
        },
    )

    response = client.get(
        "/api/v1/resources/9001",
        headers={"X-Trace-Id": "00000000-0000-0000-0000-000000000012"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["message"] == "Resource metadata retrieved"
    assert payload["data"] == {
        "id": 9001,
        "name": "Course reference PDF",
        "type": "DOCUMENT",
        "url": "https://cdn.example.test/resources/9001.pdf",
        "lesson_id": 101,
    }
    assert payload["traceId"] == "00000000-0000-0000-0000-000000000012"
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert session.rollback_count == 0


def test_resource_without_lesson_returns_success_without_parent_lookup(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra lesson_id null vẫn trả 200 và không query parent course."""

    monkeypatch.setattr(
        resource_view,
        "find_resource",
        lambda db, *, resource_id: make_resource(lesson_id=None),
    )
    monkeypatch.setattr(
        resource_view,
        "find_published_parent_course",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("resource không có lesson thì không query parent")
        ),
    )

    response = client.get("/api/v1/resources/9001")

    assert response.status_code == 200
    assert response.json()["data"]["lesson_id"] is None


@pytest.mark.parametrize(
    "resource_id",
    ["abc", "0", "-1", "9223372036854775808"],
)
def test_resource_detail_maps_invalid_path_to_not_found_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    resource_id: str,
) -> None:
    """Kiểm tra path không phải integer dương int64 trả 404 trước khi query."""

    monkeypatch.setattr(
        resource_view,
        "find_resource",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("invalid path không được query database")
        ),
    )

    response = client.get(f"/api/v1/resources/{resource_id}")

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert response.json()["message"] == "Resource not found"


def test_resource_detail_maps_missing_resource_to_not_found(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra resource ID không tồn tại trả error contract 404."""

    monkeypatch.setattr(resource_view, "find_resource", lambda db, *, resource_id: None)

    response = client.get("/api/v1/resources/9001")

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_resource_detail_hides_resource_without_published_parent(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra lesson/course thiếu hoặc course chưa publish đều được che bằng 404."""

    monkeypatch.setattr(
        resource_view,
        "find_resource",
        lambda db, *, resource_id: make_resource(),
    )
    monkeypatch.setattr(
        resource_view,
        "find_published_parent_course",
        lambda db, *, lesson_id: None,
    )

    response = client.get("/api/v1/resources/9001")

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


@pytest.mark.parametrize("failure_stage", ["resource", "parent"])
def test_resource_detail_rolls_back_and_hides_database_failure(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    failure_stage: str,
) -> None:
    """Kiểm tra lỗi Q1 hoặc Q2 rollback và không làm lộ chi tiết database."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    if failure_stage == "resource":
        monkeypatch.setattr(
            resource_view,
            "find_resource",
            lambda db, *, resource_id: (_ for _ in ()).throw(
                SQLAlchemyError("database unavailable")
            ),
        )
    else:
        monkeypatch.setattr(
            resource_view,
            "find_resource",
            lambda db, *, resource_id: make_resource(),
        )
        monkeypatch.setattr(
            resource_view,
            "find_published_parent_course",
            lambda db, *, lesson_id: (_ for _ in ()).throw(SQLAlchemyError("database unavailable")),
        )

    response = client.get("/api/v1/resources/9001")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["message"] == "Resource could not be retrieved"
    assert "database unavailable" not in response.text
    assert session.rollback_count == 1


def test_resource_detail_maps_invalid_row_to_internal_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra row thiếu field bắt buộc được ánh xạ thành lỗi 500 an toàn."""

    monkeypatch.setattr(
        resource_view,
        "find_resource",
        lambda db, *, resource_id: {"id": 9001, "lesson_id": None},
    )

    response = client.get("/api/v1/resources/9001")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"


def test_resource_queries_exclude_visibility_and_use_bound_parameters() -> None:
    """Kiểm tra SQL chỉ đọc field source-backed, không tham chiếu visibility và dùng bind params."""

    assert "visibility" not in RESOURCE_BY_ID.lower()
    assert ":resource_id" in RESOURCE_BY_ID
    assert "r.resource_type as type" in " ".join(RESOURCE_BY_ID.lower().split())
    assert ":lesson_id" in PUBLISHED_PARENT_COURSE
    assert "c.status = 'published'" in PUBLISHED_PARENT_COURSE.lower()


def test_resource_detail_openapi_keeps_int64_path_contract(client: TestClient) -> None:
    """Kiểm tra Swagger mô tả resource_id là int64 dù runtime tự parse để trả 404."""

    operation = client.app.openapi()["paths"]["/api/v1/resources/{resource_id}"]["get"]

    assert operation["parameters"] == [
        {
            "name": "resource_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer", "format": "int64"},
        }
    ]
