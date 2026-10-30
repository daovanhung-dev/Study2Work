"""Điều phối xác thực, UPDATE transaction và response cho API #70."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from datetime import datetime
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.admin.api_70_admin_user_update.models import AdminUserUpdateRequest
from app.modules.admin.api_70_admin_user_update.query import UPDATE_ADMIN_USER
from app.modules.admin.api_70_admin_user_update.validate import (
    validate_admin_user_update_request,
)
from app.modules.guest.api_04_users_me.models import UserProfile
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
MAX_INT64 = 2**63 - 1


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi query, mapping hoặc commit API #70 thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="User could not be updated.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng 404 catalog khi user ID hợp lệ không có row được cập nhật."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="User not found.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction lỗi mà không đưa dữ liệu nội bộ vào log hoặc response."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin user update rollback failed; trace_id=%s", trace_id)


def _map_updated_user(
    row: Mapping[str, Any],
    *,
    requested_user_id: int,
) -> UserProfile | None:
    """Kiểm tra projection UPDATE RETURNING và giới hạn output vào UserProfile an toàn."""

    if (
        type(row.get("id")) is not int
        or not 1 <= row["id"] <= MAX_INT64
        or row["id"] != requested_user_id
        or not isinstance(row.get("full_name"), str)
        or not isinstance(row.get("email"), str)
        or not isinstance(row.get("role"), str)
        or not isinstance(row.get("status"), str)
        or (row.get("avatar_url") is not None and not isinstance(row.get("avatar_url"), str))
        or (row.get("phone") is not None and not isinstance(row.get("phone"), str))
        or not isinstance(row.get("created_at"), datetime)
        or not isinstance(row.get("updated_at"), datetime)
    ):
        return None
    try:
        return UserProfile.model_validate(row)
    except (TypeError, ValidationError):
        return None


# API #70 admin_user_update
def update_admin_user(
    *,
    authorization: str | None,
    user_id_value: str,
    user_data: AdminUserUpdateRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN, cập nhật profile/role an toàn rồi commit sau khi map response."""

    # Xác thực quyền Admin và chuẩn hóa input trước khi truy cập user row.
    validation = validate_admin_user_update_request(
        authorization,
        user_id_value,
        user_data,
        trace_id=trace_id,
    )
    if isinstance(validation, JSONResponse):
        return validation
    user_id, user_data = validation

    # Chạy một UPDATE theo primary key, chỉ ghi các trường candidate của API #70.
    try:
        row = query_one(
            db,
            UPDATE_ADMIN_USER,
            {
                "user_id": user_id,
                "full_name": user_data.full_name,
                "phone": user_data.phone,
                "avatar_url": user_data.avatar_url,
                "role": user_data.role,
            },
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin user update query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # No row biểu diễn user không tồn tại; không ghi status hoặc lifecycle của API khác.
    if row is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(row, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin user update projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Kiểm tra safe projection trước commit để lỗi mapping không lưu mutation một phần.
    profile = _map_updated_user(row, requested_user_id=user_id)
    if profile is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin user update mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Commit mutation sau khi projection hợp lệ; dependency chỉ đóng session.
    try:
        db.commit()
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin user update commit failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_UPDATED",
        message="User updated.",
        trace_id=trace_id,
        data=profile.model_dump(mode="json"),
    )
