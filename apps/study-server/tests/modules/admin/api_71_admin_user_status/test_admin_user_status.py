"""HTTP tests cho API #71 khóa/mở khóa trạng thái tài khoản Admin."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import app.modules.admin.api_71_admin_user_status.view as status_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.admin.api_71_admin_user_status.query import (
    LOCK_ADMIN_USER_STATUS,
    REVOKE_ADMIN_USER_REFRESH_TOKENS,
    UPDATE_ADMIN_USER_STATUS,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Đếm transaction calls và mô phỏng lỗi commit cho HTTP tests API #71."""

    def __init__(self, *, fail_commit: bool = False) -> None:
        """Khởi tạo bộ đếm transaction và tùy chọn mô phỏng lỗi commit."""

        self.commit_count = 0
        self.rollback_count = 0
        self.fail_commit = fail_commit

    def commit(self) -> None:
        """Ghi nhận commit hoặc phát sinh lỗi DB đã cấu hình."""

        self.commit_count += 1
        if self.fail_commit:
            raise SQLAlchemyError("sensitive commit detail")

    def rollback(self) -> None:
        """Ghi nhận rollback của nhánh lỗi hoặc no-row."""

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
    """Cài decoder giả trả JWT Admin hoặc danh sách role được yêu cầu."""

    def decode_token(_token: str) -> dict[str, Any]:
        """Trả claim tối thiểu mà shared guard cần để xác thực request."""

        return {"sub": "9001", "roles": roles or ["ADMIN"]}

    monkeypatch.setattr(auth_utils, "decode_access_token", decode_token)


def status_body(status: str = "SUSPENDED") -> dict[str, str]:
    """Tạo request body candidate có target status được chọn."""

    return {"status": status}


def user_status_row(status: str = "ACTIVE") -> dict[str, str]:
    """Tạo row tối thiểu cho query khóa user hiện tại."""

    return {"status": status}


def updated_profile_row(
    status: str = "SUSPENDED",
    **overrides: Any,
) -> dict[str, Any]:
    """Tạo projection safe tương ứng với UPDATE RETURNING legacy users."""

    return {
        "id": 1001,
        "full_name": "Ada Lovelace",
        "email": "ada@example.test",
        "role": "STUDENT",
        "avatar_url": None,
        "phone": None,
        "status": status,
        "created_at": datetime(2026, 10, 24, 9, 0),
        "updated_at": datetime(2026, 10, 25, 9, 30),
        **overrides,
    }


