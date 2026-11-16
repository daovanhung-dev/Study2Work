from __future__ import annotations

from app.core.responses import error_response
from app.modules.guest.api_19_courses_enrollments.models import CreateEnrollmentRequest
from app.utils.auth import validate_current_user_request
from app.utils.validate import parse_integer
from starlette.responses import JSONResponse

MAX_INT64 = 9_223_372_036_854_775_807


def validate_enrollment_request(authorization: str | None, course_id_raw: str, payload: CreateEnrollmentRequest, *, trace_id: str) -> tuple[int, int] | JSONResponse:
    auth = validate_current_user_request(authorization, role="STUDENT", trace_id=trace_id)
    if isinstance(auth, JSONResponse):
        return auth
    course_id = parse_integer(course_id_raw) or 0
    if not 1 <= course_id <= MAX_INT64 or type(payload.course_id) is not int or not 1 <= payload.course_id <= MAX_INT64:
        return error_response(status_code=422, business_code="DESIGN_VALIDATION_ERROR", message="Invalid course_id.", trace_id=trace_id)
    if payload.course_id != course_id:
        return error_response(status_code=422, business_code="DESIGN_VALIDATION_ERROR", message="Path and body course_id must match.", trace_id=trace_id)
    return auth[0], course_id
