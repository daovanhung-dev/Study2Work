"""Response models for the current-user profile endpoint."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserProfile(BaseModel):
    """Safe profile fields returned by API #4."""

    model_config = ConfigDict(extra="ignore")

    id: int
    full_name: str
    email: str
    role: str
    avatar_url: str | None = None
    phone: str | None = None
    status: str
    created_at: datetime
    updated_at: datetime
