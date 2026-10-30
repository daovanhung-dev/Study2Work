"""Khai báo query đã chuẩn hóa và envelope Lesson list của Admin API #82."""

from __future__ import annotations

from typing import Any

from app.modules.guest.api_09_courses_curriculum.models import Lesson
from pydantic import BaseModel, ConfigDict


class AdminLessonsQuery(BaseModel):
    """Các filter `course` và `status` đã chuẩn hóa cho truy vấn Lesson."""

    course_id: int | None = None
    status: str | None = None

    model_config = ConfigDict(extra="forbid")


class GetAdminLessonsEnvelope(BaseModel):
    """Success envelope của API #82 với collection Lesson theo fallback DERIVED."""

    success: bool
    businessCode: str
    message: str
    data: list[Lesson]
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
