from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.student.api_35_assignments_submissions.models import Submission, UploadFile
from app.modules.student.api_35_assignments_submissions.query import (
    FIND_ACTIVE_ENROLLMENT,
    FIND_ASSIGNMENT,
    FIND_SUBMISSION_UPLOAD,
    INSERT_SUBMISSION,
)
from app.modules.student.api_35_assignments_submissions.validate import validate_submission_request
from pydantic import ValidationError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def create_submission(*, authorization: str | None, assignment_id_raw: str, payload: Any, db: Session, trace_id: str) -> dict[str, Any] | JSONResponse:
    validated = validate_submission_request(authorization, assignment_id_raw, payload, trace_id=trace_id)
    if isinstance(validated, JSONResponse):
        return validated
    user_id, assignment_id, body = validated
    try:
        assignment = query_one(db, FIND_ASSIGNMENT, {"assignment_id": assignment_id})
        if assignment is None:
            return error_response(status_code=404, business_code="DESIGN_RESOURCE_NOT_FOUND", message="Assignment not found.", trace_id=trace_id)
        if query_one(db, FIND_ACTIVE_ENROLLMENT, {"user_id": user_id, "course_id": assignment["course_id"]}) is None:
            return error_response(status_code=403, business_code="DESIGN_ACCESS_DENIED", message="Active course enrollment is required.", trace_id=trace_id)
        due_at = assignment.get("due_at")
        if due_at is not None:
            now = datetime.now(UTC)
            comparable_due = due_at.replace(tzinfo=UTC) if due_at.tzinfo is None else due_at
            if now > comparable_due:
                return error_response(status_code=409, business_code="DESIGN_STATE_CONFLICT", message="Assignment deadline has passed.", trace_id=trace_id)
        upload_row = None
        if body.upload_id is not None:
            upload_row = query_one(db, FIND_SUBMISSION_UPLOAD, {"upload_id": body.upload_id, "user_id": user_id, "course_id": assignment["course_id"]})
            if upload_row is None:
                return error_response(status_code=403, business_code="DESIGN_ACCESS_DENIED", message="Upload is not available for this assignment.", trace_id=trace_id)
        row = query_one(db, INSERT_SUBMISSION, {"assignment_id": assignment_id, "user_id": user_id, "content": body.content, "file_url": upload_row["url"] if upload_row else None})
        if row is None:
            db.rollback()
            return _internal_error(trace_id)
        submission = Submission(**row, files=[UploadFile.model_validate(upload_row)] if upload_row else [])
        db.commit()
    except (SQLAlchemyError, ValidationError, TypeError):
        db.rollback()
        logger.exception("Create assignment submission failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    return success_response(business_code="DESIGN_RESOURCE_CREATED", message="Submission created.", trace_id=trace_id, data=submission.model_dump(mode="json", exclude_none=True))


def _internal_error(trace_id: str) -> JSONResponse:
    return error_response(status_code=500, business_code="DESIGN_INTERNAL_ERROR", message="Submission could not be created.", trace_id=trace_id)
