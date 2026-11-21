"""Khai báo DeleteResult và envelope response cho API #95."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class DeleteResult(BaseModel):
    """Biểu diễn notification đã xóa theo schema tái sử dụng trong catalog."""

    id: int = Field(strict=True, json_schema_extra={"format": "int64"})
    status: Literal["deleted"]
    deleted_at: datetime

    model_config = ConfigDict(extra="forbid")


class DeleteAdminNotificationEnvelope(BaseModel):
    """Envelope thành công của API #95."""

    success: bool
    businessCode: str
    message: str
    data: DeleteResult
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
