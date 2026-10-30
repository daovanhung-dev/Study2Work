"""Các câu SQL tĩnh đếm và đọc Discussion trong hàng chờ report API #97."""

COUNT_ADMIN_REPORTED_DISCUSSIONS = """
SELECT COUNT(DISTINCT d.id)::BIGINT AS total
FROM discussions AS d
JOIN discussion_reports AS r ON r.discussion_id = d.id
WHERE r.status IN ('OPEN', 'IN_REVIEW')
  AND (:reason IS NULL OR r.reason_code = :reason)
  AND (:severity IS NULL OR r.severity = :severity)
"""

LIST_ADMIN_REPORTED_DISCUSSIONS = """
WITH latest_matching_reports AS (
    SELECT DISTINCT ON (r.discussion_id)
        r.discussion_id,
        r.created_at
    FROM discussion_reports AS r
    WHERE r.status IN ('OPEN', 'IN_REVIEW')
      AND (:reason IS NULL OR r.reason_code = :reason)
      AND (:severity IS NULL OR r.severity = :severity)
    ORDER BY r.discussion_id, r.created_at DESC, r.id DESC
)
SELECT
    d.id,
    d.course_id,
    d.content,
    d.status,
    u.id AS author_id,
    u.full_name AS author_full_name,
    u.avatar_url AS author_avatar_url,
    r.created_at AS latest_reported_at
FROM latest_matching_reports AS r
JOIN discussions AS d ON d.id = r.discussion_id
LEFT JOIN users AS u ON u.id = d.user_id
ORDER BY r.created_at DESC, d.id DESC
LIMIT :limit OFFSET :offset
"""
