from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.student.api_35_assignments_submissions.models import Submission, UploadFile
from app.modules.student.api_35_assignments_submissions.query import (
    FIND_ACTIVE_ENROLLMENT,
    FIND_ASSIGNMENT,
    FIND_SUBMISSION_UPLOADS,
    INSERT_SUBMISSION,
    INSERT_SUBMISSION_UPLOAD,
)
from app.modules.student.api_35_assignments_submissions.validate import validate_submission_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def create_submission(
    *, authorization: str | None, assignment_id_raw: str, payload: Any, db: Session, trace_id: str
) -> dict[str, Any] | JSONResponse:
    validated = validate_submission_request(
        authorization, assignment_id_raw, payload, trace_id=trace_id
    )
    if isinstance(validated, JSONResponse):
        return validated
    user_id, assignment_id, submission_text, upload_ids = validated
    try:
        assignment = query_one(db, FIND_ASSIGNMENT, {"assignment_id": assignment_id})
        if assignment is None:
            return error_response(
                status_code=404,
                business_code="DESIGN_RESOURCE_NOT_FOUND",
                message="Assignment not found.",
                trace_id=trace_id,
            )
        if (
            query_one(
                db,
                FIND_ACTIVE_ENROLLMENT,
                {"user_id": user_id, "course_id": assignment["course_id"]},
            )
            is None
        ):
            return error_response(
                status_code=403,
                business_code="DESIGN_ACCESS_DENIED",
                message="Active course enrollment is required.",
                trace_id=trace_id,
            )
        due_at = assignment.get("due_at")
        if due_at is not None:
            now = datetime.now(UTC)
            comparable_due = due_at.replace(tzinfo=UTC) if due_at.tzinfo is None else due_at
            if now > comparable_due:
                return error_response(
                    status_code=409,
                    business_code="DESIGN_STATE_CONFLICT",
                    message="Assignment deadline has passed.",
                    trace_id=trace_id,
                )
        # Đọc và xác thực toàn bộ asset theo đúng Student, course và mục đích upload.
        upload_rows = (
            query_many(
                db,
                FIND_SUBMISSION_UPLOADS,
                {
                    "upload_ids": upload_ids,
                    "user_id": user_id,
                    "course_id": assignment["course_id"],
                },
            )
            if upload_ids
            else []
        )
        uploads_by_id = {upload["id"]: upload for upload in upload_rows}
        if len(uploads_by_id) != len(upload_ids):
            return error_response(
                status_code=403,
                business_code="DESIGN_ACCESS_DENIED",
                message="Upload is not available for this assignment.",
                trace_id=trace_id,
            )
        ordered_uploads = [uploads_by_id[upload_id] for upload_id in upload_ids]
        # Ghi URL đầu tiên vào cột cũ để các consumer chưa chuyển đổi tiếp tục đọc được.
        row = query_one(
            db,
            INSERT_SUBMISSION,
            {
                "assignment_id": assignment_id,
                "user_id": user_id,
                "content": submission_text,
                "file_url": ordered_uploads[0]["url"] if ordered_uploads else None,
            },
        )
        if row is None:
            db.rollback()
            return _internal_error(trace_id)
        # Lưu từng upload cùng vị trí FE gửi, chung transaction với submission.
        for asset_position, upload in enumerate(ordered_uploads):
            linked = query_one(
                db,
                INSERT_SUBMISSION_UPLOAD,
                {
                    "submission_id": row["id"],
                    "upload_id": upload["id"],
                    "asset_position": asset_position,
                },
            )
            if linked is None:
                db.rollback()
                return _internal_error(trace_id)
        submission = Submission(
            **row, files=[UploadFile.model_validate(upload) for upload in ordered_uploads]
        )
        db.commit()
    except (SQLAlchemyError, ValidationError, TypeError):
        db.rollback()
        logger.exception("Create assignment submission failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    return success_response(
        business_code="DESIGN_RESOURCE_CREATED",
        message="Submission created.",
        trace_id=trace_id,
        data=submission.model_dump(mode="json", exclude_none=True),
    )


def _internal_error(trace_id: str) -> JSONResponse:
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Submission could not be created.",
        trace_id=trace_id,
    )
