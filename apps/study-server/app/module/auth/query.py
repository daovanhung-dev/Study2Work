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
