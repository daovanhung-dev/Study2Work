"""Định nghĩa response resource source-backed của API #12."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ResourceDetail(BaseModel):
    """Giới hạn response vào metadata public có nguồn trong bảng resources."""

    model_config = ConfigDict(extra="ignore")

    id: int
    name: str
    type: str
    url: str | None = None
    lesson_id: int | None = None
