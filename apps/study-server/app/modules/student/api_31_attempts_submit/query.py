LOCK_SUBMIT_ATTEMPT = """
SELECT a.id, a.quiz_id, a.user_id, a.status, a.started_at, q.passing_score
FROM quiz_attempts a
JOIN quizzes q ON q.id = a.quiz_id
WHERE a.id = :attempt_id
FOR UPDATE OF a
"""

LIST_QUIZ_QUESTIONS = """
SELECT id, question_type, score
FROM quiz_questions
WHERE quiz_id = :quiz_id
ORDER BY sort_order ASC, id ASC
"""

LIST_QUESTION_CHOICES = """
SELECT id
FROM quiz_choices
WHERE question_id = :question_id AND is_correct IS TRUE
ORDER BY id ASC
"""

LIST_ATTEMPT_ANSWERS = """
SELECT id, question_id, choice_id
FROM quiz_answers
WHERE attempt_id = :attempt_id
ORDER BY question_id ASC, id ASC
"""

MARK_QUESTION_ANSWERS = """
UPDATE quiz_answers
SET is_correct = :is_correct, score_received = 0
WHERE attempt_id = :attempt_id AND question_id = :question_id
"""

SET_QUESTION_SCORE = """
UPDATE quiz_answers
SET score_received = :score
WHERE id = (
    SELECT MIN(id) FROM quiz_answers
    WHERE attempt_id = :attempt_id AND question_id = :question_id
)
"""

FINALIZE_ATTEMPT = """
UPDATE quiz_attempts
SET status = 'GRADED', submitted_at = :submitted_at, score = :score
WHERE id = :attempt_id AND user_id = :user_id AND status = 'IN_PROGRESS'
RETURNING id, quiz_id, status, started_at, submitted_at, score
"""

LIST_GRADED_ANSWERS = """
SELECT q.id AS question_id,
       COALESCE(array_agg(a.choice_id ORDER BY a.id) FILTER (WHERE a.choice_id IS NOT NULL), ARRAY[]::BIGINT[]) AS choice_ids,
       CASE WHEN COUNT(a.id) = 0 THEN NULL ELSE BOOL_AND(a.is_correct) END AS correct,
       CASE WHEN COUNT(a.id) = 0 THEN NULL ELSE SUM(a.score_received) END AS score
FROM quiz_questions q
LEFT JOIN quiz_answers a ON a.question_id = q.id AND a.attempt_id = :attempt_id
WHERE q.quiz_id = :quiz_id
GROUP BY q.id, q.sort_order
ORDER BY q.sort_order ASC, q.id ASC
"""
