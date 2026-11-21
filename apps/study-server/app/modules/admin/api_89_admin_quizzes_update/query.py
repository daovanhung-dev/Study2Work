"""Câu SQL tĩnh khóa Quiz, kiểm tra lịch sử và thay question set cho API #89."""

LOCK_ADMIN_QUIZ = """
SELECT q.id, q.status
FROM quizzes AS q
WHERE q.id = :quiz_id
  AND q.status IS DISTINCT FROM 'DELETED'
FOR UPDATE OF q
"""

LOCK_ADMIN_QUIZ_QUESTIONS = """
SELECT question.id
FROM quiz_questions AS question
WHERE question.quiz_id = :quiz_id
ORDER BY question.id ASC
FOR UPDATE OF question
"""

LOCK_ADMIN_QUIZ_CHOICES = """
SELECT choice.id
FROM quiz_choices AS choice
JOIN quiz_questions AS question ON question.id = choice.question_id
WHERE question.quiz_id = :quiz_id
ORDER BY choice.id ASC
FOR UPDATE OF choice
"""

CHECK_ADMIN_QUIZ_HISTORY = """
SELECT
    EXISTS (
        SELECT 1
        FROM quiz_attempts AS attempt
        WHERE attempt.quiz_id = :quiz_id
    ) AS has_attempts,
    EXISTS (
        SELECT 1
        FROM quiz_answers AS answer
        WHERE answer.question_id IN (
            SELECT question.id
            FROM quiz_questions AS question
            WHERE question.quiz_id = :quiz_id
        )
        OR answer.choice_id IN (
            SELECT choice.id
            FROM quiz_choices AS choice
            JOIN quiz_questions AS question ON question.id = choice.question_id
            WHERE question.quiz_id = :quiz_id
        )
    ) AS has_answers
"""

LOCK_ADMIN_QUIZ_COURSE = """
SELECT course.id
FROM courses AS course
WHERE course.id = :course_id
FOR KEY SHARE OF course
"""

UPDATE_ADMIN_QUIZ = """
UPDATE quizzes
SET course_id = :course_id,
    name = :title,
    passing_score = :passing_score,
    time_limit_minutes = :duration_minutes,
    updated_at = CURRENT_TIMESTAMP
WHERE id = :quiz_id
  AND status IS DISTINCT FROM 'DELETED'
RETURNING
    id,
    course_id,
    name AS title,
    time_limit_minutes AS duration_minutes,
    passing_score
"""

DELETE_ADMIN_QUIZ_CHOICES = """
DELETE FROM quiz_choices AS choice
USING quiz_questions AS question
WHERE choice.question_id = question.id
  AND question.quiz_id = :quiz_id
RETURNING choice.id
"""

DELETE_ADMIN_QUIZ_QUESTIONS = """
DELETE FROM quiz_questions AS question
WHERE question.quiz_id = :quiz_id
RETURNING question.id
"""
