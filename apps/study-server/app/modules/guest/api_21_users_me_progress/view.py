"""Điều phối nghiệp vụ cho API #21 lấy tiến độ tổng hợp."""

from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.guest.api_21_users_me_progress.models import UserProfile
from app.modules.guest.api_21_users_me_progress.query import FIND_CURRENT_USER_PROFILE
from app.modules.guest.api_21_users_me_progress.validate import validate_progress_request
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def find_current_user(db: Session, *, user_id: int) -> dict[str, Any] | None:
    """Truy vấn thông tin hồ sơ của người dùng hiện tại theo user_id."""
    return query_one(db, FIND_CURRENT_USER_PROFILE, {"user_id": user_id})


def _authentication_error(trace_id: str) -> JSONResponse:
    return error_response(
        status_code=401,
        business_code="DESIGN_AUTHENTICATION_REQUIRED",
        message="Authentication required.",
        trace_id=trace_id,
    )


def _internal_error(trace_id: str) -> JSONResponse:
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Progress could not be retrieved.",
        trace_id=trace_id,
    )


# API #21 users_me_progress
def get_user_progress(
    *,
    authorization: str | None = None,
    course_id: str | None = None,
    aggregate: str | None = None,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Lấy thông tin tiến độ tổng hợp cho học viên hiện tại."""
    # Xác thực token Bearer và quyền Student của người dùng.
    validation = validate_progress_request(authorization, trace_id=trace_id)
    if isinstance(validation, JSONResponse):
        return validation
    user_id = validation

    # Truy vấn dữ liệu người dùng từ cơ sở dữ liệu.
    try:
        user = find_current_user(db, user_id=user_id)
    except Exception:
        db.rollback()
        logger.exception("User lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Kiểm tra xem người dùng có tồn tại trong hệ thống hay không.
    if user is None:
        return _authentication_error(trace_id)

    # Ánh xạ dữ liệu sang model phản hồi chuẩn.
    try:
        profile = UserProfile.model_validate(user)
    except Exception:
        logger.exception("User profile mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả về kết quả thành công HTTP 200.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Progress retrieved.",
        trace_id=trace_id,
        data=profile.model_dump(mode="json"),
    )

