ASSIGNMENT_BY_ID = """
SELECT
    a.id,
    a.course_id,
    a.name AS title,
    a.description,
    a.due_at,
    a.max_score
FROM assignments AS a
WHERE a.id = :assignment_id
LIMIT 1
"""
