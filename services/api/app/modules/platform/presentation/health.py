from __future__ import annotations

from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.core.responses import success_payload
from app.core.trace import get_trace_id

router = APIRouter(tags=["Platform"])


class HealthData(BaseModel):
    status: str
    service: str
    version: str
    environment: str


@router.get("/health")
async def health(request: Request) -> dict[str, object]:
    settings = request.app.state.settings
    version = getattr(settings, "app_version", "0.1.0")
    environment = getattr(settings, "app_env", "local")
    return success_payload(
        business_code="SYSTEM-HEALTH-SUCCESS",
        message="Service is healthy.",
        trace_id=get_trace_id(request),
        data=HealthData(
            status="ok",
            service="study2work-api",
            version=str(version),
            environment=str(environment),
        ).model_dump(),
    )
