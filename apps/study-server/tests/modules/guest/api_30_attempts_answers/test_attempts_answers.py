"""Bộ kiểm thử đơn vị cho API #30 autosave/lưu câu trả lời bài kiểm tra."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

import app.modules.guest.api_30_attempts_answers.view as attempts_answers_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.guest.api_30_attempts_answers.models import SaveAnswerRequest
from app.modules.guest.api_30_attempts_answers.validate import (
    validate_attempt_id,
    validate_question_id,
    validate_save_answer_request,
)
from app.modules.guest.api_30_attempts_answers.view import (
    parse_choice_id,
    save_attempt_answer,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse


class FakeSession:
    """Mock session để kiểm tra transaction commit và rollback."""

    def __init__(self) -> None:
        self.commit_count = 0
        self.rollback_count = 0
        self.executed_statements: list[str] = []

    def commit(self) -> None:
        self.commit_count += 1

    def rollback(self) -> None:
        self.rollback_count += 1

    def execute(self, statement: Any, params: Any = None) -> Any:
        self.executed_statements.append(str(statement))
        return None


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


def sample_attempt_row(
    *,
    user_id: int = 1001,
    status: str = "IN_PROGRESS",
    quiz_id: int = 501,
) -> dict[str, Any]:
    """Tạo bản ghi dữ liệu mẫu cho lượt làm bài."""
    return {
        "id": 9001,
        "quiz_id": quiz_id,
        "user_id": user_id,
        "status": status,
        "started_at": datetime(2026, 10, 21, 12, 0, 0, tzinfo=UTC),
        "submitted_at": None,
        "score": None,
    }


def sample_question_row(*, quiz_id: int = 501) -> dict[str, Any]:
    """Tạo bản ghi dữ liệu mẫu cho câu hỏi."""
    return {
        "id": 301,
        "quiz_id": quiz_id,
    }


def test_parse_choice_id() -> None:
    """Kiểm tra helper parse_choice_id trích xuất số ID lựa chọn hợp lệ."""
    assert parse_choice_id("10") == 10
    assert parse_choice_id(15) == 15
    assert parse_choice_id(" 20 ") == 20
    assert parse_choice_id("abc") is None
    assert parse_choice_id(None) is None
    assert parse_choice_id("-1") is None
    assert parse_choice_id("0") is None


def test_validate_attempt_id() -> None:
    """Kiểm tra validate_attempt_id chuyển đổi đúng số nguyên hoặc báo lỗi 422."""
    assert validate_attempt_id("9001", trace_id="test-trace") == 9001

    for invalid in ["abc", "-5", "0", str(2**63)]:
        res = validate_attempt_id(invalid, trace_id="test-trace")
        assert isinstance(res, JSONResponse)
        assert res.status_code == 422
        body = json.loads(res.body.decode())
        assert body["businessCode"] == "DESIGN_VALIDATION_ERROR"


def test_validate_question_id() -> None:
    """Kiểm tra validate_question_id kiểm tra đúng ID câu hỏi dương."""
    assert validate_question_id(301, trace_id="test-trace") == 301

    for invalid in [-1, 0, 2**63]:
        res = validate_question_id(invalid, trace_id="test-trace")
        assert isinstance(res, JSONResponse)
        assert res.status_code == 422


def test_validate_save_answer_request_auth_error() -> None:
    """Kiểm tra validate_save_answer_request trả về lỗi 401 khi thiếu token."""
    res = validate_save_answer_request(
        authorization=None,
        attempt_id_raw="9001",
        question_id_raw=301,
        trace_id="test-trace",
    )
    assert isinstance(res, JSONResponse)
    assert res.status_code == 401
    body = json.loads(res.body.decode())
    assert body["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_validate_save_answer_request_forbidden(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kiểm tra validate_save_answer_request trả về lỗi 403 khi role không phải STUDENT."""
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: mentor_claims())
    res = validate_save_answer_request(
        authorization="Bearer mentor-token",
        attempt_id_raw="9001",
        question_id_raw=301,
        trace_id="test-trace",
    )
    assert isinstance(res, JSONResponse)
    assert res.status_code == 403
    body = json.loads(res.body.decode())
    assert body["businessCode"] == "DESIGN_ACCESS_DENIED"


