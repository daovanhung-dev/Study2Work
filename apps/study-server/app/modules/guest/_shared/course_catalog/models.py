from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class MentorSummary(BaseModel):
    """Mô tả phần hồ sơ công khai của mentor được nhúng trong từng khóa học. Model chỉ cho phép các
    trường đã khai báo và avatar có thể vắng mặt."""

    model_config = ConfigDict(extra="ignore")

    id: int
    full_name: str
    avatar_url: str | None = None


class Course(BaseModel):
    """Định nghĩa các trường công khai của một khóa học đã xuất bản, bao gồm giá dạng chuỗi và phần
    tóm tắt mentor."""

    model_config = ConfigDict(extra="ignore")

    id: int
    title: str
    description: str | None = None
    thumbnail_url: str | None = None
    price: str
    status: str
    mentor: MentorSummary


class Pagination(BaseModel):
    """Chứa thông tin phân trang hiệu lực gồm trang hiện tại, kích thước trang, tổng số mục và tổng
    số trang."""

    page: int
    size: int
    total: int
    total_pages: int


class CoursePage(BaseModel):
    """Gom danh sách khóa học cùng metadata phân trang thành cấu trúc response dùng chung."""

    items: list[Course]
    pagination: Pagination
