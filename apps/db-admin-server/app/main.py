"""FastAPI composition root for the local Neon DB Admin service."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.api.routes import router
from app.core.config import Settings, get_settings
from app.core.responses import ApiError, ErrorDetail, error_response, success_response
from app.core.runtime import build_resources
from app.core.trace import TRACE_HEADER, get_trace_id, normalize_trace_id

logger = logging.getLogger("db_admin")


def create_app(settings: Settings | None = None) -> FastAPI:
    app = FastAPI(title="Study2Work Neon DB Admin", version="0.1.0")
    app.state.settings = settings
    app.state.resources = build_resources(settings) if settings is not None else None
    if settings is not None and settings.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=False,
            allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            allow_headers=["Authorization", "Content-Type", "X-Trace-Id"],
        )

    @app.middleware("http")
    async def trace_middleware(request: Request, call_next: Any) -> Any:
        request.state.trace_id = normalize_trace_id(request.headers.get(TRACE_HEADER))
        response = await call_next(request)
        response.headers[TRACE_HEADER] = get_trace_id(request)
        return response

    @app.exception_handler(ApiError)
    async def api_error_handler(request: Request, exc: ApiError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(
                business_code=exc.business_code,
                message=exc.message,
                trace_id=exc.trace_id or get_trace_id(request),
                errors=exc.errors,
            ),
        )

    @app.exception_handler(HTTPException)
    async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(
                business_code="DB_ADMIN_HTTP_ERROR",
                message="The request could not be processed.",
                trace_id=get_trace_id(request),
            ),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        errors: list[ErrorDetail] = []
        for item in exc.errors():
            location = ".".join(
                str(part) for part in item.get("loc", ()) if part not in {"body", "query", "path"}
            )
            errors.append(
                ErrorDetail(
                    field=location or None,
                    code="INVALID_FIELD",
                    message=str(item.get("msg", "Invalid value.")),
                )
            )
        return JSONResponse(
            status_code=422,
            content=error_response(
                business_code="DB_ADMIN_VALIDATION_ERROR",
                message="The request data is invalid.",
                trace_id=get_trace_id(request),
                errors=errors,
            ),
        )

    @app.exception_handler(Exception)
    async def unhandled_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(
            "Unhandled DB Admin error; trace_id=%s", get_trace_id(request), exc_info=exc
        )
        return JSONResponse(
            status_code=500,
            content=error_response(
                business_code="DB_ADMIN_INTERNAL_ERROR",
                message="An internal error occurred.",
                trace_id=get_trace_id(request),
            ),
        )

    @app.get("/", tags=["system"])
    def root(request: Request) -> dict[str, Any]:
        return success_response(
            business_code="DB_ADMIN_ROOT_LOADED",
            message="Neon DB Admin is running.",
            trace_id=get_trace_id(request),
            data={"service": "db-admin-api"},
        )

    @app.get("/health/live", tags=["system"])
    def health_live(request: Request) -> dict[str, Any]:
        return success_response(
            business_code="DB_ADMIN_HEALTH_LIVE",
            message="DB Admin API is live.",
            trace_id=get_trace_id(request),
            data={"service": "db-admin-api"},
        )

    app.include_router(router)
    return app


def _load_runtime_settings() -> Settings | None:
    """Keep imports usable for tooling while configuring CORS in a real run."""

    try:
        return get_settings()
    except (RuntimeError, ValueError):
        return None


app = create_app(_load_runtime_settings())
