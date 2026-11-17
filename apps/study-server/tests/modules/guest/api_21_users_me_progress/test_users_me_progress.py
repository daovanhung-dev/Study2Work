"""Unit test cho API #21 lấy tiến độ tổng hợp (GET /api/v1/users/me/progress)."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import app.modules.guest.api_21_users_me_progress.view as view_module
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


def make_user() -> dict[str, Any]:
    """Tạo dữ liệu người dùng giả lập."""
    created_at = datetime(2026, 9, 15, 12, 0, tzinfo=UTC)
    return {
        "id": 1001,
        "full_name": "Nguyen Van A",
        "email": "student@example.com",
        "role": "STUDENT",
        "avatar_url": None,
        "phone": None,
        "status": "ACTIVE",
        "created_at": created_at,
        "updated_at": created_at,
    }


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
    """Kiểm tra trường hợp thành công trả về HTTP 200 DESIGN_RESOURCE_RETRIEVED."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())
    monkeypatch.setattr(
        view_module,
        "find_current_user",
        lambda db, *, user_id: make_user(),
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
    assert payload["data"]["id"] == 1001
    assert payload["data"]["role"] == "STUDENT"


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


def test_user_progress_user_not_found(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra khi không tìm thấy user trong DB trả về HTTP 401."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())
    monkeypatch.setattr(
        view_module,
        "find_current_user",
        lambda db, *, user_id: None,
    )

    response = client.get(
        "/api/v1/users/me/progress",
        headers={"Authorization": "Bearer valid-token"},
    )
    assert response.status_code == 401
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_user_progress_db_failure(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra khi truy vấn DB lỗi trả về HTTP 500 và gọi rollback."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())

    def raise_error(db, *, user_id):
        raise RuntimeError("DB connection failure")

    monkeypatch.setattr(view_module, "find_current_user", raise_error)

    response = client.get(
        "/api/v1/users/me/progress",
        headers={"Authorization": "Bearer valid-token"},
    )
    assert response.status_code == 500
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1

