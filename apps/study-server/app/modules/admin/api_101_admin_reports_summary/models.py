"""Khai báo response model của API #101 Admin report summary."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AdminReportPeriod(BaseModel):
    """Biểu diễn hai đầu ngày inclusive của kỳ báo cáo."""

    from_date: date = Field(alias="from")
    to_date: date = Field(alias="to")

    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class AdminReportMetric(BaseModel):
    """Biểu diễn một count metric bằng decimal string theo API contract."""

    key: str
    value: str
    label: str

    model_config = ConfigDict(extra="forbid")


class AdminReportSummary(BaseModel):
    """Gom kỳ, bốn KPI đã chốt và thời điểm dựng báo cáo."""

    period: AdminReportPeriod
    metrics: list[AdminReportMetric]
    generated_at: datetime

    model_config = ConfigDict(extra="forbid")


class GetAdminReportSummaryEnvelope(BaseModel):
    """Khai báo envelope success chuẩn của API #101."""

    success: bool
    businessCode: str
    message: str
    data: AdminReportSummary
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
