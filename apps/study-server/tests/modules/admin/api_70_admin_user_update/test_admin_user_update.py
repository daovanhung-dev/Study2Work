"""HTTP tests cho API #70 cập nhật profile và role người dùng."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import app.modules.admin.api_70_admin_user_update.view as user_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Đếm transaction calls và có thể giả lập lỗi commit cho API #70."""

    def __init__(self, *, fail_commit: bool = False) -> None:
        self.commit_count = 0
        self.rollback_count = 0
        self.fail_commit = fail_commit

    def commit(self) -> None:
        """Ghi nhận commit hoặc phát sinh lỗi DB được cấu hình."""

        self.commit_count += 1
        if self.fail_commit:
            raise SQLAlchemyError("sensitive commit detail")

    def rollback(self) -> None:
        """Ghi nhận rollback của nhánh lỗi hoặc không tìm thấy user."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override cung cấp fake session cho TestClient."""

    def dependency():
        """Yield fake session cho dependency get_db."""

        yield session

    return dependency


def allow_admin_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Cài decoder giả trả JWT Admin hoặc role test được chỉ định."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": roles or ["ADMIN"]},
    )


def update_body(**overrides: Any) -> dict[str, Any]:
    """Tạo full-replacement body với bốn field candidate của API #70."""

    return {
        "full_name": "Ada Lovelace",
        "phone": "1234567890",
        "avatar_url": "https://example.test/avatar.png",
        "role": "STUDENT",
        **overrides,
    }


def updated_user_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection an toàn tương ứng với UPDATE RETURNING legacy users."""

    return {
        "id": 1001,
        "full_name": "Ada Lovelace",
        "email": "ada@example.test",
        "role": "STUDENT",
        "avatar_url": "https://example.test/avatar.png",
        "phone": "1234567890",
        "status": "SUSPENDED",
        "created_at": datetime(2026, 10, 24, 9, 0),
        "updated_at": datetime(2026, 10, 25, 9, 30),
        **overrides,
    }


def put_admin_user_response(
    client: TestClient,
    user_id: str,
    body: dict[str, Any] | None = None,
    *,
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi HTTP PUT API #70 với raw path và JSON body tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.put(
        f"/api/v1/admin/users/{user_id}",
        headers=headers,
        json=body if body is not None else update_body(),
    )


def test_put_admin_user_updates_profile_and_role_safely(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cập nhật các field được chọn, chuẩn hóa input và giữ status/email nguyên trạng."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured: list[tuple[str, dict[str, Any]]] = []

    def query_one(_db, query, params):
        """Ghi query/params và trả projection như UPDATE RETURNING."""

        captured.append((query, dict(params)))
        return updated_user_row(
            full_name=params["full_name"],
            phone=params["phone"],
            avatar_url=params["avatar_url"],
            role=params["role"],
            password_hash="must-not-leak",
            bio="unsupported",
        )

    monkeypatch.setattr(user_view, "query_one", query_one)

    response = put_admin_user_response(
        client,
        "1001",
        update_body(
            full_name="  Ada Lovelace  ",
            phone="   ",
            avatar_url=None,
            role="MENTOR",
        ),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_UPDATED"
    assert payload["data"]["full_name"] == "Ada Lovelace"
    assert payload["data"]["phone"] is None
    assert payload["data"]["avatar_url"] is None
    assert payload["data"]["role"] == "MENTOR"
    assert payload["data"]["status"] == "SUSPENDED"
    assert payload["data"]["email"] == "ada@example.test"
    assert "bio" not in payload["data"]
    assert "password_hash" not in payload["data"]
    assert "password_hash" not in captured[0][0]
    assert captured[0][1] == {
        "user_id": 1001,
        "full_name": "Ada Lovelace",
        "phone": None,
        "avatar_url": None,
        "role": "MENTOR",
    }
    assert "status =" not in captured[0][0]
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert session.commit_count == 1
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    ("authorization", "roles", "expected_status", "expected_code"),
    [
        (None, None, 401, "DESIGN_AUTHENTICATION_REQUIRED"),
        ("Bearer valid-token", ["STUDENT"], 403, "DESIGN_ACCESS_DENIED"),
    ],
)
def test_put_admin_user_rejects_auth_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
    roles: list[str] | None,
    expected_status: int,
    expected_code: str,
) -> None:
    """Trả 401/403 trước UPDATE nếu caller không có quyền ADMIN."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    if roles is not None:
        allow_admin_token(monkeypatch, roles=roles)

    def fail_query(*_args, **_kwargs):
        """Làm test thất bại nếu API truy vấn trước khi xác thực."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(user_view, "query_one", fail_query)

    response = put_admin_user_response(client, "1001", authorization=authorization)

    assert response.status_code == expected_status
    assert response.json()["businessCode"] == expected_code
    assert response.json()["data"] is None


@pytest.mark.parametrize("user_id", ["invalid", "9223372036854775808", "-9223372036854775809"])
def test_put_admin_user_maps_invalid_int64_path_to_validation_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    user_id: str,
) -> None:
    """Map malformed/out-of-range path thành catalog 422 mà không chạy UPDATE."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Làm test thất bại nếu path sai vẫn chạm database."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(user_view, "query_one", fail_query)

    response = put_admin_user_response(client, user_id)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0]["field"] == "user_id"


