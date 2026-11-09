"""Xử lý nghiệp vụ và điều phối dữ liệu cho API #28 lấy chi tiết bài quiz và danh sách câu hỏi."""

from __future__ import annotations

import logging
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.guest.api_28_quizzes_detail.models import (
    QuizChoiceItem,
    QuizDetail,
    QuizQuestionItem,
)
from app.modules.guest.api_28_quizzes_detail.query import (
    FIND_QUIZ_BY_ID,
    FIND_QUIZ_CHOICES,
    FIND_QUIZ_QUESTIONS,
)
from app.modules.guest.api_28_quizzes_detail.validate import (
    quiz_not_found,
    validate_quiz_detail_request,
)
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def format_decimal(value: Any) -> str:
    """Chuyển đổi giá trị số thành chuỗi định dạng thập phân (decimal-string)."""
    if value is None:
        return "0.00"
    try:
        dec = Decimal(str(value))
        return f"{dec:.2f}"
    except (InvalidOperation, TypeError, ValueError):
        return "0.00"


def find_quiz_by_id(db: Session, *, quiz_id: int) -> dict[str, Any] | None:
    """Truy vấn thông tin cơ bản của bài quiz theo quiz_id."""
    return query_one(db, FIND_QUIZ_BY_ID, {"quiz_id": quiz_id})


def find_quiz_questions(db: Session, *, quiz_id: int) -> list[dict[str, Any]]:
    """Truy vấn danh sách câu hỏi thuộc quiz theo thứ tự hiển thị sort_order."""
    return query_many(db, FIND_QUIZ_QUESTIONS, {"quiz_id": quiz_id})


def find_quiz_choices(db: Session, *, quiz_id: int) -> list[dict[str, Any]]:
    """Truy vấn danh sách các lựa chọn câu hỏi (không lấy trường is_correct để bảo mật)."""
    return query_many(db, FIND_QUIZ_CHOICES, {"quiz_id": quiz_id})


# API #28 quizzes_detail
def get_quiz_detail(
    *,
    authorization: str | None,
    quiz_id_raw: str | int,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Student, truy vấn metadata quiz, tập câu hỏi và lựa chọn rồi trả về chi tiết."""
    # Xác thực quyền Student và kiểm tra tính hợp lệ của path parameter quiz_id
    validation = validate_quiz_detail_request(
        authorization=authorization,
        quiz_id_raw=quiz_id_raw,
        trace_id=trace_id,
    )
    if isinstance(validation, JSONResponse):
        return validation
    _user_id, quiz_id = validation

    try:
        # Truy vấn thông tin bài quiz trong database
        quiz_row = find_quiz_by_id(db, quiz_id=quiz_id)
        if quiz_row is None:
            return quiz_not_found(trace_id, message="Quiz not found")

        # Truy vấn danh sách câu hỏi và danh sách lựa chọn của quiz
        question_rows = find_quiz_questions(db, quiz_id=quiz_id)
        choice_rows = find_quiz_choices(db, quiz_id=quiz_id)

        # Nhóm các lựa chọn theo question_id tương ứng
        choices_by_question: dict[int, list[QuizChoiceItem]] = defaultdict(list)
        for choice_row in choice_rows:
            q_id = choice_row["question_id"]
            choices_by_question[q_id].append(
                QuizChoiceItem(
                    id=choice_row["id"],
                    choice_text=choice_row["choice_text"],
                )
            )

        # Xây dựng danh sách câu hỏi kèm theo các lựa chọn đáp án
        questions: list[QuizQuestionItem] = []
        for q_row in question_rows:
            q_id = q_row["id"]
            questions.append(
                QuizQuestionItem(
                    id=q_id,
                    text=q_row["text"],
                    type="MULTIPLE_CHOICE",
                    choices=choices_by_question.get(q_id, []),
                )
            )

        # Ánh xạ thành model QuizDetail chuẩn theo contract
        quiz_detail = QuizDetail(
            id=quiz_row["id"],
            course_id=quiz_row["course_id"],
            title=quiz_row["title"],
            duration_minutes=quiz_row.get("duration_minutes"),
            passing_score=format_decimal(quiz_row.get("passing_score")),
            questions=questions,
        )
    except SQLAlchemyError:
        # Rollback giao dịch nếu có lỗi database và ghi log
        db.rollback()
        logger.exception("Quiz detail lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    except (ValidationError, ValueError):
        # Ghi log khi việc ánh xạ model hoặc dữ liệu gặp lỗi
        logger.exception("Quiz detail mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả về response thành công bọc trong ApiEnvelope chuẩn
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Quiz detail retrieved",
        trace_id=trace_id,
        data=quiz_detail.model_dump(mode="json"),
    )


def _internal_error(trace_id: str) -> JSONResponse:
    """Tạo response lỗi 500 chuẩn khi truy vấn database hoặc ánh xạ model thất bại."""
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Internal server error",
        trace_id=trace_id,
    )
