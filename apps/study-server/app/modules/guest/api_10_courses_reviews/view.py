from __future__ import annotations

import logging
from math import ceil
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import ApiError
from app.modules.guest.api_10_courses_reviews.models import CourseReviewsQuery
from app.modules.guest.api_10_courses_reviews.query import (
    COUNT_COURSE_REVIEWS,
    GET_PUBLISHED_COURSE,
    LIST_COURSE_REVIEWS,
    LIST_REVIEW_REPLIES,
)
from app.modules.guest.api_10_courses_reviews.validate import (
    validate_course_reviews_request,
)
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

REVIEW_PAGE_SIZE = 20


# Kiểm tra khóa học có tồn tại và đang được publish
def find_published_course(
    db: Session,
    *,
    course_id: int,
) -> dict[str, Any] | None:
    return query_one(
        db,
        GET_PUBLISHED_COURSE,
        {"course_id": course_id},
    )


# Lấy danh sách review gốc của khóa học
def find_course_reviews(
    db: Session,
    *,
    course_id: int,
    page: int,
) -> list[dict[str, Any]]:
    offset = (page - 1) * REVIEW_PAGE_SIZE

    return query_many(
        db,
        LIST_COURSE_REVIEWS,
        {
            "course_id": course_id,
            "limit": REVIEW_PAGE_SIZE,
            "offset": offset,
        },
    )


# Lấy reply của các review đang có trên trang hiện tại
def find_review_replies(
    db: Session,
    *,
    review_ids: list[int],
) -> list[dict[str, Any]]:
    if not review_ids:
        return []

    review_id_placeholders = ", ".join(
        f":review_id_{index}"
        for index in range(len(review_ids))
    )

    reply_params = {
        f"review_id_{index}": review_id
        for index, review_id in enumerate(review_ids)
    }

    reply_query = LIST_REVIEW_REPLIES.format(
        review_id_placeholders=review_id_placeholders,
    )

    return query_many(
        db,
        reply_query,
        reply_params,
    )


# Đếm tổng số review gốc để tính phân trang (pagination)
def count_course_reviews(
    db: Session,
    *,
    course_id: int,
) -> int:
    total_row = query_one(
        db,
        COUNT_COURSE_REVIEWS,
        {"course_id": course_id},
    )

    if total_row is None:
        return 0

    return int(total_row["total"])


# Lấy danh sách review của khóa học
def get_course_reviews(
    *,
    course_id: str,
    course_query: CourseReviewsQuery,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Lấy danh sách review và reply của một khóa học."""

    # Validate request đầu vào
    try:
        validated = validate_course_reviews_request(
            course_id=course_id,
            course_query=course_query,
            trace_id=trace_id,
        )
    except ValueError:
        # Behavior của malformed page hiện chưa được contract #10 chốt.
        # Không tự biến trường hợp này thành business error.
        return ApiError(
            status_code=500,
            business_code="DESIGN_INTERNAL_ERROR",
            message="Internal server error.",
            trace_id=trace_id,
        )

    if isinstance(validated, JSONResponse):
        return validated

    parsed_course_id, effective_page, _rating = validated

    # Thực hiện các query lấy dữ liệu
    try:
        course = find_published_course(
            db,
            course_id=parsed_course_id,
        )

        if course is None:
            return ApiError(
                status_code=404,
                business_code="DESIGN_RESOURCE_NOT_FOUND",
                message="Course not found.",
                trace_id=trace_id,
            )

        reviews = find_course_reviews(
            db,
            course_id=parsed_course_id,
            page=effective_page,
        )

        review_ids = [review["id"] for review in reviews]

        replies = find_review_replies(
            db,
            review_ids=review_ids,
        )

        total = count_course_reviews(
            db,
            course_id=parsed_course_id,
        )

    except SQLAlchemyError:
        db.rollback()
        logger.exception(
            "Failed to retrieve course reviews",
            extra={
                "course_id": parsed_course_id,
                "trace_id": trace_id,
            },
        )

        return ApiError(
            status_code=500,
            business_code="DESIGN_INTERNAL_ERROR",
            message="Internal server error.",
            trace_id=trace_id,
        )

    # Gom reply theo review cha
    try:
        reply_map: dict[int, list[dict[str, Any]]] = {}

        for reply in replies:
            parent_id = reply["parent_id"]

            reply_item = {
                "discussion_id": reply["id"],
                "user": {
                    "id": reply["author_id"],
                    "full_name": reply["author_full_name"],
                    "avatar_url": reply["author_avatar_url"],
                },
                "content": reply["content"],
                "created_at": reply["created_at"],
            }

            reply_map.setdefault(parent_id, []).append(reply_item)

        # Map dữ liệu review sang response
        items: list[dict[str, Any]] = []

        for review in reviews:
            review_id = review["id"]

            items.append(
                {
                    "discussion_id": review_id,
                    "title": None,
                    "content": review["content"],
                    "user": {
                        "id": review["author_id"],
                        "full_name": review["author_full_name"],
                        "avatar_url": review["author_avatar_url"],
                    },
                    "created_at": review["created_at"],
                    "comments": reply_map.get(review_id, []),
                }
            )

        total_pages = ceil(total / REVIEW_PAGE_SIZE) if total else 0

        # Trả response thành công
        return {
            "success": True,
            "businessCode": "DESIGN_RESOURCE_RETRIEVED",
            "message": "Reviews retrieved",
            "data": {
                "items": items,
                "pagination": {
                    "page": effective_page,
                    "size": REVIEW_PAGE_SIZE,
                    "total": total,
                    "total_pages": total_pages,
                },
            },
            "meta": {},
            "traceId": trace_id,
        }

    except (TypeError, ValueError, KeyError):
        db.rollback()
        logger.exception(
            "Failed to map course reviews response",
            extra={
                "course_id": parsed_course_id,
                "trace_id": trace_id,
            },
        )

        return ApiError(
            status_code=500,
            business_code="DESIGN_INTERNAL_ERROR",
            message="Internal server error.",
            trace_id=trace_id,
        )