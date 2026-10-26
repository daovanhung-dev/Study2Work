"""Khai báo request và success envelope của API #56."""

from __future__ import annotations

from typing import Annotated, Any

from app.modules.mentor.api_54_mentor_submissions_list.models import SubmissionResponse
from pydantic import BaseModel, ConfigDict, Field

Int32 = Annotated[
    int,
    Field(strict=True, ge=-(2**31), le=2**31 - 1, json_schema_extra={"format": "int32"}),
]


class GradeSubmissionRequest(BaseModel):
    """Biểu diễn điểm và rubric descriptor theo fallback API #56."""

    score: Int32
    rubric_items: str = Field(strict=True)

    model_config = ConfigDict(extra="forbid")


class GradeMentorSubmissionEnvelope(BaseModel):
    """Biểu diễn success envelope chứa Submission sau khi lưu điểm."""

    success: bool
    businessCode: str
    message: str
    data: SubmissionResponse
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
