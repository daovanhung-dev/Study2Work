from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import HTTPException, status
from pydantic import BaseModel, Field


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class ErrorDetail(BaseModel):
    field: str | None = None
    code: str
    message: str


def success_payload(
    *,
    business_code: str,
    message: str,
    trace_id: str,
    data: Any,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "success": True,
        "businessCode": business_code,
        "message": message,
        "data": data,
        "meta": meta or {},
        "traceId": trace_id,
    }


def error_payload(
    *,
    business_code: str,
    message: str,
    trace_id: str,
    errors: list[ErrorDetail],
) -> dict[str, Any]:
    return {
        "success": False,
        "businessCode": business_code,
        "message": message,
        "errors": [error.model_dump() for error in errors],
        "traceId": trace_id,
    }


class ApiResponse(BaseModel):
    business_code: str
    message: str
    result: Any = None
    trace_id: str
    meta: dict[str, Any] | None = None
    status_code: int = Field(
        default=status.HTTP_200_OK,
        ge=100,
        le=599,
    )

    def success_payload(self) -> dict[str, Any]:
        return {
            "success": True,
            "businessCode": self.business_code,
            "message": self.message,
            "data": self.result,
            "meta": self.meta or {},
            "traceId": self.trace_id,
        }

    def raise_error(self) -> None:
        raise HTTPException(
            status_code=self.status_code,
            detail={
                "success": False,
                "businessCode": self.business_code,
                "message": self.message,
                "traceId": self.trace_id,
            },
        )
