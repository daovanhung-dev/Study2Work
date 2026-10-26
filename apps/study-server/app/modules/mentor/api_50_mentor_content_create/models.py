"""Khai báo request và envelope response cho API #50."""

from typing import Annotated, Any

from app.modules.mentor.api_49_mentor_content_list.models import ContentResponse
from pydantic import BaseModel, ConfigDict, Field

Int64 = Annotated[
    int,
    Field(strict=True, ge=-(2**63), le=2**63 - 1, json_schema_extra={"format": "int64"}),
]


class CreateContentRequest(BaseModel):
    """Biểu diễn bốn trường body bắt buộc của API #50."""

    course_id: Int64
    content_type: str = Field(strict=True)
    title: str = Field(strict=True)
    payload: dict[str, Any] = Field(strict=True)

    model_config = ConfigDict(extra="forbid")


class CreateContentEnvelope(BaseModel):
    """Biểu diễn envelope thành công của API #50."""

    success: bool
    businessCode: str
    message: str
    data: ContentResponse
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
