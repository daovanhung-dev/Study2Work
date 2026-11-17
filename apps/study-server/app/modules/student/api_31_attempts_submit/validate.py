from __future__ import annotations

from app.core.responses import error_response
from app.utils.auth import validate_current_user_request
from app.utils.validate import parse_integer
from starlette.responses import JSONResponse

MAX_INT64 = 9_223_372_036_854_775_807


def validate_submit_attempt(authorization: str | None, attempt_id_raw: str, *, trace_id: str) -> tuple[int, int] | JSONResponse:
    auth = validate_current_user_request(authorization, role="STUDENT", trace_id=trace_id)
    if isinstance(auth, JSONResponse):
        return auth
    attempt_id = parse_integer(attempt_id_raw) or 0
    if not 1 <= attempt_id <= MAX_INT64:
        return error_response(status_code=422, business_code="DESIGN_VALIDATION_ERROR", message="Invalid attempt_id.", trace_id=trace_id)
    return auth[0], attempt_id
