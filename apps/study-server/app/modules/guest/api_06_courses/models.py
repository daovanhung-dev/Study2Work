from __future__ import annotations

from app.modules.guest._shared.course_catalog.constants import (
    DEFAULT_PAGE,
    DEFAULT_SIZE,
)
from pydantic import BaseModel


class CourseQuery(BaseModel):
    """Khai báo kiểu và mặc định của tham số khóa học; input rules nằm trong validate.py."""

    category: int | None = None
    page: int = DEFAULT_PAGE
    size: int = DEFAULT_SIZE
    sort: str | None = None
