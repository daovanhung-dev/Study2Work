from __future__ import annotations

from decimal import Decimal
from typing import Any

import app.modules.admin.api_87_admin_quizzes_list.view as quizzes_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Session giả dùng để xác minh API #87 chỉ đọc và rollback lỗi."""

    def __init__(self) -> None:
        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Đếm lần commit nếu API vô tình ghi dữ liệu."""

        self.commit_count += 1

    def rollback(self) -> None:
        """Đếm rollback khi truy vấn hoặc ánh xạ lỗi."""

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


def quiz_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection Quiz candidate theo legacy quizzes table."""

    return {
        "id": 501,
        "course_id": 9001,
        "title": "Quiz minh họa",
        "duration_minutes": 30,
        "passing_score": Decimal("70.00"),
        **overrides,
    }


def install_query_rows(
    monkeypatch: pytest.MonkeyPatch,
    *,
    rows: list[dict[str, Any]] | None = None,
    total: int | None = None,
) -> list[tuple[str, dict[str, Any]]]:
    """Cài query doubles và ghi lại SQL/parameters theo thứ tự gọi."""

    result_rows = [quiz_row()] if rows is None else rows
    result_total = len(result_rows) if total is None else total
    captured: list[tuple[str, dict[str, Any]]] = []

    def query_one(_db, query, params):
        """Trả count giả và từ chối câu SQL không mong đợi."""

        captured.append((query, dict(params)))
        if query != quizzes_view.COUNT_ADMIN_QUIZZES:
            raise AssertionError("unexpected count query")
        return {"total": result_total}

    def query_many(_db, query, params):
        """Trả page giả và từ chối câu SQL không mong đợi."""

        captured.append((query, dict(params)))
        if query != quizzes_view.LIST_ADMIN_QUIZZES:
            raise AssertionError("unexpected list query")
        return result_rows

    monkeypatch.setattr(quizzes_view, "query_one", query_one)
    monkeypatch.setattr(quizzes_view, "query_many", query_many)
    return captured


