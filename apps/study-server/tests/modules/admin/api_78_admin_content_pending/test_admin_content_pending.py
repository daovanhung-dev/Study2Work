from __future__ import annotations

from typing import Any

import app.modules.admin.api_78_admin_content_pending.view as pending_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Session giả để kiểm tra API #78 chỉ đọc và rollback lỗi."""

    def __init__(self) -> None:
        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Đếm commit nếu API vô tình sửa dữ liệu."""

        self.commit_count += 1

    def rollback(self) -> None:
        """Đếm rollback khi query hoặc projection thất bại."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả fake session cho TestClient."""

    def dependency():
        """Yield session dùng trong một HTTP request."""

        yield session

    return dependency


def allow_admin_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Thay decoder để cấp JWT Admin có subject số ổn định trong test."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": roles or ["ADMIN"]},
    )


def content_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection Content candidate theo legacy contents table."""

    return {
        "id": 901,
        "course_id": 501,
        "content_type": "QUIZ",
        "title": "Pending quiz",
        "payload": {"question_count": 4},
        "status": "PENDING_REVIEW",
        "parent_id": None,
        "order": 2,
        **overrides,
    }


def install_query_rows(
    monkeypatch: pytest.MonkeyPatch,
    *,
    rows: list[dict[str, Any]] | None = None,
    total: int | None = None,
) -> list[tuple[str, dict[str, Any]]]:
    """Cài query doubles và lưu SQL/parameters theo thứ tự gọi."""

    result_rows = [content_row()] if rows is None else rows
    result_total = len(result_rows) if total is None else total
    captured: list[tuple[str, dict[str, Any]]] = []

    def query_one(_db, query, params):
        """Trả count row giả và xác nhận SQL count đúng."""

        captured.append((query, dict(params)))
        if query != pending_view.COUNT_ADMIN_PENDING_CONTENTS:
            raise AssertionError("unexpected count query")
        return {"total": result_total}

    def query_many(_db, query, params):
        """Trả trang giả và xác nhận SQL list đúng."""

        captured.append((query, dict(params)))
        if query != pending_view.LIST_ADMIN_PENDING_CONTENTS:
            raise AssertionError("unexpected list query")
        return result_rows

    monkeypatch.setattr(pending_view, "query_one", query_one)
    monkeypatch.setattr(pending_view, "query_many", query_many)
    return captured


def get_pending_response(
    client: TestClient,
    *,
    authorization: str | None = "Bearer valid-admin-token",
    params: dict[str, str] | None = None,
):
    """Gửi HTTP GET API #78 với query/header tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.get("/api/v1/admin/content/pending", headers=headers, params=params or {})


def test_get_admin_pending_contents_returns_default_page_and_is_read_only(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Mặc định trả Page<Content>, map payload và không commit."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_query_rows(monkeypatch, rows=[content_row()], total=21)

    response = get_pending_response(client)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"]["pagination"] == {
        "page": 1,
        "size": 20,
        "total": 21,
        "total_pages": 2,
    }
    assert payload["data"]["items"] == [
        {
            "id": 901,
            "course_id": 501,
            "content_type": "QUIZ",
            "title": "Pending quiz",
            "payload": {"question_count": 4},
            "status": "PENDING_REVIEW",
            "parent_id": None,
            "order": 2,
        }
    ]
    assert captured[0][1] == {"content_type": None, "course_id": None}
    assert captured[1][1] == {
        "content_type": None,
        "course_id": None,
        "limit": 20,
        "offset": 0,
    }
    assert "status = 'PENDING_REVIEW'" in captured[0][0]
    assert "deleted_at IS NULL" in captured[0][0]
    assert "ORDER BY id ASC" in captured[1][0]
    assert captured[0][0].count(":content_type") == captured[1][0].count(":content_type")
    assert captured[0][0].count(":course_id") == captured[1][0].count(":course_id")
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_admin_pending_contents_applies_exact_filters_and_page_offset(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Count và list dùng exact type/course filters, page 2 offset 20."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)
    captured = install_query_rows(monkeypatch, rows=[content_row()], total=21)

    response = get_pending_response(
        client,
        params={"type": "QUIZ", "course": "501", "page": "2"},
    )

    assert response.status_code == 200
    assert response.json()["data"]["pagination"] == {
        "page": 2,
        "size": 20,
        "total": 21,
        "total_pages": 2,
    }
    assert captured[0][1] == {"content_type": "QUIZ", "course_id": 501}
    assert captured[1][1] == {
        "content_type": "QUIZ",
        "course_id": 501,
        "limit": 20,
        "offset": 20,
    }
    assert "content_type = :content_type" in captured[0][0]
    assert "course_id = :course_id" in captured[0][0]


@pytest.mark.parametrize(
    ("params", "total"),
    [({}, 0), ({"page": "9"}, 3)],
)
def test_get_admin_pending_contents_returns_empty_page_for_empty_or_late_page(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    params: dict[str, str],
    total: int,
) -> None:
    """Queue rỗng hoặc trang vượt cuối đều trả HTTP 200 với items rỗng."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)
    install_query_rows(monkeypatch, rows=[], total=total)

    response = get_pending_response(client, params=params)

    assert response.status_code == 200
    page = response.json()["data"]
    assert page["items"] == []
    assert page["pagination"]["total"] == total
    assert page["pagination"]["total_pages"] == (1 if total else 0)


@pytest.mark.parametrize(
    ("params", "field"),
    [
        ({"course": "x"}, "course"),
        ({"course": "9223372036854775808"}, "course"),
        ({"course": "-9223372036854775809"}, "course"),
        ({"page": "x"}, "page"),
        ({"page": "0"}, "page"),
        ({"page": "2147483648"}, "page"),
    ],
)
def test_get_admin_pending_contents_rejects_invalid_numeric_query_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    params: dict[str, str],
    field: str,
) -> None:
    """Query sai signed-int64/int32 trả derived 422 trước khi gọi database."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Báo lỗi nếu validator cho phép query sai đi tới database."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(pending_view, "query_one", fail_query)
    monkeypatch.setattr(pending_view, "query_many", fail_query)

    response = get_pending_response(client, params=params)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0]["field"] == field


