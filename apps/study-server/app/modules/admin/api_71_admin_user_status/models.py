"""Khai báo request status DERIVED và response envelope cho API #71."""

from __future__ import annotations

from typing import Any, Literal

from app.modules.guest.api_04_users_me.models import UserProfile
from pydantic import BaseModel, ConfigDict


class AdminUserStatusRequest(BaseModel):
    """Khai báo target status ACTIVE/SUSPENDED được chọn cho thao tác khóa/mở khóa."""

    status: Literal["ACTIVE", "SUSPENDED"]

    model_config = ConfigDict(extra="forbid", strict=True)


class UpdateAdminUserStatusEnvelope(BaseModel):
    """Khai báo success envelope API #71 chứa safe UserProfile."""

    success: bool
    businessCode: str
    message: str
    data: UserProfile
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
