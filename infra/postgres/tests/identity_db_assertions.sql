\set ON_ERROR_STOP on
-- Run as the same administrative principal used to apply the initial schema.
-- Fixtures below are rolled back; this script does not seed identity_db.

BEGIN;

CREATE OR REPLACE FUNCTION pg_temp.assert_true(p_condition boolean, p_message text)
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
  IF p_condition IS DISTINCT FROM true THEN
    RAISE EXCEPTION '%', p_message USING ERRCODE = 'P0001';
  END IF;
END
$$;

WITH expected(table_name) AS (
  VALUES
    ('users'), ('user_emails'), ('password_credentials'),
    ('email_verification_tokens'), ('password_reset_tokens'), ('mfa_methods'),
    ('mfa_recovery_codes'), ('mfa_challenges'), ('auth_sessions'),
    ('refresh_tokens'), ('signing_keys'), ('roles'), ('permissions'),
    ('role_permissions'), ('user_role_assignments'), ('idempotency_keys'),
    ('security_audit_events'), ('outbox_events'), ('consumer_inbox'),
    ('outbox_delivery_attempts')
), actual(table_name) AS (
  SELECT c.relname
  FROM pg_class c
  JOIN pg_namespace n ON n.oid = c.relnamespace
  WHERE n.nspname = 'public' AND c.relkind = 'r'
)
SELECT pg_temp.assert_true(
  NOT EXISTS (SELECT 1 FROM expected e LEFT JOIN actual a USING (table_name) WHERE a.table_name IS NULL)
  AND NOT EXISTS (SELECT 1 FROM actual a LEFT JOIN expected e USING (table_name) WHERE e.table_name IS NULL),
  'identity_db public table inventory must be exactly TBL-IAM-001..020'
);

WITH expected(table_name, code) AS (
  VALUES
    ('users', 'TBL-IAM-001'), ('user_emails', 'TBL-IAM-002'),
    ('password_credentials', 'TBL-IAM-003'), ('email_verification_tokens', 'TBL-IAM-004'),
    ('password_reset_tokens', 'TBL-IAM-005'), ('mfa_methods', 'TBL-IAM-006'),
    ('mfa_recovery_codes', 'TBL-IAM-007'), ('mfa_challenges', 'TBL-IAM-008'),
    ('auth_sessions', 'TBL-IAM-009'), ('refresh_tokens', 'TBL-IAM-010'),
    ('signing_keys', 'TBL-IAM-011'), ('roles', 'TBL-IAM-012'),
    ('permissions', 'TBL-IAM-013'), ('role_permissions', 'TBL-IAM-014'),
    ('user_role_assignments', 'TBL-IAM-015'), ('idempotency_keys', 'TBL-IAM-016'),
    ('security_audit_events', 'TBL-IAM-017'), ('outbox_events', 'TBL-IAM-018'),
    ('consumer_inbox', 'TBL-IAM-019'), ('outbox_delivery_attempts', 'TBL-IAM-020')
)
SELECT pg_temp.assert_true(
  NOT EXISTS (
    SELECT 1 FROM expected
    WHERE obj_description(to_regclass('public.' || table_name), 'pg_class') NOT LIKE code || '%'
  ),
  'each identity table must retain its TBL-IAM comment'
);

WITH expected(type_name, labels) AS (
  VALUES
    ('account_status'::name, ARRAY['PENDING_EMAIL_VERIFICATION','ACTIVE','SUSPENDED','DELETION_PENDING','ANONYMIZED']::text[]),
    ('mfa_method_type'::name, ARRAY['TOTP','RECOVERY_CODE']::text[]),
    ('token_status'::name, ARRAY['ACTIVE','CONSUMED','REVOKED','EXPIRED']::text[]),
    ('session_status'::name, ARRAY['ACTIVE','REVOKED','COMPROMISED','EXPIRED']::text[]),
    ('audit_outcome'::name, ARRAY['SUCCESS','DENIED','FAILURE']::text[]),
    ('outbox_status'::name, ARRAY['PENDING','PUBLISHED','FAILED','DEAD_LETTER']::text[])
)
SELECT pg_temp.assert_true(
  NOT EXISTS (
    SELECT 1
    FROM expected e
    LEFT JOIN LATERAL (
      SELECT array_agg(en.enumlabel::text ORDER BY en.enumsortorder) AS labels
      FROM pg_type t
      JOIN pg_namespace n ON n.oid = t.typnamespace
      JOIN pg_enum en ON en.enumtypid = t.oid
      WHERE n.nspname = 'public' AND t.typname = e.type_name
    ) actual ON true
    WHERE actual.labels IS DISTINCT FROM e.labels
  ),
  'identity_db enum labels must match BD03'
);

SELECT pg_temp.assert_true(
  to_regclass('public.uq_user_emails_active_normalized') IS NOT NULL
  AND to_regclass('public.uq_user_emails_active_primary') IS NOT NULL
  AND to_regclass('public.uq_refresh_tokens_parent_token') IS NOT NULL
  AND to_regclass('public.ix_security_audit_events_occurred_brin') IS NOT NULL,
  'required IAM uniqueness and audit indexes are missing'
);

