from __future__ import annotations

from pydantic import BaseModel


class LoginRequest(BaseModel):
    """Khai báo các trường và kiểu dữ liệu của body đăng nhập; rule input nằm trong validate.py."""

    email: str
    password: str


class RefreshRequest(BaseModel):
    """Khai báo trường và kiểu dữ liệu của body xoay vòng refresh token."""

    refresh_token: str
