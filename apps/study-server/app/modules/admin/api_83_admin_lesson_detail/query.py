"""Câu SQL tĩnh đọc chi tiết một Lesson cho Admin API #83."""

FIND_ADMIN_LESSON_DETAIL = """
SELECT
    l.id,
    l.course_id,
    l.name AS title,
    l.content,
    l.video_url,
    l.sort_order AS "order",
    l.status
FROM lessons AS l
WHERE l.id = :lesson_id
  AND l.status IS DISTINCT FROM 'DELETED'
"""
