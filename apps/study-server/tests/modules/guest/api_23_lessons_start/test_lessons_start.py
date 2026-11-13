"""Unit test cho API #23 khởi tạo lần bắt đầu học (POST /api/v1/lessons/{lesson_id}/start)."""

from __future__ import annotations

from typing import Any

import app.modules.guest.api_23_lessons_start.view as view_module
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient


class FakeSession:
    def __init__(self) -> None:
        """Khởi tạo session giả lập với các bộ đếm commit và rollback."""
        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Ghi nhận số lần gọi commit."""
        self.commit_count += 1

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


def test_lesson_start_new_progress_success(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra trường hợp bài học chưa có tiến độ: chèn mới và commit thành công."""
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
        lambda db, *, user_id, course_id: {"id": 1},
    )
    monkeypatch.setattr(
        view_module,
        "find_lesson_progress",
        lambda db, *, user_id, lesson_id: None,
    )

    inserted = False

    def fake_insert(db, *, user_id, lesson_id):
        nonlocal inserted
        inserted = True
        return {"id": 501}

    monkeypatch.setattr(view_module, "insert_lesson_progress", fake_insert)

    response = client.post(
        "/api/v1/lessons/101/start",
        headers={"Authorization": "Bearer valid-token"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["success"] is True
    assert payload["businessCode"] == "DESIGN_RESOURCE_CREATED"
    assert payload["data"]["id"] == 101
    assert inserted is True
    assert session.commit_count == 1
    assert session.rollback_count == 0


def test_lesson_start_existing_progress_success(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra trường hợp bài học đã có tiến độ: cập nhật bản ghi cũ và commit."""
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
        lambda db, *, user_id, course_id: {"id": 1},
    )
    monkeypatch.setattr(
        view_module,
        "find_lesson_progress",
        lambda db, *, user_id, lesson_id: {"id": 501, "status": "IN_PROGRESS"},
    )

    touched = False

    def fake_touch(db, *, progress_id):
        nonlocal touched
        touched = True
        return {"id": progress_id}

    monkeypatch.setattr(view_module, "touch_lesson_progress", fake_touch)

    response = client.post(
        "/api/v1/lessons/101/start",
        headers={"Authorization": "Bearer valid-token"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["success"] is True
    assert payload["businessCode"] == "DESIGN_RESOURCE_CREATED"
    assert touched is True
    assert session.commit_count == 1


def test_lesson_start_missing_auth(client: TestClient) -> None:
    """Kiểm tra khi thiếu Authorization header trả về HTTP 401."""
    response = client.post("/api/v1/lessons/101/start")
    assert response.status_code == 401
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_lesson_start_forbidden_role(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra khi role không phải STUDENT trả về HTTP 403."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda token: {"sub": "1001", "roles": ["ADMIN"]},
    )

    response = client.post(
        "/api/v1/lessons/101/start",
        headers={"Authorization": "Bearer admin-token"},
    )
    assert response.status_code == 403
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_ACCESS_DENIED"


def test_lesson_start_lesson_not_found(
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

    response = client.post(
        "/api/v1/lessons/999/start",
        headers={"Authorization": "Bearer valid-token"},
    )
    assert response.status_code == 404
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_lesson_start_not_enrolled(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra khi học viên chưa ghi danh khóa học trả về HTTP 403."""
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

    response = client.post(
        "/api/v1/lessons/101/start",
        headers={"Authorization": "Bearer valid-token"},
    )
    assert response.status_code == 403
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_ACCESS_DENIED"


def test_lesson_start_db_failure(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra khi thao tác DB gặp lỗi trả về HTTP 500 và rollback."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())

    def raise_db_error(db, *, lesson_id):
        raise RuntimeError("Database error")

    monkeypatch.setattr(view_module, "find_lesson_by_id", raise_db_error)

    response = client.post(
        "/api/v1/lessons/101/start",
        headers={"Authorization": "Bearer valid-token"},
    )
    assert response.status_code == 500
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1