@pytest.mark.parametrize(
    "body",
    [
        update_body(role="SUPER_ADMIN"),
        update_body(status="SUSPENDED"),
        {"full_name": "Ada", "avatar_url": None, "role": "STUDENT"},
        update_body(full_name="   "),
        update_body(full_name="A" * 151),
        update_body(phone="1" * 21),
    ],
)
def test_put_admin_user_rejects_invalid_candidate_body(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    body: dict[str, Any],
) -> None:
    """Body thiếu field, role lạ, field ngoài scope hoặc profile sai trả 422."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Làm test thất bại nếu body không hợp lệ chạy mutation."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(user_view, "query_one", fail_query)

    response = put_admin_user_response(client, "1001", body)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["data"] is None


def test_put_admin_user_returns_catalog_404_when_update_has_no_row(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map UPDATE RETURNING không có row thành 404 và rollback transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    monkeypatch.setattr(user_view, "query_one", lambda *_args, **_kwargs: None)

    response = put_admin_user_response(client, "1001")

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert response.json()["data"] is None
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_put_admin_user_maps_query_failure_to_safe_500_and_rolls_back(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """SQL failure trả lỗi an toàn, không lộ chi tiết và rollback."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)

    def raise_query_error(*_args, **_kwargs):
        """Tạo SQLAlchemyError giả để kiểm tra ánh xạ lỗi."""

        raise SQLAlchemyError("sensitive SQL detail")

    monkeypatch.setattr(user_view, "query_one", raise_query_error)

    response = put_admin_user_response(client, "1001")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert "sensitive SQL detail" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize(
    "row",
    [{"id": 1001}, updated_user_row(id=1002), updated_user_row(id=True)],
)
def test_put_admin_user_rejects_invalid_returning_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    row: dict[str, Any],
) -> None:
    """Projection thiếu field hoặc lệch user ID rollback và trả 500 an toàn."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    monkeypatch.setattr(user_view, "query_one", lambda *_args, **_kwargs: row)

    response = put_admin_user_response(client, "1001")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_put_admin_user_maps_commit_failure_to_safe_500_and_rolls_back(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Commit lỗi trả 500 an toàn và gọi rollback trên Session."""

    session = FakeSession(fail_commit=True)
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    monkeypatch.setattr(user_view, "query_one", lambda *_args, **_kwargs: updated_user_row())

    response = put_admin_user_response(client, "1001")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert "sensitive commit detail" not in response.text
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_put_admin_user_openapi_declares_candidate_body_and_exact_catalog_errors(
    client: TestClient,
) -> None:
    """OpenAPI công bố path int64, body candidate, Admin header và error set #70."""

    operation = client.app.openapi()["paths"]["/api/v1/admin/users/{user_id}"]["put"]
    parameters = {item["name"]: item for item in operation["parameters"]}

    assert set(parameters) == {"user_id", "Authorization"}
    assert parameters["user_id"]["required"] is True
    assert parameters["user_id"]["schema"] == {"type": "integer", "format": "int64"}
    assert parameters["Authorization"]["required"] is True
    assert set(operation["responses"]) == {"200", "401", "403", "404", "422", "500"}

    request_schema = operation["requestBody"]["content"]["application/json"]["schema"]
    request_name = request_schema["$ref"].rsplit("/", 1)[-1]
    body_schema = client.app.openapi()["components"]["schemas"][request_name]
    assert set(body_schema["required"]) == {"full_name", "phone", "avatar_url", "role"}
    assert set(body_schema["properties"]) == {"full_name", "phone", "avatar_url", "role"}
    assert body_schema["properties"]["role"]["enum"] == ["STUDENT", "MENTOR", "ADMIN"]

    response_schema = operation["responses"]["200"]["content"]["application/json"]["schema"]
    envelope_name = response_schema["$ref"].rsplit("/", 1)[-1]
    envelope = client.app.openapi()["components"]["schemas"][envelope_name]
    profile_ref = envelope["properties"]["data"]["$ref"]
    profile_name = profile_ref.rsplit("/", 1)[-1]
    profile_schema = client.app.openapi()["components"]["schemas"][profile_name]
    assert "password_hash" not in profile_schema["properties"]
    assert "bio" not in profile_schema["properties"]
