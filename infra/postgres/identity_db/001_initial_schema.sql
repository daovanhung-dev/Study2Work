-- Study2Work V1-PILOT: identity_db initial schema
-- PostgreSQL 16+. Run while connected to the already-provisioned identity_db.
-- The executing principal must be allowed to create NOLOGIN roles, transfer
-- schema ownership, and create objects in this database. This file creates no
-- LOGIN role, credential, secret, or seed data.

BEGIN;

DO $roles$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 's2w_identity_owner') THEN
        CREATE ROLE s2w_identity_owner
            NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOREPLICATION NOBYPASSRLS;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 's2w_identity_app') THEN
        CREATE ROLE s2w_identity_app
            NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOREPLICATION NOBYPASSRLS;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 's2w_identity_worker') THEN
        CREATE ROLE s2w_identity_worker
            NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOREPLICATION NOBYPASSRLS;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 's2w_identity_readonly') THEN
        CREATE ROLE s2w_identity_readonly
            NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOREPLICATION NOBYPASSRLS;
    END IF;
END
$roles$;

CREATE SCHEMA IF NOT EXISTS app_private AUTHORIZATION s2w_identity_owner;
ALTER SCHEMA public OWNER TO s2w_identity_owner;
REVOKE ALL ON DATABASE identity_db FROM PUBLIC;
GRANT CONNECT ON DATABASE identity_db
TO s2w_identity_app, s2w_identity_worker, s2w_identity_readonly;

DO $membership$
BEGIN
    IF session_user <> 's2w_identity_owner'
       AND NOT pg_has_role(session_user, 's2w_identity_owner', 'MEMBER') THEN
        EXECUTE format('GRANT %I TO %I', 's2w_identity_owner', session_user);
    END IF;
END
$membership$;

SET ROLE s2w_identity_owner;
SET LOCAL search_path = public, app_private;

CREATE TYPE account_status AS ENUM (
    'PENDING_EMAIL_VERIFICATION',
    'ACTIVE',
    'SUSPENDED',
    'DELETION_PENDING',
    'ANONYMIZED'
);

CREATE TYPE mfa_method_type AS ENUM (
    'TOTP',
    'RECOVERY_CODE'
);

CREATE TYPE token_status AS ENUM (
    'ACTIVE',
    'CONSUMED',
    'REVOKED',
    'EXPIRED'
);

CREATE TYPE session_status AS ENUM (
    'ACTIVE',
    'REVOKED',
    'COMPROMISED',
    'EXPIRED'
);

CREATE TYPE audit_outcome AS ENUM (
    'SUCCESS',
    'DENIED',
    'FAILURE'
);

CREATE TYPE outbox_status AS ENUM (
    'PENDING',
    'PUBLISHED',
    'FAILED',
    'DEAD_LETTER'
);

CREATE TABLE users (
    id uuid PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    row_version bigint NOT NULL DEFAULT 1,
    status account_status NOT NULL DEFAULT 'PENDING_EMAIL_VERIFICATION',
    display_name varchar(120),
    locale varchar(10) NOT NULL DEFAULT 'vi-VN',
    timezone varchar(64) NOT NULL DEFAULT 'Asia/Ho_Chi_Minh',
    email_verified_at timestamptz,
    suspended_at timestamptz,
    suspension_reason varchar(500),
    deletion_requested_at timestamptz,
    anonymized_at timestamptz,
    privileged_mfa_required boolean NOT NULL DEFAULT false,
    CONSTRAINT ck_users_row_version_positive CHECK (row_version >= 1),
    CONSTRAINT ck_users_suspended_details CHECK (
        status <> 'SUSPENDED'
        OR (
            suspended_at IS NOT NULL
            AND suspension_reason IS NOT NULL
            AND char_length(btrim(suspension_reason)) > 0
        )
    ),
    CONSTRAINT ck_users_anonymized_at CHECK (
        status <> 'ANONYMIZED' OR anonymized_at IS NOT NULL
    ),
    CONSTRAINT ck_users_display_name_trimmed_length CHECK (
        display_name IS NULL
        OR char_length(btrim(display_name)) BETWEEN 1 AND 120
    )
);

CREATE TABLE user_emails (
    id uuid PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    row_version bigint NOT NULL DEFAULT 1,
    user_id uuid NOT NULL REFERENCES users (id) ON DELETE RESTRICT,
    email_ciphertext bytea NOT NULL,
    email_normalized varchar(320) COLLATE "C" NOT NULL,
    is_primary boolean NOT NULL DEFAULT true,
    verified_at timestamptz,
    replaced_at timestamptz,
    CONSTRAINT ck_user_emails_row_version_positive CHECK (row_version >= 1),
    CONSTRAINT ck_user_emails_normalized_nonempty CHECK (
        char_length(email_normalized) > 0
        AND email_normalized = btrim(email_normalized)
    )
);

CREATE TABLE password_credentials (
    id uuid PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    row_version bigint NOT NULL DEFAULT 1,
    user_id uuid NOT NULL UNIQUE REFERENCES users (id) ON DELETE RESTRICT,
    password_hash varchar(512) NOT NULL,
    algorithm varchar(32) NOT NULL DEFAULT 'ARGON2ID',
    parameters jsonb NOT NULL,
    changed_at timestamptz NOT NULL,
    must_change boolean NOT NULL DEFAULT false,
    failed_count integer NOT NULL DEFAULT 0,
    locked_until timestamptz,
    CONSTRAINT ck_password_credentials_row_version_positive CHECK (row_version >= 1),
    CONSTRAINT ck_password_credentials_failed_count CHECK (failed_count >= 0),
    CONSTRAINT ck_password_credentials_algorithm CHECK (algorithm = 'ARGON2ID'),
    CONSTRAINT ck_password_credentials_parameters_object CHECK (
        jsonb_typeof(parameters) = 'object'
    )
);

