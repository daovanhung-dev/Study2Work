from __future__ import annotations

from pydantic import BaseModel


class RegisterRequest(BaseModel):
    """Khai báo các trường và kiểu dữ liệu của body đăng ký; rule input nằm trong validate.py."""

    email: str
    password: str
    full_name: str
