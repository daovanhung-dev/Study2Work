"""Điều phối quyền Admin và cập nhật title/content notification API #94."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from datetime import datetime
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import ErrorDetail, error_response, success_response
from app.modules.admin.api_92_admin_notifications_list.models import AdminNotificationResponse
from app.modules.admin.api_94_admin_notifications_update.query import (
    LOCK_ADMIN_NOTIFICATION,
    LOCK_ADMIN_NOTIFICATION_DELIVERIES,
    UPDATE_ADMIN_NOTIFICATION,
)
from app.modules.admin.api_94_admin_notifications_update.validate import (
    validate_admin_notification_update_request,
)
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
ALLOWED_CHANNELS = {"EMAIL", "PUSH"}


def _error(
    *,
    status_code: int,
    business_code: str,
    message: str,
    trace_id: str,
    field_error: ErrorDetail | None = None,
) -> JSONResponse:
    """Dựng catalog error envelope, thêm field error nếu là 422."""

    errors = [field_error] if field_error is not None else []
    return error_response(
        status_code=status_code,
        business_code=business_code,
        message=message,
        trace_id=trace_id,
        errors=errors,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction thất bại mà không che response lỗi gốc."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin notification update rollback failed; trace_id=%s", trace_id)


def _notification_row_matches(row: Any, notification_id: int) -> bool:
    """Kiểm tra projection khóa notification và kiểu timestamp legacy."""

    return (
        isinstance(row, Mapping)
        and type(row.get("id")) is int
        and row.get("id") == notification_id
        and isinstance(row.get("created_at"), datetime)
    )


def _delivery_projection(rows: Any, notification_id: int) -> tuple[list[str], bool] | None:
    """Kiểm tra channel/status rows, trả channel list và cờ tất cả QUEUED."""

    if not isinstance(rows, list):
        return None
    channels: list[str] = []
    all_queued = True
    for row in rows:
        if (
            not isinstance(row, Mapping)
            or type(row.get("notification_id")) is not int
            or row.get("notification_id") != notification_id
            or not isinstance(row.get("channel"), str)
            or row.get("channel") not in ALLOWED_CHANNELS
            or not isinstance(row.get("status"), str)
            or row.get("status") not in {"QUEUED", "SENT", "FAILED"}
        ):
            return None
        channels.append(row["channel"])
        all_queued = all_queued and row["status"] == "QUEUED"
    if len(set(channels)) != len(channels):
        return None
    return channels, all_queued


def _not_found(trace_id: str) -> JSONResponse:
    """Trả lỗi catalog khi không có notification đích."""

    return _error(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Notification not found.",
        trace_id=trace_id,
    )


def _invalid_state(trace_id: str) -> JSONResponse:
    """Trả lỗi catalog khi chưa có delivery hoặc dispatch đã bắt đầu."""

    return _error(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Notification is not editable in its current delivery state.",
        trace_id=trace_id,
        field_error=ErrorDetail(
            field="notification_id",
            code="NOTIFICATION_NOT_EDITABLE",
            message="Chỉ notification có delivery QUEUED mới được cập nhật.",
        ),
    )


def _internal_error(trace_id: str) -> JSONResponse:
    """Trả lỗi 500 an toàn khi query, mapping hoặc commit thất bại."""

    return _error(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Notification could not be updated.",
        trace_id=trace_id,
    )


def update_admin_notification(
    *,
    authorization: str | None,
    notification_id_value: object,
    raw_body: bytes,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN, khóa Notification và cập nhật hai trường text legacy."""

    # Kiểm tra role qua guard dùng chung trước khi parse input hoặc truy vấn dữ liệu.
    authentication = validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Notification could not be updated.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication

    # Validate path/body sau auth để lỗi input không làm lộ thứ tự lookup tài nguyên.
    request = validate_admin_notification_update_request(
        notification_id_value,
        raw_body,
        trace_id=trace_id,
    )
    if isinstance(request, JSONResponse):
        return request
    notification_id, update_data = request

    try:
        # Khóa row cha trước để giữ ổn định notification trong toàn bộ transaction.
        locked_notification = query_one(
            db,
            LOCK_ADMIN_NOTIFICATION,
            {"notification_id": notification_id},
        )
        if locked_notification is None:
            return _not_found(trace_id)
        if not _notification_row_matches(locked_notification, notification_id):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin notification lock projection failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)

        # Khóa delivery rows theo thứ tự channel trước khi quyết định có thể sửa hay không.
        delivery_rows = query_many(
            db,
            LOCK_ADMIN_NOTIFICATION_DELIVERIES,
            {"notification_id": notification_id},
        )
        delivery_projection = _delivery_projection(delivery_rows, notification_id)
        if delivery_projection is None:
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin notification delivery projection failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        channels, all_queued = delivery_projection
        if not channels or not all_queued:
            _rollback_safely(db, trace_id=trace_id)
            return _invalid_state(trace_id)

        # Chỉ cập nhật hai cột text; recipient, delivery và created_at được giữ nguyên.
        updated_notification = query_one(
            db,
            UPDATE_ADMIN_NOTIFICATION,
            {
                "notification_id": notification_id,
                "title": update_data.title,
                "content": update_data.content,
            },
        )
        if (
            not isinstance(updated_notification, Mapping)
            or type(updated_notification.get("id")) is not int
            or updated_notification.get("id") != notification_id
            or updated_notification.get("title") != update_data.title
            or updated_notification.get("content") != update_data.content
            or updated_notification.get("created_at") != locked_notification.get("created_at")
        ):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin notification update projection failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)

        try:
            # Kiểm tra Notification response đầy đủ trước khi commit transaction.
            response_data = AdminNotificationResponse(
                id=notification_id,
                title=update_data.title,
                content=update_data.content,
                channels=channels,
                status="QUEUED",
                created_at=updated_notification["created_at"],
            )
        except (TypeError, ValidationError):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin notification response mapping failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)

        data = response_data.model_dump(mode="json", exclude_none=True)
        result = success_response(
            business_code="DESIGN_RESOURCE_UPDATED",
            message="Notification updated.",
            trace_id=trace_id,
            data=data,
        )
        # Chốt thay đổi sau khi response đã được map và kiểm tra thành công.
        db.commit()
        return result
    except SQLAlchemyError:
        # Hủy thay đổi một phần nếu query hoặc commit gặp lỗi database.
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin notification update database operation failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
