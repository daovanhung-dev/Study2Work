"""Xử lý nghiệp vụ và điều phối dữ liệu cho API #30 autosave/lưu câu trả lời."""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.guest.api_30_attempts_answers.models import (
    QuizAnswerItem,
    QuizAttemptDetail,
    SaveAnswerRequest,
)
from app.modules.guest.api_30_attempts_answers.query import (
    FIND_ATTEMPT_ANSWERS,
    FIND_ATTEMPT_BY_ID,
    FIND_EXISTING_ANSWER,
    FIND_QUESTION_BY_ID,
    INSERT_ANSWER,
    UPDATE_ANSWER,
)
from app.modules.guest.api_30_attempts_answers.validate import (
    access_denied,
    resource_not_found,
    validate_save_answer_request,
)
from pydantic import ValidationError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def parse_choice_id(answer_raw: Any) -> int | None:
    """Trích xuất ID lựa chọn nếu câu trả lời truyền lên dạng số hợp lệ."""
    if answer_raw is None:
        return None
    try:
        val = int(str(answer_raw).strip())
        return val if val > 0 else None
    except (TypeError, ValueError):
        return None


def format_iso_timestamp(ts: Any) -> str:
    """Chuyển đổi đối tượng thời gian thành chuỗi định dạng ISO 8601 chuẩn."""
    if isinstance(ts, datetime):
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=UTC)
        return ts.isoformat()
    return str(ts)


def find_attempt(db: Session, *, attempt_id: int) -> dict[str, Any] | None:
    """Truy vấn thông tin lượt làm bài theo attempt_id."""
    return query_one(db, FIND_ATTEMPT_BY_ID, {"attempt_id": attempt_id})


def find_question(db: Session, *, question_id: int) -> dict[str, Any] | None:
    """Truy vấn thông tin câu hỏi theo question_id."""
    return query_one(db, FIND_QUESTION_BY_ID, {"question_id": question_id})


def find_existing_answer(
    db: Session,
    *,
    attempt_id: int,
    question_id: int,
) -> dict[str, Any] | None:
    """Truy vấn kiểm tra xem câu hỏi đã có câu trả lời nào được lưu trước đó hay chưa."""
    return query_one(
        db,
        FIND_EXISTING_ANSWER,
        {"attempt_id": attempt_id, "question_id": question_id},
    )


def upsert_answer(
    db: Session,
    *,
    attempt_id: int,
    question_id: int,
    choice_id: int | None,
) -> None:
    """Cập nhật câu trả lời nếu đã tồn tại hoặc tạo mới nếu chưa có (UPSERT)."""
    existing = find_existing_answer(db, attempt_id=attempt_id, question_id=question_id)
    if existing is not None:
        db.execute(
            text(UPDATE_ANSWER),
            {"choice_id": choice_id, "answer_id": existing["id"]},
        )
    else:
        db.execute(
            text(INSERT_ANSWER),
            {
                "attempt_id": attempt_id,
                "question_id": question_id,
                "choice_id": choice_id,
            },
        )


def find_attempt_answers(db: Session, *, attempt_id: int) -> list[dict[str, Any]]:
    """Truy vấn tất cả các câu trả lời hiện có của lượt làm bài."""
    return query_many(db, FIND_ATTEMPT_ANSWERS, {"attempt_id": attempt_id})


# API #30 attempts_answers
def save_attempt_answer(
    *,
    authorization: str | None,
    attempt_id_raw: str | int,
    payload: SaveAnswerRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực học viên, kiểm tra quyền sở hữu attempt, lưu câu trả lời và trả về attempt."""
    # Xác thực quyền Student và kiểm tra tính hợp lệ của attempt_id và question_id
    validation = validate_save_answer_request(
        authorization=authorization,
        attempt_id_raw=attempt_id_raw,
        question_id_raw=payload.question_id,
        trace_id=trace_id,
    )
    if isinstance(validation, JSONResponse):
        return validation
    user_id, attempt_id, question_id = validation

    try:
        # Kiểm tra sự tồn tại của lượt làm bài (attempt)
        attempt = find_attempt(db, attempt_id=attempt_id)
        if attempt is None:
            return resource_not_found(trace_id, message="Attempt not found")

        # Kiểm tra quyền sở hữu: học viên chỉ được lưu câu trả lời vào attempt của chính mình
        if attempt.get("user_id") != user_id:
            return access_denied(trace_id, message="Access denied to this attempt")

        # Kiểm tra trạng thái: chỉ được lưu câu trả lời khi attempt đang trong tiến trình
        if attempt.get("status") != "IN_PROGRESS":
            return access_denied(
                trace_id,
                message="Attempt is closed or already submitted",
            )

        # Kiểm tra câu hỏi có tồn tại và thuộc cùng bài quiz của attempt hay không
        question = find_question(db, question_id=question_id)
        if question is None or question.get("quiz_id") != attempt.get("quiz_id"):
            return resource_not_found(
                trace_id,
                message="Question not found in quiz",
            )

        # Trích xuất choice_id và thực hiện ghi hoặc cập nhật (UPSERT)
        choice_id = parse_choice_id(payload.answer)
        upsert_answer(
            db,
            attempt_id=attempt_id,
            question_id=question_id,
            choice_id=choice_id,
        )

        # Xác nhận transaction ghi dữ liệu
        db.commit()

        # Truy vấn danh sách toàn bộ câu trả lời hiện có của attempt để trả về cho client
        answer_rows = find_attempt_answers(db, attempt_id=attempt_id)
        answers: list[QuizAnswerItem] = []
        for row in answer_rows:
            c_id = row.get("choice_id")
            choice_ids = [c_id] if c_id is not None else []
            answers.append(
                QuizAnswerItem(
                    question_id=row["question_id"],
                    choice_ids=choice_ids,
                    text_answer=None,
                )
            )

        # Ánh xạ thành model QuizAttemptDetail theo contract
        attempt_detail = QuizAttemptDetail(
            id=attempt["id"],
            quiz_id=attempt["quiz_id"],
            status=attempt.get("status", "IN_PROGRESS"),
            started_at=format_iso_timestamp(attempt["started_at"]),
            submitted_at=attempt.get("submitted_at"),
            score=attempt.get("score"),
            answers=answers,
        )
    except SQLAlchemyError:
        # Rollback giao dịch khi xảy ra lỗi database và ghi log
        db.rollback()
        logger.exception("Save attempt answer failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    except (ValidationError, ValueError):
        # Ghi log khi việc ánh xạ model gặp lỗi
        logger.exception("Attempt mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả về kết quả thành công HTTP 200 bọc trong ApiEnvelope chuẩn
    return success_response(
        business_code="DESIGN_RESOURCE_UPDATED",
        message="Answer saved",
        trace_id=trace_id,
        data=attempt_detail.model_dump(mode="json"),
    )


def _internal_error(trace_id: str) -> JSONResponse:
    """Tạo response lỗi 500 chuẩn khi truy vấn database hoặc lưu dữ liệu thất bại."""
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Internal server error",
        trace_id=trace_id,
    )
