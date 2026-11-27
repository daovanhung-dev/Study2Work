"""Route-level regression tests for API #39 discussion listing."""

from __future__ import annotations

from typing import Any

import app.modules.student.api_39_discussions.view as view_module
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient


class FakeSession:
    def __init__(self) -> None:
        self.rollback_count = 0

    def rollback(self) -> None:
        self.rollback_count += 1


def override_db(session: FakeSession):
    def dependency():
        yield session

    return dependency


def discussion_row() -> dict[str, Any]:
    return {
        "id": 31,
        "course_id": 42,
        "title": "Current topic",
        "content": "A live discussion",
        "status": "ACTIVE",
        "author_id": 7,
        "author_full_name": "Learner",
        "author_avatar_url": None,
    }


def test_discussion_list_uses_student_identity_and_page_filters(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda token: {"sub": "1001", "roles": ["STUDENT"]},
    )
    query_one_calls: list[dict[str, Any]] = []
    query_many_calls: list[tuple[str, dict[str, Any]]] = []

    def query_one(db, query: str, params: dict[str, Any]):
        query_one_calls.append(params)
        return {"total": 21}

    def query_many(db, query: str, params: dict[str, Any]):
        query_many_calls.append((query, params))
        if query == view_module.LIST_ROOT_DISCUSSIONS:
            return [discussion_row()]
        if query == view_module.LIST_ACTIVE_COMMENTS:
            return []
        raise AssertionError("Unexpected API #39 query")

    monkeypatch.setattr(view_module, "query_one", query_one)
    monkeypatch.setattr(view_module, "query_many", query_many)

    response = client.get(
        "/api/v1/discussions?course_id=42&page=2",
        headers={"Authorization": "Bearer valid-token"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert query_one_calls == [{"user_id": 1001, "course_id": 42}]
    assert query_many_calls == [
        (
            view_module.LIST_ROOT_DISCUSSIONS,
            {"user_id": 1001, "course_id": 42, "limit": 20, "offset": 20},
        ),
        (view_module.LIST_ACTIVE_COMMENTS, {"discussion_id": 31}),
    ]
    assert payload["data"]["items"] == [
        {
            "id": 31,
            "course_id": 42,
            "title": "Current topic",
            "content": "A live discussion",
            "author": {"id": 7, "full_name": "Learner", "avatar_url": None},
            "status": "ACTIVE",
            "comments": [],
        }
    ]
    assert payload["data"]["pagination"] == {
        "page": 2,
        "size": 20,
        "total": 21,
        "total_pages": 2,
    }


def test_discussion_list_defaults_to_page_one_without_course_filter(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda token: {"sub": "1001", "roles": ["STUDENT"]},
    )
    query_one_calls: list[dict[str, Any]] = []

    def query_one(db, query: str, params: dict[str, Any]):
        query_one_calls.append(params)
        return {"total": 0}

    monkeypatch.setattr(view_module, "query_one", query_one)
    monkeypatch.setattr(view_module, "query_many", lambda db, query, params: [])

    response = client.get(
        "/api/v1/discussions",
        headers={"Authorization": "Bearer valid-token"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert query_one_calls == [{"user_id": 1001, "course_id": None}]
    assert payload["data"]["items"] == []
    assert payload["data"]["pagination"] == {
        "page": 1,
        "size": 20,
        "total": 0,
        "total_pages": 0,
    }


def test_discussion_list_requires_a_student_bearer_token(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(view_module, "query_one", lambda *args: pytest.fail("Unexpected query"))

    response = client.get("/api/v1/discussions")

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_discussion_list_rejects_non_student_role(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda token: {"sub": "1001", "roles": ["MENTOR"]},
    )
    monkeypatch.setattr(view_module, "query_one", lambda *args: pytest.fail("Unexpected query"))

    response = client.get(
        "/api/v1/discussions",
        headers={"Authorization": "Bearer mentor-token"},
    )

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
