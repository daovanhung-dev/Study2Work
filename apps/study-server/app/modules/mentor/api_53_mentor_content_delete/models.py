"""Khai báo response DeleteResult và envelope thành công cho API #53."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class DeleteResult(BaseModel):
    """Kết quả soft-delete Content theo schema dùng chung trong catalog."""

    id: int = Field(strict=True, json_schema_extra={"format": "int64"})
    status: Literal["deleted"]
    deleted_at: datetime

    model_config = ConfigDict(extra="forbid")


class DeleteContentEnvelope(BaseModel):
    """Envelope thành công của API #53."""

    success: bool
    businessCode: str
    message: str
    data: DeleteResult
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
