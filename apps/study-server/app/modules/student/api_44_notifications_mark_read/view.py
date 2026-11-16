from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.student._shared.notifications import NotificationPagination, StudentNotification, StudentNotificationPage
from app.modules.student.api_44_notifications_mark_read.query import FIND_ADDRESSABLE_NOTIFICATION, GET_READ_NOTIFICATION, UPSERT_NOTIFICATION_READ
from app.modules.student.api_44_notifications_mark_read.validate import validate_mark_notification_read
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def mark_notification_read(*, authorization: str | None, notification_id_raw: str, db: Session, trace_id: str) -> dict[str, Any] | JSONResponse:
    validated = validate_mark_notification_read(authorization, notification_id_raw, trace_id=trace_id)
    if isinstance(validated, JSONResponse):
        return validated
    user_id, notification_id = validated
    try:
        visible = query_one(db, FIND_ADDRESSABLE_NOTIFICATION, {"notification_id": notification_id, "user_id": user_id})
        if visible is None:
            return error_response(status_code=404, business_code="DESIGN_RESOURCE_NOT_FOUND", message="Notification not found.", trace_id=trace_id)
        query_one(db, UPSERT_NOTIFICATION_READ, {"notification_id": notification_id, "user_id": user_id})
        row = query_one(db, GET_READ_NOTIFICATION, {"notification_id": notification_id, "user_id": user_id})
        if row is None:
            db.rollback()
            return error_response(status_code=500, business_code="DESIGN_INTERNAL_ERROR", message="Notification could not be updated.", trace_id=trace_id)
        item = StudentNotification.model_validate(row)
        db.commit()
        page = StudentNotificationPage(items=[item], pagination=NotificationPagination(page=1, size=1, total=1, total_pages=1))
    except (SQLAlchemyError, ValidationError, TypeError):
        db.rollback()
        logger.exception("Mark notification read failed; trace_id=%s", trace_id)
        return error_response(status_code=500, business_code="DESIGN_INTERNAL_ERROR", message="Notification could not be updated.", trace_id=trace_id)
    return success_response(business_code="DESIGN_RESOURCE_UPDATED", message="Notification marked as read.", trace_id=trace_id, data=page.model_dump(mode="json"))
