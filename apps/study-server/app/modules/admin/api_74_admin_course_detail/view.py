"""Điều phối quyền Admin, truy vấn và ánh xạ course detail cho API #74."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_one
from app.core.responses import ErrorDetail, error_response, success_response
from app.modules.admin.api_74_admin_course_detail.query import FIND_ADMIN_COURSE_DETAIL
from app.modules.admin.api_74_admin_course_detail.validate import (
    parse_admin_course_id,
    validate_admin_request,
)
from app.modules.guest._shared.course_catalog.helpers import map_course
from app.modules.guest._shared.course_catalog.models import Course, CoursePage, Pagination
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
MAX_INT64 = 2**63 - 1


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn cho query hoặc ánh xạ course detail."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Course could not be retrieved.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 catalog cho path ID sai hoặc course không tồn tại."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Course not found.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction đọc lỗi mà không che response lỗi ban đầu."""

    try:
        # Giải phóng transaction lỗi; lỗi rollback chỉ được ghi log an toàn.
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin course detail rollback failed; trace_id=%s", trace_id)


def _map_admin_course(
    row: Mapping[str, Any],
    *,
    requested_course_id: int,
) -> Course | None:
    """Kiểm tra identity row rồi ánh xạ qua Course mapper dùng chung."""

    # Bảo đảm query đã trả đúng course và khóa BIGINT hợp lệ trước khi dựng response.
    course_id = row.get("id")
    if (
        type(course_id) is not int
        or not 1 <= course_id <= MAX_INT64
        or course_id != requested_course_id
    ):
        return None

    try:
        # Dùng allowlist Course chung để giữ mapping và định dạng giá chính xác.
        course = map_course(dict(row))
    except (TypeError, ValidationError):
        return None
    if isinstance(course, ErrorDetail):
        return None
    return course


# API #74 admin_course_detail
def get_admin_course_detail(
    *,
    authorization: str | None,
    course_id_value: str,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN, đọc một course theo int64 ID và trả CoursePage singleton."""

    # Xác thực principal và role trước khi parse path hoặc truy vấn dữ liệu course.
    authentication = validate_admin_request(authorization, trace_id=trace_id)
    if isinstance(authentication, JSONResponse):
        return authentication

    # Parse raw path để giữ đúng error set catalog, không phát sinh HTTP 422.
    course_id = parse_admin_course_id(course_id_value)
    if course_id is None:
        return _not_found(trace_id)

    try:
        # Đọc đúng projection Course/mentor bằng bind parameter và không lọc status.
        row = query_one(db, FIND_ADMIN_COURSE_DETAIL, {"course_id": course_id})
    except SQLAlchemyError:
        # Rollback transaction lỗi và trả lỗi nội bộ không chứa chi tiết database.
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course detail query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Resource vắng mặt trả về đúng 404; request vẫn giữ ranh giới read-only.
    if row is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(row, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course detail projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Từ chối projection không đầy đủ thay vì trả Course thiếu mentor hoặc giá.
    course = _map_admin_course(row, requested_course_id=course_id)
    if course is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course detail mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    try:
        # Catalog yêu cầu Page<Course>; detail được biểu diễn bằng một item cố định.
        page = CoursePage(
            items=[course],
            pagination=Pagination(page=1, size=1, total=1, total_pages=1),
        )
    except (TypeError, ValidationError):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course detail page mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả response chỉ đọc; dependency sở hữu vòng đời session và không cần commit.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Course retrieved.",
        trace_id=trace_id,
        data=page.model_dump(mode="json"),
    )
