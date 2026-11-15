from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CreateSubmissionRequest(BaseModel):
    content: str | None = None
    upload_id: int | None = None


class UploadFile(BaseModel):
    id: int
    name: str
    url: str
    content_type: str
    size_bytes: int
    status: str


class Submission(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    assignment_id: int
    user_id: int
    content: str | None = None
    files: list[UploadFile]
    status: str
    submitted_at: datetime
    score: Decimal | None = None
    feedback: str | None = None
