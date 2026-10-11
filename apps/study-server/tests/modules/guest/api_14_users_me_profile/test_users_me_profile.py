from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import app.modules.guest.api_14_users_me_profile.view as profile_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.guest.api_14_users_me_profile.query import UPDATE_CURRENT_USER_PROFILE
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    def __init__(self, *, commit_error: bool = False) -> None:
        """Khởi tạo Session giả và tùy chọn phát sinh lỗi khi commit để kiểm thử rollback."""

        self.commit_count = 0
        self.rollback_count = 0
        self.commit_error = commit_error

    def commit(self) -> None:
        """Tăng bộ đếm commit hoặc phát sinh SQLAlchemyError theo cấu hình test."""

        self.commit_count += 1
        if self.commit_error:
            raise SQLAlchemyError("commit failed")

    def rollback(self) -> None:
        """Tăng bộ đếm rollback để xác nhận transaction được hoàn tác."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency database thay thế để route sử dụng cùng một FakeSession."""

    def dependency():
        """Yield Session giả được giữ trong closure cho một request kiểm thử."""

        yield session

    return dependency


def valid_claims() -> dict[str, Any]:
    """Tạo access-token claims hợp lệ cho Student có user ID 1001."""

    return {"sub": "1001", "roles": ["STUDENT"]}


def make_updated_user(
    *,
    full_name: str = "Nguyen Van A",
    phone: str | None = None,
    avatar_url: str | None = None,
) -> dict[str, Any]:
    """Tạo hàng profile an toàn giống kết quả UPDATE RETURNING của API #14."""

    created_at = datetime(2026, 9, 15, 12, 0, tzinfo=UTC)
    return {
        "id": 1001,
        "full_name": full_name,
        "email": "student@example.com",
        "role": "STUDENT",
        "avatar_url": avatar_url,
        "phone": phone,
        "status": "ACTIVE",
        "created_at": created_at,
        "updated_at": datetime(2026, 10, 3, 8, 0, tzinfo=UTC),
    }


def valid_payload() -> dict[str, Any]:
    """Tạo request body đầy đủ cho ba field source-backed của API #14."""

    return {
        "full_name": "Nguyen Van A",
        "phone": "+84901234567",
        "avatar_url": "https://cdn.example.test/avatar.png",
    }


def test_update_profile_updates_source_backed_fields_and_ignores_bio(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra API cập nhật field hiện có, bỏ qua bio và commit profile an toàn."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    captured: dict[str, Any] = {}
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())

    def update_user(db, *, user_id: int, user_data):
        """Ghi dữ liệu đã chuẩn hóa và trả profile giả cho response thành công."""

        captured.update(
            user_id=user_id,
            full_name=user_data.full_name,
            phone=user_data.phone,
            avatar_url=user_data.avatar_url,
        )
        return make_updated_user(
            full_name=user_data.full_name,
            phone=user_data.phone,
            avatar_url=user_data.avatar_url,
        )

    monkeypatch.setattr(profile_view, "update_current_user_profile", update_user)

    response = client.put(
        "/api/v1/users/me/profile",
        headers={
            "Authorization": "Bearer access-token",
            "X-Trace-Id": "00000000-0000-0000-0000-000000000014",
        },
        json={
            "full_name": "  Nguyen Van A  ",
            "bio": "temporarily ignored",
            "phone": "   ",
            "avatar_url": "  https://cdn.example.test/avatar.png  ",
        },
    )

    assert response.status_code == 200
    assert captured == {
        "user_id": 1001,
        "full_name": "Nguyen Van A",
        "phone": None,
        "avatar_url": "https://cdn.example.test/avatar.png",
    }
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_UPDATED"
    assert payload["data"]["phone"] is None
    assert "bio" not in payload["data"]
    assert "password_hash" not in payload["data"]
    assert payload["traceId"] == "00000000-0000-0000-0000-000000000014"
    assert session.commit_count == 1
    assert session.rollback_count == 0


