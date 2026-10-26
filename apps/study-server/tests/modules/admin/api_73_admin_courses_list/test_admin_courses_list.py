from __future__ import annotations

from decimal import Decimal
from typing import Any

import app.modules.admin.api_73_admin_courses_list.view as courses_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Session giả để kiểm tra transaction chỉ đọc API #73."""

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
    """Thay decoder để cấp JWT Admin có subject số ổn định trong test."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": roles or ["ADMIN"]},
    )


def course_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection candidate theo legacy courses/users."""

    return {
        "id": 11,
        "title": "Linear Algebra",
        "description": "Vectors and matrices",
        "thumbnail_url": "https://example.test/course.png",
        "price": Decimal("125.50"),
        "status": "DRAFT",
        "mentor_id": 501,
        "mentor_full_name": "Ada Lovelace",
        "mentor_avatar_url": None,
        **overrides,
    }


def install_query_rows(
    monkeypatch: pytest.MonkeyPatch,
    *,
    rows: list[dict[str, Any]] | None = None,
    total: int | None = None,
    missing_mentor_count: int = 0,
) -> list[tuple[str, dict[str, Any]]]:
    """Cài query doubles và lưu SQL/parameters theo thứ tự gọi."""

    result_rows = [course_row()] if rows is None else rows
    result_total = len(result_rows) if total is None else total
    captured: list[tuple[str, dict[str, Any]]] = []

    def query_one(_db, query, params):
        captured.append((query, dict(params)))
        if query != courses_view.COUNT_ADMIN_COURSES:
            raise AssertionError("unexpected count query")
        return {"total": result_total, "missing_mentor_count": missing_mentor_count}

    def query_many(_db, query, params):
        captured.append((query, dict(params)))
        if query != courses_view.LIST_ADMIN_COURSES:
            raise AssertionError("unexpected list query")
        return result_rows

    monkeypatch.setattr(courses_view, "query_one", query_one)
    monkeypatch.setattr(courses_view, "query_many", query_many)
    return captured


def get_courses_response(
    client: TestClient,
    *,
    authorization: str | None = "Bearer valid-admin-token",
    params: dict[str, str] | None = None,
):
    """Gửi HTTP GET API #73 với query/header tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.get("/api/v1/admin/courses", headers=headers, params=params or {})


def test_get_admin_courses_returns_default_page_and_uses_read_only_queries(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả Page<Course>, decimal price dạng chuỗi và count/list params mặc định."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_query_rows(monkeypatch, rows=[course_row()], total=21)

    response = get_courses_response(client)

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"]["pagination"] == {
        "page": 1,
        "size": 20,
        "total": 21,
        "total_pages": 2,
    }
    assert payload["data"]["items"][0]["price"] == "125.50"
    assert payload["data"]["items"][0]["mentor"] == {
        "id": 501,
        "full_name": "Ada Lovelace",
        "avatar_url": None,
    }
    assert captured[0][1] == {"status": None, "mentor": None}
    assert captured[1][1] == {
        "status": None,
        "mentor": None,
        "limit": 20,
        "offset": 0,
    }
    assert "ORDER BY c.id ASC" in captured[1][0]
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_admin_courses_applies_exact_status_and_mentor_filters(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Count và list cùng bind exact filters, page 2 dùng offset 20."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)
    captured = install_query_rows(monkeypatch, rows=[course_row()], total=21)

    response = get_courses_response(
        client,
        params={"status": "SUSPENDED", "mentor": "501", "page": "2"},
    )

    assert response.status_code == 200
    assert response.json()["data"]["pagination"] == {
        "page": 2,
        "size": 20,
        "total": 21,
        "total_pages": 2,
    }
    assert captured[0][1] == {"status": "SUSPENDED", "mentor": 501}
    assert captured[1][1] == {
        "status": "SUSPENDED",
        "mentor": 501,
        "limit": 20,
        "offset": 20,
    }
    assert "(:status IS NULL OR c.status = :status)" in captured[0][0]
    assert "(:mentor IS NULL OR c.mentor_id = :mentor)" in captured[0][0]
    assert captured[0][0].count(":status") == captured[1][0].count(":status")
    assert captured[0][0].count(":mentor") == captured[1][0].count(":mentor")


@pytest.mark.parametrize(
    ("params", "expected_data"),
    [
        (
            {"status": "UNKNOWN"},
            {"items": [], "pagination": {"page": 1, "size": 20, "total": 0, "total_pages": 0}},
        ),
        (
            {"page": "9"},
            {"items": [], "pagination": {"page": 9, "size": 20, "total": 3, "total_pages": 1}},
        ),
    ],
)
def test_get_admin_courses_returns_empty_page_for_no_match_or_out_of_range_page(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    params: dict[str, str],
    expected_data: dict[str, Any],
) -> None:
    """Empty results and pages beyond the last page remain HTTP 200."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)
    total = 3 if params.get("page") == "9" else 0
    install_query_rows(monkeypatch, rows=[], total=total)

    response = get_courses_response(client, params=params)

    assert response.status_code == 200
    assert response.json()["data"] == expected_data


