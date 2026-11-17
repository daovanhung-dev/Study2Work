from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.student._shared.discussions import Discussion, DiscussionAuthor, DiscussionComment, DiscussionPage, Pagination
from app.modules.student.api_42_discussions_detail.query import FIND_STUDENT_DISCUSSION, LIST_ACTIVE_COMMENTS
from app.modules.student.api_42_discussions_detail.validate import validate_discussion_detail
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def get_discussion_detail(*, authorization: str | None, discussion_id_raw: str, db: Session, trace_id: str) -> dict[str, Any] | JSONResponse:
    validated = validate_discussion_detail(authorization, discussion_id_raw, trace_id=trace_id)
    if isinstance(validated, JSONResponse):
        return validated
    user_id, discussion_id = validated
    try:
        row = query_one(db, FIND_STUDENT_DISCUSSION, {"discussion_id": discussion_id, "user_id": user_id})
        if row is None:
            return error_response(status_code=404, business_code="DESIGN_RESOURCE_NOT_FOUND", message="Discussion not found.", trace_id=trace_id)
        comments = query_many(db, LIST_ACTIVE_COMMENTS, {"discussion_id": discussion_id})
        discussion = Discussion(
            id=row["id"], course_id=row["course_id"], title=row["title"], content=row["content"],
            author=DiscussionAuthor(id=row["author_id"], full_name=row["author_full_name"], avatar_url=row.get("author_avatar_url")),
            status=row["status"],
            comments=[DiscussionComment(id=c["id"], discussion_id=c["discussion_id"], content=c["content"], author=DiscussionAuthor(id=c["author_id"], full_name=c["author_full_name"], avatar_url=c.get("author_avatar_url")), created_at=c["created_at"]) for c in comments],
        )
        page = DiscussionPage(items=[discussion], pagination=Pagination(page=1, size=1, total=1, total_pages=1))
    except (SQLAlchemyError, ValidationError, KeyError, TypeError):
        db.rollback()
        logger.exception("Discussion detail failed; trace_id=%s", trace_id)
        return error_response(status_code=500, business_code="DESIGN_INTERNAL_ERROR", message="Discussion could not be retrieved.", trace_id=trace_id)
    return success_response(business_code="DESIGN_RESOURCE_RETRIEVED", message="Discussion retrieved.", trace_id=trace_id, data=page.model_dump(mode="json"))
