from __future__ import annotations

from app.modules.guest._shared.course_catalog.constants import DEFAULT_PAGE, DEFAULT_SIZE
from pydantic import BaseModel


class MentorCourseQuery(BaseModel):
    """Khai báo query fields và default của API #46.

    Quy tắc input được kiểm tra trong validate.py.
    """

    status: str | None = None
    page: int = DEFAULT_PAGE
    size: int = DEFAULT_SIZE
