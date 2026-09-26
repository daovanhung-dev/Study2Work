"""Reusable pure input-normalization and validation helpers."""

from collections.abc import Mapping
from typing import Any


def strip_email(value: object) -> object:
    """Xóa khoảng trắng ở đầu và cuối chuỗi email."""

    return value.strip() if isinstance(value, str) else value


def reject_blank_password(value: object) -> object:
    """Từ chối mật khẩu chỉ chứa khoảng trắng."""

    if isinstance(value, str) and not value.strip():
        raise ValueError("Mật khẩu không được để trống.")
    return value


def reject_blank_value(value: object) -> object:
    """Từ chối giá trị chuỗi chỉ chứa khoảng trắng."""

    if isinstance(value, str) and not value.strip():
        raise ValueError("Giá trị không được để trống.")
    return value


def normalize_login_email(value: object) -> object:
    """Chuẩn hóa email đăng nhập trước khi Pydantic kiểm tra."""

    return strip_email(value)


def validate_login_password(value: object) -> object:
    """Kiểm tra mật khẩu đăng nhập không để trống."""

    return reject_blank_password(value)


def validate_refresh_token(value: object) -> object:
    """Kiểm tra refresh token không để trống."""

    return reject_blank_value(value)


def extract_bearer_token(authorization: str | None) -> str:
    """Tách JWT từ header Authorization dùng Bearer."""

    if authorization is None:
        raise ValueError("Authorization header is required")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise ValueError("Authorization header must use Bearer scheme")

    return parts[1]


def validate_access_claims(claims: Mapping[str, Any]) -> tuple[int, list[str]]:
    """Kiểm tra và chuẩn hóa claims của access token."""

    subject = claims.get("sub")
    if not isinstance(subject, str) or not subject:
        raise ValueError("JWT subject is missing")

    try:
        user_id = int(subject)
    except ValueError as exc:
        raise ValueError("JWT subject is not a numeric user ID") from exc

    if user_id <= 0:
        raise ValueError("JWT subject is not a positive user ID")

    raw_roles = claims.get("roles")
    if not isinstance(raw_roles, list) or not raw_roles:
        raise ValueError("JWT roles are missing")

    if not all(isinstance(role, str) and role.strip() for role in raw_roles):
        raise ValueError("JWT roles are invalid")

    roles = [role.strip().upper() for role in raw_roles]
    return user_id, roles
