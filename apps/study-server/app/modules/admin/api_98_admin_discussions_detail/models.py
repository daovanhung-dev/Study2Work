"""Khai báo Discussion thread và response Page của API #98."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any

from app.modules.guest._shared.course_catalog.models import Pagination
from pydantic import BaseModel, ConfigDict, Field

PositiveInt64 = Annotated[
    int,
    Field(strict=True, ge=1, le=2**63 - 1, json_schema_extra={"format": "int64"}),
]


class AdminDiscussionAuthor(BaseModel):
    """Biểu diễn UserSummary của tác giả Discussion hoặc comment."""

    id: PositiveInt64
    full_name: str
    avatar_url: str | None = None

    model_config = ConfigDict(extra="forbid")


class AdminDiscussionComment(BaseModel):
    """Biểu diễn một Discussion con trực tiếp trong thread Admin."""

    id: PositiveInt64
    discussion_id: PositiveInt64
    content: str
    author: AdminDiscussionAuthor
    created_at: datetime

    model_config = ConfigDict(extra="forbid")


class AdminDiscussionDetail(BaseModel):
    """Biểu diễn một Discussion cùng các comment trực tiếp theo catalog."""

    id: PositiveInt64
    course_id: PositiveInt64
    title: str
    content: str
    author: AdminDiscussionAuthor
    status: str
    comments: list[AdminDiscussionComment]

    model_config = ConfigDict(extra="forbid")


class AdminDiscussionDetailPage(BaseModel):
    """Gom một Discussion và metadata Page theo response catalog #98."""

    items: list[AdminDiscussionDetail]
    pagination: Pagination

    model_config = ConfigDict(extra="forbid")


class GetAdminDiscussionDetailEnvelope(BaseModel):
    """Envelope thành công chứa Page<Discussion> theo API catalog #98."""

    success: bool
    businessCode: str
    message: str
    data: AdminDiscussionDetailPage
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
