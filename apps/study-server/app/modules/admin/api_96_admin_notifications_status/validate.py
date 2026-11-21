"""Parse raw int64 notification ID cho API #96."""

from __future__ import annotations

import re

MAX_INT64 = 2**63 - 1
_POSITIVE_INTEGER_PATTERN = re.compile(r"[0-9]+\Z")


def parse_admin_notification_status_id(value: object) -> int | None:
    """Parse ID dương trong miền signed-int64 hoặc trả None nếu không hợp lệ."""

    if (
        not isinstance(value, str)
        or len(value) > 19
        or _POSITIVE_INTEGER_PATTERN.fullmatch(value) is None
    ):
        return None
    notification_id = int(value)
    return notification_id if 1 <= notification_id <= MAX_INT64 else None
