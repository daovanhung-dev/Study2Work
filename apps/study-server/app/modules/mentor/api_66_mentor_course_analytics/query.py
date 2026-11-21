"""Các câu SQL tĩnh dùng để kiểm tra course owner và tổng hợp activity API #66."""

FIND_MENTOR_COURSE = """
SELECT
    id,
    mentor_id
FROM courses
WHERE id = :course_id
LIMIT 1
"""

AGGREGATE_COURSE_ACTIVITY = """
WITH activity_by_student_lesson AS (
    SELECT
        lp.user_id,
        lp.lesson_id,
        MAX(lp.last_accessed_at) AS last_accessed_at
    FROM lesson_progress AS lp
    JOIN lessons AS l ON l.id = lp.lesson_id
    JOIN users AS u ON u.id = lp.user_id
    JOIN courses AS c ON c.id = l.course_id
    WHERE c.id = :course_id
      AND c.mentor_id = :mentor_id
      AND l.status = 'PUBLISHED'
      AND u.role = 'STUDENT'
      AND lp.last_accessed_at IS NOT NULL
    GROUP BY lp.user_id, lp.lesson_id
)
SELECT
    COUNT(*) AS tracked_lesson_accesses,
    COUNT(DISTINCT user_id) AS students_with_activity,
    MAX(last_accessed_at) AS last_activity_at
FROM activity_by_student_lesson
"""
