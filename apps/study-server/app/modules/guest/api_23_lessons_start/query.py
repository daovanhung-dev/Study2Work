"""Hằng số truy vấn SQL cho API #23 khởi tạo lần bắt đầu học bài học."""

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
    e.id
FROM enrollments AS e
WHERE e.user_id = :user_id
  AND e.course_id = :course_id
  AND e.status IN ('ACTIVE', 'COMPLETED')
LIMIT 1
"""

UPSERT_LESSON_PROGRESS = """
INSERT INTO lesson_progress (
    user_id,
    lesson_id,
    status
)
VALUES (
    :user_id,
    :lesson_id,
    'IN_PROGRESS'
)
ON CONFLICT (user_id, lesson_id) DO UPDATE
SET status = CASE
    WHEN lesson_progress.status = 'COMPLETED' THEN lesson_progress.status
    ELSE 'IN_PROGRESS'
END
RETURNING id
"""

