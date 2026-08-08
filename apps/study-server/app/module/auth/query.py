CREATE_USER = """
INSERT INTO users (
    id,
    display_name,
    email,
    phone,
    created_at,
    updated_at
)
VALUES (
    :id,
    :display_name,
    :email,
    :phone,
    :created_at,
    :updated_at
)
RETURNING id;
"""

CREATE_AUTH_CREDENTIAL = """
INSERT INTO auth_credentials (
    user_id,
    password_hash,
    password_algorithm,
    password_login_enabled,
    must_change_password,
    failed_login_attempts,
    locked_until,
    password_changed_at,
    last_login_at,
    created_at,
    updated_at
)
VALUES (
    :user_id,
    :password_hash,
    :password_algorithm,
    :password_login_enabled,
    :must_change_password,
    :failed_login_attempts,
    :locked_until,
    :password_changed_at,
    :last_login_at,
    :created_at,
    :updated_at
);
"""

GET_LOGIN_USER = """
SELECT
    u.id::text AS id,
    u.display_name,
    u.email,
    u.phone,
    u.account_status::text AS account_status,
    u.contact_verified,
    ac.password_hash,
    ac.password_algorithm,
    ac.password_login_enabled,
    ac.must_change_password,
    ac.failed_login_attempts,
    ac.locked_until
FROM users AS u
INNER JOIN auth_credentials AS ac
    ON ac.user_id = u.id
WHERE
    LOWER(u.email) = LOWER(:identifier)
    OR u.phone = :identifier
LIMIT 1;
"""

GET_USER_BY_ID = """
SELECT
    u.id::text AS id,
    u.display_name,
    u.email,
    u.phone,
    u.account_status::text AS account_status,
    u.contact_verified
FROM users AS u
WHERE u.id = :user_id
LIMIT 1;
"""

GET_USER_ROLES = """
SELECT r.code
FROM user_roles AS ur
INNER JOIN roles AS r
    ON r.id = ur.role_id
WHERE
    ur.user_id = :user_id
    AND r.active = TRUE
ORDER BY r.code;
"""

MARK_LOGIN_SUCCESS = """
UPDATE auth_credentials
SET
    failed_login_attempts = 0,
    locked_until = NULL,
    last_login_at = CURRENT_TIMESTAMP,
    updated_at = CURRENT_TIMESTAMP
WHERE user_id = :user_id;
"""
