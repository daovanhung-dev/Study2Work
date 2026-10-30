"""Khai báo request và success envelope cho API #60."""

from __future__ import annotations

from typing import Any

from app.modules.mentor.api_58_mentor_support_requests.models import SupportRequestResponse
from pydantic import BaseModel, ConfigDict, Field


class ReplyToMentorSupportRequest(BaseModel):
    """Biểu diễn nội dung phản hồi và chuỗi attachment refs của Mentor."""

    message: str = Field(strict=True)
    attachment_refs: str = Field(strict=True)

    model_config = ConfigDict(extra="forbid")


class ReplyMentorSupportRequestEnvelope(BaseModel):
    """Success envelope chứa SupportRequest sau khi thêm reply."""

    success: bool
    businessCode: str
    message: str
    data: SupportRequestResponse
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
