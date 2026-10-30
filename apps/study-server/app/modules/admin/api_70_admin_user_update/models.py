"""Khai báo body DERIVED và response envelope cho API #70."""

from __future__ import annotations

from typing import Any, Literal

from app.modules.guest.api_04_users_me.models import UserProfile
from pydantic import BaseModel, ConfigDict


class AdminUserUpdateRequest(BaseModel):
    """Khai báo full-replacement fields được chọn cho profile và role Admin."""

    full_name: str
    phone: str | None
    avatar_url: str | None
    role: Literal["STUDENT", "MENTOR", "ADMIN"]

    model_config = ConfigDict(extra="forbid", strict=True)


class UpdateAdminUserEnvelope(BaseModel):
    """Khai báo success envelope API #70 chứa UserProfile đã cập nhật."""

    success: bool
    businessCode: str
    message: str
    data: UserProfile
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
