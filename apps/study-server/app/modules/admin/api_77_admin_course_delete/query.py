"""SQL constants khóa course, kiểm tra dependency và soft-delete API #77."""

LOCK_ADMIN_COURSE_FOR_DELETE = """
SELECT id
FROM courses
WHERE id = :course_id
  AND status IS DISTINCT FROM 'DELETED'
FOR UPDATE
"""

CHECK_ADMIN_COURSE_DELETE_DEPENDENCIES = """
SELECT
    EXISTS (
        SELECT 1
        FROM enrollments AS enrollment
        WHERE enrollment.course_id = :course_id
    ) AS has_enrollments,
    (
        EXISTS (
            SELECT 1
            FROM contents AS content
            WHERE content.course_id = :course_id
              AND content.deleted_at IS NULL
        )
        OR EXISTS (
            SELECT 1
            FROM lessons AS lesson
            WHERE lesson.course_id = :course_id
        )
        OR EXISTS (
            SELECT 1
            FROM quizzes AS quiz
            WHERE quiz.course_id = :course_id
        )
        OR EXISTS (
            SELECT 1
            FROM assignments AS assignment
            WHERE assignment.course_id = :course_id
        )
    ) AS has_content
"""

SOFT_DELETE_ADMIN_COURSE = """
UPDATE courses
SET
    status = 'DELETED',
    updated_at = CURRENT_TIMESTAMP
WHERE id = :course_id
  AND status IS DISTINCT FROM 'DELETED'
RETURNING
    id,
    updated_at AS deleted_at
"""
