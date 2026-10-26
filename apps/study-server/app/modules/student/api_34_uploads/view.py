"""Điều phối quyền course, Object Storage và metadata transaction cho API #34."""

from __future__ import annotations

import logging
from typing import Any
from uuid import uuid4

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.student.api_34_uploads.models import UploadAssetResponse, UploadPurpose
from app.modules.student.api_34_uploads.query import (
    FIND_ACTIVE_STUDENT_ENROLLMENT,
    FIND_MENTOR_OWNED_COURSE,
    INSERT_UPLOAD_ASSET,
)
from app.modules.student.api_34_uploads.validate import validate_upload_policy
from app.service.object_storage.upload import UploadStorageProvider
from app.utils.auth import validate_current_user_request
from fastapi import UploadFile
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def _internal_upload_error(trace_id: str) -> JSONResponse:
    """Tạo lỗi 500 an toàn khi DB hoặc metadata API #34 gặp lỗi."""

    # Dựng business code chung mà không phản chiếu exception nội bộ.
    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Upload could not be completed.",
        trace_id=trace_id,
    )


def _access_denied(trace_id: str) -> JSONResponse:
    """Tạo lỗi 403 chung khi principal không có quan hệ course cần thiết."""

    # Dùng cùng lỗi access cho enrollment và direct-owner không khớp.
    return error_response(
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message="Access denied.",
        trace_id=trace_id,
    )


def _best_effort_delete(
    provider: UploadStorageProvider,
    *,
    storage_key: str,
    trace_id: str,
) -> None:
    """Thử xóa object mồ côi mà không làm thay đổi kết quả lỗi đã chọn."""

    try:
        # Dùng key server-generated để bù object đã ghi dở hoặc thiếu metadata.
        provider.delete(storage_key=storage_key)
    except Exception:
        logger.error("Upload object cleanup failed; trace_id=%s", trace_id)


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback an toàn để lỗi rollback không bỏ qua bước dọn object hoặc dựng response."""

    try:
        # Giải phóng transaction trước khi view trả lỗi hoặc gọi storage cleanup.
        db.rollback()
    except Exception:
        logger.error("Upload transaction rollback failed; trace_id=%s", trace_id)


def _measure_file_size(file: UploadFile) -> int | None:
    """Đo số byte từ file spool và đưa con trỏ về đầu để provider đọc toàn bộ nội dung."""

    try:
        # Seek trên file spool để đếm bytes mà không nạp toàn bộ payload vào RAM.
        file.file.seek(0, 2)
        size_bytes = file.file.tell()
        file.file.seek(0)
    except (OSError, AttributeError):
        return None
    return size_bytes


def _has_upload_scope(
    db: Session,
    *,
    user_id: int,
    purpose: UploadPurpose,
    course_id: int | None,
) -> bool:
    """Kiểm tra enrollment ACTIVE của Student hoặc direct owner của Mentor."""

    if purpose is UploadPurpose.SUBMISSION and course_id is None:
        # Student không gắn course không cần enrollment lookup.
        return True
    if course_id is None:
        return False
    if purpose is UploadPurpose.SUBMISSION:
        # Chỉ cho Student tiếp tục khi enrollment ACTIVE khớp cả user và course.
        return (
            query_one(
                db,
                FIND_ACTIVE_STUDENT_ENROLLMENT,
                {"student_id": user_id, "course_id": course_id},
            )
            is not None
        )
    # Mentor chỉ tiếp tục khi là owner trực tiếp trong courses.mentor_id.
    return (
        query_one(
            db,
            FIND_MENTOR_OWNED_COURSE,
            {"mentor_id": user_id, "course_id": course_id},
        )
        is not None
    )


# API #34 uploads
def create_upload(
    *,
    authorization: str | None,
    file: UploadFile,
    purpose: UploadPurpose,
    course_id: int | None,
    db: Session,
    provider: UploadStorageProvider,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực actor, tải object, lưu UploadAsset rồi trả metadata có ID bền vững."""

    # Chấp nhận token có một trong hai role API #34 trước khi kiểm tra purpose.
    authentication = validate_current_user_request(
        authorization,
        role=("STUDENT", "MENTOR"),
        trace_id=trace_id,
        internal_error_message="Upload could not be completed.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    user_id, roles = authentication

    # Gắn role với purpose và kiểm tra course_id có thể biểu diễn bằng int64.
    validation_error = validate_upload_policy(
        roles=roles,
        purpose=purpose,
        course_id=course_id,
        trace_id=trace_id,
    )
    if validation_error is not None:
        return validation_error

    # Kiểm tra enrollment hoặc direct ownership trước khi ghi ra Object Storage.
    try:
        has_scope = _has_upload_scope(
            db,
            user_id=user_id,
            purpose=purpose,
            course_id=course_id,
        )
    except Exception:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Upload scope lookup failed; trace_id=%s", trace_id)
        return _internal_upload_error(trace_id)
    if not has_scope:
        _rollback_safely(db, trace_id=trace_id)
        return _access_denied(trace_id)

    # Đo kích thước file thực tế và khởi tạo metadata lấy từ multipart header.
    size_bytes = _measure_file_size(file)
    if size_bytes is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Upload file size measurement failed; trace_id=%s", trace_id)
        return _internal_upload_error(trace_id)
    file_name = file.filename or "upload"
    content_type = file.content_type or "application/octet-stream"
    storage_key = f"uploads/{uuid4()}"

    # Tải file bằng key UUID phía server; lỗi storage dùng status 503 theo catalog.
    try:
        url = provider.upload(
            storage_key=storage_key,
            file_obj=file.file,
            content_type=content_type,
        )
    except Exception:
        _rollback_safely(db, trace_id=trace_id)
        _best_effort_delete(provider, storage_key=storage_key, trace_id=trace_id)
        logger.error("Upload object write failed; trace_id=%s", trace_id)
        return error_response(
            status_code=503,
            business_code="DESIGN_DEPENDENCY_UNAVAILABLE",
            message="Upload storage is unavailable.",
            trace_id=trace_id,
        )

    # Ghi metadata sau khi object thành công và commit ID được tạo bởi BIGSERIAL.
    try:
        row = query_one(
            db,
            INSERT_UPLOAD_ASSET,
            {
                "owner_id": user_id,
                "purpose": purpose.value,
                "course_id": course_id,
                "storage_key": storage_key,
                "file_name": file_name,
                "url": url,
                "content_type": content_type,
                "size_bytes": size_bytes,
            },
        )
        asset_id = row.get("id") if row is not None else None
        if type(asset_id) is not int:
            _rollback_safely(db, trace_id=trace_id)
            _best_effort_delete(provider, storage_key=storage_key, trace_id=trace_id)
            logger.error("Upload metadata insert returned no ID; trace_id=%s", trace_id)
            return _internal_upload_error(trace_id)
        asset = UploadAssetResponse(
            id=asset_id,
            name=file_name,
            url=url,
            content_type=content_type,
            size_bytes=size_bytes,
            status="UPLOADED",
        )
        db.commit()
    except Exception:
        _rollback_safely(db, trace_id=trace_id)
        _best_effort_delete(provider, storage_key=storage_key, trace_id=trace_id)
        logger.error("Upload metadata transaction failed; trace_id=%s", trace_id)
        return _internal_upload_error(trace_id)

    # Trả metadata đã commit để caller có thể tham chiếu bằng UploadAsset ID.
    return success_response(
        business_code="DESIGN_RESOURCE_CREATED",
        message="Upload accepted.",
        trace_id=trace_id,
        data=asset.model_dump(mode="json"),
    )
