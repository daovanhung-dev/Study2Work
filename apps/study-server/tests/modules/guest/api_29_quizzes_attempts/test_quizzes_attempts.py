"""Bộ kiểm thử đơn vị cho API #29 tạo lượt làm bài kiểm tra (quiz attempt)."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

import app.modules.guest.api_29_quizzes_attempts.view as quizzes_attempts_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.guest.api_29_quizzes_attempts.validate import (
    validate_create_attempt_request,
    validate_quiz_id,
)
from app.modules.guest.api_29_quizzes_attempts.view import (
    create_quiz_attempt,
    format_iso_timestamp,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse


class FakeSession:
    """Mock session để kiểm tra transaction commit và rollback."""

    def __init__(self) -> None:
        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        self.commit_count += 1

    def rollback(self) -> None:
        self.rollback_count += 1


def override_db(session: FakeSession):
    """Fixture override get_db dependency trả về mock session."""

    def dependency():
        yield session

    return dependency


def student_claims() -> dict[str, Any]:
    """Tạo payload JWT claims hợp lệ cho Student."""
    return {"sub": "1001", "roles": ["STUDENT"]}


def mentor_claims() -> dict[str, Any]:
    """Tạo payload JWT claims của role MENTOR (không có quyền STUDENT)."""
    return {"sub": "2001", "roles": ["MENTOR"]}


def sample_quiz_row() -> dict[str, Any]:
    """Tạo bản ghi dữ liệu mẫu cho bài quiz."""
    return {
        "id": 501,
        "course_id": 9001,
        "status": "PUBLISHED",
    }


def sample_created_attempt_row() -> dict[str, Any]:
    """Tạo bản ghi dữ liệu mẫu sau khi insert attempt thành công."""
    return {
        "id": 9001,
        "quiz_id": 501,
        "user_id": 1001,
        "status": "IN_PROGRESS",
        "started_at": datetime(2026, 10, 21, 12, 0, 0, tzinfo=UTC),
        "submitted_at": None,
        "score": None,
    }


def test_format_iso_timestamp() -> None:
    """Kiểm tra format_iso_timestamp định dạng đúng ISO 8601."""
    dt_with_tz = datetime(2026, 10, 21, 12, 0, 0, tzinfo=UTC)
    assert format_iso_timestamp(dt_with_tz) == "2026-10-21T12:00:00+00:00"

    dt_naive = datetime(2026, 10, 21, 12, 0, 0)
    assert "2026-10-21T12:00:00" in format_iso_timestamp(dt_naive)

    assert format_iso_timestamp("2026-10-21T12:00:00Z") == "2026-10-21T12:00:00Z"


def test_validate_quiz_id_valid() -> None:
    """Kiểm tra validate_quiz_id chuyển đổi thành công số nguyên hợp lệ."""
    result = validate_quiz_id("501", trace_id="test-trace")
    assert result == 501


def test_validate_quiz_id_invalid() -> None:
    """Kiểm tra validate_quiz_id trả về 422 DESIGN_VALIDATION_ERROR khi path không hợp lệ."""
    for invalid_val in ["abc", "-1", "0", str(2**63)]:
        result = validate_quiz_id(invalid_val, trace_id="test-trace")
        assert isinstance(result, JSONResponse)
        assert result.status_code == 422
        payload = json.loads(result.body.decode())
        assert payload["businessCode"] == "DESIGN_VALIDATION_ERROR"
        assert payload["message"] == "Invalid quiz_id"


def test_validate_create_attempt_request_auth_error() -> None:
    """Kiểm tra validate_create_attempt_request trả về 401 khi thiếu token."""
    result = validate_create_attempt_request(
        authorization=None,
        quiz_id_raw="501",
        trace_id="test-trace",
    )
    assert isinstance(result, JSONResponse)
    assert result.status_code == 401
    payload = json.loads(result.body.decode())
    assert payload["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_validate_create_attempt_request_forbidden(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kiểm tra validate_create_attempt_request trả về 403 khi role không phải STUDENT."""
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: mentor_claims())
    result = validate_create_attempt_request(
        authorization="Bearer mentor-token",
        quiz_id_raw="501",
        trace_id="test-trace",
    )
    assert isinstance(result, JSONResponse)
    assert result.status_code == 403
    payload = json.loads(result.body.decode())
    assert payload["businessCode"] == "DESIGN_ACCESS_DENIED"


def test_create_quiz_attempt_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kiểm tra create_quiz_attempt trả về 404 khi quiz không tồn tại."""
    session = FakeSession()
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
    monkeypatch.setattr(quizzes_attempts_view, "find_quiz", lambda db, quiz_id: None)

    response = create_quiz_attempt(
        authorization="Bearer valid-token",
        quiz_id_raw="501",
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )

    assert isinstance(response, JSONResponse)
    assert response.status_code == 404
    payload = json.loads(response.body.decode())
    assert payload["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert payload["message"] == "Quiz not found"


def test_create_quiz_attempt_conflict(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kiểm tra create_quiz_attempt trả về 409 khi đã có attempt đang IN_PROGRESS."""
    session = FakeSession()
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
    monkeypatch.setattr(
        quizzes_attempts_view,
        "find_quiz",
        lambda db, quiz_id: sample_quiz_row(),
    )
    monkeypatch.setattr(
        quizzes_attempts_view,
        "find_active_attempt",
        lambda db, quiz_id, user_id: {"id": 8001, "status": "IN_PROGRESS"},
    )

    response = create_quiz_attempt(
        authorization="Bearer valid-token",
        quiz_id_raw="501",
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )

    assert isinstance(response, JSONResponse)
    assert response.status_code == 409
    payload = json.loads(response.body.decode())
    assert payload["businessCode"] == "DESIGN_STATE_CONFLICT"


