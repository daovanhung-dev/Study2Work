"""FastAPI exception handlers that preserve the public API contract."""

from __future__ import annotations

import logging
from collections.abc import Sequence
from typing import Any

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.core.responses import ApiError, ErrorDetail, error_response
from app.core.trace import get_trace_id

logger = logging.getLogger(__name__)


def _validation_field(location: Sequence[Any]) -> str | None:
    ignored_locations = {"body", "query", "path", "header", "cookie"}
    parts = [str(part) for part in location if str(part) not in ignored_locations]
    return ".".join(parts) or None


async def api_error_handler(request: Request, exc: ApiError) -> JSONResponse:
    """Render an explicitly raised application error."""

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            business_code=exc.business_code,
            message=exc.message,
            trace_id=exc.trace_id or get_trace_id(request),
            errors=exc.errors,
        ),
        headers=exc.headers,
    )


async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    """Render HTTPException without exposing arbitrary exception details."""

    trace_id = get_trace_id(request)
    if isinstance(exc.detail, dict) and exc.detail.get("success") is False:
        content = dict(exc.detail)
        content.setdefault("traceId", trace_id)
    else:
        content = error_response(
            business_code="HTTP_ERROR",
            message="Yêu cầu không thể được xử lý.",
            trace_id=trace_id,
        )

    return JSONResponse(
        status_code=exc.status_code,
        content=content,
        headers=exc.headers,
    )


async def request_validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Map FastAPI/Pydantic validation details into safe field errors."""

    errors = [
        ErrorDetail(
            field=_validation_field(error.get("loc", ())),
            code=str(error.get("type", "INVALID_FIELD")).upper().replace(".", "_"),
            message=str(error.get("msg", "Giá trị không hợp lệ.")),
        )
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=error_response(
            business_code="VALIDATION_ERROR",
            message="Dữ liệu đầu vào không hợp lệ.",
            trace_id=get_trace_id(request),
            errors=errors,
        ),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Return a safe generic error while retaining internal diagnostic logging."""

    trace_id = get_trace_id(request)
    logger.exception("Unhandled API error; trace_id=%s", trace_id, exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response(
            business_code="INTERNAL_SERVER_ERROR",
            message="Đã xảy ra lỗi nội bộ hệ thống.",
            trace_id=trace_id,
        ),
    )
