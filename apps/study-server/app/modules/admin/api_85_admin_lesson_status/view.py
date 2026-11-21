"""Điều phối Admin auth, Lesson status/audit transaction và response API #85."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import execute_query, query_one
from app.core.responses import error_response, success_response
from app.modules.admin.api_85_admin_lesson_status.models import AdminLessonStatusRequest
from app.modules.admin.api_85_admin_lesson_status.query import (
    INSERT_ADMIN_LESSON_STATUS_AUDIT,
    LOCK_ADMIN_LESSON_STATUS,
    UPDATE_ADMIN_LESSON_STATUS,
)
from app.modules.admin.api_85_admin_lesson_status.validate import (
    validate_admin_lesson_status_request,
)
from app.modules.guest.api_09_courses_curriculum.models import Lesson
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
MAX_INT64 = 2**63 - 1


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi khóa, cập nhật, audit, map hoặc commit thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Lesson status could not be updated.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 catalog khi UPDATE/lock không tìm thấy Lesson."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Lesson not found.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction lỗi mà không che response ban đầu."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin lesson status rollback failed; trace_id=%s", trace_id)


def _map_lesson(row: Mapping[str, Any], *, requested_lesson_id: int) -> Lesson | None:
    """Kiểm tra identity rồi ánh xạ projection qua reusable Lesson API #09."""

    lesson_id = row.get("id")
    if (
        type(lesson_id) is not int
        or not 1 <= lesson_id <= MAX_INT64
        or lesson_id != requested_lesson_id
    ):
        return None

    try:
        return Lesson.model_validate(dict(row))
    except (TypeError, ValidationError):
        return None


# API #85 admin_lesson_status
def update_admin_lesson_status(
    *,
    authorization: str | None,
    lesson_id_value: str,
    lesson_data: AdminLessonStatusRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN, đổi Lesson status/audit atomic và trả Lesson trực tiếp."""

    # Xác thực principal và path trước khi khóa hoặc đọc Lesson.
    validation = validate_admin_lesson_status_request(
        authorization,
        lesson_id_value,
        lesson_data,
        trace_id=trace_id,
    )
    if isinstance(validation, JSONResponse):
        return validation
    lesson_id, actor_user_id = validation

    # Khóa row để status cũ và nhánh no-op không race với một lần đổi khác.
    try:
        current = query_one(db, LOCK_ADMIN_LESSON_STATUS, {"lesson_id": lesson_id})
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin lesson status lock query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if current is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if (
        not isinstance(current, Mapping)
        or type(current.get("id")) is not int
        or current.get("id") != lesson_id
        or current.get("status") is not None
        and not isinstance(current.get("status"), str)
    ):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin lesson current status projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    previous_status = current.get("status")
    if previous_status == lesson_data.status:
        # Lặp lại target hiện tại là idempotent no-op, không append audit trùng.
        lesson = _map_lesson(current, requested_lesson_id=lesson_id)
        if lesson is None:
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin lesson no-op mapping failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)
    else:
        # Chỉ đổi status và timestamp; giữ metadata và quan hệ của Lesson.
        try:
            updated = query_one(
                db,
                UPDATE_ADMIN_LESSON_STATUS,
                {"lesson_id": lesson_id, "status": lesson_data.status},
            )
        except SQLAlchemyError:
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin lesson status update failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        if updated is None:
            _rollback_safely(db, trace_id=trace_id)
            return _not_found(trace_id)
        if not isinstance(updated, Mapping):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin lesson status update projection failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)

        lesson = _map_lesson(updated, requested_lesson_id=lesson_id)
        if lesson is None or lesson.status != lesson_data.status:
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin lesson status mapping failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)

        # Append old/new status và actor trong cùng transaction với UPDATE.
        try:
            execute_query(
                db,
                INSERT_ADMIN_LESSON_STATUS_AUDIT,
                {
                    "lesson_id": lesson_id,
                    "actor_user_id": actor_user_id,
                    "previous_status": previous_status,
                    "new_status": lesson_data.status,
                },
            )
        except SQLAlchemyError:
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin lesson status audit insert failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)

    # Commit chỉ sau khi response projection và mọi mutation đều hợp lệ.
    try:
        db.commit()
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin lesson status commit failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_UPDATED",
        message="Lesson status updated.",
        trace_id=trace_id,
        data=lesson.model_dump(mode="json"),
    )
