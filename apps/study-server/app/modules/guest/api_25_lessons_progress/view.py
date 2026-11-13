"""Điều phối nghiệp vụ cho API #25 cập nhật tiến độ bài học."""

from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.guest.api_25_lessons_progress.models import (
    LessonProgressUpdateRequest,
    LessonResponse,
)
from app.modules.guest.api_25_lessons_progress.query import (
    FIND_ACTIVE_ENROLLMENT,
    FIND_LESSON_BY_ID,
    FIND_LESSON_PROGRESS,
    INSERT_LESSON_PROGRESS_STATE,
    UPDATE_LESSON_PROGRESS_STATE,
)
from app.modules.guest.api_25_lessons_progress.validate import (
    validate_lesson_progress_request,
)
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def find_lesson_by_id(db: Session, *, lesson_id: int) -> dict[str, Any] | None:
    """Truy vấn thông tin bài học từ cơ sở dữ liệu theo lesson_id."""
    return query_one(db, FIND_LESSON_BY_ID, {"lesson_id": lesson_id})


def find_active_enrollment(
    db: Session, *, user_id: int, course_id: int
) -> dict[str, Any] | None:
    """Truy vấn bản ghi ghi danh hợp lệ của học viên trong khóa học."""
    return query_one(
        db,
        FIND_ACTIVE_ENROLLMENT,
        {"user_id": user_id, "course_id": course_id},
    )


def find_lesson_progress(
    db: Session, *, user_id: int, lesson_id: int
) -> dict[str, Any] | None:
    """Truy vấn bản ghi tiến độ hiện có của học viên đối với bài học."""
    return query_one(
        db,
        FIND_LESSON_PROGRESS,
        {"user_id": user_id, "lesson_id": lesson_id},
    )


def insert_lesson_progress_state(
    db: Session,
    *,
    user_id: int,
    lesson_id: int,
    status: str,
    progress_percent: int,
    completed: bool,
) -> dict[str, Any] | None:
    """Tạo mới bản ghi tiến độ bài học với trạng thái và phần trăm hoàn thành chỉ định."""
    return query_one(
        db,
        INSERT_LESSON_PROGRESS_STATE,
        {
            "user_id": user_id,
            "lesson_id": lesson_id,
            "status": status,
            "progress_percent": progress_percent,
            "completed": completed,
        },
    )


def update_lesson_progress_state(
    db: Session,
    *,
    progress_id: int,
    status: str,
    progress_percent: int,
    completed: bool,
) -> dict[str, Any] | None:
    """Cập nhật bản ghi tiến độ bài học hiện có với trạng thái và phần trăm mới."""
    return query_one(
        db,
        UPDATE_LESSON_PROGRESS_STATE,
        {
            "progress_id": progress_id,
            "status": status,
            "progress_percent": progress_percent,
            "completed": completed,
        },
    )


def _not_found_error(trace_id: str) -> JSONResponse:
    """Tạo phản hồi lỗi 404 khi không tìm thấy bài học."""
    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Lesson not found.",
        trace_id=trace_id,
    )


def _access_denied_error(trace_id: str) -> JSONResponse:
    """Tạo phản hồi lỗi 403 khi học viên chưa ghi danh vào khóa học."""
    return error_response(
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message="Access denied to this lesson.",
        trace_id=trace_id,
    )


def _internal_error(trace_id: str) -> JSONResponse:
    """Tạo phản hồi lỗi 500 khi gặp lỗi hệ thống hoặc cơ sở dữ liệu."""
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Lesson progress could not be updated.",
        trace_id=trace_id,
    )


# API #25 lessons_progress
def update_lesson_progress(
    *,
    lesson_id: str | int,
    progress_data: LessonProgressUpdateRequest,
    authorization: str | None = None,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Cập nhật vị trí, phần trăm tiến độ và trạng thái hoàn thành bài học."""
    # Xác thực token học viên, kiểm tra lesson_id và dữ liệu cập nhật tiến độ.
    validation = validate_lesson_progress_request(
        authorization,
        lesson_id,
        progress_data,
        trace_id=trace_id,
    )
    if isinstance(validation, JSONResponse):
        return validation
    user_id, validated_lesson_id, validated_payload = validation

    # Truy vấn bài học theo lesson_id.
    try:
        lesson = find_lesson_by_id(db, lesson_id=validated_lesson_id)
    except Exception:
        db.rollback()
        logger.exception("Lesson lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả về 404 nếu bài học không tồn tại hoặc không thuộc khóa học nào.
    if lesson is None or lesson.get("course_id") is None:
        return _not_found_error(trace_id)

    # Kiểm tra xem học viên đã ghi danh vào khóa học này chưa.
    try:
        enrollment = find_active_enrollment(
            db,
            user_id=user_id,
            course_id=lesson["course_id"],
        )
    except Exception:
        db.rollback()
        logger.exception("Enrollment check failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả về 403 nếu học viên chưa có quyền học khóa học này.
    if enrollment is None:
        return _access_denied_error(trace_id)

    # Xác định trạng thái tiến độ bài học: COMPLETED nếu completed=True, ngược lại IN_PROGRESS.
    target_status = "COMPLETED" if validated_payload.completed else "IN_PROGRESS"

    # Cập nhật hoặc chèn mới bản ghi tiến độ bài học trong transaction.
    try:
        existing_progress = find_lesson_progress(
            db,
            user_id=user_id,
            lesson_id=validated_lesson_id,
        )
        if existing_progress is None:
            insert_lesson_progress_state(
                db,
                user_id=user_id,
                lesson_id=validated_lesson_id,
                status=target_status,
                progress_percent=validated_payload.percent,
                completed=validated_payload.completed,
            )
        else:
            update_lesson_progress_state(
                db,
                progress_id=existing_progress["id"],
                status=target_status,
                progress_percent=validated_payload.percent,
                completed=validated_payload.completed,
            )

        data = LessonResponse.model_validate(lesson)
        db.commit()
    except Exception:
        db.rollback()
        logger.exception("Lesson progress update failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả về kết quả thành công HTTP 200.
    return success_response(
        business_code="DESIGN_RESOURCE_UPDATED",
        message="Lesson progress updated.",
        trace_id=trace_id,
        data=data.model_dump(mode="json"),
    )