CREATE TABLE email_verification_tokens (
    id uuid PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT now(),
    user_id uuid NOT NULL REFERENCES users (id) ON DELETE RESTRICT,
    email_id uuid NOT NULL REFERENCES user_emails (id) ON DELETE RESTRICT,
    purpose varchar(24) NOT NULL,
    token_hash char(64) NOT NULL UNIQUE,
    status token_status NOT NULL DEFAULT 'ACTIVE',
    expires_at timestamptz NOT NULL,
    consumed_at timestamptz,
    revoked_at timestamptz,
    request_ip_hash char(64),
    CONSTRAINT ck_email_verification_tokens_purpose CHECK (
        purpose IN ('REGISTER', 'CHANGE_EMAIL')
    ),
    CONSTRAINT ck_email_verification_tokens_expires_after_created CHECK (
        expires_at > created_at
    ),
    CONSTRAINT ck_email_verification_tokens_status_timestamps CHECK (
        (status = 'ACTIVE' AND consumed_at IS NULL AND revoked_at IS NULL)
        OR (status = 'CONSUMED' AND consumed_at IS NOT NULL AND revoked_at IS NULL)
        OR (status = 'REVOKED' AND consumed_at IS NULL AND revoked_at IS NOT NULL)
        OR (status = 'EXPIRED' AND consumed_at IS NULL AND revoked_at IS NULL)
    )
);

CREATE TABLE password_reset_tokens (
    id uuid PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT now(),
    user_id uuid NOT NULL REFERENCES users (id) ON DELETE RESTRICT,
    token_hash char(64) NOT NULL UNIQUE,
    status token_status NOT NULL DEFAULT 'ACTIVE',
    expires_at timestamptz NOT NULL,
    consumed_at timestamptz,
    revoked_at timestamptz,
    session_epoch bigint NOT NULL,
    request_ip_hash char(64),
    CONSTRAINT ck_password_reset_tokens_expires_after_created CHECK (
        expires_at > created_at
    ),
    CONSTRAINT ck_password_reset_tokens_session_epoch_nonnegative CHECK (
        session_epoch >= 0
    ),
    CONSTRAINT ck_password_reset_tokens_status_timestamps CHECK (
        (status = 'ACTIVE' AND consumed_at IS NULL AND revoked_at IS NULL)
        OR (status = 'CONSUMED' AND consumed_at IS NOT NULL AND revoked_at IS NULL)
        OR (status = 'REVOKED' AND consumed_at IS NULL AND revoked_at IS NOT NULL)
        OR (status = 'EXPIRED' AND consumed_at IS NULL AND revoked_at IS NULL)
    )
);

CREATE TABLE mfa_methods (
    id uuid PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    row_version bigint NOT NULL DEFAULT 1,
    user_id uuid NOT NULL REFERENCES users (id) ON DELETE RESTRICT,
    type mfa_method_type NOT NULL,
    label varchar(80),
    secret_ciphertext bytea,
    verified_at timestamptz,
    disabled_at timestamptz,
    CONSTRAINT ck_mfa_methods_row_version_positive CHECK (row_version >= 1),
    CONSTRAINT ck_mfa_methods_totp_secret CHECK (
        type <> 'TOTP' OR secret_ciphertext IS NOT NULL
    )
);

CREATE TABLE mfa_recovery_codes (
    id uuid PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT now(),
    method_id uuid NOT NULL REFERENCES mfa_methods (id) ON DELETE RESTRICT,
    code_hash char(64) NOT NULL UNIQUE,
    consumed_at timestamptz,
    batch_id uuid NOT NULL
);

CREATE TABLE mfa_challenges (
    id uuid PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    row_version bigint NOT NULL DEFAULT 1,
    user_id uuid NOT NULL REFERENCES users (id) ON DELETE RESTRICT,
    session_id uuid,
    purpose varchar(32) NOT NULL,
    challenge_hash char(64) NOT NULL UNIQUE,
    expires_at timestamptz NOT NULL,
    attempt_count integer NOT NULL DEFAULT 0,
    max_attempts integer NOT NULL DEFAULT 5,
    verified_at timestamptz,
    invalidated_at timestamptz,
    CONSTRAINT ck_mfa_challenges_row_version_positive CHECK (row_version >= 1),
    CONSTRAINT ck_mfa_challenges_expires_after_created CHECK (expires_at > created_at),
    CONSTRAINT ck_mfa_challenges_attempt_count CHECK (
        max_attempts >= 1
        AND attempt_count BETWEEN 0 AND max_attempts
    ),
    CONSTRAINT ck_mfa_challenges_terminal_exclusive CHECK (
        NOT (verified_at IS NOT NULL AND invalidated_at IS NOT NULL)
    )
);

CREATE TABLE auth_sessions (
    id uuid PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    row_version bigint NOT NULL DEFAULT 1,
    user_id uuid NOT NULL REFERENCES users (id) ON DELETE RESTRICT,
    status session_status NOT NULL DEFAULT 'ACTIVE',
    session_epoch bigint NOT NULL,
    device_id_hash char(64),
    device_name varchar(120),
    ip_hash char(64),
    user_agent_hash char(64),
    last_seen_at timestamptz NOT NULL,
    expires_at timestamptz NOT NULL,
    revoked_at timestamptz,
    revoke_reason varchar(100),
    CONSTRAINT ck_auth_sessions_row_version_positive CHECK (row_version >= 1),
    CONSTRAINT ck_auth_sessions_epoch_nonnegative CHECK (session_epoch >= 0),
    CONSTRAINT ck_auth_sessions_expires_after_created CHECK (expires_at > created_at),
    CONSTRAINT ck_auth_sessions_revocation_details CHECK (
        status NOT IN ('REVOKED', 'COMPROMISED') OR revoked_at IS NOT NULL
    )
);

