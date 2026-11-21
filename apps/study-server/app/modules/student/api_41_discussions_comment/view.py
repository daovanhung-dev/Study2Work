from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.student._shared.discussions import Discussion, DiscussionAuthor, DiscussionComment, DiscussionPage, Pagination
from app.modules.student.api_39_discussions.query import LIST_ACTIVE_COMMENTS
from app.modules.student.api_41_discussions_comment.models import CreateDiscussionCommentRequest
from app.modules.student.api_41_discussions_comment.query import FIND_DISCUSSION_AUTHOR, FIND_ROOT_FOR_COMMENT, INSERT_DISCUSSION_COMMENT
from app.modules.student.api_41_discussions_comment.validate import validate_comment_request
from pydantic import ValidationError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def add_discussion_comment(*, authorization: str | None, discussion_id_raw: str, payload: CreateDiscussionCommentRequest, db: Session, trace_id: str) -> dict[str, Any] | JSONResponse:
    validated = validate_comment_request(authorization, discussion_id_raw, payload, trace_id=trace_id)
    if isinstance(validated, JSONResponse):
        return validated
    user_id, discussion_id, body = validated
    try:
        root = query_one(db, FIND_ROOT_FOR_COMMENT, {"discussion_id": discussion_id, "user_id": user_id})
        if root is None:
            return error_response(status_code=404, business_code="DESIGN_RESOURCE_NOT_FOUND", message="Discussion not found.", trace_id=trace_id)
        inserted = query_one(db, INSERT_DISCUSSION_COMMENT, {"course_id": root["course_id"], "user_id": user_id, "parent_id": discussion_id, "content": body.content.strip()})
        if inserted is None:
            db.rollback()
            return _internal_error(trace_id)
        author_row = query_one(db, FIND_DISCUSSION_AUTHOR, {"user_id": user_id})
        if author_row is None:
            db.rollback()
            return _internal_error(trace_id)
        comments = query_many(db, LIST_ACTIVE_COMMENTS, {"discussion_id": discussion_id})
        discussion = Discussion(
            id=root["id"], course_id=root["course_id"], title=root["title"], content=root["content"],
            author=DiscussionAuthor(id=root["user_id"], full_name=root["author_full_name"], avatar_url=root.get("author_avatar_url")),
            status=root["status"],
            comments=[DiscussionComment(id=c["id"], discussion_id=c["discussion_id"], content=c["content"], author=DiscussionAuthor(id=c["author_id"], full_name=c["author_full_name"], avatar_url=c.get("author_avatar_url")), created_at=c["created_at"]) for c in comments],
        )
        db.commit()
        page = DiscussionPage(items=[discussion], pagination=Pagination(page=1, size=1, total=1, total_pages=1))
    except (SQLAlchemyError, ValidationError, KeyError, TypeError):
        db.rollback()
        logger.exception("Create discussion comment failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    return success_response(business_code="DESIGN_RESOURCE_CREATED", message="Discussion comment created.", trace_id=trace_id, data=page.model_dump(mode="json"))


def _internal_error(trace_id: str) -> JSONResponse:
    return error_response(status_code=500, business_code="DESIGN_INTERNAL_ERROR", message="Comment could not be created.", trace_id=trace_id)
