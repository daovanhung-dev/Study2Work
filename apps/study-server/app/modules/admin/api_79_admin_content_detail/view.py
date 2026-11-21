"""Điều phối quyền Admin, đọc Content hiện hành và dựng response API #79."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.admin.api_79_admin_content_detail.query import FIND_ADMIN_CONTENT
from app.modules.admin.api_79_admin_content_detail.validate import (
    parse_admin_content_id,
    validate_admin_request,
)
from app.modules.mentor.api_49_mentor_content_list.models import ContentResponse
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn cho query hoặc ánh xạ Content API #79."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Content could not be retrieved.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi catalog 404 cho path ID sai hoặc Content không hoạt động."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Content not found.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction đọc lỗi mà không làm lộ exception nội bộ."""

    try:
        # Dọn transaction bị lỗi trước khi request dependency đóng Session.
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin Content detail rollback failed; trace_id=%s", trace_id)


def _map_content(
    row: Mapping[str, Any],
    *,
    requested_content_id: int,
) -> ContentResponse | None:
    """Kiểm tra projection và ánh xạ đúng tám field reusable Content."""

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
    if not required_fields.issubset(row.keys()) or row.get("id") != requested_content_id:
        return None

    # Payload phải là JSON object theo legacy contents candidate, không phải scalar/list.
    payload = row.get("payload")
    if not isinstance(payload, Mapping):
        return None

    try:
        # Reuse API #49 model để giữ cùng field types và response allowlist.
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


# API #79 admin_content_detail
def get_admin_content(
    *,
    authorization: str | None,
    content_id_value: str,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN, đọc Content active theo signed-int64 ID và trả object catalog."""

    # Xác thực Bearer/JWT và role Admin trước khi parse path hoặc truy cập database.
    authentication = validate_admin_request(authorization, trace_id=trace_id)
    if isinstance(authentication, JSONResponse):
        return authentication

    # Parse raw path để sai format/range dùng đúng error set catalog, không trả 422.
    content_id = parse_admin_content_id(content_id_value)
    if content_id is None:
        return _not_found(trace_id)

    # Đọc một projection Content được phép trả về bằng bind parameter.
    try:
        row = query_one(db, FIND_ADMIN_CONTENT, {"content_id": content_id})
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin Content detail query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Content không có hoặc đã soft-delete được xem là không tồn tại.
    if row is None:
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(row, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin Content detail row has invalid shape; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Kiểm tra field types và ID để không trả nhầm row hoặc payload sai schema.
    content = _map_content(row, requested_content_id=content_id)
    if content is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin Content detail mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả Content hiện hành; version/author chưa có output contract và không được suy đoán.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Content retrieved.",
        trace_id=trace_id,
        data=content.model_dump(mode="json"),
    )
