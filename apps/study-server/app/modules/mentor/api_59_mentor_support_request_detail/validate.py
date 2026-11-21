"""Parse request ID theo signed-int64 contract của API #59."""

import re

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1
_SIGNED_INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+\Z")


def parse_support_request_id(value: str) -> int | None:
    """Trả request ID signed-int64 hoặc None nếu path sai định dạng hay vượt miền."""

    if len(value) > 20 or _SIGNED_INTEGER_PATTERN.fullmatch(value) is None:
        return None
    request_id = int(value)
    if not INT64_MIN <= request_id <= INT64_MAX:
        return None
    return request_id
