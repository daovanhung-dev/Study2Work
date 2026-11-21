"""Đọc resource, kiểm tra parent course public và dựng response API #12."""

from __future__ import annotations

import logging
from typing import Any
from urllib.parse import urlsplit

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.guest.api_12_resources_detail.models import ResourceDetail
from app.modules.guest.api_12_resources_detail.query import (
    ACTIVE_COURSE_ENROLLMENT,
    PUBLISHED_PARENT_COURSE,
    RESOURCE_BY_ID,
)
from app.modules.guest.api_12_resources_detail.validate import (
    resource_not_found,
    validate_resource_id,
)
from app.service.object_storage.upload import (
    UploadStorageUnavailableError,
    get_upload_storage_provider,
)
from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
RESOURCE_SIGNED_URL_TTL_SECONDS = 300


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
    authorization: str | None = None,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Đọc resource public hoặc cấp signed URL private sau khi xác minh enrollment."""

    validated_resource_id = validate_resource_id(resource_id, trace_id=trace_id)
    if isinstance(validated_resource_id, JSONResponse):
        return validated_resource_id

    try:
        resource_row = find_resource(db, resource_id=validated_resource_id)
        if resource_row is None:
            return resource_not_found(trace_id)

        lesson_id = resource_row.get("lesson_id")
        parent_course: dict[str, Any] | None = None
        if lesson_id is not None:
            parent_course = find_published_parent_course(db, lesson_id=lesson_id)
            if parent_course is None:
                return resource_not_found(trace_id)

    except SQLAlchemyError:
        db.rollback()
        logger.exception("Resource detail lookup failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if resource_row.get("visibility") == "PRIVATE":
        authentication = validate_current_user_request(
            authorization,
            role="STUDENT",
            trace_id=trace_id,
            internal_error_message="Resource access could not be verified.",
        )
        if isinstance(authentication, JSONResponse):
            return authentication
        user_id, _roles = authentication
        if parent_course is None:
            return resource_not_found(trace_id)
        try:
            enrollment = query_one(
                db,
                ACTIVE_COURSE_ENROLLMENT,
                {"user_id": user_id, "course_id": parent_course["course_id"]},
            )
        except SQLAlchemyError:
            db.rollback()
            logger.exception("Resource enrollment check failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        if enrollment is None:
            return _access_denied(trace_id)

        storage_key = resource_row.get("storage_key")
        if not isinstance(storage_key, str) or not storage_key.strip():
            return resource_not_found(trace_id)
        try:
            resource_url = get_upload_storage_provider().create_signed_url(
                storage_key=storage_key,
                expires_in=RESOURCE_SIGNED_URL_TTL_SECONDS,
            )
        except UploadStorageUnavailableError:
            logger.exception("Private resource signing failed; trace_id=%s", trace_id)
            return _dependency_unavailable(trace_id)
    else:
        resource_url = resource_row.get("url")
        try:
            parsed_url = urlsplit(resource_url) if isinstance(resource_url, str) else None
        except ValueError:
            parsed_url = None
        if parsed_url is None or parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            return resource_not_found(trace_id)

    try:
        resource = ResourceDetail.model_validate({**resource_row, "url": resource_url})
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


def _access_denied(trace_id: str) -> JSONResponse:
    """Ẩn resource private khỏi Student chưa ghi danh active."""

    return error_response(
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message="Active course enrollment is required to access this resource.",
        trace_id=trace_id,
    )


def _dependency_unavailable(trace_id: str) -> JSONResponse:
    """Báo storage signer không sẵn sàng mà không làm lộ thông tin cấu hình."""

    return error_response(
        status_code=503,
        business_code="DESIGN_DEPENDENCY_UNAVAILABLE",
        message="Resource storage is temporarily unavailable.",
        trace_id=trace_id,
    )
