from __future__ import annotations

import json

from app.core.responses import error_response
from app.modules.student.api_35_assignments_submissions.models import CreateSubmissionRequest
from app.utils.auth import validate_current_user_request
from app.utils.validate import parse_integer
from starlette.responses import JSONResponse

MAX_INT64 = 9_223_372_036_854_775_807


def validate_submission_request(
    authorization: str | None,
    assignment_id_raw: str,
    payload: CreateSubmissionRequest,
    *,
    trace_id: str,
) -> tuple[int, int, str | None, list[int]] | JSONResponse:
    auth = validate_current_user_request(authorization, role="STUDENT", trace_id=trace_id)
    if isinstance(auth, JSONResponse):
        return auth
    assignment_id = parse_integer(assignment_id_raw) or 0
    if not 1 <= assignment_id <= MAX_INT64:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Invalid assignment_id.",
            trace_id=trace_id,
        )
    # Chuẩn hóa tên text mới và content cũ; từ chối payload gửi đồng thời hai tên.
    if payload.text is not None and payload.content is not None:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Send either text or content.",
            trace_id=trace_id,
        )
    submission_text = payload.text if payload.text is not None else payload.content

    # Giải mã JSON array FE hiện gửi, vẫn chấp nhận upload_id đơn từ client cũ.
    if payload.file_refs is not None and payload.upload_id is not None:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Send either file refs or upload_id.",
            trace_id=trace_id,
        )
    if payload.file_refs is not None:
        try:
            file_ids = json.loads(payload.file_refs)
        except (json.JSONDecodeError, TypeError):
            return error_response(
                status_code=422,
                business_code="DESIGN_VALIDATION_ERROR",
                message="file refs must be a JSON array of upload IDs.",
                trace_id=trace_id,
            )
        if not isinstance(file_ids, list):
            return error_response(
                status_code=422,
                business_code="DESIGN_VALIDATION_ERROR",
                message="file refs must be a JSON array of upload IDs.",
                trace_id=trace_id,
            )
    elif payload.upload_id is not None:
        file_ids = [payload.upload_id]
    else:
        file_ids = []

    # Chỉ nhận ID BIGINT dương, không nhận bool/string hoặc ID lặp trong danh sách.
    if any(type(file_id) is not int or not 1 <= file_id <= MAX_INT64 for file_id in file_ids):
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Invalid upload ID in file refs.",
            trace_id=trace_id,
        )
    if len(set(file_ids)) != len(file_ids):
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="file refs cannot contain duplicate upload IDs.",
            trace_id=trace_id,
        )
    if (submission_text is None or not submission_text.strip()) and not file_ids:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Submission must contain text or at least one file.",
            trace_id=trace_id,
        )
    return auth[0], assignment_id, submission_text, file_ids