CREATE TABLE refresh_tokens (
    id uuid PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT now(),
    session_id uuid NOT NULL REFERENCES auth_sessions (id) ON DELETE RESTRICT,
    family_id uuid NOT NULL,
    parent_token_id uuid REFERENCES refresh_tokens (id) ON DELETE RESTRICT,
    token_hash char(64) NOT NULL UNIQUE,
    status token_status NOT NULL DEFAULT 'ACTIVE',
    issued_at timestamptz NOT NULL,
    expires_at timestamptz NOT NULL,
    rotated_to_id uuid REFERENCES refresh_tokens (id) ON DELETE RESTRICT,
    consumed_at timestamptz,
    reuse_detected_at timestamptz,
    CONSTRAINT ck_refresh_tokens_expires_after_issued CHECK (expires_at > issued_at),
    CONSTRAINT ck_refresh_tokens_parent_not_self CHECK (
        parent_token_id IS NULL OR parent_token_id <> id
    ),
    CONSTRAINT ck_refresh_tokens_rotated_to_not_self CHECK (
        rotated_to_id IS NULL OR rotated_to_id <> id
    )
);

CREATE TABLE signing_keys (
    id uuid PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    row_version bigint NOT NULL DEFAULT 1,
    kid varchar(80) NOT NULL UNIQUE,
    algorithm varchar(16) NOT NULL DEFAULT 'ES256',
    public_jwk jsonb NOT NULL,
    private_key_ref varchar(300) NOT NULL,
    not_before timestamptz NOT NULL,
    not_after timestamptz NOT NULL,
    activated_at timestamptz,
    retired_at timestamptz,
    CONSTRAINT ck_signing_keys_row_version_positive CHECK (row_version >= 1),
    CONSTRAINT ck_signing_keys_algorithm CHECK (algorithm = 'ES256'),
    CONSTRAINT ck_signing_keys_not_after CHECK (not_after > not_before),
    CONSTRAINT ck_signing_keys_public_jwk_object CHECK (
        jsonb_typeof(public_jwk) = 'object'
    )
);

CREATE TABLE roles (
    id uuid PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    row_version bigint NOT NULL DEFAULT 1,
    code varchar(80) NOT NULL UNIQUE,
    name varchar(120) NOT NULL,
    description varchar(500) NOT NULL,
    is_privileged boolean NOT NULL DEFAULT false,
    is_system boolean NOT NULL DEFAULT true,
    disabled_at timestamptz,
    CONSTRAINT ck_roles_row_version_positive CHECK (row_version >= 1),
    CONSTRAINT ck_roles_code_format CHECK (code ~ '^[A-Z][A-Z0-9_]{1,79}$')
);

CREATE TABLE permissions (
    id uuid PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    row_version bigint NOT NULL DEFAULT 1,
    code varchar(120) NOT NULL UNIQUE,
    service varchar(20) NOT NULL,
    description varchar(500) NOT NULL,
    risk_level smallint NOT NULL DEFAULT 1,
    CONSTRAINT ck_permissions_row_version_positive CHECK (row_version >= 1),
    CONSTRAINT ck_permissions_service CHECK (service IN ('IDENTITY', 'STUDY', 'WORK')),
    CONSTRAINT ck_permissions_risk_level CHECK (risk_level BETWEEN 1 AND 5)
);

CREATE TABLE role_permissions (
    id uuid PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT now(),
    role_id uuid NOT NULL REFERENCES roles (id) ON DELETE RESTRICT,
    permission_id uuid NOT NULL REFERENCES permissions (id) ON DELETE RESTRICT,
    granted_by uuid NOT NULL REFERENCES users (id) ON DELETE RESTRICT,
    revoked_at timestamptz,
    revoked_by uuid REFERENCES users (id) ON DELETE RESTRICT,
    CONSTRAINT ck_role_permissions_revoked_by CHECK (
        revoked_at IS NULL OR revoked_by IS NOT NULL
    )
);

CREATE TABLE user_role_assignments (
    id uuid PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT now(),
    user_id uuid NOT NULL REFERENCES users (id) ON DELETE RESTRICT,
    role_id uuid NOT NULL REFERENCES roles (id) ON DELETE RESTRICT,
    scope_type varchar(24) NOT NULL DEFAULT 'PLATFORM',
    scope_id uuid,
    valid_from timestamptz NOT NULL DEFAULT now(),
    valid_until timestamptz,
    granted_by uuid NOT NULL REFERENCES users (id) ON DELETE RESTRICT,
    revoked_at timestamptz,
    revoked_by uuid REFERENCES users (id) ON DELETE RESTRICT,
    reason varchar(500) NOT NULL,
    CONSTRAINT ck_user_role_assignments_valid_period CHECK (
        valid_until IS NULL OR valid_until > valid_from
    ),
    CONSTRAINT ck_user_role_assignments_platform_scope CHECK (
        scope_type <> 'PLATFORM' OR scope_id IS NULL
    ),
    CONSTRAINT ck_user_role_assignments_revoked_by CHECK (
        revoked_at IS NULL OR revoked_by IS NOT NULL
    )
);

CREATE TABLE idempotency_keys (
    id uuid PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    row_version bigint NOT NULL DEFAULT 1,
    actor_id uuid,
    operation varchar(120) NOT NULL,
    key_hash char(64) NOT NULL,
    request_hash char(64) NOT NULL,
    response_status integer,
    response_body jsonb,
    locked_until timestamptz,
    completed_at timestamptz,
    expires_at timestamptz NOT NULL,
    CONSTRAINT ck_idempotency_keys_row_version_positive CHECK (row_version >= 1)
);

CREATE TABLE security_audit_events (
    id uuid PRIMARY KEY,
    occurred_at timestamptz NOT NULL DEFAULT now(),
    actor_id uuid,
    subject_id uuid,
    action varchar(120) NOT NULL,
    outcome audit_outcome NOT NULL,
    reason_code varchar(80),
    trace_id varchar(64) NOT NULL,
    session_id uuid,
    ip_hash char(64),
    user_agent_hash char(64),
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    prev_hash char(64),
    event_hash char(64) NOT NULL UNIQUE,
    legal_hold_until timestamptz,
    CONSTRAINT ck_security_audit_events_reason_code CHECK (
        outcome = 'SUCCESS'
        OR (reason_code IS NOT NULL AND char_length(btrim(reason_code)) > 0)
    ),
    CONSTRAINT ck_security_audit_events_metadata_object CHECK (
        jsonb_typeof(metadata) = 'object'
    )
);

