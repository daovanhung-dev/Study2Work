"""Canonical response envelope and controlled API errors."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from fastapi import status
from pydantic import BaseModel, ConfigDict


class ErrorDetail(BaseModel):
    field: str | None = None
    code: str
    message: str

    model_config = ConfigDict(extra="forbid")


class ApiError(Exception):
    def __init__(
        self,
        *,
        status_code: int,
        business_code: str,
        message: str,
        trace_id: str,
        errors: Sequence[ErrorDetail] = (),
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.business_code = business_code
        self.message = message
        self.trace_id = trace_id
        self.errors = tuple(errors)


def success_response(
    *,
    business_code: str,
    message: str,
    trace_id: str,
    data: Any = None,
    meta: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "success": True,
        "businessCode": business_code,
        "message": message,
        "data": data,
        "meta": dict(meta or {}),
        "traceId": trace_id,
    }


def error_response(
    *,
    business_code: str,
    message: str,
    trace_id: str,
    errors: Sequence[ErrorDetail] = (),
) -> dict[str, Any]:
    meta: dict[str, Any] = {}
    if errors:
        meta["fieldErrors"] = [error.model_dump() for error in errors]
    return {
        "success": False,
        "businessCode": business_code,
        "message": message,
        "data": None,
        "meta": meta,
        "traceId": trace_id,
    }


def validation_error(field: str, message: str) -> ErrorDetail:
    return ErrorDetail(field=field, code="INVALID_FIELD", message=message)


HTTP_INTERNAL_ERROR = status.HTTP_500_INTERNAL_SERVER_ERROR
