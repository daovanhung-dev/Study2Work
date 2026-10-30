"""Parse raw discussion path ID theo hợp đồng API #98."""

from __future__ import annotations

import re

MAX_INT64 = 2**63 - 1
_POSITIVE_INTEGER_PATTERN = re.compile(r"[0-9]+\Z")


def parse_admin_discussion_detail_id(value: object) -> int | None:
    """Parse ID dương trong miền signed-int64 hoặc trả None nếu không hợp lệ."""

    if (
        not isinstance(value, str)
        or len(value) > 19
        or _POSITIVE_INTEGER_PATTERN.fullmatch(value) is None
    ):
        return None
    discussion_id = int(value)
    return discussion_id if 1 <= discussion_id <= MAX_INT64 else None
