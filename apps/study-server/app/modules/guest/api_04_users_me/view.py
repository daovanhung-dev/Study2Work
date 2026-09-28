"""Điều phối xác thực bearer/JWT, kiểm tra quyền Student, đọc hồ sơ và dựng response cho API
người dùng hiện tại."""

from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_one
from app.core.responses import ApiError, success_response
from app.modules.guest.api_04_users_me.models import UserProfile
from app.modules.guest.api_04_users_me.query import CURRENT_USER_PROFILE
from app.modules.guest.api_04_users_me.validate import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def find_current_user(db: Session, *, user_id: int) -> dict[str, Any] | None:
    """Đọc các cột profile công khai theo user ID bằng truy vấn CURRENT_USER_PROFILE. Trả hàng dữ
    liệu hoặc None nếu không tìm thấy và không commit Session."""

    return query_one(db, CURRENT_USER_PROFILE, {"user_id": user_id})


# API #04 users_me
def get_current_user(
    *,
    authorization: str | None,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Lấy bearer token, giải mã JWT, kiểm tra subject/roles rồi yêu cầu role STUDENT trước khi đọc
    profile. Hàm ánh xạ lỗi xác thực, quyền, database hoặc model thành JSONResponse an toàn; hồ sơ
    hợp lệ được tuần tự hóa thành success envelope."""

    authentication = validate_current_user_request(
        authorization,
        trace_id=trace_id,
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    user_id, _roles = authentication

    try:
        user = find_current_user(db, user_id=user_id)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Current-user lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if user is None:
        return _authentication_error(trace_id)

    try:
        profile = UserProfile.model_validate(user)
    except ValidationError:
        logger.exception("Current-user profile mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Profile retrieved.",
        trace_id=trace_id,
        data=profile.model_dump(mode="json"),
    )


def _authentication_error(trace_id: str) -> JSONResponse:
    """Tạo JSONResponse HTTP 401 với business code xác thực, thông điệp mặc định an toàn và trace ID
    của request."""
    return ApiError(
        status_code=401,
        business_code="DESIGN_AUTHENTICATION_REQUIRED",
        message="Authentication required.",
        trace_id=trace_id,
    )


def _internal_error(trace_id: str) -> JSONResponse:
    """Tạo JSONResponse HTTP 500 với business code nội bộ của API #4, message an toàn và trace ID đã
    nhận."""
    return ApiError(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Profile could not be retrieved.",
        trace_id=trace_id,
    )
