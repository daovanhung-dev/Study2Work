"""Điều phối quyền Admin, dependency policy và soft-delete course API #77."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from datetime import datetime
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.admin.api_77_admin_course_delete.models import DeleteResult
from app.modules.admin.api_77_admin_course_delete.query import (
    CHECK_ADMIN_COURSE_DELETE_DEPENDENCIES,
    LOCK_ADMIN_COURSE_FOR_DELETE,
    SOFT_DELETE_ADMIN_COURSE,
)
from app.modules.admin.api_77_admin_course_delete.validate import (
    validate_admin_course_delete_request,
)
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
MAX_INT64 = 2**63 - 1


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn cho query, mapping hoặc commit API #77."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Course could not be deleted.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi catalog 404 cho course thiếu hoặc đã soft-delete."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Course not found.",
        trace_id=trace_id,
    )


def _dependency_conflict(trace_id: str) -> JSONResponse:
    """Dựng lỗi 422 an toàn khi course còn enrollment hoặc nội dung học tập."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Course with enrollments or content cannot be deleted.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction lỗi mà không đưa exception database vào response."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin course delete rollback failed; trace_id=%s", trace_id)


def _map_delete_result(row: Mapping[str, Any], *, course_id: int) -> DeleteResult | None:
    """Kiểm tra ID và persisted timestamp trước khi commit mutation."""

    result_id = row.get("id")
    deleted_at = row.get("deleted_at")
    if (
        type(result_id) is not int
        or not 1 <= result_id <= MAX_INT64
        or result_id != course_id
        or not isinstance(deleted_at, datetime)
    ):
        return None
    try:
        return DeleteResult(id=result_id, status="deleted", deleted_at=deleted_at)
    except (TypeError, ValidationError):
        return None


def delete_admin_course(
    *,
    authorization: str | None,
    course_id_value: str,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN, kiểm tra dependency và soft-delete course theo policy local."""

    # Xác thực principal và role trước path parsing hoặc truy cập course.
    validation = validate_admin_course_delete_request(
        authorization,
        course_id_value,
        trace_id=trace_id,
    )
    if isinstance(validation, JSONResponse):
        return validation
    course_id = validation

    try:
        locked_course = query_one(db, LOCK_ADMIN_COURSE_FOR_DELETE, {"course_id": course_id})
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course delete lock query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if locked_course is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if (
        not isinstance(locked_course, Mapping)
        or type(locked_course.get("id")) is not int
        or locked_course.get("id") != course_id
    ):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course delete lock projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    try:
        dependency = query_one(
            db,
            CHECK_ADMIN_COURSE_DELETE_DEPENDENCIES,
            {"course_id": course_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course delete dependency query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if (
        not isinstance(dependency, Mapping)
        or type(dependency.get("has_enrollments")) is not bool
        or type(dependency.get("has_content")) is not bool
    ):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course delete dependency projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if dependency["has_enrollments"] or dependency["has_content"]:
        _rollback_safely(db, trace_id=trace_id)
        return _dependency_conflict(trace_id)

    try:
        deleted_row = query_one(db, SOFT_DELETE_ADMIN_COURSE, {"course_id": course_id})
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course soft-delete query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if deleted_row is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(deleted_row, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course delete result projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    result = _map_delete_result(deleted_row, course_id=course_id)
    if result is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course delete result mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    response_data = result.model_dump(mode="json")

    try:
        db.commit()
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin course delete commit failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_DELETED",
        message="Course deleted.",
        trace_id=trace_id,
        data=response_data,
    )
