from __future__ import annotations

from app.modules.guest._shared.course_catalog.constants import DEFAULT_PAGE
from pydantic import BaseModel


class CourseSearchQuery(BaseModel):
    """Khai báo kiểu và mặc định của tham số tìm kiếm; input rules nằm trong validate.py."""

    q: str | None = None
    category: int | None = None
    page: int = DEFAULT_PAGE
    sort: str | None = None
