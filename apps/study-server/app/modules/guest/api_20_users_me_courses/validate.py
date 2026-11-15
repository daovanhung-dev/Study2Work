from __future__ import annotations

from app.core.responses import error_response
from app.modules.guest._shared.course_catalog.constants import DEFAULT_PAGE, DEFAULT_SIZE
from app.utils.auth import validate_current_user_request
from app.utils.validate import parse_integer
from starlette.responses import JSONResponse

MAX_INT32 = 2_147_483_647


def validate_courses_request(authorization: str | None, page_raw: str | None, status_filter: str | None, *, trace_id: str) -> tuple[int, int, str | None] | JSONResponse:
    auth = validate_current_user_request(authorization, role="STUDENT", trace_id=trace_id)
    if isinstance(auth, JSONResponse):
        return auth
    page = DEFAULT_PAGE if page_raw is None else (parse_integer(page_raw) or 0)
    if not 1 <= page <= MAX_INT32:
        return error_response(status_code=422, business_code="DESIGN_VALIDATION_ERROR", message="Invalid page.", trace_id=trace_id)
    return auth[0], page, status_filter.strip() if status_filter else None
