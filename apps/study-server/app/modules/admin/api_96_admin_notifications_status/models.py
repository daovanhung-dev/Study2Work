"""Khai báo success envelope Notification cho API #96."""

from __future__ import annotations

from typing import Any

from app.modules.admin.api_92_admin_notifications_list.models import AdminNotificationResponse
from pydantic import BaseModel, ConfigDict


class GetAdminNotificationStatusEnvelope(BaseModel):
    """Envelope thành công giữ đúng reusable Notification của catalog."""

    success: bool
    businessCode: str
    message: str
    data: AdminNotificationResponse
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
