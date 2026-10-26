"""Khai báo query, Notification projection và Page envelope cho API #92."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any, Literal

from app.modules.guest._shared.course_catalog.models import Pagination
from pydantic import BaseModel, ConfigDict, Field

PositiveInt64 = Annotated[
    int,
    Field(strict=True, ge=1, le=2**63 - 1, json_schema_extra={"format": "int64"}),
]

NotificationChannel = Literal["EMAIL", "PUSH"]
NotificationStatus = Literal["FAILED", "QUEUED", "SENT"]


class AdminNotificationsQuery(BaseModel):
    """Lưu status/channel nguyên văn và page đã kiểm tra của danh sách Admin."""

    status: str | None = None
    channel: str | None = None
    page: int = 1

    model_config = ConfigDict(extra="forbid", strict=True)


class AdminNotificationResponse(BaseModel):
    """Biểu diễn một legacy notification cùng delivery aggregate cục bộ."""

    id: PositiveInt64
    title: str
    content: str
    channels: list[NotificationChannel]
    status: NotificationStatus
    read_at: datetime | None = None
    scheduled_at: datetime | None = None
    created_at: datetime

    model_config = ConfigDict(extra="forbid")


class AdminNotificationsPage(BaseModel):
    """Trang Notification Admin cùng metadata phân trang."""

    items: list[AdminNotificationResponse]
    pagination: Pagination

    model_config = ConfigDict(extra="forbid")


class GetAdminNotificationsEnvelope(BaseModel):
    """Success envelope API #92 dùng Page<Notification> theo fallback DERIVED."""

    success: bool
    businessCode: str
    message: str
    data: AdminNotificationsPage
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
