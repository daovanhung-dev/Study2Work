from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.student.api_35_assignments_submissions.models import Submission, UploadFile
from app.modules.student.api_36_submissions_detail.query import FIND_STUDENT_SUBMISSION
from app.modules.student.api_36_submissions_detail.validate import validate_submission_detail
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def get_submission_detail(*, authorization: str | None, submission_id_raw: str, db: Session, trace_id: str) -> dict[str, Any] | JSONResponse:
    validated = validate_submission_detail(authorization, submission_id_raw, trace_id=trace_id)
    if isinstance(validated, JSONResponse):
        return validated
    user_id, submission_id = validated
    try:
        row = query_one(db, FIND_STUDENT_SUBMISSION, {"submission_id": submission_id, "user_id": user_id})
        if row is None:
            return error_response(status_code=404, business_code="DESIGN_RESOURCE_NOT_FOUND", message="Submission not found.", trace_id=trace_id)
        file_data = None
        if row.get("file_id") is not None:
            file_data = {"id": row["file_id"], "name": row["file_name"], "url": row["file_url"], "content_type": row["file_content_type"], "size_bytes": row["file_size_bytes"], "status": row["file_status"]}
        data = {key: row[key] for key in ("id", "assignment_id", "user_id", "content", "status", "submitted_at", "score", "feedback")}
        data["files"] = [UploadFile.model_validate(file_data).model_dump(mode="json")] if file_data else []
        submission = Submission.model_validate(data)
    except (SQLAlchemyError, ValidationError, KeyError, TypeError):
        db.rollback()
        logger.exception("Get Student submission failed; trace_id=%s", trace_id)
        return error_response(status_code=500, business_code="DESIGN_INTERNAL_ERROR", message="Submission could not be retrieved.", trace_id=trace_id)
    return success_response(business_code="DESIGN_RESOURCE_RETRIEVED", message="Submission retrieved.", trace_id=trace_id, data=submission.model_dump(mode="json", exclude_none=True))
