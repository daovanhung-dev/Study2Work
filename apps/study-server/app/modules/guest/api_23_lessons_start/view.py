"""Điều phối nghiệp vụ cho API #23 khởi tạo lần bắt đầu học bài học."""

from __future__ import annotations

import logging
from typing import Any

from app.core.database import execute_query, query_one
from app.core.responses import error_response, success_response
from app.modules.guest.api_23_lessons_start.models import LessonResponse
from app.modules.guest.api_23_lessons_start.query import (
    FIND_ACTIVE_ENROLLMENT,
    FIND_LESSON_BY_ID,
    FIND_LESSON_PROGRESS,
    INSERT_LESSON_PROGRESS,
    TOUCH_LESSON_PROGRESS,
)
from app.modules.guest.api_23_lessons_start.validate import (
    validate_lesson_start_request,
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
    """Truy vấn tiến độ bài học hiện có của học viên."""
    return query_one(
        db,
        FIND_LESSON_PROGRESS,
        {"user_id": user_id, "lesson_id": lesson_id},
    )


def insert_lesson_progress(
    db: Session, *, user_id: int, lesson_id: int
) -> dict[str, Any] | None:
    """Tạo mới bản ghi tiến độ bài học ở trạng thái IN_PROGRESS."""
    return query_one(
        db,
        INSERT_LESSON_PROGRESS,
        {"user_id": user_id, "lesson_id": lesson_id},
    )


def touch_lesson_progress(
    db: Session, *, progress_id: int
) -> dict[str, Any] | None:
    """Cập nhật thời gian truy cập gần nhất và đảm bảo trạng thái IN_PROGRESS nếu chưa hoàn thành."""
    return query_one(
        db,
        TOUCH_LESSON_PROGRESS,
        {"progress_id": progress_id},
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
        message="Lesson could not be started.",
        trace_id=trace_id,
    )


# API #23 lessons_start
def start_lesson(
    *,
    lesson_id: str | int,
    authorization: str | None = None,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Khởi tạo hoặc cập nhật trạng thái bắt đầu học bài học cho học viên."""
    # Xác thực token học viên và chuẩn hóa định danh lesson_id.
    validation = validate_lesson_start_request(
        authorization,
        lesson_id,
        trace_id=trace_id,
    )
    if isinstance(validation, JSONResponse):
        return validation
    user_id, validated_lesson_id = validation

    # Truy vấn bài học theo lesson_id.
    try:
        lesson = find_lesson_by_id(db, lesson_id=validated_lesson_id)
    except:
        db.rollback()
        logger.exception("Lesson lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả về 404 nếu bài học không tồn tại hoặc không gắn với khóa học.
    if lesson is None or lesson.get("course_id") is None:
        return _not_found_error(trace_id)

    # Kiểm tra xem học viên đã ghi danh vào khóa học này chưa.
    try:
        enrollment = find_active_enrollment(
            db,
            user_id=user_id,
            course_id=lesson["course_id"],
        )
    except:
        db.rollback()
        logger.exception("Enrollment check failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả về 403 nếu học viên chưa có quyền học khóa học này.
    if enrollment is None:
        return _access_denied_error(trace_id)

    # Khởi tạo hoặc cập nhật tiến độ bài học trong transaction.
    try:
        existing_progress = find_lesson_progress(
            db,
            user_id=user_id,
            lesson_id=validated_lesson_id,
        )
        if existing_progress is None:
            insert_lesson_progress(
                db,
                user_id=user_id,
                lesson_id=validated_lesson_id,
            )
        else:
            touch_lesson_progress(
                db,
                progress_id=existing_progress["id"],
            )

        data = LessonResponse.model_validate(lesson)
        db.commit()
    except:
        db.rollback()
        logger.exception("Lesson start persistence failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả về kết quả thành công HTTP 201 theo đặc tả.
    return success_response(
        business_code="DESIGN_RESOURCE_CREATED",
        message="Lesson started.",
        trace_id=trace_id,
        data=data.model_dump(mode="json"),
    )