def patch_admin_user_status(
    client: TestClient,
    user_id: str,
    body: Any = None,
    *,
    authorization: str | None = "Bearer valid-admin-token",
    send_body: bool = True,
):
    """Gửi HTTP PATCH API #71 với raw path/header và body tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.patch(
        f"/api/v1/admin/users/{user_id}/status",
        headers=headers,
        json=body if send_body else None,
    )


def install_status_queries(
    monkeypatch: pytest.MonkeyPatch,
    *,
    current_status: str = "ACTIVE",
    fail_statement: str | None = None,
    returned_row: dict[str, Any] | None = None,
) -> list[tuple[str, dict[str, Any]]]:
    """Cài fake lock/update queries và trả lại danh sách SQL bindings."""

    captured: list[tuple[str, dict[str, Any]]] = []

    def query_one(_db: Any, query: str, params: dict[str, Any]) -> dict[str, Any] | None:
        """Ghi query hiện tại và trả fake row tương ứng với SQL constant."""

        captured.append((query, dict(params)))
        if query == fail_statement:
            raise SQLAlchemyError("sensitive query detail")
        if query == LOCK_ADMIN_USER_STATUS:
            return user_status_row(current_status)
        if query == UPDATE_ADMIN_USER_STATUS:
            return returned_row or updated_profile_row(params["status"])
        return None

    monkeypatch.setattr(status_view, "query_one", query_one)
    return captured


def test_patch_suspends_user_and_revokes_active_refresh_tokens(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cập nhật sang SUSPENDED, revoke refresh tokens trong transaction và lọt bỏ secret fields."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_status_queries(monkeypatch)
    revoked: list[tuple[str, dict[str, Any]]] = []

    def execute_query(_db: Any, query: str, params: dict[str, Any]) -> object:
        """Ghi câu revoke và bind user ID để xác minh side effect có giới hạn."""

        revoked.append((query, dict(params)))
        return object()

    monkeypatch.setattr(status_view, "execute_query", execute_query)

    response = patch_admin_user_status(client, "1001", status_body())

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_UPDATED"
    assert payload["data"]["status"] == "SUSPENDED"
    assert "password_hash" not in payload["data"]
    assert "token_hash" not in payload["data"]
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert [query for query, _params in captured] == [
        LOCK_ADMIN_USER_STATUS,
        UPDATE_ADMIN_USER_STATUS,
    ]
    assert captured[1][1] == {"user_id": 1001, "status": "SUSPENDED"}
    assert revoked == [(REVOKE_ADMIN_USER_REFRESH_TOKENS, {"user_id": 1001})]
    assert session.commit_count == 1
    assert session.rollback_count == 0


def test_patch_activates_user_without_restoring_refresh_tokens(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Mở khóa bằng ACTIVE nhưng không chạy câu revoke hoặc khôi phục token rows cũ."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_status_queries(monkeypatch, current_status="SUSPENDED")
    revoked: list[str] = []

    def execute_query(_db: Any, query: str, _params: dict[str, Any]) -> object:
        """Ghi nhận nếu API vô tình chạy revoke khi mở khóa."""

        revoked.append(query)
        return object()

    monkeypatch.setattr(status_view, "execute_query", execute_query)

    response = patch_admin_user_status(client, "1001", status_body("ACTIVE"))

    assert response.status_code == 200
    assert response.json()["data"]["status"] == "ACTIVE"
    assert [query for query, _params in captured] == [
        LOCK_ADMIN_USER_STATUS,
        UPDATE_ADMIN_USER_STATUS,
    ]
    assert revoked == []
    assert session.commit_count == 1
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    "body,send_body",
    [
        (None, False),
        ({}, True),
        ({"status": None}, True),
        ({"status": "PENDING_EMAIL_VERIFICATION"}, True),
        ({"status": "ACTIVE", "role": "ADMIN"}, True),
    ],
)
def test_patch_rejects_missing_invalid_or_extra_body_fields(
    client: TestClient,
    body: Any,
    send_body: bool,
) -> None:
    """Yêu cầu status rõ ràng và từ chối null, giá trị ngoài allowlist hoặc field thừa."""

    response = patch_admin_user_status(client, "1001", body, send_body=send_body)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["data"] is None


@pytest.mark.parametrize("user_id", ["abc", str(2**63), str(-(2**63) - 1)])
def test_patch_rejects_malformed_or_out_of_range_user_id(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    user_id: str,
) -> None:
    """Map raw path không phải signed-int64 sang lỗi 422 mà không query DB."""

    allow_admin_token(monkeypatch)
    calls: list[str] = []

    def query_one(_db: Any, query: str, _params: dict[str, Any]) -> None:
        """Đếm truy vấn để xác minh path lỗi dừng trước DB."""

        calls.append(query)

    monkeypatch.setattr(status_view, "query_one", query_one)

    response = patch_admin_user_status(client, user_id, status_body())

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["data"] is None
    assert calls == []


def test_patch_requires_authentication_before_database_access(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 401 khi thiếu Bearer token và không query user."""

    calls: list[str] = []

    def query_one(_db: Any, query: str, _params: dict[str, Any]) -> None:
        """Ghi nhận truy vấn nếu guard không dừng trước DB."""

        calls.append(query)

    monkeypatch.setattr(status_view, "query_one", query_one)

    response = patch_admin_user_status(
        client,
        "1001",
        status_body(),
        authorization=None,
    )

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert calls == []


