from __future__ import annotations

from decimal import Decimal
from typing import Any

import app.modules.admin.api_74_admin_course_detail.view as course_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Session giả để kiểm tra transaction chỉ đọc API #74."""

    def __init__(self) -> None:
        """Khởi tạo bộ đếm commit/rollback của session giả."""

        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Đếm commit nếu view vô tình ghi dữ liệu."""

        self.commit_count += 1

    def rollback(self) -> None:
        """Đếm rollback của nhánh lỗi hoặc không tìm thấy resource."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả session giả cho TestClient."""

    def dependency():
        """Yield session test cho dependency get_db."""

        yield session

    return dependency


def allow_admin_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Cài decoder giả trả JWT Admin hoặc role được chỉ định."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": roles or ["ADMIN"]},
    )


def course_row(**overrides: Any) -> dict[str, Any]:
    """Tạo projection Course/mentor candidate theo legacy courses/users."""

    return {
        "id": 11,
        "title": "Linear Algebra",
        "description": None,
        "thumbnail_url": None,
        "price": Decimal("125.50"),
        "status": "SUSPENDED",
        "mentor_id": 501,
        "mentor_full_name": "Ada Lovelace",
        "mentor_avatar_url": None,
        **overrides,
    }


def install_course_row(
    monkeypatch: pytest.MonkeyPatch,
    *,
    row: dict[str, Any] | None = None,
) -> list[tuple[str, dict[str, int]]]:
    """Cài query double và lưu SQL/parameter của lookup detail."""

    result_row = course_row() if row is None else row
    captured: list[tuple[str, dict[str, int]]] = []

    def query_one(_db, query, params):
        """Ghi nhận lookup và trả projection Course giả."""

        captured.append((query, dict(params)))
        return result_row

    monkeypatch.setattr(course_view, "query_one", query_one)
    return captured


def get_course_response(
    client: TestClient,
    course_id: str,
    *,
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi GET API #74 với raw path ID và Authorization tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.get(f"/api/v1/admin/courses/{course_id}", headers=headers)


def test_get_admin_course_returns_singleton_page_and_preserves_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả CoursePage singleton, giữ null/decimal/status và không query counters."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_course_row(monkeypatch)

    response = get_course_response(client, "11")

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"]["pagination"] == {
        "page": 1,
        "size": 1,
        "total": 1,
        "total_pages": 1,
    }
    assert payload["data"]["items"] == [
        {
            "id": 11,
            "title": "Linear Algebra",
            "description": None,
            "thumbnail_url": None,
            "price": "125.50",
            "status": "SUSPENDED",
            "mentor": {
                "id": 501,
                "full_name": "Ada Lovelace",
                "avatar_url": None,
            },
        }
    ]
    assert "category" not in payload["data"]["items"][0]
    assert "counters" not in payload["data"]
    assert payload["meta"] == {}
    assert captured[0][1] == {"course_id": 11}
    assert "WHERE c.id = :course_id" in captured[0][0]
    assert "AND c.status" not in captured[0][0]
    assert "category" not in captured[0][0].lower()
    assert "enrollments" not in captured[0][0].lower()
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
def test_get_admin_course_checks_auth_before_path_and_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
    roles: list[str] | None,
    expected_status: int,
    expected_code: str,
) -> None:
    """Trả lỗi auth trước parse path hoặc query khi caller chưa có role ADMIN."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    if roles is not None:
        allow_admin_token(monkeypatch, roles=roles)

    def fail_query(*_args, **_kwargs):
        """Làm test thất bại nếu lookup chạy trước khi hoàn thành auth."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(course_view, "query_one", fail_query)

    response = get_course_response(client, "not-an-int64", authorization=authorization)

    assert response.status_code == expected_status
    assert response.json()["businessCode"] == expected_code
    assert response.json()["data"] is None


@pytest.mark.parametrize(
    "course_id",
    ["not-an-id", "9223372036854775808", "-9223372036854775809", "1" * 21],
)
def test_get_admin_course_maps_invalid_int64_path_to_catalog_404(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    course_id: str,
) -> None:
    """Map malformed hoặc overflow path thành 404 mà không query database."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Làm test thất bại nếu invalid path chạm database."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(course_view, "query_one", fail_query)

    response = get_course_response(client, course_id)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert response.json()["data"] is None


def test_get_admin_course_accepts_signed_int64_then_returns_not_found_for_missing_row(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Giữ nguyên signed-int64 path contract và bind ID âm an toàn."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured: list[tuple[str, dict[str, int]]] = []

    def query_one(_db, query, params):
        """Ghi nhận ID âm hợp lệ về kiểu rồi mô phỏng course không tồn tại."""

        captured.append((query, dict(params)))
        return None

    monkeypatch.setattr(course_view, "query_one", query_one)

    response = get_course_response(client, "-1")

    assert response.status_code == 404
    assert captured[0][1] == {"course_id": -1}
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_admin_course_returns_404_when_course_is_missing(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map course không có row thành resource not found theo catalog."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    monkeypatch.setattr(course_view, "query_one", lambda *_args, **_kwargs: None)

    response = get_course_response(client, "11")

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert response.json()["data"] is None
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_admin_course_maps_query_error_to_safe_500_and_rolls_back(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """DB exception trả lỗi an toàn và rollback transaction đọc."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)

    def raise_query_error(*_args, **_kwargs):
        """Tạo lỗi SQL giả để kiểm tra status và thông điệp an toàn."""

        raise SQLAlchemyError("sensitive SQL detail")

    monkeypatch.setattr(course_view, "query_one", raise_query_error)

    response = get_course_response(client, "11")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert "sensitive SQL detail" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize(
    "overrides",
    [
        {"mentor_id": None},
        {"mentor_full_name": None},
        {"price": None},
        {"id": 12},
    ],
)
def test_get_admin_course_rejects_incomplete_or_mismatched_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    overrides: dict[str, Any],
) -> None:
    """Thiếu mentor/price hoặc sai identity row trả 500 an toàn."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_course_row(monkeypatch, row=course_row(**overrides))

    response = get_course_response(client, "11")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_admin_course_openapi_declares_int64_and_catalog_errors(client: TestClient) -> None:
    """OpenAPI công bố path int64, header Bearer và đúng error set catalog."""

    operation = client.app.openapi()["paths"]["/api/v1/admin/courses/{course_id}"]["get"]
    parameters = {parameter["name"]: parameter for parameter in operation["parameters"]}

    assert parameters["course_id"]["in"] == "path"
    assert parameters["course_id"]["required"] is True
    assert parameters["course_id"]["schema"] == {"type": "integer", "format": "int64"}
    assert parameters["Authorization"]["in"] == "header"
    assert parameters["Authorization"]["required"] is True
    assert {"200", "401", "403", "404", "500"}.issubset(operation["responses"])
    assert "422" not in operation["responses"]
