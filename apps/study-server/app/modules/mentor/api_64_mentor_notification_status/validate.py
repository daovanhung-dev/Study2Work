"""Parse notification ID theo signed-int64 contract của API #64."""

import re

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1
_SIGNED_INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+\Z")


def parse_notification_id(value: str) -> int | None:
    """Trả notification ID signed-int64 hoặc None nếu path không hợp lệ."""

    if len(value) > 20 or _SIGNED_INTEGER_PATTERN.fullmatch(value) is None:
        return None
    notification_id = int(value)
    if not INT64_MIN <= notification_id <= INT64_MAX:
        return None
    return notification_id
