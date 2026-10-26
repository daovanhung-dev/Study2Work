"""Điều phối quyền course, asset resolution và transaction tạo lecture API #47."""

from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.mentor.api_47_mentor_lectures_create.models import (
    CreateLectureRequest,
    LectureResponse,
)
from app.modules.mentor.api_47_mentor_lectures_create.query import (
    FIND_LECTURE_ASSETS,
    FIND_LECTURE_COURSE,
    INSERT_LECTURE,
    INSERT_LECTURE_ASSET_LINKS,
)
from app.modules.mentor.api_47_mentor_lectures_create.validate import (
    validate_asset_refs,
    validate_lecture_course_id,
)
from app.modules.student.api_34_uploads.models import UploadAssetResponse
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi query hoặc transaction API #47 thất bại."""

    # Không trả chi tiết DB hoặc row mapping nội bộ về client.
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Lecture could not be created.",
        trace_id=trace_id,
    )


def _course_not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 khi course ID không tồn tại."""

    # Dùng business code 404 đã khai báo trong catalog API #47.
    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Course not found.",
        trace_id=trace_id,
    )


def _assets_not_found(trace_id: str) -> JSONResponse:
    """Dựng 404 chung cho asset thiếu hoặc nằm ngoài scope được phép."""

    # Không tiết lộ liệu UploadAsset ngoài scope có tồn tại hay không.
    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Requested assets were not found.",
        trace_id=trace_id,
    )


def _access_denied(trace_id: str) -> JSONResponse:
    """Dựng lỗi 403 khi Mentor không trực tiếp sở hữu course."""

    # Giữ mapping authorization theo catalog API #47.
    return error_response(
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message="Access denied.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction và ghi trace nếu thao tác rollback của SQLAlchemy lỗi."""

    try:
        # Dọn transaction đang mở trước khi trả lỗi sớm hoặc lỗi hệ thống.
        db.rollback()
    except SQLAlchemyError:
        logger.error("Lecture transaction rollback failed; trace_id=%s", trace_id)


def _resolve_assets(
    db: Session,
    *,
    asset_ids: list[int],
    mentor_id: int,
    course_id: int,
) -> list[UploadAssetResponse] | None:
    """Đọc UploadAsset cùng Mentor/purpose/course và khôi phục thứ tự ID đầu vào."""

    if not asset_ids:
        # Mảng rỗng là hợp lệ và không cần chạy query uploads.
        return []

    # Chỉ resolve metadata thỏa owner, LECTURE purpose và course path.
    rows = query_many(
        db,
        FIND_LECTURE_ASSETS,
        {
            "asset_ids": asset_ids,
            "mentor_id": mentor_id,
            "course_id": course_id,
        },
    )
    if len(rows) != len(asset_ids):
        return None

    # Validate row shape trước khi tạo mapping ID sang UploadAsset response.
    assets_by_id = {
        asset_id: UploadAssetResponse.model_validate(row)
        for row in rows
        if (asset_id := row.get("id")) is not None
    }
    if len(assets_by_id) != len(asset_ids) or set(assets_by_id) != set(asset_ids):
        return None

    # Không dựa vào thứ tự SQL; API trả assets theo thứ tự string array đầu vào.
    return [assets_by_id[asset_id] for asset_id in asset_ids]


# API #47 mentor_lectures_create
def create_lecture(
    *,
    authorization: str | None,
    course_id: int,
    lecture_request: CreateLectureRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Mentor, resolve asset scope, tạo lecture PUBLISHED và trả Lecture envelope."""

    # Xác thực Bearer, numeric subject và role Mentor trước mọi DB access.
    authentication = validate_current_user_request(
        authorization,
        role="MENTOR",
        trace_id=trace_id,
        internal_error_message="Lecture could not be created.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    mentor_id, _roles = authentication

    # Giới hạn path ID theo signed int64 trước khi bind vào query.
    path_error = validate_lecture_course_id(course_id, trace_id=trace_id)
    if path_error is not None:
        return path_error

    # Parse ordered asset IDs và chặn JSON sai/ID lặp trước khi mở transaction.
    asset_ids = validate_asset_refs(lecture_request.asset_refs, trace_id=trace_id)
    if isinstance(asset_ids, JSONResponse):
        return asset_ids

    # Đọc course row để phân biệt course không tồn tại với course không thuộc Mentor.
    try:
        course = query_one(db, FIND_LECTURE_COURSE, {"course_id": course_id})
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Lecture course lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if course is None:
        _rollback_safely(db, trace_id=trace_id)
        return _course_not_found(trace_id)
    if course.get("mentor_id") != mentor_id:
        _rollback_safely(db, trace_id=trace_id)
        return _access_denied(trace_id)

    # Resolve metadata; asset ID không đủ điều kiện trả 404 chung theo quyết định.
    try:
        assets = _resolve_assets(
            db,
            asset_ids=asset_ids,
            mentor_id=mentor_id,
            course_id=course_id,
        )
    except (SQLAlchemyError, KeyError, TypeError, ValidationError):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Lecture asset lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if assets is None:
        _rollback_safely(db, trace_id=trace_id)
        return _assets_not_found(trace_id)

    # Insert lesson sau khi quyền và toàn bộ asset references đã đạt.
    try:
        row = query_one(
            db,
            INSERT_LECTURE,
            {
                "course_id": course_id,
                "title": lecture_request.title,
                "content": str(lecture_request.content),
                "order": lecture_request.order,
            },
        )
        if row is None or row.get("status") != "PUBLISHED":
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Lecture insert returned an invalid row; trace_id=%s", trace_id)
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
        response_data = lecture.model_dump(mode="json")
        if asset_ids:
            # Gắn các UploadAsset đã resolve vào lecture theo đúng thứ tự request.
            linked_rows = query_many(
                db,
                INSERT_LECTURE_ASSET_LINKS,
                {"lecture_id": row.get("id"), "asset_ids": asset_ids},
            )
            linked_asset_ids = [linked_row.get("upload_id") for linked_row in linked_rows]
            if len(linked_asset_ids) != len(asset_ids) or set(linked_asset_ids) != set(asset_ids):
                _rollback_safely(db, trace_id=trace_id)
                logger.error("Lecture asset links were incomplete; trace_id=%s", trace_id)
                return _internal_error(trace_id)
        db.commit()
    except (SQLAlchemyError, KeyError, TypeError, ValidationError):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Lecture transaction failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả lecture đã commit cùng metadata assets theo thứ tự yêu cầu.
    return success_response(
        business_code="DESIGN_RESOURCE_CREATED",
        message="Lecture created.",
        trace_id=trace_id,
        data=response_data,
    )