SELECT pg_temp.assert_true(
  NOT EXISTS (
    SELECT 1
    FROM pg_foreign_table ft
    JOIN pg_class c ON c.oid = ft.ftrelid
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE n.nspname = 'public'
  )
  AND NOT EXISTS (
    SELECT 1
    FROM pg_constraint fk
    JOIN pg_class child ON child.oid = fk.conrelid
    JOIN pg_namespace child_ns ON child_ns.oid = child.relnamespace
    JOIN pg_class parent ON parent.oid = fk.confrelid
    JOIN pg_namespace parent_ns ON parent_ns.oid = parent.relnamespace
    WHERE fk.contype = 'f' AND (child_ns.nspname <> 'public' OR parent_ns.nspname <> 'public')
  ),
  'identity_db must not expose a cross-database/foreign-table dependency'
);

SELECT pg_temp.assert_true(
  NOT EXISTS (
    SELECT 1 FROM pg_roles
    WHERE rolname IN ('s2w_identity_owner','s2w_identity_app','s2w_identity_worker','s2w_identity_readonly')
      AND (rolcanlogin OR rolsuper OR rolcreatedb OR rolcreaterole OR rolbypassrls)
  )
  AND has_database_privilege('s2w_identity_app', current_database(), 'CONNECT')
  AND has_database_privilege('s2w_identity_worker', current_database(), 'CONNECT')
  AND has_database_privilege('s2w_identity_readonly', current_database(), 'CONNECT')
  AND has_table_privilege('s2w_identity_app', 'public.users', 'SELECT, INSERT, UPDATE')
  AND has_table_privilege('s2w_identity_worker', 'public.outbox_delivery_attempts', 'INSERT')
  AND has_table_privilege('s2w_identity_readonly', 'public.roles', 'SELECT')
  AND NOT has_table_privilege('s2w_identity_readonly', 'public.roles', 'UPDATE')
  AND NOT has_schema_privilege('s2w_identity_app', 'public', 'CREATE'),
  'identity NOLOGIN role hardening or minimal grants are incorrect'
);

INSERT INTO users (id, status, display_name)
VALUES ('00000000-0000-0000-0000-000000000101', 'ACTIVE', 'Initial');
INSERT INTO users (id, status)
VALUES ('00000000-0000-0000-0000-000000000102', 'ACTIVE');
INSERT INTO user_emails (id, user_id, email_ciphertext, email_normalized)
VALUES (
  '00000000-0000-0000-0000-000000000111',
  '00000000-0000-0000-0000-000000000101',
  decode('01', 'hex'),
  'tester@example.invalid'
);

DO $$
BEGIN
  BEGIN
    INSERT INTO user_emails (id, user_id, email_ciphertext, email_normalized)
    VALUES (
      '00000000-0000-0000-0000-000000000112',
      '00000000-0000-0000-0000-000000000102',
      decode('02', 'hex'),
      'tester@example.invalid'
    );
    RAISE EXCEPTION 'active normalized email must be unique';
  EXCEPTION WHEN unique_violation THEN
    NULL;
  END;
END
$$;

UPDATE users
SET display_name = 'Changed'
WHERE id = '00000000-0000-0000-0000-000000000101';
SELECT pg_temp.assert_true(
  (SELECT row_version = 2 FROM users WHERE id = '00000000-0000-0000-0000-000000000101'),
  'ENTITY update must increment users.row_version'
);

INSERT INTO outbox_events (
  id, aggregate_type, aggregate_id, event_type, event_version, payload, dedupe_key, trace_id
) VALUES (
  '00000000-0000-0000-0000-000000000121', 'USER',
  '00000000-0000-0000-0000-000000000101', 'USER_TESTED', 1, '{}'::jsonb,
  'assertion-identity-outbox-1', 'trace-identity-assertion'
);
INSERT INTO security_audit_events (
  id, actor_id, subject_id, action, outcome, trace_id, event_hash
) VALUES (
  '00000000-0000-0000-0000-000000000122',
  '00000000-0000-0000-0000-000000000101',
  '00000000-0000-0000-0000-000000000101',
  'ASSERTION', 'SUCCESS', 'trace-identity-assertion', repeat('a', 64)
);

DO $$
BEGIN
  BEGIN
    UPDATE outbox_events SET event_type = 'MUTATED'
    WHERE id = '00000000-0000-0000-0000-000000000121';
    RAISE EXCEPTION 'outbox event update must be rejected';
  EXCEPTION WHEN SQLSTATE '55000' THEN
    NULL;
  END;

  BEGIN
    DELETE FROM security_audit_events
    WHERE id = '00000000-0000-0000-0000-000000000122';
    RAISE EXCEPTION 'audit event delete must be rejected';
  EXCEPTION WHEN SQLSTATE '55000' THEN
    NULL;
  END;
END
$$;

SET LOCAL enable_seqscan = off;
EXPLAIN (COSTS OFF) SELECT id FROM user_emails
WHERE email_normalized = 'tester@example.invalid' AND replaced_at IS NULL;
EXPLAIN (COSTS OFF) SELECT id FROM security_audit_events
WHERE subject_id = '00000000-0000-0000-0000-000000000101'
ORDER BY occurred_at DESC;

ROLLBACK;
