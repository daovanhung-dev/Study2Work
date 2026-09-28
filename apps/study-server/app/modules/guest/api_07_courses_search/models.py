from __future__ import annotations

from app.modules.guest._shared.course_catalog.constants import DEFAULT_PAGE
from app.modules.guest._shared.course_catalog.helpers import normalize_sort
from pydantic import BaseModel, Field, field_validator


def normalize_search_query(value: object) -> object:
    """Loại khoảng trắng hai đầu và chuyển chuỗi tìm kiếm thành chữ thường trước khi kiểm tra
    model. Chuỗi sau chuẩn hóa rỗng trở thành None để truy vấn bỏ điều kiện từ khóa; giá trị
    không phải chuỗi được giữ cho Pydantic xác thực."""

    if isinstance(value, str):
        normalized = value.strip().lower()
        return normalized or None
    return value


class CourseSearchQuery(BaseModel):
    """Định nghĩa từ khóa, category tùy chọn, trang và sort của API tìm kiếm khóa học; validator
    chuẩn hóa từ khóa và dùng chung quy tắc sort."""

    q: str | None = None
    category: int | None = None
    page: int = Field(default=DEFAULT_PAGE, ge=1)
    sort: str | None = None

    _normalize_q = field_validator("q", mode="before")(normalize_search_query)
    _normalize_sort = field_validator("sort")(normalize_sort)
