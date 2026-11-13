FIND_COURSE = """
SELECT
    c.id,
    c.status
FROM courses AS c
WHERE c.id = :course_id
LIMIT 1
"""

FIND_USER_ENROLLMENT = """
SELECT
    e.id,
    e.user_id,
    e.course_id,
    e.status,
    e.enrolled_at,
    e.completed_at
FROM enrollments AS e
WHERE e.course_id = :course_id
  AND e.user_id = :user_id
ORDER BY e.id DESC
LIMIT 1
"""

FIND_ANY_ENROLLMENT_BY_COURSE = """
SELECT
    e.id,
    e.user_id,
    e.course_id,
    e.status,
    e.enrolled_at,
    e.completed_at
FROM enrollments AS e
WHERE e.course_id = :course_id
ORDER BY e.id DESC
LIMIT 1
"""