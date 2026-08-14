\set ON_ERROR_STOP on
-- Run as the administrative principal that applied the schema. All fixtures
-- are inside this transaction and are removed by the final ROLLBACK.

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
    ('identity_projections'), ('learner_profiles'), ('service_roles'),
    ('service_permissions'), ('service_role_permissions'), ('service_role_assignments'),
    ('onboarding_submissions'), ('path_recommendation_runs'), ('learning_paths'),
    ('learning_path_versions'), ('courses'), ('course_versions'), ('path_course_items'),
    ('chapters'), ('lessons'), ('content_blocks'), ('content_rights_attestations'),
    ('content_review_decisions'), ('trusted_publisher_grants'), ('assessments'),
    ('assessment_placements'), ('quiz_questions'), ('quiz_options'), ('rubrics'),
    ('rubric_criteria'), ('primary_path_periods'), ('course_enrollments'),
    ('block_progress_facts'), ('lesson_progress_facts'), ('progress_snapshots'),
    ('course_completions'), ('path_completions'), ('assessment_attempts'),
    ('assessment_answers'), ('file_objects'), ('malware_scan_results'), ('attempt_files'),
    ('assessment_reviews'), ('assessment_review_scores'), ('evidence_records'),
    ('evidence_export_requests'), ('notification_preferences'), ('notifications'),
    ('notification_deliveries'), ('community_channels'), ('community_acceptances'),
    ('support_tickets'), ('support_messages'), ('admin_adjustments'), ('audit_events'),
    ('idempotency_keys'), ('outbox_events'), ('consumer_inbox'), ('report_snapshots'),
    ('outbox_delivery_attempts'), ('study_skills'), ('course_skill_outcomes'),
    ('course_prerequisites'), ('file_upload_sessions'), ('assessment_drafts')
), actual(table_name) AS (
  SELECT c.relname
  FROM pg_class c
  JOIN pg_namespace n ON n.oid = c.relnamespace
  WHERE n.nspname = 'public' AND c.relkind = 'r'
)
SELECT pg_temp.assert_true(
  NOT EXISTS (SELECT 1 FROM expected e LEFT JOIN actual a USING (table_name) WHERE a.table_name IS NULL)
  AND NOT EXISTS (SELECT 1 FROM actual a LEFT JOIN expected e USING (table_name) WHERE e.table_name IS NULL),
  'study_db public table inventory must be exactly TBL-STU-001..060'
);

SELECT pg_temp.assert_true(
  (SELECT count(*)
   FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
   WHERE n.nspname = 'public' AND c.relkind = 'r'
     AND obj_description(c.oid, 'pg_class') ~ '^TBL-STU-[0-9]{3}') = 60,
  'all Study tables must retain a TBL-STU comment'
);

WITH expected(type_name, labels) AS (
  VALUES
    ('account_status'::name, ARRAY['PENDING_EMAIL_VERIFICATION','ACTIVE','SUSPENDED','DELETION_PENDING','ANONYMIZED']::text[]),
    ('audit_outcome'::name, ARRAY['SUCCESS','DENIED','FAILURE']::text[]),
    ('content_version_status'::name, ARRAY['DRAFT','PUBLISHED','SUPERSEDED','DISCARDED']::text[]),
    ('primary_path_status'::name, ARRAY['ACTIVE','SWITCHED_OUT','COMPLETED','CANCELLED_BY_ADMIN']::text[]),
    ('enrollment_status'::name, ARRAY['ENROLLED','IN_PROGRESS','COMPLETED']::text[]),
    ('progress_status'::name, ARRAY['NOT_STARTED','IN_PROGRESS','COMPLETED']::text[]),
    ('assessment_type'::name, ARRAY['QUIZ','TEXT','LINK','FILE']::text[]),
    ('attempt_status'::name, ARRAY['SUBMITTED','UNDER_REVIEW','PASSED','NEEDS_REVISION','FAILED']::text[]),
    ('review_decision'::name, ARRAY['PASSED','NEEDS_REVISION','FAILED']::text[]),
    ('file_asset_status'::name, ARRAY['CREATED','UPLOADING','UPLOADED','SCANNING','CLEAN','INFECTED','SCAN_FAILED','ATTACHED','EXPIRED','DELETED']::text[]),
    ('evidence_status'::name, ARRAY['ISSUED','REVOKED']::text[]),
    ('notification_status'::name, ARRAY['QUEUED','SENT','DELIVERED','FAILED','SUPPRESSED']::text[]),
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
  'study_db enum labels must match BD03'
);

SELECT pg_temp.assert_true(
  to_regclass('public.ux_primary_path_periods_active') IS NOT NULL
  AND to_regclass('public.ix_course_versions_catalog_fts') IS NOT NULL
  AND to_regclass('public.ix_study_skills_normalized_name_trgm') IS NOT NULL
  AND to_regclass('public.ix_notifications_inbox_cursor') IS NOT NULL
  AND to_regclass('public.ix_audit_events_occurred_brin') IS NOT NULL
  AND EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_learning_paths_current_draft_same_path'),
  'required Study indexes or deferred same-aggregate FK are missing'
);

SELECT pg_temp.assert_true(
  (SELECT count(*)
   FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
   WHERE n.nspname = 'public' AND c.relkind = 'r' AND c.relrowsecurity) = 27
  AND NOT EXISTS (
    SELECT 1
    FROM pg_foreign_table ft
    JOIN pg_class c ON c.oid = ft.ftrelid
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE n.nspname = 'public'
  ),
  'Study subject RLS or no-cross-database boundary is not configured'
);

