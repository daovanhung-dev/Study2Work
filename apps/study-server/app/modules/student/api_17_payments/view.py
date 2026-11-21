from __future__ import annotations

from typing import Any

from app.core.responses import error_response
from app.modules.student.api_17_payments.models import CreatePaymentRequest
from app.modules.student.api_17_payments.validate import validate_payment_request
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse


def create_payment(*, authorization: str | None, payload: CreatePaymentRequest, db: Session, trace_id: str) -> dict[str, Any] | JSONResponse:
    validated = validate_payment_request(authorization, payload, trace_id=trace_id)
    if isinstance(validated, JSONResponse):
        return validated
    # Provider/protocol is not configured. Fail closed before any Payment or Operation read/write.
    return error_response(status_code=503, business_code="DESIGN_DEPENDENCY_UNAVAILABLE", message="Payment provider is unavailable.", trace_id=trace_id)