def test_update_profile_accepts_null_for_nullable_fields(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra phone và avatar_url có thể được xóa bằng giá trị null."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())
    monkeypatch.setattr(
        profile_view,
        "update_current_user_profile",
        lambda db, *, user_id, user_data: make_updated_user(
            full_name=user_data.full_name,
            phone=user_data.phone,
            avatar_url=user_data.avatar_url,
        ),
    )

    response = client.put(
        "/api/v1/users/me/profile",
        headers={"Authorization": "Bearer access-token"},
        json={"full_name": "Student", "phone": None, "avatar_url": None},
    )

    assert response.status_code == 200
    assert response.json()["data"]["phone"] is None
    assert response.json()["data"]["avatar_url"] is None
    assert session.commit_count == 1


@pytest.mark.parametrize(
    "payload",
    [
        {"full_name": "Student", "phone": None},
        {"full_name": "Student", "avatar_url": None},
        {"phone": None, "avatar_url": None},
    ],
)
def test_update_profile_requires_all_source_backed_fields(
    client: TestClient,
    payload: dict[str, Any],
) -> None:
    """Kiểm tra PUT yêu cầu đủ full_name, phone và avatar_url kể cả khi field nullable."""

    response = client.put(
        "/api/v1/users/me/profile",
        headers={"Authorization": "Bearer access-token"},
        json=payload,
    )

    assert response.status_code == 422
    assert response.json()["businessCode"] == "VALIDATION_ERROR"


def test_update_profile_rejects_blank_full_name_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra full_name chỉ có khoảng trắng bị từ chối trước mutation database."""

    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())
    monkeypatch.setattr(
        profile_view,
        "update_current_user_profile",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("invalid input must not update")
        ),
    )
    payload = valid_payload()
    payload["full_name"] = "   "

    response = client.put(
        "/api/v1/users/me/profile",
        headers={"Authorization": "Bearer access-token"},
        json=payload,
    )

    assert response.status_code == 422
    assert response.json()["meta"]["fieldErrors"][0]["field"] == "full_name"


def test_update_profile_requires_bearer_token(client: TestClient) -> None:
    """Kiểm tra request đủ body nhưng thiếu Bearer token nhận lỗi xác thực 401."""

    response = client.put(
        "/api/v1/users/me/profile",
        json=valid_payload(),
    )

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_update_profile_rejects_non_student_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra role không phải Student nhận 403 trước khi update database."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda token: {"sub": "1001", "roles": ["MENTOR"]},
    )
    monkeypatch.setattr(
        profile_view,
        "update_current_user_profile",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("unauthorized role must not update")
        ),
    )

    response = client.put(
        "/api/v1/users/me/profile",
        headers={"Authorization": "Bearer access-token"},
        json=valid_payload(),
    )

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"


def test_update_profile_maps_missing_user_to_authentication_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra UPDATE không trả row được ánh xạ thành lỗi xác thực và rollback."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())
    monkeypatch.setattr(
        profile_view,
        "update_current_user_profile",
        lambda db, **kwargs: None,
    )

    response = client.put(
        "/api/v1/users/me/profile",
        headers={"Authorization": "Bearer access-token"},
        json=valid_payload(),
    )

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_update_profile_rolls_back_database_failure(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra lỗi UPDATE được che giấu, rollback và trả lỗi nội bộ an toàn."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())
    monkeypatch.setattr(
        profile_view,
        "update_current_user_profile",
        lambda db, **kwargs: (_ for _ in ()).throw(SQLAlchemyError("database unavailable")),
    )

    response = client.put(
        "/api/v1/users/me/profile",
        headers={"Authorization": "Bearer access-token"},
        json=valid_payload(),
    )

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "database unavailable" not in response.text
    assert session.rollback_count == 1


def test_update_profile_rolls_back_invalid_returning_shape(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra profile RETURNING thiếu field bị rollback trước commit."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())
    monkeypatch.setattr(
        profile_view,
        "update_current_user_profile",
        lambda db, **kwargs: {"id": 1001},
    )

    response = client.put(
        "/api/v1/users/me/profile",
        headers={"Authorization": "Bearer access-token"},
        json=valid_payload(),
    )

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_update_profile_rolls_back_commit_failure(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra commit thất bại được rollback và trả lỗi nội bộ."""

    session = FakeSession(commit_error=True)
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: valid_claims())
    monkeypatch.setattr(
        profile_view,
        "update_current_user_profile",
        lambda db, **kwargs: make_updated_user(),
    )

    response = client.put(
        "/api/v1/users/me/profile",
        headers={"Authorization": "Bearer access-token"},
        json=valid_payload(),
    )

    assert response.status_code == 500
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_update_query_excludes_bio_and_sensitive_fields() -> None:
    """Kiểm tra SQL API #14 không ghi bio chưa tồn tại hoặc field nhạy cảm/ngoài phạm vi."""

    normalized_query = UPDATE_CURRENT_USER_PROFILE.lower()
    assert "bio" not in normalized_query
    assert "password_hash" not in normalized_query
    assert "email =" not in normalized_query
    assert "role =" not in normalized_query
    assert "status =" not in normalized_query
