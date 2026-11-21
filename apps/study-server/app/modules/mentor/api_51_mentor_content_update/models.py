"""Khai báo request và envelope response cho API #51."""

from typing import Any

from app.modules.mentor.api_49_mentor_content_list.models import ContentResponse
from pydantic import BaseModel, ConfigDict, Field


class UpdateContentRequest(BaseModel):
    """Biểu diễn body thay thế Content theo fallback DERIVED từ API #50."""

    content_type: str = Field(strict=True)
    title: str = Field(strict=True)
    payload: dict[str, Any] = Field(strict=True)

    model_config = ConfigDict(extra="forbid")


class UpdateContentEnvelope(BaseModel):
    """Biểu diễn envelope thành công của API #51."""

    success: bool
    businessCode: str
    message: str
    data: ContentResponse
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
