"""Câu SQL tĩnh đếm và đọc trang Quiz cho API #87."""

COUNT_ADMIN_QUIZZES = """
SELECT COUNT(*) AS total
FROM quizzes AS q
WHERE q.status IS DISTINCT FROM 'DELETED'
  AND (CAST(:course_id AS BIGINT) IS NULL OR q.course_id = CAST(:course_id AS BIGINT))
  AND (CAST(:status AS VARCHAR) IS NULL OR q.status = CAST(:status AS VARCHAR))
"""

LIST_ADMIN_QUIZZES = """
SELECT
    q.id,
    q.course_id,
    q.name AS title,
    q.time_limit_minutes AS duration_minutes,
    q.passing_score
FROM quizzes AS q
WHERE q.status IS DISTINCT FROM 'DELETED'
  AND (CAST(:course_id AS BIGINT) IS NULL OR q.course_id = CAST(:course_id AS BIGINT))
  AND (CAST(:status AS VARCHAR) IS NULL OR q.status = CAST(:status AS VARCHAR))
ORDER BY q.id ASC
LIMIT :limit OFFSET :offset
"""
