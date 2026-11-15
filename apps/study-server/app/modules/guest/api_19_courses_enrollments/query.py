LOCK_ENROLLMENT_COURSE = """
SELECT id, price, status
FROM courses
WHERE id = :course_id
FOR UPDATE
"""

FIND_ACTIVE_ENROLLMENT = """
SELECT id FROM enrollments
WHERE user_id = :user_id AND course_id = :course_id AND status = 'ACTIVE'
LIMIT 1
"""

FIND_PAID_ORDER = """
SELECT id FROM orders
WHERE user_id = :user_id AND course_id = :course_id AND status = 'PAID'
ORDER BY created_at DESC, id DESC
LIMIT 1
"""

INSERT_ENROLLMENT = """
INSERT INTO enrollments (user_id, course_id, status, enrolled_at)
VALUES (:user_id, :course_id, 'ACTIVE', CURRENT_TIMESTAMP)
RETURNING id, course_id, user_id, status, enrolled_at, completed_at
"""

INSERT_INITIAL_LESSON_PROGRESS = """
INSERT INTO lesson_progress (user_id, lesson_id, status, progress_percent)
SELECT :user_id, l.id, 'NOT_STARTED', 0
FROM lessons AS l
WHERE l.course_id = :course_id AND l.status = 'PUBLISHED'
"""
