"""Khai báo request, normalized payload và response envelope cho API #93."""

from __future__ import annotations

from typing import Annotated, Any
from uuid import UUID

from app.modules.admin.api_92_admin_notifications_list.models import (
    AdminNotificationResponse,
    NotificationChannel,
)
from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr

PositiveInt64 = Annotated[
    int,
    Field(strict=True, ge=1, le=2**63 - 1, json_schema_extra={"format": "int64"}),
]


class CreateAdminNotificationBody(BaseModel):
    """Giữ body trực tiếp của #93, trong đó segment chưa có schema được định nghĩa."""

    recipients: list[StrictInt] | None = None
    segment: Any = Field(default=None, description="AudienceSegment chưa được định nghĩa.")
    title: StrictStr
    content: StrictStr
    channels: list[StrictStr]

    model_config = ConfigDict(extra="forbid", strict=True)


class NormalizedAdminNotificationRequest(BaseModel):
    """Lưu explicit recipients, text và channels sau khi áp dụng fallback local."""

    recipient_ids: list[PositiveInt64]
    title: StrictStr
    content: StrictStr
    channels: list[NotificationChannel]

    model_config = ConfigDict(extra="forbid", strict=True)


class AdminNotificationCreateMeta(BaseModel):
    """Mô tả batch UUID và các notification ID của từng recipient trong metadata."""

    operation_id: UUID
    notification_ids: list[PositiveInt64]

    model_config = ConfigDict(extra="forbid")


class CreateAdminNotificationEnvelope(BaseModel):
    """Success envelope API #93 giữ data Notification theo direct endpoint contract."""

    success: bool
    businessCode: str
    message: str
    data: AdminNotificationResponse
    meta: AdminNotificationCreateMeta
    traceId: str

    model_config = ConfigDict(extra="forbid")
