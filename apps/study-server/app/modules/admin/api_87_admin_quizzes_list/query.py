"""Câu SQL tĩnh đếm và đọc trang Quiz cho API #87."""

COUNT_ADMIN_QUIZZES = """
SELECT COUNT(*) AS total
FROM quizzes AS q
WHERE q.status IS DISTINCT FROM 'DELETED'
  AND (:course_id IS NULL OR q.course_id = :course_id)
  AND (:status IS NULL OR q.status = :status)
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
  AND (:course_id IS NULL OR q.course_id = :course_id)
  AND (:status IS NULL OR q.status = :status)
ORDER BY q.id ASC
LIMIT :limit OFFSET :offset
"""
