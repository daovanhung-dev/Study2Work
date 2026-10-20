"""Mô hình dữ liệu cho API #23 khởi tạo lần bắt đầu học bài học."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class LessonResponse(BaseModel):
    """Thông tin bài học trả về khi khởi tạo lần bắt đầu học thành công."""

    model_config = ConfigDict(extra="ignore")

    id: int
    course_id: int
    title: str
    content: str | None = None
    video_url: str | None = None
    order: int
    status: str

