"""Khai báo query đã chuẩn hóa và response models cho API #73."""

from __future__ import annotations

from typing import Any

from app.modules.guest._shared.course_catalog.models import CoursePage
from pydantic import BaseModel, ConfigDict


class AdminCoursesQuery(BaseModel):
    """Các filter và trang đã parse của danh sách khóa học Admin."""

    status: str | None = None
    mentor: int | None = None
    category: int | None = None
    page: int = 1

    model_config = ConfigDict(extra="forbid")


class GetAdminCoursesEnvelope(BaseModel):
    """Success envelope API #73 chứa một trang Course dùng chung."""

    success: bool
    businessCode: str
    message: str
    data: CoursePage
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
