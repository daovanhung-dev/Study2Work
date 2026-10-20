"""Điều phối nghiệp vụ cho API #22 kiểm tra quyền truy cập bài học."""

from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.guest.api_22_lessons_access.models import LessonResponse
from app.modules.guest.api_22_lessons_access.query import (
    FIND_ACTIVE_ENROLLMENT,
    FIND_LESSON_BY_ID,
)
from app.modules.guest.api_22_lessons_access.validate import (
    validate_lesson_access_request,
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
        message="Lesson access could not be verified.",
        trace_id=trace_id,
    )


# API #22 lessons_access
def check_lesson_access(
    *,
    lesson_id: str | int,
    authorization: str | None = None,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Kiểm tra quyền truy cập vào bài học cho học viên hiện tại."""
    # Xác thực token học viên và chuẩn hóa định danh lesson_id.
    validation = validate_lesson_access_request(
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

    # Trả về 403 nếu học viên chưa có quyền học khóa học chứa bài này.
    if enrollment is None:
        return _access_denied_error(trace_id)

    # Ánh xạ thông tin bài học sang model response chuẩn.
    try:
        data = LessonResponse.model_validate(lesson)
    except:
        logger.exception("Lesson response mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả về kết quả thành công HTTP 200.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Lesson access granted.",
        trace_id=trace_id,
        data=data.model_dump(mode="json"),
    )

