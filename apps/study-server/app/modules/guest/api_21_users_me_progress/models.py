"""Mô hình dữ liệu cho API #21 lấy tiến độ tổng hợp."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProgressQuery(BaseModel):
    """Tham số query lọc hoặc tổng hợp tiến độ của học viên."""

    model_config = ConfigDict(extra="ignore")

    course_id: str | None = None
    aggregate: str | None = None


class UserProfile(BaseModel):
    """Mô hình hồ sơ trả về cho API #21 theo đúng schema catalog ApiEnvelope<UserProfile>."""

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

