"""Khai báo response envelope cho Admin API #80."""

from typing import Any

from app.modules.mentor.api_49_mentor_content_list.models import ContentResponse
from pydantic import BaseModel, ConfigDict


class ApproveAdminContentEnvelope(BaseModel):
    """Envelope thành công mang đúng một Content theo catalog API #80."""

    success: bool
    businessCode: str
    message: str
    data: ContentResponse
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
