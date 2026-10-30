"""Khai báo request và response models cho API #88."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, StrictBool, StrictInt, StrictStr

QuestionType = Literal["SINGLE_CHOICE", "MULTIPLE_CHOICE", "TRUE_FALSE"]


class CreateAdminQuizBody(BaseModel):
    """Khai báo outer body đúng hai chuỗi mà API catalog yêu cầu."""

    config: StrictStr
    questions: StrictStr

    model_config = ConfigDict(extra="forbid", strict=True)


class CreateAdminQuizConfig(BaseModel):
    """Khai báo cấu hình Quiz lồng trong chuỗi config theo fallback DERIVED."""

    course_id: StrictInt
    title: StrictStr
    duration_minutes: StrictInt | None = None
    passing_score: StrictStr

    model_config = ConfigDict(extra="forbid", strict=True)


class CreateAdminQuizChoiceInput(BaseModel):
    """Khai báo text và cờ đáp án đúng của một lựa chọn đầu vào."""

    text: StrictStr
    is_correct: StrictBool = False

    model_config = ConfigDict(extra="forbid", strict=True)


class CreateAdminQuizQuestionInput(BaseModel):
    """Khai báo câu hỏi đầu vào với type và danh sách choices."""

    text: StrictStr
    type: QuestionType
    choices: list[CreateAdminQuizChoiceInput]

    model_config = ConfigDict(extra="forbid", strict=True)


class CreateAdminQuizInput(BaseModel):
    """Gom config và question set sau khi decode hai chuỗi outer body."""

    config: CreateAdminQuizConfig
    questions: list[CreateAdminQuizQuestionInput]

    model_config = ConfigDict(extra="forbid", strict=True)


class AdminQuizChoiceResponse(BaseModel):
    """Khai báo lựa chọn trả về cho Admin, gồm answer key theo fallback DERIVED."""

    id: int
    text: str
    is_correct: bool

    model_config = ConfigDict(extra="forbid")


class AdminQuizQuestionResponse(BaseModel):
    """Khai báo Question response với type và choices theo Quiz contract."""

    id: int
    text: str
    type: QuestionType
    choices: list[AdminQuizChoiceResponse]

    model_config = ConfigDict(extra="forbid")


class CreateAdminQuizData(BaseModel):
    """Khai báo Quiz response được tạo từ các hàng INSERT/RETURNING."""

    id: int
    course_id: int
    title: str
    duration_minutes: int | None = None
    passing_score: str
    questions: list[AdminQuizQuestionResponse]

    model_config = ConfigDict(extra="forbid")


class CreateAdminQuizEnvelope(BaseModel):
    """Khai báo success envelope cho API #88."""

    success: bool
    businessCode: str
    message: str
    data: CreateAdminQuizData
    meta: dict[str, object]
    traceId: str

    model_config = ConfigDict(extra="forbid")
