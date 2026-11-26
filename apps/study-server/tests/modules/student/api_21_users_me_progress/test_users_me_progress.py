"""Unit test cho API #21 lấy tiến độ tổng hợp (GET /api/v1/users/me/progress)."""

from __future__ import annotations

from typing import Any

import app.modules.student.api_21_users_me_progress.view as view_module
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


def make_progress_rows() -> list[dict[str, Any]]:
    """Tạo dữ liệu tiến độ từng khóa học giả lập."""
    return [
        {
            "course_id": 1,
            "course_name": "FastAPI Backend",
            "enrollment_status": "ACTIVE",
            "total_lessons": 2,
            "completed_lessons": 1,
        },
        {
            "course_id": 2,
            "course_name": "Vue 3 Frontend",
            "enrollment_status": "COMPLETED",
            "total_lessons": 2,
            "completed_lessons": 2,
        },
    ]


def override_db(session: FakeSession):
    """Dependency override cho database session."""

    def dependency():
        yield session

    return dependency


def valid_claims() -> dict[str, Any]:
    """Tạo claims JWT hợp lệ cho Student."""
    return {"sub": "1001", "roles": ["STUDENT"]}


def test_user_progress_success(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra trường hợp thành công trả về tổng hợp tiến độ HTTP 200."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())
    monkeypatch.setattr(
        view_module,
        "find_user_course_progress",
        lambda db, *, user_id, course_id=None: make_progress_rows(),
    )

    response = client.get(
        "/api/v1/users/me/progress",
        headers={
            "Authorization": "Bearer valid-token",
            "X-Trace-Id": "00000000-0000-0000-0000-000000000001",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"]["total_enrolled_courses"] == 2
    assert payload["data"]["active_courses"] == 1
    assert payload["data"]["completed_courses"] == 1
    assert payload["data"]["total_lessons"] == 4
    assert payload["data"]["completed_lessons"] == 3
    assert payload["data"]["overall_progress_percent"] == 75.0
    assert len(payload["data"]["courses"]) == 2


def test_user_progress_missing_auth(client: TestClient) -> None:
    """Kiểm tra khi thiếu header Authorization trả về HTTP 401."""
    response = client.get(
        "/api/v1/users/me/progress",
        headers={"X-Trace-Id": "00000000-0000-0000-0000-000000000002"},
    )
    assert response.status_code == 401
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_user_progress_forbidden_role(
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
        "/api/v1/users/me/progress",
        headers={"Authorization": "Bearer mentor-token"},
    )
    assert response.status_code == 403
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_ACCESS_DENIED"


def test_user_progress_empty_courses(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra khi học viên chưa ghi danh khóa học nào trả về 0% và danh sách rỗng."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())
    monkeypatch.setattr(
        view_module,
        "find_user_course_progress",
        lambda db, *, user_id, course_id=None: [],
    )

    response = client.get(
        "/api/v1/users/me/progress",
        headers={"Authorization": "Bearer valid-token"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["data"]["total_enrolled_courses"] == 0
    assert payload["data"]["overall_progress_percent"] == 0.0
    assert payload["data"]["courses"] == []


def test_user_progress_db_failure(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra khi truy vấn DB lỗi trả về HTTP 500 và gọi rollback."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())

    def raise_error(db, *, user_id, course_id=None):
        raise RuntimeError("DB connection failure")

    monkeypatch.setattr(view_module, "find_user_course_progress", raise_error)

    response = client.get(
        "/api/v1/users/me/progress",
        headers={"Authorization": "Bearer valid-token"},
    )
    assert response.status_code == 500
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1
