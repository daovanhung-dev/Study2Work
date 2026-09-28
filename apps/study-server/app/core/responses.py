"""Canonical API response models and controlled API errors."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from fastapi import status
from pydantic import BaseModel, ConfigDict

from app.core.trace import create_trace_id, get_current_trace_id

INTERNAL_ERROR_MESSAGE = "Đã xảy ra lỗi nội bộ hệ thống."


class ErrorDetail(BaseModel):
    """One safe, client-facing validation or business error detail."""

    field: str | None = None
    code: str
    message: str

    model_config = ConfigDict(extra="forbid")


class ApiError(Exception):
    """Controlled API error handled by the global exception handler."""

    def __init__(
        self,
        *,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        business_code: str = "INTERNAL_SERVER_ERROR",
        message: str = INTERNAL_ERROR_MESSAGE,
        trace_id: str | None = None,
        data: Any = None,
        meta: Mapping[str, Any] | None = None,
        errors: Sequence[ErrorDetail] = (),
        headers: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__(message)

        self.status_code = status_code
        self.business_code = business_code
        self.message = message
        self.trace_id = trace_id or get_current_trace_id() or create_trace_id()
        self.data = data
        self.meta = dict(meta or {})
        self.errors = tuple(errors)
        self.headers = dict(headers or {})

    @classmethod
    def internal(cls, *, trace_id: str | None = None) -> ApiError:
        """Create a safe internal error when no request-specific mapping exists."""

        return cls(trace_id=trace_id)


def success_response(
    *,
    business_code: str,
    message: str,
    trace_id: str,
    data: Any = None,
    meta: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the canonical success response envelope."""

    return {
        "success": True,
        "businessCode": business_code,
        "message": message,
        "data": data,
        "meta": dict(meta or {}),
        "traceId": trace_id,
    }


def error_response(
    error: ApiError,
) -> dict[str, Any]:
    """Serialize an ApiError into the canonical error response envelope."""

    response_meta = dict(error.meta)
    if error.errors:
        response_meta["fieldErrors"] = [detail.model_dump() for detail in error.errors]

    return {
        "success": False,
        "businessCode": error.business_code,
        "message": error.message,
        "data": error.data if error.data is not None else {},
        "meta": response_meta,
        "traceId": error.trace_id,
    }
