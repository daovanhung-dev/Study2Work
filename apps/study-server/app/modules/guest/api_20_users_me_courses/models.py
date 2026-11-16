from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CourseSummary(BaseModel):
    model_config = ConfigDict(extra="ignore")

    course_id: int
    name: str
    description: str | None = None
    thumbnail_url: str | None = None
    price: Decimal | None = None
    course_status: str | None = None
    enrollment_status: str
    enrolled_at: datetime


class Pagination(BaseModel):
    page: int
    size: int
    total: int
    total_pages: int


class CourseSummaryPage(BaseModel):
    items: list[CourseSummary]
    pagination: Pagination
