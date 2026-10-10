from __future__ import annotations

from pydantic import BaseModel, ConfigDict

DEFAULT_LOCALE = "vi-VN"


class CategoryQuery(BaseModel):
    """Định nghĩa tham số tùy chọn locale cho endpoint danh mục công khai; nếu thiếu, lớp view sẽ
    áp dụng locale mặc định."""

    locale: str | None = None


class Category(BaseModel):
    """Định nghĩa các trường danh mục được phép trả về công khai, trong đó description có thể không
    có."""

    model_config = ConfigDict(extra="ignore")

    id: int
    name: str
    slug: str
    description: str | None = None


class Pagination(BaseModel):
    """Mô tả metadata một trang duy nhất của API #5, gồm page, size, total và total_pages."""

    page: int
    size: int
    total: int
    total_pages: int


class CategoryPage(BaseModel):
    """Gom các danh mục đã ánh xạ cùng metadata trang duy nhất vào response của API #5."""

    items: list[Category]
    pagination: Pagination
