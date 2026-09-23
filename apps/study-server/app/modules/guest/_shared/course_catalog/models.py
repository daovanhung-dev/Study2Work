from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class MentorSummary(BaseModel):
    """Public mentor projection embedded in a course item."""

    model_config = ConfigDict(extra="ignore")

    id: int
    full_name: str
    avatar_url: str | None = None


class Course(BaseModel):
    """Public fields returned for one published course."""

    model_config = ConfigDict(extra="ignore")

    id: int
    title: str
    description: str | None = None
    thumbnail_url: str | None = None
    price: str
    status: str
    mentor: MentorSummary


class Pagination(BaseModel):
    """Effective pagination metadata for public course APIs."""

    page: int
    size: int
    total: int
    total_pages: int


class CoursePage(BaseModel):
    """Public course collection and pagination metadata."""

    items: list[Course]
    pagination: Pagination
