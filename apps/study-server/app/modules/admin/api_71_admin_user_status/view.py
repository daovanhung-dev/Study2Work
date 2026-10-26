"""Điều phối xác thực, khóa trạng thái, thu hồi refresh token và response API #71."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from datetime import datetime
from typing import Any

from app.core.database import execute_query, query_one
from app.core.responses import ErrorDetail, error_response, success_response
from app.modules.admin.api_71_admin_user_status.models import AdminUserStatusRequest
from app.modules.admin.api_71_admin_user_status.query import (
    LOCK_ADMIN_USER_STATUS,
    REVOKE_ADMIN_USER_REFRESH_TOKENS,
    UPDATE_ADMIN_USER_STATUS,
)
from app.modules.admin.api_71_admin_user_status.validate import (
    validate_admin_user_status_request,
)
from app.modules.guest.api_04_users_me.models import UserProfile
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
MAX_INT64 = 2**63 - 1
SUPPORTED_ACCOUNT_STATUSES = {"ACTIVE", "SUSPENDED"}


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn cho query, mapping, revoke hoặc commit API #71."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="User status could not be updated.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 catalog khi user ID hợp lệ không có bản ghi."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="User not found.",
        trace_id=trace_id,
    )


def _unsupported_current_status(trace_id: str) -> JSONResponse:
    """Báo 422 khi trạng thái hiện tại thuộc luồng xác minh hoặc lifecycle khác."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Trạng thái hiện tại không thể đổi qua thao tác khóa/mở khóa.",
        trace_id=trace_id,
        errors=[
            ErrorDetail(
                field="status",
                code="VALUE_ERROR",
                message="Current account status is not lockable through this endpoint",
            )
        ],
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction lỗi mà không đưa dữ liệu nội bộ vào response hoặc log."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin user status rollback failed; trace_id=%s", trace_id)


def _map_user_profile(
    row: Mapping[str, Any],
    *,
    requested_user_id: int,
    expected_status: str,
) -> UserProfile | None:
    """Kiểm tra UPDATE RETURNING và giới hạn response vào safe UserProfile fields."""

    if (
        type(row.get("id")) is not int
        or not 1 <= row["id"] <= MAX_INT64
        or row["id"] != requested_user_id
        or not isinstance(row.get("full_name"), str)
        or not isinstance(row.get("email"), str)
        or not isinstance(row.get("role"), str)
        or row.get("status") != expected_status
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


# API #71 admin_user_status
def update_admin_user_status(
    *,
    authorization: str | None,
    user_id_value: str,
    user_data: AdminUserStatusRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN, cập nhật account status và thu hồi refresh token khi khóa."""

    # Xác thực principal và path trước mọi thao tác đọc/ghi user.
    validation = validate_admin_user_status_request(
        authorization,
        user_id_value,
        user_data,
        trace_id=trace_id,
    )
    if isinstance(validation, JSONResponse):
        return validation
    user_id, user_data = validation

    # Khóa row để đọc trạng thái hiện tại và tránh chuyển các trạng thái lifecycle khác.
    try:
        current = query_one(db, LOCK_ADMIN_USER_STATUS, {"user_id": user_id})
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin user status lock query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Không tìm thấy resource dùng 404; projection sai là lỗi nội bộ, trạng thái khác là 422.
    if current is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(current, Mapping) or not isinstance(current.get("status"), str):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin user current status projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if current["status"] not in SUPPORTED_ACCOUNT_STATUSES:
        _rollback_safely(db, trace_id=trace_id)
        return _unsupported_current_status(trace_id)

    # Cập nhật trạng thái và timestamp trên user row, chỉ trả safe profile fields.
    try:
        row = query_one(
            db,
            UPDATE_ADMIN_USER_STATUS,
            {"user_id": user_id, "status": user_data.status},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin user status update failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Row lock giữ user tồn tại trong transaction; xử lý zero-row theo catalog 404.
    if row is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(row, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin user status returned projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Xác thực response trước token side effect để không commit dữ liệu không map được.
    profile = _map_user_profile(
        row,
        requested_user_id=user_id,
        expected_status=user_data.status,
    )
    if profile is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin user status profile mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Khi khóa tài khoản, thu hồi refresh credentials còn hiệu lực cùng transaction.
    if user_data.status == "SUSPENDED":
        try:
            execute_query(db, REVOKE_ADMIN_USER_REFRESH_TOKENS, {"user_id": user_id})
        except SQLAlchemyError:
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin user refresh-token revoke failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)

    # Commit status và revoke cùng lúc; activation không khôi phục token đã revoke.
    try:
        db.commit()
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin user status commit failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_UPDATED",
        message="User status updated.",
        trace_id=trace_id,
        data=profile.model_dump(mode="json"),
    )
