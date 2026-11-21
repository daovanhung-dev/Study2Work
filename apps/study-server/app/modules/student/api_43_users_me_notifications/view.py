from __future__ import annotations

import logging
import math
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.student._shared.notifications import NotificationPagination, StudentNotification, StudentNotificationPage
from app.modules.student.api_43_users_me_notifications.query import COUNT_USER_NOTIFICATIONS, LIST_USER_NOTIFICATIONS
from app.modules.student.api_43_users_me_notifications.validate import validate_notification_list
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
PAGE_SIZE = 20


def get_notifications(*, authorization: str | None, unread_only: bool, page_raw: str | None, db: Session, trace_id: str) -> dict[str, Any] | JSONResponse:
    validated = validate_notification_list(authorization, page_raw, trace_id=trace_id)
    if isinstance(validated, JSONResponse):
        return validated
    user_id, page_number = validated
    try:
        params = {"user_id": user_id, "unread_only": unread_only}
        count_row = query_one(db, COUNT_USER_NOTIFICATIONS, params)
        total = int((count_row or {}).get("total", 0))
        rows = query_many(db, LIST_USER_NOTIFICATIONS, {**params, "limit": PAGE_SIZE, "offset": (page_number - 1) * PAGE_SIZE})
        result = StudentNotificationPage(items=[StudentNotification.model_validate(row) for row in rows], pagination=NotificationPagination(page=page_number, size=PAGE_SIZE, total=total, total_pages=math.ceil(total / PAGE_SIZE) if total else 0))
    except (SQLAlchemyError, ValidationError, TypeError):
        db.rollback()
        logger.exception("Notification list failed; trace_id=%s", trace_id)
        return error_response(status_code=500, business_code="DESIGN_INTERNAL_ERROR", message="Notifications could not be retrieved.", trace_id=trace_id)
    return success_response(business_code="DESIGN_RESOURCE_RETRIEVED", message="Notifications retrieved.", trace_id=trace_id, data=result.model_dump(mode="json"))
