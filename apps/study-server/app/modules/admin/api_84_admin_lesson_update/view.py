"""Điều phối quyền Admin, cập nhật metadata và ánh xạ Lesson API #84."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.admin.api_84_admin_lesson_update.models import AdminLessonUpdateRequest
from app.modules.admin.api_84_admin_lesson_update.query import UPDATE_ADMIN_LESSON_METADATA
from app.modules.admin.api_84_admin_lesson_update.validate import (
    validate_admin_lesson_update_request,
)
from app.modules.guest.api_09_courses_curriculum.models import Lesson
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
MAX_INT64 = 2**63 - 1


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi query, mapping hoặc commit API #84 thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Lesson could not be updated.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 catalog khi UPDATE không tìm thấy Lesson cần sửa."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Lesson not found.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction lỗi mà không che response ban đầu."""

    try:
        # Dọn transaction mutation lỗi; chỉ ghi trace nếu rollback cũng thất bại.
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin lesson update rollback failed; trace_id=%s", trace_id)


def _map_updated_lesson(
    row: Mapping[str, Any],
    *,
    requested_lesson_id: int,
) -> Lesson | None:
    """Kiểm tra identity rồi ánh xạ projection qua reusable Lesson API #09."""

    lesson_id = row.get("id")
    if (
        type(lesson_id) is not int
        or not 1 <= lesson_id <= MAX_INT64
        or lesson_id != requested_lesson_id
    ):
        return None

    try:
        # Reuse schema Lesson để giữ response field và nullability contract thống nhất.
        return Lesson.model_validate(dict(row))
    except (TypeError, ValidationError):
        return None


# API #84 admin_lesson_update
def update_admin_lesson(
    *,
    authorization: str | None,
    lesson_id_value: str,
    lesson_data: AdminLessonUpdateRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN, thay metadata Lesson đầy đủ và commit sau mapping thành công."""

    # Xác thực role Admin và path trước khi gọi câu UPDATE.
    validation = validate_admin_lesson_update_request(
        authorization,
        lesson_id_value,
        trace_id=trace_id,
    )
    if isinstance(validation, JSONResponse):
        return validation
    lesson_id = validation

    # Thay bốn field metadata DERIVED; giữ nguyên course_id, status và quan hệ asset.
    try:
        updated_row = query_one(
            db,
            UPDATE_ADMIN_LESSON_METADATA,
            {
                "lesson_id": lesson_id,
                "title": lesson_data.title,
                "content": lesson_data.content,
                "video_url": lesson_data.video_url,
                "order": lesson_data.order,
            },
        )
    except SQLAlchemyError:
        # Hủy mutation lỗi và trả thông báo nội bộ an toàn.
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin lesson update query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # UPDATE không trả row là Lesson không tồn tại; không commit transaction rỗng.
    if updated_row is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(updated_row, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin lesson update projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Kiểm tra identity và mọi field response trước khi commit mutation.
    lesson = _map_updated_lesson(updated_row, requested_lesson_id=lesson_id)
    if lesson is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin lesson update mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Commit duy nhất sau khi UPDATE RETURNING đã tạo được response hợp lệ.
    try:
        db.commit()
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin lesson update commit failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_UPDATED",
        message="Lesson updated.",
        trace_id=trace_id,
        data=lesson.model_dump(mode="json"),
    )
