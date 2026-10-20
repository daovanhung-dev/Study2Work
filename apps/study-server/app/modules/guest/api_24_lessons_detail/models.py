"""Mô hình dữ liệu cho API #24 nạp nội dung chi tiết bài học."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class LessonResponse(BaseModel):
    """Thông tin bài học trả về khi đọc nội dung bài học thành công."""

    model_config = ConfigDict(extra="ignore")

    id: int
    course_id: int
    title: str
    content: str | None = None
    video_url: str | None = None
    order: int
    status: str

