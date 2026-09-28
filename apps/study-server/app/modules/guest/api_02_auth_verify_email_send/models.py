from __future__ import annotations

from pydantic import BaseModel, EmailStr, StrictInt


class VerifyEmailSendRequest(BaseModel):
    """Định nghĩa body tiếp nhận yêu cầu gửi email xác minh. user_id phải là số nguyên nghiêm ngặt
    và email phải qua kiểm tra định dạng."""

    user_id: StrictInt
    email: EmailStr
