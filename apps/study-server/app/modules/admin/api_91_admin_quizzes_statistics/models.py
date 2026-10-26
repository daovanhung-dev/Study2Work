"""Khai báo response riêng cho phương án thống kê Quiz API #91."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AdminQuizStatistics(BaseModel):
    """Chứa số lượt làm và điểm tổng hợp của một Quiz theo proposal trong DD."""

    quiz_id: int = Field(json_schema_extra={"format": "int64"})
    attempt_count: int = Field(json_schema_extra={"format": "int64"})
    submitted_attempt_count: int = Field(json_schema_extra={"format": "int64"})
    graded_attempt_count: int = Field(json_schema_extra={"format": "int64"})
    average_score: str | None
    passed_attempt_count: int | None = Field(json_schema_extra={"format": "int64"})
    pass_rate_percent: str | None

    model_config = ConfigDict(extra="forbid")


class GetAdminQuizStatisticsEnvelope(BaseModel):
    """Khai báo envelope thành công cho response QuizStatistics dạng DERIVED."""

    success: bool
    businessCode: str
    message: str
    data: AdminQuizStatistics
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
