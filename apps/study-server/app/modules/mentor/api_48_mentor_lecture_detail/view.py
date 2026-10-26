"""Điều phối quyền Mentor, đọc Lecture/UploadAsset và dựng response API #48."""

from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.mentor.api_47_mentor_lectures_create.models import LectureResponse
from app.modules.mentor.api_48_mentor_lecture_detail.query import (
    FIND_LECTURE_UPLOAD_ASSETS,
    FIND_MENTOR_LECTURE,
)
from app.modules.mentor.api_48_mentor_lecture_detail.validate import parse_lecture_id
from app.modules.student.api_34_uploads.models import UploadAssetResponse
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi truy vấn hoặc ánh xạ Lecture API #48 thất bại."""

    # Không trả SQL, exception hoặc row mapping nội bộ cho client.
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Lecture could not be retrieved.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 cho path ID không hợp lệ hoặc lecture không tồn tại."""

    # Giữ status/business code trong catalog mà không thêm lỗi 422 cho path.
    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Lecture not found.",
        trace_id=trace_id,
    )


def _access_denied(trace_id: str) -> JSONResponse:
    """Dựng lỗi 403 khi Mentor không sở hữu course chứa lecture."""

    # Không cho biết lecture thuộc principal/course nào khác.
    return error_response(
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message="Access denied.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback session đọc dở và ghi nhận lỗi rollback mà không làm lộ nội bộ."""

    try:
        # Đóng transaction bị lỗi trước khi trả về response an toàn.
        db.rollback()
    except SQLAlchemyError:
        logger.error("Lecture detail rollback failed; trace_id=%s", trace_id)


def _map_assets(rows: list[dict[str, Any]]) -> list[UploadAssetResponse] | None:
    """Ánh xạ asset link rows theo thứ tự query hoặc báo metadata/link integrity lỗi."""

    assets: list[UploadAssetResponse] = []
    for row in rows:
        if row.get("id") != row.get("upload_id"):
            return None
        # Chỉ chuyển các field thuộc UploadAsset public contract.
        assets.append(
            UploadAssetResponse(
                id=row.get("id"),
                name=row.get("name"),
                url=row.get("url"),
                content_type=row.get("content_type"),
                size_bytes=row.get("size_bytes"),
                status=row.get("status"),
            )
        )
    return assets


# API #48 mentor_lecture_detail
def get_lecture(
    *,
    authorization: str | None,
    lecture_id_value: str,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Mentor, kiểm tra direct owner và trả Lecture cùng assets đã liên kết."""

    # Xác thực Bearer, numeric subject và role trước khi đọc path hoặc database.
    authentication = validate_current_user_request(
        authorization,
        role="MENTOR",
        trace_id=trace_id,
        internal_error_message="Lecture could not be retrieved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    mentor_id, _roles = authentication

    # Parse path trong view để map lỗi sang 404 đã có trong catalog thay vì tự thêm 422.
    lecture_id = parse_lecture_id(lecture_id_value)
    if lecture_id is None:
        return _not_found(trace_id)

    # Đọc lecture cùng course parent để phân biệt 404, owner mismatch và integrity failure.
    try:
        row = query_one(db, FIND_MENTOR_LECTURE, {"lecture_id": lecture_id})
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Lecture detail lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if row is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if row.get("course_id") is None or row.get("parent_course_id") is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Lecture detail parent course is missing; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if row.get("mentor_id") != mentor_id:
        _rollback_safely(db, trace_id=trace_id)
        return _access_denied(trace_id)

    # Lấy đúng uploads đã gắn với lecture và kiểm tra scope owner/purpose/course.
    try:
        asset_rows = query_many(
            db,
            FIND_LECTURE_UPLOAD_ASSETS,
            {
                "lecture_id": lecture_id,
                "mentor_id": mentor_id,
                "course_id": row["course_id"],
            },
        )
        assets = _map_assets(asset_rows)
        if assets is None:
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Lecture detail asset mapping failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        lecture = LectureResponse(
            id=row.get("id"),
            course_id=row.get("course_id"),
            title=row.get("name"),
            content=row.get("content"),
            assets=assets,
            order=row.get("sort_order"),
            status=row.get("status"),
        )
    except (SQLAlchemyError, KeyError, TypeError, ValidationError):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Lecture detail mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả response read-only; status gốc được giữ nguyên, gồm cả DRAFT nếu có.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Lecture retrieved.",
        trace_id=trace_id,
        data=lecture.model_dump(mode="json"),
    )
