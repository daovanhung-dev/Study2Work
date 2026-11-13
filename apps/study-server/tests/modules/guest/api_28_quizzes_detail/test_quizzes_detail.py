"""Bộ kiểm thử đơn vị cho API #28 lấy chi tiết quiz và danh sách câu hỏi."""

from __future__ import annotations

import json
from typing import Any

import app.modules.guest.api_28_quizzes_detail.view as quizzes_detail_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.guest.api_28_quizzes_detail.validate import (
    validate_quiz_detail_request,
    validate_quiz_id,
)
from app.modules.guest.api_28_quizzes_detail.view import (
    format_decimal,
    get_quiz_detail,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse


class FakeSession:
    """Mock session để kiểm tra transaction rollback khi xảy ra lỗi database."""

    def __init__(self) -> None:
        self.rollback_count = 0

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
        "title": "Kiểm tra kiến thức cơ bản Python",
        "duration_minutes": 45,
        "passing_score": "70.00",
        "status": "PUBLISHED",
    }


def sample_question_rows() -> list[dict[str, Any]]:
    """Tạo danh sách câu hỏi mẫu cho bài quiz."""
    return [
        {
            "id": 1,
            "quiz_id": 501,
            "text": "Python là ngôn ngữ thông dịch hay biên dịch?",
            "sort_order": 1,
        },
        {
            "id": 2,
            "quiz_id": 501,
            "text": "Kiểu dữ liệu nào là immutable trong Python?",
            "sort_order": 2,
        },
    ]


def sample_choice_rows() -> list[dict[str, Any]]:
    """Tạo danh sách lựa chọn mẫu cho các câu hỏi (không có trường is_correct)."""
    return [
        {"id": 10, "question_id": 1, "choice_text": "Thông dịch"},
        {"id": 11, "question_id": 1, "choice_text": "Biên dịch"},
        {"id": 20, "question_id": 2, "choice_text": "Tuple"},
        {"id": 21, "question_id": 2, "choice_text": "List"},
    ]


def test_format_decimal() -> None:
    """Kiểm tra helper chuyển đổi số sang chuỗi thập phân decimal-string chuẩn."""
    assert format_decimal(None) == "0.00"
    assert format_decimal(70) == "70.00"
    assert format_decimal("70.5") == "70.50"
    assert format_decimal("invalid") == "0.00"


def test_validate_quiz_id_valid() -> None:
    """Kiểm tra validate_quiz_id chuyển đổi thành công chuỗi số nguyên hợp lệ."""
    result = validate_quiz_id("501", trace_id="test-trace")
    assert result == 501


