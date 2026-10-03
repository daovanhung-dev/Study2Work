"""Điều phối xác thực, cập nhật transaction và dựng response hồ sơ cho API #14."""

from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_one
from app.core.responses import ApiError, success_response
from app.modules.guest.api_04_users_me.models import UserProfile
from app.modules.guest.api_14_users_me_profile.models import ProfileUpdateRequest
from app.modules.guest.api_14_users_me_profile.query import UPDATE_CURRENT_USER_PROFILE
from app.modules.guest.api_14_users_me_profile.validate import (
    validate_profile_update_request,
)
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def update_current_user_profile(
    db: Session,
    *,
    user_id: int,
    user_data: ProfileUpdateRequest,
) -> dict[str, Any] | None:
    """Cập nhật các cột profile source-backed và trả hàng an toàn bằng UPDATE RETURNING."""

    return query_one(
        db,
        UPDATE_CURRENT_USER_PROFILE,
        {
            "user_id": user_id,
            "full_name": user_data.full_name,
            "phone": user_data.phone,
            "avatar_url": user_data.avatar_url,
        },
    )


# API #14 users_me_profile
def update_profile(
    *,
    authorization: str | None,
    user_data: ProfileUpdateRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Student, cập nhật profile theo JWT subject và commit sau khi mapping an toàn."""

    validation = validate_profile_update_request(
        authorization,
        user_data,
        trace_id=trace_id,
    )
    if isinstance(validation, JSONResponse):
        return validation
    user_id, user_data = validation

    try:
        updated_user = update_current_user_profile(
            db,
            user_id=user_id,
            user_data=user_data,
        )
        if updated_user is None:
            db.rollback()
            return _authentication_error(trace_id)

        profile = UserProfile.model_validate(updated_user)
        db.commit()
    except ValidationError:
        db.rollback()
        logger.exception("Updated profile mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Profile update database error; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_UPDATED",
        message="Profile updated.",
        trace_id=trace_id,
        data=profile.model_dump(mode="json"),
    )


def _authentication_error(trace_id: str) -> JSONResponse:
    """Trả lỗi xác thực khi JWT subject không còn ánh xạ tới user trong database."""

    return ApiError(
        status_code=401,
        business_code="DESIGN_AUTHENTICATION_REQUIRED",
        message="Authentication required.",
        trace_id=trace_id,
    )


def _internal_error(trace_id: str) -> JSONResponse:
    """Trả lỗi nội bộ an toàn khi update, mapping hoặc commit profile thất bại."""

    return ApiError(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Profile could not be updated.",
        trace_id=trace_id,
    )
