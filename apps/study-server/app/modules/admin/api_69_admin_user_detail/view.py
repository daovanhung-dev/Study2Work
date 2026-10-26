"""Điều phối quyền Admin, đọc user profile và dựng response API #69."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.admin.api_69_admin_user_detail.query import FIND_ADMIN_USER
from app.modules.admin.api_69_admin_user_detail.validate import (
    parse_admin_user_id,
    validate_admin_request,
)
from app.modules.guest.api_04_users_me.models import UserProfile
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
MAX_INT64 = 2**63 - 1


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn cho query hoặc mapping API #69."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="User could not be retrieved.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 catalog cho path ID sai hoặc user không tồn tại."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="User not found.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction đọc lỗi mà không làm lộ exception nội bộ."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin user detail rollback failed; trace_id=%s", trace_id)


def _map_user_profile(row: Mapping[str, Any], *, requested_user_id: int) -> UserProfile | None:
    """Kiểm tra projection user và ánh xạ qua safe UserProfile model dùng chung."""

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
    ):
        return None
    try:
        return UserProfile.model_validate(row)
    except (TypeError, ValidationError):
        return None


# API #69 admin_user_detail
def get_admin_user(
    *,
    authorization: str | None,
    user_id_value: str,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN, đọc một user theo int64 ID và trả UserProfile an toàn."""

    # Xác thực principal và role trước khi parse path hoặc query user data.
    authentication = validate_admin_request(authorization, trace_id=trace_id)
    if isinstance(authentication, JSONResponse):
        return authentication

    # Parse raw path để giữ nguyên error set catalog, không phát sinh HTTP 422.
    user_id = parse_admin_user_id(user_id_value)
    if user_id is None:
        return _not_found(trace_id)

    # Đọc duy nhất projection profile được phép trả về bằng bind parameter.
    try:
        row = query_one(db, FIND_ADMIN_USER, {"user_id": user_id})
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin user detail query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Không có row biểu diễn resource không tồn tại theo contract detail.
    if row is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(row, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin user detail projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Kiểm tra và serialize allowlist; không trả thêm credential từ row.
    profile = _map_user_profile(row, requested_user_id=user_id)
    if profile is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin user detail mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả response chỉ đọc; Session và transaction lifecycle thuộc dependency.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="User retrieved.",
        trace_id=trace_id,
        data=profile.model_dump(mode="json"),
    )
