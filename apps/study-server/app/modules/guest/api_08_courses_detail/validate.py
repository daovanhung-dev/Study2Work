from __future__ import annotations


def parse_course_id(value: str | int) -> int:
    """Parse and validate course_id from path parameter.
    Args:
        value: Raw course_id segment from the URL path.
    Returns:
        The parsed integer course ID.
    Raises:
        ValueError: If value cannot be parsed into an integer.
    """
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("course_id must be a valid integer.") from exc
