from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CreateEnrollmentRequest(BaseModel):
    course_id: int


class Enrollment(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    course_id: int
    user_id: int
    status: str
    enrolled_at: datetime
    completed_at: datetime | None = None
