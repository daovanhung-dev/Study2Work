"""Chuẩn hóa path ID API #57 theo integer 64 bit có dấu."""

from __future__ import annotations

import re

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1
_SIGNED_INTEGER_PATTERN = re.compile(r"[+-]?[0-9]+\Z")


def parse_submission_id(value: str) -> int | None:
    """Trả signed-int64 submission ID hoặc None nếu path sai định dạng/vượt miền."""

    if len(value) > 20 or _SIGNED_INTEGER_PATTERN.fullmatch(value) is None:
        return None
    submission_id = int(value)
    if not INT64_MIN <= submission_id <= INT64_MAX:
        return None
    return submission_id
