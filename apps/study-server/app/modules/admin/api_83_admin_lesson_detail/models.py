"""Khai báo success envelope Lesson detail của Admin API #83."""

from __future__ import annotations

from typing import Any

from app.modules.guest.api_09_courses_curriculum.models import Lesson
from pydantic import BaseModel, ConfigDict


class GetAdminLessonEnvelope(BaseModel):
    """Envelope thành công mang đúng một Lesson theo catalog API #83."""

    success: bool
    businessCode: str
    message: str
    data: Lesson
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
