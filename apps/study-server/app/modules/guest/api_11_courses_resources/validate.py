"""Chuẩn hóa và kiểm tra dữ liệu đầu vào cho API #11 lấy tài nguyên khóa học."""

from __future__ import annotations


def validate_course_id(course_id: int) -> int:
    """Xác thực course_id từ path segment đảm bảo là số nguyên hợp lệ."""

    if not isinstance(course_id, int):
        raise ValueError("course_id must be an integer.")
    return course_id
