from __future__ import annotations

from datetime import datetime
from typing import Any

import app.modules.admin.api_69_admin_user_detail.view as user_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Session giả lập để kiểm tra read-only behavior của API #69."""

    def __init__(self) -> None:
        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Đếm commit nếu view vô tình ghi dữ liệu."""

        self.commit_count += 1

    def rollback(self) -> None:
        """Đếm rollback của nhánh lỗi hoặc không tìm thấy resource."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override cung cấp fake session cho TestClient."""

    def dependency():
        """Yield session test cho dependency get_db."""

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


def admin_user_row(**overrides: Any) -> dict[str, Any]:
    """Tạo safe profile projection theo legacy users candidate."""

    return {
        "id": 1001,
        "full_name": "Ada Lovelace",
        "email": "ada@example.test",
        "role": "STUDENT",
        "avatar_url": None,
        "phone": None,
        "status": "ACTIVE",
        "created_at": datetime(2026, 10, 24, 9, 0),
        "updated_at": datetime(2026, 10, 24, 9, 30),
        **overrides,
    }


def get_admin_user_response(
    client: TestClient,
    user_id: str,
    *,
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi HTTP GET API #69 với raw path ID và Authorization tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.get(f"/api/v1/admin/users/{user_id}", headers=headers)


def test_get_admin_user_returns_safe_profile_and_preserves_nullable_fields(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả một UserProfile an toàn, giữ nullable fields và không lộ credential."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured: list[tuple[str, dict[str, int]]] = []

    def query_one(_db, query, params):
        """Ghi nhận query và trả row candidate cho user được yêu cầu."""

        captured.append((query, dict(params)))
        return admin_user_row(bio="unsupported", password_hash="must-not-leak")

    monkeypatch.setattr(user_view, "query_one", query_one)

    response = get_admin_user_response(client, "1001")

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"]["id"] == 1001
    assert payload["data"]["avatar_url"] is None
    assert payload["data"]["phone"] is None
    assert "bio" not in payload["data"]
    assert "password_hash" not in payload["data"]
    assert "password_hash" not in captured[0][0]
    assert captured[0][1] == {"user_id": 1001}
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert session.commit_count == 0
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    ("authorization", "roles", "expected_status", "expected_code"),
    [
        (None, None, 401, "DESIGN_AUTHENTICATION_REQUIRED"),
        ("Bearer valid-token", ["STUDENT"], 403, "DESIGN_ACCESS_DENIED"),
    ],
)
def test_get_admin_user_rejects_auth_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
    roles: list[str] | None,
    expected_status: int,
    expected_code: str,
) -> None:
    """Trả 401/403 trước khi lookup user nếu principal chưa được phép."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    if roles is not None:
        allow_admin_token(monkeypatch, roles=roles)

    def fail_query(*_args, **_kwargs):
        """Làm test thất bại nếu code truy vấn trước khi xác thực."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(user_view, "query_one", fail_query)

    response = get_admin_user_response(client, "1001", authorization=authorization)

    assert response.status_code == expected_status
    assert response.json()["businessCode"] == expected_code
    assert response.json()["data"] is None


@pytest.mark.parametrize(
    "user_id",
    ["invalid", "9223372036854775808", "-9223372036854775809", "1" * 21],
)
def test_get_admin_user_maps_invalid_int64_path_to_catalog_404(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    user_id: str,
) -> None:
    """Map malformed hoặc overflow path thành 404 và không query database."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Làm test thất bại nếu invalid path chạm tới database."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(user_view, "query_one", fail_query)

    response = get_admin_user_response(client, user_id)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert response.json()["data"] is None


def test_get_admin_user_returns_catalog_404_when_row_is_missing(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map missing user row thành resource not found sau authorization."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    monkeypatch.setattr(user_view, "query_one", lambda *_args, **_kwargs: None)

    response = get_admin_user_response(client, "1001")

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert response.json()["data"] is None
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_admin_user_maps_query_error_to_safe_500_and_rolls_back(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """DB exception trả lỗi an toàn, null data và rollback read transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)

    def raise_query_error(*_args, **_kwargs):
        """Tạo lỗi SQL giả để xác minh mapping an toàn."""

        raise SQLAlchemyError("sensitive SQL detail")

    monkeypatch.setattr(user_view, "query_one", raise_query_error)

    response = get_admin_user_response(client, "1001")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert "sensitive SQL detail" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize(
    "row",
    [{"id": 1002}, {"id": 1001}, admin_user_row(id=True)],
)
def test_get_admin_user_rejects_invalid_profile_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    row: dict[str, Any] | None,
) -> None:
    """Projection không hợp lệ hoặc lệch requested ID trả 500 an toàn."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    monkeypatch.setattr(user_view, "query_one", lambda *_args, **_kwargs: row)

    response = get_admin_user_response(client, "1001")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_admin_user_openapi_declares_int64_and_exact_error_set(
    client: TestClient,
) -> None:
    """OpenAPI khai báo int64 path, Admin header và đúng error set catalog."""

    operation = client.app.openapi()["paths"]["/api/v1/admin/users/{user_id}"]["get"]
    parameters = {item["name"]: item for item in operation["parameters"]}

    assert set(parameters) == {"user_id", "Authorization"}
    assert parameters["user_id"]["required"] is True
    assert parameters["user_id"]["schema"] == {"type": "integer", "format": "int64"}
    assert parameters["Authorization"]["required"] is True
    assert {"200", "401", "403", "404", "500"} <= set(operation["responses"])
    assert "422" not in operation["responses"]

    response_schema = operation["responses"]["200"]["content"]["application/json"]["schema"]
    envelope_name = response_schema["$ref"].rsplit("/", 1)[-1]
    envelope = client.app.openapi()["components"]["schemas"][envelope_name]
    profile_ref = envelope["properties"]["data"]["$ref"]
    profile_name = profile_ref.rsplit("/", 1)[-1]
    profile_schema = client.app.openapi()["components"]["schemas"][profile_name]
    assert "password_hash" not in profile_schema["properties"]
    assert "bio" not in profile_schema["properties"]
