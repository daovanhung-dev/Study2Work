from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import app.modules.guest.api_15_courses_enrollment_status.view as enrollment_view
import pytest
from app.core.database import get_db
from app.modules.guest.api_15_courses_enrollment_status.models import (
    EnrollmentStatusResponse,
)
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


def sample_enrollment_row() -> dict[str, Any]:
    return {
        "id": 501,
        "user_id": 1001,
        "course_id": 101,
        "status": "ACTIVE",
        "enrolled_at": datetime(2026, 9, 20, 10, 0, 0, tzinfo=UTC),
        "completed_at": None,
    }


def test_enrollment_status_model_validates_required_fields() -> None:
    now = datetime.now(UTC)
    model = EnrollmentStatusResponse(
        id=1,
        user_id=2,
        course_id=3,
        status="ACTIVE",
        enrolled_at=now,
        completed_at=None,
    )
    assert model.id == 1
    assert model.user_id == 2
    assert model.course_id == 3
    assert model.status == "ACTIVE"
    assert model.enrolled_at == now
    assert model.completed_at is None


def test_get_enrollment_status_course_not_found(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)

    monkeypatch.setattr(
        enrollment_view,
        "find_course_by_id",
        lambda db, *, course_id: None,
    )

    response = client.get("/api/v1/courses/999/enrollment-status")
    assert response.status_code == 404
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert payload["message"] == "Enrollment status not found."


def test_get_enrollment_status_enrollment_not_found(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)

    monkeypatch.setattr(
        enrollment_view,
        "find_course_by_id",
        lambda db, *, course_id: {"id": course_id, "status": "PUBLISHED"},
    )
    monkeypatch.setattr(
        enrollment_view,
        "find_enrollment",
        lambda db, *, course_id, user_id=None: None,
    )

    response = client.get("/api/v1/courses/1/enrollment-status")
    assert response.status_code == 404
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_get_enrollment_status_success(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)

    monkeypatch.setattr(
        enrollment_view,
        "find_course_by_id",
        lambda db, *, course_id: {"id": course_id, "status": "PUBLISHED"},
    )
    monkeypatch.setattr(
        enrollment_view,
        "find_enrollment",
        lambda db, *, course_id, user_id=None: sample_enrollment_row(),
    )

    response = client.get(
        "/api/v1/courses/101/enrollment-status",
        headers={"X-Trace-Id": "00000000-0000-0000-0000-000000000015"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["message"] == "Enrollment status retrieved."
    assert payload["data"]["id"] == 501
    assert payload["data"]["user_id"] == 1001
    assert payload["data"]["course_id"] == 101
    assert payload["data"]["status"] == "ACTIVE"
    assert payload["traceId"] == "00000000-0000-0000-0000-000000000015"


def test_get_enrollment_status_database_error_rolls_back(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)

    def fail_course(db, *, course_id):
        raise SQLAlchemyError("DB error")

    monkeypatch.setattr(enrollment_view, "find_course_by_id", fail_course)

    response = client.get("/api/v1/courses/1/enrollment-status")
    assert response.status_code == 500
    assert session.rollback_count == 1
    payload = response.json()
    assert payload["success"] is False
    assert payload["businessCode"] == "DESIGN_INTERNAL_ERROR"
