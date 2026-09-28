from __future__ import annotations

from app.modules.guest._shared.course_catalog.constants import (
    DEFAULT_PAGE,
    DEFAULT_SIZE,
    MAX_SIZE,
)
from app.modules.guest._shared.course_catalog.helpers import normalize_sort
from pydantic import BaseModel, Field, field_validator


class CourseQuery(BaseModel):
    """Định nghĩa category tùy chọn, trang, kích thước trang và sort của endpoint khóa học công
    khai; Pydantic kiểm tra giới hạn số trang và helper chung chuẩn hóa sort."""

    category: int | None = None
    page: int = Field(default=DEFAULT_PAGE, ge=1)
    size: int = Field(default=DEFAULT_SIZE, ge=1, le=MAX_SIZE)
    sort: str | None = None

    _normalize_sort = field_validator("sort")(normalize_sort)
