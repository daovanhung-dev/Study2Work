"""Khai báo query, Discussion summary và Page envelope cho API #97."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any

from app.modules.guest._shared.course_catalog.models import Pagination
from pydantic import BaseModel, ConfigDict, Field

PositiveInt64 = Annotated[
    int,
    Field(strict=True, ge=1, le=2**63 - 1, json_schema_extra={"format": "int64"}),
]


class AdminReportedDiscussionsQuery(BaseModel):
    """Lưu filter report nguyên văn và số trang đã kiểm tra."""

    reason: str | None = None
    severity: str | None = None
    page: int = 1

    model_config = ConfigDict(extra="forbid", strict=True)


class AdminDiscussionAuthor(BaseModel):
    """Biểu diễn UserSummary của tác giả trong Discussion."""

    id: PositiveInt64
    full_name: str
    avatar_url: str | None = None

    model_config = ConfigDict(extra="forbid")


class AdminDiscussionComment(BaseModel):
    """Biểu diễn một comment trực tiếp trong reusable Discussion schema."""

    id: PositiveInt64
    discussion_id: PositiveInt64
    content: str
    author: AdminDiscussionAuthor
    created_at: datetime

    model_config = ConfigDict(extra="forbid")


class AdminReportedDiscussion(BaseModel):
    """Biểu diễn Discussion summary trong hàng chờ kiểm duyệt."""

    id: PositiveInt64
    course_id: PositiveInt64
    title: str
    content: str
    author: AdminDiscussionAuthor
    status: str
    comments: list[AdminDiscussionComment]

    model_config = ConfigDict(extra="forbid")


class AdminReportedDiscussionsPage(BaseModel):
    """Gom Discussion items và metadata trang của hàng chờ report."""

    items: list[AdminReportedDiscussion]
    pagination: Pagination

    model_config = ConfigDict(extra="forbid")


class GetAdminReportedDiscussionsEnvelope(BaseModel):
    """Envelope thành công chứa Page<Discussion> theo API catalog #97."""

    success: bool
    businessCode: str
    message: str
    data: AdminReportedDiscussionsPage
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
