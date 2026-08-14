\set ON_ERROR_STOP on
-- Run as the administrative principal that applied the schema. All fixtures
-- are created inside this transaction and are removed by the final ROLLBACK.

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
    ('identity_projections'), ('file_objects'), ('malware_scan_results'),
    ('candidate_profiles'), ('candidate_search_preferences'), ('skills'),
    ('candidate_skills'), ('candidate_experiences'), ('candidate_educations'),
    ('cvs'), ('cv_versions'), ('portfolio_items'), ('saved_jobs'),
    ('enterprise_tenants'), ('enterprise_verification_cases'), ('enterprise_memberships'),
    ('enterprise_invites'), ('trusted_publisher_grants'), ('university_tenants'),
    ('university_verification_cases'), ('university_memberships'), ('university_invites'),
    ('student_affiliations'), ('cohorts'), ('cohort_memberships'),
    ('internship_programs'), ('campus_job_distributions'), ('partnerships'),
    ('candidate_referrals'), ('data_consent_grants'), ('university_report_runs'),
    ('jobs'), ('job_revisions'), ('job_skill_requirements'), ('job_review_decisions'),
    ('job_status_history'), ('candidate_search_documents'), ('candidate_invitations'),
    ('talent_lists'), ('talent_list_items'), ('applications'), ('application_snapshots'),
    ('application_evidence_selections'), ('evidence_export_requests'),
    ('application_evidence_snapshots'), ('application_status_history'),
    ('application_assignments'), ('application_notes'), ('interviews'),
    ('interview_schedule_versions'), ('interview_participants'),
    ('interview_status_history'), ('conversations'), ('messages'),
    ('conversation_read_cursors'), ('websocket_connection_leases'),
    ('ai_model_versions'), ('ai_prompt_versions'), ('ai_policy_versions'), ('ai_jobs'),
    ('ai_outputs'), ('ai_human_reviews'), ('match_score_snapshots'), ('ai_kill_switches'),
    ('products'), ('product_prices'), ('orders'), ('order_items'), ('payment_attempts'),
    ('payment_webhook_events'), ('payment_reconciliations'), ('refunds'), ('chargebacks'),
    ('entitlements'), ('credit_ledger_entries'), ('promotion_campaigns'),
    ('sponsored_placements'), ('invoices'), ('notification_preferences'),
    ('notifications'), ('notification_deliveries'), ('moderation_reports'),
    ('audit_events'), ('idempotency_keys'), ('outbox_events'), ('consumer_inbox'),
    ('admin_adjustments'), ('tenant_roles'), ('tenant_permissions'),
    ('tenant_role_permissions'), ('application_evidence_state_events'),
    ('outbox_delivery_attempts'), ('internship_program_participants'),
    ('application_offer_versions'), ('application_offer_state_events'),
    ('job_screening_questions'), ('interview_feedback'), ('file_upload_sessions')
), actual(table_name) AS (
  SELECT c.relname
  FROM pg_class c
  JOIN pg_namespace n ON n.oid = c.relnamespace
  WHERE n.nspname = 'public' AND c.relkind = 'r'
)
SELECT pg_temp.assert_true(
  NOT EXISTS (SELECT 1 FROM expected e LEFT JOIN actual a USING (table_name) WHERE a.table_name IS NULL)
  AND NOT EXISTS (SELECT 1 FROM actual a LEFT JOIN expected e USING (table_name) WHERE e.table_name IS NULL),
  'work_db public table inventory must be exactly WRK 76 + AIX 8 + PAY 14'
);

SELECT pg_temp.assert_true(
  (SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
   WHERE n.nspname = 'public' AND c.relkind = 'r'
     AND obj_description(c.oid, 'pg_class') ~ '^TBL-WRK-[0-9]{3}') = 76
  AND (SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
       WHERE n.nspname = 'public' AND c.relkind = 'r'
         AND obj_description(c.oid, 'pg_class') ~ '^TBL-AIX-[0-9]{3}') = 8
  AND (SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
       WHERE n.nspname = 'public' AND c.relkind = 'r'
         AND obj_description(c.oid, 'pg_class') ~ '^TBL-PAY-[0-9]{3}') = 14,
  'all Work, AI and Payment tables must retain their TBL comments'
);

