"""Điều phối quyền Admin, truy vấn read-only và ánh xạ Page Notification API #92."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from datetime import datetime
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.admin.api_92_admin_notifications_list.models import (
    AdminNotificationResponse,
    AdminNotificationsPage,
    AdminNotificationsQuery,
    GetAdminNotificationsEnvelope,
)
from app.modules.admin.api_92_admin_notifications_list.query import (
    COUNT_ADMIN_NOTIFICATIONS,
    LIST_ADMIN_NOTIFICATIONS,
)
from app.modules.admin.api_92_admin_notifications_list.validate import (
    validate_admin_notifications_request,
)
from app.modules.guest._shared.course_catalog.models import Pagination
from pydantic import ValidationError
from sqlalchemy.exc import DBAPIError, OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
DEFAULT_PAGE_SIZE = 20
MAX_INT64 = 2**63 - 1
MAX_INT32 = 2**31 - 1
ALLOWED_CHANNELS = {"EMAIL", "PUSH"}
ALLOWED_DELIVERY_STATUSES = {"FAILED", "QUEUED", "SENT"}


def _is_database_unavailable(exc: SQLAlchemyError) -> bool:
    """Nhận diện lỗi kết nối database để dùng business code dependency 503."""

    return isinstance(exc, OperationalError) or (
        isinstance(exc, DBAPIError) and bool(exc.connection_invalidated)
    )


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi query hoặc Notification projection thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Notifications could not be retrieved.",
        trace_id=trace_id,
    )


def _dependency_unavailable(trace_id: str) -> JSONResponse:
    """Dựng lỗi 503 khi kết nối database không khả dụng."""

    return error_response(
        status_code=503,
        business_code="DESIGN_DEPENDENCY_UNAVAILABLE",
        message="Notifications are temporarily unavailable.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback read transaction sau lỗi mà không che phản hồi HTTP gốc."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin notification list rollback failed; trace_id=%s", trace_id)


def _query_error_response(exc: SQLAlchemyError, trace_id: str) -> JSONResponse:
    """Ghi log lỗi DB theo trace và phân loại unavailable 503 hoặc internal 500."""

    logger.error("Admin notification list query failed; trace_id=%s", trace_id)
    if _is_database_unavailable(exc):
        return _dependency_unavailable(trace_id)
    return _internal_error(trace_id)


def _query_parameters(query: AdminNotificationsQuery) -> dict[str, Any]:
    """Tạo bindings exact-match dùng chung cho count và page query."""

    return {"status": query.status, "channel": query.channel}


def _normalize_count_row(count_row: Any, *, trace_id: str) -> int | None:
    """Kiểm tra COUNT projection và miền int64 của PageMeta.total."""

    if not isinstance(count_row, Mapping):
        return None
    total = count_row.get("total")
    if type(total) is not int or not 0 <= total <= MAX_INT64:
        logger.error("Admin notification count mapping failed; trace_id=%s", trace_id)
        return None
    return total


def _map_notification_row(row: Mapping[str, Any]) -> AdminNotificationResponse | None:
    """Map một notification row và channel/status aggregate theo fallback API #63/#64."""

    notification_id = row.get("id")
    title = row.get("title")
    content = row.get("content")
    channels = row.get("channels")
    status = row.get("status")
    created_at = row.get("created_at")
    if (
        type(notification_id) is not int
        or not 1 <= notification_id <= MAX_INT64
        or not isinstance(title, str)
        or not isinstance(content, str)
        or not isinstance(channels, list)
        or not channels
        or any(
            not isinstance(channel, str) or channel not in ALLOWED_CHANNELS for channel in channels
        )
        or len(set(channels)) != len(channels)
        or not isinstance(status, str)
        or status not in ALLOWED_DELIVERY_STATUSES
        or not isinstance(created_at, datetime)
    ):
        return None

    try:
        return AdminNotificationResponse(
            id=notification_id,
            title=title,
            content=content,
            channels=channels,
            status=status,
            created_at=created_at,
        )
    except (TypeError, ValidationError):
        return None


