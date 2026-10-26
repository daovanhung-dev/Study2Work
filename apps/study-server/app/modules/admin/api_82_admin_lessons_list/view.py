"""Điều phối quyền Admin, truy vấn và ánh xạ danh sách Lesson API #82."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_many
from app.core.responses import error_response, success_response
from app.modules.admin.api_82_admin_lessons_list.models import AdminLessonsQuery
from app.modules.admin.api_82_admin_lessons_list.query import LIST_ADMIN_LESSONS
from app.modules.admin.api_82_admin_lessons_list.validate import (
    validate_admin_lessons_query,
    validate_admin_request,
)
from app.modules.guest.api_09_courses_curriculum.models import Lesson
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi truy vấn hoặc ánh xạ danh sách Lesson thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Lessons could not be retrieved.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction đọc lỗi mà không làm lộ hoặc che response ban đầu."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin lessons rollback failed; trace_id=%s", trace_id)


def _map_lesson_rows(
    rows: Any,
    *,
    trace_id: str,
) -> list[Lesson] | None:
    """Ánh xạ projection list sang reusable Lesson, từ chối row thiếu field bắt buộc."""

    if not isinstance(rows, list):
        return None

    items: list[Lesson] = []
    for row in rows:
        if not isinstance(row, Mapping):
            return None
        try:
            items.append(Lesson.model_validate(dict(row)))
        except (TypeError, ValidationError):
            logger.error("Admin lesson projection failed; trace_id=%s", trace_id)
            return None
    return items


def _query_parameters(query: AdminLessonsQuery) -> dict[str, Any]:
    """Tạo bind parameters cho filter course/status đã được chuẩn hóa."""

    return {"course_id": query.course_id, "status": query.status}


# API #82 admin_lessons_list
def get_admin_lessons(
    *,
    authorization: str | None,
    course_value: str | None,
    status: str | None,
    type_value: str | None,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Trả danh sách Lesson theo filter course/status cho Admin; chưa hỗ trợ type."""

    # Xác thực Bearer/JWT và role Admin trước khi parse query hoặc truy cập DB.
    authentication = validate_admin_request(authorization, trace_id=trace_id)
    if isinstance(authentication, JSONResponse):
        return authentication

    # Chuẩn hóa course và trả lỗi rõ ràng nếu client gửi type chưa có schema mapping.
    validated_query = validate_admin_lessons_query(
        course_value=course_value,
        status=status,
        type_value=type_value,
        trace_id=trace_id,
    )
    if isinstance(validated_query, JSONResponse):
        return validated_query

    # Đọc candidate legacy Lesson bằng bind parameters; GET không count hoặc phân trang.
    try:
        rows = query_many(
            db,
            LIST_ADMIN_LESSONS,
            _query_parameters(validated_query),
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin lessons query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Từ chối projection hỏng để không trả về danh sách thiếu hoặc sai contract âm thầm.
    items = _map_lesson_rows(rows, trace_id=trace_id)
    if items is None:
        _rollback_safely(db, trace_id=trace_id)
        return _internal_error(trace_id)

    # Trả Lesson[] trực tiếp; collection rỗng vẫn là thành công và không commit transaction.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Lessons retrieved." if items else "No lessons found.",
        trace_id=trace_id,
        data=[item.model_dump(mode="json") for item in items],
    )
