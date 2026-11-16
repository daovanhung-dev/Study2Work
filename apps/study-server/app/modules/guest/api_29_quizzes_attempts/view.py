"""Xử lý nghiệp vụ và điều phối dữ liệu cho API #29 tạo lượt làm bài kiểm tra."""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.guest.api_29_quizzes_attempts.models import QuizAttemptDetail
from app.modules.guest.api_29_quizzes_attempts.query import (
    FIND_ACTIVE_ATTEMPT,
    FIND_QUIZ_BY_ID,
    INSERT_QUIZ_ATTEMPT,
)
from app.modules.guest.api_29_quizzes_attempts.validate import (
    attempt_conflict,
    quiz_not_found,
    validate_create_attempt_request,
)
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def format_iso_timestamp(ts: Any) -> str:
    """Chuyển đổi đối tượng thời gian thành chuỗi định dạng ISO 8601 chuẩn."""
    if isinstance(ts, datetime):
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=UTC)
        return ts.isoformat()
    return str(ts)


def find_quiz(db: Session, *, quiz_id: int) -> dict[str, Any] | None:
    """Truy vấn kiểm tra sự tồn tại của bài quiz theo quiz_id."""
    return query_one(db, FIND_QUIZ_BY_ID, {"quiz_id": quiz_id})


def find_active_attempt(
    db: Session,
    *,
    quiz_id: int,
    user_id: int,
) -> dict[str, Any] | None:
    """Truy vấn tìm lượt làm bài đang trong tiến trình (IN_PROGRESS) của học viên."""
    return query_one(
        db,
        FIND_ACTIVE_ATTEMPT,
        {"quiz_id": quiz_id, "user_id": user_id},
    )


def create_quiz_attempt_record(
    db: Session,
    *,
    quiz_id: int,
    user_id: int,
    started_at: datetime,
) -> dict[str, Any] | None:
    """Thực thi ghi bản ghi lượt làm bài mới vào bảng quiz_attempts."""
    return query_one(
        db,
        INSERT_QUIZ_ATTEMPT,
        {
            "quiz_id": quiz_id,
            "user_id": user_id,
            "started_at": started_at,
        },
    )


# API #29 quizzes_attempts
def create_quiz_attempt(
    *,
    authorization: str | None,
    quiz_id_raw: str | int,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Student, kiểm tra quiz và trạng thái conflict rồi tạo mới lượt làm bài."""
    # Xác thực quyền Student và kiểm tra tính hợp lệ của path parameter quiz_id
    validation = validate_create_attempt_request(
        authorization=authorization,
        quiz_id_raw=quiz_id_raw,
        trace_id=trace_id,
    )
    if isinstance(validation, JSONResponse):
        return validation
    user_id, quiz_id = validation

    try:
        # Kiểm tra bài quiz có tồn tại trong hệ thống hay không
        quiz = find_quiz(db, quiz_id=quiz_id)
        if quiz is None:
            return quiz_not_found(trace_id, message="Quiz not found")

        # Kiểm tra xem học viên đã có lượt làm bài nào đang IN_PROGRESS hay chưa
        existing_attempt = find_active_attempt(db, quiz_id=quiz_id, user_id=user_id)
        if existing_attempt is not None:
            return attempt_conflict(
                trace_id,
                message="An attempt is already in progress for this quiz",
            )

        # Tạo bản ghi attempt mới với trạng thái IN_PROGRESS và mốc thời gian hiện tại
        now = datetime.now(UTC)
        created_row = create_quiz_attempt_record(
            db,
            quiz_id=quiz_id,
            user_id=user_id,
            started_at=now,
        )
        if created_row is None:
            db.rollback()
            return _internal_error(trace_id)

        # Xác nhận transaction ghi dữ liệu
        db.commit()

        # Ánh xạ dữ liệu thành model QuizAttemptDetail theo contract
        attempt_detail = QuizAttemptDetail(
            id=created_row["id"],
            quiz_id=created_row["quiz_id"],
            status=created_row.get("status", "IN_PROGRESS"),
            started_at=format_iso_timestamp(created_row["started_at"]),
            submitted_at=created_row.get("submitted_at"),
            score=created_row.get("score"),
            answers=[],
        )
    except SQLAlchemyError:
        # Rollback giao dịch khi có lỗi kết nối hoặc thao tác DB
        db.rollback()
        logger.exception("Create quiz attempt failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    except (ValidationError, ValueError):
        # Ghi log khi việc ánh xạ model gặp lỗi
        logger.exception("Quiz attempt mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả về kết quả thành công bọc trong ApiEnvelope chuẩn
    return success_response(
        business_code="DESIGN_RESOURCE_CREATED",
        message="Quiz attempt created",
        trace_id=trace_id,
        data=attempt_detail.model_dump(mode="json"),
    )


def _internal_error(trace_id: str) -> JSONResponse:
    """Tạo response lỗi 500 chuẩn khi truy vấn database hoặc tạo bản ghi thất bại."""
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Internal server error",
        trace_id=trace_id,
    )
