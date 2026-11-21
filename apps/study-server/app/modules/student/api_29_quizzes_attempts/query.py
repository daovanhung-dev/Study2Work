"""Các câu lệnh SQL cho API #29 tạo lượt làm bài kiểm tra."""

FIND_QUIZ_BY_ID = """
SELECT
    q.id,
    q.course_id,
    q.status
FROM quizzes AS q
WHERE q.id = :quiz_id
LIMIT 1
"""

FIND_ACTIVE_ATTEMPT = """
SELECT
    qa.id,
    qa.quiz_id,
    qa.user_id,
    qa.status,
    qa.started_at
FROM quiz_attempts AS qa
WHERE qa.quiz_id = :quiz_id
  AND qa.user_id = :user_id
  AND qa.status = 'IN_PROGRESS'
LIMIT 1
"""

INSERT_QUIZ_ATTEMPT = """
INSERT INTO quiz_attempts (
    quiz_id,
    user_id,
    started_at,
    status
)
VALUES (
    :quiz_id,
    :user_id,
    :started_at,
    'IN_PROGRESS'
)
RETURNING id, quiz_id, status, started_at, submitted_at, score
"""

