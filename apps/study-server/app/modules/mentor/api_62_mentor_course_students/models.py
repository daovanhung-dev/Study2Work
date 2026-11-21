"""Khai báo response models cho danh sách người nhận API #62."""

from __future__ import annotations

from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field

Int64 = Annotated[
    int,
    Field(strict=True, ge=1, le=2**63 - 1, json_schema_extra={"format": "int64"}),
]


class StudentSummaryResponse(BaseModel):
    """Biểu diễn UserSummary tối thiểu trong roster course."""

    id: Int64
    full_name: str
    avatar_url: str | None = None

    model_config = ConfigDict(extra="forbid")


class GetMentorCourseStudentsEnvelope(BaseModel):
    """Biểu diễn success envelope của API #62 chứa Student summaries."""

    success: bool
    businessCode: str
    message: str
    data: list[StudentSummaryResponse]
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
