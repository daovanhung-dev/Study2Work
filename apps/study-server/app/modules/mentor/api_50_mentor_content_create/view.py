"""Điều phối xác thực Mentor, kiểm tra course và transaction tạo Content API #50."""

from __future__ import annotations

import json
import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.mentor.api_49_mentor_content_list.models import ContentResponse
from app.modules.mentor.api_50_mentor_content_create.models import CreateContentRequest
from app.modules.mentor.api_50_mentor_content_create.query import (
    INSERT_CONTENT,
    LOCK_MENTOR_COURSE,
    NEXT_ROOT_CONTENT_ORDER,
)
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
INT32_MAX = 2**31 - 1


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi query, insert hoặc ánh xạ Content thất bại."""

    # Chỉ trả thông tin lỗi chung, không đưa SQL hoặc chi tiết DB ra response.
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Content could not be created.",
        trace_id=trace_id,
    )


def _access_denied(trace_id: str) -> JSONResponse:
    """Dựng lỗi 403 chung cho course vắng mặt hoặc không thuộc quyền Mentor."""

    # Giữ course vắng và course ngoài quyền trong một nhánh để không lộ tồn tại.
    return error_response(
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message="Access denied.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction đang mở mà không thay thế response lỗi ban đầu."""

    try:
        # Dọn transaction trước khi dependency request đóng Session.
        db.rollback()
    except SQLAlchemyError:
        logger.error("Content create rollback failed; trace_id=%s", trace_id)


def _map_inserted_content(
    row: Mapping[str, Any],
    *,
    request: CreateContentRequest,
    content_order: int,
) -> ContentResponse | None:
    """Kiểm tra projection INSERT/RETURNING rồi dựng model Content dùng chung với API #49."""

    # Đảm bảo DB đã trả đúng course, request fields, trạng thái và root order vừa cấp.
    if (
        row.get("course_id") != request.course_id
        or row.get("content_type") != request.content_type
        or row.get("title") != request.title
        or row.get("payload") != request.payload
        or row.get("status") != "PENDING_REVIEW"
        or row.get("parent_id") is not None
        or row.get("order") != content_order
    ):
        return None

    try:
        # Dùng cùng Content projection để create response khớp cây đọc của API #49.
        return ContentResponse(
            id=row.get("id"),
            course_id=row.get("course_id"),
            content_type=row.get("content_type"),
            title=row.get("title"),
            payload=row.get("payload"),
            status=row.get("status"),
            parent_id=row.get("parent_id"),
            order=row.get("order"),
        )
    except (TypeError, ValidationError):
        # Thiếu ID hoặc sai kiểu DB row là lỗi integrity, không phải client validation.
        return None


# API #50 mentor_content_create
def create_content(
    *,
    authorization: str | None,
    content_request: CreateContentRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Mentor, tạo Content root ở trạng thái chờ duyệt và trả envelope 201."""

    # Xác thực Bearer, numeric subject và MENTOR role trước mọi truy cập database.
    authentication = validate_current_user_request(
        authorization,
        role="MENTOR",
        trace_id=trace_id,
        internal_error_message="Content could not be created.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    mentor_id, _roles = authentication

    # Lock course row để POST đồng thời cùng course không cấp trùng root order.
    try:
        course = query_one(db, LOCK_MENTOR_COURSE, {"course_id": content_request.course_id})
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content course lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if course is None:
        _rollback_safely(db, trace_id=trace_id)
        return _access_denied(trace_id)
    if (
        not isinstance(course, Mapping)
        or course.get("id") != content_request.course_id
        or "mentor_id" not in course
    ):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content course row has invalid shape; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    course_owner_id = course.get("mentor_id")
    if course_owner_id is not None and type(course_owner_id) is not int:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content course owner projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if course_owner_id != mentor_id:
        _rollback_safely(db, trace_id=trace_id)
        return _access_denied(trace_id)

    # Lấy order kế tiếp trong các root còn hoạt động; node đầu tiên bắt đầu từ 0.
    try:
        order_row = query_one(
            db,
            NEXT_ROOT_CONTENT_ORDER,
            {"course_id": content_request.course_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content order lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if not isinstance(order_row, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content order projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    content_order = order_row.get("next_order")
    if type(content_order) is not int or not 0 <= content_order <= INT32_MAX:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content order is outside int32 range; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Serialize payload explicitly for PostgreSQL JSONB text binding.
    try:
        payload_json = json.dumps(
            content_request.payload,
            ensure_ascii=False,
            separators=(",", ":"),
        )
        row = query_one(
            db,
            INSERT_CONTENT,
            {
                "course_id": content_request.course_id,
                "content_type": content_request.content_type,
                "title": content_request.title,
                "payload": payload_json,
                "status": "PENDING_REVIEW",
                "content_order": content_order,
            },
        )
    except (SQLAlchemyError, TypeError):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content insert failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if not isinstance(row, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content insert returned no row; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Xác minh row đầy đủ trước commit để không lưu thành công một response lỗi.
    content = _map_inserted_content(
        row,
        request=content_request,
        content_order=content_order,
    )
    if content is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content insert mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    response_data = content.model_dump(mode="json", exclude_none=True)

    # Chỉ commit sau khi insert projection đã khớp Content response contract.
    try:
        db.commit()
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content create commit failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả Content đã commit cùng business code create của catalog.
    return success_response(
        business_code="DESIGN_RESOURCE_CREATED",
        message="Content created.",
        trace_id=trace_id,
        data=response_data,
    )