WITH expected(type_name, labels) AS (
  VALUES
    ('account_status'::name, ARRAY['PENDING_EMAIL_VERIFICATION','ACTIVE','SUSPENDED','DELETION_PENDING','ANONYMIZED']::text[]),
    ('audit_outcome'::name, ARRAY['SUCCESS','DENIED','FAILURE']::text[]),
    ('file_asset_status'::name, ARRAY['CREATED','UPLOADING','UPLOADED','SCANNING','CLEAN','INFECTED','SCAN_FAILED','ATTACHED','EXPIRED','DELETED']::text[]),
    ('notification_status'::name, ARRAY['QUEUED','SENT','DELIVERED','FAILED','SUPPRESSED']::text[]),
    ('candidate_visibility'::name, ARRAY['PRIVATE','SEARCHABLE']::text[]),
    ('tenant_status'::name, ARRAY['PENDING_VERIFICATION','VERIFIED','SUSPENDED','REJECTED','CLOSED']::text[]),
    ('membership_status'::name, ARRAY['INVITED','ACTIVE','SUSPENDED','LEFT','REVOKED']::text[]),
    ('cv_revision_status'::name, ARRAY['DRAFT','PUBLISHED','SUPERSEDED','DISCARDED']::text[]),
    ('job_revision_status'::name, ARRAY['DRAFT','REVIEW_PENDING','APPROVED','PUBLISHED','SUPERSEDED','REJECTED','DISCARDED']::text[]),
    ('job_status'::name, ARRAY['DRAFT','REVIEW_PENDING','PUBLISHED','PAUSED','CLOSED','EXPIRED','TAKEN_DOWN']::text[]),
    ('application_status'::name, ARRAY['SUBMITTED','UNDER_REVIEW','SHORTLISTED','INTERVIEWING','OFFERED','HIRED','REJECTED','WITHDRAWN','OFFER_DECLINED']::text[]),
    ('interview_status'::name, ARRAY['PROPOSED','CONFIRMED','CANCELLED','NO_SHOW','COMPLETED']::text[]),
    ('conversation_status'::name, ARRAY['ACTIVE','READ_ONLY']::text[]),
    ('evidence_export_status'::name, ARRAY['PENDING','READY','UNAVAILABLE','HIDDEN','REVOKED']::text[]),
    ('ai_job_status'::name, ARRAY['QUEUED','RUNNING','SUCCEEDED','FAILED','CANCELLED']::text[]),
    ('ai_review_decision'::name, ARRAY['ACCEPTED','EDITED_ACCEPT','REJECTED']::text[]),
    ('order_status'::name, ARRAY['CREATED','PENDING','SETTLED','FAILED','EXPIRED','CANCELLED']::text[]),
    ('payment_status'::name, ARRAY['CREATED','PENDING','SETTLED','FAILED','EXPIRED','CANCELLED']::text[]),
    ('payment_provider'::name, ARRAY['VNPAY','MOMO']::text[]),
    ('entitlement_status'::name, ARRAY['ACTIVE','EXHAUSTED','EXPIRED','FROZEN','REVOKED']::text[]),
    ('ledger_entry_type'::name, ARRAY['GRANT','SPEND','REFUND','EXPIRE','REVERSAL','ADJUSTMENT']::text[]),
    ('promotion_status'::name, ARRAY['SCHEDULED','ACTIVE','PAUSED','ENDED','CANCELLED']::text[]),
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
  'work_db enum labels must match BD03'
);

SELECT pg_temp.assert_true(
  to_regclass('public.applications_tenant_job_status_submitted_idx') IS NOT NULL
  AND to_regclass('public.jobs_status_published_idx') IS NOT NULL
  AND to_regclass('public.candidate_search_documents_vector_gin_idx') IS NOT NULL
  AND to_regclass('public.messages_conversation_sequence_idx') IS NOT NULL
  AND to_regclass('public.payment_webhook_events_processing_received_idx') IS NOT NULL
  AND to_regclass('public.credit_ledger_entries_entitlement_occurred_idx') IS NOT NULL
  AND to_regclass('public.audit_events_occurred_brin_idx') IS NOT NULL
  AND EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'applications_tenant_id_job_id_fkey')
  AND EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'job_revisions_tenant_id_job_id_fkey')
  AND EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'cohort_memberships_tenant_id_cohort_id_fkey'),
  'mandatory Work indexes or composite tenant foreign keys are missing'
);

