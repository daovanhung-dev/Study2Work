"""Khai báo DeleteResult theo catalog cho API #77."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class DeleteResult(BaseModel):
    """Kết quả soft-delete course trả về cho Admin."""

    id: int = Field(strict=True, json_schema_extra={"format": "int64"})
    status: Literal["deleted"]
    deleted_at: datetime

    model_config = ConfigDict(extra="forbid")


class DeleteAdminCourseEnvelope(BaseModel):
    """Envelope thành công của API #77."""

    success: bool
    businessCode: str
    message: str
    data: DeleteResult
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
