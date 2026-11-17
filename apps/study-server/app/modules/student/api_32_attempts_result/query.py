"""Các câu SQL chỉ đọc dữ liệu attempt và câu trả lời cho API #32."""

ATTEMPT_RESULT_BY_ID = """
SELECT
    a.id,
    a.quiz_id,
    a.status,
    a.started_at,
    a.submitted_at,
    a.score,
    q.passing_score,
    (
        SELECT COALESCE(SUM(question.score), 0)
        FROM quiz_questions AS question
        WHERE question.quiz_id = a.quiz_id
    ) AS possible_points
FROM quiz_attempts AS a
JOIN quizzes AS q ON q.id = a.quiz_id
WHERE a.id = :attempt_id
  AND a.user_id = :user_id
LIMIT 1
"""

ATTEMPT_ANSWERS_BY_ID = """
SELECT q.id AS question_id,
       COALESCE(array_agg(ans.choice_id ORDER BY ans.id) FILTER (WHERE ans.choice_id IS NOT NULL), ARRAY[]::BIGINT[]) AS choice_ids,
       CASE WHEN COUNT(ans.id) = 0 THEN NULL ELSE BOOL_AND(ans.is_correct) END AS correct,
       CASE WHEN COUNT(ans.id) = 0 THEN NULL ELSE SUM(ans.score_received) END AS score
FROM quiz_attempts AS a
JOIN quiz_questions AS q ON q.quiz_id = a.quiz_id
LEFT JOIN quiz_answers AS ans ON ans.attempt_id = a.id AND ans.question_id = q.id
WHERE a.id = :attempt_id AND a.user_id = :user_id
GROUP BY q.id, q.sort_order
ORDER BY q.sort_order ASC, q.id ASC
"""
