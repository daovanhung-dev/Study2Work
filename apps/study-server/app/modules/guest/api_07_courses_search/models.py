from __future__ import annotations

from app.modules.guest._shared.course_catalog.constants import DEFAULT_PAGE
from app.modules.guest._shared.course_catalog.helpers import normalize_sort
from pydantic import BaseModel, Field, field_validator


def normalize_search_query(value: object) -> object:
    """Trim and lowercase the optional public course-search keyword."""

    if isinstance(value, str):
        normalized = value.strip().lower()
        return normalized or None
    return value


class CourseSearchQuery(BaseModel):
    """Public query contract for the course-search endpoint."""

    q: str | None = None
    category: int | None = None
    page: int = Field(default=DEFAULT_PAGE, ge=1)
    sort: str | None = None

    _normalize_q = field_validator("q", mode="before")(normalize_search_query)
    _normalize_sort = field_validator("sort")(normalize_sort)
