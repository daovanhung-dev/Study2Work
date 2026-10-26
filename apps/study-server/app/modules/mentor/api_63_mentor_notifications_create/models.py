"""Khai báo request, Operation và envelope response cho API #63."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

SignedInt64 = Annotated[
    int,
    Field(
        strict=True,
        ge=-(2**63),
        le=2**63 - 1,
        json_schema_extra={"format": "int64"},
    ),
]

PositiveInt64 = Annotated[
    int,
    Field(strict=True, ge=1, le=2**63 - 1, json_schema_extra={"format": "int64"}),
]

NotificationChannel = Literal["PUSH", "EMAIL"]


class CreateNotificationRequest(BaseModel):
    """Biểu diễn body trực tiếp của API #63 theo các kiểu trong API catalog."""

    recipients: str
    title: str = Field(max_length=200)
    content: SignedInt64
    channels: str

    model_config = ConfigDict(extra="forbid", strict=True)


class NormalizedNotificationRequest(BaseModel):
    """Chứa recipient IDs và delivery channels sau khi parse CSV."""

    recipient_ids: list[PositiveInt64]
    channels: list[NotificationChannel]

    model_config = ConfigDict(extra="forbid", strict=True)


class OperationResponse(BaseModel):
    """Biểu diễn Operation đang QUEUED sau khi delivery outbox đã commit."""

    id: UUID
    kind: str
    status: str
    owner_id: PositiveInt64
    submitted_at: datetime
    updated_at: datetime
    completed_at: datetime | None = None

    model_config = ConfigDict(extra="forbid")


class CreateNotificationEnvelope(BaseModel):
    """Biểu diễn success envelope API #63 và metadata notification IDs cho API #64."""

    success: bool
    businessCode: str
    message: str
    data: OperationResponse
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
