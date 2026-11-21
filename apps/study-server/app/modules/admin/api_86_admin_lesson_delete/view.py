"""Điều phối quyền, dependency policy và transaction xóa mềm Lesson API #86."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from datetime import datetime
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.admin.api_86_admin_lesson_delete.models import DeleteResult
from app.modules.admin.api_86_admin_lesson_delete.query import (
    CHECK_ADMIN_LESSON_DELETE_DEPENDENCIES,
    LOCK_ADMIN_LESSON_FOR_DELETE,
    SOFT_DELETE_ADMIN_LESSON,
)
from app.modules.admin.api_86_admin_lesson_delete.validate import (
    validate_admin_lesson_delete_request,
)
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
MAX_INT64 = 2**63 - 1


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi truy vấn, mapping hoặc commit thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Lesson could not be deleted.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 khi Lesson vắng mặt hoặc đã có tombstone."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Lesson not found.",
        trace_id=trace_id,
    )


def _dependency_conflict(trace_id: str) -> JSONResponse:
    """Dựng lỗi 422 an toàn khi Lesson còn progress hoặc liên kết nội dung."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Lesson with progress or linked resources cannot be deleted.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction mà không đưa chi tiết database vào HTTP response."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin lesson delete rollback failed; trace_id=%s", trace_id)


def _map_delete_result(row: Mapping[str, Any], *, lesson_id: int) -> DeleteResult | None:
    """Kiểm tra Lesson identity và timestamp đã persist trước commit."""

    result_id = row.get("id")
    deleted_at = row.get("deleted_at")
    if (
        type(result_id) is not int
        or not 1 <= result_id <= MAX_INT64
        or result_id != lesson_id
        or not isinstance(deleted_at, datetime)
    ):
        return None
    try:
        return DeleteResult(id=result_id, status="deleted", deleted_at=deleted_at)
    except (TypeError, ValidationError):
        return None


# API #86 admin_lesson_delete
def delete_admin_lesson(
    *,
    authorization: str | None,
    lesson_id_value: str,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN, kiểm tra liên kết rồi xóa mềm Lesson trong một transaction."""

    # Xác thực principal và path trước khi khóa hoặc đọc Lesson.
    validation = validate_admin_lesson_delete_request(
        authorization,
        lesson_id_value,
        trace_id=trace_id,
    )
    if isinstance(validation, JSONResponse):
        return validation
    lesson_id = validation

    # Khóa Lesson chưa bị xóa để tránh cạnh tranh giữa dependency-check và mutation.
    try:
        current = query_one(db, LOCK_ADMIN_LESSON_FOR_DELETE, {"lesson_id": lesson_id})
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin lesson delete lock query failed; trace_id=%s", trace_id)
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
        logger.error("Admin lesson delete lock projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # EXISTS kiểm tra progress và hai relation nội dung mà không tải dữ liệu riêng tư.
    try:
        dependency = query_one(
            db,
            CHECK_ADMIN_LESSON_DELETE_DEPENDENCIES,
            {"lesson_id": lesson_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin lesson delete dependency query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    dependency_keys = ("has_progress", "has_resources", "has_uploads")
    if not isinstance(dependency, Mapping) or any(
        type(dependency.get(key)) is not bool for key in dependency_keys
    ):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin lesson delete dependency projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if any(dependency[key] for key in dependency_keys):
        _rollback_safely(db, trace_id=trace_id)
        return _dependency_conflict(trace_id)

    # Ghi tombstone và lấy timestamp do database lưu làm deleted_at trong response.
    try:
        deleted_row = query_one(db, SOFT_DELETE_ADMIN_LESSON, {"lesson_id": lesson_id})
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin lesson soft-delete query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if deleted_row is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(deleted_row, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin lesson delete result projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    result = _map_delete_result(deleted_row, lesson_id=lesson_id)
    if result is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin lesson delete result mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    response_data = result.model_dump(mode="json")

    # Commit sau khi DeleteResult đã hợp lệ; lỗi commit sẽ rollback transaction.
    try:
        db.commit()
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin lesson delete commit failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_DELETED",
        message="Lesson deleted.",
        trace_id=trace_id,
        data=response_data,
    )