SELECT pg_temp.assert_true(
  NOT EXISTS (
    SELECT 1 FROM pg_roles
    WHERE rolname IN ('s2w_study_owner','s2w_study_app','s2w_study_worker','s2w_study_readonly')
      AND (rolcanlogin OR rolsuper OR rolcreatedb OR rolcreaterole OR rolbypassrls)
  )
  AND has_database_privilege('s2w_study_app', current_database(), 'CONNECT')
  AND has_database_privilege('s2w_study_worker', current_database(), 'CONNECT')
  AND has_database_privilege('s2w_study_readonly', current_database(), 'CONNECT')
  AND has_table_privilege('s2w_study_app', 'public.learner_profiles', 'SELECT, INSERT, UPDATE, DELETE')
  AND has_table_privilege('s2w_study_worker', 'public.outbox_delivery_attempts', 'INSERT')
  AND has_table_privilege('s2w_study_readonly', 'public.learner_profiles', 'SELECT')
  AND NOT has_table_privilege('s2w_study_readonly', 'public.learner_profiles', 'UPDATE')
  AND NOT has_schema_privilege('s2w_study_app', 'public', 'CREATE'),
  'Study NOLOGIN role hardening or minimal grants are incorrect'
);

INSERT INTO learner_profiles (id, identity_subject_id, full_name)
VALUES
  ('00000000-0000-0000-0000-000000000201', '00000000-0000-0000-0000-000000000211', 'Learner One'),
  ('00000000-0000-0000-0000-000000000202', '00000000-0000-0000-0000-000000000212', 'Learner Two');

UPDATE learner_profiles
SET headline = 'Row version assertion'
WHERE id = '00000000-0000-0000-0000-000000000201';
SELECT pg_temp.assert_true(
  (SELECT row_version = 2 FROM learner_profiles WHERE id = '00000000-0000-0000-0000-000000000201'),
  'ENTITY update must increment learner_profiles.row_version'
);

INSERT INTO learning_paths (id, slug, owner_subject_id)
VALUES ('00000000-0000-0000-0000-000000000221', 'assertion-path', '00000000-0000-0000-0000-000000000211');
INSERT INTO learning_path_versions (
  id, path_id, version_no, status, title, summary, description_markdown,
  estimated_hours, content_hash, created_by_subject_id, published_at
) VALUES (
  '00000000-0000-0000-0000-000000000222',
  '00000000-0000-0000-0000-000000000221', 1, 'PUBLISHED', 'Assertion Path',
  'Assertion summary', 'Assertion description', 1, repeat('a', 64),
  '00000000-0000-0000-0000-000000000211', now()
);
INSERT INTO primary_path_periods (id, learner_id, path_version_id, status, started_at)
VALUES (
  '00000000-0000-0000-0000-000000000223',
  '00000000-0000-0000-0000-000000000201',
  '00000000-0000-0000-0000-000000000222', 'ACTIVE', now()
);

DO $$
BEGIN
  BEGIN
    INSERT INTO primary_path_periods (id, learner_id, path_version_id, status, started_at)
    VALUES (
      '00000000-0000-0000-0000-000000000224',
      '00000000-0000-0000-0000-000000000201',
      '00000000-0000-0000-0000-000000000222', 'ACTIVE', now()
    );
    RAISE EXCEPTION 'a learner must not have two ACTIVE primary paths';
  EXCEPTION WHEN unique_violation OR exclusion_violation THEN
    NULL;
  END;
END
$$;

INSERT INTO onboarding_submissions (id, learner_id, schema_version, answers, submitted_at)
VALUES (
  '00000000-0000-0000-0000-000000000225',
  '00000000-0000-0000-0000-000000000201', 1, '{}'::jsonb, now()
);
INSERT INTO audit_events (id, actor_subject_id, action, resource_type, outcome, business_code, trace_id, event_hash)
VALUES (
  '00000000-0000-0000-0000-000000000226',
  '00000000-0000-0000-0000-000000000211', 'ASSERTION', 'LEARNER', 'SUCCESS',
  'ASSERTION_OK', 'trace-study-assertion', repeat('b', 64)
);

DO $$
BEGIN
  BEGIN
    UPDATE onboarding_submissions SET answers = '{"mutated":true}'::jsonb
    WHERE id = '00000000-0000-0000-0000-000000000225';
    RAISE EXCEPTION 'onboarding submission update must be rejected';
  EXCEPTION WHEN SQLSTATE '55000' THEN
    NULL;
  END;
  BEGIN
    DELETE FROM audit_events WHERE id = '00000000-0000-0000-0000-000000000226';
    RAISE EXCEPTION 'audit event delete must be rejected';
  EXCEPTION WHEN SQLSTATE '55000' THEN
    NULL;
  END;
END
$$;

SET LOCAL ROLE s2w_study_app;
RESET app.subject_id;
SELECT pg_temp.assert_true(
  (SELECT count(*) = 0 FROM learner_profiles),
  'Study RLS must deny learner rows with no subject context'
);
SET LOCAL app.subject_id = '00000000-0000-0000-0000-000000000211';
SELECT pg_temp.assert_true(
  (SELECT count(*) = 1 FROM learner_profiles)
  AND (SELECT count(*) = 0 FROM learner_profiles WHERE id = '00000000-0000-0000-0000-000000000202'),
  'Study RLS must expose only the current learner subject'
);
RESET ROLE;

SET LOCAL enable_seqscan = off;
EXPLAIN (COSTS OFF) SELECT id FROM primary_path_periods
WHERE learner_id = '00000000-0000-0000-0000-000000000201' AND status = 'ACTIVE';
EXPLAIN (COSTS OFF) SELECT id FROM notifications
WHERE learner_id = '00000000-0000-0000-0000-000000000201'
ORDER BY read_at ASC NULLS LAST, created_at DESC, id DESC
LIMIT 100;

ROLLBACK;
