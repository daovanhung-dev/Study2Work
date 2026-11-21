"""Câu SQL tĩnh đọc Submission và course scope cho API #55."""

FIND_MENTOR_SUBMISSION = """
SELECT
    s.id,
    s.assignment_id,
    s.user_id,
    s.content,
    s.status,
    s.submitted_at,
    s.score,
    s.feedback,
    a.id AS matched_assignment_id,
    a.course_id,
    c.id AS matched_course_id,
    c.mentor_id
FROM assignment_submissions AS s
LEFT JOIN assignments AS a ON a.id = s.assignment_id
LEFT JOIN courses AS c ON c.id = a.course_id
WHERE s.id = :submission_id
LIMIT 1
"""
