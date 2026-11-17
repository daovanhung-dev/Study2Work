"""Các câu lệnh SQL cho API #28 lấy chi tiết quiz và danh sách câu hỏi."""

FIND_QUIZ_BY_ID = """
SELECT
    q.id,
    q.course_id,
    q.name AS title,
    q.time_limit_minutes AS duration_minutes,
    q.passing_score,
    q.status
FROM quizzes AS q
WHERE q.id = :quiz_id
LIMIT 1
"""

FIND_QUIZ_QUESTIONS = """
SELECT
    qq.id,
    qq.quiz_id,
    qq.question_text AS text,
    qq.sort_order
FROM quiz_questions AS qq
WHERE qq.quiz_id = :quiz_id
ORDER BY qq.sort_order ASC, qq.id ASC
"""

FIND_QUIZ_CHOICES = """
SELECT
    qc.id,
    qc.question_id,
    qc.choice_text
FROM quiz_choices AS qc
JOIN quiz_questions AS qq ON qq.id = qc.question_id
WHERE qq.quiz_id = :quiz_id
ORDER BY qc.id ASC
"""

