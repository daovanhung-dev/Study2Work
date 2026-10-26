"""Điều phối quyền Admin, ghi Quiz cùng children và dựng response API #88."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from decimal import Decimal, InvalidOperation
from typing import Any

from app.core.database import query_one
from app.core.responses import ErrorDetail, error_response, success_response
from app.modules.admin.api_88_admin_quizzes_create.models import (
    AdminQuizChoiceResponse,
    AdminQuizQuestionResponse,
    CreateAdminQuizData,
    CreateAdminQuizInput,
)
from app.modules.admin.api_88_admin_quizzes_create.query import (
    INSERT_ADMIN_QUIZ,
    INSERT_ADMIN_QUIZ_CHOICE,
    INSERT_ADMIN_QUIZ_QUESTION,
    SELECT_ADMIN_QUIZ_COURSE,
)
from app.modules.admin.api_88_admin_quizzes_create.validate import (
    validate_create_admin_quiz_request,
)
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
MAX_INT64 = 2**63 - 1


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn cho query, insert, mapping hoặc commit."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Quiz could not be created.",
        trace_id=trace_id,
    )


def _course_not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 422 theo catalog khi course reference không tồn tại."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Dữ liệu đầu vào không hợp lệ.",
        trace_id=trace_id,
        errors=[
            ErrorDetail(
                field="config.course_id",
                code="RESOURCE_NOT_FOUND",
                message="Course không tồn tại.",
            )
        ],
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction mà không làm thay đổi response lỗi ban đầu."""

    try:
        # Dọn mọi row đã insert trước khi request dependency đóng Session.
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin quiz create rollback failed; trace_id=%s", trace_id)


def _decimal_string(value: Any) -> str | None:
    """Chuyển giá trị numeric hữu hạn thành chuỗi thập phân không dùng exponent."""

    if value is None or isinstance(value, bool):
        return None
    try:
        decimal_value = Decimal(str(value))
    except InvalidOperation:
        return None
    if not decimal_value.is_finite():
        return None
    return format(decimal_value, "f")


def _valid_id(value: Any) -> bool:
    """Xác nhận ID database là số nguyên dương trong miền BIGSERIAL/int64."""

    return type(value) is int and 1 <= value <= MAX_INT64


def _map_choice_row(
    row: Mapping[str, Any],
    *,
    question_id: int,
    requested_text: str,
    requested_is_correct: bool,
    requested_order: int,
) -> AdminQuizChoiceResponse | None:
    """Kiểm tra INSERT/RETURNING của Choice rồi dựng projection Admin cục bộ."""

    choice_id = row.get("id")
    if (
        not _valid_id(choice_id)
        or type(row.get("question_id")) is not int
        or row.get("question_id") != question_id
        or row.get("text") != requested_text
        or type(row.get("is_correct")) is not bool
        or row.get("is_correct") is not requested_is_correct
        or type(row.get("sort_order")) is not int
        or row.get("sort_order") != requested_order
    ):
        return None
    try:
        return AdminQuizChoiceResponse(
            id=choice_id,
            text=requested_text,
            is_correct=requested_is_correct,
        )
    except (TypeError, ValidationError):
        return None


def _map_question_row(
    row: Mapping[str, Any],
    *,
    quiz_id: int,
    requested_question: Any,
    requested_order: int,
    db: Session,
    trace_id: str,
) -> AdminQuizQuestionResponse | None:
    """Ghi choices theo thứ tự request rồi xác minh projection Question được trả về."""

    question_id = row.get("id")
    question_type = row.get("type")
    if (
        not _valid_id(question_id)
        or type(row.get("quiz_id")) is not int
        or row.get("quiz_id") != quiz_id
        or row.get("text") != requested_question.text
        or not isinstance(question_type, str)
        or question_type != requested_question.type
        or type(row.get("sort_order")) is not int
        or row.get("sort_order") != requested_order
    ):
        return None

    choices: list[AdminQuizChoiceResponse] = []
    for choice_order, choice_input in enumerate(requested_question.choices):
        try:
            # Ghi một lựa chọn và lấy ID ngay trong transaction tạo Quiz.
            choice_row = query_one(
                db,
                INSERT_ADMIN_QUIZ_CHOICE,
                {
                    "question_id": question_id,
                    "text": choice_input.text,
                    "is_correct": choice_input.is_correct,
                    "sort_order": choice_order,
                },
            )
        except SQLAlchemyError:
            logger.error("Admin quiz choice insert failed; trace_id=%s", trace_id)
            return None
        if not isinstance(choice_row, Mapping):
            logger.error("Admin quiz choice mapping failed; trace_id=%s", trace_id)
            return None
        choice = _map_choice_row(
            choice_row,
            question_id=question_id,
            requested_text=choice_input.text,
            requested_is_correct=choice_input.is_correct,
            requested_order=choice_order,
        )
        if choice is None:
            logger.error("Admin quiz choice projection failed; trace_id=%s", trace_id)
            return None
        choices.append(choice)

    try:
        return AdminQuizQuestionResponse(
            id=question_id,
            text=requested_question.text,
            type=question_type,
            choices=choices,
        )
    except (TypeError, ValidationError):
        return None


