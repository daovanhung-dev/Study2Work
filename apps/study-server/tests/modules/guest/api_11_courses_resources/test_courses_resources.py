from __future__ import annotations

from typing import Any

import app.modules.guest.api_11_courses_resources.view as resources_view
import pytest
from app.core.database import get_db
from app.modules.guest.api_11_courses_resources.models import ResourceItem
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    def __init__(self) -> None:
        self.rollback_count = 0

    def rollback(self) -> None:
        self.rollback_count += 1


def override_db(session: FakeSession):
    def dependency():
        yield session

    return dependency


def sample_resource_row() -> dict[str, Any]:
    return {
        "id": 101,
        "name": "Tai lieu tham khao.pdf",
        "resource_type": "DOCUMENT",
        "url": "https://cdn.example.com/res/101.pdf",
        "lesson_id": 12,
    }


def test_resource_item_model_maps_type() -> None:
    item = ResourceItem(
        id=1,
        name="Doc",
        type="DOCUMENT",
        url="https://example.com/1.pdf",
        lesson_id=10,
    )
    assert item.id == 1
    assert item.name == "Doc"
    assert item.type == "DOCUMENT"
    assert item.url == "https://example.com/1.pdf"
    assert item.lesson_id == 10


def test_get_resources_course_not_found(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)

    monkeypatch.setattr(
        resources_view,
        "find_published_course",
        lambda db, *, course_id: None,
    )

    response = client.get("/api/v1/courses/999/resources")
    assert response.status_code == 404
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_get_resources_empty_resources_returns_404(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)

    monkeypatch.setattr(
        resources_view,
        "find_published_course",
        lambda db, *, course_id: {"id": course_id, "status": "PUBLISHED"},
    )
    monkeypatch.setattr(
        resources_view,
        "find_course_resources",
        lambda db, *, course_id: [],
    )

    response = client.get("/api/v1/courses/1/resources")
    assert response.status_code == 404
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_get_resources_success(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)

    monkeypatch.setattr(
        resources_view,
        "find_published_course",
        lambda db, *, course_id: {"id": course_id, "status": "PUBLISHED"},
    )
    monkeypatch.setattr(
        resources_view,
        "find_course_resources",
        lambda db, *, course_id: [sample_resource_row()],
    )

    response = client.get(
        "/api/v1/courses/1/resources",
        headers={"X-Trace-Id": "00000000-0000-0000-0000-000000000011"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"] == {
        "id": 101,
        "name": "Tai lieu tham khao.pdf",
        "type": "DOCUMENT",
        "url": "https://cdn.example.com/res/101.pdf",
        "lesson_id": 12,
    }
    assert payload["traceId"] == "00000000-0000-0000-0000-000000000011"


def test_get_resources_database_error_rolls_back(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)

    def fail_course(db, *, course_id):
        raise SQLAlchemyError("DB error")

    monkeypatch.setattr(resources_view, "find_published_course", fail_course)

    response = client.get("/api/v1/courses/1/resources")
    assert response.status_code == 500
    assert session.rollback_count == 1
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_INTERNAL_ERROR"


def test_validate_course_id_success() -> None:
    from app.modules.guest.api_11_courses_resources.validate import validate_course_id

    result = validate_course_id(1, trace_id="test-trace-id")
    assert result == 1


def test_validate_course_id_invalid_returns_error_response() -> None:
    from app.modules.guest.api_11_courses_resources.validate import validate_course_id
    from starlette.responses import JSONResponse

    result = validate_course_id(0, trace_id="test-trace-id")
    assert isinstance(result, JSONResponse)
    assert result.status_code == 404
