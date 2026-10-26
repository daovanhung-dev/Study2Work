"""Điều phối quyền Mentor, truy vấn và ánh xạ danh sách Submission cho API #54."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.guest._shared.course_catalog.constants import DEFAULT_SIZE
from app.modules.guest._shared.course_catalog.models import Pagination
from app.modules.mentor.api_54_mentor_submissions_list.models import (
    GetMentorSubmissionsEnvelope,
    MentorSubmissionsQuery,
    SubmissionPage,
    SubmissionResponse,
)
from app.modules.mentor.api_54_mentor_submissions_list.query import (
    COUNT_MENTOR_SUBMISSIONS,
    FIND_MENTOR_COURSE,
    LIST_MENTOR_SUBMISSIONS,
)
from app.modules.student.api_34_uploads.models import UploadAssetResponse
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn cho truy vấn hoặc ánh xạ Submission."""

    # Chỉ trả business code chung, không phản chiếu SQL hoặc dữ liệu nội bộ.
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Submissions could not be retrieved.",
        trace_id=trace_id,
    )


def _access_denied(trace_id: str) -> JSONResponse:
    """Dựng lỗi 403 khi course được yêu cầu thuộc Mentor khác."""

    # Không tiết lộ dữ liệu bài nộp của course ngoài quyền sở hữu trực tiếp.
    return error_response(
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message="Access denied.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction đọc dở mà không che mất lỗi gốc."""

    try:
        # Dọn transaction lỗi trước khi dependency đóng session.
        db.rollback()
    except SQLAlchemyError:
        logger.error("Mentor submissions rollback failed; trace_id=%s", trace_id)


def _map_submissions(
    rows: list[dict[str, Any]],
) -> list[SubmissionResponse] | None:
    """Ánh xạ các hàng SQL thành Submission và tối đa một UploadAsset tương ứng."""

    submissions: list[SubmissionResponse] = []
    try:
        # Chỉ dựng UploadAsset khi LATERAL query trả về một metadata row hoàn chỉnh.
        for row in rows:
            if not isinstance(row, Mapping):
                return None
            file_id = row.get("file_id")
            files: list[UploadAssetResponse] = []
            file_fields = (
                "file_name",
                "file_url",
                "file_content_type",
                "file_size_bytes",
                "file_status",
            )
            if file_id is None:
                if any(row.get(field) is not None for field in file_fields):
                    return None
            else:
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

            score = row.get("score")
            submissions.append(
                SubmissionResponse(
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
            )
    except (TypeError, ValidationError):
        # Sai kiểu hoặc thiếu cột bắt buộc khiến projection không thể phục vụ contract.
        return None

    return submissions


def get_mentor_submissions(
    *,
    authorization: str | None,
    submission_query: MentorSubmissionsQuery,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Mentor rồi trả trang bài nộp thuộc các course Mentor sở hữu."""

    # Xác thực Bearer, subject số và role Mentor trước mọi truy vấn dữ liệu.
    authentication = validate_current_user_request(
        authorization,
        role="MENTOR",
        trace_id=trace_id,
        internal_error_message="Submissions could not be retrieved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    mentor_id, _roles = authentication

    # Khi có course_id, dùng cùng direct-owner policy với các API Mentor hiện hành.
    if submission_query.course_id is not None:
        try:
            course = query_one(
                db,
                FIND_MENTOR_COURSE,
                {"course_id": submission_query.course_id},
            )
        except SQLAlchemyError:
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Mentor course access lookup failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        if course is not None:
            if not isinstance(course, Mapping) or course.get("id") != submission_query.course_id:
                _rollback_safely(db, trace_id=trace_id)
                logger.error("Mentor course access mapping failed; trace_id=%s", trace_id)
                return _internal_error(trace_id)
            if course.get("mentor_id") != mentor_id:
                _rollback_safely(db, trace_id=trace_id)
                return _access_denied(trace_id)

    # Đếm theo đúng Mentor, course và status predicates của truy vấn trang.
    params: dict[str, Any] = {
        "mentor_id": mentor_id,
        "course_id": submission_query.course_id,
        "status": submission_query.status,
    }
    try:
        count_row = query_one(db, COUNT_MENTOR_SUBMISSIONS, params)
        total = count_row.get("total") if isinstance(count_row, Mapping) else None
        if type(total) is not int or total < 0:
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Mentor submissions count mapping failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        offset = (submission_query.page - 1) * DEFAULT_SIZE
        rows = query_many(
            db,
            LIST_MENTOR_SUBMISSIONS,
            {**params, "limit": DEFAULT_SIZE, "offset": offset},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor submissions lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Kiểm tra toàn bộ projection trước khi trả dữ liệu cho client.
    items = _map_submissions(rows)
    if items is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor submissions response mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    total_pages = (total + DEFAULT_SIZE - 1) // DEFAULT_SIZE if total else 0
    try:
        page = SubmissionPage(
            items=items,
            pagination=Pagination(
                page=submission_query.page,
                size=DEFAULT_SIZE,
                total=total,
                total_pages=total_pages,
            ),
        )
        data = GetMentorSubmissionsEnvelope(
            success=True,
            businessCode="DESIGN_RESOURCE_RETRIEVED",
            message=("Submissions retrieved." if items else "No submissions found."),
            data=page,
            meta={},
            traceId=trace_id,
        )
    except (TypeError, ValidationError):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Mentor submissions page mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả collection, kể cả khi rỗng, để UI AC-23 có thể chọn bài cần chấm.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message=data.message,
        trace_id=trace_id,
        data=data.data.model_dump(mode="json", exclude_none=True),
    )
