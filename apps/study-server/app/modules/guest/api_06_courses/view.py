from __future__ import annotations

import logging
from decimal import InvalidOperation
from typing import Any

from app.core.responses import ApiError, success_response
from app.modules.guest._shared.course_catalog.helpers import (
    course_internal_error,
    map_course,
)
from app.modules.guest._shared.course_catalog.models import CoursePage, Pagination
from app.modules.guest.api_06_courses.models import CourseQuery
from app.modules.guest.api_06_courses.query import (
    count_published_courses,
    find_published_courses,
)
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def get_courses(
    *,
    course_query: CourseQuery,
    db: Session,
    trace_id: str,
) -> dict[str, Any]:
    """Return one public page of published courses."""

    if course_query.category is not None:
        raise ApiError(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Bộ lọc category chưa được hỗ trợ.",
            trace_id=trace_id,
        )

    try:
        count_row = count_published_courses(db)
        if int(count_row.get("missing_mentor_count") or 0) > 0:
            raise course_internal_error(trace_id)
        rows = find_published_courses(
            db,
            page=course_query.page,
            size=course_query.size,
            sort=course_query.sort,
        )
    except ApiError:
        db.rollback()
        raise
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Course lookup failed; trace_id=%s", trace_id)
        raise course_internal_error(trace_id) from exc

    try:
        items = [map_course(row) for row in rows]
        total = int(count_row.get("total") or 0)
        total_pages = (total + course_query.size - 1) // course_query.size if total else 0
        page = CoursePage(
            items=items,
            pagination=Pagination(
                page=course_query.page,
                size=course_query.size,
                total=total,
                total_pages=total_pages,
            ),
        )
    except (InvalidOperation, TypeError, ValueError, ValidationError) as exc:
        logger.exception("Course mapping failed; trace_id=%s", trace_id)
        raise course_internal_error(trace_id) from exc

    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Courses retrieved." if items else "No published courses.",
        trace_id=trace_id,
        data=page.model_dump(mode="json"),
    )
