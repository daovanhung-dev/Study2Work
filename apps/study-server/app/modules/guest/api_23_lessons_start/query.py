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

FIND_LESSON_PROGRESS = """
SELECT
    lp.id,
    lp.status
FROM lesson_progress AS lp
WHERE lp.user_id = :user_id
  AND lp.lesson_id = :lesson_id
ORDER BY lp.id DESC
LIMIT 1
"""

INSERT_LESSON_PROGRESS = """
INSERT INTO lesson_progress (
    user_id,
    lesson_id,
    status,
    progress_percent,
    last_accessed_at
)
VALUES (
    :user_id,
    :lesson_id,
    'IN_PROGRESS',
    0,
    CURRENT_TIMESTAMP
)
RETURNING id
"""

TOUCH_LESSON_PROGRESS = """
UPDATE lesson_progress
SET
    status = CASE
        WHEN status = 'COMPLETED' THEN status
        ELSE 'IN_PROGRESS'
    END,
    last_accessed_at = CURRENT_TIMESTAMP
WHERE id = :progress_id
RETURNING id
"""

