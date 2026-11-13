"""Định nghĩa response model cho API #32 lấy điểm/kết quả được phép xem."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class QuizAnswer(BaseModel):
    """Mô tả câu trả lời trong kết quả quiz attempt theo schema dùng chung."""

    model_config = ConfigDict(extra="ignore")

    question_id: int
    choice_ids: list[int] | None = None
    text_answer: str | None = None
    correct: bool | None = None
    score: Decimal | None = None


class QuizAttempt(BaseModel):
    """Mô tả kết quả quiz attempt API #32 trả về cho Student."""

    model_config = ConfigDict(extra="ignore")

    id: int
    quiz_id: int
    status: str
    started_at: datetime
    submitted_at: datetime | None = None
    score: Decimal | None = None
    answers: list[QuizAnswer]