@pytest.mark.parametrize(
    ("authorization", "roles", "expected_status", "expected_code"),
    [
        (None, None, 401, "DESIGN_AUTHENTICATION_REQUIRED"),
        ("Bearer valid-token", ["STUDENT"], 403, "DESIGN_ACCESS_DENIED"),
    ],
)
def test_get_admin_pending_contents_checks_auth_before_query_validation_or_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
    roles: list[str] | None,
    expected_status: int,
    expected_code: str,
) -> None:
    """Auth precedes invalid query parsing and all queue reads."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    if roles is not None:
        allow_admin_token(monkeypatch, roles=roles)

    def fail_query(*_args, **_kwargs):
        """Báo lỗi nếu request trái quyền chạm database."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(pending_view, "query_one", fail_query)
    monkeypatch.setattr(pending_view, "query_many", fail_query)

    response = get_pending_response(
        client,
        authorization=authorization,
        params={"page": "invalid"},
    )

    assert response.status_code == expected_status
    assert response.json()["businessCode"] == expected_code


@pytest.mark.parametrize(
    ("count_row", "rows", "params"),
    [
        (None, [], {}),
        ({}, [], {}),
        ({"total": -1}, [], {}),
        ({"total": "2"}, [], {}),
        ({"total": 1}, [{"id": 901}], {}),
        ({"total": 1}, [content_row(payload=["not", "object"])], {}),
        ({"total": 1}, [content_row(status="PUBLISHED")], {}),
        ({"total": 1}, [content_row(content_type="LESSON")], {"type": "QUIZ"}),
    ],
)
def test_get_admin_pending_contents_rejects_invalid_count_or_content_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    count_row: dict[str, Any] | None,
    rows: list[dict[str, Any]],
    params: dict[str, str],
) -> None:
    """Count hoặc Content projection không hợp lệ trả safe 500 và rollback."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    monkeypatch.setattr(pending_view, "query_one", lambda *_args, **_kwargs: count_row)
    monkeypatch.setattr(pending_view, "query_many", lambda *_args, **_kwargs: rows)

    response = get_pending_response(client, params=params)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize("failing_query", ["count", "list"])
def test_get_admin_pending_contents_maps_database_errors_to_safe_500(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    failing_query: str,
) -> None:
    """SQLAlchemy failure from either query rolls back and hides database detail."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Phát sinh lỗi query giả có thông tin nhạy cảm."""

        raise SQLAlchemyError("sensitive pending content SQL")

    monkeypatch.setattr(
        pending_view,
        "query_one",
        fail_query if failing_query == "count" else lambda *_args, **_kwargs: {"total": 0},
    )
    monkeypatch.setattr(
        pending_view,
        "query_many",
        fail_query if failing_query == "list" else lambda *_args, **_kwargs: [],
    )

    response = get_pending_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "sensitive pending content SQL" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_admin_pending_contents_openapi_declares_page_content_and_errors(
    client: TestClient,
) -> None:
    """OpenAPI ghi query int64/int32, derived Page<Content> và status errors."""

    openapi = client.app.openapi()
    operation = openapi["paths"]["/api/v1/admin/content/pending"]["get"]
    parameters = {item["name"]: item for item in operation["parameters"]}

    assert set(parameters) == {"type", "course", "page", "Authorization"}
    assert parameters["Authorization"]["required"] is True
    assert parameters["type"]["schema"] == {"type": "string"}
    assert parameters["course"]["schema"] == {"type": "integer", "format": "int64"}
    assert parameters["page"]["schema"] == {
        "type": "integer",
        "format": "int32",
        "minimum": 1,
        "maximum": 2147483647,
        "default": 1,
    }
    assert {"200", "401", "403", "422", "500"} <= set(operation["responses"])
    assert "404" not in operation["responses"]

    envelope_schema = operation["responses"]["200"]["content"]["application/json"]["schema"]
    envelope_name = envelope_schema["$ref"].rsplit("/", 1)[-1]
    envelope = openapi["components"]["schemas"][envelope_name]
    page_schema = envelope["properties"]["data"]
    page_name = page_schema["$ref"].rsplit("/", 1)[-1]
    page = openapi["components"]["schemas"][page_name]
    content_schema = page["properties"]["items"]["items"]
    content_name = content_schema["$ref"].rsplit("/", 1)[-1]
    content = openapi["components"]["schemas"][content_name]
    assert {"id", "course_id", "content_type", "title", "payload", "status", "order"} <= set(
        content["properties"]
    )
    assert "requestBody" not in operation
