"""Các câu lệnh SQL cho API #9 danh sách bài học của khóa học (curriculum)."""

CHECK_PUBLISHED_COURSE = """
SELECT
    c.id,
    c.status
FROM courses AS c
WHERE c.id = :course_id AND c.status = :status
"""

LIST_PUBLISHED_LESSONS = """
SELECT
    l.id,
    l.course_id,
    l.name AS title,
    l.content,
    l.video_url,
    l.sort_order AS "order",
    l.status
FROM lessons AS l
WHERE l.course_id = :course_id AND l.status = :status
ORDER BY l.sort_order ASC, l.id ASC
"""
