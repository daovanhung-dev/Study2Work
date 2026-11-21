"""Các câu lệnh SQL cho API #27 tìm bài học tiếp theo theo curriculum."""

FIND_CURRENT_LESSON = """
SELECT
    l.id,
    l.course_id,
    l.sort_order,
    l.status
FROM lessons AS l
JOIN courses AS c ON c.id = l.course_id
WHERE l.id = :lesson_id
  AND c.status = 'PUBLISHED'
LIMIT 1
"""

FIND_NEXT_LESSON = """
SELECT
    l.id,
    l.course_id,
    l.name AS title,
    l.content,
    l.video_url,
    l.sort_order AS "order",
    l.status
FROM lessons AS l
WHERE l.course_id = :course_id
  AND l.status = 'PUBLISHED'
  AND (
      l.sort_order > :current_sort_order
      OR (l.sort_order = :current_sort_order AND l.id > :current_lesson_id)
  )
ORDER BY l.sort_order ASC, l.id ASC
LIMIT 1
"""

