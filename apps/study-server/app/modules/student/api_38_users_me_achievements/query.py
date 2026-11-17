COUNT_ACHIEVEMENTS = """
SELECT COUNT(*) AS total FROM user_achievements
WHERE user_id = :user_id AND (CAST(:course_id AS BIGINT) IS NULL OR course_id = CAST(:course_id AS BIGINT))
"""

LIST_ACHIEVEMENTS = """
SELECT id, achievement_code AS code, title, awarded_at, course_id
FROM user_achievements
WHERE user_id = :user_id AND (CAST(:course_id AS BIGINT) IS NULL OR course_id = CAST(:course_id AS BIGINT))
ORDER BY awarded_at DESC, id DESC
"""
