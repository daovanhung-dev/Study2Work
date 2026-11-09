"""Xử lý nghiệp vụ và điều phối dữ liệu cho API #27 tìm bài học tiếp theo theo curriculum."""

from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.guest.api_27_lessons_next.models import NextLesson
from app.modules.guest.api_27_lessons_next.query import FIND_CURRENT_LESSON, FIND_NEXT_LESSON
from app.modules.guest.api_27_lessons_next.validate import (
    lesson_not_found,
    validate_next_lesson_request,
)
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def find_current_lesson(db: Session, *, lesson_id: int) -> dict[str, Any] | None:
    """Truy vấn thông tin bài học hiện tại kèm trạng thái PUBLISHED của khóa học cha."""
    return query_one(db, FIND_CURRENT_LESSON, {"lesson_id": lesson_id})


def find_next_lesson(
    db: Session,
    *,
    course_id: int,
    current_sort_order: int,
    current_lesson_id: int,
) -> dict[str, Any] | None:
    """Truy vấn bài học PUBLISHED kế tiếp theo thứ tự curriculum (sort_order ASC, id ASC)."""
    return query_one(
        db,
        FIND_NEXT_LESSON,
        {
            "course_id": course_id,
            "current_sort_order": current_sort_order,
            "current_lesson_id": current_lesson_id,
        },
    )


# API #27 lessons_next
def get_next_lesson(
    *,
    authorization: str | None,
    lesson_id_raw: str | int,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Student, kiểm tra vị trí bài hiện tại và tìm bài học tiếp theo trong curriculum."""
    validation = validate_next_lesson_request(
        authorization=authorization,
        lesson_id_raw=lesson_id_raw,
        trace_id=trace_id,
    )
    if isinstance(validation, JSONResponse):
        return validation
    _user_id, lesson_id = validation

    try:
        current_lesson = find_current_lesson(db, lesson_id=lesson_id)
        if current_lesson is None:
            return lesson_not_found(trace_id, message="Current lesson not found")

        next_row = find_next_lesson(
            db,
            course_id=current_lesson["course_id"],
            current_sort_order=current_lesson["sort_order"],
            current_lesson_id=current_lesson["id"],
        )
        if next_row is None:
            return lesson_not_found(trace_id, message="Next lesson not found in curriculum")

        next_lesson = NextLesson.model_validate(next_row)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Next lesson lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    except ValidationError:
        logger.exception("Next lesson mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Next lesson retrieved",
        trace_id=trace_id,
        data=next_lesson.model_dump(mode="json"),
    )


def _internal_error(trace_id: str) -> JSONResponse:
    """Tạo response lỗi 500 chuẩn khi truy vấn database hoặc mapping thất bại."""
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Next lesson could not be retrieved",
        trace_id=trace_id,
    )