SELECT pg_temp.assert_true(
  (SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
   WHERE n.nspname = 'public' AND c.relkind = 'r' AND c.relrowsecurity) = 97
  AND NOT EXISTS (
    SELECT 1
    FROM pg_attribute a
    JOIN pg_class c ON c.oid = a.attrelid
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE n.nspname = 'public' AND c.relkind = 'r'
      AND a.attname = 'tenant_id' AND a.attnum > 0 AND NOT a.attisdropped
      AND NOT c.relrowsecurity
  )
  AND NOT EXISTS (
    SELECT 1
    FROM pg_foreign_table ft
    JOIN pg_class c ON c.oid = ft.ftrelid
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE n.nspname = 'public'
  ),
  'tenant RLS or no-cross-database boundary is not configured'
);

SELECT pg_temp.assert_true(
  NOT EXISTS (
    SELECT 1 FROM pg_roles
    WHERE rolname IN ('s2w_work_owner','s2w_work_app','s2w_work_worker','s2w_work_readonly')
      AND (rolcanlogin OR rolsuper OR rolcreatedb OR rolcreaterole OR rolbypassrls)
  )
  AND has_database_privilege('s2w_work_app', current_database(), 'CONNECT')
  AND has_database_privilege('s2w_work_worker', current_database(), 'CONNECT')
  AND has_database_privilege('s2w_work_readonly', current_database(), 'CONNECT')
  AND has_table_privilege('s2w_work_app', 'public.applications', 'SELECT, INSERT, UPDATE, DELETE')
  AND has_table_privilege('s2w_work_worker', 'public.payment_webhook_events', 'INSERT')
  AND has_table_privilege('s2w_work_readonly', 'public.applications', 'SELECT')
  AND NOT has_table_privilege('s2w_work_readonly', 'public.applications', 'UPDATE')
  AND NOT has_schema_privilege('s2w_work_app', 'public', 'CREATE'),
  'Work NOLOGIN role hardening or minimal grants are incorrect'
);

INSERT INTO enterprise_tenants (id, legal_name, display_name, tax_code, slug)
VALUES
  ('00000000-0000-0000-0000-000000000301', 'Assertion Enterprise A', 'Assertion A', 'ASSERT-A', 'assertion-enterprise-a'),
  ('00000000-0000-0000-0000-000000000302', 'Assertion Enterprise B', 'Assertion B', 'ASSERT-B', 'assertion-enterprise-b');
INSERT INTO enterprise_memberships (
  id, tenant_id, identity_subject_id, role_code, status, joined_at
) VALUES (
  '00000000-0000-0000-0000-000000000303',
  '00000000-0000-0000-0000-000000000301',
  '00000000-0000-0000-0000-000000000304', 'OWNER', 'ACTIVE', now()
);
INSERT INTO candidate_profiles (id, identity_subject_id, full_name)
VALUES (
  '00000000-0000-0000-0000-000000000305',
  '00000000-0000-0000-0000-000000000306', 'Assertion Candidate'
);
INSERT INTO jobs (id, tenant_id, slug, created_by_subject_id)
VALUES (
  '00000000-0000-0000-0000-000000000307',
  '00000000-0000-0000-0000-000000000301', 'assertion-job',
  '00000000-0000-0000-0000-000000000304'
);
INSERT INTO job_revisions (
  id, tenant_id, job_id, revision_no, status, title, description_markdown,
  requirements_markdown, employment_type, work_mode, location_codes, content_hash,
  created_by_subject_id
) VALUES (
  '00000000-0000-0000-0000-000000000308',
  '00000000-0000-0000-0000-000000000301',
  '00000000-0000-0000-0000-000000000307', 1, 'DRAFT', 'Assertion Job',
  'Description', 'Requirements', 'FULL_TIME', 'REMOTE', ARRAY['VN-HCM'],
  repeat('c', 64), '00000000-0000-0000-0000-000000000304'
);

