"""Khai báo request và success envelope của API #57."""

from __future__ import annotations

from typing import Any

from app.modules.mentor.api_54_mentor_submissions_list.models import SubmissionResponse
from pydantic import BaseModel, ConfigDict, Field


class FeedbackSubmissionRequest(BaseModel):
    """Biểu diễn feedback và attachment descriptor theo fallback API #57."""

    feedback_text: str = Field(strict=True)
    attachments: str = Field(strict=True)

    model_config = ConfigDict(extra="forbid")


class FeedbackMentorSubmissionEnvelope(BaseModel):
    """Biểu diễn success envelope chứa Submission sau khi lưu feedback."""

    success: bool
    businessCode: str
    message: str
    data: SubmissionResponse
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
