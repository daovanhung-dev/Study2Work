"""Đọc resource, kiểm tra parent course public và dựng response API #12."""

from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.guest.api_12_resources_detail.models import ResourceDetail
from app.modules.guest.api_12_resources_detail.query import (
    PUBLISHED_PARENT_COURSE,
    RESOURCE_BY_ID,
)
from app.modules.guest.api_12_resources_detail.validate import (
    resource_not_found,
    validate_resource_id,
)
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def find_resource(db: Session, *, resource_id: int) -> dict[str, Any] | None:
    """Đọc metadata resource theo ID và không thay đổi transaction của Session."""

    return query_one(db, RESOURCE_BY_ID, {"resource_id": resource_id})


def find_published_parent_course(db: Session, *, lesson_id: int) -> dict[str, Any] | None:
    """Đọc lesson cùng course cha khi course đang ở trạng thái PUBLISHED."""

    return query_one(db, PUBLISHED_PARENT_COURSE, {"lesson_id": lesson_id})


# API #12 resources_detail
def get_resource_detail(
    *,
    resource_id: str,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Validate path, đọc resource và chỉ expose parent-linked resource của course đã publish."""

    validated_resource_id = validate_resource_id(resource_id, trace_id=trace_id)
    if isinstance(validated_resource_id, JSONResponse):
        return validated_resource_id

    try:
        resource_row = find_resource(db, resource_id=validated_resource_id)
        if resource_row is None:
            return resource_not_found(trace_id)

        lesson_id = resource_row.get("lesson_id")
        if lesson_id is not None:
            parent_course = find_published_parent_course(db, lesson_id=lesson_id)
            if parent_course is None:
                return resource_not_found(trace_id)

        resource = ResourceDetail.model_validate(resource_row)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Resource detail lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    except ValidationError:
        logger.exception("Resource detail mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Resource metadata retrieved",
        trace_id=trace_id,
        data=resource.model_dump(mode="json"),
    )


def _internal_error(trace_id: str) -> JSONResponse:
    """Tạo response 500 an toàn khi query hoặc mapping resource thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Resource could not be retrieved",
        trace_id=trace_id,
    )
