"""Câu SQL tĩnh đọc danh sách Lesson cho Admin API #82."""

LIST_ADMIN_LESSONS = """
SELECT
    l.id,
    l.course_id,
    l.name AS title,
    l.content,
    l.video_url,
    l.sort_order AS "order",
    l.status
FROM lessons AS l
WHERE (:course_id IS NULL OR l.course_id = :course_id)
  AND (:status IS NULL OR l.status = :status)
  AND l.status IS DISTINCT FROM 'DELETED'
ORDER BY l.course_id ASC NULLS LAST, l.sort_order ASC NULLS LAST, l.id ASC
"""
