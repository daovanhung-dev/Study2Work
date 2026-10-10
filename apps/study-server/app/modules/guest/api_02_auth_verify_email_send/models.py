from __future__ import annotations

from pydantic import BaseModel


class VerifyEmailSendRequest(BaseModel):
    """Khai báo các trường và kiểu dữ liệu của body xác minh; rule input nằm trong validate.py."""

    user_id: int
    email: str
