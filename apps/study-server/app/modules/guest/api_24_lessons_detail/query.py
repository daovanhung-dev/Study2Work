"""Hằng số truy vấn SQL cho API #24 nạp nội dung bài học."""

FIND_LESSON_AND_COURSE_STATUS = """
SELECT
    l.id,
    l.course_id,
    l.name AS title,
    l.content,
    l.video_url,
    l.sort_order AS "order",
    l.status,
    c.status AS course_status
FROM lessons AS l
INNER JOIN courses AS c ON c.id = l.course_id
WHERE l.id = :lesson_id
LIMIT 1
"""

FIND_ACTIVE_ENROLLMENT = """
SELECT
    e.id
FROM enrollments AS e
WHERE e.user_id = :user_id
  AND e.course_id = :course_id
  AND e.status IN ('ACTIVE', 'COMPLETED')
LIMIT 1
"""

