"""Điều phối quyền, dependency check và soft-delete Content cho API #53."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from datetime import datetime
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.mentor.api_53_mentor_content_delete.models import DeleteResult
from app.modules.mentor.api_53_mentor_content_delete.query import (
    HAS_ACTIVE_CHILD_CONTENT,
    LOCK_MENTOR_CONTENT,
    SOFT_DELETE_CONTENT,
)
from app.modules.mentor.api_53_mentor_content_delete.validate import parse_content_id
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn cho lookup, soft-delete hoặc mapping thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Content could not be deleted.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 cho Content ID sai hoặc không còn hoạt động."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Content not found.",
        trace_id=trace_id,
    )


def _access_denied(trace_id: str) -> JSONResponse:
    """Dựng lỗi 403 khi Mentor không sở hữu course chứa Content."""

    return error_response(
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message="Access denied.",
        trace_id=trace_id,
    )


def _validation_error(trace_id: str, *, message: str) -> JSONResponse:
    """Dựng lỗi 422 cho guard dependency hoặc publication DERIVED."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message=message,
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction đang mở mà không thay response lỗi ban đầu."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Content deletion rollback failed; trace_id=%s", trace_id)


def _valid_content_projection(row: Mapping[str, Any], *, content_id: int) -> bool:
    """Kiểm tra projection cần cho ownership, lifecycle guard và DELETE result."""

    if (
        row.get("id") != content_id
        or type(row.get("course_id")) is not int
        or "mentor_id" not in row
        or type(row.get("status")) is not str
    ):
        return False
    mentor_id = row.get("mentor_id")
    return mentor_id is None or type(mentor_id) is int


def _map_delete_result(row: Mapping[str, Any], *, content_id: int) -> DeleteResult | None:
    """Xác minh UPDATE RETURNING trước khi commit và dựng schema catalog."""

    result_id = row.get("id")
    deleted_at = row.get("deleted_at")
    if (
        type(result_id) is not int
        or result_id != content_id
        or not isinstance(deleted_at, datetime)
    ):
        return None
    try:
        return DeleteResult(
            id=result_id,
            status="deleted",
            deleted_at=deleted_at,
        )
    except (TypeError, ValidationError):
        return None


def delete_content(
    *,
    authorization: str | None,
    content_id_value: str,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Mentor, kiểm tra điều kiện và soft-delete một Content."""

    # Xác thực Bearer, numeric subject và MENTOR role trước khi truy cập database.
    authentication = validate_current_user_request(
        authorization,
        role="MENTOR",
        trace_id=trace_id,
        internal_error_message="Content could not be deleted.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    mentor_id, _roles = authentication

    # Giữ raw path để cùng quy ước Content APIs: ID sai format/range trả 404.
    content_id = parse_content_id(content_id_value)
    if content_id is None:
        return _not_found(trace_id)

    # Khóa Content cùng Course; API #50 cũng khóa Course trước insert Content.
    try:
        current = query_one(db, LOCK_MENTOR_CONTENT, {"content_id": content_id})
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content deletion lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if current is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(current, Mapping) or not _valid_content_projection(
        current,
        content_id=content_id,
    ):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content deletion access projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if current.get("mentor_id") != mentor_id:
        _rollback_safely(db, trace_id=trace_id)
        return _access_denied(trace_id)

    course_id = current["course_id"]
    if current["status"] == "PUBLISHED":
        _rollback_safely(db, trace_id=trace_id)
        return _validation_error(
            trace_id,
            message="Unpublish Content before deleting it.",
        )

    # Chặn xóa parent đang có child active để API #49 không nhận cây thiếu parent.
    try:
        dependency = query_one(
            db,
            HAS_ACTIVE_CHILD_CONTENT,
            {"content_id": content_id, "course_id": course_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content dependency lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if not isinstance(dependency, Mapping) or type(dependency.get("has_active_child")) is not bool:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content dependency projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if dependency["has_active_child"]:
        _rollback_safely(db, trace_id=trace_id)
        return _validation_error(
            trace_id,
            message="Delete active child Content before deleting its parent.",
        )

    try:
        deleted = query_one(
            db,
            SOFT_DELETE_CONTENT,
            {"content_id": content_id, "course_id": course_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content soft-delete failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if not isinstance(deleted, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content soft-delete returned no row; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    result = _map_delete_result(deleted, content_id=content_id)
    if result is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content delete result mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    response_data = result.model_dump(mode="json")

    # Commit only after the returned tombstone timestamp validates against DeleteResult.
    try:
        db.commit()
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content deletion commit failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_DELETED",
        message="Content deleted.",
        trace_id=trace_id,
        data=response_data,
    )
