"""Khai báo request metadata candidate và success envelope cho API #75."""

from __future__ import annotations

from typing import Any

from app.modules.guest._shared.course_catalog.models import CoursePage
from pydantic import BaseModel, ConfigDict


class AdminCourseUpdateRequest(BaseModel):
    """Biểu diễn body full-replacement DERIVED cho metadata khóa học Admin."""

    title: str
    description: str | None
    thumbnail_url: str | None
    price: str

    model_config = ConfigDict(extra="forbid", strict=True)


class UpdateAdminCourseEnvelope(BaseModel):
    """Khai báo envelope thành công chứa một CoursePage sau khi cập nhật."""

    success: bool
    businessCode: str
    message: str
    data: CoursePage
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
