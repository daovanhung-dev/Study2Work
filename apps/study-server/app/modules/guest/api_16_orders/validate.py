from __future__ import annotations

from app.core.responses import error_response
from app.modules.guest.api_16_orders.models import CreateOrderRequest
from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse

MAX_INT64 = 9_223_372_036_854_775_807


def validate_order_request(
    authorization: str | None,
    payload: CreateOrderRequest,
    *,
    trace_id: str,
) -> tuple[int, CreateOrderRequest] | JSONResponse:
    auth = validate_current_user_request(authorization, role="STUDENT", trace_id=trace_id)
    if isinstance(auth, JSONResponse):
        return auth
    if type(payload.course_id) is not int or not 1 <= payload.course_id <= MAX_INT64:
        return error_response(status_code=422, business_code="DESIGN_VALIDATION_ERROR", message="Invalid course_id.", trace_id=trace_id)
    provider = payload.payment_provider.strip()
    if not provider:
        return error_response(status_code=422, business_code="DESIGN_VALIDATION_ERROR", message="Invalid payment_provider.", trace_id=trace_id)
    return auth[0], payload.model_copy(update={"payment_provider": provider})
