from __future__ import annotations

from app.core.responses import error_response
from app.modules.student.api_35_assignments_submissions.models import CreateSubmissionRequest
from app.utils.auth import validate_current_user_request
from app.utils.validate import parse_integer
from starlette.responses import JSONResponse

MAX_INT64 = 9_223_372_036_854_775_807


def validate_submission_request(authorization: str | None, assignment_id_raw: str, payload: CreateSubmissionRequest, *, trace_id: str) -> tuple[int, int, CreateSubmissionRequest] | JSONResponse:
    auth = validate_current_user_request(authorization, role="STUDENT", trace_id=trace_id)
    if isinstance(auth, JSONResponse):
        return auth
    assignment_id = parse_integer(assignment_id_raw) or 0
    if not 1 <= assignment_id <= MAX_INT64:
        return error_response(status_code=422, business_code="DESIGN_VALIDATION_ERROR", message="Invalid assignment_id.", trace_id=trace_id)
    if payload.upload_id is not None and (type(payload.upload_id) is not int or not 1 <= payload.upload_id <= MAX_INT64):
        return error_response(status_code=422, business_code="DESIGN_VALIDATION_ERROR", message="Invalid upload_id.", trace_id=trace_id)
    if (payload.content is None or not payload.content.strip()) and payload.upload_id is None:
        return error_response(status_code=422, business_code="DESIGN_VALIDATION_ERROR", message="Submission must contain text or one file.", trace_id=trace_id)
    return auth[0], assignment_id, payload