CREATE TABLE outbox_events (
    id uuid PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT now(),
    aggregate_type varchar(80) NOT NULL,
    aggregate_id uuid NOT NULL,
    event_type varchar(120) NOT NULL,
    event_version integer NOT NULL,
    payload jsonb NOT NULL,
    available_at timestamptz NOT NULL DEFAULT now(),
    dedupe_key varchar(180) NOT NULL UNIQUE,
    trace_id varchar(64) NOT NULL,
    CONSTRAINT ck_outbox_events_event_version CHECK (event_version >= 1)
);

CREATE TABLE consumer_inbox (
    id uuid PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT now(),
    consumer varchar(100) NOT NULL,
    event_id uuid NOT NULL,
    event_type varchar(120) NOT NULL,
    payload_hash char(64) NOT NULL,
    received_at timestamptz NOT NULL DEFAULT now(),
    processed_at timestamptz,
    result_code varchar(80),
    trace_id varchar(64) NOT NULL,
    CONSTRAINT uq_consumer_inbox_consumer_event UNIQUE (consumer, event_id)
);

CREATE TABLE outbox_delivery_attempts (
    id uuid PRIMARY KEY,
    occurred_at timestamptz NOT NULL DEFAULT now(),
    outbox_event_id uuid NOT NULL REFERENCES outbox_events (id) ON DELETE RESTRICT,
    attempt_no integer NOT NULL,
    status outbox_status NOT NULL,
    worker_id varchar(120) NOT NULL,
    broker_message_id varchar(180),
    error_code varchar(80),
    next_retry_at timestamptz,
    payload_hash char(64) NOT NULL,
    CONSTRAINT uq_outbox_delivery_attempts_event_attempt UNIQUE (outbox_event_id, attempt_no),
    CONSTRAINT ck_outbox_delivery_attempts_attempt_no CHECK (attempt_no >= 1),
    CONSTRAINT ck_outbox_delivery_attempts_not_pending CHECK (status <> 'PENDING')
);

CREATE UNIQUE INDEX uq_user_emails_active_normalized
    ON user_emails (email_normalized)
    WHERE replaced_at IS NULL;
CREATE UNIQUE INDEX uq_user_emails_active_primary
    ON user_emails (user_id)
    WHERE is_primary = true AND replaced_at IS NULL;
CREATE INDEX ix_user_emails_user_replaced
    ON user_emails (user_id, replaced_at);

CREATE INDEX ix_users_status_created_at
    ON users (status, created_at DESC);
CREATE INDEX ix_users_deletion_requested_at
    ON users (deletion_requested_at)
    WHERE deletion_requested_at IS NOT NULL;

CREATE INDEX ix_email_verification_tokens_user_status_expires
    ON email_verification_tokens (user_id, status, expires_at DESC);
CREATE INDEX ix_password_reset_tokens_user_status_expires
    ON password_reset_tokens (user_id, status, expires_at DESC);
CREATE INDEX ix_mfa_methods_user_disabled
    ON mfa_methods (user_id, disabled_at);
CREATE UNIQUE INDEX uq_mfa_methods_active_user_type
    ON mfa_methods (user_id, type)
    WHERE disabled_at IS NULL;
CREATE INDEX ix_mfa_recovery_codes_method_consumed
    ON mfa_recovery_codes (method_id, consumed_at);
CREATE INDEX ix_mfa_challenges_user_purpose_expires
    ON mfa_challenges (user_id, purpose, expires_at DESC);
CREATE INDEX ix_auth_sessions_user_status_last_seen
    ON auth_sessions (user_id, status, last_seen_at DESC);
CREATE INDEX ix_auth_sessions_active_expires
    ON auth_sessions (expires_at)
    WHERE status = 'ACTIVE';
CREATE UNIQUE INDEX uq_refresh_tokens_parent_token
    ON refresh_tokens (parent_token_id)
    WHERE parent_token_id IS NOT NULL;
CREATE INDEX ix_refresh_tokens_family_status
    ON refresh_tokens (family_id, status);
CREATE INDEX ix_refresh_tokens_session_issued
    ON refresh_tokens (session_id, issued_at DESC);
CREATE INDEX ix_refresh_tokens_expires
    ON refresh_tokens (expires_at);
CREATE INDEX ix_signing_keys_activated_retired
    ON signing_keys (activated_at, retired_at);

CREATE INDEX ix_roles_disabled_code
    ON roles (disabled_at, code);
CREATE INDEX ix_permissions_service_code
    ON permissions (service, code);
CREATE UNIQUE INDEX uq_role_permissions_active
    ON role_permissions (role_id, permission_id)
    WHERE revoked_at IS NULL;
CREATE INDEX ix_role_permissions_permission_revoked
    ON role_permissions (permission_id, revoked_at);
CREATE UNIQUE INDEX uq_user_role_assignments_effective
    ON user_role_assignments (user_id, role_id, scope_type, scope_id) NULLS NOT DISTINCT
    WHERE revoked_at IS NULL;
CREATE INDEX ix_user_role_assignments_user_effective
    ON user_role_assignments (user_id, revoked_at, valid_until);
CREATE INDEX ix_user_role_assignments_scope_effective
    ON user_role_assignments (scope_type, scope_id, revoked_at);

CREATE UNIQUE INDEX uq_idempotency_keys_actor_operation_key
    ON idempotency_keys (actor_id, operation, key_hash) NULLS NOT DISTINCT;
CREATE INDEX ix_idempotency_keys_expires
    ON idempotency_keys (expires_at);
CREATE INDEX ix_security_audit_events_subject_occurred
    ON security_audit_events (subject_id, occurred_at DESC);
CREATE INDEX ix_security_audit_events_actor_occurred
    ON security_audit_events (actor_id, occurred_at DESC);
CREATE INDEX ix_security_audit_events_trace
    ON security_audit_events (trace_id);
CREATE INDEX ix_security_audit_events_occurred_brin
    ON security_audit_events USING brin (occurred_at);
CREATE INDEX ix_outbox_events_available_id
    ON outbox_events (available_at, id);
CREATE INDEX ix_outbox_events_aggregate_created
    ON outbox_events (aggregate_type, aggregate_id, created_at);
