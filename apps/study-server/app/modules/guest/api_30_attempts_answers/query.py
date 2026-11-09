"""Các câu lệnh SQL cho API #30 autosave/lưu câu trả lời bài kiểm tra."""

FIND_ATTEMPT_BY_ID = """
SELECT
    qa.id,
    qa.quiz_id,
    qa.user_id,
    qa.status,
    qa.started_at,
    qa.submitted_at,
    qa.score
FROM quiz_attempts AS qa
WHERE qa.id = :attempt_id
LIMIT 1
"""

FIND_QUESTION_BY_ID = """
SELECT
    qq.id,
    qq.quiz_id
FROM quiz_questions AS qq
WHERE qq.id = :question_id
LIMIT 1
"""

FIND_EXISTING_ANSWER = """
SELECT
    id,
    attempt_id,
    question_id,
    choice_id
FROM quiz_answers
WHERE attempt_id = :attempt_id
  AND question_id = :question_id
LIMIT 1
"""

UPDATE_ANSWER = """
UPDATE quiz_answers
SET choice_id = :choice_id
WHERE id = :answer_id
"""

INSERT_ANSWER = """
INSERT INTO quiz_answers (
    attempt_id,
    question_id,
    choice_id,
    is_correct,
    score_received
)
VALUES (
    :attempt_id,
    :question_id,
    :choice_id,
    FALSE,
    0
)
"""

FIND_ATTEMPT_ANSWERS = """
SELECT
    question_id,
    choice_id
FROM quiz_answers
WHERE attempt_id = :attempt_id
ORDER BY id ASC
"""

