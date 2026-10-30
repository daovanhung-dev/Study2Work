"""Khai báo response envelope cho API #59."""

from typing import Any

from app.modules.mentor.api_58_mentor_support_requests.models import SupportRequestResponse
from pydantic import BaseModel, ConfigDict


class GetMentorSupportRequestEnvelope(BaseModel):
    """Success envelope chứa một SupportRequest cùng conversation đã tải."""

    success: bool
    businessCode: str
    message: str
    data: SupportRequestResponse
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
