"""Định nghĩa response Assignment cho API #33."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class AssignmentDetail(BaseModel):
    """Giới hạn response vào các trường Assignment được API #33 công bố."""

    model_config = ConfigDict(extra="ignore")

    id: int
    course_id: int
    title: str
    description: str | None = None
    due_at: datetime | None = None
    max_score: Decimal