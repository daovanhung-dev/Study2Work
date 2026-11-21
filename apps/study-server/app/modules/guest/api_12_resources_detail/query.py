RESOURCE_BY_ID = """
SELECT
    r.id,
    r.lesson_id,
    r.name,
    r.resource_type AS type,
    r.url,
    r.visibility,
    r.storage_key
FROM resources AS r
WHERE r.id = :resource_id
LIMIT 1
"""

PUBLISHED_PARENT_COURSE = """
SELECT
    l.id AS lesson_id,
    l.course_id,
    c.id AS course_id,
    c.status AS course_status
FROM lessons AS l
JOIN courses AS c ON c.id = l.course_id
WHERE l.id = :lesson_id
  AND l.status IS DISTINCT FROM 'DELETED'
  AND c.status = 'PUBLISHED'
LIMIT 1
"""

ACTIVE_COURSE_ENROLLMENT = """
SELECT 1
FROM enrollments AS e
WHERE e.user_id = :user_id
  AND e.course_id = :course_id
  AND e.status = 'ACTIVE'
LIMIT 1
"""
