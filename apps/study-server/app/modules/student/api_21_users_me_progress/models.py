"""Mô hình dữ liệu cho API #21 lấy tiến độ tổng hợp."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ProgressQuery(BaseModel):
    """Tham số query lọc hoặc tổng hợp tiến độ của học viên."""

    model_config = ConfigDict(extra="ignore")

    course_id: str | None = None
    aggregate: str | None = None


class CourseProgressItem(BaseModel):
    """Tiến độ tóm tắt của học viên trong một khóa học đã ghi danh."""

    model_config = ConfigDict(extra="ignore")

    course_id: int
    course_name: str
    enrollment_status: str
    total_lessons: int
    completed_lessons: int
    progress_percent: float


class OverallProgressSummary(BaseModel):
    """Dữ liệu tổng hợp tiến độ học tập toàn khóa của học viên hiện tại."""

    model_config = ConfigDict(extra="ignore")

    total_enrolled_courses: int
    active_courses: int
    completed_courses: int
    total_lessons: int
    completed_lessons: int
    overall_progress_percent: float
    courses: list[CourseProgressItem]
