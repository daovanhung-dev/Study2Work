"""Khai báo response models cho cây nội dung API #49."""

from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field

Int64 = Annotated[
    int,
    Field(strict=True, ge=-(2**63), le=2**63 - 1, json_schema_extra={"format": "int64"}),
]
Int32 = Annotated[
    int,
    Field(strict=True, ge=-(2**31), le=2**31 - 1, json_schema_extra={"format": "int32"}),
]


class ContentResponse(BaseModel):
    """Biểu diễn một node Content cùng liên kết cha-con để client dựng cây."""

    id: Int64
    course_id: Int64
    content_type: str
    title: str
    payload: dict[str, Any]
    status: str
    parent_id: Int64 | None = None
    order: Int32

    model_config = ConfigDict(extra="forbid")


class GetCourseContentsEnvelope(BaseModel):
    """Biểu diễn envelope thành công của API #49 chứa toàn bộ node Content."""

    success: bool
    businessCode: str
    message: str
    data: list[ContentResponse]
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
