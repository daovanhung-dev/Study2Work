"""Khai báo response envelope cho API #74."""

from __future__ import annotations

from typing import Any

from app.modules.guest._shared.course_catalog.models import CoursePage
from pydantic import BaseModel, ConfigDict


class GetAdminCourseDetailEnvelope(BaseModel):
    """Biểu diễn envelope chứa một trang Course trong response API #74."""

    success: bool
    businessCode: str
    message: str
    data: CoursePage
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
