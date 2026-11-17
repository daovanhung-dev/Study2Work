FIND_PUBLISHED_COURSE = """
SELECT
    c.id,
    c.status
FROM courses AS c
WHERE c.id = :course_id
  AND c.status = 'PUBLISHED'
LIMIT 1
"""

FIND_COURSE_RESOURCES = """
SELECT
    r.id,
    r.lesson_id,
    r.name,
    r.resource_type,
    r.url
FROM lessons AS l
INNER JOIN resources AS r ON r.lesson_id = l.id
WHERE l.course_id = :course_id
ORDER BY r.id ASC
"""