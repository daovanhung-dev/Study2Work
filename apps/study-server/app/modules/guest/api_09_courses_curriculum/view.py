"""Xử lý nghiệp vụ và điều phối dữ liệu cho API #9 curriculum của khóa học."""

from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.guest.api_09_courses_curriculum.models import (
    Lesson,
    LessonPage,
    Pagination,
)
from app.modules.guest.api_09_courses_curriculum.query import (
    CHECK_PUBLISHED_COURSE,
    LIST_PUBLISHED_LESSONS,
)
from app.modules.guest.api_09_courses_curriculum.validate import validate_course_id
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def find_published_course(
    db: Session,
    *,
    course_id: int,
) -> dict[str, Any] | None:
    """Kiểm tra sự tồn tại của khóa học ở trạng thái PUBLISHED (Q1)."""
    return query_one(
        db,
        CHECK_PUBLISHED_COURSE,
        {
            "course_id": course_id,
            "status": "PUBLISHED",
        },
    )


def find_published_lessons(
    db: Session,
    *,
    course_id: int,
) -> list[dict[str, Any]]:
    """Truy vấn danh sách các bài học PUBLISHED của khóa học (Q2)."""
    return query_many(
        db,
        LIST_PUBLISHED_LESSONS,
        {
            "course_id": course_id,
            "status": "PUBLISHED",
        },
    )


def _course_not_found_error(trace_id: str) -> JSONResponse:
    """Tạo response lỗi 404 chuẩn khi không tìm thấy khóa học hoặc khóa học chưa publish."""
    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Published course not found.",
        trace_id=trace_id,
    )


def _internal_error(trace_id: str) -> JSONResponse:
    """Tạo response lỗi 500 chuẩn khi truy vấn database hoặc mapping thất bại."""
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Curriculum could not be retrieved.",
        trace_id=trace_id,
    )


# API #09 get_course_curriculum
def get_course_curriculum(
    *,
    course_id_raw: str | int,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Trả về danh sách bài học đã publish theo thứ tự sắp xếp của khóa học."""

    # Xác thực course_id; định dạng không hợp lệ sẽ trả về 404 theo DD #09.
    validated_course_id = validate_course_id(course_id_raw, trace_id=trace_id)
    if isinstance(validated_course_id, JSONResponse):
        return validated_course_id
    course_id = validated_course_id

    # Kiểm tra khóa học có tồn tại và ở trạng thái PUBLISHED hay không (Q1).
    try:
        course = find_published_course(db, course_id=course_id)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Course lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if course is None:
        return _course_not_found_error(trace_id)

    # Truy vấn các bài học PUBLISHED của khóa học (Q2).
    try:
        rows = find_published_lessons(db, course_id=course_id)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Curriculum lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Ánh xạ danh sách bài học và tạo LessonPage response.
    try:
        items = [Lesson.model_validate(row) for row in rows]
        total = len(items)
        page = LessonPage(
            items=items,
            pagination=Pagination(
                page=1,
                size=total,
                total=total,
                total_pages=1 if total > 0 else 0,
            ),
        )
    except ValidationError:
        logger.exception("Curriculum mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả về response thành công chuẩn.
    message = "Curriculum retrieved." if total else "No published lessons."
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message=message,
        trace_id=trace_id,
        data=page.model_dump(mode="json"),
    )