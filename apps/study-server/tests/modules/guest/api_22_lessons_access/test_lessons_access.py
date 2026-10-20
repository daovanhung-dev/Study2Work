"""Unit test cho API #22 kiểm tra quyền truy cập bài học (GET /api/v1/lessons/{lesson_id}/access)."""

from __future__ import annotations

from typing import Any

import app.modules.guest.api_22_lessons_access.view as view_module
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient


class FakeSession:
    def __init__(self) -> None:
        """Khởi tạo session giả lập với bộ đếm rollback."""
        self.rollback_count = 0

    def rollback(self) -> None:
        """Ghi nhận số lần gọi rollback."""
        self.rollback_count += 1


def make_lesson() -> dict[str, Any]:
    """Tạo dữ liệu bài học giả lập."""
    return {
        "id": 101,
        "course_id": 10,
        "title": "Bai hoc so 1",
        "content": "Noi dung bai hoc",
        "video_url": "https://example.com/video.mp4",
        "order": 1,
        "status": "PUBLISHED",
    }


def override_db(session: FakeSession):
    """Dependency override cho database session."""
    def dependency():
        yield session

    return dependency


def valid_claims() -> dict[str, Any]:
    """Tạo claims JWT hợp lệ cho Student."""
    return {"sub": "1001", "roles": ["STUDENT"]}


def test_lesson_access_success(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra trường hợp thành công khi học viên có enrollment hợp lệ."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())
    monkeypatch.setattr(
        view_module,
        "find_lesson_by_id",
        lambda db, *, lesson_id: make_lesson(),
    )
    monkeypatch.setattr(
        view_module,
        "find_active_enrollment",
        lambda db, *, user_id, course_id: {"id": 1, "status": "ACTIVE"},
    )

    response = client.get(
        "/api/v1/lessons/101/access",
        headers={"Authorization": "Bearer valid-token"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"]["id"] == 101
    assert payload["data"]["course_id"] == 10
    assert payload["data"]["title"] == "Bai hoc so 1"


def test_lesson_access_missing_auth(client: TestClient) -> None:
    """Kiểm tra khi thiếu Authorization header trả về HTTP 401."""
    response = client.get("/api/v1/lessons/101/access")
    assert response.status_code == 401
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_lesson_access_forbidden_role(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra khi role không phải STUDENT trả về HTTP 403."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda token: {"sub": "1001", "roles": ["MENTOR"]},
    )

    response = client.get(
        "/api/v1/lessons/101/access",
        headers={"Authorization": "Bearer mentor-token"},
    )
    assert response.status_code == 403
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_ACCESS_DENIED"


def test_lesson_access_lesson_not_found(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra khi bài học không tồn tại trả về HTTP 404."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())
    monkeypatch.setattr(
        view_module,
        "find_lesson_by_id",
        lambda db, *, lesson_id: None,
    )

    response = client.get(
        "/api/v1/lessons/999/access",
        headers={"Authorization": "Bearer valid-token"},
    )
    assert response.status_code == 404
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_lesson_access_not_enrolled(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra khi học viên chưa ghi danh vào khóa học trả về HTTP 403."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())
    monkeypatch.setattr(
        view_module,
        "find_lesson_by_id",
        lambda db, *, lesson_id: make_lesson(),
    )
    monkeypatch.setattr(
        view_module,
        "find_active_enrollment",
        lambda db, *, user_id, course_id: None,
    )

    response = client.get(
        "/api/v1/lessons/101/access",
        headers={"Authorization": "Bearer valid-token"},
    )
    assert response.status_code == 403
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_ACCESS_DENIED"


def test_lesson_access_db_failure(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra khi truy vấn DB bị lỗi trả về HTTP 500 và rollback."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())

    def raise_db_error(db, *, lesson_id):
        raise RuntimeError("Database error")

    monkeypatch.setattr(view_module, "find_lesson_by_id", raise_db_error)

    response = client.get(
        "/api/v1/lessons/101/access",
        headers={"Authorization": "Bearer valid-token"},
    )
    assert response.status_code == 500
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1

