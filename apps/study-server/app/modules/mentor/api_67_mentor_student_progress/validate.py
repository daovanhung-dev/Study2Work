"""Chuẩn hóa signed-int64 path IDs cho API tiến độ Student #67."""

import re

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1
_SIGNED_INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+\Z")


def parse_int64_path_value(value: str) -> int | None:
    """Trả signed-int64 từ path hoặc None nếu giá trị không biểu diễn được."""

    if len(value) > 20 or _SIGNED_INTEGER_PATTERN.fullmatch(value) is None:
        return None
    parsed = int(value)
    if not INT64_MIN <= parsed <= INT64_MAX:
        return None
    return parsed
