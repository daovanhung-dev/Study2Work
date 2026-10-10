"""Kiểm tra và chuẩn hóa dữ liệu đăng nhập, làm mới phiên API #3."""

from __future__ import annotations

from app.core.responses import ErrorDetail, error_response
from app.modules.guest.api_03_auth_login.models import LoginRequest, RefreshRequest
from app.utils.validate import normalize_email
from starlette.responses import JSONResponse


def validate_login_request(
    user_data: LoginRequest,
    *,
    trace_id: str,
) -> LoginRequest | JSONResponse:
    """Chuẩn hóa email đăng nhập và từ chối thông tin xác thực chỉ có khoảng trắng."""

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
    if not user_data.password.strip():
        errors.append(
            ErrorDetail(
                field="password",
                code="VALUE_ERROR",
                message="Value error, Mật khẩu không được để trống.",
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
    return user_data.model_copy(update={"email": email})


def validate_refresh_request(
    user_data: RefreshRequest,
    *,
    trace_id: str,
) -> RefreshRequest | JSONResponse:
    """Từ chối refresh token rỗng hoặc chỉ có khoảng trắng."""

    if user_data.refresh_token.strip():
        return user_data
    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Dữ liệu đầu vào không hợp lệ.",
        trace_id=trace_id,
        errors=[
            ErrorDetail(
                field="refresh_token",
                code="VALUE_ERROR",
                message="Value error, Giá trị không được để trống.",
            )
        ],
    )
