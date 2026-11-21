"""Parse các path value signed-int64 cho API #62."""

import re

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1
_SIGNED_INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+\Z")


def parse_course_id(value: str) -> int | None:
    """Trả course ID signed-int64 hoặc None nếu path không biểu diễn được giá trị đó."""

    if len(value) > 20 or _SIGNED_INTEGER_PATTERN.fullmatch(value) is None:
        return None
    course_id = int(value)
    if not INT64_MIN <= course_id <= INT64_MAX:
        return None
    return course_id
