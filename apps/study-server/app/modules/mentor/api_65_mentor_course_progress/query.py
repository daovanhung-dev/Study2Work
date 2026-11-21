"""Các câu SQL tĩnh truy vấn course owner và aggregate progress cho API #65."""

FIND_MENTOR_COURSE = """
SELECT
    id,
    mentor_id
FROM courses
WHERE id = :course_id
LIMIT 1
"""

LIST_ACTIVE_STUDENT_PROGRESS = """
WITH course_students AS (
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
),
published_lessons AS (
    SELECT l.id
    FROM lessons AS l
    WHERE l.course_id = :course_id
      AND l.status = 'PUBLISHED'
),
latest_progress AS (
    SELECT DISTINCT ON (lp.user_id, lp.lesson_id)
        lp.user_id,
        lp.lesson_id,
        lp.status,
        lp.progress_percent
    FROM lesson_progress AS lp
    JOIN published_lessons AS pl ON pl.id = lp.lesson_id
    ORDER BY
        lp.user_id,
        lp.lesson_id,
        lp.last_accessed_at DESC NULLS LAST,
        lp.id DESC
),
progress_by_student AS (
    SELECT
        cs.id AS student_id,
        COUNT(*) FILTER (WHERE lp.status = 'COMPLETED') AS completed_lessons,
        COALESCE(SUM(COALESCE(lp.progress_percent, 0)), 0) AS progress_sum,
        COUNT(*) FILTER (
            WHERE lp.user_id IS NOT NULL
              AND (
                  lp.status IS NULL
                  OR lp.status NOT IN ('NOT_STARTED', 'IN_PROGRESS', 'COMPLETED')
                  OR lp.progress_percent < 0
                  OR lp.progress_percent > 100
              )
        ) AS invalid_progress_count
    FROM course_students AS cs
    CROSS JOIN published_lessons AS pl
    LEFT JOIN latest_progress AS lp
        ON lp.user_id = cs.id
       AND lp.lesson_id = pl.id
    GROUP BY cs.id
),
lesson_total AS (
    SELECT COUNT(*) AS total_lessons
    FROM published_lessons
)
SELECT
    cs.id AS student_id,
    cs.full_name,
    cs.avatar_url,
    lt.total_lessons,
    COALESCE(pbs.completed_lessons, 0) AS completed_lessons,
    COALESCE(pbs.progress_sum, 0) AS progress_sum,
    COALESCE(pbs.invalid_progress_count, 0) AS invalid_progress_count
FROM course_students AS cs
CROSS JOIN lesson_total AS lt
LEFT JOIN progress_by_student AS pbs ON pbs.student_id = cs.id
ORDER BY cs.id ASC
"""
