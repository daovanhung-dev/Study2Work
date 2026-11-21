"""Câu SQL tĩnh để kiểm tra Course và tạo Quiz, Question, Choice cho API #88."""

SELECT_ADMIN_QUIZ_COURSE = """
SELECT c.id
FROM courses AS c
WHERE c.id = :course_id
"""

INSERT_ADMIN_QUIZ = """
INSERT INTO quizzes (
    course_id,
    name,
    passing_score,
    time_limit_minutes,
    created_at,
    updated_at
)
VALUES (
    :course_id,
    :title,
    :passing_score,
    :duration_minutes,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
)
RETURNING
    id,
    course_id,
    name AS title,
    time_limit_minutes AS duration_minutes,
    passing_score
"""

INSERT_ADMIN_QUIZ_QUESTION = """
INSERT INTO quiz_questions (
    quiz_id,
    question_text,
    question_type,
    sort_order
)
VALUES (
    :quiz_id,
    :text,
    :question_type,
    :sort_order
)
RETURNING
    id,
    quiz_id,
    question_text AS text,
    question_type AS type,
    sort_order
"""

INSERT_ADMIN_QUIZ_CHOICE = """
INSERT INTO quiz_choices (
    question_id,
    choice_text,
    is_correct,
    sort_order
)
VALUES (
    :question_id,
    :text,
    :is_correct,
    :sort_order
)
RETURNING
    id,
    question_id,
    choice_text AS text,
    is_correct,
    sort_order
"""