def test_create_quiz_attempt_database_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kiểm tra create_quiz_attempt rollback và trả về 500 khi gặp SQLAlchemyError."""
    session = FakeSession()
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
    monkeypatch.setattr(
        quizzes_attempts_view,
        "find_quiz",
        lambda db, quiz_id: sample_quiz_row(),
    )
    monkeypatch.setattr(
        quizzes_attempts_view,
        "find_active_attempt",
        lambda db, quiz_id, user_id: None,
    )

    def raise_db_error(db, quiz_id, user_id, started_at):
        raise SQLAlchemyError("Insert attempt failed")

    monkeypatch.setattr(quizzes_attempts_view, "create_quiz_attempt_record", raise_db_error)

    response = create_quiz_attempt(
        authorization="Bearer valid-token",
        quiz_id_raw="501",
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )

    assert session.rollback_count == 1
    assert isinstance(response, JSONResponse)
    assert response.status_code == 500
    payload = json.loads(response.body.decode())
    assert payload["businessCode"] == "DESIGN_INTERNAL_ERROR"


def test_create_quiz_attempt_success(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kiểm tra create_quiz_attempt tạo mới thành công, commit transaction và trả về 201 data."""
    session = FakeSession()
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
    monkeypatch.setattr(
        quizzes_attempts_view,
        "find_quiz",
        lambda db, quiz_id: sample_quiz_row(),
    )
    monkeypatch.setattr(
        quizzes_attempts_view,
        "find_active_attempt",
        lambda db, quiz_id, user_id: None,
    )
    monkeypatch.setattr(
        quizzes_attempts_view,
        "create_quiz_attempt_record",
        lambda db, quiz_id, user_id, started_at: sample_created_attempt_row(),
    )

    response = create_quiz_attempt(
        authorization="Bearer valid-token",
        quiz_id_raw="501",
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )

    assert session.commit_count == 1
    assert isinstance(response, dict)
    assert response["success"] is True
    assert response["businessCode"] == "DESIGN_RESOURCE_CREATED"
    data = response["data"]
    assert data["id"] == 9001
    assert data["quiz_id"] == 501
    assert data["status"] == "IN_PROGRESS"
    assert "2026-10-21T12:00:00" in data["started_at"]
    assert data["answers"] == []


def test_quiz_attempt_route_via_client(
    client: TestClient,
    app: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra gọi endpoint POST /api/v1/quizzes/{quiz_id}/attempts thông qua TestClient."""
    session = FakeSession()
    app.dependency_overrides[get_db] = override_db(session)

    try:
        # 1. Gọi không có Authorization -> 401
        res_401 = client.post("/api/v1/quizzes/501/attempts")
        assert res_401.status_code == 401
        body_401 = res_401.json()
        assert body_401["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"

        # 2. Gọi với role MENTOR -> 403
        monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: mentor_claims())
        res_403 = client.post(
            "/api/v1/quizzes/501/attempts",
            headers={"Authorization": "Bearer mentor-token"},
        )
        assert res_403.status_code == 403
        body_403 = res_403.json()
        assert body_403["businessCode"] == "DESIGN_ACCESS_DENIED"

        # 3. Path parameter không hợp lệ -> 422
        monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
        res_422 = client.post(
            "/api/v1/quizzes/invalid-id/attempts",
            headers={"Authorization": "Bearer student-token"},
        )
        assert res_422.status_code == 422
        body_422 = res_422.json()
        assert body_422["businessCode"] == "DESIGN_VALIDATION_ERROR"

        # 4. Quiz không tồn tại -> 404
        monkeypatch.setattr(quizzes_attempts_view, "find_quiz", lambda db, quiz_id: None)
        res_404 = client.post(
            "/api/v1/quizzes/9999/attempts",
            headers={"Authorization": "Bearer student-token"},
        )
        assert res_404.status_code == 404
        body_404 = res_404.json()
        assert body_404["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"

        # 5. Đã có attempt in progress -> 409
        monkeypatch.setattr(
            quizzes_attempts_view,
            "find_quiz",
            lambda db, quiz_id: sample_quiz_row(),
        )
        monkeypatch.setattr(
            quizzes_attempts_view,
            "find_active_attempt",
            lambda db, quiz_id, user_id: {"id": 8001, "status": "IN_PROGRESS"},
        )
        res_409 = client.post(
            "/api/v1/quizzes/501/attempts",
            headers={"Authorization": "Bearer student-token"},
        )
        assert res_409.status_code == 409
        body_409 = res_409.json()
        assert body_409["businessCode"] == "DESIGN_STATE_CONFLICT"

        # 6. Thành công -> 201 Created
        monkeypatch.setattr(
            quizzes_attempts_view,
            "find_active_attempt",
            lambda db, quiz_id, user_id: None,
        )
        monkeypatch.setattr(
            quizzes_attempts_view,
            "create_quiz_attempt_record",
            lambda db, quiz_id, user_id, started_at: sample_created_attempt_row(),
        )
        res_201 = client.post(
            "/api/v1/quizzes/501/attempts",
            headers={"Authorization": "Bearer student-token"},
        )
        assert res_201.status_code == 201
        body_201 = res_201.json()
        assert body_201["success"] is True
        assert body_201["businessCode"] == "DESIGN_RESOURCE_CREATED"
        assert body_201["data"]["id"] == 9001
        assert body_201["data"]["quiz_id"] == 501
        assert body_201["data"]["status"] == "IN_PROGRESS"
        assert "traceId" in body_201
        assert "meta" in body_201

    finally:
        app.dependency_overrides.clear()
