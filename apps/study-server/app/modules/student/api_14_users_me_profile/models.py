"""Định nghĩa request cập nhật các trường hồ sơ đã có trong bảng users."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ProfileUpdateRequest(BaseModel):
    """Khai báo body cập nhật profile; bio tạm thời bị bỏ qua vì database chưa có cột."""

    model_config = ConfigDict(extra="ignore")

    full_name: str
    phone: str | None
    avatar_url: str | None
