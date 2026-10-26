"""Điều phối Admin auth, course status/audit transaction và response API #76."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import execute_query, query_one
from app.core.responses import ErrorDetail, error_response, success_response
from app.modules.admin.api_74_admin_course_detail.query import FIND_ADMIN_COURSE_DETAIL
from app.modules.admin.api_76_admin_course_status.models import AdminCourseStatusRequest
from app.modules.admin.api_76_admin_course_status.query import (
    INSERT_ADMIN_COURSE_STATUS_AUDIT,
    LOCK_ADMIN_COURSE_STATUS,
    UPDATE_ADMIN_COURSE_STATUS,
)
from app.modules.admin.api_76_admin_course_status.validate import (
    validate_admin_course_status_request,
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
    """Dựng lỗi 500 an toàn cho status, audit, projection hoặc commit API #76."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Course status could not be updated.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 catalog khi UPDATE/lock không tìm thấy course."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Course not found.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction lỗi mà không che response ban đầu."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin course status rollback failed; trace_id=%s", trace_id)


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


# API #76 admin_course_status
def update_admin_course_status(
    *,
    authorization: str | None,
    course_id_value: str,
    course_data: AdminCourseStatusRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN, cập nhật status/audit atomically rồi trả CoursePage."""

    # Xác thực principal và path trước mọi thao tác đọc/ghi course.
    validation = validate_admin_course_status_request(
        authorization,
        course_id_value,
        course_data,
        trace_id=trace_id,
    )
    if isinstance(validation, JSONResponse):
        return validation
    course_id, actor_user_id = validation

    # Khóa row để status cũ và quyết định no-op không bị race với cập nhật khác.
    try:
        current = query_one(db, LOCK_ADMIN_COURSE_STATUS, {"course_id": course_id})
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course status lock query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if current is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(current, Mapping) or "status" not in current or (
        current.get("status") is not None and not isinstance(current.get("status"), str)
    ):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course current status projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    previous_status = current.get("status")
    # Lặp lại target hiện tại là idempotent no-op; không tạo audit duplicate.
    if previous_status != course_data.status:
        try:
            updated = query_one(
                db,
                UPDATE_ADMIN_COURSE_STATUS,
                {"course_id": course_id, "status": course_data.status},
            )
        except SQLAlchemyError:
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin course status update failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        if updated is None:
            _rollback_safely(db, trace_id=trace_id)
            return _not_found(trace_id)
        if (
            not isinstance(updated, Mapping)
            or type(updated.get("id")) is not int
            or updated.get("id") != course_id
            or updated.get("status") != course_data.status
        ):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin course status update result failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)

        # Ghi old/new status và actor cùng transaction để không commit thiếu audit.
        try:
            execute_query(
                db,
                INSERT_ADMIN_COURSE_STATUS_AUDIT,
                {
                    "course_id": course_id,
                    "actor_user_id": actor_user_id,
                    "previous_status": previous_status,
                    "new_status": course_data.status,
                },
            )
        except SQLAlchemyError:
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin course status audit insert failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)

    # Đọc Course/mentor projection trong cùng transaction trước khi commit.
    try:
        course_row = query_one(db, FIND_ADMIN_COURSE_DETAIL, {"course_id": course_id})
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course status projection query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if not isinstance(course_row, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course status projection missing; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    course = _map_updated_course(course_row, requested_course_id=course_id)
    if course is None or course.status != course_data.status:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course status mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Catalog yêu cầu Page<Course>; by-ID response theo singleton convention #74/#75.
    try:
        page = CoursePage(
            items=[course],
            pagination=Pagination(page=1, size=1, total=1, total_pages=1),
        )
    except (TypeError, ValidationError):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course status page mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Commit status và audit chỉ sau khi response projection đã được xác thực.
    try:
        db.commit()
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course status commit failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_UPDATED",
        message="Course status updated.",
        trace_id=trace_id,
        data=page.model_dump(mode="json"),
    )
