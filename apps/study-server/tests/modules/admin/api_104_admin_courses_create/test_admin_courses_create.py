from __future__ import annotations

from decimal import Decimal
from typing import Any

import app.modules.admin.api_104_admin_courses_create.view as courses_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.admin.api_104_admin_courses_create.query import (
    GET_CREATED_ADMIN_COURSE,
    INSERT_ADMIN_COURSE,
    SELECT_ACTIVE_ADMIN_COURSE_MENTOR,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Session giả để xác minh transaction tạo khóa học."""

    def __init__(self, *, fail_commit: bool = False) -> None:
        self.commit_count = 0
        self.rollback_count = 0
        self.fail_commit = fail_commit

    def commit(self) -> None:
        """Đếm commit hoặc phát sinh lỗi theo cấu hình test."""

        self.commit_count += 1
        if self.fail_commit:
            raise SQLAlchemyError("private commit detail")

    def rollback(self) -> None:
        """Đếm lần rollback của transaction cần hủy."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả FakeSession cho TestClient."""

    def dependency():
        """Yield session giả trong một HTTP request."""

        yield session

    return dependency


def allow_admin_token(monkeypatch: pytest.MonkeyPatch, *, roles: list[str] | None = None) -> None:
    """Cấp token giả có role Admin cho request test."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": roles or ["ADMIN"]},
    )


def post_course(
    client: TestClient,
    *,
    body: Any | None = None,
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi HTTP POST API #104 với body hoặc Authorization có thể tùy chỉnh."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    if body is None:
        body = {
            "title": "Khóa học minh họa",
            "description": "Mô tả khóa học",
            "thumbnail_url": "https://example.test/course.png",
            "price": "250000.00",
            "mentor_id": 801,
        }
    if isinstance(body, bytes):
        return client.post("/api/v1/admin/courses", headers=headers, content=body)
    return client.post("/api/v1/admin/courses", headers=headers, json=body)


def install_create_queries(
    monkeypatch: pytest.MonkeyPatch,
    *,
    missing_mentor: bool = False,
    failing_query: str | None = None,
    bad_projection: bool = False,
) -> list[tuple[str, dict[str, Any]]]:
    """Cài query double cho kiểm tra Mentor, insert và projection Course."""

    captured: list[tuple[str, dict[str, Any]]] = []
    inserted: dict[str, Any] = {}

    def query_one(_db, query, params):
        """Trả về row phù hợp với SQL của luồng tạo khóa học."""

        captured.append((query, dict(params)))
        if query == failing_query:
            raise SQLAlchemyError("private query detail")
        if query == SELECT_ACTIVE_ADMIN_COURSE_MENTOR:
            return None if missing_mentor else {"id": params["mentor_id"]}
        if query == INSERT_ADMIN_COURSE:
            inserted.update(params)
            return {"id": 4901}
        if query == GET_CREATED_ADMIN_COURSE:
            row = {
                "id": params["course_id"],
                "title": inserted["title"],
                "description": inserted["description"],
                "thumbnail_url": inserted["thumbnail_url"],
                "price": inserted["price"],
                "status": "DRAFT",
                "mentor_id": inserted["mentor_id"],
                "mentor_full_name": "Giảng viên A",
                "mentor_avatar_url": None,
            }
            if bad_projection:
                row["status"] = "PUBLISHED"
            return row
        raise AssertionError("unexpected SQL query")

    monkeypatch.setattr(courses_view, "query_one", query_one)
    return captured


def test_create_admin_course_persists_draft_and_returns_course(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Tạo Course DRAFT, xác thực Mentor và trả projection dùng bởi API #73."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_create_queries(monkeypatch)

    response = post_course(client)

    assert response.status_code == 201
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_CREATED"
    assert payload["data"] == {
        "id": 4901,
        "title": "Khóa học minh họa",
        "description": "Mô tả khóa học",
        "thumbnail_url": "https://example.test/course.png",
        "price": "250000.00",
        "status": "DRAFT",
        "mentor": {"id": 801, "full_name": "Giảng viên A", "avatar_url": None},
    }
    assert [query for query, _ in captured] == [
        SELECT_ACTIVE_ADMIN_COURSE_MENTOR,
        INSERT_ADMIN_COURSE,
        GET_CREATED_ADMIN_COURSE,
    ]
    assert captured[0][1] == {"mentor_id": 801}
    assert captured[1][1] == {
        "mentor_id": 801,
        "title": "Khóa học minh họa",
        "description": "Mô tả khóa học",
        "thumbnail_url": "https://example.test/course.png",
        "price": Decimal("250000.00"),
    }
    assert "FOR SHARE" in SELECT_ACTIVE_ADMIN_COURSE_MENTOR
    assert "'DRAFT'" in INSERT_ADMIN_COURSE
    assert session.commit_count == 1
    assert session.rollback_count == 0
    assert response.headers["X-Trace-Id"] == payload["traceId"]


def test_create_admin_course_uses_null_for_omitted_optional_fields(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cho phép bỏ description và thumbnail_url trong body."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_create_queries(monkeypatch)

    response = post_course(client, body={"title": "Tối giản", "price": "0", "mentor_id": 801})

    assert response.status_code == 201
    assert captured[1][1]["description"] is None
    assert captured[1][1]["thumbnail_url"] is None


def test_create_admin_course_authenticates_before_parsing_body_or_querying(
    client: TestClient,
) -> None:
    """Body hỏng không được parse hoặc đưa tới database trước khi xác thực."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)

    response = post_course(client, body=b"{", authorization=None)

    assert response.status_code == 401
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_create_admin_course_rejects_invalid_fields_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối tên trống, học phí sai precision và mentor ID sai kiểu."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_create_queries(monkeypatch)

    response = post_course(
        client,
        body={"title": "  ", "price": "1.234", "mentor_id": "801"},
    )

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert captured == []
    assert session.commit_count == 0


def test_create_admin_course_rejects_missing_inactive_or_non_mentor_selection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối Mentor không thỏa role=MENTOR và status=ACTIVE trong truy vấn."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_create_queries(monkeypatch, missing_mentor=True)

    response = post_course(client)

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0]["field"] == "mentor_id"
    assert [query for query, _ in captured] == [SELECT_ACTIVE_ADMIN_COURSE_MENTOR]
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_create_admin_course_rolls_back_when_projection_or_commit_fails(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Rollback rows when response mapping fails or commit is rejected."""

    projection_session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(projection_session)
    allow_admin_token(monkeypatch)
    install_create_queries(monkeypatch, bad_projection=True)

    projection_response = post_course(client)

    assert projection_response.status_code == 500
    assert projection_session.commit_count == 0
    assert projection_session.rollback_count == 1

    commit_session = FakeSession(fail_commit=True)
    client.app.dependency_overrides[get_db] = override_db(commit_session)
    install_create_queries(monkeypatch)

    commit_response = post_course(client)

    assert commit_response.status_code == 500
    assert commit_session.commit_count == 1
    assert commit_session.rollback_count == 1

