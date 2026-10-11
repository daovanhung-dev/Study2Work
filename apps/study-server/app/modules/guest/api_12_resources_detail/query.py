RESOURCE_BY_ID = """
SELECT
    r.id,
    r.lesson_id,
    r.name,
    r.resource_type AS type,
    r.url
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
  AND c.status = 'PUBLISHED'
LIMIT 1
"""
