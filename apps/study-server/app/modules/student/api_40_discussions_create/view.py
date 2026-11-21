from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.student._shared.discussions import Discussion, DiscussionAuthor, DiscussionPage, Pagination
from app.modules.student.api_40_discussions_create.models import CreateDiscussionRequest
from app.modules.student.api_40_discussions_create.query import FIND_ACTIVE_ENROLLMENT, FIND_DISCUSSION_AUTHOR, INSERT_ROOT_DISCUSSION
from app.modules.student.api_40_discussions_create.validate import validate_create_discussion
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def create_discussion(*, authorization: str | None, payload: CreateDiscussionRequest, db: Session, trace_id: str) -> dict[str, Any] | JSONResponse:
    validated = validate_create_discussion(authorization, payload, trace_id=trace_id)
    if isinstance(validated, JSONResponse):
        return validated
    user_id, body = validated
    try:
        if query_one(db, FIND_ACTIVE_ENROLLMENT, {"user_id": user_id, "course_id": body.course_id}) is None:
            return error_response(status_code=403, business_code="DESIGN_ACCESS_DENIED", message="Active course enrollment is required.", trace_id=trace_id)
        row = query_one(db, INSERT_ROOT_DISCUSSION, {"user_id": user_id, "course_id": body.course_id, "title": body.title.strip(), "content": body.content.strip()})
        author_row = query_one(db, FIND_DISCUSSION_AUTHOR, {"user_id": user_id})
        if row is None or author_row is None:
            db.rollback()
            return _internal_error(trace_id)
        discussion = Discussion(id=row["id"], course_id=row["course_id"], title=row["title"], content=row["content"], author=DiscussionAuthor(id=author_row["author_id"], full_name=author_row["author_full_name"], avatar_url=author_row.get("author_avatar_url")), status=row["status"], comments=[])
        db.commit()
        result = DiscussionPage(items=[discussion], pagination=Pagination(page=1, size=1, total=1, total_pages=1))
    except (SQLAlchemyError, ValidationError, KeyError, TypeError):
        db.rollback()
        logger.exception("Create discussion failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    return success_response(business_code="DESIGN_RESOURCE_CREATED", message="Discussion created.", trace_id=trace_id, data=result.model_dump(mode="json"))


def _internal_error(trace_id: str) -> JSONResponse:
    return error_response(status_code=500, business_code="DESIGN_INTERNAL_ERROR", message="Discussion could not be created.", trace_id=trace_id)
