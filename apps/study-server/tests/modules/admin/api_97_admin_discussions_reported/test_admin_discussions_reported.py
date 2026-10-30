from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import app.modules.admin.api_97_admin_discussions_reported.view as reported_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Session giả dùng để xác minh API #97 không ghi dữ liệu."""

    def __init__(self) -> None:
        """Khởi tạo bộ đếm commit và rollback cho mỗi request test."""

        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Đếm commit nếu endpoint GET vô tình ghi dữ liệu."""

        self.commit_count += 1

    def rollback(self) -> None:
        """Đếm rollback khi query hoặc projection thất bại."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả session giả cho một request."""

    def dependency():
        """Yield session giả qua dependency database."""

        yield session

    return dependency


def allow_admin_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Thay decoder để cấp JWT có subject và role tùy chọn cho test."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": roles or ["ADMIN"]},
    )


def discussion_row(**overrides: Any) -> dict[str, Any]:
    """Tạo Discussion projection đúng các cột SQL API #97 đọc."""

    return {
        "id": 701,
        "course_id": 55,
        "content": "  Cần   xem xét\nphản ánh này. ",
        "status": "ACTIVE",
        "author_id": 8,
        "author_full_name": "Nguyễn An",
        "author_avatar_url": "https://example.test/avatar.png",
        "latest_reported_at": datetime(2026, 10, 26, 8, 30, tzinfo=UTC),
        **overrides,
    }


def install_query_results(
    monkeypatch: pytest.MonkeyPatch,
    *,
    rows: Any = None,
    count_row: Any = None,
    failure: tuple[str, SQLAlchemyError] | None = None,
) -> list[tuple[str, dict[str, Any]]]:
    """Cài query doubles và ghi nhận SQL cùng bindings theo thứ tự gọi."""

    result_rows = [discussion_row()] if rows is None else rows
    result_count = {"total": len(result_rows)} if count_row is None else count_row
    captured: list[tuple[str, dict[str, Any]]] = []

    def query_one(_db, query, params):
        """Trả count giả hoặc phát lỗi count đã cấu hình."""

        captured.append((query, dict(params)))
        if query != reported_view.COUNT_ADMIN_REPORTED_DISCUSSIONS:
            raise AssertionError("unexpected count query")
        if failure is not None and failure[0] == "count":
            raise failure[1]
        return result_count

    def query_many(_db, query, params):
        """Trả page giả hoặc phát lỗi list đã cấu hình."""

        captured.append((query, dict(params)))
        if query != reported_view.LIST_ADMIN_REPORTED_DISCUSSIONS:
            raise AssertionError("unexpected list query")
        if failure is not None and failure[0] == "list":
            raise failure[1]
        return result_rows

    monkeypatch.setattr(reported_view, "query_one", query_one)
    monkeypatch.setattr(reported_view, "query_many", query_many)
    return captured


def get_reported_response(
    client: TestClient,
    *,
    authorization: str | None = "Bearer valid-admin-token",
    params: dict[str, str] | None = None,
):
    """Gửi HTTP GET API #97 với query/header tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.get("/api/v1/admin/discussions/reported", headers=headers, params=params or {})


def test_get_admin_reported_discussions_returns_page_and_is_read_only(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả Discussion summary và pagination theo filter exact-match."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_query_results(
        monkeypatch,
        rows=[discussion_row()],
        count_row={"total": 21},
    )

    response = get_reported_response(
        client,
        params={"reason": "SPAM", "severity": "HIGH", "page": "2"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"]["pagination"] == {
        "page": 2,
        "size": 20,
        "total": 21,
        "total_pages": 2,
    }
    assert payload["data"]["items"] == [
        {
            "id": 701,
            "course_id": 55,
            "title": "Cần xem xét phản ánh này.",
            "content": "  Cần   xem xét\nphản ánh này. ",
            "author": {
                "id": 8,
                "full_name": "Nguyễn An",
                "avatar_url": "https://example.test/avatar.png",
            },
            "status": "ACTIVE",
            "comments": [],
        }
    ]
    assert captured[0][1] == {"reason": "SPAM", "severity": "HIGH"}
    assert captured[1][1] == {
        "reason": "SPAM",
        "severity": "HIGH",
        "limit": 20,
        "offset": 20,
    }
    assert "COUNT(DISTINCT d.id)" in captured[0][0]
    assert "r.status IN ('OPEN', 'IN_REVIEW')" in captured[0][0]
    assert "r.reason_code = :reason" in captured[0][0]
    assert "r.severity = :severity" in captured[0][0]
    assert "DISTINCT ON (r.discussion_id)" in captured[1][0]
    assert "ORDER BY r.created_at DESC, d.id DESC" in captured[1][0]
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_admin_reported_discussions_uses_default_page_and_empty_page(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả trang 1/20 với total_pages bằng 0 khi không có report mở."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_query_results(monkeypatch, rows=[], count_row={"total": 0})

    response = get_reported_response(client)

    assert response.status_code == 200
    payload = response.json()
    assert payload["data"] == {
        "items": [],
        "pagination": {"page": 1, "size": 20, "total": 0, "total_pages": 0},
    }
    assert payload["message"] == "No reported discussions found."
    assert captured[0][1] == {"reason": None, "severity": None}
    assert captured[1][1] == {
        "reason": None,
        "severity": None,
        "limit": 20,
        "offset": 0,
    }


@pytest.mark.parametrize("page", ["abc", "0", "-1", "2147483648", "1.5"])
def test_get_admin_reported_discussions_rejects_invalid_page_without_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    page: str,
) -> None:
    """Trả 422 cho page không dương/int32 trước khi gọi query."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_query_results(monkeypatch)

    response = get_reported_response(client, params={"page": page})

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert captured == []
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_get_admin_reported_discussions_checks_admin_before_page_parse_or_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 403 trước lỗi page và không truy cập database cho principal không Admin."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch, roles=["MENTOR"])
    captured = install_query_results(monkeypatch)

    response = get_reported_response(client, params={"page": "invalid"})

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert captured == []
    assert session.rollback_count == 0


def test_get_admin_reported_discussions_requires_authentication_before_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 401 khi thiếu Bearer token mà không chạy query."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    captured = install_query_results(monkeypatch)

    response = get_reported_response(client, authorization=None)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert captured == []
    assert session.rollback_count == 0


@pytest.mark.parametrize(
    "overrides",
    [
        {"course_id": None},
        {"author_id": None},
        {"author_full_name": None},
        {"status": None},
    ],
)
def test_get_admin_reported_discussions_rejects_incomplete_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    overrides: dict[str, Any],
) -> None:
    """Trả lỗi 500 và rollback khi Discussion thiếu field bắt buộc."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_query_results(monkeypatch, rows=[discussion_row(**overrides)])

    response = get_reported_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert session.rollback_count == 1


def test_get_admin_reported_discussions_maps_database_error_to_500(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Rollback và trả 500 khi query report source phát sinh lỗi SQLAlchemy."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_query_results(
        monkeypatch,
        failure=("count", SQLAlchemyError("database failure")),
    )

    response = get_reported_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert captured[0][0] == reported_view.COUNT_ADMIN_REPORTED_DISCUSSIONS
    assert session.rollback_count == 1


def test_get_admin_reported_discussions_maps_invalid_count_to_500(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Không trả pagination giả khi count row không thuộc kiểu hợp lệ."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_query_results(monkeypatch, rows=[], count_row={"total": "0"})

    response = get_reported_response(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.rollback_count == 1
