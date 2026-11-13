"""Kiểm thử validation, truy vấn, ánh xạ và HTTP contract của API #32."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

import app.modules.guest.api_32_attempts_result.view as attempt_view
import pytest
from app.modules.guest.api_32_attempts_result.query import (
    ATTEMPT_ANSWERS_BY_ID,
    ATTEMPT_RESULT_BY_ID,
)
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse


class FakeSession:
    """Theo dõi rollback của API đọc kết quả mà không kết nối database thật."""

    def __init__(self) -> None:
        """Khởi tạo bộ đếm rollback cho một trường hợp kiểm thử."""

        self.rollback_count = 0

    def rollback(self) -> None:
        """Ghi nhận lần view hoàn tác transaction sau lỗi SQL."""

        self.rollback_count += 1


def attempt_row(**overrides: Any) -> dict[str, Any]:
    """Tạo row quiz attempt với các field view sử dụng và cho phép ghi đè."""

    row: dict[str, Any] = {
        "id": 3201,
        "quiz_id": 88,
        "status": "GRADED",
        "started_at": datetime(2026, 10, 1, 9, 0, tzinfo=UTC),
        "submitted_at": datetime(2026, 10, 1, 9, 30, tzinfo=UTC),
        "score": Decimal("87.50"),
    }
    row.update(overrides)
    return row


def answer_rows() -> list[dict[str, Any]]:
    """Tạo answer rows có field nhạy cảm để kiểm tra chúng không vào response."""

    return [
        {
            "question_id": 11,
            "choice_id": 3,
            "correct": True,
            "score": Decimal("2"),
        },
        {
            "question_id": 12,
            "choice_id": 5,
            "correct": False,
            "score": Decimal("0"),
        },
    ]


def test_validate_attempt_id_accepts_signed_int64_values() -> None:
    """Kiểm tra parser chấp nhận các giá trị trong miền signed int64 hiện tại."""

    from app.modules.guest.api_32_attempts_result.validate import validate_attempt_id

    assert validate_attempt_id("3201", trace_id="test-trace") == 3201
    assert validate_attempt_id(str(-(2**63)), trace_id="test-trace") == -(2**63)
    assert validate_attempt_id(str(2**63 - 1), trace_id="test-trace") == 2**63 - 1


@pytest.mark.parametrize(
    "raw_id",
    ["not-an-int", str(-(2**63) - 1), str(2**63)],
)
def test_validate_attempt_id_maps_unparseable_or_out_of_range_to_404(
    raw_id: str,
) -> None:
    """Kiểm tra path không parse được hoặc vượt miền int64 được ánh xạ thành 404."""

    from app.modules.guest.api_32_attempts_result.validate import validate_attempt_id

    response = validate_attempt_id(raw_id, trace_id="test-trace")

    assert isinstance(response, JSONResponse)
    assert response.status_code == 404
    assert b"DESIGN_RESOURCE_NOT_FOUND" in response.body


def test_build_attempt_result_only_exposes_question_id_and_graded_score() -> None:
    """Kiểm tra model chỉ mang question_id và điểm tổng của attempt GRADED."""

    result = attempt_view._build_attempt_result(attempt_row(), answer_rows())

    assert result.id == 3201
    assert result.quiz_id == 88
    assert result.status == "GRADED"
    assert result.started_at == attempt_row()["started_at"]
    assert result.submitted_at == attempt_row()["submitted_at"]
    assert str(result.score) == "87.50"
    assert [answer.question_id for answer in result.answers] == [11, 12]

    # Kiểm tra projection JSON thực tế sau khi bỏ các field có giá trị None.
    serialized = result.model_dump_json(exclude_none=True)
    assert "choice_id" not in serialized
    assert "is_correct" not in serialized
    assert "score_received" not in serialized


def test_build_attempt_result_omits_score_when_pending_grade() -> None:
    """Kiểm tra score không được đưa vào projection khi status là PENDING_GRADE."""

    result = attempt_view._build_attempt_result(
        attempt_row(status="PENDING_GRADE"),
        answer_rows(),
    )
    serialized = result.model_dump(mode="json", exclude_none=True)

    assert "score" not in serialized


def test_build_attempt_result_omits_none_optional_fields_when_serialized() -> None:
    """Kiểm tra field optional có giá trị None bị lược khỏi projection JSON."""

    result = attempt_view._build_attempt_result(
        attempt_row(status="GRADED", submitted_at=None, score=None),
        [],
    )

    assert result.submitted_at is None
    assert result.score is None
    assert result.answers == []

    serialized = result.model_dump(mode="json", exclude_none=True)
    assert "submitted_at" not in serialized
    assert "score" not in serialized
    assert serialized["answers"] == []


def test_get_attempt_result_returns_validator_error_without_query(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra response lỗi từ validator được trả nguyên trạng, không truy vấn dữ liệu."""

    expected = JSONResponse(
        status_code=401,
        content={
            "success": False,
            "businessCode": "DESIGN_AUTHENTICATION_REQUIRED",
        },
    )
    monkeypatch.setattr(
        attempt_view,
        "validate_attempt_result_request",
        lambda *args, **kwargs: expected,
    )
    monkeypatch.setattr(
        attempt_view,
        "find_attempt_result",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("request lỗi không được query")
        ),
    )

    response = attempt_view.get_attempt_result(
        authorization=None,
        attempt_id_raw="3201",
        db=FakeSession(),  # type: ignore[arg-type]
        trace_id="test-trace",
    )

    assert response is expected
    assert response.status_code == 401


