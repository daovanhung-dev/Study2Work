from __future__ import annotations

import json
from typing import Any

import app.modules.guest.api_09_courses_curriculum.view as curriculum_view
from app.core.database import get_db
from app.main import app
from app.modules.guest.api_09_courses_curriculum.validate import validate_course_id
from app.modules.guest.api_09_courses_curriculum.view import get_course_curriculum
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse


class FakeSession:
    def __init__(self) -> None:
        self.rollback_count = 0

    def rollback(self) -> None:
        self.rollback_count += 1


def override_db(session: FakeSession):
    def dependency():
        yield session

    return dependency


def sample_lesson_rows() -> list[dict[str, Any]]:
    return [
        {
            "id": 1,
            "course_id": 101,
            "title": "Lesson 1: Introduction",
            "content": "Overview of course",
            "video_url": "https://example.com/video1.mp4",
            "order": 1,
            "status": "PUBLISHED",
        },
        {
            "id": 2,
            "course_id": 101,
            "title": "Lesson 2: Getting Started",
            "content": None,
            "video_url": None,
            "order": 2,
            "status": "PUBLISHED",
        },
    ]


def test_validate_course_id_valid() -> None:
    result = validate_course_id("101", trace_id="test-trace")
    assert result == 101


def test_validate_course_id_invalid() -> None:
    result = validate_course_id("abc", trace_id="test-trace")
    assert isinstance(result, JSONResponse)
    assert result.status_code == 404
    payload = json.loads(result.body.decode())
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_get_course_curriculum_invalid_id() -> None:
    session = FakeSession()
    response = get_course_curriculum(
        course_id_raw="abc",
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )
    assert isinstance(response, JSONResponse)
    assert response.status_code == 404


def test_get_course_curriculum_course_not_found(monkeypatch: Any) -> None:
    session = FakeSession()
    monkeypatch.setattr(curriculum_view, "find_published_course", lambda db, *, course_id: None)

    response = get_course_curriculum(
        course_id_raw=101,
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )
    assert isinstance(response, JSONResponse)
    assert response.status_code == 404
    payload = json.loads(response.body.decode())
    assert payload["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_get_course_curriculum_db_error_on_course(monkeypatch: Any) -> None:
    session = FakeSession()

    def raise_db_error(db: Any, *, course_id: int) -> None:
        raise SQLAlchemyError("DB error")

    monkeypatch.setattr(curriculum_view, "find_published_course", raise_db_error)

    response = get_course_curriculum(
        course_id_raw=101,
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )
    assert isinstance(response, JSONResponse)
    assert response.status_code == 500
    assert session.rollback_count == 1
    payload = json.loads(response.body.decode())
    assert payload["businessCode"] == "DESIGN_INTERNAL_ERROR"


def test_get_course_curriculum_db_error_on_lessons(monkeypatch: Any) -> None:
    session = FakeSession()
    monkeypatch.setattr(
        curriculum_view,
        "find_published_course",
        lambda db, *, course_id: {"id": 101, "status": "PUBLISHED"},
    )

    def raise_db_error(db: Any, *, course_id: int) -> None:
        raise SQLAlchemyError("DB error")

    monkeypatch.setattr(curriculum_view, "find_published_lessons", raise_db_error)

    response = get_course_curriculum(
        course_id_raw=101,
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )
    assert isinstance(response, JSONResponse)
    assert response.status_code == 500
    assert session.rollback_count == 1


def test_get_course_curriculum_success(monkeypatch: Any) -> None:
    session = FakeSession()
    monkeypatch.setattr(
        curriculum_view,
        "find_published_course",
        lambda db, *, course_id: {"id": 101, "status": "PUBLISHED"},
    )
    monkeypatch.setattr(
        curriculum_view, "find_published_lessons", lambda db, *, course_id: sample_lesson_rows()
    )

    response = get_course_curriculum(
        course_id_raw=101,
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )
    assert isinstance(response, dict)
    assert response["success"] is True
    assert response["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert len(response["data"]["items"]) == 2
    assert response["data"]["pagination"]["total"] == 2
    assert response["data"]["pagination"]["total_pages"] == 1


def test_get_course_curriculum_empty_lessons(monkeypatch: Any) -> None:
    session = FakeSession()
    monkeypatch.setattr(
        curriculum_view,
        "find_published_course",
        lambda db, *, course_id: {"id": 101, "status": "PUBLISHED"},
    )
    monkeypatch.setattr(curriculum_view, "find_published_lessons", lambda db, *, course_id: [])

    response = get_course_curriculum(
        course_id_raw=101,
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )
    assert isinstance(response, dict)
    assert response["success"] is True
    assert response["message"] == "No published lessons."
    assert len(response["data"]["items"]) == 0
    assert response["data"]["pagination"]["total"] == 0
    assert response["data"]["pagination"]["total_pages"] == 0


def test_course_curriculum_route_via_client(monkeypatch: Any) -> None:
    session = FakeSession()
    monkeypatch.setattr(
        curriculum_view,
        "find_published_course",
        lambda db, *, course_id: {"id": 101, "status": "PUBLISHED"},
    )
    monkeypatch.setattr(
        curriculum_view, "find_published_lessons", lambda db, *, course_id: sample_lesson_rows()
    )

    app.dependency_overrides[get_db] = override_db(session)
    try:
        client = TestClient(app)
        res = client.get("/api/v1/courses/101/curriculum")
        assert res.status_code == 200
        data = res.json()
        assert data["success"] is True
        assert len(data["data"]["items"]) == 2
    finally:
        app.dependency_overrides.clear()
