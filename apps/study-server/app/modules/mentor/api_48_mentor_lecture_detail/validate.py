"""Parse path lecture ID theo int64 contract của API #48."""

import re

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1
_SIGNED_INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+\Z")


def parse_lecture_id(value: str) -> int | None:
    """Trả lecture ID signed-int64 hoặc None nếu path không biểu diễn được giá trị hợp lệ."""

    if len(value) > 20 or _SIGNED_INTEGER_PATTERN.fullmatch(value) is None:
        return None
    lecture_id = int(value)
    if not INT64_MIN <= lecture_id <= INT64_MAX:
        return None
    return lecture_id
