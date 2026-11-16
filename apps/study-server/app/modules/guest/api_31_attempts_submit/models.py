from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SubmittedAnswer(BaseModel):
    model_config = ConfigDict(extra="ignore")

    question_id: int
    choice_ids: list[int] = Field(default_factory=list)
    correct: bool | None = None
    score: Decimal | None = None


class SubmittedAttempt(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    quiz_id: int
    status: str
    started_at: datetime
    submitted_at: datetime
    score: Decimal
    passed: bool
    answers: list[SubmittedAnswer]