DO $$
BEGIN
  BEGIN
    INSERT INTO job_revisions (
      id, tenant_id, job_id, revision_no, title, description_markdown,
      requirements_markdown, employment_type, work_mode, location_codes, content_hash,
      created_by_subject_id
    ) VALUES (
      '00000000-0000-0000-0000-000000000309',
      '00000000-0000-0000-0000-000000000302',
      '00000000-0000-0000-0000-000000000307', 2, 'Cross tenant', 'Description',
      'Requirements', 'FULL_TIME', 'REMOTE', ARRAY['VN-HCM'], repeat('d', 64),
      '00000000-0000-0000-0000-000000000304'
    );
    RAISE EXCEPTION 'cross-tenant job revision must be rejected';
  EXCEPTION WHEN foreign_key_violation THEN
    NULL;
  END;

  BEGIN
    INSERT INTO applications (
      id, tenant_id, candidate_id, job_id, job_revision_id, submitted_at,
      source, last_status_at, consent_policy_version, row_security_key
    ) VALUES (
      '00000000-0000-0000-0000-000000000310',
      '00000000-0000-0000-0000-000000000301',
      '00000000-0000-0000-0000-000000000305',
      '00000000-0000-0000-0000-000000000307',
      '00000000-0000-0000-0000-000000000308', now(), 'SELF', now(), 1,
      '00000000-0000-0000-0000-000000000311'
    );
    RAISE EXCEPTION 'application must reject a DRAFT job revision';
  EXCEPTION WHEN check_violation THEN
    NULL;
  END;
END
$$;

UPDATE job_revisions
SET status = 'PUBLISHED', published_at = now()
WHERE id = '00000000-0000-0000-0000-000000000308';
INSERT INTO applications (
  id, tenant_id, candidate_id, job_id, job_revision_id, submitted_at,
  source, last_status_at, consent_policy_version, row_security_key
) VALUES (
  '00000000-0000-0000-0000-000000000310',
  '00000000-0000-0000-0000-000000000301',
  '00000000-0000-0000-0000-000000000305',
  '00000000-0000-0000-0000-000000000307',
  '00000000-0000-0000-0000-000000000308', now(), 'SELF', now(), 1,
  '00000000-0000-0000-0000-000000000311'
);

DO $$
BEGIN
  BEGIN
    INSERT INTO applications (
      id, tenant_id, candidate_id, job_id, job_revision_id, submitted_at,
      source, last_status_at, consent_policy_version, row_security_key
    ) VALUES (
      '00000000-0000-0000-0000-000000000312',
      '00000000-0000-0000-0000-000000000301',
      '00000000-0000-0000-0000-000000000305',
      '00000000-0000-0000-0000-000000000307',
      '00000000-0000-0000-0000-000000000308', now(), 'SELF', now(), 1,
      '00000000-0000-0000-0000-000000000313'
    );
    RAISE EXCEPTION 'candidate/job application must be unique';
  EXCEPTION WHEN unique_violation THEN
    NULL;
  END;
END
$$;

INSERT INTO saved_jobs (id, candidate_id, job_id, saved_at)
VALUES (
  '00000000-0000-0000-0000-000000000314',
  '00000000-0000-0000-0000-000000000305',
  '00000000-0000-0000-0000-000000000307', now()
);
UPDATE saved_jobs SET removed_at = now()
WHERE id = '00000000-0000-0000-0000-000000000314';

INSERT INTO payment_webhook_events (
  id, provider, provider_event_id, provider_order_id, received_at, signature_valid,
  headers_redacted, payload_ciphertext, payload_hash, trace_id
) VALUES (
  '00000000-0000-0000-0000-000000000315', 'VNPAY', 'assertion-event-1',
  'assertion-order-1', now(), true, '{}'::jsonb, decode('01', 'hex'),
  repeat('e', 64), 'trace-work-assertion'
);

