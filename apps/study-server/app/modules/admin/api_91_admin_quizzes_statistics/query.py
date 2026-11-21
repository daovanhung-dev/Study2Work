"""Câu SQL tổng hợp số lượt làm và điểm Quiz cho API #91."""

GET_ADMIN_QUIZ_STATISTICS = """
SELECT
    quiz.id AS quiz_id,
    quiz.passing_score,
    COUNT(attempt.id)::bigint AS attempt_count,
    COUNT(attempt.submitted_at)::bigint AS submitted_attempt_count,
    COUNT(attempt.score)::bigint AS graded_attempt_count,
    AVG(attempt.score) AS average_score,
    CASE
        WHEN quiz.passing_score IS NULL THEN NULL
        ELSE COUNT(attempt.id) FILTER (
            WHERE attempt.score IS NOT NULL
              AND attempt.score >= quiz.passing_score
        )::bigint
    END AS passed_attempt_count,
    CASE
        WHEN quiz.passing_score IS NULL OR COUNT(attempt.score) = 0 THEN NULL
        ELSE 100.0 * COUNT(attempt.id) FILTER (
            WHERE attempt.score IS NOT NULL
              AND attempt.score >= quiz.passing_score
        ) / NULLIF(COUNT(attempt.score), 0)
    END AS pass_rate_percent
FROM quizzes AS quiz
LEFT JOIN quiz_attempts AS attempt ON attempt.quiz_id = quiz.id
WHERE quiz.id = :quiz_id
GROUP BY quiz.id, quiz.passing_score
"""
