"""Khai báo request đích publish/unpublish và envelope cho API #52."""

from typing import Any

from app.modules.mentor.api_49_mentor_content_list.models import ContentResponse
from pydantic import BaseModel, ConfigDict, Field


class PublishContentRequest(BaseModel):
    """Biểu diễn target state DERIVED dùng để phân biệt publish và unpublish."""

    published: bool = Field(strict=True)

    model_config = ConfigDict(extra="forbid")


class PublishContentEnvelope(BaseModel):
    """Biểu diễn envelope thành công của API #52 cùng Content đã cập nhật."""

    success: bool
    businessCode: str
    message: str
    data: ContentResponse
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
