"""Khai báo query đã chuẩn hóa và response Page cho Admin API #78."""

from __future__ import annotations

from typing import Any

from app.modules.guest._shared.course_catalog.models import Pagination
from app.modules.mentor.api_49_mentor_content_list.models import ContentResponse
from pydantic import BaseModel, ConfigDict


class AdminPendingContentsQuery(BaseModel):
    """Các filter và page đã parse cho hàng chờ duyệt Content."""

    content_type: str | None = None
    course_id: int | None = None
    page: int = 1

    model_config = ConfigDict(extra="forbid")


class AdminPendingContentsPage(BaseModel):
    """Một trang Content chờ duyệt cùng metadata phân trang."""

    items: list[ContentResponse]
    pagination: Pagination

    model_config = ConfigDict(extra="forbid")


class GetAdminPendingContentsEnvelope(BaseModel):
    """Success envelope của API #78 chứa trang Content chờ duyệt."""

    success: bool
    businessCode: str
    message: str
    data: AdminPendingContentsPage
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
