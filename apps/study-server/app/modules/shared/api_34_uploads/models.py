"""Khai báo purpose và response model cho API #34."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class UploadPurpose(StrEnum):
    """Các mục đích upload được API #34 chấp nhận."""

    SUBMISSION = "SUBMISSION"
    LECTURE = "LECTURE"


class UploadAssetResponse(BaseModel):
    """Biểu diễn metadata UploadAsset mà API #34 trả về."""

    id: int
    name: str
    url: str
    content_type: str
    size_bytes: int
    status: str

    model_config = ConfigDict(extra="forbid")
