"""Khai báo success envelope cho chi tiết user API #69."""

from __future__ import annotations

from typing import Any

from app.modules.guest.api_04_users_me.models import UserProfile
from pydantic import BaseModel, ConfigDict


class GetAdminUserEnvelope(BaseModel):
    """Biểu diễn success envelope Admin chứa profile an toàn của một user."""

    success: bool
    businessCode: str
    message: str
    data: UserProfile
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