CREATE INDEX ix_consumer_inbox_consumer_processed_received
    ON consumer_inbox (consumer, processed_at, received_at);
CREATE INDEX ix_outbox_delivery_attempts_event_attempt
    ON outbox_delivery_attempts (outbox_event_id, attempt_no DESC);
CREATE INDEX ix_outbox_delivery_attempts_status_retry_occurred
    ON outbox_delivery_attempts (status, next_retry_at, occurred_at);

CREATE FUNCTION app_private.touch_entity()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = pg_catalog, public, app_private
AS $function$
BEGIN
    NEW.updated_at := now();
    NEW.row_version := OLD.row_version + 1;
    RETURN NEW;
END
$function$;

CREATE FUNCTION app_private.reject_immutable_change()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = pg_catalog, public, app_private
AS $function$
BEGIN
    RAISE EXCEPTION 'immutable or append-only record % cannot be %', TG_TABLE_NAME, TG_OP
        USING ERRCODE = '55000';
END
$function$;

CREATE FUNCTION app_private.enforce_token_transition()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = pg_catalog, public, app_private
AS $function$
BEGIN
    IF (to_jsonb(NEW) - ARRAY['status', 'consumed_at', 'revoked_at'])
       IS DISTINCT FROM
       (to_jsonb(OLD) - ARRAY['status', 'consumed_at', 'revoked_at']) THEN
        RAISE EXCEPTION 'only token state fields may change on %', TG_TABLE_NAME
            USING ERRCODE = '55000';
    END IF;

    IF OLD.status <> 'ACTIVE'
       OR NEW.status NOT IN ('CONSUMED', 'REVOKED', 'EXPIRED') THEN
        RAISE EXCEPTION 'token status transition from % to % is not permitted',
            OLD.status, NEW.status USING ERRCODE = '55000';
    END IF;

    RETURN NEW;
END
$function$;

CREATE FUNCTION app_private.enforce_mfa_recovery_code_transition()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = pg_catalog, public, app_private
AS $function$
BEGIN
    IF (to_jsonb(NEW) - 'consumed_at') IS DISTINCT FROM (to_jsonb(OLD) - 'consumed_at')
       OR OLD.consumed_at IS NOT NULL
       OR NEW.consumed_at IS NULL THEN
        RAISE EXCEPTION 'a recovery code may only be consumed once'
            USING ERRCODE = '55000';
    END IF;
    RETURN NEW;
END
$function$;

CREATE FUNCTION app_private.enforce_mfa_challenge_transition()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = pg_catalog, public, app_private
AS $function$
BEGIN
    IF (to_jsonb(NEW) - ARRAY[
        'attempt_count', 'verified_at', 'invalidated_at', 'updated_at', 'row_version'
    ]) IS DISTINCT FROM (to_jsonb(OLD) - ARRAY[
        'attempt_count', 'verified_at', 'invalidated_at', 'updated_at', 'row_version'
    ]) THEN
        RAISE EXCEPTION 'only challenge attempt and terminal fields may change'
            USING ERRCODE = '55000';
    END IF;

    IF NEW.attempt_count < OLD.attempt_count
       OR (OLD.verified_at IS NOT NULL AND NEW.verified_at IS DISTINCT FROM OLD.verified_at)
       OR (OLD.invalidated_at IS NOT NULL AND NEW.invalidated_at IS DISTINCT FROM OLD.invalidated_at)
       OR ((OLD.verified_at IS NOT NULL OR OLD.invalidated_at IS NOT NULL)
           AND NEW.attempt_count IS DISTINCT FROM OLD.attempt_count) THEN
        RAISE EXCEPTION 'MFA challenge transition is not one-way'
            USING ERRCODE = '55000';
    END IF;

    RETURN NEW;
END
$function$;

CREATE FUNCTION app_private.enforce_refresh_token_transition()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = pg_catalog, public, app_private
AS $function$
BEGIN
    IF (to_jsonb(NEW) - ARRAY[
        'status', 'rotated_to_id', 'consumed_at', 'reuse_detected_at'
    ]) IS DISTINCT FROM (to_jsonb(OLD) - ARRAY[
        'status', 'rotated_to_id', 'consumed_at', 'reuse_detected_at'
    ]) THEN
        RAISE EXCEPTION 'only refresh-token lifecycle fields may change'
            USING ERRCODE = '55000';
    END IF;

    IF (OLD.rotated_to_id IS NOT NULL AND NEW.rotated_to_id IS DISTINCT FROM OLD.rotated_to_id)
       OR (OLD.consumed_at IS NOT NULL AND NEW.consumed_at IS DISTINCT FROM OLD.consumed_at)
       OR (OLD.reuse_detected_at IS NOT NULL
           AND NEW.reuse_detected_at IS DISTINCT FROM OLD.reuse_detected_at) THEN
        RAISE EXCEPTION 'refresh-token lifecycle values are write-once'
            USING ERRCODE = '55000';
    END IF;

    IF OLD.status <> NEW.status
       AND NOT (
            (OLD.status = 'ACTIVE' AND NEW.status IN ('CONSUMED', 'REVOKED', 'EXPIRED'))
            OR (OLD.status = 'CONSUMED' AND NEW.status = 'REVOKED')
       ) THEN
        RAISE EXCEPTION 'refresh-token status transition from % to % is not permitted',
            OLD.status, NEW.status USING ERRCODE = '55000';
    END IF;

    RETURN NEW;
END
$function$;

CREATE FUNCTION app_private.enforce_auth_session_transition()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = pg_catalog, public, app_private
AS $function$
BEGIN
    IF NEW.id IS DISTINCT FROM OLD.id
       OR NEW.created_at IS DISTINCT FROM OLD.created_at
       OR NEW.user_id IS DISTINCT FROM OLD.user_id THEN
        RAISE EXCEPTION 'authentication session identity is immutable'
            USING ERRCODE = '55000';
    END IF;

    IF OLD.revoked_at IS NOT NULL AND NEW.revoked_at IS DISTINCT FROM OLD.revoked_at THEN
        RAISE EXCEPTION 'authentication session revocation timestamp is write-once'
            USING ERRCODE = '55000';
    END IF;

    IF OLD.status <> NEW.status
       AND NOT (
           OLD.status = 'ACTIVE'
           AND NEW.status IN ('REVOKED', 'COMPROMISED', 'EXPIRED')
       ) THEN
        RAISE EXCEPTION 'authentication session status transition from % to % is not permitted',
            OLD.status, NEW.status USING ERRCODE = '55000';
    END IF;

    RETURN NEW;