def test_patch_requires_admin_role_before_database_access(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 403 cho JWT không có ADMIN role và không query user."""

    allow_admin_token(monkeypatch, roles=["MENTOR"])
    calls: list[str] = []

    def query_one(_db: Any, query: str, _params: dict[str, Any]) -> None:
        """Ghi nhận truy vấn nếu role guard không dừng trước DB."""

        calls.append(query)

    monkeypatch.setattr(status_view, "query_one", query_one)

    response = patch_admin_user_status(client, "1001", status_body())

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert calls == []


def test_patch_returns_not_found_and_rolls_back_when_user_is_missing(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map missing locked user row sang catalog 404 và đóng read transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)

    def query_one(_db: Any, _query: str, _params: dict[str, Any]) -> None:
        """Mô phỏng không có user row cho câu SELECT FOR UPDATE."""

        return None

    monkeypatch.setattr(status_view, "query_one", query_one)

    response = patch_admin_user_status(client, "1001", status_body())

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize("current_status", ["PENDING_EMAIL_VERIFICATION", "DELETED"])
def test_patch_rejects_non_lockable_current_account_state(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    current_status: str,
) -> None:
    """Không cho API lock/unlock chuyển pending/deleted lifecycle status sang ACTIVE."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_status_queries(
        monkeypatch,
        current_status=current_status,
    )
    revoked: list[str] = []

    def execute_query(_db: Any, query: str, _params: dict[str, Any]) -> object:
        """Ghi nhận rằng trạng thái không hợp lệ không thu hồi token."""

        revoked.append(query)
        return object()

    monkeypatch.setattr(status_view, "execute_query", execute_query)

    response = patch_admin_user_status(client, "1001", status_body("ACTIVE"))

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["data"] is None
    assert [query for query, _params in captured] == [LOCK_ADMIN_USER_STATUS]
    assert revoked == []
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_patch_maps_malformed_locked_status_projection_to_safe_500(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map malformed SELECT FOR UPDATE projection thành safe 500."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)

    def query_one(_db: Any, _query: str, _params: dict[str, Any]) -> dict[str, Any]:
        """Trả status projection sai kiểu để kiểm tra integrity guard."""

        return {"status": 7}

    monkeypatch.setattr(status_view, "query_one", query_one)

    response = patch_admin_user_status(client, "1001", status_body())

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert "sensitive" not in response.text
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize("statement", [LOCK_ADMIN_USER_STATUS, UPDATE_ADMIN_USER_STATUS])
def test_patch_rolls_back_query_failures_safely(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    statement: str,
) -> None:
    """Rollback khi lock hoặc update SQL lỗi và không phản chiếu chi tiết DB."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_status_queries(monkeypatch, fail_statement=statement)

    response = patch_admin_user_status(client, "1001", status_body())

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert "sensitive query detail" not in response.text
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_patch_rolls_back_invalid_updated_profile_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Không commit nếu UPDATE RETURNING có row sai user ID hoặc sai target status."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_status_queries(
        monkeypatch,
        returned_row=updated_profile_row(status="ACTIVE", id=1002),
    )

    response = patch_admin_user_status(client, "1001", status_body())

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_patch_rolls_back_when_refresh_revoke_fails(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Rollback cả status mutation nếu revoke refresh-token rows lỗi."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_status_queries(monkeypatch)

    def execute_query(_db: Any, query: str, _params: dict[str, Any]) -> object:
        """Phát sinh lỗi giả khi transaction thực hiện conditional revoke."""

        assert query == REVOKE_ADMIN_USER_REFRESH_TOKENS
        raise SQLAlchemyError("sensitive revoke detail")

    monkeypatch.setattr(status_view, "execute_query", execute_query)

    response = patch_admin_user_status(client, "1001", status_body())

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "sensitive revoke detail" not in response.text
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_patch_rolls_back_commit_failure_safely(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map commit failure thành safe 500 và thử rollback transaction."""

    session = FakeSession(fail_commit=True)
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_status_queries(monkeypatch)

    def execute_query(_db: Any, _query: str, _params: dict[str, Any]) -> object:
        """Cho phép revoke query thành công trước khi commit lỗi."""

        return object()

    monkeypatch.setattr(status_view, "execute_query", execute_query)

    response = patch_admin_user_status(client, "1001", status_body())

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "sensitive commit detail" not in response.text
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_patch_openapi_declares_direct_contract_and_derived_body(
    client: TestClient,
) -> None:
    """Kiểm tra route method/path/body/Authorization và exact catalog response set."""

    schema = client.app.openapi()
    path = "/api/v1/admin/users/{user_id}/status"
    operation = schema["paths"][path]["patch"]
    parameters = {item["name"]: item for item in operation["parameters"]}
    assert parameters["user_id"]["required"] is True
    assert parameters["user_id"]["schema"] == {"type": "integer", "format": "int64"}
    assert parameters["Authorization"]["required"] is True

    request_schema = operation["requestBody"]["content"]["application/json"]["schema"]
    if "$ref" in request_schema:
        name = request_schema["$ref"].rsplit("/", 1)[-1]
        request_schema = schema["components"]["schemas"][name]
    assert request_schema["required"] == ["status"]
    assert request_schema["properties"]["status"]["enum"] == ["ACTIVE", "SUSPENDED"]
    assert set(operation["responses"]) == {"200", "401", "403", "404", "422", "500"}
