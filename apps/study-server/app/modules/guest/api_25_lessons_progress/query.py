"""Hằng số truy vấn SQL cho API #25 lưu tiến độ bài học."""

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
    lp.status,
    lp.progress_percent,
    lp.completed_at
FROM lesson_progress AS lp
WHERE lp.user_id = :user_id
  AND lp.lesson_id = :lesson_id
ORDER BY lp.id DESC
LIMIT 1
"""

INSERT_LESSON_PROGRESS_STATE = """
INSERT INTO lesson_progress (
    user_id,
    lesson_id,
    status,
    progress_percent,
    last_accessed_at,
    completed_at
)
VALUES (
    :user_id,
    :lesson_id,
    :status,
    :progress_percent,
    CURRENT_TIMESTAMP,
    CASE WHEN :completed THEN CURRENT_TIMESTAMP ELSE NULL END
)
RETURNING id
"""

UPDATE_LESSON_PROGRESS_STATE = """
UPDATE lesson_progress
SET
    status = :status,
    progress_percent = :progress_percent,
    last_accessed_at = CURRENT_TIMESTAMP,
    completed_at = CASE
        WHEN :completed THEN COALESCE(completed_at, CURRENT_TIMESTAMP)
        ELSE completed_at
    END
WHERE id = :progress_id
RETURNING id
"""

