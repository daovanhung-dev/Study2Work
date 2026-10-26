"""Khai báo request và response models cho API #47."""

from typing import Annotated, Any

from app.modules.student.api_34_uploads.models import UploadAssetResponse
from pydantic import BaseModel, ConfigDict, Field

Int64 = Annotated[
    int,
    Field(strict=True, ge=-(2**63), le=2**63 - 1, json_schema_extra={"format": "int64"}),
]
Int32 = Annotated[
    int,
    Field(strict=True, ge=-(2**31), le=2**31 - 1, json_schema_extra={"format": "int32"}),
]


class CreateLectureRequest(BaseModel):
    """Biểu diễn request JSON tạo lecture theo contract API #47."""

    title: str = Field(strict=True, max_length=200)
    content: Int64
    asset_refs: str = Field(strict=True)
    order: Int32

    model_config = ConfigDict(extra="forbid")


class LectureResponse(BaseModel):
    """Biểu diễn lecture mới cùng các UploadAsset đã được xác thực."""

    id: int
    course_id: int
    title: str
    content: str | None
    assets: list[UploadAssetResponse]
    order: int
    status: str

    model_config = ConfigDict(extra="forbid")


class CreateLectureEnvelope(BaseModel):
    """Describe the standard Study success envelope for a created lecture."""

    success: bool
    businessCode: str
    message: str
    data: LectureResponse
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
