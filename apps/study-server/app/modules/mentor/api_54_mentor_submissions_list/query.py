"""Câu SQL tĩnh kiểm tra quyền course và đọc Submission cho API #54."""

FIND_MENTOR_COURSE = """
SELECT
    id,
    mentor_id
FROM courses
WHERE id = :course_id
LIMIT 1
"""

COUNT_MENTOR_SUBMISSIONS = """
SELECT COUNT(*) AS total
FROM assignment_submissions AS s
JOIN assignments AS a ON a.id = s.assignment_id
JOIN courses AS c ON c.id = a.course_id
JOIN users AS student ON student.id = s.user_id
WHERE c.mentor_id = :mentor_id
  AND (CAST(:course_id AS BIGINT) IS NULL OR a.course_id = CAST(:course_id AS BIGINT))
  AND (CAST(:status AS VARCHAR) IS NULL OR s.status = CAST(:status AS VARCHAR))
"""

LIST_MENTOR_SUBMISSIONS = """
SELECT
    s.id,
    s.assignment_id,
    s.user_id,
    s.content,
    s.status,
    s.submitted_at,
    s.score,
    s.feedback
FROM assignment_submissions AS s
JOIN assignments AS a ON a.id = s.assignment_id
JOIN courses AS c ON c.id = a.course_id
JOIN users AS student ON student.id = s.user_id
WHERE c.mentor_id = :mentor_id
  AND (CAST(:course_id AS BIGINT) IS NULL OR a.course_id = CAST(:course_id AS BIGINT))
  AND (CAST(:status AS VARCHAR) IS NULL OR s.status = CAST(:status AS VARCHAR))
ORDER BY s.submitted_at DESC, s.id DESC
LIMIT :limit OFFSET :offset
"""
