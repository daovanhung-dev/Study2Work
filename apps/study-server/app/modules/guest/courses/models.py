from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator

DEFAULT_PAGE = 1
DEFAULT_SIZE = 20
MAX_SIZE = 100
SORT_FIELDS = frozenset({"id", "name", "price", "created_at"})
SORT_DIRECTIONS = frozenset({"asc", "desc"})


def normalize_sort(value: str | None) -> str | None:
    """Validate and normalize one public ``field:direction`` sort expression."""

    if value is None:
        return None

    parts = value.split(":")
    if len(parts) != 2:
        raise ValueError("sort phải có định dạng field:direction.")

    field, direction = parts
    if field not in SORT_FIELDS:
        raise ValueError("sort field không được hỗ trợ.")
    if direction not in SORT_DIRECTIONS:
        raise ValueError("sort direction không được hỗ trợ.")
    return f"{field}:{direction}"


def normalize_search_query(value: object) -> object:
    """Trim and lowercase the optional public course-search keyword."""

    if isinstance(value, str):
        normalized = value.strip().lower()
        return normalized or None
    return value


class CourseQuery(BaseModel):
    """Public query contract for the course-discovery endpoint."""

    category: int | None = None
    page: int = Field(default=DEFAULT_PAGE, ge=1)
    size: int = Field(default=DEFAULT_SIZE, ge=1, le=MAX_SIZE)
    sort: str | None = None

    _normalize_sort = field_validator("sort")(normalize_sort)


class CourseSearchQuery(BaseModel):
    """Public query contract for the course-search endpoint."""

    q: str | None = None
    category: int | None = None
    page: int = Field(default=DEFAULT_PAGE, ge=1)
    sort: str | None = None

    _normalize_q = field_validator("q", mode="before")(normalize_search_query)
    _normalize_sort = field_validator("sort")(normalize_sort)


class MentorSummary(BaseModel):
    """Public mentor projection embedded in a course item."""

    model_config = ConfigDict(extra="ignore")

    id: int
    full_name: str
    avatar_url: str | None = None


class Course(BaseModel):
    """Public fields returned for one published course."""

    model_config = ConfigDict(extra="ignore")

    id: int
    title: str
    description: str | None = None
    thumbnail_url: str | None = None
    price: str
    status: str
    mentor: MentorSummary


class Pagination(BaseModel):
    """Effective pagination metadata for API #6."""

    page: int
    size: int
    total: int
    total_pages: int


class CoursePage(BaseModel):
    """Published course collection and pagination metadata."""

    items: list[Course]
    pagination: Pagination
