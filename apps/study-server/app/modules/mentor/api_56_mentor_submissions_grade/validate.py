"""Chuẩn hóa path ID và kiểm tra score API #56 theo schema legacy candidate."""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from typing import Any

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


def parse_assignment_max_score(value: Any) -> Decimal | None:
    """Chuyển max_score candidate sang Decimal hữu hạn không âm, hoặc None khi row lỗi."""

    if value is None or isinstance(value, bool):
        return None
    try:
        max_score = Decimal(str(value))
    except (InvalidOperation, TypeError):
        return None
    if not max_score.is_finite() or max_score < 0:
        return None
    return max_score


def score_is_within_assignment_max(score: int, max_score: Decimal) -> bool:
    """Kiểm tra fallback DERIVED: score nguyên nằm trong [0, assignment.max_score]."""

    return score >= 0 and Decimal(score) <= max_score
