"""Khai báo success envelope của API #79 theo reusable Content contract."""

from typing import Any

from app.modules.mentor.api_49_mentor_content_list.models import ContentResponse
from pydantic import BaseModel, ConfigDict


class GetAdminContentEnvelope(BaseModel):
    """Envelope thành công mang đúng một Content theo catalog API #79."""

    success: bool
    businessCode: str
    message: str
    data: ContentResponse
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
