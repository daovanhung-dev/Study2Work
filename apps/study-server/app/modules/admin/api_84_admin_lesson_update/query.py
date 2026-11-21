"""Câu SQL tĩnh cập nhật metadata candidate cho Admin Lesson API #84."""

UPDATE_ADMIN_LESSON_METADATA = """
UPDATE lessons AS l
SET
    name = :title,
    content = :content,
    video_url = :video_url,
    sort_order = :order,
    updated_at = CURRENT_TIMESTAMP
WHERE l.id = :lesson_id
  AND l.status IS DISTINCT FROM 'DELETED'
RETURNING
    l.id,
    l.course_id,
    l.name AS title,
    l.content,
    l.video_url,
    l.sort_order AS "order",
    l.status
"""