def test_save_attempt_answer_attempt_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kiểm tra save_attempt_answer trả về 404 khi không tìm thấy attempt."""
    session = FakeSession()
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
    monkeypatch.setattr(attempts_answers_view, "find_attempt", lambda db, attempt_id: None)

    payload = SaveAnswerRequest(question_id=301, answer="10")
    res = save_attempt_answer(
        authorization="Bearer valid-token",
        attempt_id_raw="9001",
        payload=payload,
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )

    assert isinstance(res, JSONResponse)
    assert res.status_code == 404
    body = json.loads(res.body.decode())
    assert body["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert body["message"] == "Attempt not found"


def test_save_attempt_answer_wrong_owner(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kiểm tra save_attempt_answer trả về 403 khi attempt thuộc về học viên khác."""
    session = FakeSession()
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
    # attempt owned by user 9999 instead of 1001
    monkeypatch.setattr(
        attempts_answers_view,
        "find_attempt",
        lambda db, attempt_id: sample_attempt_row(user_id=9999),
    )

    payload = SaveAnswerRequest(question_id=301, answer="10")
    res = save_attempt_answer(
        authorization="Bearer valid-token",
        attempt_id_raw="9001",
        payload=payload,
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )

    assert isinstance(res, JSONResponse)
    assert res.status_code == 403
    body = json.loads(res.body.decode())
    assert body["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert body["message"] == "Access denied to this attempt"


def test_save_attempt_answer_closed_attempt(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kiểm tra save_attempt_answer trả về 403 khi attempt đã nộp hoặc không ở IN_PROGRESS."""
    session = FakeSession()
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
    monkeypatch.setattr(
        attempts_answers_view,
        "find_attempt",
        lambda db, attempt_id: sample_attempt_row(status="SUBMITTED"),
    )

    payload = SaveAnswerRequest(question_id=301, answer="10")
    res = save_attempt_answer(
        authorization="Bearer valid-token",
        attempt_id_raw="9001",
        payload=payload,
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )

    assert isinstance(res, JSONResponse)
    assert res.status_code == 403
    body = json.loads(res.body.decode())
    assert body["businessCode"] == "DESIGN_ACCESS_DENIED"


def test_save_attempt_answer_question_mismatch(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kiểm tra save_attempt_answer trả về 404 khi question không thuộc quiz của attempt."""
    session = FakeSession()
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
    monkeypatch.setattr(
        attempts_answers_view,
        "find_attempt",
        lambda db, attempt_id: sample_attempt_row(quiz_id=501),
    )
    # Question belongs to quiz 999 instead of 501
    monkeypatch.setattr(
        attempts_answers_view,
        "find_question",
        lambda db, question_id: sample_question_row(quiz_id=999),
    )

    payload = SaveAnswerRequest(question_id=301, answer="10")
    res = save_attempt_answer(
        authorization="Bearer valid-token",
        attempt_id_raw="9001",
        payload=payload,
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )

    assert isinstance(res, JSONResponse)
    assert res.status_code == 404
    body = json.loads(res.body.decode())
    assert body["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"


def test_save_attempt_answer_db_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kiểm tra save_attempt_answer rollback và trả về 500 khi gặp SQLAlchemyError."""
    session = FakeSession()
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
    monkeypatch.setattr(
        attempts_answers_view,
        "find_attempt",
        lambda db, attempt_id: sample_attempt_row(),
    )
    monkeypatch.setattr(
        attempts_answers_view,
        "find_question",
        lambda db, question_id: sample_question_row(),
    )

    def raise_error(db, attempt_id, question_id, choice_id):
        raise SQLAlchemyError("Database error")

    monkeypatch.setattr(attempts_answers_view, "upsert_answer", raise_error)

    payload = SaveAnswerRequest(question_id=301, answer="10")
    res = save_attempt_answer(
        authorization="Bearer valid-token",
        attempt_id_raw="9001",
        payload=payload,
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )

    assert session.rollback_count == 1
    assert isinstance(res, JSONResponse)
    assert res.status_code == 500
    body = json.loads(res.body.decode())
    assert body["businessCode"] == "DESIGN_INTERNAL_ERROR"


def test_save_attempt_answer_success(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kiểm tra save_attempt_answer thành công, commit transaction và trả về danh sách answer."""
    session = FakeSession()
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
    monkeypatch.setattr(
        attempts_answers_view,
        "find_attempt",
        lambda db, attempt_id: sample_attempt_row(),
    )
    monkeypatch.setattr(
        attempts_answers_view,
        "find_question",
        lambda db, question_id: sample_question_row(),
    )
    monkeypatch.setattr(
        attempts_answers_view,
        "find_existing_answer",
        lambda db, attempt_id, question_id: None,
    )
    monkeypatch.setattr(
        attempts_answers_view,
        "find_attempt_answers",
        lambda db, attempt_id: [{"question_id": 301, "choice_id": 10}],
    )

    payload = SaveAnswerRequest(question_id=301, answer="10")
    res = save_attempt_answer(
        authorization="Bearer valid-token",
        attempt_id_raw="9001",
        payload=payload,
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )

    assert session.commit_count == 1
    assert isinstance(res, dict)
    assert res["success"] is True
    assert res["businessCode"] == "DESIGN_RESOURCE_UPDATED"
    data = res["data"]
    assert data["id"] == 9001
    assert len(data["answers"]) == 1
    ans = data["answers"][0]
    assert ans["question_id"] == 301
    assert ans["choice_ids"] == [10]
    # Đảm bảo không lộ correct hay score trong answer
    assert "correct" not in ans
    assert "score" not in ans


def test_attempt_answer_route_via_client(
    client: TestClient,
    app: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra gọi endpoint PUT /api/v1/attempts/{attempt_id}/answers qua TestClient."""
    session = FakeSession()
    app.dependency_overrides[get_db] = override_db(session)

    try:
        # 1. Thiếu auth -> 401
        res_401 = client.put(
            "/api/v1/attempts/9001/answers",
            json={"question_id": 301, "answer(s)": "10"},
        )
        assert res_401.status_code == 401
        assert res_401.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"

        # 2. Sai role -> 403
        monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: mentor_claims())
        res_403 = client.put(
            "/api/v1/attempts/9001/answers",
            headers={"Authorization": "Bearer mentor-token"},
            json={"question_id": 301, "answer(s)": "10"},
        )
        assert res_403.status_code == 403
        assert res_403.json()["businessCode"] == "DESIGN_ACCESS_DENIED"

        # 3. Path attempt_id không hợp lệ -> 422
        monkeypatch.setattr(auth_utils, "decode_access_token", lambda token: student_claims())
        res_422 = client.put(
            "/api/v1/attempts/invalid-id/answers",
            headers={"Authorization": "Bearer student-token"},
            json={"question_id": 301, "answer(s)": "10"},
        )
        assert res_422.status_code == 422
        assert res_422.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"

        # 4. Thành công với alias "answer(s)" -> 200
        monkeypatch.setattr(
            attempts_answers_view,
            "find_attempt",
            lambda db, attempt_id: sample_attempt_row(),
        )
        monkeypatch.setattr(
            attempts_answers_view,
            "find_question",
            lambda db, question_id: sample_question_row(),
        )
        monkeypatch.setattr(
            attempts_answers_view,
            "find_existing_answer",
            lambda db, attempt_id, question_id: None,
        )
        monkeypatch.setattr(
            attempts_answers_view,
            "find_attempt_answers",
            lambda db, attempt_id: [{"question_id": 301, "choice_id": 10}],
        )

        res_200 = client.put(
            "/api/v1/attempts/9001/answers",
            headers={"Authorization": "Bearer student-token"},
            json={"question_id": 301, "answer(s)": "10"},
        )
        assert res_200.status_code == 200
        body_200 = res_200.json()
        assert body_200["success"] is True
        assert body_200["businessCode"] == "DESIGN_RESOURCE_UPDATED"
        assert body_200["data"]["id"] == 9001
        assert len(body_200["data"]["answers"]) == 1

        # 5. Thành công với alias "answer" -> 200
        res_200_alt = client.put(
            "/api/v1/attempts/9001/answers",
            headers={"Authorization": "Bearer student-token"},
            json={"question_id": 301, "answer": "10"},
        )
        assert res_200_alt.status_code == 200

    finally:
        app.dependency_overrides.clear()
