-- DB Admin control plane. This script is intentionally independent from the
-- Study/Work business schema and contains no passwords or live credentials.

CREATE SCHEMA IF NOT EXISTS db_admin;
REVOKE ALL ON SCHEMA db_admin FROM PUBLIC;

CREATE TABLE IF NOT EXISTS db_admin.admin_users (
    user_id UUID PRIMARY KEY,
    username VARCHAR(64) NOT NULL,
    display_name VARCHAR(150) NOT NULL,
    password_hash TEXT NOT NULL,
    password_algorithm VARCHAR(16) NOT NULL DEFAULT 'argon2id',
    is_root BOOLEAN NOT NULL DEFAULT FALSE,
    status VARCHAR(16) NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'disabled')),
    must_change_password BOOLEAN NOT NULL DEFAULT TRUE,
    failed_login_attempts INTEGER NOT NULL DEFAULT 0
        CHECK (failed_login_attempts >= 0),
    locked_until TIMESTAMPTZ,
    last_login_at TIMESTAMPTZ,
    password_changed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX IF NOT EXISTS admin_users_username_key
    ON db_admin.admin_users (LOWER(username));

CREATE TABLE IF NOT EXISTS db_admin.admin_roles (
    role_id UUID PRIMARY KEY,
    role_key VARCHAR(64) NOT NULL UNIQUE,
    display_name VARCHAR(150) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS db_admin.admin_permissions (
    permission_id UUID PRIMARY KEY,
    permission_key VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(150) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS db_admin.admin_user_roles (
    user_id UUID NOT NULL REFERENCES db_admin.admin_users(user_id) ON DELETE CASCADE,
    role_id UUID NOT NULL REFERENCES db_admin.admin_roles(role_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);

CREATE TABLE IF NOT EXISTS db_admin.admin_role_permissions (
    role_id UUID NOT NULL REFERENCES db_admin.admin_roles(role_id) ON DELETE CASCADE,
    permission_id UUID NOT NULL REFERENCES db_admin.admin_permissions(permission_id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE IF NOT EXISTS db_admin.admin_user_schema_bindings (
    binding_id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES db_admin.admin_users(user_id) ON DELETE CASCADE,
    database_target VARCHAR(64) NOT NULL,
    schema_name VARCHAR(63) NOT NULL,
    postgres_role_name VARCHAR(63) NOT NULL,
    access_level VARCHAR(16) NOT NULL DEFAULT 'owner'
        CHECK (access_level IN ('owner', 'read_write', 'read_only')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, database_target, schema_name),
    UNIQUE (database_target, schema_name)
);

CREATE INDEX IF NOT EXISTS admin_user_schema_bindings_target_key
    ON db_admin.admin_user_schema_bindings (database_target, is_active);

CREATE TABLE IF NOT EXISTS db_admin.admin_audit_events (
    event_id UUID PRIMARY KEY,
    actor_user_id UUID,
    actor_username VARCHAR(64),
    database_target VARCHAR(64),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(64),
    resource_name VARCHAR(255),
    outcome VARCHAR(32) NOT NULL,
    trace_id VARCHAR(128) NOT NULL,
    sql_hash CHAR(64),
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS admin_audit_events_created_at_key
    ON db_admin.admin_audit_events (created_at DESC);

CREATE INDEX IF NOT EXISTS admin_audit_events_target_key
    ON db_admin.admin_audit_events (database_target, created_at DESC);

INSERT INTO db_admin.admin_roles (role_id, role_key, display_name)
VALUES
    ('00000000-0000-0000-0000-000000000001', 'root', 'DB Admin root'),
    ('00000000-0000-0000-0000-000000000002', 'developer', 'Scoped developer')
ON CONFLICT (role_key) DO UPDATE
SET display_name = EXCLUDED.display_name;

INSERT INTO db_admin.admin_permissions (permission_id, permission_key, display_name)
VALUES
    ('00000000-0000-0000-0000-000000000011', 'db_admin:read', 'Read catalog and audit'),
    ('00000000-0000-0000-0000-000000000012', 'db_admin:sql', 'Validate and execute SQL'),
    ('00000000-0000-0000-0000-000000000013', 'db_admin:write', 'Use legacy write operations'),
    ('00000000-0000-0000-0000-000000000014', 'db_admin:manage', 'Manage accounts and grants')
ON CONFLICT (permission_key) DO UPDATE
SET display_name = EXCLUDED.display_name;

INSERT INTO db_admin.admin_role_permissions (role_id, permission_id)
SELECT r.role_id, p.permission_id
FROM db_admin.admin_roles AS r
JOIN db_admin.admin_permissions AS p ON (
    r.role_key = 'root'
    OR (r.role_key = 'developer' AND p.permission_key IN ('db_admin:read', 'db_admin:sql'))
)
ON CONFLICT DO NOTHING;
