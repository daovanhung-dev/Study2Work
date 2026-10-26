"""Điều phối Admin auth, metadata update và response projection cho API #75."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_one
from app.core.responses import ErrorDetail, error_response, success_response
from app.modules.admin.api_74_admin_course_detail.query import FIND_ADMIN_COURSE_DETAIL
from app.modules.admin.api_75_admin_course_update.models import AdminCourseUpdateRequest
from app.modules.admin.api_75_admin_course_update.query import UPDATE_ADMIN_COURSE_METADATA
from app.modules.admin.api_75_admin_course_update.validate import (
    validate_admin_course_update_request,
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
    """Dựng lỗi 500 an toàn cho query, projection hoặc commit API #75."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Course could not be updated.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 catalog khi UPDATE không tìm được course cần sửa."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Course not found.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction lỗi mà không che response ban đầu."""

    try:
        # Giải phóng transaction lỗi; lỗi rollback chỉ được ghi log an toàn.
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin course update rollback failed; trace_id=%s", trace_id)


def _map_updated_course(
    row: Mapping[str, Any],
    *,
    requested_course_id: int,
) -> Course | None:
    """Kiểm tra identity của projection rồi dùng Course mapper chung."""

    course_id = row.get("id")
    if (
        type(course_id) is not int
        or not 1 <= course_id <= MAX_INT64
        or course_id != requested_course_id
    ):
        return None

    try:
        # Giữ response allowlist và decimal serialization chung với Course catalog.
        course = map_course(dict(row))
    except (TypeError, ValidationError):
        return None
    if isinstance(course, ErrorDetail):
        return None
    return course


# API #75 admin_course_update
def update_admin_course(
    *,
    authorization: str | None,
    course_id_value: str,
    course_data: AdminCourseUpdateRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN, cập nhật metadata và commit sau khi response hợp lệ."""

    # Xác thực role và input trước khi mở query mutation.
    validation = validate_admin_course_update_request(
        authorization,
        course_id_value,
        course_data,
        trace_id=trace_id,
    )
    if isinstance(validation, JSONResponse):
        return validation
    course_id, price = validation

    # Chỉ cập nhật bốn field metadata được chọn cùng timestamp; status và owner giữ nguyên.
    try:
        updated_row = query_one(
            db,
            UPDATE_ADMIN_COURSE_METADATA,
            {
                "course_id": course_id,
                "title": course_data.title,
                "description": course_data.description,
                "thumbnail_url": course_data.thumbnail_url,
                "price": price,
            },
        )
    except SQLAlchemyError:
        # Hủy mutation lỗi và trả lỗi nội bộ không chứa chi tiết SQL.
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course update query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Không có row được cập nhật là resource không tồn tại theo ID.
    if updated_row is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if (
        not isinstance(updated_row, Mapping)
        or type(updated_row.get("id")) is not int
        or updated_row.get("id") != course_id
    ):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course update result failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Đọc Course/mentor projection trong cùng transaction để phản hồi trạng thái đã ghi.
    try:
        course_row = query_one(db, FIND_ADMIN_COURSE_DETAIL, {"course_id": course_id})
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course update projection query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if not isinstance(course_row, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course update projection missing; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Từ chối projection thiếu mentor/price hoặc lệch identity trước khi commit.
    course = _map_updated_course(course_row, requested_course_id=course_id)
    if course is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course update mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Catalog yêu cầu Page<Course>; update detail dùng singleton page theo API #74.
    try:
        page = CoursePage(
            items=[course],
            pagination=Pagination(page=1, size=1, total=1, total_pages=1),
        )
    except (TypeError, ValidationError):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course update page mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Commit sau khi toàn bộ response projection đã được kiểm tra.
    try:
        db.commit()
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course update commit failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_UPDATED",
        message="Course updated.",
        trace_id=trace_id,
        data=page.model_dump(mode="json"),
    )
