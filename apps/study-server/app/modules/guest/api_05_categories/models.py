from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

DEFAULT_LOCALE = "vi-VN"


class CategoryQuery(BaseModel):
    """Optional query contract for the public category endpoint."""

    locale: str | None = Field(default=None)


class Category(BaseModel):
    """Public category fields returned by API #5."""

    model_config = ConfigDict(extra="ignore")

    id: int
    name: str
    slug: str
    description: str | None = None


class Pagination(BaseModel):
    """Implicit single-page metadata for API #5."""

    page: int
    size: int
    total: int
    total_pages: int


class CategoryPage(BaseModel):
    """Category collection and its implicit pagination metadata."""

    items: list[Category]
    pagination: Pagination
