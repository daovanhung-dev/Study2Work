"""Hằng số truy vấn SQL cho API #21 lấy tiến độ tổng hợp."""

FIND_USER_COURSE_PROGRESS_ROWS = """
SELECT
    e.course_id,
    c.name AS course_name,
    e.status AS enrollment_status,
    COUNT(DISTINCT l.id) FILTER (WHERE l.status = 'PUBLISHED') AS total_lessons,
    COUNT(DISTINCT lp.lesson_id) FILTER (
        WHERE l.status = 'PUBLISHED' AND lp.status = 'COMPLETED'
    ) AS completed_lessons
FROM enrollments AS e
JOIN courses AS c ON c.id = e.course_id
LEFT JOIN lessons AS l ON l.course_id = e.course_id
LEFT JOIN lesson_progress AS lp
    ON lp.lesson_id = l.id AND lp.user_id = e.user_id
WHERE e.user_id = :user_id
  AND (CAST(:course_id AS BIGINT) IS NULL OR e.course_id = CAST(:course_id AS BIGINT))
GROUP BY e.course_id, c.name, e.status, e.enrolled_at
ORDER BY e.enrolled_at DESC, e.course_id DESC
"""
