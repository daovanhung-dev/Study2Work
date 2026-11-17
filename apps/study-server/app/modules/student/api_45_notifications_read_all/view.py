from __future__ import annotations

import logging
from typing import Any

from app.core.responses import error_response, success_response
from app.modules.student._shared.notifications import NotificationsReadSummary
from app.modules.student.api_45_notifications_read_all.query import MARK_ALL_USER_NOTIFICATIONS_READ
from app.utils.auth import validate_current_user_request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def mark_all_notifications_read(*, authorization: str | None, db: Session, trace_id: str) -> dict[str, Any] | JSONResponse:
    auth = validate_current_user_request(authorization, role="STUDENT", trace_id=trace_id)
    if isinstance(auth, JSONResponse):
        return auth
    try:
        result = db.execute(text(MARK_ALL_USER_NOTIFICATIONS_READ), {"user_id": auth[0]})
        count = len(result.fetchall())
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Mark all notifications read failed; trace_id=%s", trace_id)
        return error_response(status_code=500, business_code="DESIGN_INTERNAL_ERROR", message="Notifications could not be updated.", trace_id=trace_id)
    summary = NotificationsReadSummary(updated_count=count)
    return success_response(business_code="DESIGN_RESOURCE_UPDATED", message="Notifications marked as read.", trace_id=trace_id, data=summary.model_dump(mode="json"))
