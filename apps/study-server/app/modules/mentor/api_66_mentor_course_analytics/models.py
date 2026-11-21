"""Khai báo response model cho analytics hoạt động course của Mentor API #66."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field

NonNegativeInt64 = Annotated[int, Field(strict=True, ge=0, le=2**63 - 1)]


class MentorCourseActivityAnalytics(BaseModel):
    """Tóm tắt activity proxy từ các cặp Student/lesson có dấu thời gian truy cập."""

    tracked_lesson_accesses: NonNegativeInt64
    students_with_activity: NonNegativeInt64
    last_activity_at: datetime | None

    model_config = ConfigDict(extra="forbid")


class GetMentorCourseAnalyticsEnvelope(BaseModel):
    """Success envelope API #66 cho một course do Mentor hiện tại sở hữu."""

    success: bool
    businessCode: str
    message: str
    data: MentorCourseActivityAnalytics
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
