"""Khai báo response models cho tiến độ toàn lớp API #65."""

from __future__ import annotations

from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field

PositiveInt64 = Annotated[
    int,
    Field(strict=True, ge=1, le=2**63 - 1, json_schema_extra={"format": "int64"}),
]
NonNegativeInt32 = Annotated[int, Field(strict=True, ge=0, le=2**31 - 1)]


class ProgressStudentSummary(BaseModel):
    """Thông tin tối thiểu nhận diện Student trong bảng tiến độ course."""

    id: PositiveInt64
    full_name: str
    avatar_url: str | None = None

    model_config = ConfigDict(extra="forbid")


class MentorStudentProgress(BaseModel):
    """Tiến độ tổng hợp của một Student trong các lesson đã publish."""

    student: ProgressStudentSummary
    completed_lessons: NonNegativeInt32
    total_lessons: NonNegativeInt32
    progress_percent: Annotated[int, Field(strict=True, ge=0, le=100)]

    model_config = ConfigDict(extra="forbid")


class ProgressPagination(BaseModel):
    """Metadata của toàn bộ roster trong một trang do request không có page/size."""

    page: Annotated[int, Field(strict=True, ge=1)]
    size: NonNegativeInt32
    total: NonNegativeInt32
    total_pages: Annotated[int, Field(strict=True, ge=0)]

    model_config = ConfigDict(extra="forbid")


class MentorStudentProgressPage(BaseModel):
    """Page progress cục bộ theo mục tiêu AC-26; đây là fallback DERIVED của catalog."""

    items: list[MentorStudentProgress]
    pagination: ProgressPagination

    model_config = ConfigDict(extra="forbid")


class GetMentorCourseProgressEnvelope(BaseModel):
    """Success envelope API #65 với một tiến độ cho mỗi Student đủ điều kiện."""

    success: bool
    businessCode: str
    message: str
    data: MentorStudentProgressPage
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
