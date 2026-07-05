from __future__ import annotations

from fastapi import APIRouter, Request

from app.core.responses import success_payload
from app.core.trace import get_trace_id

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/live")
async def live(request: Request) -> dict[str, object]:
    settings = request.app.state.settings
    return success_payload(
        business_code="SYSTEM_HEALTH_LIVE",
        message="Study API is live.",
        trace_id=get_trace_id(request),
        data={
            "status": "ok",
            "service": "study-api",
            "version": settings.app_version,
            "environment": settings.app_env,
        },
    )


@router.get("/ready")
async def ready(request: Request) -> dict[str, object]:
    settings = request.app.state.settings
    return success_payload(
        business_code="SYSTEM_HEALTH_READY",
        message="Study API is ready.",
        trace_id=get_trace_id(request),
        data={
            "status": "ok",
            "service": "study-api",
            "dependencies": {
                "database": "configured",
                "redis": "configured",
            },
            "environment": settings.app_env,
        },
    )
