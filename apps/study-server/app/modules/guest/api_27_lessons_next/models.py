"""Mô hình dữ liệu cho API #27 tìm bài học tiếp theo theo curriculum."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class NextLesson(BaseModel):
    """Mô hình dữ liệu bài học tiếp theo theo contract API #27."""

    model_config = ConfigDict(extra="ignore")

    id: int
    course_id: int
    title: str
    content: str | None = None
    video_url: str | None = None
    order: int
    status: str

