from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class Achievement(BaseModel):
    id: int
    code: str
    title: str
    awarded_at: datetime
    course_id: int | None = None


class Pagination(BaseModel):
    page: int
    size: int
    total: int
    total_pages: int


class AchievementPage(BaseModel):
    items: list[Achievement]
    pagination: Pagination
