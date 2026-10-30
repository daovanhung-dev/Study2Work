"""Parse và kiểm tra CSV recipients/channels của API #63."""

from __future__ import annotations

import re

from app.core.responses import ErrorDetail, error_response
from app.modules.mentor.api_63_mentor_notifications_create.models import (
    NormalizedNotificationRequest,
)
from starlette.responses import JSONResponse

INT64_MAX = 2**63 - 1
_POSITIVE_INTEGER_PATTERN = re.compile(r"[0-9]+\Z")
_ALLOWED_CHANNELS = {"PUSH", "EMAIL"}


def _validation_error(
    *,
    trace_id: str,
    field: str,
    code: str,
    message: str,
) -> JSONResponse:
    """Dựng error envelope 422 cho một CSV field sai định dạng."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Notification request is invalid.",
        trace_id=trace_id,
        errors=[ErrorDetail(field=field, code=code, message=message)],
    )


def _parse_recipients(value: str) -> list[int] | None:
    """Parse CSV positive int64 Student IDs và loại duplicate theo vị trí đầu."""

    if not value.strip():
        return None

    recipient_ids: list[int] = []
    seen_ids: set[int] = set()
    for raw_id in value.split(","):
        token = raw_id.strip()
        if (
            not token
            or len(token) > 19
            or _POSITIVE_INTEGER_PATTERN.fullmatch(token) is None
        ):
            return None
        recipient_id = int(token)
        if recipient_id < 1 or recipient_id > INT64_MAX:
            return None
        if recipient_id not in seen_ids:
            recipient_ids.append(recipient_id)
            seen_ids.add(recipient_id)

    return recipient_ids or None


def _parse_channels(value: str) -> list[str] | None:
    """Parse CSV `PUSH`/`EMAIL` tokens và loại duplicate theo vị trí đầu."""

    if not value.strip():
        return None

    channels: list[str] = []
    seen_channels: set[str] = set()
    for raw_channel in value.split(","):
        channel = raw_channel.strip()
        if not channel or channel not in _ALLOWED_CHANNELS:
            return None
        if channel not in seen_channels:
            channels.append(channel)
            seen_channels.add(channel)

    return channels or None


def validate_notification_request(
    *,
    recipients: str,
    channels: str,
    trace_id: str,
) -> NormalizedNotificationRequest | JSONResponse:
    """Chuẩn hóa CSV inputs hoặc trả lỗi HTTP 422 theo field không hợp lệ."""

    recipient_ids = _parse_recipients(recipients)
    if recipient_ids is None:
        return _validation_error(
            trace_id=trace_id,
            field="recipients",
            code="INVALID_RECIPIENTS",
            message="Recipients must be comma-separated positive int64 Student IDs.",
        )

    parsed_channels = _parse_channels(channels)
    if parsed_channels is None:
        return _validation_error(
            trace_id=trace_id,
            field="channels",
            code="INVALID_CHANNELS",
            message="Channels must contain PUSH and/or EMAIL.",
        )

    return NormalizedNotificationRequest(
        recipient_ids=recipient_ids,
        channels=parsed_channels,
    )
