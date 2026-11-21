from __future__ import annotations

from app.core.responses import error_response
from app.modules.student.api_17_payments.models import CreatePaymentRequest
from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse

MAX_INT64 = 9_223_372_036_854_775_807


def validate_payment_request(authorization: str | None, payload: CreatePaymentRequest, *, trace_id: str) -> JSONResponse | tuple[int, CreatePaymentRequest]:
    auth = validate_current_user_request(authorization, role="STUDENT", trace_id=trace_id)
    if isinstance(auth, JSONResponse):
        return auth
    if type(payload.order_id) is not int or not 1 <= payload.order_id <= MAX_INT64 or not payload.provider.strip():
        return error_response(status_code=422, business_code="DESIGN_VALIDATION_ERROR", message="Invalid payment request.", trace_id=trace_id)
    return auth[0], payload.model_copy(update={"provider": payload.provider.strip()})
