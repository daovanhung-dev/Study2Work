from __future__ import annotations

import json
from typing import Any

import app.modules.guest.api_27_lessons_next.view as lessons_next_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.guest.api_27_lessons_next.validate import (
    validate_lesson_id,
    validate_next_lesson_request,
)
from app.modules.guest.api_27_lessons_next.view import get_next_lesson
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


def student_claims() -> dict[str, Any]:
    return {"sub": "1001", "roles": ["STUDENT"]}


def mentor_claims() -> dict[str, Any]:
    return {"sub": "2001", "roles": ["MENTOR"]}


def sample_current_lesson_row() -> dict[str, Any]:
    return {
        "id": 101,
        "course_id": 9001,
        "sort_order": 1,
        "status": "PUBLISHED",
    }


def sample_next_lesson_row() -> dict[str, Any]:
    return {
        "id": 102,
        "course_id": 9001,
        "title": "Lesson 2: Advanced Topics",
        "content": "Deep dive into topics",
        "video_url": "https://example.com/video2.mp4",
        "order": 2,
        "status": "PUBLISHED",
    }


def test_validate_lesson_id_valid() -> None:
    result = validate_lesson_id("101", trace_id="test-trace")
    assert result == 101


def test_validate_lesson_id_invalid() -> None:
    for invalid_val in ["abc", "-1", "0", str(2**63)]:
        result = validate_lesson_id(invalid_val, trace_id="test-trace")
        assert isinstance(result, JSONResponse)
        assert result.status_code == 404
        payload = json.loads(result.body.decode())
        assert payload["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_validate_next_lesson_request_auth_error() -> None:
    result = validate_next_lesson_request(
        authorization=None,
        lesson_id_raw="101",
        trace_id="test-trace",
    )
    assert isinstance(result, JSONResponse)
    assert result.status_code == 401


def test_validate_next_lesson_request_forbidden(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: mentor_claims())
    result = validate_next_lesson_request(
        authorization="Bearer mentor-token",
        lesson_id_raw="101",
        trace_id="test-trace",
    )
    assert isinstance(result, JSONResponse)
    assert result.status_code == 403


def test_get_next_lesson_current_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    session = FakeSession()
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
    monkeypatch.setattr(
        lessons_next_view,
        "find_current_lesson",
        lambda db, *, lesson_id: None,
    )

    response = get_next_lesson(
        authorization="Bearer student-token",
        lesson_id_raw="101",
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )
    assert isinstance(response, JSONResponse)
    assert response.status_code == 404
    payload = json.loads(response.body.decode())
    assert payload["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert payload["message"] == "Current lesson not found"


def test_get_next_lesson_no_next_lesson(monkeypatch: pytest.MonkeyPatch) -> None:
    session = FakeSession()
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
    monkeypatch.setattr(
        lessons_next_view,
        "find_current_lesson",
        lambda db, *, lesson_id: sample_current_lesson_row(),
    )
    monkeypatch.setattr(
        lessons_next_view,
        "find_next_lesson",
        lambda db, *, course_id, current_sort_order, current_lesson_id: None,
    )

    response = get_next_lesson(
        authorization="Bearer student-token",
        lesson_id_raw="101",
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )
    assert isinstance(response, JSONResponse)
    assert response.status_code == 404
    payload = json.loads(response.body.decode())
    assert payload["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert payload["message"] == "Next lesson not found in curriculum"


def test_get_next_lesson_db_error_current(monkeypatch: pytest.MonkeyPatch) -> None:
    session = FakeSession()
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())

    def raise_db_error(db: Any, *, lesson_id: int) -> None:
        raise SQLAlchemyError("DB error")

    monkeypatch.setattr(lessons_next_view, "find_current_lesson", raise_db_error)

    response = get_next_lesson(
        authorization="Bearer student-token",
        lesson_id_raw="101",
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )
    assert isinstance(response, JSONResponse)
    assert response.status_code == 500
    assert session.rollback_count == 1
    payload = json.loads(response.body.decode())
    assert payload["businessCode"] == "DESIGN_INTERNAL_ERROR"


def test_get_next_lesson_db_error_next(monkeypatch: pytest.MonkeyPatch) -> None:
    session = FakeSession()
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
    monkeypatch.setattr(
        lessons_next_view,
        "find_current_lesson",
        lambda db, *, lesson_id: sample_current_lesson_row(),
    )

    def raise_db_error(db: Any, *, course_id, current_sort_order, current_lesson_id) -> None:
        raise SQLAlchemyError("DB error")

    monkeypatch.setattr(lessons_next_view, "find_next_lesson", raise_db_error)

    response = get_next_lesson(
        authorization="Bearer student-token",
        lesson_id_raw="101",
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )
    assert isinstance(response, JSONResponse)
    assert response.status_code == 500
    assert session.rollback_count == 1


def test_get_next_lesson_success(monkeypatch: pytest.MonkeyPatch) -> None:
    session = FakeSession()
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
    monkeypatch.setattr(
        lessons_next_view,
        "find_current_lesson",
        lambda db, *, lesson_id: sample_current_lesson_row(),
    )
    monkeypatch.setattr(
        lessons_next_view,
        "find_next_lesson",
        lambda db, *, course_id, current_sort_order, current_lesson_id: sample_next_lesson_row(),
    )

    response = get_next_lesson(
        authorization="Bearer student-token",
        lesson_id_raw="101",
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )
    assert isinstance(response, dict)
    assert response["success"] is True
    assert response["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert response["data"]["id"] == 102
    assert response["data"]["title"] == "Lesson 2: Advanced Topics"
    assert response["data"]["order"] == 2


def test_next_lesson_route_via_client(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
    monkeypatch.setattr(
        lessons_next_view,
        "find_current_lesson",
        lambda db, *, lesson_id: sample_current_lesson_row(),
    )
    monkeypatch.setattr(
        lessons_next_view,
        "find_next_lesson",
        lambda db, *, course_id, current_sort_order, current_lesson_id: sample_next_lesson_row(),
    )

    try:
        res = client.get(
            "/api/v1/lessons/101/next",
            headers={"Authorization": "Bearer student-token"},
        )
        assert res.status_code == 200
        data = res.json()
        assert data["success"] is True
        assert data["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
        assert data["data"]["id"] == 102
        assert data["data"]["title"] == "Lesson 2: Advanced Topics"
    finally:
        client.app.dependency_overrides.clear()
