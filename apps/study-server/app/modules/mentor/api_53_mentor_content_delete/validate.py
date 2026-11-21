"""Parse Content ID theo path int64 của API #53."""

import re

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1
_SIGNED_INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+\Z")


def parse_content_id(value: str) -> int | None:
    """Trả Content ID signed-int64 hoặc None nếu path sai format/range."""

    if len(value) > 20 or _SIGNED_INTEGER_PATTERN.fullmatch(value) is None:
        return None
    content_id = int(value)
    if not INT64_MIN <= content_id <= INT64_MAX:
        return None
    return content_id
