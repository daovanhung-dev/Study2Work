"""Kiểm tra xác thực và dữ liệu cập nhật hồ sơ cho API #14."""

from __future__ import annotations

from app.core.responses import ErrorDetail, error_response
from app.modules.guest.api_04_users_me.validate import validate_current_user_request
from app.modules.guest.api_14_users_me_profile.models import ProfileUpdateRequest
from starlette.responses import JSONResponse


def validate_profile_update_request(
    authorization: str | None,
    user_data: ProfileUpdateRequest,
    *,
    trace_id: str,
) -> tuple[int, ProfileUpdateRequest] | JSONResponse:
    """Xác thực Student và chuẩn hóa các giá trị profile theo constraint database hiện tại."""

    authentication = validate_current_user_request(
        authorization,
        trace_id=trace_id,
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    user_id, _roles = authentication

    errors: list[ErrorDetail] = []
    full_name = user_data.full_name.strip()
    if not full_name:
        errors.append(
            ErrorDetail(
                field="full_name",
                code="STRING_TOO_SHORT",
                message="String should have at least 1 character",
            )
        )
    elif len(full_name) > 150:
        errors.append(
            ErrorDetail(
                field="full_name",
                code="STRING_TOO_LONG",
                message="String should have at most 150 characters",
            )
        )

    phone = _normalize_nullable_text(user_data.phone)
    if phone is not None and len(phone) > 20:
        errors.append(
            ErrorDetail(
                field="phone",
                code="STRING_TOO_LONG",
                message="String should have at most 20 characters",
            )
        )

    avatar_url = _normalize_nullable_text(user_data.avatar_url)
    if errors:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Dữ liệu đầu vào không hợp lệ.",
            trace_id=trace_id,
            errors=errors,
        )

    return user_id, user_data.model_copy(
        update={
            "full_name": full_name,
            "phone": phone,
            "avatar_url": avatar_url,
        }
    )


def _normalize_nullable_text(value: str | None) -> str | None:
    """Trim chuỗi nullable và đổi chuỗi chỉ có khoảng trắng thành None để xóa dữ liệu."""

    if value is None:
        return None
    normalized = value.strip()
    return normalized or None
