"""SQL constants khóa, kiểm tra history và xóa Quiz cho API #90."""

LOCK_ADMIN_QUIZ_FOR_DELETE = """
SELECT id, status, updated_at
FROM quizzes
WHERE id = :quiz_id
FOR UPDATE
"""

LOCK_ADMIN_QUIZ_QUESTIONS_FOR_DELETE = """
SELECT question.id
FROM quiz_questions AS question
WHERE question.quiz_id = :quiz_id
ORDER BY question.id ASC
FOR UPDATE OF question
"""

LOCK_ADMIN_QUIZ_CHOICES_FOR_DELETE = """
SELECT choice.id
FROM quiz_choices AS choice
JOIN quiz_questions AS question ON question.id = choice.question_id
WHERE question.quiz_id = :quiz_id
ORDER BY choice.id ASC
FOR UPDATE OF choice
"""

CHECK_ADMIN_QUIZ_DELETE_HISTORY = """
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

SOFT_DELETE_ADMIN_QUIZ = """
UPDATE quizzes
SET
    status = 'DELETED',
    updated_at = CURRENT_TIMESTAMP
WHERE id = :quiz_id
  AND status IS DISTINCT FROM 'DELETED'
RETURNING
    id,
    updated_at AS deleted_at
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

DELETE_ADMIN_QUIZ = """
DELETE FROM quizzes
WHERE id = :quiz_id
RETURNING id, CURRENT_TIMESTAMP AS deleted_at
"""
