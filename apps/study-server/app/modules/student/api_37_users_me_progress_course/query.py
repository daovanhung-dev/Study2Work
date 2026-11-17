COURSE_LESSON_PROGRESS = """
SELECT c.id AS course_id,
       COUNT(l.id)::BIGINT AS total_lessons,
       COUNT(l.id) FILTER (WHERE EXISTS (
           SELECT 1 FROM lesson_progress p
           WHERE p.lesson_id = l.id AND p.user_id = :user_id
             AND (p.status = 'COMPLETED' OR p.completed_at IS NOT NULL)
       ))::BIGINT AS completed_lessons
FROM courses c
LEFT JOIN lessons l ON l.course_id = c.id AND l.status = 'PUBLISHED'
JOIN enrollments e ON e.course_id = c.id AND e.user_id = :user_id AND e.status = 'ACTIVE'
WHERE c.id = :course_id
GROUP BY c.id
"""
