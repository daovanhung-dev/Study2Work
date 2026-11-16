from __future__ import annotations

from app.core.responses import error_response
from app.modules.student.api_40_discussions_create.models import CreateDiscussionRequest
from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse

MAX_INT64 = 9_223_372_036_854_775_807


def validate_create_discussion(authorization: str | None, payload: CreateDiscussionRequest, *, trace_id: str) -> tuple[int, CreateDiscussionRequest] | JSONResponse:
    auth = validate_current_user_request(authorization, role="STUDENT", trace_id=trace_id)
    if isinstance(auth, JSONResponse):
        return auth
    if type(payload.course_id) is not int or not 1 <= payload.course_id <= MAX_INT64:
        return error_response(status_code=422, business_code="DESIGN_VALIDATION_ERROR", message="Invalid course_id.", trace_id=trace_id)
    if not payload.title.strip() or not payload.content.strip():
        return error_response(status_code=422, business_code="DESIGN_VALIDATION_ERROR", message="Title and content are required.", trace_id=trace_id)
    return auth[0], payload
