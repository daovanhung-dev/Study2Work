"""HTTP tests cho API #72 soft-delete user trong Admin."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import app.modules.admin.api_72_admin_user_delete.view as delete_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.admin.api_72_admin_user_delete.query import SOFT_DELETE_ADMIN_USER
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Đếm transaction calls và mô phỏng commit failure cho API #72."""

    def __init__(self, *, fail_commit: bool = False) -> None:
        """Khởi tạo bộ đếm transaction với tùy chọn lỗi commit."""

        self.commit_count = 0
        self.rollback_count = 0
        self.fail_commit = fail_commit

    def commit(self) -> None:
        """Ghi nhận commit hoặc phát sinh lỗi database đã cấu hình."""

        self.commit_count += 1
        if self.fail_commit:
            raise SQLAlchemyError("sensitive commit detail")

    def rollback(self) -> None:
        """Ghi nhận rollback của nhánh lỗi hoặc không tìm thấy row."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override cấp fake session cho TestClient."""

    def dependency():
        """Yield fake session cho dependency get_db."""

        yield session

    return dependency


def allow_admin_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Cài decoder giả trả claim ADMIN hoặc role được test yêu cầu."""

    def decode_token(_token: str) -> dict[str, Any]:
        """Trả claim tối thiểu mà shared role guard cần."""

        return {"sub": "9001", "roles": roles or ["ADMIN"]}

    monkeypatch.setattr(auth_utils, "decode_access_token", decode_token)


def delete_request(
    client: TestClient,
    user_id: str,
    *,
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi HTTP DELETE API #72 với raw path và Authorization tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.request("DELETE", f"/api/v1/admin/users/{user_id}", headers=headers)


def deleted_user_row(**overrides: Any) -> dict[str, Any]:
    """Tạo UPDATE RETURNING row gồm ID và timestamp của soft-delete."""

    return {
        "id": 1001,
        "deleted_at": datetime(2026, 10, 25, 10, 30),
        **overrides,
    }


def install_delete_query(
    monkeypatch: pytest.MonkeyPatch,
    *,
    returned_row: Any = None,
    fail_query: bool = False,
) -> list[tuple[str, dict[str, Any]]]:
    """Cài query giả, ghi statement/bindings và trả row cấu hình."""

    captured: list[tuple[str, dict[str, Any]]] = []

    def query_one(_db: Any, query: str, params: dict[str, Any]) -> Any:
        """Ghi một truy vấn và mô phỏng success, no-row hoặc database failure."""

        captured.append((query, dict(params)))
        if fail_query:
            raise SQLAlchemyError("sensitive query detail")
        return returned_row

    monkeypatch.setattr(delete_view, "query_one", query_one)
    return captured


def test_delete_soft_marks_user_and_returns_delete_result(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Ghi status marker thay cho hard-delete và trả timestamp từ UPDATE."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_delete_query(monkeypatch, returned_row=deleted_user_row())

    response = delete_request(client, "1001")

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_DELETED"
    assert payload["data"] == {
        "id": 1001,
        "status": "deleted",
        "deleted_at": "2026-10-25T10:30:00",
    }
    assert payload["meta"] == {}
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert captured == [(SOFT_DELETE_ADMIN_USER, {"user_id": 1001})]
    assert "DELETE FROM" not in SOFT_DELETE_ADMIN_USER.upper()
    assert session.commit_count == 1
    assert session.rollback_count == 0


def test_delete_returns_not_found_and_rolls_back_when_update_has_no_row(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map missing/already-DELETED row sang catalog 404."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_delete_query(monkeypatch)

    response = delete_request(client, "1001")

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert response.json()["data"] is None
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize("user_id", ["abc", str(2**63), str(-(2**63) - 1)])
def test_delete_rejects_malformed_or_out_of_range_int64_before_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    user_id: str,
) -> None:
    """Map raw path không phải signed-int64 thành 422 trước database."""

    allow_admin_token(monkeypatch)
    calls: list[str] = []

    def query_one(_db: Any, query: str, _params: dict[str, Any]) -> None:
        """Ghi lại truy vấn bất ngờ nếu path invalid vượt qua validator."""

        calls.append(query)

    monkeypatch.setattr(delete_view, "query_one", query_one)

    response = delete_request(client, user_id)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["data"] is None
    assert calls == []


def test_delete_requires_authentication_before_database_access(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 401 khi thiếu Bearer JWT và không query user."""

    calls: list[str] = []

    def query_one(_db: Any, query: str, _params: dict[str, Any]) -> None:
        """Ghi lại truy vấn bất ngờ nếu auth guard không chặn request."""

        calls.append(query)

    monkeypatch.setattr(delete_view, "query_one", query_one)
    response = delete_request(client, "1001", authorization=None)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert calls == []


def test_delete_requires_admin_role_before_database_access(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 403 cho JWT không có ADMIN role và không query user."""

    allow_admin_token(monkeypatch, roles=["MENTOR"])
    calls: list[str] = []

    def query_one(_db: Any, query: str, _params: dict[str, Any]) -> None:
        """Ghi truy vấn bất ngờ để kiểm tra thứ tự role guard."""

        calls.append(query)

    monkeypatch.setattr(delete_view, "query_one", query_one)
    response = delete_request(client, "1001")

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert calls == []


def test_delete_maps_malformed_returning_projection_to_safe_500(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Không commit khi UPDATE RETURNING thiếu timestamp hợp lệ hoặc sai ID."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_delete_query(
        monkeypatch,
        returned_row=deleted_user_row(id=1002, deleted_at="not-a-timestamp"),
    )

    response = delete_request(client, "1001")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert "not-a-timestamp" not in response.text
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_delete_rolls_back_query_failure_without_exposing_database_detail(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Rollback query exception và chỉ trả message hệ thống an toàn."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_delete_query(monkeypatch, fail_query=True)

    response = delete_request(client, "1001")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "sensitive query detail" not in response.text
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_delete_rolls_back_commit_failure_safely(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map lỗi commit thành 500 an toàn và gọi rollback."""

    session = FakeSession(fail_commit=True)
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_delete_query(monkeypatch, returned_row=deleted_user_row())

    response = delete_request(client, "1001")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "sensitive commit detail" not in response.text
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_delete_openapi_matches_catalog_and_has_no_request_body(client: TestClient) -> None:
    """Kiểm tra DELETE path, int64/header, không body và exact error response set."""

    schema = client.app.openapi()
    operation = schema["paths"]["/api/v1/admin/users/{user_id}"]["delete"]
    parameters = {item["name"]: item for item in operation["parameters"]}

    assert parameters["user_id"]["required"] is True
    assert parameters["user_id"]["schema"] == {"type": "integer", "format": "int64"}
    assert parameters["Authorization"]["required"] is True
    assert "requestBody" not in operation
    assert set(operation["responses"]) == {"200", "401", "403", "404", "422", "500"}
    assert operation["responses"]["200"]["content"]["application/json"]["schema"]
