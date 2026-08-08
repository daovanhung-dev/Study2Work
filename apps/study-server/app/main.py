"""FastAPI composition root for the Study API."""

from __future__ import annotations

from typing import Any, cast

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException

from app.api.v1 import router
from app.core.config import Settings, get_settings
from app.core.database import build_engine, build_session_factory, get_db, get_db_from_factory
from app.core.exceptions import (
    api_error_handler,
    http_exception_handler,
    request_validation_exception_handler,
    unhandled_exception_handler,
)
from app.core.middleware import TraceIdMiddleware
from app.core.responses import ApiError, success_response
from app.core.trace import get_trace_id


def _settings_for_request(request: Request) -> Settings:
    configured_settings = getattr(request.app.state, "settings", None)
    return configured_settings or get_settings()


def create_app(app_settings: Settings | None = None) -> FastAPI:
    """Build an application instance with optional test/runtime settings."""

    docs_enabled = app_settings.enable_docs if app_settings is not None else True
    app = FastAPI(
        title="Study API",
        docs_url="/docs" if docs_enabled else None,
        redoc_url="/redoc" if docs_enabled else None,
        openapi_url="/openapi.json" if docs_enabled else None,
    )
    app.state.settings = app_settings
    if app_settings is not None:
        app.state.engine = build_engine(app_settings)
        app.state.session_factory = build_session_factory(app.state.engine)
        app.dependency_overrides[get_db] = lambda: get_db_from_factory(app.state.session_factory)

    if app_settings is not None and app_settings.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=app_settings.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.add_middleware(TraceIdMiddleware)
    app.add_exception_handler(ApiError, cast(Any, api_error_handler))
    app.add_exception_handler(
        RequestValidationError, cast(Any, request_validation_exception_handler)
    )
    app.add_exception_handler(Exception, unhandled_exception_handler)
    app.include_router(router)

    @app.get("/", tags=["system"])
    def root(request: Request) -> dict[str, Any]:
        return success_response(
            business_code="SYSTEM_ROOT_LOADED",
            message="Welcome to Study2Work.",
            trace_id=get_trace_id(request),
            data={"service": "study-api"},
        )

    @app.get("/health/live", tags=["health"])
    def health_live(request: Request) -> dict[str, Any]:
        settings = _settings_for_request(request)
        return success_response(
            business_code="SYSTEM_HEALTH_LIVE",
            message="Study API is live.",
            trace_id=get_trace_id(request),
            data={
                "service": "study-api",
                "environment": settings.app_env,
            },
        )

    @app.get("/health/ready", tags=["health"])
    def health_ready(request: Request) -> dict[str, Any]:
        settings = _settings_for_request(request)
        return success_response(
            business_code="SYSTEM_HEALTH_READY",
            message="Study API is ready.",
            trace_id=get_trace_id(request),
            data={
                "service": "study-api",
                "environment": settings.app_env,
                "dependencies": {
                    "database": "configured",
                    "redis": "configured" if settings.redis_url else "not_configured",
                },
            },
        )

    # HTTPException is registered after the generic handler so FastAPI keeps
    # its standard protocol errors while still using our safe envelope.
    app.add_exception_handler(HTTPException, cast(Any, http_exception_handler))
    return app


app = create_app()
