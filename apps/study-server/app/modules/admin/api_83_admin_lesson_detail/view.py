"""Điều phối quyền Admin, lookup và ánh xạ Lesson detail API #83."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.admin.api_83_admin_lesson_detail.query import FIND_ADMIN_LESSON_DETAIL
from app.modules.admin.api_83_admin_lesson_detail.validate import (
    parse_admin_lesson_id,
    validate_admin_request,
)
from app.modules.guest.api_09_courses_curriculum.models import Lesson
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
MAX_INT64 = 2**63 - 1


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi truy vấn hoặc ánh xạ Lesson detail thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Lesson could not be retrieved.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 catalog cho path ID sai hoặc Lesson không tồn tại."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Lesson not found.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction đọc lỗi mà không làm lộ hoặc che response ban đầu."""

    try:
        # Giải phóng transaction lỗi; lỗi rollback chỉ được ghi log an toàn.
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin lesson detail rollback failed; trace_id=%s", trace_id)


def _map_admin_lesson(
    row: Mapping[str, Any],
    *,
    requested_lesson_id: int,
) -> Lesson | None:
    """Kiểm tra identity row rồi ánh xạ projection qua reusable Lesson API #09."""

    # Bảo đảm query trả đúng khóa BIGINT hợp lệ trước khi dựng response.
    lesson_id = row.get("id")
    if (
        type(lesson_id) is not int
        or not 1 <= lesson_id <= MAX_INT64
        or lesson_id != requested_lesson_id
    ):
        return None

    try:
        # Reuse Lesson để giữ tên field và kiểu response thống nhất với API #09/#82.
        return Lesson.model_validate(dict(row))
    except (TypeError, ValidationError):
        return None


# API #83 admin_lesson_detail
def get_admin_lesson_detail(
    *,
    authorization: str | None,
    lesson_id_value: str,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN, đọc một Lesson theo int64 ID và trả Lesson trực tiếp."""

    # Xác thực principal và role trước khi parse path hoặc truy vấn Lesson.
    authentication = validate_admin_request(authorization, trace_id=trace_id)
    if isinstance(authentication, JSONResponse):
        return authentication

    # Parse raw path để giữ đúng error set catalog, không phát sinh HTTP 422.
    lesson_id = parse_admin_lesson_id(lesson_id_value)
    if lesson_id is None:
        return _not_found(trace_id)

    try:
        # Đọc đúng projection Lesson bằng bind parameter; không lọc theo status.
        row = query_one(db, FIND_ADMIN_LESSON_DETAIL, {"lesson_id": lesson_id})
    except SQLAlchemyError:
        # Rollback transaction lỗi và trả lỗi nội bộ không chứa chi tiết database.
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin lesson detail query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Lesson vắng mặt trả đúng 404; không đọc resources/progress chưa có output rule.
    if row is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(row, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin lesson detail projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Từ chối row sai identity hoặc thiếu field bắt buộc thay vì làm sai contract.
    lesson = _map_admin_lesson(row, requested_lesson_id=lesson_id)
    if lesson is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin lesson detail mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả Lesson trực tiếp; dependency sở hữu vòng đời session và không cần commit.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Lesson retrieved.",
        trace_id=trace_id,
        data=lesson.model_dump(mode="json"),
    )
