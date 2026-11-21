"""Khai báo request full-replacement DERIVED và success envelope cho API #84."""

from __future__ import annotations

from typing import Annotated, Any

from app.modules.guest.api_09_courses_curriculum.models import Lesson
from pydantic import BaseModel, ConfigDict, Field

Int32 = Annotated[
    int,
    Field(strict=True, ge=-(2**31), le=2**31 - 1, json_schema_extra={"format": "int32"}),
]


class AdminLessonUpdateRequest(BaseModel):
    """Biểu diễn bốn field metadata DERIVED mà PUT #84 thay thế đầy đủ."""

    title: str = Field(max_length=200)
    content: str | None
    video_url: str | None
    order: Int32

    model_config = ConfigDict(extra="forbid", strict=True)


class UpdateAdminLessonEnvelope(BaseModel):
    """Envelope thành công mang đúng một Lesson theo catalog API #84."""

    success: bool
    businessCode: str
    message: str
    data: Lesson
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
