"""Khai báo response envelope cho API #48."""

from typing import Any

from app.modules.mentor.api_47_mentor_lectures_create.models import LectureResponse
from pydantic import BaseModel, ConfigDict


class GetLectureEnvelope(BaseModel):
    """Biểu diễn Study success envelope chứa Lecture và UploadAsset đã lưu."""

    success: bool
    businessCode: str
    message: str
    data: LectureResponse
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
