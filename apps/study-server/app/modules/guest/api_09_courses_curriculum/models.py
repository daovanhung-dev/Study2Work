"""Mô hình dữ liệu cho API #9 danh sách bài học của khóa học (curriculum)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Lesson(BaseModel):
    """Mô hình bài học công khai trong curriculum của khóa học."""

    model_config = ConfigDict(extra="ignore")
    id: int
    course_id: int
    title: str
    content: str | None = None
    video_url: str | None = None
    order: int
    status: str


class Pagination(BaseModel):
    """Thông tin phân trang cho trang curriculum."""

    page: int
    size: int
    total: int
    total_pages: int


class LessonPage(BaseModel):
    """Tập hợp danh sách bài học và metadata phân trang."""

    items: list[Lesson]
    pagination: Pagination
