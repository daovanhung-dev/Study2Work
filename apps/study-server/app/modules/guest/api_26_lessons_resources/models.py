"""Mô hình dữ liệu cho API #26 lấy tài nguyên đính kèm của bài học."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ResourceItem(BaseModel):
    """Mô hình thông tin tài nguyên đính kèm bài học."""

    model_config = ConfigDict(extra="ignore")

    id: int
    name: str
    type: str
    url: str | None = None
    lesson_id: int | None = None


class LessonResources(BaseModel):
    """Mô hình dữ liệu bài học kèm danh sách tài nguyên theo contract API #26."""

    model_config = ConfigDict(extra="ignore")

    id: int
    course_id: int
    title: str
    content: str | None = None
    video_url: str | None = None
    order: int
    status: str
    resources: list[ResourceItem] = []

