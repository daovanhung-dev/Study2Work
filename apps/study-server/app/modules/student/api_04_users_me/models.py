"""Định nghĩa model chứa các trường hồ sơ an toàn mà endpoint người dùng hiện tại trả về."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserProfile(BaseModel):
    """Giới hạn response hồ sơ API #4 vào các trường công khai, có kiểu dữ liệu rõ ràng; các trường
    ngoài model bị bỏ qua khi ánh xạ dữ liệu nguồn."""

    model_config = ConfigDict(extra="ignore")

    id: int
    full_name: str
    email: str
    role: str
    avatar_url: str | None = None
    phone: str | None = None
    status: str
    created_at: datetime
    updated_at: datetime
