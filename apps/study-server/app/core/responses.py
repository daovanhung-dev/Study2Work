from __future__ import annotations

from typing import Any

from fastapi import HTTPException, status
from pydantic import BaseModel, Field


class ApiResponse(BaseModel):
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
        return {
            "success": True,
            "businessCode": self.business_code,
            "message": self.message,
            "data": self.result,
            "meta": self.meta or {},
            "traceId": self.trace_id,
        }

    def raise_error(self) -> None:
        raise HTTPException(
            status_code=self.status_code,
            detail={
                "success": False,
                "businessCode": self.business_code,
                "message": self.message,
                "traceId": self.trace_id,
            },
        )
