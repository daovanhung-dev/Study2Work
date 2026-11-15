from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.guest.api_38_users_me_achievements.models import Achievement, AchievementPage, Pagination
from app.modules.guest.api_38_users_me_achievements.query import COUNT_ACHIEVEMENTS, LIST_ACHIEVEMENTS
from app.modules.guest.api_38_users_me_achievements.validate import validate_achievements_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def get_achievements(*, authorization: str | None, course_id_raw: str | None, db: Session, trace_id: str) -> dict[str, Any] | JSONResponse:
    validated = validate_achievements_request(authorization, course_id_raw, trace_id=trace_id)
    if isinstance(validated, JSONResponse):
        return validated
    user_id, course_id = validated
    try:
        params = {"user_id": user_id, "course_id": course_id}
        count_row = query_one(db, COUNT_ACHIEVEMENTS, params)
        total = int((count_row or {}).get("total", 0))
        rows = query_many(db, LIST_ACHIEVEMENTS, params)
        items = [Achievement.model_validate(row) for row in rows]
        page = AchievementPage(items=items, pagination=Pagination(page=1, size=max(len(items), 1), total=total, total_pages=1 if total else 0))
    except (SQLAlchemyError, ValidationError, TypeError):
        db.rollback()
        logger.exception("Achievement query failed; trace_id=%s", trace_id)
        return error_response(status_code=500, business_code="DESIGN_INTERNAL_ERROR", message="Achievements could not be retrieved.", trace_id=trace_id)
    return success_response(business_code="DESIGN_RESOURCE_RETRIEVED", message="Achievements retrieved.", trace_id=trace_id, data=page.model_dump(mode="json"))
