from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.responses import ErrorDetail, error_payload
from app.core.trace import get_trace_id


@dataclass(slots=True)
class AppError(Exception):
    business_code: str
    message: str
    http_status: int = status.HTTP_400_BAD_REQUEST
    errors: list[ErrorDetail] = field(default_factory=list)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.http_status,
            content=error_payload(
                business_code=exc.business_code,
                message=exc.message,
                trace_id=get_trace_id(request),
                errors=exc.errors,
            ),
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        details = [
            ErrorDetail(
                field=".".join(str(part) for part in error["loc"]),
                code="E422",
                message=str(error["msg"]),
            )
            for error in exc.errors()
        ]
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=error_payload(
                business_code="SYSTEM-RESP-INVALID_INPUT",
                message="Validation failed.",
                trace_id=get_trace_id(request),
                errors=details,
            ),
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        request.app.state.logger.exception("SYSTEM-UNEXPECTED-ERROR", exc_info=exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_payload(
                business_code="SYSTEM-RESP-INTERNAL_ERROR",
                message="Internal server error.",
                trace_id=get_trace_id(request),
                errors=[ErrorDetail(field=None, code="E500", message="Internal server error.")],
            ),
        )


def serialize_error_details(errors: list[ErrorDetail]) -> list[dict[str, Any]]:
    return [error.model_dump() for error in errors]
