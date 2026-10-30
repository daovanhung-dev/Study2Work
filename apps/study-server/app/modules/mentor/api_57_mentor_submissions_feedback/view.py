"""Điều phối quyền Mentor, cập nhật feedback và dựng Submission response API #57."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_one
from app.core.responses import ErrorDetail, error_response, success_response
from app.modules.mentor.api_54_mentor_submissions_list.models import SubmissionResponse
from app.modules.mentor.api_57_mentor_submissions_feedback.models import (
    FeedbackSubmissionRequest,
)
from app.modules.mentor.api_57_mentor_submissions_feedback.query import (
    FIND_FEEDBACK_SUBMISSION_UPLOAD,
    LOCK_MENTOR_SUBMISSION_FOR_FEEDBACK,
    UPDATE_MENTOR_SUBMISSION_FEEDBACK,
)
from app.modules.mentor.api_57_mentor_submissions_feedback.validate import (
    INT64_MAX,
    parse_submission_id,
)
from app.modules.student.api_34_uploads.models import UploadAssetResponse
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn cho truy vấn, ghi feedback hoặc ánh xạ Submission."""

    # Không phản chiếu SQL, exception hay dữ liệu row nội bộ ra response.
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Submission feedback could not be saved.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 khi Submission không tồn tại."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Submission not found.",
        trace_id=trace_id,
    )


def _access_denied(trace_id: str) -> JSONResponse:
    """Dựng lỗi 403 khi course chứa Submission không thuộc Mentor hiện tại."""

    return error_response(
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message="Access denied.",
        trace_id=trace_id,
    )


def _invalid_path(trace_id: str) -> JSONResponse:
    """Dựng lỗi 422 cho path ID sai định dạng hoặc vượt miền int64."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Submission ID is invalid.",
        trace_id=trace_id,
        errors=(
            ErrorDetail(
                field="submission_id",
                code="INVALID_INT64",
                message="Submission ID must be a signed 64-bit integer.",
            ),
        ),
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction dở mà không che mất lỗi gốc."""

    try:
        # Nhả khóa row và hủy update dở trước khi dependency đóng Session.
        db.rollback()
    except SQLAlchemyError:
        logger.error("Mentor submission feedback rollback failed; trace_id=%s", trace_id)


def _required_database_ids_are_valid(row: Mapping[str, Any], submission_id: int) -> bool:
    """Kiểm tra Submission, Assignment, Course và Mentor trước khi xử lý."""

    required_ids = (
        "id",
        "assignment_id",
        "user_id",
        "matched_assignment_id",
        "course_id",
        "matched_course_id",
        "mentor_id",
    )
    # Các khóa candidate phải thuộc miền dương của schema BIGINT legacy.
    for field in required_ids:
        value = row.get(field)
        if type(value) is not int or not 1 <= value <= INT64_MAX:
            return False
    # Các JOIN phải khớp FK thật sự, không chỉ có cột tên giống nhau.
    return (
        row.get("id") == submission_id
        and row.get("matched_assignment_id") == row.get("assignment_id")
        and row.get("matched_course_id") == row.get("course_id")
    )


def _updated_row_matches_candidate(
    row: Mapping[str, Any],
    *,
    current: Mapping[str, Any],
    submission_id: int,
    feedback_text: str,
) -> bool:
    """Xác nhận UPDATE trả đúng Submission, feedback mới và score/status giữ nguyên."""

    return (
        row.get("id") == submission_id
        and row.get("assignment_id") == current.get("assignment_id")
        and row.get("user_id") == current.get("user_id")
        and row.get("feedback") == feedback_text
        and row.get("score") == current.get("score")
        and row.get("status") == current.get("status")
    )


