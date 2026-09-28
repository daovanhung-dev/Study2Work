from __future__ import annotations

from app.utils.validate import reject_blank_password, strip_email
from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    """Định nghĩa body đăng ký công khai với email, mật khẩu và họ tên. Model giới hạn độ dài,
    chuẩn hóa khoảng trắng và từ chối mật khẩu chỉ gồm khoảng trắng theo các validator dùng
    chung."""

    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=1)
    full_name: str = Field(min_length=1, max_length=150)

    _strip_email = field_validator("email", mode="before")(strip_email)
    _reject_blank_password_ = field_validator("password", mode="before")(reject_blank_password)

    @field_validator("full_name", mode="before")
    @classmethod
    def strip_full_name(cls, value: object) -> object:
        """Chuẩn hóa trường full_name trước khi Pydantic áp dụng các ràng buộc độ dài. Giá trị
        chuỗi được loại khoảng trắng ở hai đầu; kiểu khác được giữ nguyên để bước xác thực của
        model quyết định."""
        if isinstance(value, str):
            return value.strip()
        return value
