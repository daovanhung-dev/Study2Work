from __future__ import annotations

from app.core.responses import error_response
from app.utils.auth import validate_current_user_request
from app.utils.validate import parse_integer
from starlette.responses import JSONResponse

MAX_INT64 = 9_223_372_036_854_775_807


def validate_achievements_request(authorization: str | None, course_id_raw: str | None, *, trace_id: str) -> tuple[int, int | None] | JSONResponse:
    auth = validate_current_user_request(authorization, role="STUDENT", trace_id=trace_id)
    if isinstance(auth, JSONResponse):
        return auth
    course_id = None
    if course_id_raw is not None:
        course_id = parse_integer(course_id_raw) or 0
        if not 1 <= course_id <= MAX_INT64:
            return error_response(status_code=500, business_code="DESIGN_INTERNAL_ERROR", message="Achievements could not be retrieved.", trace_id=trace_id)
    return auth[0], course_id
