"""Mô hình dữ liệu cho API #22 kiểm tra quyền truy cập bài học."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class LessonResponse(BaseModel):
    """Thông tin bài học trả về khi kiểm tra quyền truy cập thành công."""

    model_config = ConfigDict(extra="ignore")

    id: int
    course_id: int
    title: str
    content: str | None = None
    video_url: str | None = None
    order: int
    status: str

