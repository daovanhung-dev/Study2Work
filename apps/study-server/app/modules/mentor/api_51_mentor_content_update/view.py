"""Điều phối xác thực Mentor, snapshot phiên bản và cập nhật Content API #51."""

from __future__ import annotations

import json
import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.mentor.api_49_mentor_content_list.models import ContentResponse
from app.modules.mentor.api_51_mentor_content_update.models import UpdateContentRequest
from app.modules.mentor.api_51_mentor_content_update.query import (
    ARCHIVE_CONTENT_VERSION,
    LOCK_MENTOR_CONTENT,
    UPDATE_CONTENT,
)
from app.modules.mentor.api_51_mentor_content_update.validate import parse_content_id
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi đọc, ghi snapshot hoặc cập nhật Content thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Content could not be updated.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 cho ID sai định dạng hoặc Content không hoạt động."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Content not found.",
        trace_id=trace_id,
    )


def _access_denied(trace_id: str) -> JSONResponse:
    """Dựng lỗi 403 khi Mentor không sở hữu course chứa Content."""

    return error_response(
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message="Access denied.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction đang mở mà không thay thế response lỗi ban đầu."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Content update rollback failed; trace_id=%s", trace_id)


def _map_updated_content(
    row: Mapping[str, Any],
    *,
    content_id: int,
    current: Mapping[str, Any],
    request: UpdateContentRequest,
) -> ContentResponse | None:
    """Kiểm tra UPDATE/RETURNING projection rồi dựng Content response."""

    if (
        row.get("id") != content_id
        or row.get("course_id") != current.get("course_id")
        or row.get("content_type") != request.content_type
        or row.get("title") != request.title
        or row.get("payload") != request.payload
        or row.get("status") != "PENDING_REVIEW"
        or row.get("parent_id") != current.get("parent_id")
        or row.get("order") != current.get("order")
    ):
        return None

    try:
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
        return None


def update_content(
    *,
    authorization: str | None,
    content_id_value: str,
    content_request: UpdateContentRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Mentor, snapshot Content hiện tại rồi cập nhật revision chờ duyệt."""

    # Xác thực Bearer, numeric subject và role trước mọi truy cập database.
    authentication = validate_current_user_request(
        authorization,
        role="MENTOR",
        trace_id=trace_id,
        internal_error_message="Content could not be updated.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    mentor_id, _roles = authentication

    # Parse path trong view để ID sai format/range ánh xạ về 404 catalog.
    content_id = parse_content_id(content_id_value)
    if content_id is None:
        return _not_found(trace_id)

    # Lock Content cùng Course để serialize version và cố định ownership khi ghi.
    try:
        current = query_one(db, LOCK_MENTOR_CONTENT, {"content_id": content_id})
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content update access lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if current is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    # Từ chối projection lỗi trước khi ghi snapshot để không lưu dữ liệu không xác minh.
    if (
        not isinstance(current, Mapping)
        or current.get("id") != content_id
        or "mentor_id" not in current
        or "course_id" not in current
    ):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content update access projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    owner_id = current.get("mentor_id")
    if owner_id is not None and type(owner_id) is not int:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content update owner projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    # Chỉ Mentor sở hữu trực tiếp course mới được sửa Content.
    if owner_id != mentor_id:
        _rollback_safely(db, trace_id=trace_id)
        return _access_denied(trace_id)

    # Ghi snapshot đầy đủ trạng thái cũ trong cùng transaction với UPDATE.
    try:
        archived_payload = json.dumps(
            current.get("payload"),
            ensure_ascii=False,
            separators=(",", ":"),
        )
        archived = query_one(
            db,
            ARCHIVE_CONTENT_VERSION,
            {
                "content_id": content_id,
                "course_id": current.get("course_id"),
                "content_type": current.get("content_type"),
                "title": current.get("title"),
                "payload": archived_payload,
                "status": current.get("status"),
                "parent_id": current.get("parent_id"),
                "content_order": current.get("order"),
                "archived_by": mentor_id,
            },
        )
    except (SQLAlchemyError, TypeError):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content version snapshot failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if not isinstance(archived, Mapping) or type(archived.get("version_no")) is not int:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content version snapshot returned no version; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Thay ba trường thuộc body và đưa projection hiện tại về hàng chờ review.
    try:
        updated = query_one(
            db,
            UPDATE_CONTENT,
            {
                "content_id": content_id,
                "content_type": content_request.content_type,
                "title": content_request.title,
                "payload": json.dumps(
                    content_request.payload,
                    ensure_ascii=False,
                    separators=(",", ":"),
                ),
            },
        )
    except (SQLAlchemyError, TypeError):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content update query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if not isinstance(updated, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content update returned no row; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    content = _map_updated_content(
        updated,
        content_id=content_id,
        current=current,
        request=content_request,
    )
    if content is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content update mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    response_data = content.model_dump(mode="json", exclude_none=True)

    # Chỉ commit sau khi snapshot và response projection đều hợp lệ.
    try:
        db.commit()
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Content update commit failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả reusable Content cùng business code update của catalog.
    return success_response(
        business_code="DESIGN_RESOURCE_UPDATED",
        message="Content updated.",
        trace_id=trace_id,
        data=response_data,
    )
