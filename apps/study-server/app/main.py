"""Là composition root của Study API: lắp settings, database dependency, middleware, exception
handler, router và endpoint hệ thống."""

from __future__ import annotations

from typing import Any, cast

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException

from app.api.v1 import router
from app.core.config import Settings, get_settings
from app.core.database import build_engine, build_session_factory, get_db, get_db_from_factory
from app.core.middleware import (
    TraceIdMiddleware,
    api_error_handler,
    http_exception_handler,
    request_validation_exception_handler,
    unhandled_exception_handler,
)
from app.core.responses import _ApiError, success_response
from app.core.trace import get_trace_id


def _settings_for_request(request: Request) -> Settings:
    """Lấy Settings đã gắn trên app.state của request nếu có, nếu không thì dùng get_settings() mặc
    định. Helper này cho phép health endpoint đọc cấu hình được inject trong test hoặc runtime."""

    configured_settings = getattr(request.app.state, "settings", None)
    return configured_settings or get_settings()


def create_app(app_settings: Settings | None = None) -> FastAPI:
    """Tạo FastAPI app và lắp tài liệu API, settings, engine/session factory khi được inject, CORS,
    trace middleware, exception handler và router v1. Trả về app đã compose; engine chỉ được tạo
    khi caller truyền Settings tường minh."""

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
    app.add_exception_handler(_ApiError, cast(Any, api_error_handler))
    app.add_exception_handler(
        RequestValidationError, cast(Any, request_validation_exception_handler)
    )
    app.add_exception_handler(Exception, unhandled_exception_handler)
    app.include_router(router)

    # API GET /
    @app.get("/", tags=["system"])
    def root(request: Request) -> dict[str, Any]:
        """Xử lý GET / và trả envelope thành công chứa tên dịch vụ cùng trace ID của request.
        Endpoint không truy vấn database."""

        return success_response(
            business_code="SYSTEM_ROOT_LOADED",
            message="Welcome to Study2Work.",
            trace_id=get_trace_id(request),
            data={"service": "study-api"},
        )

    # API GET /health/live
    @app.get("/health/live", tags=["health"])
    def health_live(request: Request) -> dict[str, Any]:
        """Xử lý GET /health/live, báo service còn phản hồi và cung cấp environment lấy từ
        Settings. Endpoint không kiểm tra kết nối dependency."""

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

    # API GET /health/ready
    @app.get("/health/ready", tags=["health"])
    def health_ready(request: Request) -> dict[str, Any]:
        """Xử lý GET /health/ready và trả nhãn cấu hình database/Redis cùng trace ID. Hàm chỉ kiểm
        tra sự hiện diện cấu hình; không mở kết nối hay chạy probe database."""

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

# Đăng ký HTTPException sau bộ xử lý tổng quát để FastAPI giữ nguyên
# các lỗi giao thức chuẩn nhưng vẫn dùng cấu trúc phản hồi an toàn của ứng dụng.
    app.add_exception_handler(HTTPException, cast(Any, http_exception_handler))
    return app


app = create_app()
