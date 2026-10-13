from __future__ import annotations

import json
from decimal import Decimal
from typing import Any

import app.modules.guest.api_08_courses_detail.view as detail_view
from app.core.database import get_db
from app.main import app
from app.modules.guest.api_08_courses_detail.validate import validate_course_id
from app.modules.guest.api_08_courses_detail.view import get_course_detail
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


def sample_course_row() -> dict[str, Any]:
    return {
        "id": 101,
        "title": "Introduction to Programming",
        "description": "Fundamentals of programming",
        "thumbnail_url": "https://cdn.example.test/courses/101.png",
        "price": Decimal("49.90"),
        "status": "PUBLISHED",
        "mentor_id": 7,
        "mentor_full_name": "Nguyen Van Mentor",
        "mentor_avatar_url": None,
    }


def test_validate_course_id_valid() -> None:
    result = validate_course_id("101", trace_id="test-trace")
    assert result == 101


def test_validate_course_id_invalid() -> None:
    result = validate_course_id("invalid-id", trace_id="test-trace")
    assert isinstance(result, JSONResponse)
    assert result.status_code == 404
    payload = json.loads(result.body.decode())
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_get_course_detail_invalid_id() -> None:
    session = FakeSession()
    response = get_course_detail(
        course_id_raw="abc",
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )
    assert isinstance(response, JSONResponse)
    assert response.status_code == 404


def test_get_course_detail_not_found(monkeypatch: Any) -> None:
    session = FakeSession()
    monkeypatch.setattr(detail_view, "find_published_course_detail", lambda db, *, course_id: None)

    response = get_course_detail(
        course_id_raw=101,
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )
    assert isinstance(response, JSONResponse)
    assert response.status_code == 404
    payload = json.loads(response.body.decode())
    assert payload["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_get_course_detail_db_error(monkeypatch: Any) -> None:
    session = FakeSession()

    def raise_db_error(db: Any, *, course_id: int) -> None:
        raise SQLAlchemyError("Connection failed")

    monkeypatch.setattr(detail_view, "find_published_course_detail", raise_db_error)

    response = get_course_detail(
        course_id_raw=101,
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )
    assert isinstance(response, JSONResponse)
    assert response.status_code == 500
    assert session.rollback_count == 1
    payload = json.loads(response.body.decode())
    assert payload["businessCode"] == "DESIGN_INTERNAL_ERROR"


def test_get_course_detail_success(monkeypatch: Any) -> None:
    session = FakeSession()
    monkeypatch.setattr(
        detail_view, "find_published_course_detail", lambda db, *, course_id: sample_course_row()
    )

    response = get_course_detail(
        course_id_raw=101,
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )
    assert isinstance(response, dict)
    assert response["success"] is True
    assert response["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert response["data"]["items"][0]["id"] == 101
    assert response["data"]["items"][0]["mentor"]["full_name"] == "Nguyen Van Mentor"
    assert response["data"]["pagination"]["total"] == 1


def test_course_detail_route_via_client(monkeypatch: Any) -> None:
    session = FakeSession()
    monkeypatch.setattr(
        detail_view, "find_published_course_detail", lambda db, *, course_id: sample_course_row()
    )

    app.dependency_overrides[get_db] = override_db(session)
    try:
        client = TestClient(app)
        res = client.get("/api/v1/courses/101")
        assert res.status_code == 200
        data = res.json()
        assert data["success"] is True
        assert data["data"]["items"][0]["title"] == "Introduction to Programming"
    finally:
        app.dependency_overrides.clear()