DO $$
BEGIN
  BEGIN
    UPDATE saved_jobs SET removed_at = NULL
    WHERE id = '00000000-0000-0000-0000-000000000314';
    RAISE EXCEPTION 'immutable removal marker must not regress';
  EXCEPTION WHEN SQLSTATE '55000' THEN
    NULL;
  END;
  BEGIN
    INSERT INTO payment_webhook_events (
      id, provider, provider_event_id, provider_order_id, received_at, signature_valid,
      headers_redacted, payload_ciphertext, payload_hash, trace_id
    ) VALUES (
      '00000000-0000-0000-0000-000000000316', 'VNPAY', 'assertion-event-2',
      'assertion-order-1', now(), true, '{}'::jsonb, decode('02', 'hex'),
      repeat('e', 64), 'trace-work-assertion'
    );
    RAISE EXCEPTION 'duplicate webhook payload must be rejected';
  EXCEPTION WHEN unique_violation THEN
    NULL;
  END;
  BEGIN
    UPDATE payment_webhook_events SET processing_status = 'PROCESSED'
    WHERE id = '00000000-0000-0000-0000-000000000315';
    RAISE EXCEPTION 'append-only webhook update must be rejected';
  EXCEPTION WHEN SQLSTATE '55000' THEN
    NULL;
  END;
  BEGIN
    INSERT INTO credit_ledger_entries (
      id, entitlement_id, owner_subject_id, entry_type, quantity_delta,
      balance_after, reference_type, reference_id, idempotency_key
    ) VALUES (
      '00000000-0000-0000-0000-000000000317',
      '00000000-0000-0000-0000-000000000318',
      '00000000-0000-0000-0000-000000000306', 'SPEND', -1, -1,
      'ASSERTION', '00000000-0000-0000-0000-000000000319', 'ledger-negative'
    );
    RAISE EXCEPTION 'ledger balance must not become negative';
  EXCEPTION WHEN check_violation THEN
    NULL;
  END;
END
$$;

SET SESSION AUTHORIZATION s2w_work_app;
RESET app.subject_id;
RESET app.tenant_id;
SELECT pg_temp.assert_true(
  (SELECT count(*) = 0 FROM candidate_profiles)
  AND (SELECT count(*) = 0 FROM jobs),
  'Work RLS must deny subject and tenant rows without GUC context'
);
SET LOCAL app.subject_id = '00000000-0000-0000-0000-000000000306';
SELECT pg_temp.assert_true(
  (SELECT count(*) = 1 FROM candidate_profiles)
  AND (SELECT count(*) = 1 FROM applications),
  'candidate subject context must expose only owned candidate/application rows'
);
SET LOCAL app.subject_id = '00000000-0000-0000-0000-000000000304';
SET LOCAL app.tenant_id = '00000000-0000-0000-0000-000000000301';
SELECT pg_temp.assert_true(
  (SELECT count(*) = 1 FROM jobs WHERE id = '00000000-0000-0000-0000-000000000307'),
  'active tenant membership with matching tenant GUC must access tenant row'
);
SET LOCAL app.tenant_id = '00000000-0000-0000-0000-000000000302';
SELECT pg_temp.assert_true(
  (SELECT count(*) = 0 FROM jobs WHERE id = '00000000-0000-0000-0000-000000000307'),
  'tenant mismatch must be denied even when a row UUID is known'
);
RESET SESSION AUTHORIZATION;

SET LOCAL enable_seqscan = off;
EXPLAIN (COSTS OFF) SELECT id FROM applications
WHERE tenant_id = '00000000-0000-0000-0000-000000000301'
  AND job_id = '00000000-0000-0000-0000-000000000307'
  AND status = 'SUBMITTED';
EXPLAIN (COSTS OFF) SELECT id FROM jobs
WHERE status = 'PUBLISHED' AND published_at IS NOT NULL;
EXPLAIN (COSTS OFF) SELECT id FROM payment_webhook_events
WHERE processing_status = 'RECEIVED' ORDER BY received_at, id;

ROLLBACK;
