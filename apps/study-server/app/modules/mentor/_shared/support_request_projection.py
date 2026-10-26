"""Ánh xạ SupportRequest và thread theo reusable response schema."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.modules.mentor.api_58_mentor_support_requests.models import (
    SupportMessageResponse,
    SupportRequestResponse,
    UserSummaryResponse,
)
from app.modules.student.api_34_uploads.models import UploadAssetResponse
from pydantic import ValidationError

_MESSAGE_FIELDS = (
    "author_id",
    "author_user_id",
    "author_role",
    "author_full_name",
    "content",
    "message_created_at",
)
_ASSET_FIELDS = (
    "attachment_id",
    "attachment_name",
    "attachment_url",
    "attachment_content_type",
    "attachment_size_bytes",
    "attachment_status",
)


def map_support_request(row: Mapping[str, Any], request_id: int) -> SupportRequestResponse | None:
    """Kiểm tra parent projections và ánh xạ một support request đã được scope."""

    # Không xây response từ FK hoặc parent projection thiếu, sai kiểu hay không khớp.
    if type(row.get("id")) is not int or row.get("id") != request_id:
        return None
    if type(row.get("course_id")) is not int or row.get("course_id") < 1:
        return None
    if (
        type(row.get("parent_course_id")) is not int
        or row.get("parent_course_id") != row.get("course_id")
    ):
        return None
    if type(row.get("mentor_id")) is not int:
        return None
    if type(row.get("student_id")) is not int or row.get("student_id") < 1:
        return None
    if row.get("student_user_id") != row.get("student_id"):
        return None

    try:
        return SupportRequestResponse(
            id=request_id,
            course_id=row.get("course_id"),
            student=UserSummaryResponse(
                id=row.get("student_user_id"),
                full_name=row.get("student_full_name"),
                avatar_url=row.get("student_avatar_url"),
            ),
            status=row.get("status"),
            messages=[],
            created_at=row.get("created_at"),
            resolved_at=row.get("resolved_at"),
        )
    except (TypeError, ValidationError):
        return None


def append_support_messages(
    support_request: SupportRequestResponse,
    rows: list[dict[str, Any]],
    *,
    mentor_id: int,
) -> bool:
    """Gom thread theo query order và từ chối author/link/upload projection lỗi."""

    messages_by_id: dict[int, SupportMessageResponse] = {}
    assets_by_message: dict[int, set[int]] = {}
    if not rows:
        return False

    try:
        for row in rows:
            # Q2 lặp lại owner predicate; kiểm tra mọi hàng trước khi dùng projection.
            if not isinstance(row, Mapping):
                return False
            if (
                type(row.get("request_id")) is not int
                or row.get("request_id") != support_request.id
            ):
                return False
            if (
                type(row.get("course_id")) is not int
                or row.get("course_id") != support_request.course_id
            ):
                return False
            if (
                type(row.get("parent_course_id")) is not int
                or row.get("parent_course_id") != support_request.course_id
            ):
                return False
            if type(row.get("mentor_id")) is not int or row.get("mentor_id") != mentor_id:
                return False

            message_id = row.get("message_id")
            linked_upload_id = row.get("linked_upload_id")
            if message_id is None:
                if linked_upload_id is not None:
                    return False
                if any(row.get(field) is not None for field in _MESSAGE_FIELDS):
                    return False
                if any(row.get(field) is not None for field in _ASSET_FIELDS):
                    return False
                continue
            if type(message_id) is not int or message_id < 1:
                return False
            if (
                type(row.get("author_id")) is not int
                or row.get("author_user_id") != row.get("author_id")
            ):
                return False

            message = messages_by_id.get(message_id)
            if message is None:
                message = SupportMessageResponse(
                    id=message_id,
                    author=UserSummaryResponse(
                        id=row.get("author_user_id"),
                        full_name=row.get("author_full_name"),
                        avatar_url=row.get("author_avatar_url"),
                    ),
                    content=row.get("content"),
                    attachments=[],
                    created_at=row.get("message_created_at"),
                )
                messages_by_id[message_id] = message
                assets_by_message[message_id] = set()
                support_request.messages.append(message)
            elif (
                message.author.id != row.get("author_user_id")
                or message.author.full_name != row.get("author_full_name")
                or message.author.avatar_url != row.get("author_avatar_url")
                or message.content != row.get("content")
                or message.created_at != row.get("message_created_at")
            ):
                return False

            if linked_upload_id is None:
                if any(row.get(field) is not None for field in _ASSET_FIELDS):
                    return False
                continue

            # Link row không resolve đúng UploadAsset scoped là lỗi toàn response.
            attachment_id = row.get("attachment_id")
            if (
                type(linked_upload_id) is not int
                or type(attachment_id) is not int
                or attachment_id != linked_upload_id
            ):
                return False
            if attachment_id in assets_by_message[message_id]:
                return False
            asset = UploadAssetResponse(
                id=attachment_id,
                name=row.get("attachment_name"),
                url=row.get("attachment_url"),
                content_type=row.get("attachment_content_type"),
                size_bytes=row.get("attachment_size_bytes"),
                status=row.get("attachment_status"),
            )
            assets_by_message[message_id].add(attachment_id)
            message.attachments.append(asset)
    except (TypeError, ValidationError):
        return False

    return True
