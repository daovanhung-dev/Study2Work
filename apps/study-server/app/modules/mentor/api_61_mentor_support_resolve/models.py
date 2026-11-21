"""Khai báo success envelope cho API #61."""

from __future__ import annotations

from typing import Any

from app.modules.mentor.api_58_mentor_support_requests.models import SupportRequestResponse
from pydantic import BaseModel, ConfigDict


class ResolveMentorSupportRequestEnvelope(BaseModel):
    """Biểu diễn envelope chứa SupportRequest sau khi được resolve."""

    success: bool
    businessCode: str
    message: str
    data: SupportRequestResponse
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
