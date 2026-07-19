from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel


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
