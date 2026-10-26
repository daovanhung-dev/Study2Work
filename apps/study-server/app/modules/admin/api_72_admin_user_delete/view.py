"""Điều phối quyền Admin, soft-delete user và response API #72."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from datetime import datetime
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.admin.api_72_admin_user_delete.models import DeleteResult
from app.modules.admin.api_72_admin_user_delete.query import SOFT_DELETE_ADMIN_USER
from app.modules.admin.api_72_admin_user_delete.validate import (
    validate_admin_user_delete_request,
)
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
MAX_INT64 = 2**63 - 1


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi update, mapping hoặc commit API #72 thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="User could not be deleted.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi catalog 404 khi user không tồn tại hoặc đã được đánh dấu DELETED."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="User not found.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction lỗi mà không đưa exception DB vào response."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin user delete rollback failed; trace_id=%s", trace_id)


def _map_delete_result(row: Mapping[str, Any], *, user_id: int) -> DeleteResult | None:
    """Kiểm tra ID và timestamp từ UPDATE RETURNING trước khi commit."""

    result_id = row.get("id")
    deleted_at = row.get("deleted_at")
    if (
        type(result_id) is not int
        or not 1 <= result_id <= MAX_INT64
        or result_id != user_id
        or not isinstance(deleted_at, datetime)
    ):
        return None
    try:
        return DeleteResult(id=result_id, status="deleted", deleted_at=deleted_at)
    except (TypeError, ValidationError):
        return None


# API #72 admin_user_delete
def delete_admin_user(
    *,
    authorization: str | None,
    user_id_value: str,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN, đánh dấu user DELETED và trả DeleteResult an toàn."""

    # Xác thực principal và role trước path parsing hoặc truy cập user row.
    validation = validate_admin_user_delete_request(
        authorization,
        user_id_value,
        trace_id=trace_id,
    )
    if isinstance(validation, JSONResponse):
        return validation
    user_id = validation

    # Chỉ đổi marker/timestamp trên users; các hàng phụ thuộc được giữ nguyên.
    try:
        row = query_one(db, SOFT_DELETE_ADMIN_USER, {"user_id": user_id})
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin user delete query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Không có RETURNING row nghĩa là user thiếu hoặc đã mang marker DELETED.
    if row is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(row, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin user delete projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Map event timestamp từ updated_at RETURNING trước khi commit mutation.
    result = _map_delete_result(row, user_id=user_id)
    if result is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin user delete result mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    response_data = result.model_dump(mode="json")

    # Commit chỉ sau khi DeleteResult hợp lệ; Session lifecycle thuộc dependency.
    try:
        db.commit()
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin user delete commit failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_DELETED",
        message="User deleted.",
        trace_id=trace_id,
        data=response_data,
    )
