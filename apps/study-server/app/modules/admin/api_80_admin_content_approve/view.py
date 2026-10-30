"""Điều phối quyền Admin, status transition/audit và response API #80."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import execute_query, query_one
from app.core.responses import error_response, success_response
from app.modules.admin.api_80_admin_content_approve.query import (
    APPROVE_ADMIN_CONTENT,
    INSERT_ADMIN_CONTENT_REVIEW_AUDIT,
    LOCK_ADMIN_CONTENT_FOR_APPROVAL,
)
from app.modules.admin.api_80_admin_content_approve.validate import (
    validate_admin_content_approval_request,
)
from app.modules.mentor.api_49_mentor_content_list.models import ContentResponse
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn cho update, audit, projection hoặc commit."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Content approval could not be completed.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 catalog khi Content thiếu hoặc đã soft-delete."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Content not found.",
        trace_id=trace_id,
    )


def _invalid_state(trace_id: str) -> JSONResponse:
    """Dựng lỗi 422 khi Content hiện tại không ở trạng thái chờ duyệt."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Content is not pending review.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction lỗi mà không làm lộ exception nội bộ."""

    try:
        # Dọn transaction chưa hoàn tất trước khi request dependency đóng Session.
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin Content approval rollback failed; trace_id=%s", trace_id)


def _map_approved_content(
    row: Mapping[str, Any],
    *,
    requested_content_id: int,
) -> ContentResponse | None:
    """Kiểm tra update projection và ánh xạ đúng tám field reusable Content."""

    required_fields = {
        "id",
        "course_id",
        "content_type",
        "title",
        "payload",
        "status",
        "parent_id",
        "order",
    }
    if not required_fields.issubset(row.keys()):
        return None
    if type(row.get("id")) is not int or row.get("id") != requested_content_id:
        return None
    if row.get("status") != "APPROVED":
        return None

    # Payload phải là object JSON theo legacy contents candidate.
    payload = row.get("payload")
    if not isinstance(payload, Mapping):
        return None

    try:
        # Reuse API #49 model để giới hạn response đúng Content contract.
        return ContentResponse(
            id=row.get("id"),
            course_id=row.get("course_id"),
            content_type=row.get("content_type"),
            title=row.get("title"),
            payload=dict(payload),
            status=row.get("status"),
            parent_id=row.get("parent_id"),
            order=row.get("order"),
        )
    except (TypeError, ValidationError):
        return None


# API #80 admin_content_approve
def approve_admin_content(
    *,
    authorization: str | None,
    content_id_value: str,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN, chuyển Content pending sang APPROVED và ghi audit atomic."""

    # Xác thực principal và path trước khi đọc hoặc ghi Content.
    validation = validate_admin_content_approval_request(
        authorization,
        content_id_value,
        trace_id=trace_id,
    )
    if isinstance(validation, JSONResponse):
        return validation
    content_id, actor_user_id = validation

    # Khóa row active để kiểm tra eligibility và cập nhật trên cùng trạng thái.
    try:
        current = query_one(
            db,
            LOCK_ADMIN_CONTENT_FOR_APPROVAL,
            {"content_id": content_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin Content approval lock failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if current is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if (
        not isinstance(current, Mapping)
        or type(current.get("id")) is not int
        or current.get("id") != content_id
        or not isinstance(current.get("status"), str)
    ):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin Content approval lock projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if current.get("status") != "PENDING_REVIEW":
        _rollback_safely(db, trace_id=trace_id)
        return _invalid_state(trace_id)

    # Chỉ đổi trạng thái của row vẫn active/pending; lấy Content projection bằng RETURNING.
    try:
        updated = query_one(
            db,
            APPROVE_ADMIN_CONTENT,
            {"content_id": content_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin Content approval update failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if updated is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(updated, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin Content approval update row is malformed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Xác thực response trước khi append audit hoặc commit thay đổi.
    content = _map_approved_content(updated, requested_content_id=content_id)
    if content is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin Content approval projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Ghi actor và trạng thái cũ/mới cùng transaction với status update.
    try:
        execute_query(
            db,
            INSERT_ADMIN_CONTENT_REVIEW_AUDIT,
            {
                "content_id": content_id,
                "actor_user_id": actor_user_id,
                "previous_status": "PENDING_REVIEW",
                "new_status": "APPROVED",
                "reason": None,
            },
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin Content approval audit insert failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Commit chỉ khi status update, audit row và response mapping đều hợp lệ.
    try:
        db.commit()
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin Content approval commit failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_UPDATED",
        message="Content approved.",
        trace_id=trace_id,
        data=content.model_dump(mode="json"),
    )
