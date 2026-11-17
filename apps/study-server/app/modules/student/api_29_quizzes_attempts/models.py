"""Mô hình dữ liệu cho API #29 tạo lượt làm bài kiểm tra (quiz attempt)."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class QuizAttemptDetail(BaseModel):
    """Mô hình dữ liệu chi tiết lượt làm bài kiểm tra theo contract API #29."""

    model_config = ConfigDict(extra="ignore")

    id: int
    quiz_id: int
    status: str = "IN_PROGRESS"
    started_at: str
    submitted_at: str | None = None
    score: str | None = None
    answers: list[Any] = []

