"""Mô hình dữ liệu cho API #28 lấy chi tiết quiz và danh sách câu hỏi."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class QuizChoiceItem(BaseModel):
    """Mô hình dữ liệu cho lựa chọn câu hỏi trong quiz (không chứa đáp án đúng)."""

    model_config = ConfigDict(extra="ignore")

    id: int
    choice_text: str


class QuizQuestionItem(BaseModel):
    """Mô hình dữ liệu cho câu hỏi trong bài quiz."""

    model_config = ConfigDict(extra="ignore")

    id: int
    text: str
    type: str = "MULTIPLE_CHOICE"
    choices: list[QuizChoiceItem] = []


class QuizDetail(BaseModel):
    """Mô hình dữ liệu chi tiết quiz theo contract API #28."""

    model_config = ConfigDict(extra="ignore")

    id: int
    course_id: int
    title: str
    duration_minutes: int | None = None
    passing_score: str
    questions: list[QuizQuestionItem] = []

