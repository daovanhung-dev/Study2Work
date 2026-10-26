"""Khai báo request và envelope response cho API #94."""

from __future__ import annotations

from typing import Any

from app.modules.admin.api_92_admin_notifications_list.models import AdminNotificationResponse
from pydantic import BaseModel, ConfigDict, Field, StrictStr


class AdminNotificationUpdateRequest(BaseModel):
    """Nhận các trường text mà legacy notification có thể cập nhật."""

    title: StrictStr = Field(max_length=200)
    content: StrictStr

    model_config = ConfigDict(extra="forbid", strict=True)


class UpdateAdminNotificationEnvelope(BaseModel):
    """Success envelope API #94 trả một Notification đã cập nhật."""

    success: bool
    businessCode: str
    message: str
    data: AdminNotificationResponse
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
