"""Câu SQL tĩnh cập nhật metadata candidate cho API #75."""

UPDATE_ADMIN_COURSE_METADATA = """
UPDATE courses
SET
    name = :title,
    description = :description,
    thumbnail_url = :thumbnail_url,
    price = :price,
    updated_at = CURRENT_TIMESTAMP
WHERE id = :course_id
RETURNING id
"""
