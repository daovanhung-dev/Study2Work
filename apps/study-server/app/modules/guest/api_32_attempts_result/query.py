"""Các câu SQL chỉ đọc dữ liệu attempt và câu trả lời cho API #32."""

ATTEMPT_RESULT_BY_ID = """
SELECT
    a.id,
    a.quiz_id,
    a.status,
    a.started_at,
    a.submitted_at,
    a.score
FROM quiz_attempts AS a
WHERE a.id = :attempt_id
  AND a.user_id = :user_id
LIMIT 1
"""

ATTEMPT_ANSWERS_BY_ID = """
SELECT
    ans.question_id,
    ans.choice_id,
    ans.is_correct AS correct,
    ans.score_received AS score
FROM quiz_answers AS ans
JOIN quiz_attempts AS a ON a.id = ans.attempt_id
WHERE a.id = :attempt_id
  AND a.user_id = :user_id
"""