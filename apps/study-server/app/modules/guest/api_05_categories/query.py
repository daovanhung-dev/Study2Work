ACTIVE_CATEGORIES = """
SELECT
    c.id,
    c.name,
    c.slug,
    c.description
FROM categories AS c
WHERE c.status = :status
  AND c.locale = :locale
ORDER BY c.id ASC
"""
