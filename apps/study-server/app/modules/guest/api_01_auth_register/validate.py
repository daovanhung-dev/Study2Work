"""Kiểm tra và chuẩn hóa dữ liệu đăng ký tài khoản API #1."""

from __future__ import annotations

from app.core.responses import ErrorDetail, error_response
from app.modules.guest.api_01_auth_register.models import RegisterRequest
from app.utils.validate import normalize_email
from starlette.responses import JSONResponse


def validate_register_request(
    user_data: RegisterRequest,
    *,
    trace_id: str,
) -> RegisterRequest | JSONResponse:
    """Chuẩn hóa dữ liệu đăng ký hoặc trả response 422 kèm chi tiết lỗi theo trường."""

    errors: list[ErrorDetail] = []
    email = user_data.email
    try:
        email = normalize_email(email, max_length=255)
    except ValueError as exc:
        message = str(exc)
        errors.append(
            ErrorDetail(
                field="email",
                code=(
                    "STRING_TOO_LONG"
                    if message.startswith("String should have at most")
                    else "VALUE_ERROR"
                ),
                message=message,
            )
        )

    password = user_data.password
    if not password.strip():
        errors.append(
            ErrorDetail(
                field="password",
                code="VALUE_ERROR",
                message="Value error, Mật khẩu không được để trống.",
            )
        )

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

    if errors:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Dữ liệu đầu vào không hợp lệ.",
            trace_id=trace_id,
            errors=errors,
        )

    return user_data.model_copy(
        update={"email": email, "full_name": full_name},
    )
