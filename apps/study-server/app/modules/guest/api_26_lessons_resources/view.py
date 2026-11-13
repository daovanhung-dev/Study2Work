"""Xử lý nghiệp vụ và điều phối dữ liệu cho API #26 lấy tài nguyên đính kèm bài học."""

from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.guest.api_26_lessons_resources.models import LessonResources, ResourceItem
from app.modules.guest.api_26_lessons_resources.query import (
    CHECK_PUBLISHED_LESSON,
    FIND_LESSON_RESOURCES,
)
from app.modules.guest.api_26_lessons_resources.validate import (
    lesson_not_found,
    validate_lesson_resources_request,
)
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def find_published_lesson(db: Session, *, lesson_id: int) -> dict[str, Any] | None:
    """Truy vấn thông tin bài học có khóa học cha ở trạng thái PUBLISHED."""
    return query_one(db, CHECK_PUBLISHED_LESSON, {"lesson_id": lesson_id})


def find_lesson_resources(db: Session, *, lesson_id: int) -> list[dict[str, Any]]:
    """Truy vấn danh sách các tài nguyên đính kèm bài học."""
    return query_many(db, FIND_LESSON_RESOURCES, {"lesson_id": lesson_id})


# API #26 lessons_resources
def get_lesson_resources(
    *,
    authorization: str | None,
    lesson_id_raw: str | int,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Student, kiểm tra lesson cha và trả về thông tin bài học kèm tài nguyên."""
    validation = validate_lesson_resources_request(
        authorization=authorization,
        lesson_id_raw=lesson_id_raw,
        trace_id=trace_id,
    )
    if isinstance(validation, JSONResponse):
        return validation
    _user_id, lesson_id = validation

    try:
        lesson_row = find_published_lesson(db, lesson_id=lesson_id)
        if lesson_row is None:
            return lesson_not_found(trace_id)

        resource_rows = find_lesson_resources(db, lesson_id=lesson_id)
        resources = [ResourceItem.model_validate(r) for r in resource_rows]

        lesson_data = dict(lesson_row)
        lesson_data["resources"] = resources
        response_model = LessonResources.model_validate(lesson_data)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Lesson resources lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    except ValidationError:
        logger.exception("Lesson resources mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Lesson resources retrieved",
        trace_id=trace_id,
        data=response_model.model_dump(mode="json"),
    )


def _internal_error(trace_id: str) -> JSONResponse:
    """Tạo response lỗi 500 chuẩn khi truy vấn database hoặc mapping thất bại."""
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Lesson resources could not be retrieved",
        trace_id=trace_id,
    )
