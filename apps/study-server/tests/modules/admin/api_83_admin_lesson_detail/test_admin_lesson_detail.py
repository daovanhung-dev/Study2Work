"""HTTP tests cho Admin Lesson detail API #83."""

from __future__ import annotations

from typing import Any

import app.modules.admin.api_83_admin_lesson_detail.view as lesson_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Session giả để xác nhận API #83 chỉ đọc và rollback nhánh lỗi."""

    def __init__(self) -> None:
        """Khởi tạo bộ đếm commit/rollback của session giả."""

        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Đếm commit nếu API vô tình ghi dữ liệu."""

        self.commit_count += 1

    def rollback(self) -> None:
        """Đếm rollback khi lookup hoặc ánh xạ thất bại."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả fake session cho TestClient."""

    def dependency():
        """Cung cấp session giả cho một HTTP request."""

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


def lesson_row(**overrides: Any) -> dict[str, Any]:
    """Tạo Lesson projection theo các cột legacy `lessons` đã chọn."""

    return {
        "id": 501,
        "course_id": 42,
        "title": "Giới thiệu khóa học",
        "content": "Nội dung bài học",
        "video_url": "https://cdn.example.test/lessons/501.mp4",
        "order": 1,
        "status": "DRAFT",
        **overrides,
    }


def install_lesson_row(
    monkeypatch: pytest.MonkeyPatch,
    *,
    row: Any = ...,
) -> list[tuple[str, dict[str, int]]]:
    """Cài query double và lưu SQL/parameter của lookup detail."""

    result_row = lesson_row() if row is ... else row
    captured: list[tuple[str, dict[str, int]]] = []

    def query_one(_db, query, params):
        """Ghi nhận lookup và trả projection Lesson giả."""

        captured.append((query, dict(params)))
        if query != lesson_view.FIND_ADMIN_LESSON_DETAIL:
            raise AssertionError("unexpected lesson query")
        return result_row

    monkeypatch.setattr(lesson_view, "query_one", query_one)
    return captured


def get_lesson_response(
    client: TestClient,
    lesson_id: str,
    *,
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi GET API #83 với raw path ID và Authorization tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.get(f"/api/v1/admin/lessons/{lesson_id}", headers=headers)


def test_get_admin_lesson_returns_direct_lesson_and_preserves_optional_nulls(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả một Lesson trực tiếp, giữ field null/status và chỉ query theo khóa chính."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_lesson_row(
        monkeypatch,
        row=lesson_row(content=None, video_url=None),
    )

    response = get_lesson_response(client, "000501")

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"] == {
        "id": 501,
        "course_id": 42,
        "title": "Giới thiệu khóa học",
        "content": None,
        "video_url": None,
        "order": 1,
        "status": "DRAFT",
    }
    assert payload["meta"] == {}
    assert payload["traceId"] == response.headers["X-Trace-Id"]
    assert captured[0][1] == {"lesson_id": 501}
    assert "WHERE l.id = :lesson_id" in captured[0][0]
    assert "l.status IS DISTINCT FROM 'DELETED'" in captured[0][0]
    assert "PUBLISHED" not in captured[0][0]
    assert "resources" not in captured[0][0].lower()
    assert "lesson_progress" not in captured[0][0].lower()
    assert session.commit_count == 0
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    ("authorization", "roles", "expected_status", "expected_code"),
    [
        (None, None, 401, "DESIGN_AUTHENTICATION_REQUIRED"),
        ("Bearer valid-token", ["STUDENT"], 403, "DESIGN_ACCESS_DENIED"),
    ],
)
def test_get_admin_lesson_checks_auth_before_path_or_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
    roles: list[str] | None,
    expected_status: int,
    expected_code: str,
) -> None:
    """Thiếu token hoặc role ADMIN trả lỗi trước khi parse path hay query."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    if roles is not None:
        allow_admin_token(monkeypatch, roles=roles)

    def fail_query(*_args, **_kwargs):
        """Làm test thất bại nếu lookup chạy trước khi hoàn tất auth."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(lesson_view, "query_one", fail_query)

    response = get_lesson_response(
        client,
        "not-an-int64",
        authorization=authorization,
    )

    assert response.status_code == expected_status
    assert response.json()["businessCode"] == expected_code
    assert response.json()["data"] is None


@pytest.mark.parametrize(
    "lesson_id",
    ["not-an-id", "9223372036854775808", "-9223372036854775809", "1" * 21],
)
def test_get_admin_lesson_maps_invalid_int64_path_to_catalog_404(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    lesson_id: str,
) -> None:
    """Map malformed hoặc overflow path thành 404 mà không query database."""

    client.app.dependency_overrides[get_db] = override_db(FakeSession())
    allow_admin_token(monkeypatch)

    def fail_query(*_args, **_kwargs):
        """Làm test thất bại nếu invalid path chạm database."""

        raise AssertionError("database should not be queried")

    monkeypatch.setattr(lesson_view, "query_one", fail_query)

    response = get_lesson_response(client, lesson_id)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert response.json()["data"] is None


def test_get_admin_lesson_returns_404_when_lesson_is_missing(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map Lesson không có row thành resource not found theo catalog."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_lesson_row(monkeypatch, row=None)

    response = get_lesson_response(client, "501")

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert response.json()["data"] is None
    assert captured[0][1] == {"lesson_id": 501}
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_admin_lesson_maps_query_error_to_safe_500_and_rolls_back(
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

    monkeypatch.setattr(lesson_view, "query_one", raise_query_error)

    response = get_lesson_response(client, "501")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert "sensitive SQL detail" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0


@pytest.mark.parametrize(
    "overrides",
    [
        {"course_id": None},
        {"title": None},
        {"order": None},
        {"status": None},
        {"id": 502},
    ],
)
def test_get_admin_lesson_rejects_incomplete_or_mismatched_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    overrides: dict[str, Any],
) -> None:
    """Required field thiếu hoặc row sai identity trả 500 an toàn và rollback."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_lesson_row(monkeypatch, row=lesson_row(**overrides))

    response = get_lesson_response(client, "501")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_get_admin_lesson_openapi_declares_int64_and_catalog_errors(
    client: TestClient,
) -> None:
    """OpenAPI công bố path int64, header Bearer và đúng error set catalog."""

    operation = client.app.openapi()["paths"]["/api/v1/admin/lessons/{lesson_id}"]["get"]
    parameters = {parameter["name"]: parameter for parameter in operation["parameters"]}

    assert parameters["lesson_id"]["in"] == "path"
    assert parameters["lesson_id"]["required"] is True
    assert parameters["lesson_id"]["schema"] == {"type": "integer", "format": "int64"}
    assert parameters["Authorization"]["in"] == "header"
    assert parameters["Authorization"]["required"] is True
    assert {"200", "401", "403", "404", "500"}.issubset(operation["responses"])
    assert "422" not in operation["responses"]
