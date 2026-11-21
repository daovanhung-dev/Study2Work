"""Khai báo response models cho tiến độ một Student trong course API #67."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class ProgressStudentSummary(BaseModel):
    """Thông tin tối thiểu nhận diện Student thuộc roster đang hoạt động."""

    id: Annotated[
        int,
        Field(strict=True, ge=1, le=2**63 - 1, json_schema_extra={"format": "int64"}),
    ]
    full_name: str
    avatar_url: str | None = None

    model_config = ConfigDict(extra="forbid")


class StudentLessonProgress(BaseModel):
    """Trạng thái hiện tại của một lesson đã publish trong course."""

    lesson_id: Annotated[
        int,
        Field(strict=True, ge=1, le=2**63 - 1, json_schema_extra={"format": "int64"}),
    ]
    title: str
    order: Annotated[int, Field(strict=True)]
    progress_status: Literal["NOT_STARTED", "IN_PROGRESS", "COMPLETED"]
    progress_percent: Annotated[int, Field(strict=True, ge=0, le=100)]
    last_accessed_at: datetime | None
    completed_at: datetime | None

    model_config = ConfigDict(extra="forbid")


class StudentCourseProgressSummary(BaseModel):
    """Các chỉ số lesson progress tổng hợp theo cùng quy tắc cục bộ với API #65."""

    completed_lessons: Annotated[int, Field(strict=True, ge=0, le=2**31 - 1)]
    total_lessons: Annotated[int, Field(strict=True, ge=0, le=2**31 - 1)]
    progress_percent: Annotated[int, Field(strict=True, ge=0, le=100)]

    model_config = ConfigDict(extra="forbid")


class StudentCourseProgress(BaseModel):
    """Tiến độ hiện tại của một Student trong một course theo mục tiêu AC-26."""

    course_id: Annotated[
        int,
        Field(strict=True, ge=1, le=2**63 - 1, json_schema_extra={"format": "int64"}),
    ]
    student: ProgressStudentSummary
    summary: StudentCourseProgressSummary
    lessons: list[StudentLessonProgress]

    model_config = ConfigDict(extra="forbid")


class GetMentorStudentProgressEnvelope(BaseModel):
    """Success envelope API #67 cho tiến độ lesson của một Student."""

    success: bool
    businessCode: str
    message: str
    data: StudentCourseProgress
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
