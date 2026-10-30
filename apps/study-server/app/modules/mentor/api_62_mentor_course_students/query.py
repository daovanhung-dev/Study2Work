"""Các câu SQL tĩnh kiểm tra course owner và đọc active Student roster API #62."""

FIND_MENTOR_COURSE = """
SELECT
    id,
    mentor_id
FROM courses
WHERE id = :course_id
LIMIT 1
"""

LIST_ACTIVE_COURSE_STUDENTS = """
SELECT DISTINCT
    u.id,
    u.full_name,
    u.avatar_url
FROM courses AS c
JOIN enrollments AS e ON e.course_id = c.id
JOIN users AS u ON u.id = e.user_id
WHERE c.id = :course_id
  AND c.mentor_id = :mentor_id
  AND e.status = 'ACTIVE'
  AND u.role = 'STUDENT'
ORDER BY u.id ASC
"""
