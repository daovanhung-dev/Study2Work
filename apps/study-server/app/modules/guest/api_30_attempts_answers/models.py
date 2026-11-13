"""Mô hình dữ liệu cho API #30 autosave/lưu câu trả lời bài kiểm tra."""

from __future__ import annotations

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class SaveAnswerRequest(BaseModel):
    """Mô hình dữ liệu yêu cầu lưu câu trả lời bài kiểm tra."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    question_id: int
    answer: str = Field(
        default="",
        validation_alias=AliasChoices("answer(s)", "answer", "choice_id"),
    )


class QuizAnswerItem(BaseModel):
    """Mô hình dữ liệu thông tin câu trả lời của học viên (không chứa kết quả đúng sai)."""

    model_config = ConfigDict(extra="ignore")

    question_id: int
    choice_ids: list[int] = []
    text_answer: str | None = None


class QuizAttemptDetail(BaseModel):
    """Mô hình dữ liệu thông tin lượt làm bài kiểm tra kèm các câu trả lời đã lưu."""

    model_config = ConfigDict(extra="ignore")

    id: int
    quiz_id: int
    status: str
    started_at: str
    submitted_at: str | None = None
    score: str | None = None
    answers: list[QuizAnswerItem] = []