END
$function$;

CREATE FUNCTION app_private.enforce_revocation_only()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = pg_catalog, public, app_private
AS $function$
BEGIN
    IF (to_jsonb(NEW) - ARRAY['revoked_at', 'revoked_by'])
       IS DISTINCT FROM
       (to_jsonb(OLD) - ARRAY['revoked_at', 'revoked_by'])
       OR OLD.revoked_at IS NOT NULL
       OR NEW.revoked_at IS NULL
       OR NEW.revoked_by IS NULL THEN
        RAISE EXCEPTION 'immutable grant/assignment may only be revoked once'
            USING ERRCODE = '55000';
    END IF;
    RETURN NEW;
END
$function$;

CREATE FUNCTION app_private.enforce_consumer_inbox_transition()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = pg_catalog, public, app_private
AS $function$
BEGIN
    IF (to_jsonb(NEW) - ARRAY['processed_at', 'result_code'])
       IS DISTINCT FROM
       (to_jsonb(OLD) - ARRAY['processed_at', 'result_code'])
       OR OLD.processed_at IS NOT NULL
       OR NEW.processed_at IS NULL THEN
        RAISE EXCEPTION 'consumer inbox record may only be marked processed once'
            USING ERRCODE = '55000';
    END IF;
    RETURN NEW;
END
$function$;

CREATE FUNCTION app_private.enforce_system_role()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = pg_catalog, public, app_private
AS $function$
BEGIN
    IF TG_OP = 'DELETE' AND OLD.is_system THEN
        RAISE EXCEPTION 'system role cannot be deleted' USING ERRCODE = '55000';
    END IF;
    IF TG_OP = 'UPDATE' AND OLD.is_system AND NEW.code IS DISTINCT FROM OLD.code THEN
        RAISE EXCEPTION 'system role code cannot be changed' USING ERRCODE = '55000';
    END IF;
    RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END
$function$;

CREATE FUNCTION app_private.current_subject_id()
RETURNS uuid
LANGUAGE plpgsql
STABLE
SET search_path = pg_catalog, public, app_private
AS $function$
DECLARE
    subject_value text := current_setting('app.subject_id', true);
BEGIN
    IF subject_value IS NULL OR subject_value = '' THEN
        RETURN NULL;
    END IF;
    RETURN subject_value::uuid;
END
$function$;

CREATE FUNCTION app_private.current_tenant_id()
RETURNS uuid
LANGUAGE plpgsql
STABLE
SET search_path = pg_catalog, public, app_private
AS $function$
DECLARE
    tenant_value text := current_setting('app.tenant_id', true);
BEGIN
    IF tenant_value IS NULL OR tenant_value = '' THEN
        RETURN NULL;
    END IF;
    RETURN tenant_value::uuid;
END
$function$;

CREATE PROCEDURE app_private.transition_email_verification_token(
    p_token_id uuid,
    p_target_status token_status
)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = pg_catalog, public, app_private
AS $procedure$
BEGIN
    IF p_target_status NOT IN ('CONSUMED', 'REVOKED', 'EXPIRED') THEN
        RAISE EXCEPTION 'invalid email verification token target status: %', p_target_status
            USING ERRCODE = '22023';
    END IF;

    UPDATE public.email_verification_tokens
       SET status = p_target_status,
           consumed_at = CASE WHEN p_target_status = 'CONSUMED' THEN now() ELSE NULL END,
           revoked_at = CASE WHEN p_target_status = 'REVOKED' THEN now() ELSE NULL END
     WHERE id = p_token_id
       AND status = 'ACTIVE'
       AND (p_target_status <> 'CONSUMED' OR expires_at > now());

    IF NOT FOUND THEN
        RAISE EXCEPTION 'email verification token is unavailable'
            USING ERRCODE = '55000';
    END IF;
END
$procedure$;

CREATE PROCEDURE app_private.transition_password_reset_token(
    p_token_id uuid,
    p_target_status token_status
)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = pg_catalog, public, app_private
AS $procedure$
BEGIN
    IF p_target_status NOT IN ('CONSUMED', 'REVOKED', 'EXPIRED') THEN
        RAISE EXCEPTION 'invalid password reset token target status: %', p_target_status
            USING ERRCODE = '22023';
    END IF;

    UPDATE public.password_reset_tokens
       SET status = p_target_status,
           consumed_at = CASE WHEN p_target_status = 'CONSUMED' THEN now() ELSE NULL END,
           revoked_at = CASE WHEN p_target_status = 'REVOKED' THEN now() ELSE NULL END
     WHERE id = p_token_id
       AND status = 'ACTIVE'
       AND (p_target_status <> 'CONSUMED' OR expires_at > now());

    IF NOT FOUND THEN
        RAISE EXCEPTION 'password reset token is unavailable'
            USING ERRCODE = '55000';
    END IF;
END
$procedure$;

CREATE PROCEDURE app_private.consume_mfa_recovery_code(p_code_id uuid)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = pg_catalog, public, app_private
AS $procedure$
BEGIN
    UPDATE public.mfa_recovery_codes
       SET consumed_at = now()
     WHERE id = p_code_id
       AND consumed_at IS NULL;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'MFA recovery code is unavailable'
            USING ERRCODE = '55000';
    END IF;
END
$procedure$;

