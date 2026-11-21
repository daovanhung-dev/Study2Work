"""Điều phối auth Admin, aggregate read-only và Notification response API #96."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.admin.api_92_admin_notifications_list.models import AdminNotificationResponse
from app.modules.admin.api_96_admin_notifications_status.models import (
    GetAdminNotificationStatusEnvelope,
)
from app.modules.admin.api_96_admin_notifications_status.query import (
    FIND_ADMIN_NOTIFICATION_STATUS,
)
from app.modules.admin.api_96_admin_notifications_status.validate import (
    parse_admin_notification_status_id,
)
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
MAX_INT64 = 2**63 - 1
ALLOWED_CHANNELS = {"EMAIL", "PUSH"}


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng 404 cho ID sai hoặc notification không có delivery status."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Notification status was not found.",
        trace_id=trace_id,
    )


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi query hoặc ánh xạ aggregate thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Notification status could not be retrieved.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback read transaction sau lỗi mà không che response gốc."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin notification status rollback failed; trace_id=%s", trace_id)


def _map_notification(
    row: Any,
    *,
    notification_id: int,
    trace_id: str,
) -> AdminNotificationResponse | None:
    """Kiểm tra projection và map vào các field Notification hiện có."""

    if not isinstance(row, Mapping):
        return None
    if type(row.get("id")) is not int or row.get("id") != notification_id:
        return None
    if not 1 <= notification_id <= MAX_INT64:
        return None
    channels = row.get("channels")
    if (
        not isinstance(channels, list)
        or not channels
        or any(
            not isinstance(channel, str) or channel not in ALLOWED_CHANNELS for channel in channels
        )
        or len(set(channels)) != len(channels)
    ):
        return None
    try:
        return AdminNotificationResponse.model_validate(row)
    except (TypeError, ValidationError):
        logger.error("Admin notification status projection failed; trace_id=%s", trace_id)
        return None


def get_admin_notification_status(
    *,
    authorization: str | None,
    notification_id_value: object,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN rồi đọc delivery aggregate cho đúng một notification."""

    # Xác thực role trước path parsing và mọi truy cập database.
    authentication = validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Notification status could not be retrieved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication

    # Catalog không có 422 cho endpoint này; malformed int64 dùng 404 như API status #64.
    notification_id = parse_admin_notification_status_id(notification_id_value)
    if notification_id is None:
        return _not_found(trace_id)

    try:
        # Giới hạn aggregate vào notification đích và đọc Notification cùng một snapshot query.
        row = query_one(
            db,
            FIND_ADMIN_NOTIFICATION_STATUS,
            {"notification_id": notification_id},
        )
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin notification status lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Không có delivery row tương ứng cũng đồng nghĩa chưa có delivery-status resource.
    if row is None:
        return _not_found(trace_id)

    notification = _map_notification(
        row,
        notification_id=notification_id,
        trace_id=trace_id,
    )
    if notification is None:
        _rollback_safely(db, trace_id=trace_id)
        return _internal_error(trace_id)

    try:
        envelope = GetAdminNotificationStatusEnvelope.model_validate(
            success_response(
                business_code="DESIGN_RESOURCE_RETRIEVED",
                message="Notification status was retrieved.",
                trace_id=trace_id,
                data=notification.model_dump(mode="json", exclude_none=True),
            )
        )
    except (TypeError, ValidationError):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin notification status envelope failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # GET chỉ đọc; không commit hoặc gọi provider delivery.
    return envelope.model_dump(mode="json", exclude_none=True)