def test_get_attempt_result_not_found_returns_404(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra attempt không tìm thấy theo lookup hiện tại trả về 404."""

    monkeypatch.setattr(
        attempt_view,
        "validate_attempt_result_request",
        lambda *args, **kwargs: (501, 3201),
    )
    monkeypatch.setattr(
        attempt_view,
        "find_attempt_result",
        lambda *args, **kwargs: None,
    )

    response = attempt_view.get_attempt_result(
        authorization="Bearer test-token",
        attempt_id_raw="3201",
        db=FakeSession(),  # type: ignore[arg-type]
        trace_id="test-trace",
    )

    assert isinstance(response, JSONResponse)
    assert response.status_code == 404
    assert b"DESIGN_RESOURCE_NOT_FOUND" in response.body


def test_get_attempt_result_success_returns_safe_envelope(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra envelope thành công giữ trace ID và không lộ field answer nhạy cảm."""

    monkeypatch.setattr(
        attempt_view,
        "validate_attempt_result_request",
        lambda *args, **kwargs: (501, 3201),
    )
    monkeypatch.setattr(
        attempt_view,
        "find_attempt_result",
        lambda db, *, attempt_id, user_id: attempt_row(),
    )
    monkeypatch.setattr(
        attempt_view,
        "find_attempt_answers",
        lambda db, *, attempt_id, user_id: answer_rows(),
    )

    response = attempt_view.get_attempt_result(
        authorization="Bearer test-token",
        attempt_id_raw="3201",
        db=FakeSession(),  # type: ignore[arg-type]
        trace_id="test-trace",
    )

    assert isinstance(response, dict)
    assert response["success"] is True
    assert response["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert response["traceId"] == "test-trace"
    assert response["data"]["score"] == "87.50"
    assert response["data"]["answers"] == [
        {"question_id": 11},
        {"question_id": 12},
    ]
    assert "choice_id" not in str(response["data"])
    assert "correct" not in str(response["data"])
    assert "score_received" not in str(response["data"])


def test_get_attempt_result_rolls_back_on_attempt_query_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra lỗi SQL khi đọc attempt rollback session và trả lỗi nội bộ an toàn."""

    session = FakeSession()
    monkeypatch.setattr(
        attempt_view,
        "validate_attempt_result_request",
        lambda *args, **kwargs: (501, 3201),
    )
    monkeypatch.setattr(
        attempt_view,
        "find_attempt_result",
        lambda *args, **kwargs: (_ for _ in ()).throw(SQLAlchemyError("database unavailable")),
    )

    response = attempt_view.get_attempt_result(
        authorization="Bearer test-token",
        attempt_id_raw="3201",
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )

    assert isinstance(response, JSONResponse)
    assert response.status_code == 500
    assert b"DESIGN_INTERNAL_ERROR" in response.body
    assert b"database unavailable" not in response.body
    assert session.rollback_count == 1


def test_get_attempt_result_rolls_back_on_answers_query_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra lỗi SQL khi đọc answers rollback session và không lộ chi tiết database."""

    session = FakeSession()
    monkeypatch.setattr(
        attempt_view,
        "validate_attempt_result_request",
        lambda *args, **kwargs: (501, 3201),
    )
    monkeypatch.setattr(
        attempt_view,
        "find_attempt_result",
        lambda db, *, attempt_id, user_id: attempt_row(),
    )
    monkeypatch.setattr(
        attempt_view,
        "find_attempt_answers",
        lambda *args, **kwargs: (_ for _ in ()).throw(SQLAlchemyError("database unavailable")),
    )

    response = attempt_view.get_attempt_result(
        authorization="Bearer test-token",
        attempt_id_raw="3201",
        db=session,  # type: ignore[arg-type]
        trace_id="test-trace",
    )

    assert isinstance(response, JSONResponse)
    assert response.status_code == 500
    assert b"DESIGN_INTERNAL_ERROR" in response.body
    assert b"database unavailable" not in response.body
    assert session.rollback_count == 1


def test_get_attempt_result_maps_malformed_row_to_safe_internal_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra row thiếu field bắt buộc thành lỗi nội bộ, không làm lộ exception."""

    monkeypatch.setattr(
        attempt_view,
        "validate_attempt_result_request",
        lambda *args, **kwargs: (501, 3201),
    )
    monkeypatch.setattr(
        attempt_view,
        "find_attempt_result",
        lambda db, *, attempt_id, user_id: {"id": 3201},
    )
    monkeypatch.setattr(
        attempt_view,
        "find_attempt_answers",
        lambda *args, **kwargs: [],
    )

    response = attempt_view.get_attempt_result(
        authorization="Bearer test-token",
        attempt_id_raw="3201",
        db=FakeSession(),  # type: ignore[arg-type]
        trace_id="test-trace",
    )

    assert isinstance(response, JSONResponse)
    assert response.status_code == 500
    assert b"DESIGN_INTERNAL_ERROR" in response.body


def test_attempt_result_queries_bind_attempt_and_user_ids() -> None:
    """Kiểm tra SQL bind ID và giới hạn truy vấn theo user đã xác thực."""

    attempt_sql = " ".join(ATTEMPT_RESULT_BY_ID.lower().split())
    answers_sql = " ".join(ATTEMPT_ANSWERS_BY_ID.lower().split())

    assert ":attempt_id" in attempt_sql
    assert ":user_id" in attempt_sql
    assert "user_id = :user_id" in attempt_sql

    assert ":attempt_id" in answers_sql
    assert ":user_id" in answers_sql
    assert "user_id = :user_id" in answers_sql
    assert "3201" not in attempt_sql
    assert "3201" not in answers_sql
    assert "quiz_choices" not in answers_sql
