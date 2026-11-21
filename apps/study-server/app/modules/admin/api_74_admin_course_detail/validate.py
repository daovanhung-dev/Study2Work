"""Xác thực role Admin và parse course_id theo signed-int64 contract của API #74."""

from __future__ import annotations

import re

from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1
_SIGNED_INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+\Z")


def validate_admin_request(
    authorization: str | None,
    *,
    trace_id: str,
) -> int | JSONResponse:
    """Yêu cầu JWT role ADMIN qua shared guard trước khi đọc course."""

    authentication = validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Course could not be retrieved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    admin_id, _roles = authentication
    return admin_id


def parse_admin_course_id(value: str) -> int | None:
    """Trả course ID signed-int64 hoặc None nếu path sai định dạng/vượt miền."""

    if len(value) > 20 or _SIGNED_INTEGER_PATTERN.fullmatch(value) is None:
        return None
    course_id = int(value)
    if not INT64_MIN <= course_id <= INT64_MAX:
        return None
    return course_id
