"""Khai báo request tạo user Admin và envelope trả profile an toàn."""

from __future__ import annotations

from typing import Any, Literal

from app.modules.student.api_04_users_me.models import UserProfile
from pydantic import BaseModel, ConfigDict, Field, StrictStr


class CreateAdminUserRequest(BaseModel):
    """Biểu diễn thông tin user mới do Admin nhập."""

    full_name: StrictStr
    email: StrictStr
    password: StrictStr = Field(repr=False)
    role: Literal["STUDENT", "MENTOR", "ADMIN"]

    model_config = ConfigDict(extra="forbid", strict=True)


class CreateAdminUserEnvelope(BaseModel):
    """Khai báo envelope trả UserProfile mà không lộ credential."""

    success: bool
    businessCode: str
    message: str
    data: UserProfile
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