def test_get_admin_courses_rejects_category_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Không giả lập quan hệ category; trả fallback 422 trước query."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        raise AssertionError("database should not be queried")

    monkeypatch.setattr(courses_view, "query_one", fail_query)
    monkeypatch.setattr(courses_view, "query_many", fail_query)

    response = get_courses_response(client, params={"category": "17"})

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["message"] == "Bộ lọc category chưa được hỗ trợ."


@pytest.mark.parametrize(
    ("params", "field"),
    [
        ({"mentor": "x"}, "mentor"),
        ({"mentor": "9223372036854775808"}, "mentor"),
        ({"category": "x"}, "category"),
        ({"category": "-9223372036854775809"}, "category"),
        ({"page": "x"}, "page"),
        ({"page": "0"}, "page"),
        ({"page": "2147483648"}, "page"),
    ],
)
def test_get_admin_courses_rejects_invalid_query_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    params: dict[str, str],
    field: str,
) -> None:
    """Sai kiểu hoặc ngoài miền int64/int32 trả field error và không truy vấn DB."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        raise AssertionError("database should not be queried")

    monkeypatch.setattr(courses_view, "query_one", fail_query)
    monkeypatch.setattr(courses_view, "query_many", fail_query)

    response = get_courses_response(client, params=params)

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
def test_get_admin_courses_rejects_auth_before_database_and_query_validation(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
    roles: list[str] | None,
    expected_status: int,
    expected_code: str,
) -> None:
    """Auth được kiểm tra trước query, kể cả khi tham số phía sau không hợp lệ."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    if roles is not None:
        allow_admin_token(monkeypatch, roles=roles)

    def fail_query(*_args, **_kwargs):
        raise AssertionError("database should not be queried")

    monkeypatch.setattr(courses_view, "query_one", fail_query)
    monkeypatch.setattr(courses_view, "query_many", fail_query)

    response = get_courses_response(
        client,
        authorization=authorization,
        params={"page": "invalid"},
    )

    assert response.status_code == expected_status
    assert response.json()["businessCode"] == expected_code


@pytest.mark.parametrize(
    ("count_row", "rows"),
    [
        (None, []),
        ({"total": -1, "missing_mentor_count": 0}, []),
        ({"total": None, "missing_mentor_count": 0}, []),
        ({"total": 1, "missing_mentor_count": None}, []),
        ({"total": 1}, []),
        ({"total": 1, "missing_mentor_count": 1}, []),
        ({"total": 1, "missing_mentor_count": 0}, [{"id": 11}]),
    ],
)
def test_get_admin_courses_rejects_invalid_count_or_course_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    count_row: dict[str, Any] | None,
    rows: list[dict[str, Any]],
) -> None:
    """Count integrity/orphan mentor/course mapping failures return safe 500 and rollback."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    monkeypatch.setattr(courses_view, "query_one", lambda *_args, **_kwargs: count_row)
    monkeypatch.setattr(courses_view, "query_many", lambda *_args, **_kwargs: rows)

    response = get_courses_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_admin_courses_maps_database_error_to_safe_500_and_rolls_back(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """DB exception không lộ SQL và dọn transaction đọc."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)

    def raise_query_error(*_args, **_kwargs):
        raise SQLAlchemyError("sensitive SQL detail")

    monkeypatch.setattr(courses_view, "query_one", raise_query_error)

    response = get_courses_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "sensitive SQL detail" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_admin_courses_maps_course_mapper_exception_to_safe_500(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Unexpected row conversion errors are contained and roll back the read transaction."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_query_rows(monkeypatch, rows=[course_row()])

    def raise_mapping_error(_row):
        raise ValueError("invalid projection")

    monkeypatch.setattr(courses_view, "map_course", raise_mapping_error)

    response = get_courses_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "invalid projection" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_admin_courses_openapi_declares_query_page_course_and_errors(
    client: TestClient,
) -> None:
    """OpenAPI phản ánh raw filters, signed ID formats, Page<Course> và status set."""

    openapi = client.app.openapi()
    operation = openapi["paths"]["/api/v1/admin/courses"]["get"]
    parameters = {item["name"]: item for item in operation["parameters"]}

    assert set(parameters) == {"status", "mentor", "category", "page", "Authorization"}
    assert parameters["Authorization"]["required"] is True
    assert parameters["mentor"]["schema"] == {"type": "integer", "format": "int64"}
    assert parameters["category"]["schema"] == {"type": "integer", "format": "int64"}
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
    envelope = openapi["components"]["schemas"][envelope_name]
    page_ref = envelope["properties"]["data"]["$ref"]
    page = openapi["components"]["schemas"][page_ref.rsplit("/", 1)[-1]]
    course_ref = page["properties"]["items"]["items"]["$ref"]
    course = openapi["components"]["schemas"][course_ref.rsplit("/", 1)[-1]]
    assert {"id", "title", "price", "status", "mentor"} <= set(course["properties"])
