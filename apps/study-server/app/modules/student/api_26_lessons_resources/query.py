"""Các câu lệnh SQL cho API #26 lấy tài nguyên đính kèm bài học."""

CHECK_PUBLISHED_LESSON = """
SELECT
    l.id,
    l.course_id,
    l.name AS title,
    l.content,
    l.video_url,
    l.sort_order AS "order",
    l.status
FROM lessons AS l
JOIN courses AS c ON c.id = l.course_id
WHERE l.id = :lesson_id
  AND c.status = 'PUBLISHED'
LIMIT 1
"""

FIND_LESSON_RESOURCES = """
SELECT
    r.id,
    r.lesson_id,
    r.name,
    r.resource_type AS type,
    r.url
FROM resources AS r
WHERE r.lesson_id = :lesson_id
ORDER BY r.id ASC
"""

