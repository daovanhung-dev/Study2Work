from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Lesson(BaseModel):
    """Public lesson projection in a course curriculum."""

    model_config = ConfigDict(extra="ignore")
    id: int
    course_id: int
    title: str
    content: str | None = None
    video_url: str | None = None
    order: int
    status: str


class Pagination(BaseModel):
    """Pagination metadata for the curriculum page."""

    page: int
    size: int
    total: int
    total_pages: int


class LessonPage(BaseModel):
    """Public curriculum page collection and pagination metadata."""

    items: list[Lesson]
    pagination: Pagination
