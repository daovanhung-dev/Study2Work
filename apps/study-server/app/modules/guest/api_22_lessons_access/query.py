"""Hằng số truy vấn SQL cho API #22 kiểm tra quyền truy cập bài học."""

FIND_LESSON_BY_ID = """
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
LIMIT 1
"""

FIND_ACTIVE_ENROLLMENT = """
SELECT
    e.id,
    e.status
FROM enrollments AS e
WHERE e.user_id = :user_id
  AND e.course_id = :course_id
  AND e.status IN ('ACTIVE', 'COMPLETED')
LIMIT 1
"""

