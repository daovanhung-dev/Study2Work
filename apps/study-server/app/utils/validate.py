"""Cung cấp helper thuần để chuẩn hóa đầu vào và kiểm tra dữ liệu xác thực dùng lại trong Study
API."""

from collections.abc import Mapping
from typing import Any

from app.core.responses import ApiError, _ApiError


def strip_email(value: object) -> object:
    """Nếu đầu vào là chuỗi, loại khoảng trắng ở hai đầu để email được chuẩn hóa trước khi kiểm
    tra; kiểu dữ liệu khác được trả lại nguyên trạng để Pydantic báo lỗi phù hợp."""

    return value.strip() if isinstance(value, str) else value


def reject_blank_password(value: object) -> object:
    """Từ chối password là chuỗi chỉ chứa khoảng trắng bằng ValueError, còn giá trị hợp lệ hoặc
    kiểu khác được trả nguyên trạng cho validator tiếp theo."""

    if isinstance(value, str) and not value.strip():
        raise ValueError("Mật khẩu không được để trống.")
    return value


def reject_blank_value(value: object) -> object:
    """Từ chối chuỗi rỗng hoặc chỉ có khoảng trắng bằng ValueError. Các giá trị còn lại được giữ
    nguyên để caller tiếp tục xác thực."""

    if isinstance(value, str) and not value.strip():
        raise ValueError("Giá trị không được để trống.")
    return value


def normalize_login_email(value: object) -> object:
    """Tái sử dụng strip_email để chuẩn hóa email đăng nhập trước khi Pydantic kiểm tra định dạng.
    Hàm giữ nguyên kiểu dữ liệu không phải chuỗi."""

    return strip_email(value)


def validate_login_password(value: object) -> object:
    """Ủy quyền kiểm tra password đăng nhập cho reject_blank_password để mọi API dùng cùng quy tắc
    từ chối chuỗi chỉ có khoảng trắng."""

    return reject_blank_password(value)


def validate_refresh_token(value: object) -> object:
    """Ủy quyền kiểm tra refresh token cho reject_blank_value để từ chối token rỗng hoặc chỉ có
    khoảng trắng trước khi xử lý nghiệp vụ."""

    return reject_blank_value(value)


def extract_bearer_token(authorization: str | None) -> str:
    """Tách token từ Authorization header theo cú pháp gồm đúng hai phần và scheme Bearer không
    phân biệt hoa thường. Header thiếu hoặc sai định dạng phát sinh _ApiError 401; thành công
    trả phần token."""

    if authorization is None:
        raise _authentication_error("Authorization header is required")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise _authentication_error("Authorization header must use Bearer scheme")

    return parts[1]


def validate_access_claims(claims: Mapping[str, Any]) -> tuple[int, list[str]]:
    """Kiểm tra sub là user ID số nguyên dương và roles là danh sách chuỗi không rỗng, sau đó chuẩn
    hóa role thành chữ hoa. Trả bộ (user_id, roles); claim thiếu, sai kiểu hoặc không hợp lệ sẽ
    phát sinh _ApiError 401."""

    subject = claims.get("sub")
    if not isinstance(subject, str) or not subject:
        raise _authentication_error("JWT subject is missing")

    try:
        user_id = int(subject)
    except ValueError as exc:
        raise _authentication_error("JWT subject is not a numeric user ID") from exc

    if user_id <= 0:
        raise _authentication_error("JWT subject is not a positive user ID")

    raw_roles = claims.get("roles")
    if not isinstance(raw_roles, list) or not raw_roles:
        raise _authentication_error("JWT roles are missing")

    if not all(isinstance(role, str) and role.strip() for role in raw_roles):
        raise _authentication_error("JWT roles are invalid")

    roles = [role.strip().upper() for role in raw_roles]
    return user_id, roles


def _authentication_error(message: str) -> _ApiError:
    """Tạo _ApiError HTTP 401 với business code yêu cầu xác thực và message do caller cung cấp để
    các validator dùng chung một cách ánh xạ lỗi."""
    return ApiError(
        status_code=401,
        business_code="DESIGN_AUTHENTICATION_REQUIRED",
        message=message,
    )
