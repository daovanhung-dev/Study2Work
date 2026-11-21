"""Response models for the course resources endpoint."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ResourceItem(BaseModel):
    """Resource contract fields returned by API #11."""

    model_config = ConfigDict(extra="ignore")

    id: int
    name: str
    type: str = Field(..., description="Resource type mapped from resource_type")
    url: str
    visibility: Literal["PUBLIC"]
    lesson_id: int | None = None