CREATE PROCEDURE app_private.transition_refresh_token(
    p_token_id uuid,
    p_target_status token_status,
    p_rotated_to_id uuid DEFAULT NULL,
    p_record_reuse boolean DEFAULT false
)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = pg_catalog, public, app_private
AS $procedure$
BEGIN
    IF p_target_status NOT IN ('CONSUMED', 'REVOKED', 'EXPIRED') THEN
        RAISE EXCEPTION 'invalid refresh token target status: %', p_target_status
            USING ERRCODE = '22023';
    END IF;

    UPDATE public.refresh_tokens
       SET status = p_target_status,
           rotated_to_id = COALESCE(p_rotated_to_id, rotated_to_id),
           consumed_at = CASE
               WHEN p_target_status = 'CONSUMED' AND consumed_at IS NULL THEN now()
               ELSE consumed_at
           END,
           reuse_detected_at = CASE
               WHEN p_record_reuse AND reuse_detected_at IS NULL THEN now()
               ELSE reuse_detected_at
           END
     WHERE id = p_token_id
       AND (
           status = 'ACTIVE'
           OR (status = 'CONSUMED' AND p_target_status = 'REVOKED')
       )
       AND (p_target_status <> 'CONSUMED' OR expires_at > now());

    IF NOT FOUND THEN
        RAISE EXCEPTION 'refresh token is unavailable for the requested transition'
            USING ERRCODE = '55000';
    END IF;
END
$procedure$;

CREATE TRIGGER z_touch_users
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION app_private.touch_entity();
CREATE TRIGGER z_touch_user_emails
    BEFORE UPDATE ON user_emails
    FOR EACH ROW EXECUTE FUNCTION app_private.touch_entity();
CREATE TRIGGER z_touch_password_credentials
    BEFORE UPDATE ON password_credentials
    FOR EACH ROW EXECUTE FUNCTION app_private.touch_entity();
CREATE TRIGGER z_touch_mfa_methods
    BEFORE UPDATE ON mfa_methods
    FOR EACH ROW EXECUTE FUNCTION app_private.touch_entity();
CREATE TRIGGER a_enforce_mfa_challenge_transition
    BEFORE UPDATE ON mfa_challenges
    FOR EACH ROW EXECUTE FUNCTION app_private.enforce_mfa_challenge_transition();
CREATE TRIGGER z_touch_mfa_challenges
    BEFORE UPDATE ON mfa_challenges
    FOR EACH ROW EXECUTE FUNCTION app_private.touch_entity();
CREATE TRIGGER a_enforce_auth_session_transition
    BEFORE UPDATE ON auth_sessions
    FOR EACH ROW EXECUTE FUNCTION app_private.enforce_auth_session_transition();
CREATE TRIGGER z_touch_auth_sessions
    BEFORE UPDATE ON auth_sessions
    FOR EACH ROW EXECUTE FUNCTION app_private.touch_entity();
CREATE TRIGGER z_touch_signing_keys
    BEFORE UPDATE ON signing_keys
    FOR EACH ROW EXECUTE FUNCTION app_private.touch_entity();
CREATE TRIGGER a_enforce_system_role
    BEFORE UPDATE OR DELETE ON roles
    FOR EACH ROW EXECUTE FUNCTION app_private.enforce_system_role();
CREATE TRIGGER z_touch_roles
    BEFORE UPDATE ON roles
    FOR EACH ROW EXECUTE FUNCTION app_private.touch_entity();
CREATE TRIGGER z_touch_permissions
    BEFORE UPDATE ON permissions
    FOR EACH ROW EXECUTE FUNCTION app_private.touch_entity();
CREATE TRIGGER z_touch_idempotency_keys
    BEFORE UPDATE ON idempotency_keys
    FOR EACH ROW EXECUTE FUNCTION app_private.touch_entity();

CREATE TRIGGER a_enforce_email_verification_token_transition
    BEFORE UPDATE ON email_verification_tokens
    FOR EACH ROW EXECUTE FUNCTION app_private.enforce_token_transition();
CREATE TRIGGER a_reject_email_verification_token_delete
    BEFORE DELETE ON email_verification_tokens
    FOR EACH ROW EXECUTE FUNCTION app_private.reject_immutable_change();
CREATE TRIGGER a_enforce_password_reset_token_transition
    BEFORE UPDATE ON password_reset_tokens
    FOR EACH ROW EXECUTE FUNCTION app_private.enforce_token_transition();
CREATE TRIGGER a_reject_password_reset_token_delete
    BEFORE DELETE ON password_reset_tokens
    FOR EACH ROW EXECUTE FUNCTION app_private.reject_immutable_change();
CREATE TRIGGER a_enforce_mfa_recovery_code_transition
    BEFORE UPDATE ON mfa_recovery_codes
    FOR EACH ROW EXECUTE FUNCTION app_private.enforce_mfa_recovery_code_transition();
CREATE TRIGGER a_reject_mfa_recovery_code_delete
    BEFORE DELETE ON mfa_recovery_codes
    FOR EACH ROW EXECUTE FUNCTION app_private.reject_immutable_change();
CREATE TRIGGER a_enforce_refresh_token_transition
    BEFORE UPDATE ON refresh_tokens
    FOR EACH ROW EXECUTE FUNCTION app_private.enforce_refresh_token_transition();
CREATE TRIGGER a_reject_refresh_token_delete
    BEFORE DELETE ON refresh_tokens
    FOR EACH ROW EXECUTE FUNCTION app_private.reject_immutable_change();
CREATE TRIGGER a_enforce_role_permission_revocation
    BEFORE UPDATE ON role_permissions
    FOR EACH ROW EXECUTE FUNCTION app_private.enforce_revocation_only();
CREATE TRIGGER a_reject_role_permission_delete
    BEFORE DELETE ON role_permissions
    FOR EACH ROW EXECUTE FUNCTION app_private.reject_immutable_change();
CREATE TRIGGER a_enforce_user_role_assignment_revocation
    BEFORE UPDATE ON user_role_assignments
    FOR EACH ROW EXECUTE FUNCTION app_private.enforce_revocation_only();
CREATE TRIGGER a_reject_user_role_assignment_delete
    BEFORE DELETE ON user_role_assignments
    FOR EACH ROW EXECUTE FUNCTION app_private.reject_immutable_change();
