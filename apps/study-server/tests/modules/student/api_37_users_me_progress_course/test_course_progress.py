"""Route-level regression tests for API #37 course progress."""

from __future__ import annotations

from typing import Any

import app.modules.student.api_37_users_me_progress_course.view as view_module
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


def test_course_progress_uses_student_identity_and_returns_aggregate(
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
    query_calls: list[tuple[str, dict[str, Any]]] = []

    def query_one(db, query: str, params: dict[str, Any]):
        query_calls.append((query, params))
        return {"course_id": 42, "completed_lessons": 2, "total_lessons": 5}

    monkeypatch.setattr(view_module, "query_one", query_one)

    response = client.get(
        "/api/v1/users/me/progress/42",
        headers={"Authorization": "Bearer valid-token"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert query_calls == [
        (
            view_module.COURSE_LESSON_PROGRESS,
            {"course_id": 42, "user_id": 1001},
        )
    ]
    assert "e.status = 'ACTIVE'" in query_calls[0][0]
    assert payload["data"] == {
        "course_id": 42,
        "completed_lessons": 2,
        "total_lessons": 5,
        "progress_percent": 40,
        "has_content": True,
    }


def test_course_progress_requires_a_student_bearer_token(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(view_module, "query_one", lambda *args: pytest.fail("Unexpected query"))

    response = client.get("/api/v1/users/me/progress/42")

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_course_progress_rejects_non_student_role(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda token: {"sub": "2001", "roles": ["MENTOR"]},
    )
    monkeypatch.setattr(view_module, "query_one", lambda *args: pytest.fail("Unexpected query"))

    response = client.get(
        "/api/v1/users/me/progress/42",
        headers={"Authorization": "Bearer mentor-token"},
    )

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
