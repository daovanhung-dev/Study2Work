from __future__ import annotations

from datetime import datetime
from typing import Any

import app.modules.admin.api_68_admin_users_list.view as users_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Session giả lập để kiểm tra transaction chỉ đọc của API #68."""

    def __init__(self) -> None:
        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        self.commit_count += 1

    def rollback(self) -> None:
        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả fake session cho TestClient."""

    def dependency():
        yield session

    return dependency


def allow_admin_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Thay decoder để tạo JWT Admin có subject số ổn định trong test."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": roles or ["ADMIN"]},
    )


def user_row(**overrides: Any) -> dict[str, Any]:
    """Tạo profile projection candidate từ legacy users."""

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


def install_query_rows(
    monkeypatch: pytest.MonkeyPatch,
    *,
    rows: list[dict[str, Any]] | None = None,
    total: int | None = None,
) -> list[tuple[str, dict[str, Any]]]:
    """Cài query doubles và lưu SQL/parameters theo đúng thứ tự gọi."""

    result_rows = [user_row()] if rows is None else rows
    result_total = len(result_rows) if total is None else total
    captured: list[tuple[str, dict[str, Any]]] = []

    def query_one(_db, query, params):
        captured.append((query, dict(params)))
        if query != users_view.COUNT_ADMIN_USERS:
            raise AssertionError("unexpected count query")
        return {"total": result_total}

    def query_many(_db, query, params):
        captured.append((query, dict(params)))
        if query != users_view.LIST_ADMIN_USERS:
            raise AssertionError("unexpected list query")
        return result_rows

    monkeypatch.setattr(users_view, "query_one", query_one)
    monkeypatch.setattr(users_view, "query_many", query_many)
    return captured


def get_users_response(
    client: TestClient,
    *,
    authorization: str | None = "Bearer valid-admin-token",
    params: dict[str, str] | None = None,
):
    """Gửi HTTP GET API #68 với query/header tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.get("/api/v1/admin/users", headers=headers, params=params or {})


def test_get_admin_users_returns_page_profile_and_excludes_credentials(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả Page<UserProfile> mặc định, nullable fields và không lộ credential."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_query_rows(
        monkeypatch,
        rows=[user_row(password_hash="must-not-leak")],
        total=21,
    )

    response = get_users_response(client)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"]["pagination"] == {
        "page": 1,
        "size": 20,
        "total": 21,
        "total_pages": 2,
    }
    assert payload["data"]["items"][0]["id"] == 1001
    assert payload["data"]["items"][0]["avatar_url"] is None
    assert payload["data"]["items"][0]["phone"] is None
    assert "password_hash" not in payload["data"]["items"][0]
    assert "bio" not in payload["data"]["items"][0]
    assert "password_hash" not in users_view.LIST_ADMIN_USERS
    assert captured[0][1] == {"role": None, "status": None, "keyword": None}
    assert captured[1][1] == {
        "role": None,
        "status": None,
        "keyword": None,
        "limit": 20,
        "offset": 0,
    }
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_admin_users_applies_exact_filters_and_literal_keyword(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Count/list share role/status filters and normalized literal substring."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_query_rows(monkeypatch, rows=[user_row()], total=21)

    response = get_users_response(
        client,
        params={
            "role": "MENTOR",
            "status": "SUSPENDED",
            "keyword": "  ADA%_  ",
            "page": "2",
        },
    )

    assert response.status_code == 200
    assert response.json()["data"]["pagination"] == {
        "page": 2,
        "size": 20,
        "total": 21,
        "total_pages": 2,
    }
    assert captured[0][1] == {
        "role": "MENTOR",
        "status": "SUSPENDED",
        "keyword": "ada%_",
    }
    assert captured[1][1] == {
        "role": "MENTOR",
        "status": "SUSPENDED",
        "keyword": "ada%_",
        "limit": 20,
        "offset": 20,
    }
    assert "POSITION(:keyword IN LOWER(u.full_name))" in captured[0][0]
    assert "POSITION(:keyword IN LOWER(u.email))" in captured[0][0]


def test_get_admin_users_returns_empty_page_when_no_rows_match(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Biểu diễn no-match bằng page rỗng HTTP 200."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)
    install_query_rows(monkeypatch, rows=[], total=0)

    response = get_users_response(client, params={"role": "UNKNOWN"})

    assert response.status_code == 200
    assert response.json()["data"] == {
        "items": [],
        "pagination": {"page": 1, "size": 20, "total": 0, "total_pages": 0},
    }


@pytest.mark.parametrize(
    ("authorization", "roles", "expected_status", "expected_code"),
    [
        (None, None, 401, "DESIGN_AUTHENTICATION_REQUIRED"),
        ("Bearer valid-token", ["STUDENT"], 403, "DESIGN_ACCESS_DENIED"),
    ],
)
def test_get_admin_users_rejects_missing_or_non_admin_auth_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
    roles: list[str] | None,
    expected_status: int,
    expected_code: str,
) -> None:
    """Trả 401/403 trước khi chạy count hoặc list query."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    if roles is not None:
        allow_admin_token(monkeypatch, roles=roles)

    def fail_query(*_args, **_kwargs):
        raise AssertionError("database should not be queried")

    monkeypatch.setattr(users_view, "query_one", fail_query)
    monkeypatch.setattr(users_view, "query_many", fail_query)

    response = get_users_response(client, authorization=authorization)

    assert response.status_code == expected_status
    assert response.json()["businessCode"] == expected_code


@pytest.mark.parametrize("page", ["invalid", "0", "-1", "2147483648"])
def test_get_admin_users_rejects_invalid_page_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    page: str,
) -> None:
    """Trả 422 DESIGN_VALIDATION_ERROR cho page không hợp lệ sau auth."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        raise AssertionError("database should not be queried")

    monkeypatch.setattr(users_view, "query_one", fail_query)
    monkeypatch.setattr(users_view, "query_many", fail_query)

    response = get_users_response(client, params={"page": page})

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0]["field"] == "page"