def _map_quiz_row(
    row: Mapping[str, Any],
    *,
    request: CreateAdminQuizInput,
    db: Session,
    trace_id: str,
) -> CreateAdminQuizData | None:
    """Ghi question/choice rows rồi xác thực toàn bộ Quiz response projection."""

    quiz_id = row.get("id")
    config = request.config
    duration_minutes = row.get("duration_minutes")
    passing_score = _decimal_string(row.get("passing_score"))
    try:
        requested_score = Decimal(config.passing_score)
        stored_score = Decimal(passing_score) if passing_score is not None else None
    except InvalidOperation:
        return None
    if (
        not _valid_id(quiz_id)
        or row.get("course_id") != config.course_id
        or row.get("title") != config.title
        or duration_minutes != config.duration_minutes
        or (duration_minutes is not None and type(duration_minutes) is not int)
        or stored_score is None
        or stored_score != requested_score
    ):
        return None

    questions: list[AdminQuizQuestionResponse] = []
    for question_order, question_input in enumerate(request.questions):
        try:
            # Ghi câu hỏi theo đúng index mảng và đọc projection có generated ID.
            question_row = query_one(
                db,
                INSERT_ADMIN_QUIZ_QUESTION,
                {
                    "quiz_id": quiz_id,
                    "text": question_input.text,
                    "question_type": question_input.type,
                    "sort_order": question_order,
                },
            )
        except SQLAlchemyError:
            logger.error("Admin quiz question insert failed; trace_id=%s", trace_id)
            return None
        if not isinstance(question_row, Mapping):
            logger.error("Admin quiz question mapping failed; trace_id=%s", trace_id)
            return None
        question = _map_question_row(
            question_row,
            quiz_id=quiz_id,
            requested_question=question_input,
            requested_order=question_order,
            db=db,
            trace_id=trace_id,
        )
        if question is None:
            return None
        questions.append(question)

    try:
        return CreateAdminQuizData(
            id=quiz_id,
            course_id=config.course_id,
            title=config.title,
            duration_minutes=duration_minutes,
            passing_score=passing_score,
            questions=questions,
        )
    except (TypeError, ValidationError):
        return None


# API #88 admin_quizzes_create
def create_admin_quiz(
    *,
    authorization: str | None,
    raw_body: bytes,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Admin, kiểm tra request và tạo Quiz cùng toàn bộ children atomically."""

    # Xác thực role ADMIN trước khi parse body hoặc truy cập database.
    authentication = validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Quiz could not be created.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication

    # Chỉ chấp nhận embedded schema DERIVED sau khi đã xác thực access token.
    validated_request = validate_create_admin_quiz_request(raw_body, trace_id=trace_id)
    if isinstance(validated_request, JSONResponse):
        return validated_request

    try:
        # Kiểm tra Course trước khi ghi Quiz; course_id cũng được bảo vệ bởi DB FK candidate.
        course_row = query_one(
            db,
            SELECT_ADMIN_QUIZ_COURSE,
            {"course_id": validated_request.config.course_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin quiz course lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if course_row is None:
        _rollback_safely(db, trace_id=trace_id)
        return _course_not_found(trace_id)
    if (
        not isinstance(course_row, Mapping)
        or type(course_row.get("id")) is not int
        or course_row.get("id") != validated_request.config.course_id
    ):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin quiz course projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    try:
        # Tạo parent Quiz và lấy các giá trị đã lưu để dựng response contract.
        quiz_row = query_one(
            db,
            INSERT_ADMIN_QUIZ,
            {
                "course_id": validated_request.config.course_id,
                "title": validated_request.config.title,
                "passing_score": validated_request.config.passing_score,
                "duration_minutes": validated_request.config.duration_minutes,
            },
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin quiz insert failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if not isinstance(quiz_row, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin quiz insert returned no projection; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Ghi question/choice rows, xác minh response mapping rồi mới commit.
    quiz = _map_quiz_row(
        quiz_row,
        request=validated_request,
        db=db,
        trace_id=trace_id,
    )
    if quiz is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin quiz response projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    response_data = quiz.model_dump(mode="json", exclude_none=True)

    try:
        # Chỉ lưu transaction sau khi parent và toàn bộ nested response hợp lệ.
        db.commit()
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin quiz create commit failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả Quiz đầy đủ cùng business code tạo resource trong catalog.
    return success_response(
        business_code="DESIGN_RESOURCE_CREATED",
        message="Quiz created.",
        trace_id=trace_id,
        data=response_data,
    )
