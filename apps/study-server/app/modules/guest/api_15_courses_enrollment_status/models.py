"""Response models for the course enrollment status endpoint."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EnrollmentStatusResponse(BaseModel):
    """Enrollment fields returned by API #15."""

    model_config = ConfigDict(extra="ignore")

    id: int
    user_id: int
    course_id: int
    status: str
    enrolled_at: datetime
    completed_at: datetime | None = None