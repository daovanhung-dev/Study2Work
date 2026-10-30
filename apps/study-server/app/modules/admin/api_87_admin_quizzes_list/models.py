"""Khai báo filter, Quiz list projection và Page envelope cho Admin API #87."""

from __future__ import annotations

from typing import Any

from app.modules.guest._shared.course_catalog.models import Pagination
from pydantic import BaseModel, ConfigDict


class AdminQuizzesQuery(BaseModel):
    """Filter course/status và page đã chuẩn hóa cho danh sách Quiz Admin."""

    course_id: int | None = None
    status: str | None = None
    page: int = 1

    model_config = ConfigDict(extra="forbid")


class AdminQuizResponse(BaseModel):
    """Quiz metadata trong danh sách; câu hỏi không được tải ở list projection."""

    id: int
    course_id: int
    title: str
    duration_minutes: int | None = None
    passing_score: str
    questions: list[dict[str, Any]]

    model_config = ConfigDict(extra="forbid")


class AdminQuizzesPage(BaseModel):
    """Trang Quiz Admin cùng metadata phân trang cố định."""

    items: list[AdminQuizResponse]
    pagination: Pagination

    model_config = ConfigDict(extra="forbid")


class GetAdminQuizzesEnvelope(BaseModel):
    """Success envelope API #87 với Page<Quiz> theo fallback DERIVED."""

    success: bool
    businessCode: str
    message: str
    data: AdminQuizzesPage
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
