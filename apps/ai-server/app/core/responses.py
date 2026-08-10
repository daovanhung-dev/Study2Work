"""Canonical API response builders and compatibility adapters."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from typing import Any, NoReturn

from fastapi import status
from pydantic import BaseModel, ConfigDict, Field


def utc_now_iso() -> str:
    """Return the current UTC time in the API's ISO-8601 format."""

    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class ErrorDetail(BaseModel):
    """One safe, client-facing validation or business error detail."""

    field: str | None = None
    code: str
    message: str

    model_config = ConfigDict(extra="forbid")


class ApiError(Exception):
    """A controlled error that can be converted into the standard envelope."""

    def __init__(
        self,
        *,
        status_code: int,
        business_code: str,
        message: str,
        trace_id: str,
        errors: Sequence[ErrorDetail] = (),
        headers: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.business_code = business_code
        self.message = message
        self.trace_id = trace_id
        self.errors = tuple(errors)
        self.headers = dict(headers or {})


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
    *,
    business_code: str,
    message: str,
    trace_id: str,
    errors: Sequence[ErrorDetail] = (),
    meta: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the canonical error envelope.

    Field-level errors are stored under ``meta.fieldErrors`` according to the
    canonical API design.  The legacy ``error_payload`` adapter below keeps
    top-level ``errors`` for existing callers during the transition.
    """

    response_meta = dict(meta or {})
    if errors:
        response_meta["fieldErrors"] = [error.model_dump(exclude_none=True) for error in errors]

    return {
        "success": False,
        "businessCode": business_code,
        "message": message,
        "data": None,
        "meta": response_meta,
        "traceId": trace_id,
    }


def raise_api_error(
    *,
    status_code: int,
    business_code: str,
    message: str,
    trace_id: str,
    errors: Sequence[ErrorDetail] = (),
    headers: Mapping[str, str] | None = None,
) -> NoReturn:
    """Raise a controlled error from a view or dependency."""

    raise ApiError(
        status_code=status_code,
        business_code=business_code,
        message=message,
        trace_id=trace_id,
        errors=errors,
        headers=headers,
    )


def success_payload(
    *,
    business_code: str,
    message: str,
    trace_id: str,
    data: Any = None,
    meta: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Compatibility alias for the original success helper."""

    return success_response(
        business_code=business_code,
        message=message,
        trace_id=trace_id,
        data=data,
        meta=meta,
    )


def error_payload(
    *,
    business_code: str,
    message: str,
    trace_id: str,
    errors: Sequence[ErrorDetail],
) -> dict[str, Any]:
    """Compatibility adapter that preserves top-level ``errors``."""

    return {
        "success": False,
        "businessCode": business_code,
        "message": message,
        "errors": [error.model_dump() for error in errors],
        "traceId": trace_id,
    }


class ApiResponse(BaseModel):
    """Compatibility model used by older module code."""

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
        return success_response(
            business_code=self.business_code,
            message=self.message,
            trace_id=self.trace_id,
            data=self.result,
            meta=self.meta,
        )

    def raise_error(self) -> NoReturn:
        raise_api_error(
            status_code=self.status_code,
            business_code=self.business_code,
            message=self.message,
            trace_id=self.trace_id,
        )
