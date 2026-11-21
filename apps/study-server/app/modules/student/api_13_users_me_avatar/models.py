"""Khai báo request và response cho API tải avatar #13."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, StrictStr


class AvatarUploadRequest(BaseModel):
    """Khai báo JSON body chỉ nhận Data URL trong field image."""

    model_config = ConfigDict(extra="forbid")

    image: StrictStr


class AvatarUploadResult(BaseModel):
    """Chứa URL công khai do Object Storage trả về sau khi tải avatar."""

    model_config = ConfigDict(extra="forbid")

    avatar_url: str
