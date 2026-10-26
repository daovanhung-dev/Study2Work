"""Các câu SQL tĩnh đọc quyền course, Student đủ điều kiện và lesson progress API #67."""

FIND_MENTOR_COURSE = """
SELECT
    id,
    mentor_id
FROM courses
WHERE id = :course_id
LIMIT 1
"""

FIND_ACTIVE_STUDENT = """
SELECT DISTINCT
    u.id,
    u.full_name,
    u.avatar_url
FROM enrollments AS e
JOIN courses AS c ON c.id = e.course_id
JOIN users AS u ON u.id = e.user_id
WHERE c.id = :course_id
  AND c.mentor_id = :mentor_id
  AND e.status = 'ACTIVE'
  AND u.role = 'STUDENT'
  AND u.id = :student_id
LIMIT 1
"""

LIST_STUDENT_LESSON_PROGRESS = """
WITH course_students AS (
    SELECT DISTINCT u.id
    FROM enrollments AS e
    JOIN courses AS c ON c.id = e.course_id
    JOIN users AS u ON u.id = e.user_id
    WHERE c.id = :course_id
      AND c.mentor_id = :mentor_id
      AND e.status = 'ACTIVE'
      AND u.role = 'STUDENT'
      AND u.id = :student_id
),
published_lessons AS (
    SELECT
        l.id,
        l.name AS title,
        l.sort_order AS lesson_order
    FROM lessons AS l
    WHERE l.course_id = :course_id
      AND l.status = 'PUBLISHED'
),
latest_progress AS (
    SELECT DISTINCT ON (lp.user_id, lp.lesson_id)
        lp.id,
        lp.user_id,
        lp.lesson_id,
        lp.status,
        lp.progress_percent,
        lp.last_accessed_at,
        lp.completed_at
    FROM lesson_progress AS lp
    JOIN published_lessons AS pl ON pl.id = lp.lesson_id
    WHERE lp.user_id = :student_id
    ORDER BY
        lp.user_id,
        lp.lesson_id,
        lp.last_accessed_at DESC NULLS LAST,
        lp.id DESC
)
SELECT
    pl.id AS lesson_id,
    pl.title,
    pl.lesson_order AS "order",
    CASE
        WHEN lp.id IS NULL THEN 'NOT_STARTED'
        ELSE lp.status
    END AS progress_status,
    CASE
        WHEN lp.id IS NULL THEN 0
        ELSE lp.progress_percent
    END AS progress_percent,
    lp.last_accessed_at,
    lp.completed_at
FROM course_students AS cs
CROSS JOIN published_lessons AS pl
LEFT JOIN latest_progress AS lp
    ON lp.user_id = cs.id
   AND lp.lesson_id = pl.id
ORDER BY pl.lesson_order ASC, pl.id ASC
"""
