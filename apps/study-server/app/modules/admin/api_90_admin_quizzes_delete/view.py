"""Điều phối authorization, history policy và transaction xóa Quiz API #90."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from datetime import datetime
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.admin.api_90_admin_quizzes_delete.models import DeleteResult
from app.modules.admin.api_90_admin_quizzes_delete.query import (
    CHECK_ADMIN_QUIZ_DELETE_HISTORY,
    DELETE_ADMIN_QUIZ,
    DELETE_ADMIN_QUIZ_CHOICES,
    DELETE_ADMIN_QUIZ_QUESTIONS,
    LOCK_ADMIN_QUIZ_CHOICES_FOR_DELETE,
    LOCK_ADMIN_QUIZ_FOR_DELETE,
    LOCK_ADMIN_QUIZ_QUESTIONS_FOR_DELETE,
    SOFT_DELETE_ADMIN_QUIZ,
)
from app.modules.admin.api_90_admin_quizzes_delete.validate import (
    validate_admin_quiz_delete_request,
)
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
MAX_INT64 = 2**63 - 1


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi query, mutation, mapping hoặc commit thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Quiz could not be deleted.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 khi Quiz không tồn tại hoặc đã hard-delete."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Quiz not found.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction mà không đưa chi tiết database vào HTTP response."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin quiz delete rollback failed; trace_id=%s", trace_id)


def _valid_id(value: Any) -> bool:
    """Kiểm tra projection ID là số nguyên dương trong miền signed-int64."""

    return type(value) is int and 1 <= value <= MAX_INT64


def _locked_ids(rows: Any) -> list[int] | None:
    """Lấy dãy ID đã khóa, từ chối projection sai hoặc ID lặp."""

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


def _returned_ids_match(rows: Any, expected: list[int]) -> bool:
    """Xác nhận DELETE RETURNING chứa đúng các child ID đã khóa."""

    returned = _locked_ids(rows)
    return (
        returned is not None and len(returned) == len(expected) and set(returned) == set(expected)
    )


def _map_delete_result(row: Mapping[str, Any], *, quiz_id: int) -> DeleteResult | None:
    """Kiểm tra identity/timestamp rồi dựng DeleteResult theo catalog."""

    result_id = row.get("id")
    deleted_at = row.get("deleted_at")
    if not _valid_id(result_id) or result_id != quiz_id or not isinstance(deleted_at, datetime):
        return None
    try:
        return DeleteResult(id=result_id, status="deleted", deleted_at=deleted_at)
    except (TypeError, ValidationError):
        return None


def _map_tombstone_result(row: Mapping[str, Any], *, quiz_id: int) -> DeleteResult | None:
    """Dùng updated_at đã lưu để trả lại kết quả DELETE lặp an toàn."""

    result_id = row.get("id")
    updated_at = row.get("updated_at")
    if not _valid_id(result_id) or result_id != quiz_id or not isinstance(updated_at, datetime):
        return None
    try:
        return DeleteResult(id=result_id, status="deleted", deleted_at=updated_at)
    except (TypeError, ValidationError):
        return None


def _commit_delete_result(
    db: Session,
    result: DeleteResult,
    *,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Commit sau khi response hợp lệ rồi trả envelope xóa theo catalog."""

    response_data = result.model_dump(mode="json")
    try:
        db.commit()
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin quiz delete commit failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    return success_response(
        business_code="DESIGN_RESOURCE_DELETED",
        message="Quiz deleted.",
        trace_id=trace_id,
        data=response_data,
    )


