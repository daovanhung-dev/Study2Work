FIND_ORDER_COURSE = """
SELECT id, price, status
FROM courses
WHERE id = :course_id
LIMIT 1
"""

INSERT_ORDER = """
INSERT INTO orders (user_id, course_id, amount, currency, payment_provider, status)
VALUES (:user_id, :course_id, :amount, 'VND', :payment_provider, 'PENDING')
RETURNING id, course_id, user_id, amount, currency, status, created_at
"""
