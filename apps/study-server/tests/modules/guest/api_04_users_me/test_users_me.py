from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import app.modules.guest.api_04_users_me.view as users_me_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.core.responses import error_response
from app.modules.guest.api_04_users_me.query import CURRENT_USER_PROFILE
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    def __init__(self) -> None:
        """Khởi tạo phiên database giả với các bộ đếm commit/rollback dùng để xác minh transaction
        trong test."""
        self.rollback_count = 0

    def rollback(self) -> None:
        """Tăng bộ đếm rollback để test xác nhận transaction được hoàn tác khi lỗi."""
        self.rollback_count += 1


def make_user(*, include_password: bool = False) -> dict[str, Any]:
    """Tạo profile Student giả; có thể thêm hash để kiểm tra response không lộ
    thông tin xác thực."""
    created_at = datetime(2026, 9, 15, 12, 0, tzinfo=UTC)
    user: dict[str, Any] = {
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
    if include_password:
        user["password_hash"] = "secret-hash"
    return user


def override_db(session: FakeSession):
    """Tạo dependency thay thế database để route dùng FakeSession mà không mở kết nối thật."""
    def dependency():
        """Yield FakeSession được giữ trong closure cho request kiểm thử."""
        yield session

    return dependency


def valid_claims() -> dict[str, Any]:
    """Tạo claim access token hợp lệ cho một Student dùng trong kiểm thử."""
    return {"sub": "1001", "roles": ["STUDENT"]}


def test_current_user_returns_safe_profile_and_preserves_trace_id(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra API hồ sơ chỉ trả trường an toàn của Student và giữ trace ID trong body/header."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())
    monkeypatch.setattr(
        users_me_view,
        "find_current_user",
        lambda db, *, user_id: make_user(include_password=True),
    )

    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": "Bearer access-token",
            "X-Trace-Id": "00000000-0000-0000-0000-000000000001",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"]["id"] == 1001
    assert payload["data"]["role"] == "STUDENT"
    assert payload["data"]["created_at"] == "2026-09-15T12:00:00Z"
    assert payload["meta"] == {}
    assert payload["traceId"] == "00000000-0000-0000-0000-000000000001"
    assert "password_hash" not in payload["data"]
    assert "bio" not in payload["data"]
    assert response.headers["X-Trace-Id"] == "00000000-0000-0000-0000-000000000001"


def test_current_user_uses_sub_as_numeric_user_id(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra claim sub dạng chuỗi số được đổi thành user ID nguyên trước khi truy vấn."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    captured: dict[str, int] = {}
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())

    def find_user(db, *, user_id: int):
        """Ghi user ID được tra cứu và trả profile giả để kiểm tra ánh xạ claim sub."""
        captured["user_id"] = user_id
        return make_user()

    monkeypatch.setattr(users_me_view, "find_current_user", find_user)

    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer access-token"},
    )

    assert response.status_code == 200
    assert captured == {"user_id": 1001}
    assert "password_hash" not in CURRENT_USER_PROFILE


@pytest.mark.parametrize(
    "authorization",
    [None, "", "Basic access-token", "Bearer", "Bearer one two"],
)
def test_current_user_rejects_missing_or_malformed_bearer_header(
    client: TestClient,
    authorization: str | None,
) -> None:
    """Kiểm tra Authorization thiếu hoặc sai cú pháp Bearer bị từ chối trước khi đọc hồ sơ."""
    headers = {} if authorization is None else {"Authorization": authorization}

    response = client.get("/api/v1/users/me", headers=headers)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_current_user_rejects_invalid_jwt(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra JWT không hợp lệ hoặc hết hạn được ánh xạ thành lỗi xác thực HTTP 401."""
    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda token: error_response(
            status_code=401,
            business_code="DESIGN_AUTHENTICATION_REQUIRED",
            message="invalid token",
        ),
    )

    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


@pytest.mark.parametrize(
    "claims",
    [
        {"roles": ["STUDENT"]},
        {"sub": "not-a-number", "roles": ["STUDENT"]},
        {"sub": "1001"},
        {"sub": "1001", "roles": []},
        {"sub": "1001", "roles": [1]},
    ],
)
def test_current_user_rejects_invalid_required_claims(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    claims: dict[str, Any],
) -> None:
    """Kiểm tra access token thiếu subject hoặc role hợp lệ bị từ chối an toàn."""
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: claims)

    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer access-token"},
    )

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_current_user_rejects_non_student_before_database_lookup(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra user không có role STUDENT bị chặn trước khi gọi truy vấn database."""
    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda token: {"sub": "1001", "roles": ["MENTOR"]},
    )
    monkeypatch.setattr(
        users_me_view,
        "find_current_user",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer access-token"},
    )

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"


def test_current_user_maps_missing_database_record_to_authentication_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra không tìm thấy profile cho user đã xác thực được ánh xạ thành lỗi 401."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())
    monkeypatch.setattr(users_me_view, "find_current_user", lambda db, *, user_id: None)

    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer access-token"},
    )

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert session.rollback_count == 0


def test_current_user_rolls_back_and_hides_database_failure(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra lỗi truy vấn profile làm rollback Session và không lộ chi tiết database."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())
    monkeypatch.setattr(
        users_me_view,
        "find_current_user",
        lambda db, *, user_id: (_ for _ in ()).throw(SQLAlchemyError("database unavailable")),
    )

    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer access-token"},
    )

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "database unavailable" not in response.text
    assert session.rollback_count == 1


def test_current_user_maps_invalid_profile_shape_to_internal_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra hàng thiếu trường bắt buộc của UserProfile thành lỗi nội bộ an toàn."""
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())
    monkeypatch.setattr(
        users_me_view,
        "find_current_user",
        lambda db, *, user_id: {"id": 1001},
    )

    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer access-token"},
    )

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
