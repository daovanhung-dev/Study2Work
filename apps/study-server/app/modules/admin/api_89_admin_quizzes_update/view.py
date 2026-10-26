"""Điều phối khóa, kiểm tra lịch sử, thay Quiz cùng question set cho API #89."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from decimal import Decimal, InvalidOperation
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import ErrorDetail, error_response, success_response
from app.modules.admin.api_88_admin_quizzes_create.models import (
    AdminQuizChoiceResponse,
    AdminQuizQuestionResponse,
    CreateAdminQuizData,
    CreateAdminQuizInput,
)
from app.modules.admin.api_88_admin_quizzes_create.query import (
    INSERT_ADMIN_QUIZ_CHOICE,
    INSERT_ADMIN_QUIZ_QUESTION,
)
from app.modules.admin.api_89_admin_quizzes_update.query import (
    CHECK_ADMIN_QUIZ_HISTORY,
    DELETE_ADMIN_QUIZ_CHOICES,
    DELETE_ADMIN_QUIZ_QUESTIONS,
    LOCK_ADMIN_QUIZ,
    LOCK_ADMIN_QUIZ_CHOICES,
    LOCK_ADMIN_QUIZ_COURSE,
    LOCK_ADMIN_QUIZ_QUESTIONS,
    UPDATE_ADMIN_QUIZ,
)
from app.modules.admin.api_89_admin_quizzes_update.validate import (
    validate_admin_quiz_update_request,
)
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
MAX_INT64 = 2**63 - 1


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn cho query, projection hoặc transaction."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Quiz could not be updated.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 cho Quiz không tồn tại hoặc đã được đánh dấu DELETED."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Quiz not found.",
        trace_id=trace_id,
    )


def _history_conflict(trace_id: str) -> JSONResponse:
    """Dựng lỗi 422 khi attempts hoặc answers đang tham chiếu lịch sử Quiz."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Quiz có lịch sử làm bài và không thể thay question set.",
        trace_id=trace_id,
        errors=[
            ErrorDetail(
                field="quiz_id",
                code="RESOURCE_HAS_HISTORY",
                message="Quiz có attempt hoặc answer đã được lưu.",
            )
        ],
    )