def _map_submission(
    row: Mapping[str, Any],
    *,
    asset_row: Mapping[str, Any] | None,
) -> SubmissionResponse | None:
    """Ánh xạ row sau UPDATE và tối đa một UploadAsset sang Submission."""

    files: list[UploadAssetResponse] = []
    if asset_row is not None:
        try:
            # Chỉ dựng asset khi truy vấn scoped lookup trả metadata đầy đủ.
            files.append(
                UploadAssetResponse(
                    id=asset_row.get("id"),
                    name=asset_row.get("name"),
                    url=asset_row.get("url"),
                    content_type=asset_row.get("content_type"),
                    size_bytes=asset_row.get("size_bytes"),
                    status=asset_row.get("status"),
                )
            )
        except (TypeError, ValidationError):
            return None

    try:
        # Giữ nguyên field và nullable behavior của Submission API #54–56.
        return SubmissionResponse(
            id=row.get("id"),
            assignment_id=row.get("assignment_id"),
            user_id=row.get("user_id"),
            content=row.get("content"),
            files=files,
            status=row.get("status"),
            submitted_at=row.get("submitted_at"),
            score=None if row.get("score") is None else str(row.get("score")),
            feedback=row.get("feedback"),
        )
    except (TypeError, ValidationError):
        # Không commit nếu projection không còn thỏa Submission response model.
        return None


# API #57 mentor_submissions_feedback
def save_mentor_submission_feedback(
    *,
    authorization: str | None,
    submission_id_value: str,
    feedback_request: FeedbackSubmissionRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Mentor, cập nhật feedback rồi trả Submission đã lưu."""

    # Xác thực Bearer, subject số và role Mentor trước khi parse ID hoặc đọc DB.
    authentication = validate_current_user_request(
        authorization,
        role="MENTOR",
        trace_id=trace_id,
        internal_error_message="Submission feedback could not be saved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    mentor_id, _roles = authentication

    # API catalog có 422 nên path sai định dạng hoặc overflow dùng validation error.
    submission_id = parse_submission_id(submission_id_value)
    if submission_id is None:
        return _invalid_path(trace_id)

    # Lock Submission rồi LEFT JOIN để phát hiện assignment/course null hoặc orphan.
    try:
        current = query_one(
            db,
            LOCK_MENTOR_SUBMISSION_FOR_FEEDBACK,
            {"submission_id": submission_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor submission feedback lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if current is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(current, Mapping) or not _required_database_ids_are_valid(
        current,
        submission_id,
    ):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor submission feedback relation mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if current.get("mentor_id") != mentor_id:
        _rollback_safely(db, trace_id=trace_id)
        return _access_denied(trace_id)

    # Chỉ ghi feedback; attachments chưa có target storage được chứng minh.
    try:
        updated = query_one(
            db,
            UPDATE_MENTOR_SUBMISSION_FEEDBACK,
            {
                "submission_id": submission_id,
                "assignment_id": current.get("assignment_id"),
                "mentor_id": mentor_id,
                "feedback_text": feedback_request.feedback_text,
            },
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor submission feedback update failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if updated is None:
        # Owner predicate được kiểm lại tại UPDATE để tránh ghi sau khi quyền đổi.
        _rollback_safely(db, trace_id=trace_id)
        return _access_denied(trace_id)
    if not isinstance(updated, Mapping) or not _updated_row_matches_candidate(
        updated,
        current=current,
        submission_id=submission_id,
        feedback_text=feedback_request.feedback_text,
    ):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor submission feedback UPDATE projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Reuse the constrained student-file projection shared with API #54–56.
    asset_row: Mapping[str, Any] | None = None
    file_url = updated.get("file_url")
    if file_url is not None and not isinstance(file_url, str):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor submission file URL projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if file_url is not None:
        try:
            found_asset = query_one(
                db,
                FIND_FEEDBACK_SUBMISSION_UPLOAD,
                {
                    "file_url": file_url,
                    "user_id": updated.get("user_id"),
                    "course_id": current.get("course_id"),
                },
            )
        except SQLAlchemyError:
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Mentor submission file lookup failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        if found_asset is not None and not isinstance(found_asset, Mapping):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Mentor submission file mapping failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        asset_row = found_asset

    # Kiểm tra Submission và UploadAsset projection trước khi commit.
    submission = _map_submission(updated, asset_row=asset_row)
    if submission is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor submission feedback response mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Chỉ commit sau khi update và response projection đều hợp lệ.
    try:
        db.commit()
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor submission feedback commit failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_UPDATED",
        message="Submission feedback saved.",
        trace_id=trace_id,
        data=submission.model_dump(mode="json", exclude_none=True),
    )
