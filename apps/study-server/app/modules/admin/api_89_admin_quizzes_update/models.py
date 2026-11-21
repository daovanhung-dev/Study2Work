"""Khai báo success envelope cho API #89 và tái sử dụng Quiz projection của API #88."""

from __future__ import annotations

from typing import Any

from app.modules.admin.api_88_admin_quizzes_create.models import CreateAdminQuizData
from pydantic import BaseModel, ConfigDict


class UpdateAdminQuizEnvelope(BaseModel):
    """Khai báo envelope trả về Quiz sau khi metadata và child set đã được thay."""

    success: bool
    businessCode: str
    message: str
    data: CreateAdminQuizData
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
