"""Khai báo response DeleteResult theo catalog cho API #72."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class DeleteResult(BaseModel):
    """Mô tả kết quả soft-delete user trả về cho Admin."""

    id: int = Field(strict=True, json_schema_extra={"format": "int64"})
    status: Literal["deleted"]
    deleted_at: datetime

    model_config = ConfigDict(extra="forbid")


class DeleteAdminUserEnvelope(BaseModel):
    """Khai báo success envelope API #72 chứa DeleteResult."""

    success: bool
    businessCode: str
    message: str
    data: DeleteResult
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
