from __future__ import annotations

import logging
import math
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.student._shared.discussions import Discussion, DiscussionAuthor, DiscussionComment, DiscussionPage, Pagination
from app.modules.student.api_39_discussions.query import COUNT_ROOT_DISCUSSIONS, LIST_ACTIVE_COMMENTS, LIST_ROOT_DISCUSSIONS
from app.modules.student.api_39_discussions.validate import validate_discussion_list
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
PAGE_SIZE = 20


def _discussion(row: dict[str, Any], comments: list[dict[str, Any]]) -> Discussion:
    author = DiscussionAuthor(id=row["author_id"], full_name=row["author_full_name"], avatar_url=row.get("author_avatar_url"))
    mapped_comments = [DiscussionComment(id=c["id"], discussion_id=c["discussion_id"], content=c["content"], author=DiscussionAuthor(id=c["author_id"], full_name=c["author_full_name"], avatar_url=c.get("author_avatar_url")), created_at=c["created_at"]) for c in comments]
    return Discussion(id=row["id"], course_id=row["course_id"], title=row["title"], content=row["content"], author=author, status=row["status"], comments=mapped_comments)


def get_discussions(*, authorization: str | None, course_id_raw: str | None, page_raw: str | None, sort_raw: str | None, db: Session, trace_id: str) -> dict[str, Any] | JSONResponse:
    validated = validate_discussion_list(authorization, course_id_raw, page_raw, trace_id=trace_id)
    if isinstance(validated, JSONResponse):
        return validated
    user_id, course_id, page_number = validated
    try:
        params = {"user_id": user_id, "course_id": course_id}
        count = query_one(db, COUNT_ROOT_DISCUSSIONS, params)
        total = int((count or {}).get("total", 0))
        rows = query_many(db, LIST_ROOT_DISCUSSIONS, {**params, "limit": PAGE_SIZE, "offset": (page_number - 1) * PAGE_SIZE})
        items = [_discussion(row, query_many(db, LIST_ACTIVE_COMMENTS, {"discussion_id": row["id"]})) for row in rows]
        result = DiscussionPage(items=items, pagination=Pagination(page=page_number, size=PAGE_SIZE, total=total, total_pages=math.ceil(total / PAGE_SIZE) if total else 0))
    except (SQLAlchemyError, ValidationError, KeyError, TypeError):
        db.rollback()
        logger.exception("Discussion list failed; trace_id=%s", trace_id)
        return error_response(status_code=500, business_code="DESIGN_INTERNAL_ERROR", message="Discussions could not be retrieved.", trace_id=trace_id)
    return success_response(business_code="DESIGN_RESOURCE_RETRIEVED", message="Discussions retrieved.", trace_id=trace_id, data=result.model_dump(mode="json"))
