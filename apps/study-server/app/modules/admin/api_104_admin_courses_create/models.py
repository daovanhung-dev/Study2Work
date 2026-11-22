"""Khai báo request và response cho API #104 tạo khóa học Admin."""

from __future__ import annotations

from typing import Any

from app.modules.shared.course_catalog.models import Course
from pydantic import BaseModel, ConfigDict, StrictInt, StrictStr


class CreateAdminCourseRequest(BaseModel):
    """Biểu diễn metadata khóa học cần tạo với Mentor được chọn."""

    title: StrictStr
    description: StrictStr | None = None
    thumbnail_url: StrictStr | None = None
    price: StrictStr
    mentor_id: StrictInt

    model_config = ConfigDict(extra="forbid", strict=True)


class CreateAdminCourseEnvelope(BaseModel):
    """Khai báo success envelope trả Course vừa được tạo."""

    success: bool
    businessCode: str
    message: str
    data: Course
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
