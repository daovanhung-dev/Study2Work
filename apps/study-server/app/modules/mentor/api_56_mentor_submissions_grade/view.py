"""Điều phối quyền Mentor, cập nhật grade và dựng Submission response API #56."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from decimal import Decimal, InvalidOperation
from typing import Any

from app.core.database import query_one
from app.core.responses import ErrorDetail, error_response, success_response
from app.modules.mentor.api_54_mentor_submissions_list.models import SubmissionResponse
from app.modules.mentor.api_56_mentor_submissions_grade.models import GradeSubmissionRequest
from app.modules.mentor.api_56_mentor_submissions_grade.query import (
    FIND_GRADED_SUBMISSION_UPLOAD,
    LOCK_MENTOR_SUBMISSION_FOR_GRADE,
    UPDATE_MENTOR_SUBMISSION_GRADE,
)
from app.modules.mentor.api_56_mentor_submissions_grade.validate import (
    INT64_MAX,
    parse_assignment_max_score,
    parse_submission_id,
    score_is_within_assignment_max,
)
from app.modules.student.api_34_uploads.models import UploadAssetResponse
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn cho truy vấn, ghi điểm hoặc ánh xạ Submission."""

    # Không phản chiếu SQL, exception hay dữ liệu row nội bộ ra response.
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Submission grade could not be saved.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 cho path không hợp lệ hoặc Submission không tồn tại."""

    # Giữ lỗi resource trong đúng error set của API catalog.
    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Submission not found.",
        trace_id=trace_id,
    )


def _access_denied(trace_id: str) -> JSONResponse:
    """Dựng lỗi 403 khi Submission không thuộc course của Mentor hiện tại."""

    # Không tiết lộ bài nộp thuộc course của Mentor khác.
    return error_response(
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message="Access denied.",
        trace_id=trace_id,
    )


def _score_out_of_range(trace_id: str) -> JSONResponse:
    """Dựng lỗi 422 cho score ngoài fallback [0, assignment.max_score]."""

    # Dùng field error an toàn để client biết score không đạt candidate range.
    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Score is outside the assignment range.",
        trace_id=trace_id,
        errors=(
            ErrorDetail(
                field="score",
                code="VALUE_OUT_OF_RANGE",
                message="Score must be between zero and the assignment maximum.",
            ),
        ),
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction do dở mà không che mất lỗi gốc."""

    try:
        # Nhả khóa row và hủy update dở trước khi dependency đóng Session.
        db.rollback()
    except SQLAlchemyError:
        logger.error("Mentor submission grade rollback failed; trace_id=%s", trace_id)


def _required_database_ids_are_valid(row: Mapping[str, Any], submission_id: int) -> bool:
    """Kiểm tra khóa Submission, Assignment, Course và Mentor trước khi xử lý."""

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
    score: int,
) -> bool:
    """Xác nhận UPDATE trả đúng row, score/status mục tiêu và feedback được giữ nguyên."""

    if (
        row.get("id") != submission_id
        or row.get("assignment_id") != current.get("assignment_id")
        or row.get("user_id") != current.get("user_id")
        or row.get("status") != "GRADED"
        or row.get("feedback") != current.get("feedback")
        or row.get("score") is None
    ):
        return False
    try:
        # Decimal so sánh chính xác integer request với NUMERIC(6,2) RETURNING.
        return Decimal(str(row.get("score"))) == Decimal(score)
    except (InvalidOperation, TypeError):
        return False


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
        # Giữ nguyên field, decimal-string score và omit-null behavior của API #54/#55.
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


# API #56 mentor_submissions_grade
def grade_mentor_submission(
    *,
    authorization: str | None,
    submission_id_value: str,
    grade_request: GradeSubmissionRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Mentor, cập nhật score/status và trả Submission đã chấm."""

    # Xác thực Bearer, subject số và role Mentor trước khi parse ID hoặc đọc DB.
    authentication = validate_current_user_request(
        authorization,
        role="MENTOR",
        trace_id=trace_id,
        internal_error_message="Submission grade could not be saved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    mentor_id, _roles = authentication

    # Parse raw path để sai định dạng hoặc overflow dùng mã 404 trong catalog.
    submission_id = parse_submission_id(submission_id_value)
    if submission_id is None:
        return _not_found(trace_id)

    # Lock Submission rồi LEFT JOIN để phát hiện assignment/course null hoặc orphan.
    try:
        current = query_one(
            db,
            LOCK_MENTOR_SUBMISSION_FOR_GRADE,
            {"submission_id": submission_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor submission grade lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if current is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(current, Mapping) or not _required_database_ids_are_valid(
        current,
        submission_id,
    ):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor submission grade relation mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if current.get("mentor_id") != mentor_id:
        _rollback_safely(db, trace_id=trace_id)
        return _access_denied(trace_id)

    # Xác nhận candidate max_score trước khi áp dụng range fallback cho điểm nguyên.
    max_score = parse_assignment_max_score(current.get("max_score"))
    if max_score is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Assignment maximum score projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if not score_is_within_assignment_max(grade_request.score, max_score):
        _rollback_safely(db, trace_id=trace_id)
        return _score_out_of_range(trace_id)

    # Cập nhật score và trạng thái AC-23 trong cùng transaction; rubric descriptor không có target.
    try:
        updated = query_one(
            db,
            UPDATE_MENTOR_SUBMISSION_GRADE,
            {
                "submission_id": submission_id,
                "assignment_id": current.get("assignment_id"),
                "mentor_id": mentor_id,
                "score": Decimal(grade_request.score),
            },
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor submission grade update failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if updated is None:
        # Owner predicate được kiểm lại tại UPDATE để tránh ghi sau khi quyền đổi.
        _rollback_safely(db, trace_id=trace_id)
        return _access_denied(trace_id)
    if not isinstance(updated, Mapping) or not _updated_row_matches_candidate(
        updated,
        current=current,
        submission_id=submission_id,
        score=grade_request.score,
    ):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor submission grade UPDATE projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Dùng cùng lookup file exact URL/owner/purpose/course với API #55.
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
                FIND_GRADED_SUBMISSION_UPLOAD,
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

    # Kiểm tra Submission và UploadAsset projection trước commit để lỗi có thể rollback.
    submission = _map_submission(updated, asset_row=asset_row)
    if submission is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor submission grade response mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Chỉ commit sau khi cả update và response projection đều hợp lệ.
    try:
        db.commit()
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor submission grade commit failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả reusable Submission với business code update của API catalog.
    return success_response(
        business_code="DESIGN_RESOURCE_UPDATED",
        message="Submission grade saved.",
        trace_id=trace_id,
        data=submission.model_dump(mode="json", exclude_none=True),
    )
