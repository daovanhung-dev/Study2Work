"""Các câu SQL chỉ đọc, đếm bốn nhóm bản ghi của API #101."""

COUNT_ADMIN_REPORT_USERS = """
SELECT COUNT(*)::BIGINT AS total
FROM users
WHERE DATE(created_at) BETWEEN :from_date AND :to_date
"""

COUNT_ADMIN_REPORT_COURSES = """
SELECT COUNT(*)::BIGINT AS total
FROM courses
WHERE DATE(created_at) BETWEEN :from_date AND :to_date
"""

COUNT_ADMIN_REPORT_ENROLLMENTS = """
SELECT COUNT(*)::BIGINT AS total
FROM enrollments
WHERE DATE(enrolled_at) BETWEEN :from_date AND :to_date
"""

COUNT_ADMIN_REPORT_DISCUSSIONS = """
SELECT COUNT(*)::BIGINT AS total
FROM discussions
WHERE DATE(created_at) BETWEEN :from_date AND :to_date
"""
