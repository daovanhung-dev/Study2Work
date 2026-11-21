"""Khai báo request reason và response envelope cho Admin API #81."""

from typing import Any

from app.modules.mentor.api_49_mentor_content_list.models import ContentResponse
from pydantic import BaseModel, ConfigDict


class RejectAdminContentRequest(BaseModel):
    """Biểu diễn reason string bắt buộc theo catalog API #81."""

    reason: str

    model_config = ConfigDict(extra="forbid", strict=True)


class RejectAdminContentEnvelope(BaseModel):
    """Biểu diễn success envelope chứa đúng một Content theo catalog API #81."""

    success: bool
    businessCode: str
    message: str
    data: ContentResponse
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
