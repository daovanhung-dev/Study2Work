from __future__ import annotations

# Nhập các tiện ích dùng chung.
from app.utils.validate import (
    normalize_login_email,
    validate_login_password,
    validate_refresh_token,
)

# Nhập các thành phần của framework.
from pydantic import BaseModel, EmailStr, Field, field_validator


class LoginRequest(BaseModel):
    """Định nghĩa body đăng nhập với email và mật khẩu. Email được loại khoảng trắng trước khi kiểm
    tra, còn mật khẩu chỉ gồm khoảng trắng bị từ chối."""

    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=1)

    _normalize_email = field_validator("email", mode="before")(normalize_login_email)
    _validate_password = field_validator("password", mode="before")(validate_login_password)


class RefreshRequest(BaseModel):
    """Định nghĩa body xoay vòng phiên đăng nhập với refresh token bắt buộc không rỗng."""

    refresh_token: str = Field(min_length=1)

    _validate_refresh_token = field_validator("refresh_token", mode="before")(
        validate_refresh_token
    )
