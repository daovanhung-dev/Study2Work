"""Khai báo request DERIVED và success envelope cho API #85."""

from __future__ import annotations

from typing import Any, Literal

from app.modules.guest.api_09_courses_curriculum.models import Lesson
from pydantic import BaseModel, ConfigDict


class AdminLessonStatusRequest(BaseModel):
    """Biểu diễn target status DERIVED theo tập trạng thái Admin Course #76."""

    status: Literal["DRAFT", "PUBLISHED", "SUSPENDED"]

    model_config = ConfigDict(extra="forbid", strict=True)


class UpdateAdminLessonStatusEnvelope(BaseModel):
    """Envelope thành công mang một Lesson theo catalog API #85."""

    success: bool
    businessCode: str
    message: str
    data: Lesson
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
