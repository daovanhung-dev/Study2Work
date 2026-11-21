"""Khai báo Operation và envelope response cho API #64."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

PositiveInt64 = Annotated[
    int,
    Field(strict=True, ge=1, le=2**63 - 1, json_schema_extra={"format": "int64"}),
]


class NotificationStatusOperation(BaseModel):
    """Biểu diễn Operation được dựng từ notification và delivery outbox của API #63."""

    id: UUID
    kind: str
    status: str
    owner_id: PositiveInt64
    submitted_at: datetime
    updated_at: datetime
    completed_at: datetime | None = None

    model_config = ConfigDict(extra="forbid")


class GetMentorNotificationStatusEnvelope(BaseModel):
    """Biểu diễn success envelope API #64 chứa trạng thái Operation."""

    success: bool
    businessCode: str
    message: str
    data: NotificationStatusOperation
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