CREATE TRIGGER a_reject_security_audit_event_change
    BEFORE UPDATE OR DELETE ON security_audit_events
    FOR EACH ROW EXECUTE FUNCTION app_private.reject_immutable_change();
CREATE TRIGGER a_reject_outbox_event_change
    BEFORE UPDATE OR DELETE ON outbox_events
    FOR EACH ROW EXECUTE FUNCTION app_private.reject_immutable_change();
CREATE TRIGGER a_enforce_consumer_inbox_transition
    BEFORE UPDATE ON consumer_inbox
    FOR EACH ROW EXECUTE FUNCTION app_private.enforce_consumer_inbox_transition();
CREATE TRIGGER a_reject_consumer_inbox_delete
    BEFORE DELETE ON consumer_inbox
    FOR EACH ROW EXECUTE FUNCTION app_private.reject_immutable_change();
CREATE TRIGGER a_reject_outbox_delivery_attempt_change
    BEFORE UPDATE OR DELETE ON outbox_delivery_attempts
    FOR EACH ROW EXECUTE FUNCTION app_private.reject_immutable_change();

COMMENT ON TABLE users IS 'TBL-IAM-001 — Platform identities.';
COMMENT ON TABLE user_emails IS 'TBL-IAM-002 — Encrypted, normalized user email addresses.';
COMMENT ON TABLE password_credentials IS 'TBL-IAM-003 — Argon2id password credential metadata.';
COMMENT ON TABLE email_verification_tokens IS 'TBL-IAM-004 — Immutable email verification token records.';
COMMENT ON TABLE password_reset_tokens IS 'TBL-IAM-005 — Immutable password reset token records.';
COMMENT ON TABLE mfa_methods IS 'TBL-IAM-006 — MFA methods; TOTP secrets are application-envelope encrypted.';
COMMENT ON TABLE mfa_recovery_codes IS 'TBL-IAM-007 — Immutable hashed MFA recovery codes.';
COMMENT ON TABLE mfa_challenges IS 'TBL-IAM-008 — MFA challenges with one-way completion.';
COMMENT ON TABLE auth_sessions IS 'TBL-IAM-009 — Authentication sessions.';
COMMENT ON TABLE refresh_tokens IS 'TBL-IAM-010 — Immutable, rotating refresh-token family records.';
COMMENT ON TABLE signing_keys IS 'TBL-IAM-011 — Public JWKS metadata and private KMS/Vault references.';
COMMENT ON TABLE roles IS 'TBL-IAM-012 — Platform roles.';
COMMENT ON TABLE permissions IS 'TBL-IAM-013 — Platform permissions.';
COMMENT ON TABLE role_permissions IS 'TBL-IAM-014 — Immutable role-permission grants with revocation.';
COMMENT ON TABLE user_role_assignments IS 'TBL-IAM-015 — Immutable platform role assignments with revocation.';
COMMENT ON TABLE idempotency_keys IS 'TBL-IAM-016 — Idempotency request and masked response records.';
COMMENT ON TABLE security_audit_events IS 'TBL-IAM-017 — Append-only security audit event hash chain.';
COMMENT ON TABLE outbox_events IS 'TBL-IAM-018 — Immutable transactional outbox events.';
COMMENT ON TABLE consumer_inbox IS 'TBL-IAM-019 — Immutable consumer deduplication inbox records.';
COMMENT ON TABLE outbox_delivery_attempts IS 'TBL-IAM-020 — Append-only outbox delivery attempts.';

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA app_private FROM PUBLIC;
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA app_private FROM PUBLIC;
REVOKE ALL ON ALL PROCEDURES IN SCHEMA app_private FROM PUBLIC;

GRANT USAGE ON SCHEMA public TO s2w_identity_app, s2w_identity_worker, s2w_identity_readonly;
GRANT USAGE ON SCHEMA app_private TO s2w_identity_app, s2w_identity_worker;

GRANT SELECT, INSERT, UPDATE ON TABLE
    users,
    user_emails,
    password_credentials,
    mfa_methods,
    mfa_challenges,
    auth_sessions,
    signing_keys,
    roles,
    permissions,
    idempotency_keys
TO s2w_identity_app;
GRANT SELECT, INSERT ON TABLE
    email_verification_tokens,
    password_reset_tokens,
    mfa_recovery_codes,
    refresh_tokens,
    role_permissions,
    user_role_assignments,
    security_audit_events,
    outbox_events,
    consumer_inbox,
    outbox_delivery_attempts
TO s2w_identity_app;
GRANT UPDATE ON TABLE role_permissions, user_role_assignments, consumer_inbox
TO s2w_identity_app;

GRANT SELECT ON TABLE
    outbox_events,
    outbox_delivery_attempts,
    consumer_inbox,
    auth_sessions,
    refresh_tokens
TO s2w_identity_worker;
GRANT INSERT ON TABLE outbox_delivery_attempts, security_audit_events
TO s2w_identity_worker;
GRANT UPDATE ON TABLE consumer_inbox TO s2w_identity_worker;

GRANT SELECT ON TABLE roles, permissions TO s2w_identity_readonly;

GRANT EXECUTE ON PROCEDURE app_private.transition_email_verification_token(uuid, token_status)
TO s2w_identity_app, s2w_identity_worker;
GRANT EXECUTE ON PROCEDURE app_private.transition_password_reset_token(uuid, token_status)
TO s2w_identity_app, s2w_identity_worker;
GRANT EXECUTE ON PROCEDURE app_private.consume_mfa_recovery_code(uuid)
TO s2w_identity_app;
GRANT EXECUTE ON PROCEDURE app_private.transition_refresh_token(
    uuid,
    token_status,
    uuid,
    boolean
)
TO s2w_identity_app, s2w_identity_worker;

ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE ALL ON TABLES FROM PUBLIC;
ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE ALL ON SEQUENCES FROM PUBLIC;
ALTER DEFAULT PRIVILEGES IN SCHEMA app_private REVOKE ALL ON FUNCTIONS FROM PUBLIC;
ALTER DEFAULT PRIVILEGES IN SCHEMA app_private REVOKE ALL ON TYPES FROM PUBLIC;

RESET ROLE;
COMMIT;
