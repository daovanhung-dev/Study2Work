"""Khai báo request status DERIVED và success envelope cho API #76."""

from __future__ import annotations

from typing import Any, Literal

from app.modules.guest._shared.course_catalog.models import CoursePage
from pydantic import BaseModel, ConfigDict


class AdminCourseStatusRequest(BaseModel):
    """Biểu diễn trạng thái đích được chọn trong AC-32 candidate contract."""

    status: Literal["DRAFT", "PUBLISHED", "SUSPENDED"]

    model_config = ConfigDict(extra="forbid", strict=True)


class UpdateAdminCourseStatusEnvelope(BaseModel):
    """Khai báo envelope thành công chứa một CoursePage sau khi đổi trạng thái."""

    success: bool
    businessCode: str
    message: str
    data: CoursePage
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
