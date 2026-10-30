"""Điều phối quyền Mentor, đọc Submission và dựng response API #55."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.mentor.api_54_mentor_submissions_list.models import SubmissionResponse
from app.modules.mentor.api_55_mentor_submissions_detail.query import FIND_MENTOR_SUBMISSION
from app.modules.mentor.api_55_mentor_submissions_detail.validate import (
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
    """Dựng lỗi 500 an toàn khi truy vấn hoặc ánh xạ Submission thất bại."""

    # Không phản chiếu SQL, exception hoặc dữ liệu row nội bộ ra response.
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Submission could not be retrieved.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 cho path không hợp lệ hoặc Submission không tồn tại."""

    # Giữ lỗi path trong error set catalog mà không tự thêm 422.
    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Submission not found.",
        trace_id=trace_id,
    )


def _access_denied(trace_id: str) -> JSONResponse:
    """Dựng lỗi 403 khi course chứa Submission không thuộc Mentor hiện tại."""

    # Không tiết lộ dữ liệu bài nộp thuộc course của Mentor khác.
    return error_response(
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message="Access denied.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction đọc dở mà không che lỗi gốc."""

    try:
        # Dọn transaction lỗi trước khi dependency đóng session.
        db.rollback()
    except SQLAlchemyError:
        logger.error("Mentor submission rollback failed; trace_id=%s", trace_id)


def _required_database_ids_are_valid(row: Mapping[str, Any]) -> bool:
    """Kiểm tra các khóa candidate bắt buộc và quan hệ JOIN trước khi xét quyền."""

    required_ids = (
        "id",
        "assignment_id",
        "user_id",
        "matched_assignment_id",
        "course_id",
        "matched_course_id",
        "mentor_id",
    )
    # FK và owner ID phải là số dương trong miền BIGINT legacy.
    for field in required_ids:
        value = row.get(field)
        if type(value) is not int or not 1 <= value <= INT64_MAX:
            return False
    # Xác nhận JOIN thực sự khớp FK thay vì trả một projection sai quan hệ.
    return (
        row.get("matched_assignment_id") == row.get("assignment_id")
        and row.get("matched_course_id") == row.get("course_id")
    )


def _map_submission(row: Mapping[str, Any]) -> SubmissionResponse | None:
    """Ánh xạ một SQL row sang reusable Submission và tối đa một UploadAsset."""

    file_id = row.get("file_id")
    file_fields = (
        "file_name",
        "file_url",
        "file_content_type",
        "file_size_bytes",
        "file_status",
    )
    files: list[UploadAssetResponse] = []
    if file_id is None:
        # Một projection thiếu asset ID không được chứa metadata nửa vời.
        if any(row.get(field) is not None for field in file_fields):
            return None
    else:
        # Chỉ trả asset metadata khi LATERAL lookup khớp đầy đủ.
        try:
            files.append(
                UploadAssetResponse(
                    id=file_id,
                    name=row.get("file_name"),
                    url=row.get("file_url"),
                    content_type=row.get("file_content_type"),
                    size_bytes=row.get("file_size_bytes"),
                    status=row.get("file_status"),
                )
            )
        except (TypeError, ValidationError):
            return None

    score = row.get("score")
    try:
        # Giữ tên, kiểu và nullable fields của Submission mà API #54 đã dùng.
        return SubmissionResponse(
            id=row.get("id"),
            assignment_id=row.get("assignment_id"),
            user_id=row.get("user_id"),
            content=row.get("content"),
            files=files,
            status=row.get("status"),
            submitted_at=row.get("submitted_at"),
            score=None if score is None else str(score),
            feedback=row.get("feedback"),
        )
    except (TypeError, ValidationError):
        # Sai kiểu hoặc thiếu cột bắt buộc làm projection không còn dùng được.
        return None


# API #55 mentor_submission_detail
def get_mentor_submission(
    *,
    authorization: str | None,
    submission_id_value: str,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Mentor, kiểm tra course owner và trả Submission được chọn."""

    # Xác thực Bearer, subject số và role Mentor trước khi parse path hoặc đọc DB.
    authentication = validate_current_user_request(
        authorization,
        role="MENTOR",
        trace_id=trace_id,
        internal_error_message="Submission could not be retrieved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    mentor_id, _roles = authentication

    # Parse raw path để dùng mã 404 catalog cho sai định dạng hoặc vượt miền int64.
    submission_id = parse_submission_id(submission_id_value)
    if submission_id is None:
        return _not_found(trace_id)

    # LEFT JOIN giữ lại row để phát hiện assignment/course bị null hoặc orphan.
    try:
        row = query_one(
            db,
            FIND_MENTOR_SUBMISSION,
            {"submission_id": submission_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor submission lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if row is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(row, Mapping) or not _required_database_ids_are_valid(row):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor submission relation mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if row.get("id") != submission_id:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor submission ID mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if row.get("mentor_id") != mentor_id:
        _rollback_safely(db, trace_id=trace_id)
        return _access_denied(trace_id)

    # Chỉ dựng field Submission sau khi course access đã được xác nhận.
    submission = _map_submission(row)
    if submission is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor submission response mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả bản ghi read-only; rubric chưa có relation trong legacy assignment schema.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Submission retrieved.",
        trace_id=trace_id,
        data=submission.model_dump(mode="json", exclude_none=True),
    )
