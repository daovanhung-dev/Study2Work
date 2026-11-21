from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StudentNotification(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    title: str
    content: str
    type: str | None = None
    is_read: bool
    read_at: datetime | None = None
    created_at: datetime


class NotificationPagination(BaseModel):
    page: int
    size: int
    total: int
    total_pages: int


class StudentNotificationPage(BaseModel):
    items: list[StudentNotification]
    pagination: NotificationPagination


class NotificationsReadSummary(BaseModel):
    updated_count: int