def test_get_admin_users_maps_sql_error_to_safe_500_and_rolls_back(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """DB exception không lộ chi tiết và dọn read transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)

    def raise_query_error(*_args, **_kwargs):
        raise SQLAlchemyError("sensitive SQL detail")

    monkeypatch.setattr(users_view, "query_one", raise_query_error)

    response = get_users_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "sensitive SQL detail" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize(
    ("count_row", "rows"),
    [
        (None, []),
        ({"total": -1}, []),
        ({"total": 1}, [{"id": 1001, "email": "missing-required-fields"}]),
        ({"total": 1}, [user_row(id=True)]),
    ],
)
def test_get_admin_users_rejects_invalid_count_or_profile_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    count_row: dict[str, Any] | None,
    rows: list[dict[str, Any]],
) -> None:
    """Projection/count lỗi trả 500 an toàn và rollback transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)

    monkeypatch.setattr(users_view, "query_one", lambda *_args, **_kwargs: count_row)
    monkeypatch.setattr(users_view, "query_many", lambda *_args, **_kwargs: rows)

    response = get_users_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_admin_users_openapi_declares_admin_page_and_exact_error_set(
    client: TestClient,
) -> None:
    """OpenAPI mô tả query int32, required Bearer header và Page<UserProfile>."""

    operation = client.app.openapi()["paths"]["/api/v1/admin/users"]["get"]
    parameters = {item["name"]: item for item in operation["parameters"]}

    assert set(parameters) == {"role", "status", "keyword", "page", "Authorization"}
    assert parameters["Authorization"]["required"] is True
    assert parameters["page"]["schema"] == {
        "type": "integer",
        "format": "int32",
        "minimum": 1,
        "maximum": 2147483647,
        "default": 1,
    }
    assert {"200", "401", "403", "422", "500"} <= set(operation["responses"])
    assert "404" not in operation["responses"]

    schema = operation["responses"]["200"]["content"]["application/json"]["schema"]
    envelope_name = schema["$ref"].rsplit("/", 1)[-1]
    envelope = client.app.openapi()["components"]["schemas"][envelope_name]
    page_ref = envelope["properties"]["data"]["$ref"]
    page_name = page_ref.rsplit("/", 1)[-1]
    page_schema = client.app.openapi()["components"]["schemas"][page_name]
    profile_ref = page_schema["properties"]["items"]["items"]["$ref"]
    profile_name = profile_ref.rsplit("/", 1)[-1]
    profile_schema = client.app.openapi()["components"]["schemas"][profile_name]
    assert "password_hash" not in profile_schema["properties"]
    assert "bio" not in profile_schema["properties"]