def test_validate_quiz_id_invalid() -> None:
    """Kiểm tra validate_quiz_id trả về lỗi 404 DESIGN_RESOURCE_NOT_FOUND khi id không hợp lệ."""
    for invalid_val in ["abc", "-1", "0", str(2**63)]:
        result = validate_quiz_id(invalid_val, trace_id="test-trace")
        assert isinstance(result, JSONResponse)
        assert result.status_code == 404
        payload = json.loads(result.body.decode())
        assert payload["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
        assert payload["message"] == "Quiz not found"


def test_validate_quiz_detail_request_auth_error() -> None:
    """Kiểm tra validate_quiz_detail_request trả về lỗi 401 khi thiếu token."""
    result = validate_quiz_detail_request(
        authorization=None,
        quiz_id_raw="501",
        trace_id="test-trace",
    )
    assert isinstance(result, JSONResponse)
    assert result.status_code == 401
    payload = json.loads(result.body.decode())
    assert payload["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_validate_quiz_detail_request_forbidden(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kiểm tra validate_quiz_detail_request trả về lỗi 403 khi role không phải STUDENT."""
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: mentor_claims())
    result = validate_quiz_detail_request(
        authorization="Bearer mentor-token",
        quiz_id_raw="501",
        trace_id="test-trace",
    )
    assert isinstance(result, JSONResponse)
    assert result.status_code == 403
    payload = json.loads(result.body.decode())
    assert payload["businessCode"] == "DESIGN_ACCESS_DENIED"


def test_get_quiz_detail_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kiểm tra get_quiz_detail trả về 404 khi không tìm thấy quiz trong database."""
    session = FakeSession()
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
    monkeypatch.setattr(quizzes_detail_view, "find_quiz_by_id", lambda db, quiz_id: None)

    response = get_quiz_detail(
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


def test_get_quiz_detail_database_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kiểm tra get_quiz_detail gọi rollback và trả về 500 khi xảy ra SQLAlchemyError."""
    session = FakeSession()
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())

    def raise_db_error(db, quiz_id):
        raise SQLAlchemyError("Connection failed")

    monkeypatch.setattr(quizzes_detail_view, "find_quiz_by_id", raise_db_error)

    response = get_quiz_detail(
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


def test_get_quiz_detail_success_without_questions(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kiểm tra get_quiz_detail trả về 200 khi quiz hợp lệ và chưa có câu hỏi nào."""
    session = FakeSession()
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
    monkeypatch.setattr(
        quizzes_detail_view,
        "find_quiz_by_id",
        lambda db, quiz_id: sample_quiz_row(),
    )
    monkeypatch.setattr(
        quizzes_detail_view,
        "find_quiz_questions",
        lambda db, quiz_id: [],
    )
    monkeypatch.setattr(
        quizzes_detail_view,
        "find_quiz_choices",
        lambda db, quiz_id: [],
    )

    response = get_quiz_detail(
        authorization="Bearer valid-token",
        quiz_id_raw="501",
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )

    assert isinstance(response, dict)
    assert response["success"] is True
    assert response["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    data = response["data"]
    assert data["id"] == 501
    assert data["course_id"] == 9001
    assert data["title"] == "Kiểm tra kiến thức cơ bản Python"
    assert data["duration_minutes"] == 45
    assert data["passing_score"] == "70.00"
    assert data["questions"] == []


def test_get_quiz_detail_success_with_questions_and_choices(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra get_quiz_detail trả về 200 với đầy đủ câu hỏi và lựa chọn, không lộ is_correct."""
    session = FakeSession()
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
    monkeypatch.setattr(
        quizzes_detail_view,
        "find_quiz_by_id",
        lambda db, quiz_id: sample_quiz_row(),
    )
    monkeypatch.setattr(
        quizzes_detail_view,
        "find_quiz_questions",
        lambda db, quiz_id: sample_question_rows(),
    )
    monkeypatch.setattr(
        quizzes_detail_view,
        "find_quiz_choices",
        lambda db, quiz_id: sample_choice_rows(),
    )

    response = get_quiz_detail(
        authorization="Bearer valid-token",
        quiz_id_raw="501",
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )

    assert isinstance(response, dict)
    assert response["success"] is True
    data = response["data"]
    assert len(data["questions"]) == 2

    # Kiểm tra câu hỏi 1 và các lựa chọn
    q1 = data["questions"][0]
    assert q1["id"] == 1
    assert q1["text"] == "Python là ngôn ngữ thông dịch hay biên dịch?"
    assert q1["type"] == "MULTIPLE_CHOICE"
    assert len(q1["choices"]) == 2
    assert q1["choices"][0]["choice_text"] == "Thông dịch"

    # Kiểm tra bảo mật: tuyệt đối không có trường is_correct trong bất kỳ choice nào
    for q in data["questions"]:
        for choice in q["choices"]:
            assert "is_correct" not in choice


def test_quiz_detail_route_via_client(
    client: TestClient,
    app: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra gọi endpoint GET /api/v1/quizzes/{quiz_id} thông qua TestClient."""
    session = FakeSession()
    app.dependency_overrides[get_db] = override_db(session)

    try:
        # 1. Gọi không có Authorization -> 401
        res_401 = client.get("/api/v1/quizzes/501")
        assert res_401.status_code == 401
        body_401 = res_401.json()
        assert body_401["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"

        # 2. Gọi với role MENTOR -> 403
        monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: mentor_claims())
        res_403 = client.get(
            "/api/v1/quizzes/501",
            headers={"Authorization": "Bearer mentor-token"},
        )
        assert res_403.status_code == 403
        body_403 = res_403.json()
        assert body_403["businessCode"] == "DESIGN_ACCESS_DENIED"

        # 3. Gọi với STUDENT role nhưng quiz không tồn tại -> 404
        monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
        monkeypatch.setattr(quizzes_detail_view, "find_quiz_by_id", lambda db, quiz_id: None)
        res_404 = client.get(
            "/api/v1/quizzes/9999",
            headers={"Authorization": "Bearer student-token"},
        )
        assert res_404.status_code == 404
        body_404 = res_404.json()
        assert body_404["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"

        # 4. Thành công 200
        monkeypatch.setattr(
            quizzes_detail_view,
            "find_quiz_by_id",
            lambda db, quiz_id: sample_quiz_row(),
        )
        monkeypatch.setattr(
            quizzes_detail_view,
            "find_quiz_questions",
            lambda db, quiz_id: sample_question_rows(),
        )
        monkeypatch.setattr(
            quizzes_detail_view,
            "find_quiz_choices",
            lambda db, quiz_id: sample_choice_rows(),
        )

        res_200 = client.get(
            "/api/v1/quizzes/501",
            headers={"Authorization": "Bearer student-token"},
        )
        assert res_200.status_code == 200
        body_200 = res_200.json()
        assert body_200["success"] is True
        assert body_200["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
        assert body_200["data"]["id"] == 501
        assert len(body_200["data"]["questions"]) == 2
        # Kiểm tra traceId và meta
        assert "traceId" in body_200
        assert "meta" in body_200

    finally:
        app.dependency_overrides.clear()

