"""Unit test cho API #25 lưu tiến độ bài học (PATCH /api/v1/lessons/{lesson_id}/progress)."""

from __future__ import annotations

from typing import Any

import app.modules.guest.api_25_lessons_progress.view as view_module
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


def test_lesson_progress_new_progress_success(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra trường hợp bài học chưa có bản ghi: chèn mới với trạng thái IN_PROGRESS."""
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

    inserted_data = {}

    def fake_insert(db, *, user_id, lesson_id, status, progress_percent, completed):
        nonlocal inserted_data
        inserted_data = {
            "user_id": user_id,
            "lesson_id": lesson_id,
            "status": status,
            "percent": progress_percent,
            "completed": completed,
        }
        return {"id": 1}

    monkeypatch.setattr(view_module, "insert_lesson_progress_state", fake_insert)

    response = client.patch(
        "/api/v1/lessons/101/progress",
        headers={"Authorization": "Bearer valid-token"},
        json={"position": 120, "percent": 45, "completed": False},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["businessCode"] == "DESIGN_RESOURCE_UPDATED"
    assert payload["data"]["id"] == 101
    assert inserted_data["status"] == "IN_PROGRESS"
    assert inserted_data["percent"] == 45
    assert session.commit_count == 1
    assert session.rollback_count == 0


def test_lesson_progress_existing_completed_success(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra trường hợp cập nhật bài học thành COMPLETED."""
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
        lambda db, *, user_id, lesson_id: {"id": 77, "status": "IN_PROGRESS"},
    )

    updated_data = {}

    def fake_update(db, *, progress_id, status, progress_percent, completed):
        nonlocal updated_data
        updated_data = {
            "progress_id": progress_id,
            "status": status,
            "percent": progress_percent,
            "completed": completed,
        }
        return {"id": progress_id}

    monkeypatch.setattr(view_module, "update_lesson_progress_state", fake_update)

    response = client.patch(
        "/api/v1/lessons/101/progress",
        headers={"Authorization": "Bearer valid-token"},
        json={"position": 300, "percent": 100, "completed": True},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["businessCode"] == "DESIGN_RESOURCE_UPDATED"
    assert updated_data["status"] == "COMPLETED"
    assert updated_data["percent"] == 100
    assert session.commit_count == 1


def test_lesson_progress_missing_auth(client: TestClient) -> None:
    """Kiểm tra khi thiếu Authorization header trả về HTTP 401."""
    response = client.patch(
        "/api/v1/lessons/101/progress",
        json={"position": 10, "percent": 20, "completed": False},
    )
    assert response.status_code == 401
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_lesson_progress_forbidden_role(
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

    response = client.patch(
        "/api/v1/lessons/101/progress",
        headers={"Authorization": "Bearer admin-token"},
        json={"position": 10, "percent": 20, "completed": False},
    )
    assert response.status_code == 403
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_ACCESS_DENIED"


def test_lesson_progress_does_not_apply_range_validation(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """DD #25 không quy định range cho position/percent nên validate không trả HTTP 422."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())
    monkeypatch.setattr(
        view_module,
        "find_lesson_by_id",
        lambda db, *, lesson_id: None,
    )

    response = client.patch(
        "/api/v1/lessons/101/progress",
        headers={"Authorization": "Bearer valid-token"},
        json={"position": -1, "percent": 150, "completed": False},
    )
    assert response.status_code == 404
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_lesson_progress_not_found(
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

    response = client.patch(
        "/api/v1/lessons/999/progress",
        headers={"Authorization": "Bearer valid-token"},
        json={"position": 10, "percent": 20, "completed": False},
    )
    assert response.status_code == 404
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_lesson_progress_not_enrolled(
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

    response = client.patch(
        "/api/v1/lessons/101/progress",
        headers={"Authorization": "Bearer valid-token"},
        json={"position": 10, "percent": 20, "completed": False},
    )
    assert response.status_code == 403
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_ACCESS_DENIED"


def test_lesson_progress_db_failure(
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

    response = client.patch(
        "/api/v1/lessons/101/progress",
        headers={"Authorization": "Bearer valid-token"},
        json={"position": 10, "percent": 20, "completed": False},
    )
    assert response.status_code == 500
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1
