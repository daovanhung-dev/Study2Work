"""Xác thực Admin, path ID và body cập nhật cho API #70."""

from __future__ import annotations

import re

import app.utils.auth as auth_utils
from app.core.responses import ErrorDetail, error_response
from app.modules.admin.api_70_admin_user_update.models import AdminUserUpdateRequest
from starlette.responses import JSONResponse

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1
_SIGNED_INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+\Z")


def parse_admin_update_user_id(value: str) -> int | None:
    """Trả user ID signed-int64 hoặc None nếu path sai định dạng/vượt miền."""

    if len(value) > 20 or _SIGNED_INTEGER_PATTERN.fullmatch(value) is None:
        return None
    user_id = int(value)
    if not INT64_MIN <= user_id <= INT64_MAX:
        return None
    return user_id


def validate_admin_user_update_request(
    authorization: str | None,
    user_id_value: str,
    user_data: AdminUserUpdateRequest,
    *,
    trace_id: str,
) -> tuple[int, AdminUserUpdateRequest] | JSONResponse:
    """Yêu cầu ADMIN rồi parse path và chuẩn hóa full-replacement body candidate."""

    authentication = auth_utils.validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="User could not be updated.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication

    user_id = parse_admin_update_user_id(user_id_value)
    if user_id is None:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Dữ liệu đầu vào không hợp lệ.",
            trace_id=trace_id,
            errors=[
                ErrorDetail(
                    field="user_id",
                    code="INT_PARSING",
                    message="Input should be a valid signed 64-bit integer",
                )
            ],
        )

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
    """Trim giá trị nullable và chuẩn hóa chuỗi trắng thành None như API #14."""

    if value is None:
        return None
    normalized = value.strip()
    return normalized or None
