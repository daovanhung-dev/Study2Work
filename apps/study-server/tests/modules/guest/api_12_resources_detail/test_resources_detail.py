"""Kiểm thử HTTP, validation, query và error mapping của API #12."""

from __future__ import annotations

from typing import Any

import app.modules.guest.api_12_resources_detail.view as resource_view
import pytest
from app.core.database import get_db
from app.modules.guest.api_12_resources_detail.query import (
    ACTIVE_COURSE_ENROLLMENT,
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


def make_resource(
    *,
    lesson_id: int | None = 101,
    visibility: str = "PUBLIC",
) -> dict[str, Any]:
    """Tạo row resource hợp lệ giống kết quả RESOURCE_BY_ID."""

    return {
        "id": 9001,
        "lesson_id": lesson_id,
        "name": "Course reference PDF",
        "type": "DOCUMENT",
        "url": "https://cdn.example.test/resources/9001.pdf",
        "visibility": visibility,
        "storage_key": "resources/9001.pdf" if visibility == "PRIVATE" else None,
    }


def test_resource_detail_returns_public_fields_without_auth(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra resource public thuộc course published trả URL và visibility."""

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
        "visibility": "PUBLIC",
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


def test_private_resource_requires_student_and_returns_signed_url(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra private resource cần Student active và URL ký có TTL 300 giây."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        resource_view,
        "find_resource",
        lambda db, *, resource_id: make_resource(visibility="PRIVATE"),
    )
    monkeypatch.setattr(
        resource_view,
        "find_published_parent_course",
        lambda db, *, lesson_id: {"lesson_id": lesson_id, "course_id": 7},
    )
    authorization_values: list[str | None] = []

    def allow_student(authorization: str | None, **_kwargs: Any) -> tuple[int, list[str]]:
        """Giả lập guard chấp nhận Student và ghi lại Authorization được truyền."""

        authorization_values.append(authorization)
        return 55, ["STUDENT"]

    monkeypatch.setattr(resource_view, "validate_current_user_request", allow_student)
    enrollment_queries: list[dict[str, Any]] = []

    def find_enrollment(db: FakeSession, query: str, params: dict[str, Any]) -> dict[str, int]:
        """Giả lập truy vấn membership ACTIVE theo user/course đã xác thực."""

        assert query == ACTIVE_COURSE_ENROLLMENT
        enrollment_queries.append(params)
        return {"active": 1}

    monkeypatch.setattr(resource_view, "query_one", find_enrollment)
    signed_url_requests: list[dict[str, Any]] = []

    class FakeStorage:
        def create_signed_url(self, *, storage_key: str, expires_in: int) -> str:
            """Ghi nhận yêu cầu ký URL và trả về URL thử nghiệm."""

            signed_url_requests.append({"storage_key": storage_key, "expires_in": expires_in})
            return "https://signed.example.test/resources/9001?ttl=300"

    monkeypatch.setattr(resource_view, "get_upload_storage_provider", lambda: FakeStorage())

    response = client.get(
        "/api/v1/resources/9001",
        headers={"Authorization": "Bearer student-token"},
    )

    assert response.status_code == 200
    assert response.json()["data"]["visibility"] == "PRIVATE"
    assert response.json()["data"]["url"] == "https://signed.example.test/resources/9001?ttl=300"
    assert authorization_values == ["Bearer student-token"]
    assert enrollment_queries == [{"user_id": 55, "course_id": 7}]
    assert signed_url_requests == [{"storage_key": "resources/9001.pdf", "expires_in": 300}]


def test_private_resource_denies_student_without_active_enrollment(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra private resource không lộ khi Student chưa ghi danh active."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        resource_view,
        "find_resource",
        lambda db, *, resource_id: make_resource(visibility="PRIVATE"),
    )
    monkeypatch.setattr(
        resource_view,
        "find_published_parent_course",
        lambda db, *, lesson_id: {"lesson_id": lesson_id, "course_id": 7},
    )
    monkeypatch.setattr(
        resource_view,
        "validate_current_user_request",
        lambda authorization, **_kwargs: (55, ["STUDENT"]),
    )
    monkeypatch.setattr(resource_view, "query_one", lambda db, query, params: None)

    response = client.get(
        "/api/v1/resources/9001",
        headers={"Authorization": "Bearer student-token"},
    )

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"


@pytest.mark.parametrize(
    "resource_id",
    ["abc", "-9223372036854775809", "9223372036854775808"],
)
def test_resource_detail_maps_invalid_path_to_not_found_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    resource_id: str,
) -> None:
    """Kiểm tra malformed/out-of-range path trả 404 trước khi query."""

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


@pytest.mark.parametrize(
    "resource_id",
    ["-9223372036854775808", "-1", "0", "1", "9223372036854775807"],
)
def test_resource_detail_allows_signed_int64_values_to_reach_lookup(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    resource_id: str,
) -> None:
    """In-range IDs, including zero/negative, are checked by the resource lookup."""
    queried_ids: list[int] = []
    monkeypatch.setattr(
        resource_view,
        "find_resource",
        lambda db, *, resource_id: queried_ids.append(resource_id) or None,
    )

    response = client.get(f"/api/v1/resources/{resource_id}")

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert queried_ids == [int(resource_id)]


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
        lambda db, *, resource_id: {**make_resource(lesson_id=None), "id": "not-an-integer"},
    )

    response = client.get("/api/v1/resources/9001")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"


def test_resource_queries_select_visibility_and_use_bound_parameters() -> None:
    """Kiểm tra SQL chọn visibility/storage key và dùng bind params."""

    assert "r.visibility" in RESOURCE_BY_ID.lower()
    assert "r.storage_key" in RESOURCE_BY_ID.lower()
    assert ":resource_id" in RESOURCE_BY_ID
    assert "r.resource_type as type" in " ".join(RESOURCE_BY_ID.lower().split())
    assert ":lesson_id" in PUBLISHED_PARENT_COURSE
    assert "c.status = 'published'" in PUBLISHED_PARENT_COURSE.lower()
    assert "l.status is distinct from 'deleted'" in PUBLISHED_PARENT_COURSE.lower()


def test_resource_detail_openapi_keeps_int64_path_contract(client: TestClient) -> None:
    """Kiểm tra Swagger mô tả resource_id là int64 dù runtime tự parse để trả 404."""

    operation = client.app.openapi()["paths"]["/api/v1/resources/{resource_id}"]["get"]

    assert operation["parameters"] == [
        {
            "name": "Authorization",
            "in": "header",
            "required": False,
            "schema": {
                "anyOf": [{"type": "string"}, {"type": "null"}],
                "title": "Authorization",
            },
        },
        {
            "name": "resource_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer", "format": "int64"},
        }
    ]
