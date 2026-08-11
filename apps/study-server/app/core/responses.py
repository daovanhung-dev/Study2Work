"""Canonical API response models and controlled API errors."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, NoReturn

from fastapi import status
from pydantic import BaseModel, ConfigDict, Field


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


class ApiResponse(BaseModel):
    """Build the standard success API response."""

    business_code: str
    message: str
    trace_id: str

    result: Any = None
    meta: dict[str, Any] | None = None

    status_code: int = Field(
        default=status.HTTP_200_OK,
        ge=100,
        le=599,
    )

    def success_payload(self) -> dict[str, Any]:
        """Return the canonical success response envelope."""

        return {
            "success": True,
            "businessCode": self.business_code,
            "message": self.message,
            "data": self.result,
            "meta": self.meta or {},
            "traceId": self.trace_id,
        }

    def raise_error(
        self,
        *,
        errors: Sequence[ErrorDetail] = (),
        headers: Mapping[str, str] | None = None,
    ) -> NoReturn:
        """Raise a controlled API error."""

        raise ApiError(
            status_code=self.status_code,
            business_code=self.business_code,
            message=self.message,
            trace_id=self.trace_id,
            errors=errors,
            headers=headers,
        )