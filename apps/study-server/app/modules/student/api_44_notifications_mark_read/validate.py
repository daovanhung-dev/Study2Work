from __future__ import annotations

from app.core.responses import error_response
from app.utils.auth import validate_current_user_request
from app.utils.validate import parse_integer
from starlette.responses import JSONResponse

MAX_INT64 = 9_223_372_036_854_775_807


def validate_mark_notification_read(authorization: str | None, notification_id_raw: str, *, trace_id: str) -> tuple[int, int] | JSONResponse:
    auth = validate_current_user_request(authorization, role="STUDENT", trace_id=trace_id)
    if isinstance(auth, JSONResponse):
        return auth
    notification_id = parse_integer(notification_id_raw) or 0
    if not 1 <= notification_id <= MAX_INT64:
        return error_response(status_code=422, business_code="DESIGN_VALIDATION_ERROR", message="Invalid notification_id.", trace_id=trace_id)
    return auth[0], notification_id