def _course_not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 422 catalog khi Course đích không tồn tại."""

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
    """Hủy transaction đang cập nhật mà không che response lỗi ban đầu."""

    try:
        # Hoàn tác parent hoặc child write nếu transaction chưa commit.
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin quiz update rollback failed; trace_id=%s", trace_id)


def _valid_id(value: Any) -> bool:
    """Xác nhận ID trả về là số nguyên dương trong miền BIGSERIAL/int64."""

    return type(value) is int and 1 <= value <= MAX_INT64


def _locked_ids(rows: Any) -> list[int] | None:
    """Kiểm tra danh sách hàng khóa và trả về ID duy nhất theo DB order."""

    if not isinstance(rows, list):
        return None
    identifiers: list[int] = []
    for row in rows:
        if not isinstance(row, Mapping) or not _valid_id(row.get("id")):
            return None
        identifiers.append(row["id"])
    if len(set(identifiers)) != len(identifiers):
        return None
    return identifiers


def _returned_ids_match(rows: Any, expected_ids: list[int]) -> bool:
    """Xác nhận DELETE RETURNING đúng tập ID đã khóa trước đó."""

    actual_ids = _locked_ids(rows)
    return (
        actual_ids is not None
        and set(actual_ids) == set(expected_ids)
        and len(actual_ids) == len(expected_ids)
    )


def _decimal_string(value: Any) -> str | None:
    """Chuyển numeric hữu hạn từ DB sang decimal string không dùng exponent."""

    if value is None or isinstance(value, bool):
        return None
    try:
        decimal_value = Decimal(str(value))
    except InvalidOperation:
        return None
    if not decimal_value.is_finite():
        return None
    return format(decimal_value, "f")


def _map_choice(
    row: Mapping[str, Any],
    *,
    question_id: int,
    requested_text: str,
    requested_is_correct: bool,
    requested_order: int,
) -> AdminQuizChoiceResponse | None:
    """Xác thực generated Choice row và tạo response answer-key cho Admin."""

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


def _map_question_set(
    db: Session,
    *,
    quiz_id: int,
    request: CreateAdminQuizInput,
    trace_id: str,
) -> list[AdminQuizQuestionResponse] | None:
    """Insert ordered replacement questions/choices and validate their response rows."""

    questions: list[AdminQuizQuestionResponse] = []
    for question_order, question_input in enumerate(request.questions):
        # Chèn câu hỏi theo input order và nhận generated ID để gắn các choices.
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
        if not isinstance(question_row, Mapping):
            logger.error("Admin quiz question insert projection missing; trace_id=%s", trace_id)
            return None
        question_id = question_row.get("id")
        if (
            not _valid_id(question_id)
            or type(question_row.get("quiz_id")) is not int
            or question_row.get("quiz_id") != quiz_id
            or question_row.get("text") != question_input.text
            or question_row.get("type") != question_input.type
            or type(question_row.get("sort_order")) is not int
            or question_row.get("sort_order") != question_order
        ):
            logger.error("Admin quiz question projection invalid; trace_id=%s", trace_id)
            return None

        choices: list[AdminQuizChoiceResponse] = []
        for choice_order, choice_input in enumerate(question_input.choices):
            # Ghi choices cùng question và giữ thứ tự đầu vào trong transaction.
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
            if not isinstance(choice_row, Mapping):
                logger.error("Admin quiz choice insert projection missing; trace_id=%s", trace_id)
                return None
            choice = _map_choice(
                choice_row,
                question_id=question_id,
                requested_text=choice_input.text,
                requested_is_correct=choice_input.is_correct,
                requested_order=choice_order,
            )
            if choice is None:
                logger.error("Admin quiz choice projection invalid; trace_id=%s", trace_id)
                return None
            choices.append(choice)

        try:
            questions.append(
                AdminQuizQuestionResponse(
                    id=question_id,
                    text=question_input.text,
                    type=question_input.type,
                    choices=choices,
                )
            )
        except (TypeError, ValidationError):
            return None
    return questions


def _map_quiz(
    row: Mapping[str, Any],
    *,
    quiz_id: int,
    request: CreateAdminQuizInput,
    questions: list[AdminQuizQuestionResponse],
) -> CreateAdminQuizData | None:
    """Validate updated parent projection and build the complete Quiz response."""

    duration = row.get("duration_minutes")
    passing_score = _decimal_string(row.get("passing_score"))
    try:
        stored_score = Decimal(passing_score) if passing_score is not None else None
        requested_score = Decimal(request.config.passing_score)
    except InvalidOperation:
        return None
    if (
        not _valid_id(row.get("id"))
        or row.get("id") != quiz_id
        or row.get("course_id") != request.config.course_id
        or row.get("title") != request.config.title
        or duration != request.config.duration_minutes
        or (duration is not None and type(duration) is not int)
        or stored_score is None
        or stored_score != requested_score
    ):
        return None
    try:
        return CreateAdminQuizData(
            id=quiz_id,
            course_id=request.config.course_id,
            title=request.config.title,
            duration_minutes=duration,
            passing_score=passing_score,
            questions=questions,
        )
    except (TypeError, ValidationError):
        return None


def update_admin_quiz(
    *,
    authorization: str | None,
    quiz_id_value: str,
    raw_body: bytes,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Authenticate Admin and atomically replace an unattempted Quiz and its question set."""

    # Xác thực ADMIN và kiểm tra raw path/body trước khi bắt đầu truy vấn.
    validated = validate_admin_quiz_update_request(
        authorization,
        quiz_id_value,
        raw_body,
        trace_id=trace_id,
    )
    if isinstance(validated, JSONResponse):
        return validated
    quiz_id, request = validated

    try:
        # Khóa parent Quiz rồi khóa child rows theo ID ổn định trước history check.
        quiz_row = query_one(db, LOCK_ADMIN_QUIZ, {"quiz_id": quiz_id})
        if quiz_row is None:
            _rollback_safely(db, trace_id=trace_id)
            return _not_found(trace_id)
        if not isinstance(quiz_row, Mapping) or quiz_row.get("id") != quiz_id or not _valid_id(
            quiz_row.get("id")
        ):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin quiz lock projection invalid; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        if quiz_row.get("status") == "DELETED":
            _rollback_safely(db, trace_id=trace_id)
            return _not_found(trace_id)

        question_ids = _locked_ids(
            query_many(db, LOCK_ADMIN_QUIZ_QUESTIONS, {"quiz_id": quiz_id})
        )
        choice_ids = _locked_ids(
            query_many(db, LOCK_ADMIN_QUIZ_CHOICES, {"quiz_id": quiz_id})
        )
        if question_ids is None or choice_ids is None:
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin quiz child lock projection invalid; trace_id=%s", trace_id)
            return _internal_error(trace_id)

        # Chặn thay ID đã được tham chiếu trước khi chạm vào bất kỳ hàng nào.
        history = query_one(db, CHECK_ADMIN_QUIZ_HISTORY, {"quiz_id": quiz_id})
        if (
            not isinstance(history, Mapping)
            or type(history.get("has_attempts")) is not bool
            or type(history.get("has_answers")) is not bool
        ):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin quiz history projection invalid; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        if history["has_attempts"] or history["has_answers"]:
            _rollback_safely(db, trace_id=trace_id)
            return _history_conflict(trace_id)

        # Khóa Course đích để xác nhận FK candidate còn tồn tại khi cập nhật parent.
        course_row = query_one(
            db,
            LOCK_ADMIN_QUIZ_COURSE,
            {"course_id": request.config.course_id},
        )
        if course_row is None:
            _rollback_safely(db, trace_id=trace_id)
            return _course_not_found(trace_id)
        if (
            not isinstance(course_row, Mapping)
            or course_row.get("id") != request.config.course_id
            or not _valid_id(course_row.get("id"))
        ):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin quiz Course projection invalid; trace_id=%s", trace_id)
            return _internal_error(trace_id)

        # Chỉ cập nhật field thuộc config; giữ status, description và created_at.
        updated_row = query_one(
            db,
            UPDATE_ADMIN_QUIZ,
            {
                "quiz_id": quiz_id,
                "course_id": request.config.course_id,
                "title": request.config.title,
                "passing_score": request.config.passing_score,
                "duration_minutes": request.config.duration_minutes,
            },
        )
        if not isinstance(updated_row, Mapping):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin quiz update returned no projection; trace_id=%s", trace_id)
            return _internal_error(trace_id)

        # Xóa Choices trước Questions và xác nhận không còn sai lệch giữa lock/delete.
        deleted_choice_rows = query_many(
            db,
            DELETE_ADMIN_QUIZ_CHOICES,
            {"quiz_id": quiz_id},
        )
        if not _returned_ids_match(deleted_choice_rows, choice_ids):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin quiz Choice delete projection mismatch; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        deleted_question_rows = query_many(
            db,
            DELETE_ADMIN_QUIZ_QUESTIONS,
            {"quiz_id": quiz_id},
        )
        if not _returned_ids_match(deleted_question_rows, question_ids):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin quiz Question delete projection mismatch; trace_id=%s", trace_id)
            return _internal_error(trace_id)

        # Ghi child set mới theo thứ tự request và kiểm tra toàn bộ Quiz trước commit.
        questions = _map_question_set(
            db,
            quiz_id=quiz_id,
            request=request,
            trace_id=trace_id,
        )
        if questions is None:
            _rollback_safely(db, trace_id=trace_id)
            return _internal_error(trace_id)
        quiz = _map_quiz(
            updated_row,
            quiz_id=quiz_id,
            request=request,
            questions=questions,
        )
        if quiz is None:
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin quiz response projection invalid; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        response_data = quiz.model_dump(mode="json", exclude_none=True)
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin quiz update query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    try:
        # Chỉ commit sau khi parent, deletes, inserts và response mapping đều hoàn tất.
        db.commit()
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin quiz update commit failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả model Quiz vừa kiểm tra với business code update trong catalog.
    return success_response(
        data=response_data,
        business_code="DESIGN_RESOURCE_UPDATED",
        message="Quiz updated successfully.",
        trace_id=trace_id,
    )
