"""Mô hình dữ liệu cho API #25 lưu vị trí và trạng thái tiến độ bài học."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class LessonProgressUpdateRequest(BaseModel):
    """Dữ liệu yêu cầu cập nhật vị trí và phần trăm hoàn thành bài học."""

    model_config = ConfigDict(extra="ignore")

    position: int
    percent: int
    completed: bool


class LessonResponse(BaseModel):
    """Thông tin bài học trả về khi cập nhật tiến độ thành công."""

    model_config = ConfigDict(extra="ignore")

    id: int
    course_id: int
    title: str
    content: str | None = None
    video_url: str | None = None
    order: int
    status: str

