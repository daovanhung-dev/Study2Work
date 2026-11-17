COUNT_USER_COURSES = """
SELECT COUNT(*) AS total
FROM enrollments e JOIN courses c ON c.id = e.course_id
WHERE e.user_id = :user_id AND (CAST(:status AS VARCHAR) IS NULL OR e.status = CAST(:status AS VARCHAR))
"""

LIST_USER_COURSES = """
SELECT c.id AS course_id, c.name, c.description, c.thumbnail_url, c.price,
       c.status AS course_status, e.status AS enrollment_status, e.enrolled_at
FROM enrollments e JOIN courses c ON c.id = e.course_id
WHERE e.user_id = :user_id AND (CAST(:status AS VARCHAR) IS NULL OR e.status = CAST(:status AS VARCHAR))
ORDER BY e.enrolled_at DESC, e.id DESC
LIMIT :limit OFFSET :offset
"""
