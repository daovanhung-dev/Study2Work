"""Mô hình dữ liệu cho API #22 kiểm tra quyền truy cập bài học."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class LessonResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    course_id: int
    title: str
    content: str | None = None
    video_url: str | None = None
    order: int
    status: str

