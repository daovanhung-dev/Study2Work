"""Khai báo success envelope cho API #55."""

from typing import Any

from app.modules.mentor.api_54_mentor_submissions_list.models import SubmissionResponse
from pydantic import BaseModel, ConfigDict


class GetMentorSubmissionEnvelope(BaseModel):
    """Biểu diễn Study success envelope chứa Submission được Mentor chọn."""

    success: bool
    businessCode: str
    message: str
    data: SubmissionResponse
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