def _map_notification_page(
    rows: Any,
    *,
    total: int,
    query: AdminNotificationsQuery,
    trace_id: str,
) -> AdminNotificationsPage | None:
    """Map Page items và kiểm tra giới hạn total_pages theo schema reusable."""

    if not isinstance(rows, list) or len(rows) > DEFAULT_PAGE_SIZE:
        return None

    # Chỉ đưa các projection hợp lệ vào response, không trả recipient hoặc sender ID.
    items: list[AdminNotificationResponse] = []
    for row in rows:
        if not isinstance(row, Mapping):
            return None
        item = _map_notification_row(row)
        if item is None:
            logger.error("Admin notification row mapping failed; trace_id=%s", trace_id)
            return None
        items.append(item)

    total_pages = (total + DEFAULT_PAGE_SIZE - 1) // DEFAULT_PAGE_SIZE if total else 0
    if total_pages > MAX_INT32:
        logger.error("Admin notification total pages exceed int32; trace_id=%s", trace_id)
        return None
    try:
        return AdminNotificationsPage(
            items=items,
            pagination=Pagination(
                page=query.page,
                size=DEFAULT_PAGE_SIZE,
                total=total,
                total_pages=total_pages,
            ),
        )
    except (TypeError, ValidationError):
        return None


# API #92 — Danh sách notification Admin.
def get_admin_notifications(
    *,
    authorization: str | None,
    status_value: str | None,
    channel_value: str | None,
    page_value: str | None,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN rồi trả trang notification có delivery theo fallback local."""

    # Kiểm tra quyền trước khi parse page hoặc truy cập database.
    validated_query = validate_admin_notifications_request(
        authorization,
        status_value=status_value,
        channel_value=channel_value,
        page_value=page_value,
        trace_id=trace_id,
    )
    if isinstance(validated_query, JSONResponse):
        return validated_query

    # Dùng cùng filter cho count/page và lấy hai mươi notification mới nhất ổn định.
    base_parameters = _query_parameters(validated_query)
    page_parameters = {
        **base_parameters,
        "limit": DEFAULT_PAGE_SIZE,
        "offset": (validated_query.page - 1) * DEFAULT_PAGE_SIZE,
    }
    try:
        count_row = query_one(db, COUNT_ADMIN_NOTIFICATIONS, base_parameters)
        rows = query_many(db, LIST_ADMIN_NOTIFICATIONS, page_parameters)
    except SQLAlchemyError as exc:
        # Hoàn tác transaction chỉ đọc rồi ánh xạ connection error theo catalog.
        _rollback_safely(db, trace_id=trace_id)
        return _query_error_response(exc, trace_id)

    # Từ chối count/page sai cấu trúc để không trả metadata hoặc item thiếu tin cậy.
    total = _normalize_count_row(count_row, trace_id=trace_id)
    if total is None:
        _rollback_safely(db, trace_id=trace_id)
        return _internal_error(trace_id)
    page = _map_notification_page(
        rows,
        total=total,
        query=validated_query,
        trace_id=trace_id,
    )
    if page is None:
        _rollback_safely(db, trace_id=trace_id)
        return _internal_error(trace_id)

    # Trả Page rỗng hợp lệ khi không có notification hoặc page vượt trang cuối.
    try:
        envelope = GetAdminNotificationsEnvelope.model_validate(
            success_response(
                business_code="DESIGN_RESOURCE_RETRIEVED",
                message="Notifications retrieved." if page.items else "No notifications found.",
                trace_id=trace_id,
                data=page.model_dump(mode="json", exclude_none=True),
            )
        )
    except ValidationError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin notification response mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # GET chỉ đọc; không commit transaction hoặc gọi notification provider.
    return envelope.model_dump(mode="json", exclude_none=True)
