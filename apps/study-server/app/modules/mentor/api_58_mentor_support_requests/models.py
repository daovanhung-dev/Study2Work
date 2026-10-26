"""Khai báo query và response models cho API #58."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any

from app.modules.student.api_34_uploads.models import UploadAssetResponse
from pydantic import BaseModel, ConfigDict, Field

Int64 = Annotated[
    int,
    Field(strict=True, ge=1, le=2**63 - 1, json_schema_extra={"format": "int64"}),
]


class MentorSupportRequestsQuery(BaseModel):
    """Khai báo hai filter mà API #58 hỗ trợ."""

    course_id: Int64 | None = None
    status: str | None = None

    model_config = ConfigDict(extra="forbid")


class UserSummaryResponse(BaseModel):
    """Biểu diễn thông tin người dùng công khai trong SupportRequest."""

    id: Int64
    full_name: str
    avatar_url: str | None = None

    model_config = ConfigDict(extra="forbid")


class SupportMessageResponse(BaseModel):
    """Biểu diễn một message cùng các UploadAsset được liên kết."""

    id: Int64
    author: UserSummaryResponse
    content: str
    attachments: list[UploadAssetResponse]
    created_at: datetime

    model_config = ConfigDict(extra="forbid")


class SupportRequestResponse(BaseModel):
    """Biểu diễn một support request theo reusable schema của Study API."""

    id: Int64
    course_id: Int64
    student: UserSummaryResponse
    status: str
    messages: list[SupportMessageResponse]
    created_at: datetime
    resolved_at: datetime | None = None

    model_config = ConfigDict(extra="forbid")


class GetMentorSupportRequestsEnvelope(BaseModel):
    """Success envelope chứa collection SupportRequest của Mentor."""

    success: bool
    businessCode: str
    message: str
    data: list[SupportRequestResponse]
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