def get_quizzes_response(
    client: TestClient,
    *,
    authorization: str | None = "Bearer valid-admin-token",
    params: dict[str, str] | None = None,
):
    """Gửi HTTP GET API #87 với query/header tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.get("/api/v1/admin/quizzes", headers=headers, params=params or {})


def test_get_admin_quizzes_returns_default_page_and_is_read_only(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Mặc định trả Page<Quiz>, decimal string và danh sách câu hỏi chưa hydrate."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_query_rows(monkeypatch, rows=[quiz_row()], total=21)

    response = get_quizzes_response(client)

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
            "id": 501,
            "course_id": 9001,
            "title": "Quiz minh họa",
            "duration_minutes": 30,
            "passing_score": "70.00",
            "questions": [],
        }
    ]
    assert captured[0][1] == {"course_id": None, "status": None}
    assert captured[1][1] == {
        "course_id": None,
        "status": None,
        "limit": 20,
        "offset": 0,
    }
    assert "q.status IS DISTINCT FROM 'DELETED'" in captured[0][0]
    assert "q.status IS DISTINCT FROM 'DELETED'" in captured[1][0]
    assert "ORDER BY q.id ASC" in captured[1][0]
    assert "quiz_questions" not in captured[1][0]
    assert captured[0][0].count(":course_id") == captured[1][0].count(":course_id")
    assert captured[0][0].count(":status") == captured[1][0].count(":status")
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_admin_quizzes_applies_exact_filters_and_page_offset(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Bind course/status chính xác và tính offset cho page 2."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_query_rows(monkeypatch, rows=[quiz_row(id=502)], total=30)

    response = get_quizzes_response(
        client,
        params={"course": "9001", "status": "DRAFT", "page": "2"},
    )

    assert response.status_code == 200
    assert response.json()["data"]["pagination"] == {
        "page": 2,
        "size": 20,
        "total": 30,
        "total_pages": 2,
    }
    assert captured[0][1] == {"course_id": 9001, "status": "DRAFT"}
    assert captured[1][1] == {
        "course_id": 9001,
        "status": "DRAFT",
        "limit": 20,
        "offset": 20,
    }
    assert "(:course_id IS NULL OR q.course_id = :course_id)" in captured[0][0]
    assert "(:status IS NULL OR q.status = :status)" in captured[0][0]
    assert captured[0][0].count(":course_id") == captured[1][0].count(":course_id")
    assert captured[0][0].count(":status") == captured[1][0].count(":status")
    assert session.commit_count == 0


def test_get_admin_quizzes_preserves_status_text_exactly(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Không trim hoặc đổi case status trước khi bind filter."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_query_rows(monkeypatch, rows=[], total=0)

    response = get_quizzes_response(client, params={"status": " draft "})

    assert response.status_code == 200
    assert captured[0][1]["status"] == " draft "
    assert captured[1][1]["status"] == " draft "
    assert response.json()["data"]["items"] == []


def test_get_admin_quizzes_never_returns_deleted_rows_even_for_explicit_filter(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Giữ tombstone khỏi list kể cả khi status filter yêu cầu DELETED."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_query_rows(monkeypatch, rows=[], total=0)

    response = get_quizzes_response(client, params={"status": "DELETED"})

    assert response.status_code == 200
    assert captured[0][1]["status"] == "DELETED"
    assert "q.status IS DISTINCT FROM 'DELETED'" in captured[0][0]
    assert response.json()["data"]["items"] == []


@pytest.mark.parametrize(
    ("params", "field"),
    [
        ({"course": "9223372036854775808"}, "course"),
        ({"course": "invalid"}, "course"),
        ({"page": "2147483648"}, "page"),
        ({"page": "0"}, "page"),
        ({"page": "1.5"}, "page"),
    ],
)
def test_get_admin_quizzes_rejects_invalid_numeric_query_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    params: dict[str, str],
    field: str,
) -> None:
    """Trả lỗi validation có field rõ ràng trước khi gọi DB."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Làm test thất bại nếu query chạy trước khi input được kiểm tra."""

        raise AssertionError("database must not be queried")

    monkeypatch.setattr(quizzes_view, "query_one", fail_query)
    monkeypatch.setattr(quizzes_view, "query_many", fail_query)

    response = get_quizzes_response(client, params=params)

    assert response.status_code == 422
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert payload["data"] is None
    assert payload["meta"]["fieldErrors"][0]["field"] == field
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_admin_quizzes_checks_auth_before_query_validation_or_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Authentication và role ADMIN chạy trước parse query hoặc database access."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)

    def fail_query(*_args, **_kwargs):
        """Làm test thất bại nếu unauthenticated request truy vấn database."""

        raise AssertionError("database must not be queried")

    monkeypatch.setattr(quizzes_view, "query_one", fail_query)
    monkeypatch.setattr(quizzes_view, "query_many", fail_query)

    missing_token_response = get_quizzes_response(
        client,
        authorization=None,
        params={"course": "invalid"},
    )
    assert missing_token_response.status_code == 401
    assert missing_token_response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert missing_token_response.json()["data"] is None

    allow_admin_token(monkeypatch, roles=["STUDENT"])
    wrong_role_response = get_quizzes_response(
        client,
        params={"course": "invalid"},
    )
    assert wrong_role_response.status_code == 403
    assert wrong_role_response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert wrong_role_response.json()["data"] is None
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_admin_quizzes_returns_empty_page_for_empty_or_late_page(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Empty results and page beyond total still return a valid 200 Page."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_query_rows(monkeypatch, rows=[], total=1)

    response = get_quizzes_response(client, params={"page": "4"})

    assert response.status_code == 200
    assert response.json()["data"] == {
        "items": [],
        "pagination": {"page": 4, "size": 20, "total": 1, "total_pages": 1},
    }
    assert captured[1][1]["offset"] == 60
    assert session.commit_count == 0
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    "bad_row",
    [
        {
            "id": 501,
            "course_id": None,
            "title": "Quiz",
            "duration_minutes": None,
            "passing_score": Decimal("70.00"),
        },
        {
            "id": 501,
            "course_id": 9001,
            "title": "Quiz",
            "duration_minutes": None,
            "passing_score": None,
        },
        {
            "id": 0,
            "course_id": 9001,
            "title": "Quiz",
            "duration_minutes": None,
            "passing_score": Decimal("70.00"),
        },
        quiz_row(duration_minutes=2**31),
    ],
)
def test_get_admin_quizzes_rejects_invalid_required_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    bad_row: dict[str, Any],
) -> None:
    """Required Quiz fields outside the contract shape produce safe 500 and rollback."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_query_rows(monkeypatch, rows=[bad_row], total=1)

    response = get_quizzes_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize("failing_query", ["count", "list"])
def test_get_admin_quizzes_maps_database_errors_to_safe_500(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    failing_query: str,
) -> None:
    """Database exceptions return safe DESIGN 500, rollback and never expose SQL."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)

    def fail_count(_db, _query, _params):
        """Raise a simulated SQLAlchemy failure for the count branch."""

        raise SQLAlchemyError("private quiz SQL")

    def fail_list(_db, _query, _params):
        """Raise a simulated SQLAlchemy failure for the page branch."""

        raise SQLAlchemyError("private quiz SQL")

    monkeypatch.setattr(
        quizzes_view,
        "query_one",
        fail_count if failing_query == "count" else lambda *_args, **_kwargs: {"total": 1},
    )
    monkeypatch.setattr(
        quizzes_view,
        "query_many",
        fail_list if failing_query == "list" else lambda *_args, **_kwargs: [quiz_row()],
    )

    response = get_quizzes_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert "private quiz SQL" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_admin_quizzes_rejects_invalid_count_or_page_shape(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Malformed count and unexpected page shapes return safe 500 with rollback."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    monkeypatch.setattr(quizzes_view, "query_one", lambda *_args, **_kwargs: {"total": "1"})
    monkeypatch.setattr(quizzes_view, "query_many", lambda *_args, **_kwargs: [quiz_row()])

    bad_count_response = get_quizzes_response(client)
    assert bad_count_response.status_code == 500
    assert session.rollback_count == 1

    session.rollback_count = 0
    monkeypatch.setattr(quizzes_view, "query_one", lambda *_args, **_kwargs: {"total": 1})
    monkeypatch.setattr(quizzes_view, "query_many", lambda *_args, **_kwargs: {"id": 501})

    bad_page_response = get_quizzes_response(client)
    assert bad_page_response.status_code == 500
    assert bad_page_response.json()["data"] is None
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_admin_quizzes_openapi_declares_page_filters_and_error_contract(
    client: TestClient,
) -> None:
    """OpenAPI ghi đúng query types, Page<Quiz>, no-body và local error set."""

    openapi = client.app.openapi()
    operation = openapi["paths"]["/api/v1/admin/quizzes"]["get"]
    parameters = {(item["name"], item["in"]): item for item in operation["parameters"]}

    assert set(parameters) == {
        ("course", "query"),
        ("status", "query"),
        ("page", "query"),
        ("Authorization", "header"),
    }
    assert parameters[("course", "query")]["schema"] == {
        "type": "integer",
        "format": "int64",
    }
    assert parameters[("status", "query")]["schema"] == {"type": "string"}
    assert parameters[("page", "query")]["schema"] == {
        "type": "integer",
        "format": "int32",
        "minimum": 1,
        "maximum": 2147483647,
        "default": 1,
    }
    assert parameters[("Authorization", "header")]["required"] is True
    assert "requestBody" not in operation
    assert {"200", "401", "403", "422", "500"} <= set(operation["responses"])

    envelope_schema = operation["responses"]["200"]["content"]["application/json"]["schema"]
    envelope_name = envelope_schema["$ref"].rsplit("/", 1)[-1]
    envelope = openapi["components"]["schemas"][envelope_name]
    page_schema = envelope["properties"]["data"]
    page_name = page_schema["$ref"].rsplit("/", 1)[-1]
    page = openapi["components"]["schemas"][page_name]
    item_schema = page["properties"]["items"]["items"]
    item_name = item_schema["$ref"].rsplit("/", 1)[-1]
    quiz = openapi["components"]["schemas"][item_name]
    assert {"id", "course_id", "title", "passing_score", "questions"} <= set(
        quiz["properties"]
    )


def test_get_admin_quizzes_matches_static_design_error_path(
    client: TestClient,
) -> None:
    """Static quiz route is registered for DESIGN exception business codes."""

    from app.core.middleware import DESIGN_CONTRACT_PATHS

    assert "/api/v1/admin/quizzes" in DESIGN_CONTRACT_PATHS
    assert "/api/v1/admin/quizzes" in client.app.openapi()["paths"]
