"""Khai báo query và response models cho API #54."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any

from app.modules.guest._shared.course_catalog.models import Pagination
from app.modules.student.api_34_uploads.models import UploadAssetResponse
from pydantic import BaseModel, ConfigDict, Field

Int64 = Annotated[
    int,
    Field(strict=True, ge=1, le=2**63 - 1, json_schema_extra={"format": "int64"}),
]


class MentorSubmissionsQuery(BaseModel):
    """Khai báo các bộ lọc và trang được API #54 hỗ trợ."""

    course_id: Int64 | None = None
    status: str | None = None
    page: int = 1

    model_config = ConfigDict(extra="forbid")


class SubmissionResponse(BaseModel):
    """Biểu diễn Submission theo reusable schema và metadata file đã được liên kết."""

    id: Int64
    assignment_id: Int64
    user_id: Int64
    content: str | None = None
    files: list[UploadAssetResponse]
    status: str
    submitted_at: datetime
    score: str | None = None
    feedback: str | None = None

    model_config = ConfigDict(extra="forbid")


class SubmissionPage(BaseModel):
    """Gom các Submission cùng metadata phân trang cho màn hình chấm bài."""

    items: list[SubmissionResponse]
    pagination: Pagination

    model_config = ConfigDict(extra="forbid")


class GetMentorSubmissionsEnvelope(BaseModel):
    """Biểu diễn success envelope của API #54 chứa một trang Submission."""

    success: bool
    businessCode: str
    message: str
    data: SubmissionPage
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