# API #90 admin_quizzes_delete
def delete_admin_quiz(
    *,
    authorization: str | None,
    quiz_id_value: str,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN, giữ history và xóa mềm/cứng Quiz theo nhánh AC-35."""

    # Xác thực ADMIN và path trước khi bắt đầu truy vấn database.
    validated = validate_admin_quiz_delete_request(
        authorization,
        quiz_id_value,
        trace_id=trace_id,
    )
    if isinstance(validated, JSONResponse):
        return validated
    quiz_id = validated

    try:
        # Khóa Quiz kể cả khi đã tombstone để DELETE lặp giữ nguyên timestamp.
        quiz_row = query_one(db, LOCK_ADMIN_QUIZ_FOR_DELETE, {"quiz_id": quiz_id})
        if quiz_row is None:
            _rollback_safely(db, trace_id=trace_id)
            return _not_found(trace_id)
        if (
            not isinstance(quiz_row, Mapping)
            or not _valid_id(quiz_row.get("id"))
            or quiz_row.get("id") != quiz_id
            or quiz_row.get("status") is not None
            and not isinstance(quiz_row.get("status"), str)
        ):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin quiz delete lock projection invalid; trace_id=%s", trace_id)
            return _internal_error(trace_id)

        if quiz_row.get("status") == "DELETED":
            # Không cập nhật lại updated_at để DELETE lặp trả cùng thời điểm.
            result = _map_tombstone_result(quiz_row, quiz_id=quiz_id)
            if result is None:
                _rollback_safely(db, trace_id=trace_id)
                logger.error("Admin quiz tombstone projection invalid; trace_id=%s", trace_id)
                return _internal_error(trace_id)
            return _commit_delete_result(db, result, trace_id=trace_id)

        # Khóa question rồi choice theo cùng thứ tự ổn định với API #89.
        question_ids = _locked_ids(
            query_many(db, LOCK_ADMIN_QUIZ_QUESTIONS_FOR_DELETE, {"quiz_id": quiz_id})
        )
        choice_ids = _locked_ids(
            query_many(db, LOCK_ADMIN_QUIZ_CHOICES_FOR_DELETE, {"quiz_id": quiz_id})
        )
        if question_ids is None or choice_ids is None:
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin quiz child lock projection invalid; trace_id=%s", trace_id)
            return _internal_error(trace_id)

        # Giữ child rows khi có attempt hoặc answer tham chiếu đến Quiz.
        history = query_one(db, CHECK_ADMIN_QUIZ_DELETE_HISTORY, {"quiz_id": quiz_id})
        if (
            not isinstance(history, Mapping)
            or type(history.get("has_attempts")) is not bool
            or type(history.get("has_answers")) is not bool
        ):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin quiz delete history projection invalid; trace_id=%s", trace_id)
            return _internal_error(trace_id)

        if history["has_attempts"] or history["has_answers"]:
            # Soft-delete giữ nguyên lịch sử và map DB updated_at sang deleted_at.
            deleted_row = query_one(db, SOFT_DELETE_ADMIN_QUIZ, {"quiz_id": quiz_id})
            if deleted_row is None:
                _rollback_safely(db, trace_id=trace_id)
                return _not_found(trace_id)
            if not isinstance(deleted_row, Mapping):
                _rollback_safely(db, trace_id=trace_id)
                logger.error("Admin quiz soft-delete projection invalid; trace_id=%s", trace_id)
                return _internal_error(trace_id)
            result = _map_delete_result(deleted_row, quiz_id=quiz_id)
            if result is None:
                _rollback_safely(db, trace_id=trace_id)
                logger.error("Admin quiz soft-delete mapping invalid; trace_id=%s", trace_id)
                return _internal_error(trace_id)
            return _commit_delete_result(db, result, trace_id=trace_id)

        # Không có history thì xóa choices trước questions theo FK candidate.
        deleted_choices = query_many(db, DELETE_ADMIN_QUIZ_CHOICES, {"quiz_id": quiz_id})
        if not _returned_ids_match(deleted_choices, choice_ids):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin quiz Choice delete projection mismatch; trace_id=%s", trace_id)
            return _internal_error(trace_id)

        deleted_questions = query_many(
            db,
            DELETE_ADMIN_QUIZ_QUESTIONS,
            {"quiz_id": quiz_id},
        )
        if not _returned_ids_match(deleted_questions, question_ids):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin quiz Question delete projection mismatch; trace_id=%s", trace_id)
            return _internal_error(trace_id)

        # Xóa parent sau cùng và lấy timestamp từ cùng transaction DB.
        deleted_quiz = query_one(db, DELETE_ADMIN_QUIZ, {"quiz_id": quiz_id})
        if deleted_quiz is None:
            _rollback_safely(db, trace_id=trace_id)
            return _not_found(trace_id)
        if not isinstance(deleted_quiz, Mapping):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin quiz hard-delete projection invalid; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        result = _map_delete_result(deleted_quiz, quiz_id=quiz_id)
        if result is None:
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin quiz hard-delete mapping invalid; trace_id=%s", trace_id)
            return _internal_error(trace_id)
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin quiz delete query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Commit chỉ sau khi mutation và toàn bộ DeleteResult đã hợp lệ.
    return _commit_delete_result(db, result, trace_id=trace_id)
