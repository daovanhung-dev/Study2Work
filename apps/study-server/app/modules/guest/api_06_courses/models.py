from __future__ import annotations

from app.modules.guest._shared.course_catalog.constants import (
    DEFAULT_PAGE,
    DEFAULT_SIZE,
    MAX_SIZE,
)
from app.modules.guest._shared.course_catalog.helpers import normalize_sort
from pydantic import BaseModel, Field, field_validator


class CourseQuery(BaseModel):
    """Public query contract for the course-discovery endpoint."""

    category: int | None = None
    page: int = Field(default=DEFAULT_PAGE, ge=1)
    size: int = Field(default=DEFAULT_SIZE, ge=1, le=MAX_SIZE)
    sort: str | None = None

    _normalize_sort = field_validator("sort")(normalize_sort)
