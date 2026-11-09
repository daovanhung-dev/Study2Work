from __future__ import annotations

import json
from typing import Any

import app.modules.guest.api_26_lessons_resources.view as lessons_resources_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.guest.api_26_lessons_resources.validate import (
    validate_lesson_id,
    validate_lesson_resources_request,
)
from app.modules.guest.api_26_lessons_resources.view import get_lesson_resources
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


def sample_lesson_row() -> dict[str, Any]:
    return {
        "id": 101,
        "course_id": 9001,
        "title": "Introduction to Python",
        "content": "Lesson content here",
        "video_url": "https://example.com/video.mp4",
        "order": 1,
        "status": "PUBLISHED",
    }


def sample_resource_rows() -> list[dict[str, Any]]:
    return [
        {
            "id": 1,
            "lesson_id": 101,
            "name": "Slides PDF",
            "type": "DOCUMENT",
            "url": "https://example.com/slides.pdf",
        },
        {
            "id": 2,
            "lesson_id": 101,
            "name": "Source Code ZIP",
            "type": "ARCHIVE",
            "url": "https://example.com/code.zip",
        },
    ]


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


def test_validate_lesson_resources_request_auth_error() -> None:
    result = validate_lesson_resources_request(
        authorization=None,
        lesson_id_raw="101",
        trace_id="test-trace",
    )
    assert isinstance(result, JSONResponse)
    assert result.status_code == 401


def test_validate_lesson_resources_request_forbidden(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: mentor_claims())
    result = validate_lesson_resources_request(
        authorization="Bearer mentor-token",
        lesson_id_raw="101",
        trace_id="test-trace",
    )
    assert isinstance(result, JSONResponse)
    assert result.status_code == 403


def test_get_lesson_resources_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    session = FakeSession()
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
    monkeypatch.setattr(
        lessons_resources_view,
        "find_published_lesson",
        lambda db, *, lesson_id: None,
    )

    response = get_lesson_resources(
        authorization="Bearer student-token",
        lesson_id_raw="101",
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )
    assert isinstance(response, JSONResponse)
    assert response.status_code == 404
    payload = json.loads(response.body.decode())
    assert payload["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_get_lesson_resources_db_error(monkeypatch: pytest.MonkeyPatch) -> None:
    session = FakeSession()
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())

    def raise_db_error(db: Any, *, lesson_id: int) -> None:
        raise SQLAlchemyError("DB error")

    monkeypatch.setattr(lessons_resources_view, "find_published_lesson", raise_db_error)

    response = get_lesson_resources(
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


def test_get_lesson_resources_success(monkeypatch: pytest.MonkeyPatch) -> None:
    session = FakeSession()
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
    monkeypatch.setattr(
        lessons_resources_view,
        "find_published_lesson",
        lambda db, *, lesson_id: sample_lesson_row(),
    )
    monkeypatch.setattr(
        lessons_resources_view,
        "find_lesson_resources",
        lambda db, *, lesson_id: sample_resource_rows(),
    )

    response = get_lesson_resources(
        authorization="Bearer student-token",
        lesson_id_raw="101",
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )
    assert isinstance(response, dict)
    assert response["success"] is True
    assert response["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert response["data"]["id"] == 101
    assert len(response["data"]["resources"]) == 2
    assert response["data"]["resources"][0]["name"] == "Slides PDF"


def test_get_lesson_resources_empty_resources(monkeypatch: pytest.MonkeyPatch) -> None:
    session = FakeSession()
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
    monkeypatch.setattr(
        lessons_resources_view,
        "find_published_lesson",
        lambda db, *, lesson_id: sample_lesson_row(),
    )
    monkeypatch.setattr(
        lessons_resources_view,
        "find_lesson_resources",
        lambda db, *, lesson_id: [],
    )

    response = get_lesson_resources(
        authorization="Bearer student-token",
        lesson_id_raw="101",
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )
    assert isinstance(response, dict)
    assert response["success"] is True
    assert response["data"]["id"] == 101
    assert response["data"]["resources"] == []


def test_lesson_resources_route_via_client(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
    monkeypatch.setattr(
        lessons_resources_view,
        "find_published_lesson",
        lambda db, *, lesson_id: sample_lesson_row(),
    )
    monkeypatch.setattr(
        lessons_resources_view,
        "find_lesson_resources",
        lambda db, *, lesson_id: sample_resource_rows(),
    )

    try:
        res = client.get(
            "/api/v1/lessons/101/resources",
            headers={"Authorization": "Bearer student-token"},
        )
        assert res.status_code == 200
        data = res.json()
        assert data["success"] is True
        assert data["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
        assert data["data"]["id"] == 101
        assert len(data["data"]["resources"]) == 2
    finally:
        client.app.dependency_overrides.clear()
