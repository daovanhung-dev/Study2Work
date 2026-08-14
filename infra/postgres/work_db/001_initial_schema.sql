-- Study2Work V1-PILOT: work_db initial schema (PostgreSQL 16)
-- Source of truth: docs/BD/03_THIET_KE_CO_SO_DU_LIEU.md, sections 1--14.
-- This script intentionally creates no database, LOGIN role, seed data, or
-- cross-database foreign key.  Execute it against an empty work_db as a
-- principal permitted to create roles, extensions, schemas, and objects.
-- Source gaps intentionally not modeled: historical candidate-search consent,
-- public-job slug semantics, entitlement reservation/hold and refund-approval
-- history, promotion raw impression/click events, and AI evaluation or
-- kill-switch execution state. These require an approved BD update.

BEGIN;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 's2w_work_owner') THEN
    CREATE ROLE s2w_work_owner NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 's2w_work_app') THEN
    CREATE ROLE s2w_work_app NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 's2w_work_worker') THEN
    CREATE ROLE s2w_work_worker NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 's2w_work_readonly') THEN
    CREATE ROLE s2w_work_readonly NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS;
  END IF;
END
$$;

GRANT s2w_work_owner TO CURRENT_USER;
ALTER ROLE s2w_work_owner NOBYPASSRLS;
ALTER ROLE s2w_work_app NOBYPASSRLS;
ALTER ROLE s2w_work_worker NOBYPASSRLS;
ALTER ROLE s2w_work_readonly NOBYPASSRLS;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS btree_gist;
REVOKE ALL ON DATABASE work_db FROM PUBLIC;
GRANT CONNECT ON DATABASE work_db TO s2w_work_owner, s2w_work_app, s2w_work_worker, s2w_work_readonly;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
ALTER SCHEMA public OWNER TO s2w_work_owner;
CREATE SCHEMA IF NOT EXISTS app_private AUTHORIZATION s2w_work_owner;
REVOKE ALL ON SCHEMA app_private FROM PUBLIC;

SET ROLE s2w_work_owner;
SET search_path = public, app_private;

CREATE TYPE account_status AS ENUM (
  'PENDING_EMAIL_VERIFICATION', 'ACTIVE', 'SUSPENDED', 'DELETION_PENDING', 'ANONYMIZED'
);
CREATE TYPE audit_outcome AS ENUM ('SUCCESS', 'DENIED', 'FAILURE');
CREATE TYPE file_asset_status AS ENUM (
  'CREATED', 'UPLOADING', 'UPLOADED', 'SCANNING', 'CLEAN', 'INFECTED', 'SCAN_FAILED',
  'ATTACHED', 'EXPIRED', 'DELETED'
);
CREATE TYPE notification_status AS ENUM ('QUEUED', 'SENT', 'DELIVERED', 'FAILED', 'SUPPRESSED');
CREATE TYPE candidate_visibility AS ENUM ('PRIVATE', 'SEARCHABLE');
CREATE TYPE tenant_status AS ENUM (
  'PENDING_VERIFICATION', 'VERIFIED', 'SUSPENDED', 'REJECTED', 'CLOSED'
);
CREATE TYPE membership_status AS ENUM ('INVITED', 'ACTIVE', 'SUSPENDED', 'LEFT', 'REVOKED');
CREATE TYPE cv_revision_status AS ENUM ('DRAFT', 'PUBLISHED', 'SUPERSEDED', 'DISCARDED');
CREATE TYPE job_revision_status AS ENUM (
  'DRAFT', 'REVIEW_PENDING', 'APPROVED', 'PUBLISHED', 'SUPERSEDED', 'REJECTED', 'DISCARDED'
);
CREATE TYPE job_status AS ENUM (
  'DRAFT', 'REVIEW_PENDING', 'PUBLISHED', 'PAUSED', 'CLOSED', 'EXPIRED', 'TAKEN_DOWN'
);
CREATE TYPE application_status AS ENUM (
  'SUBMITTED', 'UNDER_REVIEW', 'SHORTLISTED', 'INTERVIEWING', 'OFFERED', 'HIRED',
  'REJECTED', 'WITHDRAWN', 'OFFER_DECLINED'
);
CREATE TYPE interview_status AS ENUM ('PROPOSED', 'CONFIRMED', 'CANCELLED', 'NO_SHOW', 'COMPLETED');
CREATE TYPE conversation_status AS ENUM ('ACTIVE', 'READ_ONLY');
CREATE TYPE evidence_export_status AS ENUM ('PENDING', 'READY', 'UNAVAILABLE', 'HIDDEN', 'REVOKED');
CREATE TYPE ai_job_status AS ENUM ('QUEUED', 'RUNNING', 'SUCCEEDED', 'FAILED', 'CANCELLED');
CREATE TYPE ai_review_decision AS ENUM ('ACCEPTED', 'EDITED_ACCEPT', 'REJECTED');
CREATE TYPE order_status AS ENUM ('CREATED', 'PENDING', 'SETTLED', 'FAILED', 'EXPIRED', 'CANCELLED');
CREATE TYPE payment_status AS ENUM ('CREATED', 'PENDING', 'SETTLED', 'FAILED', 'EXPIRED', 'CANCELLED');
CREATE TYPE payment_provider AS ENUM ('VNPAY', 'MOMO');
CREATE TYPE entitlement_status AS ENUM ('ACTIVE', 'EXHAUSTED', 'EXPIRED', 'FROZEN', 'REVOKED');
CREATE TYPE ledger_entry_type AS ENUM ('GRANT', 'SPEND', 'REFUND', 'EXPIRE', 'REVERSAL', 'ADJUSTMENT');
CREATE TYPE promotion_status AS ENUM ('SCHEDULED', 'ACTIVE', 'PAUSED', 'ENDED', 'CANCELLED');
CREATE TYPE outbox_status AS ENUM ('PENDING', 'PUBLISHED', 'FAILED', 'DEAD_LETTER');

CREATE FUNCTION app_private.touch_entity()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  NEW.updated_at := now();
  NEW.row_version := OLD.row_version + 1;
  RETURN NEW;
END;
$$;

CREATE FUNCTION app_private.reject_append_mutation()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  RAISE EXCEPTION '% is append-only', TG_TABLE_NAME USING ERRCODE = '55000';
END;
$$;

CREATE FUNCTION app_private.immutable_columns_only()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  changed_column text;
  old_document jsonb;
  new_document jsonb;
BEGIN
  IF TG_OP = 'DELETE' THEN
    RAISE EXCEPTION '% is immutable and cannot be deleted', TG_TABLE_NAME USING ERRCODE = '55000';
  END IF;
  old_document := to_jsonb(OLD);
  new_document := to_jsonb(NEW);
  FOR changed_column IN
    SELECT n.key
    FROM jsonb_each(new_document) AS n
    WHERE (old_document -> n.key) IS DISTINCT FROM n.value
  LOOP
    IF TG_NARGS = 0 OR changed_column <> ALL (TG_ARGV) THEN
      RAISE EXCEPTION '% column % is immutable', TG_TABLE_NAME, changed_column USING ERRCODE = '55000';
    END IF;
    IF old_document -> changed_column <> 'null'::jsonb THEN
      RAISE EXCEPTION '% column % is write-once and may not regress', TG_TABLE_NAME, changed_column
        USING ERRCODE = '55000';
    END IF;
  END LOOP;
  RETURN NEW;
END;
$$;

CREATE FUNCTION app_private.require_clean_file()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  checked_file_id uuid;
BEGIN
  checked_file_id := NULLIF(to_jsonb(NEW) ->> TG_ARGV[0], '')::uuid;
  IF checked_file_id IS NOT NULL
     AND NOT EXISTS (
       SELECT 1 FROM public.file_objects f
       WHERE f.id = checked_file_id AND f.scan_status = 'CLEAN'
     ) THEN
    RAISE EXCEPTION 'file in %.% must be CLEAN', TG_TABLE_NAME, TG_ARGV[0]
      USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END;
$$;

-- TBL-WRK-001 through TBL-WRK-013: identity projection, candidates and CVs.
CREATE TABLE identity_projections (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  identity_subject_id uuid NOT NULL UNIQUE,
  account_status account_status NOT NULL,
  email_verified boolean NOT NULL DEFAULT false,
  display_name varchar(120),
  identity_version bigint NOT NULL CHECK (identity_version >= 1),
  last_event_id uuid NOT NULL UNIQUE,
  projected_at timestamptz NOT NULL
);
COMMENT ON TABLE identity_projections IS 'TBL-WRK-001 — identity projection synchronized from identity_db; no cross-database FK.';
CREATE INDEX identity_projections_status_projected_idx ON identity_projections (account_status, projected_at DESC);

CREATE TABLE file_objects (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  owner_subject_id uuid NOT NULL,
  tenant_id uuid,
  purpose varchar(40) NOT NULL CHECK (purpose IN (
    'AVATAR', 'CV', 'PORTFOLIO', 'ENTERPRISE_LOGO', 'UNIVERSITY_LOGO', 'VERIFICATION', 'JOB', 'INVOICE'
  )),
  storage_key varchar(700) NOT NULL UNIQUE,
  original_name varchar(255) NOT NULL,
  declared_mime varchar(120) NOT NULL,
  detected_mime varchar(120),
  size_bytes bigint NOT NULL CHECK (size_bytes > 0),
  sha256 char(64) NOT NULL,
  scan_status file_asset_status NOT NULL DEFAULT 'CREATED',
  uploaded_at timestamptz,
  available_at timestamptz,
  quarantined_at timestamptz,
  expires_at timestamptz,
  deleted_at timestamptz,
  CHECK (sha256 ~ '^[0-9a-fA-F]{64}$')
);
COMMENT ON TABLE file_objects IS 'TBL-WRK-002 — file metadata only; object storage is external.';
CREATE INDEX file_objects_owner_purpose_created_idx ON file_objects (owner_subject_id, purpose, created_at DESC);
CREATE INDEX file_objects_tenant_purpose_created_idx ON file_objects (tenant_id, purpose, created_at DESC);
CREATE INDEX file_objects_scan_created_idx ON file_objects (scan_status, created_at);
CREATE INDEX file_objects_expires_idx ON file_objects (expires_at);

CREATE TABLE malware_scan_results (
  id uuid PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  file_id uuid NOT NULL REFERENCES file_objects(id) ON DELETE RESTRICT,
  scanner varchar(40) NOT NULL DEFAULT 'CLAMAV',
  engine_version varchar(80) NOT NULL,
  signature_version varchar(80) NOT NULL,
  result file_asset_status NOT NULL CHECK (result IN ('CLEAN', 'INFECTED', 'SCAN_FAILED')),
  detected_mime varchar(120),
  threat_name varchar(200),
  error_code varchar(80),
  scan_duration_ms integer NOT NULL CHECK (scan_duration_ms >= 0),
  worker_id varchar(120) NOT NULL,
  CHECK (result <> 'INFECTED' OR threat_name IS NOT NULL)
);
COMMENT ON TABLE malware_scan_results IS 'TBL-WRK-003 — append-only malware scan evidence.';
CREATE INDEX malware_scan_results_file_occurred_idx ON malware_scan_results (file_id, occurred_at DESC);
CREATE INDEX malware_scan_results_result_occurred_idx ON malware_scan_results (result, occurred_at);

CREATE TABLE candidate_profiles (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  identity_subject_id uuid NOT NULL UNIQUE,
  full_name varchar(160),
  headline varchar(200),
  summary text,
  phone_ciphertext bytea,
  phone_last4 char(4),
  city_code varchar(20),
  country_code char(2) NOT NULL DEFAULT 'VN',
  avatar_file_id uuid REFERENCES file_objects(id) ON DELETE RESTRICT,
  visibility candidate_visibility NOT NULL DEFAULT 'PRIVATE',
  search_opted_in_at timestamptz,
  search_opted_out_at timestamptz,
  available_from date,
  deleted_at timestamptz,
  CHECK (
    (visibility <> 'SEARCHABLE' OR search_opted_in_at IS NOT NULL)
    AND (search_opted_in_at IS NULL OR visibility <> 'PRIVATE' OR search_opted_out_at IS NOT NULL)
  )
);
COMMENT ON TABLE candidate_profiles IS 'TBL-WRK-004 — candidate PII and explicit search preference.';
CREATE INDEX candidate_profiles_visibility_updated_idx ON candidate_profiles (visibility, updated_at DESC);
CREATE INDEX candidate_profiles_city_visibility_idx ON candidate_profiles (city_code, visibility);
CREATE INDEX candidate_profiles_deleted_idx ON candidate_profiles (deleted_at);

CREATE TABLE candidate_search_preferences (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  candidate_id uuid NOT NULL UNIQUE REFERENCES candidate_profiles(id) ON DELETE RESTRICT,
  desired_titles varchar(120)[] NOT NULL DEFAULT '{}',
  desired_locations varchar(20)[] NOT NULL DEFAULT '{}',
  work_modes varchar(16)[] NOT NULL DEFAULT '{}',
  employment_types varchar(24)[] NOT NULL DEFAULT '{}',
  salary_min_vnd bigint CHECK (salary_min_vnd >= 0),
  salary_visibility boolean NOT NULL DEFAULT false,
  notice_days integer CHECK (notice_days BETWEEN 0 AND 365),
  excluded_enterprise_ids uuid[] NOT NULL DEFAULT '{}',
  CHECK (cardinality(desired_titles) <= 20),
  CHECK (cardinality(desired_locations) <= 20),
  CHECK (cardinality(work_modes) <= 5),
  CHECK (cardinality(employment_types) <= 10),
  CHECK (cardinality(excluded_enterprise_ids) <= 200)
);
COMMENT ON TABLE candidate_search_preferences IS 'TBL-WRK-005 — candidate search preferences.';
CREATE INDEX candidate_search_preferences_titles_gin_idx ON candidate_search_preferences USING gin (desired_titles);
CREATE INDEX candidate_search_preferences_locations_gin_idx ON candidate_search_preferences USING gin (desired_locations);
CREATE INDEX candidate_search_preferences_modes_gin_idx ON candidate_search_preferences USING gin (work_modes);
CREATE INDEX candidate_search_preferences_types_gin_idx ON candidate_search_preferences USING gin (employment_types);

CREATE TABLE skills (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  slug varchar(120) NOT NULL UNIQUE CHECK (slug ~ '^[a-z0-9]+(?:-[a-z0-9]+)*$'),
  name varchar(160) NOT NULL,
  normalized_name varchar(160) NOT NULL UNIQUE,
  category varchar(80),
  status varchar(16) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'ARCHIVED')),
  aliases varchar(160)[] NOT NULL DEFAULT '{}'
);
COMMENT ON TABLE skills IS 'TBL-WRK-006 — public skills catalogue.';
CREATE INDEX skills_normalized_name_trgm_idx ON skills USING gin (normalized_name gin_trgm_ops);
CREATE INDEX skills_aliases_gin_idx ON skills USING gin (aliases);

CREATE TABLE candidate_skills (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  candidate_id uuid NOT NULL REFERENCES candidate_profiles(id) ON DELETE RESTRICT,
  skill_id uuid NOT NULL REFERENCES skills(id) ON DELETE RESTRICT,
  proficiency smallint CHECK (proficiency BETWEEN 1 AND 5),
  years_experience numeric(4,1) CHECK (years_experience BETWEEN 0 AND 80),
  last_used_year smallint,
  source varchar(24) NOT NULL CHECK (source IN ('SELF', 'CV_PARSED', 'ADMIN')),
  is_visible boolean NOT NULL DEFAULT true,
  UNIQUE (candidate_id, skill_id)
);
COMMENT ON TABLE candidate_skills IS 'TBL-WRK-007 — candidate skills, including unconfirmed parsed suggestions.';
CREATE INDEX candidate_skills_visible_skill_candidate_idx ON candidate_skills (skill_id, candidate_id) WHERE is_visible;
CREATE INDEX candidate_skills_candidate_updated_idx ON candidate_skills (candidate_id, updated_at DESC);

CREATE TABLE candidate_experiences (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  candidate_id uuid NOT NULL REFERENCES candidate_profiles(id) ON DELETE RESTRICT,
  company_name varchar(200) NOT NULL,
  title varchar(160) NOT NULL,
  start_date date NOT NULL,
  end_date date,
  is_current boolean NOT NULL DEFAULT false,
  description text,
  position integer NOT NULL,
  visibility varchar(16) NOT NULL DEFAULT 'PRIVATE' CHECK (visibility IN ('PRIVATE', 'SEARCH')),
  UNIQUE (candidate_id, position),
  CHECK (end_date IS NULL OR end_date >= start_date),
  CHECK (NOT is_current OR end_date IS NULL)
);
COMMENT ON TABLE candidate_experiences IS 'TBL-WRK-008 — candidate employment history.';
CREATE INDEX candidate_experiences_candidate_position_idx ON candidate_experiences (candidate_id, position);

CREATE TABLE candidate_educations (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  candidate_id uuid NOT NULL REFERENCES candidate_profiles(id) ON DELETE RESTRICT,
  institution_name varchar(240) NOT NULL,
  degree varchar(160),
  field_of_study varchar(160),
  start_date date,
  end_date date,
  description varchar(2000),
  position integer NOT NULL,
  visibility varchar(16) NOT NULL DEFAULT 'PRIVATE' CHECK (visibility IN ('PRIVATE', 'SEARCH')),
  UNIQUE (candidate_id, position),
  CHECK (end_date IS NULL OR start_date IS NULL OR end_date >= start_date)
);
COMMENT ON TABLE candidate_educations IS 'TBL-WRK-009 — candidate education history.';
CREATE INDEX candidate_educations_candidate_position_idx ON candidate_educations (candidate_id, position);

CREATE TABLE cvs (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  candidate_id uuid NOT NULL REFERENCES candidate_profiles(id) ON DELETE RESTRICT,
  title varchar(160) NOT NULL,
  is_default boolean NOT NULL DEFAULT false,
  current_draft_version_id uuid,
  latest_published_version_id uuid,
  archived_at timestamptz
);
COMMENT ON TABLE cvs IS 'TBL-WRK-010 — CV aggregate root.';
CREATE UNIQUE INDEX cvs_one_default_active_idx ON cvs (candidate_id) WHERE is_default AND archived_at IS NULL;
CREATE INDEX cvs_candidate_archived_updated_idx ON cvs (candidate_id, archived_at, updated_at DESC);

CREATE TABLE cv_versions (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  cv_id uuid NOT NULL REFERENCES cvs(id) ON DELETE RESTRICT,
  version_no integer NOT NULL CHECK (version_no >= 1),
  status cv_revision_status NOT NULL DEFAULT 'DRAFT',
  template_code varchar(80) NOT NULL,
  template_version integer NOT NULL CHECK (template_version >= 1),
  content_json jsonb NOT NULL,
  rendered_file_id uuid REFERENCES file_objects(id) ON DELETE RESTRICT,
  source_file_id uuid REFERENCES file_objects(id) ON DELETE RESTRICT,
  content_hash char(64) NOT NULL,
  created_by_subject_id uuid NOT NULL,
  published_at timestamptz,
  superseded_at timestamptz,
  discarded_at timestamptz,
  source_version_id uuid REFERENCES cv_versions(id) ON DELETE RESTRICT,
  UNIQUE (cv_id, version_no),
  CHECK (content_hash ~ '^[0-9a-fA-F]{64}$'),
  CHECK (status <> 'PUBLISHED' OR (published_at IS NOT NULL AND rendered_file_id IS NOT NULL))
);
COMMENT ON TABLE cv_versions IS 'TBL-WRK-011 — versioned CV content; non-draft revisions are immutable.';
CREATE INDEX cv_versions_cv_status_version_idx ON cv_versions (cv_id, status, version_no DESC);

CREATE TABLE portfolio_items (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  candidate_id uuid NOT NULL REFERENCES candidate_profiles(id) ON DELETE RESTRICT,
  title varchar(200) NOT NULL,
  description text,
  url varchar(2048),
  file_id uuid REFERENCES file_objects(id) ON DELETE RESTRICT,
  position integer NOT NULL,
  visibility varchar(16) NOT NULL DEFAULT 'PRIVATE'
    CHECK (visibility IN ('PRIVATE', 'SEARCH', 'APPLICATION_ONLY')),
  published_at timestamptz,
  archived_at timestamptz,
  UNIQUE (candidate_id, position),
  CHECK (
    (url IS NOT NULL AND file_id IS NULL AND url ~ '^https://')
    OR (url IS NULL AND file_id IS NOT NULL)
  )
);
COMMENT ON TABLE portfolio_items IS 'TBL-WRK-012 — candidate portfolio item.';
CREATE INDEX portfolio_items_candidate_archived_position_idx ON portfolio_items (candidate_id, archived_at, position);

CREATE TABLE saved_jobs (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  candidate_id uuid NOT NULL REFERENCES candidate_profiles(id) ON DELETE RESTRICT,
  job_id uuid NOT NULL,
  saved_at timestamptz NOT NULL,
  removed_at timestamptz
);
COMMENT ON TABLE saved_jobs IS 'TBL-WRK-013 — immutable save record with one-way removal marker.';
CREATE UNIQUE INDEX saved_jobs_active_candidate_job_idx ON saved_jobs (candidate_id, job_id) WHERE removed_at IS NULL;
CREATE INDEX saved_jobs_candidate_removed_saved_idx ON saved_jobs (candidate_id, removed_at, saved_at DESC);

-- TBL-WRK-014 through TBL-WRK-031: enterprise/university tenancy and consent.
CREATE TABLE enterprise_tenants (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  legal_name varchar(240) NOT NULL,
  display_name varchar(200) NOT NULL,
  tax_code varchar(32) NOT NULL,
  tax_code_country char(2) NOT NULL DEFAULT 'VN',
  slug varchar(120) NOT NULL UNIQUE,
  status tenant_status NOT NULL DEFAULT 'PENDING_VERIFICATION',
  website_url varchar(2048),
  description text,
  logo_file_id uuid REFERENCES file_objects(id) ON DELETE RESTRICT,
  verified_at timestamptz,
  suspended_at timestamptz,
  closed_at timestamptz,
  UNIQUE (tax_code_country, tax_code),
  CHECK (status <> 'VERIFIED' OR verified_at IS NOT NULL),
  CHECK (website_url IS NULL OR website_url ~ '^https://')
);
COMMENT ON TABLE enterprise_tenants IS 'TBL-WRK-014 — enterprise tenancy aggregate root.';
CREATE INDEX enterprise_tenants_status_created_idx ON enterprise_tenants (status, created_at DESC);
CREATE INDEX enterprise_tenants_display_name_trgm_idx ON enterprise_tenants USING gin (display_name gin_trgm_ops);

CREATE TABLE enterprise_verification_cases (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL REFERENCES enterprise_tenants(id) ON DELETE RESTRICT,
  case_no integer NOT NULL CHECK (case_no >= 1),
  status varchar(24) NOT NULL DEFAULT 'SUBMITTED'
    CHECK (status IN ('SUBMITTED', 'IN_REVIEW', 'APPROVED', 'REJECTED', 'EXPIRED')),
  submitted_by_subject_id uuid NOT NULL,
  document_file_ids uuid[] NOT NULL CHECK (cardinality(document_file_ids) > 0),
  submitted_snapshot jsonb NOT NULL,
  reviewer_subject_id uuid,
  reviewed_at timestamptz,
  decision_reason_codes varchar(80)[] NOT NULL DEFAULT '{}',
  comment varchar(2000),
  expires_at timestamptz,
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, case_no),
  CHECK (
    status NOT IN ('APPROVED', 'REJECTED', 'EXPIRED')
    OR (reviewer_subject_id IS NOT NULL AND reviewed_at IS NOT NULL)
  )
);
COMMENT ON TABLE enterprise_verification_cases IS 'TBL-WRK-015 — enterprise verification case.';
CREATE INDEX enterprise_verification_cases_status_created_idx ON enterprise_verification_cases (status, created_at);
CREATE INDEX enterprise_verification_cases_tenant_case_idx ON enterprise_verification_cases (tenant_id, case_no DESC);

CREATE TABLE enterprise_memberships (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL REFERENCES enterprise_tenants(id) ON DELETE RESTRICT,
  identity_subject_id uuid NOT NULL,
  role_code varchar(40) NOT NULL CHECK (role_code IN (
    'OWNER', 'ADMIN', 'RECRUITER', 'HIRING_MANAGER', 'BILLING', 'VIEWER'
  )),
  status membership_status NOT NULL,
  joined_at timestamptz,
  suspended_at timestamptz,
  left_at timestamptz,
  invited_by_subject_id uuid,
  valid_until timestamptz,
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, identity_subject_id),
  CHECK (status <> 'ACTIVE' OR joined_at IS NOT NULL)
);
COMMENT ON TABLE enterprise_memberships IS 'TBL-WRK-016 — enterprise membership; owner continuity is transaction-enforced.';
CREATE INDEX enterprise_memberships_subject_status_idx ON enterprise_memberships (identity_subject_id, status);
CREATE INDEX enterprise_memberships_tenant_status_role_idx ON enterprise_memberships (tenant_id, status, role_code);

CREATE TABLE enterprise_invites (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL REFERENCES enterprise_tenants(id) ON DELETE RESTRICT,
  email_normalized varchar(320) NOT NULL,
  email_ciphertext bytea NOT NULL,
  role_code varchar(40) NOT NULL CHECK (role_code IN (
    'OWNER', 'ADMIN', 'RECRUITER', 'HIRING_MANAGER', 'BILLING', 'VIEWER'
  )),
  token_hash char(64) NOT NULL UNIQUE,
  invited_by_subject_id uuid NOT NULL,
  expires_at timestamptz NOT NULL,
  accepted_at timestamptz,
  revoked_at timestamptz,
  UNIQUE (tenant_id, id),
  CHECK (expires_at > created_at),
  CHECK (token_hash ~ '^[0-9a-fA-F]{64}$')
);
COMMENT ON TABLE enterprise_invites IS 'TBL-WRK-017 — enterprise invite; raw email/token are never stored.';
CREATE UNIQUE INDEX enterprise_invites_live_email_idx
  ON enterprise_invites (tenant_id, email_normalized)
  WHERE accepted_at IS NULL AND revoked_at IS NULL;
CREATE INDEX enterprise_invites_tenant_expires_idx ON enterprise_invites (tenant_id, expires_at);

CREATE TABLE trusted_publisher_grants (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  tenant_id uuid NOT NULL REFERENCES enterprise_tenants(id) ON DELETE RESTRICT,
  scope varchar(24) NOT NULL DEFAULT 'JOB' CHECK (scope = 'JOB'),
  valid_from timestamptz NOT NULL,
  valid_until timestamptz NOT NULL,
  granted_by_subject_id uuid NOT NULL,
  grant_reason varchar(1000) NOT NULL,
  eligibility_snapshot jsonb NOT NULL,
  revoked_at timestamptz,
  revoked_by_subject_id uuid,
  revoke_reason varchar(1000),
  CHECK (valid_until > valid_from),
  CHECK (
    (revoked_at IS NULL AND revoked_by_subject_id IS NULL AND revoke_reason IS NULL)
    OR revoked_at IS NOT NULL
  )
);
COMMENT ON TABLE trusted_publisher_grants IS 'TBL-WRK-018 — immutable trusted publisher grant with revocation marker.';
CREATE UNIQUE INDEX trusted_publisher_grants_active_scope_idx
  ON trusted_publisher_grants (tenant_id, scope)
  WHERE revoked_at IS NULL;
CREATE INDEX trusted_publisher_grants_tenant_scope_idx
  ON trusted_publisher_grants (tenant_id, scope, revoked_at, valid_until);

CREATE TABLE university_tenants (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  legal_name varchar(240) NOT NULL,
  display_name varchar(200) NOT NULL,
  institution_code varchar(80) NOT NULL UNIQUE,
  slug varchar(120) NOT NULL UNIQUE,
  status tenant_status NOT NULL DEFAULT 'PENDING_VERIFICATION',
  website_url varchar(2048),
  logo_file_id uuid REFERENCES file_objects(id) ON DELETE RESTRICT,
  verified_at timestamptz,
  suspended_at timestamptz,
  closed_at timestamptz,
  CHECK (status <> 'VERIFIED' OR verified_at IS NOT NULL),
  CHECK (website_url IS NULL OR website_url ~ '^https://')
);
COMMENT ON TABLE university_tenants IS 'TBL-WRK-019 — university tenancy aggregate root.';
CREATE INDEX university_tenants_status_created_idx ON university_tenants (status, created_at DESC);
CREATE INDEX university_tenants_display_name_trgm_idx ON university_tenants USING gin (display_name gin_trgm_ops);

CREATE TABLE university_verification_cases (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL REFERENCES university_tenants(id) ON DELETE RESTRICT,
  case_no integer NOT NULL CHECK (case_no >= 1),
  status varchar(24) NOT NULL DEFAULT 'SUBMITTED'
    CHECK (status IN ('SUBMITTED', 'IN_REVIEW', 'APPROVED', 'REJECTED', 'EXPIRED')),
  submitted_by_subject_id uuid NOT NULL,
  document_file_ids uuid[] NOT NULL CHECK (cardinality(document_file_ids) > 0),
  submitted_snapshot jsonb NOT NULL,
  reviewer_subject_id uuid,
  reviewed_at timestamptz,
  decision_reason_codes varchar(80)[] NOT NULL DEFAULT '{}',
  comment varchar(2000),
  expires_at timestamptz,
  accreditation_code varchar(120),
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, case_no),
  CHECK (
    status NOT IN ('APPROVED', 'REJECTED', 'EXPIRED')
    OR (reviewer_subject_id IS NOT NULL AND reviewed_at IS NOT NULL)
  )
);
COMMENT ON TABLE university_verification_cases IS 'TBL-WRK-020 — university verification case.';
CREATE INDEX university_verification_cases_status_created_idx ON university_verification_cases (status, created_at);
CREATE INDEX university_verification_cases_tenant_case_idx ON university_verification_cases (tenant_id, case_no DESC);

CREATE TABLE university_memberships (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL REFERENCES university_tenants(id) ON DELETE RESTRICT,
  identity_subject_id uuid NOT NULL,
  role_code varchar(40) NOT NULL CHECK (role_code IN (
    'OWNER', 'ADMIN', 'COORDINATOR', 'ANALYST', 'VIEWER'
  )),
  status membership_status NOT NULL,
  joined_at timestamptz,
  suspended_at timestamptz,
  left_at timestamptz,
  invited_by_subject_id uuid,
  valid_until timestamptz,
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, identity_subject_id),
  CHECK (status <> 'ACTIVE' OR joined_at IS NOT NULL)
);
COMMENT ON TABLE university_memberships IS 'TBL-WRK-021 — university membership; owner continuity is transaction-enforced.';
CREATE INDEX university_memberships_subject_status_idx ON university_memberships (identity_subject_id, status);
CREATE INDEX university_memberships_tenant_status_role_idx ON university_memberships (tenant_id, status, role_code);

CREATE TABLE university_invites (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL REFERENCES university_tenants(id) ON DELETE RESTRICT,
  email_normalized varchar(320) NOT NULL,
  email_ciphertext bytea NOT NULL,
  role_code varchar(40) NOT NULL CHECK (role_code IN (
    'OWNER', 'ADMIN', 'COORDINATOR', 'ANALYST', 'VIEWER'
  )),
  token_hash char(64) NOT NULL UNIQUE,
  invited_by_subject_id uuid NOT NULL,
  expires_at timestamptz NOT NULL,
  accepted_at timestamptz,
  revoked_at timestamptz,
  UNIQUE (tenant_id, id),
  CHECK (expires_at > created_at),
  CHECK (token_hash ~ '^[0-9a-fA-F]{64}$')
);
COMMENT ON TABLE university_invites IS 'TBL-WRK-022 — university invite; raw email/token are never stored.';
CREATE UNIQUE INDEX university_invites_live_email_idx
  ON university_invites (tenant_id, email_normalized)
  WHERE accepted_at IS NULL AND revoked_at IS NULL;
CREATE INDEX university_invites_tenant_expires_idx ON university_invites (tenant_id, expires_at);

CREATE TABLE student_affiliations (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL REFERENCES university_tenants(id) ON DELETE RESTRICT,
  candidate_id uuid NOT NULL REFERENCES candidate_profiles(id) ON DELETE RESTRICT,
  student_code_ciphertext bytea,
  student_code_fingerprint char(64),
  affiliation_status varchar(24) NOT NULL DEFAULT 'PENDING'
    CHECK (affiliation_status IN ('PENDING', 'VERIFIED', 'REJECTED', 'ENDED', 'REVOKED')),
  starts_on date,
  ends_on date,
  verified_by_subject_id uuid,
  verified_at timestamptz,
  revoked_at timestamptz,
  UNIQUE (tenant_id, id),
  CHECK (ends_on IS NULL OR starts_on IS NULL OR ends_on >= starts_on)
);
COMMENT ON TABLE student_affiliations IS 'TBL-WRK-023 — university student affiliation.';
CREATE UNIQUE INDEX student_affiliations_active_candidate_idx
  ON student_affiliations (tenant_id, candidate_id)
  WHERE affiliation_status IN ('PENDING', 'VERIFIED');
CREATE UNIQUE INDEX student_affiliations_tenant_fingerprint_idx
  ON student_affiliations (tenant_id, student_code_fingerprint)
  WHERE student_code_fingerprint IS NOT NULL;
CREATE INDEX student_affiliations_tenant_status_idx ON student_affiliations (tenant_id, affiliation_status);
CREATE INDEX student_affiliations_candidate_status_idx ON student_affiliations (candidate_id, affiliation_status);

CREATE TABLE cohorts (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL REFERENCES university_tenants(id) ON DELETE RESTRICT,
  code varchar(80) NOT NULL,
  name varchar(200) NOT NULL,
  academic_year varchar(20) NOT NULL,
  starts_on date,
  ends_on date,
  archived_at timestamptz,
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, code),
  CHECK (ends_on IS NULL OR starts_on IS NULL OR ends_on >= starts_on)
);
COMMENT ON TABLE cohorts IS 'TBL-WRK-024 — university cohort.';
CREATE INDEX cohorts_tenant_academic_archived_idx ON cohorts (tenant_id, academic_year, archived_at);

CREATE TABLE cohort_memberships (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL,
  cohort_id uuid NOT NULL,
  affiliation_id uuid NOT NULL,
  joined_at timestamptz NOT NULL,
  left_at timestamptz,
  UNIQUE (tenant_id, id),
  FOREIGN KEY (tenant_id, cohort_id) REFERENCES cohorts(tenant_id, id) ON DELETE RESTRICT,
  FOREIGN KEY (tenant_id, affiliation_id) REFERENCES student_affiliations(tenant_id, id) ON DELETE RESTRICT,
  CHECK (left_at IS NULL OR left_at >= joined_at)
);
COMMENT ON TABLE cohort_memberships IS 'TBL-WRK-025 — cohort membership with composite tenant FKs.';
CREATE UNIQUE INDEX cohort_memberships_active_idx
  ON cohort_memberships (tenant_id, cohort_id, affiliation_id)
  WHERE left_at IS NULL;
CREATE INDEX cohort_memberships_tenant_cohort_idx ON cohort_memberships (tenant_id, cohort_id, left_at);
CREATE INDEX cohort_memberships_tenant_affiliation_idx ON cohort_memberships (tenant_id, affiliation_id);

CREATE TABLE internship_programs (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL REFERENCES university_tenants(id) ON DELETE RESTRICT,
  code varchar(80) NOT NULL,
  name varchar(200) NOT NULL,
  description text NOT NULL,
  starts_on date NOT NULL,
  ends_on date NOT NULL,
  status varchar(24) NOT NULL DEFAULT 'DRAFT'
    CHECK (status IN ('DRAFT', 'PUBLISHED', 'CLOSED', 'CANCELLED')),
  eligibility_rule jsonb NOT NULL,
  created_by_subject_id uuid NOT NULL,
  published_at timestamptz,
  closed_at timestamptz,
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, code),
  CHECK (ends_on >= starts_on)
);
COMMENT ON TABLE internship_programs IS 'TBL-WRK-026 — university internship program.';
CREATE INDEX internship_programs_tenant_status_starts_idx ON internship_programs (tenant_id, status, starts_on);

CREATE TABLE campus_job_distributions (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL REFERENCES university_tenants(id) ON DELETE RESTRICT,
  job_id uuid NOT NULL,
  program_id uuid,
  cohort_id uuid,
  distributed_by_subject_id uuid NOT NULL,
  distributed_at timestamptz NOT NULL,
  expires_at timestamptz,
  message varchar(1000),
  withdrawn_at timestamptz,
  UNIQUE (tenant_id, id),
  FOREIGN KEY (tenant_id, program_id) REFERENCES internship_programs(tenant_id, id) ON DELETE RESTRICT,
  FOREIGN KEY (tenant_id, cohort_id) REFERENCES cohorts(tenant_id, id) ON DELETE RESTRICT,
  CHECK (program_id IS NOT NULL OR cohort_id IS NOT NULL)
);
COMMENT ON TABLE campus_job_distributions IS 'TBL-WRK-027 — job distribution to a university program or cohort.';
CREATE UNIQUE INDEX campus_job_distributions_active_target_idx
  ON campus_job_distributions (tenant_id, job_id, program_id, cohort_id)
  WHERE withdrawn_at IS NULL;
CREATE INDEX campus_job_distributions_tenant_distributed_idx ON campus_job_distributions (tenant_id, distributed_at DESC);
CREATE INDEX campus_job_distributions_job_withdrawn_idx ON campus_job_distributions (job_id, withdrawn_at);

CREATE TABLE partnerships (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL REFERENCES university_tenants(id) ON DELETE RESTRICT,
  enterprise_tenant_id uuid NOT NULL REFERENCES enterprise_tenants(id) ON DELETE RESTRICT,
  status varchar(24) NOT NULL DEFAULT 'PROPOSED'
    CHECK (status IN ('PROPOSED', 'ACTIVE', 'DECLINED', 'ENDED')),
  scope jsonb NOT NULL,
  starts_on date,
  ends_on date,
  proposed_by_subject_id uuid NOT NULL,
  accepted_by_subject_id uuid,
  accepted_at timestamptz,
  ended_at timestamptz,
  UNIQUE (tenant_id, id),
  CHECK (ends_on IS NULL OR starts_on IS NULL OR ends_on >= starts_on)
);
COMMENT ON TABLE partnerships IS 'TBL-WRK-028 — university/enterprise partnership.';
CREATE UNIQUE INDEX partnerships_live_pair_idx
  ON partnerships (tenant_id, enterprise_tenant_id)
  WHERE status IN ('PROPOSED', 'ACTIVE');
CREATE INDEX partnerships_tenant_status_idx ON partnerships (tenant_id, status);
CREATE INDEX partnerships_enterprise_status_idx ON partnerships (enterprise_tenant_id, status);

CREATE TABLE data_consent_grants (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  candidate_id uuid NOT NULL REFERENCES candidate_profiles(id) ON DELETE RESTRICT,
  grantee_type varchar(24) NOT NULL CHECK (grantee_type IN ('UNIVERSITY', 'ENTERPRISE')),
  grantee_tenant_id uuid NOT NULL,
  scope varchar(40)[] NOT NULL CHECK (cardinality(scope) > 0),
  purpose varchar(500) NOT NULL,
  valid_from timestamptz NOT NULL,
  valid_until timestamptz NOT NULL,
  policy_version integer NOT NULL CHECK (policy_version >= 1),
  granted_at timestamptz NOT NULL,
  withdrawn_at timestamptz,
  withdrawal_reason varchar(500),
  CHECK (valid_until > valid_from),
  CHECK (withdrawn_at IS NOT NULL OR withdrawal_reason IS NULL)
);
COMMENT ON TABLE data_consent_grants IS 'TBL-WRK-030 — immutable consent grant; grantee is intentionally not a polymorphic FK.';
CREATE INDEX data_consent_grants_candidate_grantee_idx
  ON data_consent_grants (candidate_id, grantee_type, grantee_tenant_id, withdrawn_at, valid_until);

CREATE TABLE candidate_referrals (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL REFERENCES university_tenants(id) ON DELETE RESTRICT,
  candidate_id uuid NOT NULL REFERENCES candidate_profiles(id) ON DELETE RESTRICT,
  job_id uuid NOT NULL,
  affiliation_id uuid NOT NULL,
  referred_by_subject_id uuid NOT NULL,
  consent_grant_id uuid NOT NULL REFERENCES data_consent_grants(id) ON DELETE RESTRICT,
  status varchar(24) NOT NULL DEFAULT 'SENT'
    CHECK (status IN ('SENT', 'VIEWED', 'ACCEPTED', 'DECLINED', 'EXPIRED')),
  message varchar(1000),
  sent_at timestamptz NOT NULL,
  responded_at timestamptz,
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, candidate_id, job_id),
  FOREIGN KEY (tenant_id, affiliation_id) REFERENCES student_affiliations(tenant_id, id) ON DELETE RESTRICT
);
COMMENT ON TABLE candidate_referrals IS 'TBL-WRK-029 — university candidate referral, contingent on active consent.';
CREATE INDEX candidate_referrals_tenant_status_sent_idx ON candidate_referrals (tenant_id, status, sent_at DESC);
CREATE INDEX candidate_referrals_candidate_sent_idx ON candidate_referrals (candidate_id, sent_at DESC);

CREATE TABLE university_report_runs (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL REFERENCES university_tenants(id) ON DELETE RESTRICT,
  report_code varchar(80) NOT NULL,
  filters jsonb NOT NULL,
  period_start date NOT NULL,
  period_end date NOT NULL,
  status varchar(20) NOT NULL DEFAULT 'QUEUED'
    CHECK (status IN ('QUEUED', 'RUNNING', 'READY', 'FAILED', 'EXPIRED')),
  requested_by_subject_id uuid NOT NULL,
  result_metrics jsonb,
  group_size_min integer NOT NULL DEFAULT 10 CHECK (group_size_min >= 10),
  source_high_watermark timestamptz,
  completed_at timestamptz,
  expires_at timestamptz NOT NULL,
  UNIQUE (tenant_id, id),
  CHECK (period_end >= period_start)
);
COMMENT ON TABLE university_report_runs IS 'TBL-WRK-031 — university aggregate-only report run.';
CREATE INDEX university_report_runs_tenant_status_created_idx ON university_report_runs (tenant_id, status, created_at DESC);

-- TBL-WRK-032 through TBL-WRK-056: jobs, ATS, interviews and conversation.
CREATE TABLE jobs (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL REFERENCES enterprise_tenants(id) ON DELETE RESTRICT,
  slug varchar(160) NOT NULL,
  status job_status NOT NULL DEFAULT 'DRAFT',
  current_draft_revision_id uuid,
  published_revision_id uuid,
  created_by_subject_id uuid NOT NULL,
  published_at timestamptz,
  paused_at timestamptz,
  closed_at timestamptz,
  expires_at timestamptz,
  taken_down_at timestamptz,
  terminal_reason_code varchar(80),
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, slug),
  CHECK (status <> 'PUBLISHED' OR published_at IS NOT NULL),
  CHECK (status NOT IN ('CLOSED', 'EXPIRED', 'TAKEN_DOWN') OR terminal_reason_code IS NOT NULL)
);
COMMENT ON TABLE jobs IS 'TBL-WRK-032 — enterprise job aggregate root.';
CREATE INDEX jobs_tenant_status_updated_idx ON jobs (tenant_id, status, updated_at DESC);
CREATE INDEX jobs_status_published_idx ON jobs (status, published_at DESC);
CREATE INDEX jobs_active_expiry_idx ON jobs (expires_at) WHERE status IN ('PUBLISHED', 'PAUSED');

CREATE TABLE job_revisions (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL,
  job_id uuid NOT NULL,
  revision_no integer NOT NULL CHECK (revision_no >= 1),
  status job_revision_status NOT NULL DEFAULT 'DRAFT',
  title varchar(200) NOT NULL,
  description_markdown text NOT NULL,
  requirements_markdown text NOT NULL,
  benefits_markdown text,
  employment_type varchar(24) NOT NULL,
  work_mode varchar(16) NOT NULL,
  location_codes varchar(20)[] NOT NULL,
  salary_min_vnd bigint,
  salary_max_vnd bigint,
  salary_visible boolean NOT NULL DEFAULT false,
  headcount integer NOT NULL DEFAULT 1 CHECK (headcount BETWEEN 1 AND 10000),
  application_deadline timestamptz,
  content_hash char(64) NOT NULL,
  created_by_subject_id uuid NOT NULL,
  submitted_at timestamptz,
  approved_at timestamptz,
  published_at timestamptz,
  superseded_at timestamptz,
  discarded_at timestamptz,
  source_revision_id uuid REFERENCES job_revisions(id) ON DELETE RESTRICT,
  UNIQUE (tenant_id, id),
  UNIQUE (job_id, revision_no),
  FOREIGN KEY (tenant_id, job_id) REFERENCES jobs(tenant_id, id) ON DELETE RESTRICT,
  CHECK (salary_min_vnd IS NULL OR salary_min_vnd >= 0),
  CHECK (salary_max_vnd IS NULL OR salary_max_vnd >= 0),
  CHECK (salary_min_vnd IS NULL OR salary_max_vnd IS NULL OR salary_max_vnd >= salary_min_vnd),
  CHECK (content_hash ~ '^[0-9a-fA-F]{64}$')
);
COMMENT ON TABLE job_revisions IS 'TBL-WRK-033 — versioned job content; non-draft revisions are immutable.';
CREATE INDEX job_revisions_tenant_job_revision_idx ON job_revisions (tenant_id, job_id, revision_no DESC);
CREATE INDEX job_revisions_fts_idx ON job_revisions
  USING gin (to_tsvector('simple', title || ' ' || description_markdown || ' ' || requirements_markdown));
CREATE INDEX job_revisions_locations_gin_idx ON job_revisions USING gin (location_codes);
CREATE INDEX job_revisions_status_submitted_idx ON job_revisions (status, submitted_at);

CREATE TABLE job_skill_requirements (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL,
  job_revision_id uuid NOT NULL,
  skill_id uuid NOT NULL REFERENCES skills(id) ON DELETE RESTRICT,
  required_level smallint CHECK (required_level BETWEEN 1 AND 5),
  min_years numeric(4,1) CHECK (min_years BETWEEN 0 AND 80),
  is_required boolean NOT NULL DEFAULT false,
  weight numeric(5,2) NOT NULL DEFAULT 1 CHECK (weight BETWEEN 0 AND 100),
  UNIQUE (job_revision_id, skill_id),
  FOREIGN KEY (tenant_id, job_revision_id) REFERENCES job_revisions(tenant_id, id) ON DELETE RESTRICT
);
COMMENT ON TABLE job_skill_requirements IS 'TBL-WRK-034 — requirements belonging to a draft job revision.';
CREATE INDEX job_skill_requirements_skill_revision_idx ON job_skill_requirements (skill_id, job_revision_id);
CREATE INDEX job_skill_requirements_tenant_revision_idx ON job_skill_requirements (tenant_id, job_revision_id);

CREATE TABLE job_review_decisions (
  id uuid PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  tenant_id uuid NOT NULL,
  job_id uuid NOT NULL,
  job_revision_id uuid NOT NULL,
  reviewer_subject_id uuid NOT NULL,
  decision varchar(24) NOT NULL CHECK (decision IN ('APPROVE', 'REJECT', 'REQUEST_CHANGES', 'TAKE_DOWN')),
  reason_codes varchar(80)[] NOT NULL DEFAULT '{}',
  comment varchar(2000),
  expected_job_version bigint NOT NULL CHECK (expected_job_version >= 1),
  trace_id varchar(64) NOT NULL,
  FOREIGN KEY (tenant_id, job_id) REFERENCES jobs(tenant_id, id) ON DELETE RESTRICT,
  FOREIGN KEY (tenant_id, job_revision_id) REFERENCES job_revisions(tenant_id, id) ON DELETE RESTRICT,
  CHECK (decision = 'APPROVE' OR cardinality(reason_codes) > 0)
);
COMMENT ON TABLE job_review_decisions IS 'TBL-WRK-035 — append-only job review decision.';
CREATE INDEX job_review_decisions_revision_occurred_idx ON job_review_decisions (job_revision_id, occurred_at DESC);
CREATE INDEX job_review_decisions_reviewer_occurred_idx ON job_review_decisions (reviewer_subject_id, occurred_at DESC);

CREATE TABLE job_status_history (
  id uuid PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  tenant_id uuid NOT NULL,
  job_id uuid NOT NULL,
  from_status job_status,
  to_status job_status NOT NULL,
  actor_subject_id uuid,
  reason_code varchar(80) NOT NULL,
  job_revision_id uuid,
  trace_id varchar(64) NOT NULL,
  FOREIGN KEY (tenant_id, job_id) REFERENCES jobs(tenant_id, id) ON DELETE RESTRICT,
  FOREIGN KEY (tenant_id, job_revision_id) REFERENCES job_revisions(tenant_id, id) ON DELETE RESTRICT
);
COMMENT ON TABLE job_status_history IS 'TBL-WRK-036 — append-only job lifecycle history.';
CREATE INDEX job_status_history_job_occurred_idx ON job_status_history (job_id, occurred_at, id);
CREATE INDEX job_status_history_tenant_status_occurred_idx ON job_status_history (tenant_id, to_status, occurred_at DESC);

CREATE TABLE candidate_search_documents (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  candidate_id uuid NOT NULL UNIQUE REFERENCES candidate_profiles(id) ON DELETE RESTRICT,
  visibility candidate_visibility NOT NULL,
  search_vector tsvector,
  skill_ids uuid[] NOT NULL DEFAULT '{}',
  location_codes varchar(20)[] NOT NULL DEFAULT '{}',
  experience_months integer CHECK (experience_months >= 0),
  headline_redacted varchar(200),
  source_version bigint NOT NULL CHECK (source_version >= 1),
  indexed_at timestamptz,
  remove_by timestamptz,
  removed_at timestamptz,
  CHECK (visibility <> 'PRIVATE' OR search_vector IS NULL),
  CHECK (remove_by IS NULL OR remove_by <= now() + interval '5 minutes')
);
COMMENT ON TABLE candidate_search_documents IS 'TBL-WRK-037 — rebuildable redacted candidate search projection.';
CREATE INDEX candidate_search_documents_vector_gin_idx ON candidate_search_documents USING gin (search_vector);
CREATE INDEX candidate_search_documents_skills_gin_idx ON candidate_search_documents USING gin (skill_ids);
CREATE INDEX candidate_search_documents_locations_gin_idx ON candidate_search_documents USING gin (location_codes);
CREATE INDEX candidate_search_documents_visibility_indexed_idx ON candidate_search_documents (visibility, indexed_at);
CREATE INDEX candidate_search_documents_remove_by_idx ON candidate_search_documents (remove_by) WHERE removed_at IS NULL;

CREATE TABLE candidate_invitations (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL REFERENCES enterprise_tenants(id) ON DELETE RESTRICT,
  job_id uuid NOT NULL,
  candidate_id uuid NOT NULL REFERENCES candidate_profiles(id) ON DELETE RESTRICT,
  invited_by_subject_id uuid NOT NULL,
  message varchar(1000),
  status varchar(24) NOT NULL DEFAULT 'SENT'
    CHECK (status IN ('SENT', 'VIEWED', 'ACCEPTED', 'DECLINED', 'EXPIRED')),
  sent_at timestamptz NOT NULL,
  viewed_at timestamptz,
  responded_at timestamptz,
  expires_at timestamptz NOT NULL,
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, job_id, candidate_id),
  FOREIGN KEY (tenant_id, job_id) REFERENCES jobs(tenant_id, id) ON DELETE RESTRICT,
  CHECK (expires_at > sent_at)
);
COMMENT ON TABLE candidate_invitations IS 'TBL-WRK-038 — enterprise invitation to a searchable candidate.';
CREATE INDEX candidate_invitations_candidate_status_sent_idx ON candidate_invitations (candidate_id, status, sent_at DESC);
CREATE INDEX candidate_invitations_tenant_job_status_idx ON candidate_invitations (tenant_id, job_id, status);

CREATE TABLE talent_lists (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL REFERENCES enterprise_tenants(id) ON DELETE RESTRICT,
  name varchar(160) NOT NULL,
  description varchar(1000),
  created_by_subject_id uuid NOT NULL,
  archived_at timestamptz,
  UNIQUE (tenant_id, id)
);
COMMENT ON TABLE talent_lists IS 'TBL-WRK-039 — enterprise talent list.';
CREATE UNIQUE INDEX talent_lists_active_name_idx ON talent_lists (tenant_id, name) WHERE archived_at IS NULL;
CREATE INDEX talent_lists_tenant_archived_updated_idx ON talent_lists (tenant_id, archived_at, updated_at DESC);

CREATE TABLE talent_list_items (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL,
  list_id uuid NOT NULL,
  candidate_id uuid NOT NULL REFERENCES candidate_profiles(id) ON DELETE RESTRICT,
  added_by_subject_id uuid NOT NULL,
  source varchar(24) NOT NULL,
  removed_at timestamptz,
  UNIQUE (tenant_id, id),
  FOREIGN KEY (tenant_id, list_id) REFERENCES talent_lists(tenant_id, id) ON DELETE RESTRICT
);
COMMENT ON TABLE talent_list_items IS 'TBL-WRK-040 — candidate item in enterprise talent list.';
CREATE UNIQUE INDEX talent_list_items_active_idx
  ON talent_list_items (tenant_id, list_id, candidate_id) WHERE removed_at IS NULL;
CREATE INDEX talent_list_items_tenant_list_removed_created_idx
  ON talent_list_items (tenant_id, list_id, removed_at, created_at DESC);

CREATE TABLE applications (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL REFERENCES enterprise_tenants(id) ON DELETE RESTRICT,
  candidate_id uuid NOT NULL REFERENCES candidate_profiles(id) ON DELETE RESTRICT,
  job_id uuid NOT NULL,
  job_revision_id uuid NOT NULL,
  status application_status NOT NULL DEFAULT 'SUBMITTED',
  submitted_at timestamptz NOT NULL,
  source varchar(24) NOT NULL,
  current_assignee_subject_id uuid,
  last_status_at timestamptz NOT NULL,
  withdrawn_at timestamptz,
  terminal_at timestamptz,
  consent_policy_version integer NOT NULL CHECK (consent_policy_version >= 1),
  row_security_key uuid NOT NULL,
  UNIQUE (tenant_id, id),
  UNIQUE (candidate_id, job_id),
  FOREIGN KEY (tenant_id, job_id) REFERENCES jobs(tenant_id, id) ON DELETE RESTRICT,
  FOREIGN KEY (tenant_id, job_revision_id) REFERENCES job_revisions(tenant_id, id) ON DELETE RESTRICT,
  CHECK (status <> 'WITHDRAWN' OR withdrawn_at IS NOT NULL),
  CHECK (
    status NOT IN ('HIRED', 'REJECTED', 'WITHDRAWN', 'OFFER_DECLINED')
    OR terminal_at IS NOT NULL
  )
);
COMMENT ON TABLE applications IS 'TBL-WRK-041 — ATS application, tenant-bound and candidate/job unique.';
CREATE INDEX applications_candidate_submitted_idx ON applications (candidate_id, submitted_at DESC);
CREATE INDEX applications_tenant_job_status_submitted_idx ON applications (tenant_id, job_id, status, submitted_at DESC);
CREATE INDEX applications_tenant_assignee_status_idx ON applications (tenant_id, current_assignee_subject_id, status);

CREATE TABLE application_snapshots (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  tenant_id uuid NOT NULL,
  application_id uuid NOT NULL UNIQUE,
  candidate_profile_snapshot jsonb NOT NULL,
  cv_version_id uuid NOT NULL REFERENCES cv_versions(id) ON DELETE RESTRICT,
  cv_snapshot jsonb NOT NULL,
  portfolio_snapshot jsonb NOT NULL DEFAULT '[]',
  cover_letter_snapshot text,
  screening_answers_snapshot jsonb NOT NULL DEFAULT '[]',
  job_revision_id uuid NOT NULL REFERENCES job_revisions(id) ON DELETE RESTRICT,
  job_snapshot jsonb NOT NULL,
  schema_version integer NOT NULL CHECK (schema_version >= 1),
  snapshot_hash char(64) NOT NULL,
  captured_at timestamptz NOT NULL,
  UNIQUE (tenant_id, id),
  FOREIGN KEY (tenant_id, application_id) REFERENCES applications(tenant_id, id) ON DELETE RESTRICT,
  CHECK (snapshot_hash ~ '^[0-9a-fA-F]{64}$')
);
COMMENT ON TABLE application_snapshots IS 'TBL-WRK-042 — immutable application snapshot.';
CREATE INDEX application_snapshots_tenant_application_idx ON application_snapshots (tenant_id, application_id);

CREATE TABLE application_evidence_selections (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  tenant_id uuid NOT NULL,
  application_id uuid NOT NULL,
  study_evidence_id uuid NOT NULL,
  selected_by_subject_id uuid NOT NULL,
  consent_id uuid NOT NULL REFERENCES data_consent_grants(id) ON DELETE RESTRICT,
  consent_policy_version integer NOT NULL CHECK (consent_policy_version >= 1),
  selected_at timestamptz NOT NULL,
  UNIQUE (tenant_id, id),
  UNIQUE (application_id, study_evidence_id),
  FOREIGN KEY (tenant_id, application_id) REFERENCES applications(tenant_id, id) ON DELETE RESTRICT
);
COMMENT ON TABLE application_evidence_selections IS 'TBL-WRK-043 — immutable selection of study evidence by applicant.';
CREATE INDEX application_evidence_selections_application_selected_idx ON application_evidence_selections (application_id, selected_at);

CREATE TABLE evidence_export_requests (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL,
  application_id uuid NOT NULL,
  request_id uuid NOT NULL UNIQUE,
  selected_evidence_ids uuid[] NOT NULL CHECK (cardinality(selected_evidence_ids) > 0),
  consent_id uuid NOT NULL REFERENCES data_consent_grants(id) ON DELETE RESTRICT,
  status evidence_export_status NOT NULL DEFAULT 'PENDING',
  attempt_count integer NOT NULL DEFAULT 0 CHECK (attempt_count >= 0),
  next_retry_at timestamptz,
  last_error_code varchar(80),
  sent_at timestamptz,
  completed_at timestamptz,
  request_payload_hash char(64) NOT NULL,
  UNIQUE (tenant_id, id),
  UNIQUE (application_id, request_id),
  FOREIGN KEY (tenant_id, application_id) REFERENCES applications(tenant_id, id) ON DELETE RESTRICT,
  CHECK (request_payload_hash ~ '^[0-9a-fA-F]{64}$')
);
COMMENT ON TABLE evidence_export_requests IS 'TBL-WRK-044 — work-to-study evidence export request; study evidence remains external.';
CREATE INDEX evidence_export_requests_status_retry_idx ON evidence_export_requests (status, next_retry_at, id);
CREATE INDEX evidence_export_requests_application_created_idx ON evidence_export_requests (application_id, created_at DESC);

CREATE TABLE application_evidence_snapshots (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  tenant_id uuid NOT NULL,
  application_id uuid NOT NULL,
  study_evidence_id uuid NOT NULL,
  request_id uuid NOT NULL REFERENCES evidence_export_requests(request_id) ON DELETE RESTRICT,
  result_status evidence_export_status NOT NULL CHECK (result_status IN ('READY', 'UNAVAILABLE')),
  evidence_type varchar(32),
  title varchar(200),
  description varchar(1000),
  issuer varchar(160),
  issued_at timestamptz,
  source_version_id uuid,
  claims_snapshot jsonb,
  claims_hash char(64),
  signature_verification jsonb,
  received_at timestamptz,
  unavailable_reason_code varchar(80),
  UNIQUE (tenant_id, id),
  UNIQUE (application_id, study_evidence_id),
  FOREIGN KEY (tenant_id, application_id) REFERENCES applications(tenant_id, id) ON DELETE RESTRICT,
  CHECK (
    result_status <> 'READY'
    OR (claims_snapshot IS NOT NULL AND claims_hash IS NOT NULL AND signature_verification IS NOT NULL)
  ),
  CHECK (
    result_status <> 'UNAVAILABLE'
    OR (claims_snapshot IS NULL AND claims_hash IS NULL AND signature_verification IS NULL)
  )
);
COMMENT ON TABLE application_evidence_snapshots IS 'TBL-WRK-045 — immutable study evidence export result snapshot.';
CREATE INDEX application_evidence_snapshots_application_status_idx ON application_evidence_snapshots (application_id, result_status);
CREATE INDEX application_evidence_snapshots_evidence_status_idx ON application_evidence_snapshots (study_evidence_id, result_status);

CREATE TABLE application_status_history (
  id uuid PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  tenant_id uuid NOT NULL,
  application_id uuid NOT NULL,
  from_status application_status,
  to_status application_status NOT NULL,
  actor_subject_id uuid NOT NULL,
  reason_code varchar(80) NOT NULL,
  comment varchar(1000),
  expected_application_version bigint NOT NULL CHECK (expected_application_version >= 1),
  source varchar(24) NOT NULL CHECK (source <> 'AI'),
  trace_id varchar(64) NOT NULL,
  FOREIGN KEY (tenant_id, application_id) REFERENCES applications(tenant_id, id) ON DELETE RESTRICT
);
COMMENT ON TABLE application_status_history IS 'TBL-WRK-046 — append-only ATS lifecycle history; AI cannot transition it.';
CREATE INDEX application_status_history_application_occurred_idx ON application_status_history (application_id, occurred_at, id);
CREATE INDEX application_status_history_tenant_status_occurred_idx ON application_status_history (tenant_id, to_status, occurred_at DESC);

CREATE TABLE application_assignments (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  tenant_id uuid NOT NULL,
  application_id uuid NOT NULL,
  assignee_subject_id uuid NOT NULL,
  assigned_by_subject_id uuid NOT NULL,
  assigned_at timestamptz NOT NULL,
  unassigned_at timestamptz,
  unassigned_by_subject_id uuid,
  reason varchar(500),
  UNIQUE (tenant_id, id),
  FOREIGN KEY (tenant_id, application_id) REFERENCES applications(tenant_id, id) ON DELETE RESTRICT,
  CHECK ((unassigned_at IS NULL AND unassigned_by_subject_id IS NULL) OR unassigned_at IS NOT NULL)
);
COMMENT ON TABLE application_assignments IS 'TBL-WRK-047 — immutable assignment with one-way unassignment marker.';
CREATE UNIQUE INDEX application_assignments_active_idx
  ON application_assignments (application_id, assignee_subject_id) WHERE unassigned_at IS NULL;
CREATE INDEX application_assignments_tenant_assignee_active_idx
  ON application_assignments (tenant_id, assignee_subject_id, unassigned_at, assigned_at DESC);

CREATE TABLE application_notes (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL REFERENCES enterprise_tenants(id) ON DELETE RESTRICT,
  application_id uuid NOT NULL,
  author_subject_id uuid NOT NULL,
  body text NOT NULL,
  visibility varchar(24) NOT NULL DEFAULT 'RECRUITING_TEAM'
    CHECK (visibility IN ('PRIVATE_AUTHOR', 'RECRUITING_TEAM')),
  edited_at timestamptz,
  deleted_at timestamptz,
  content_hash char(64) NOT NULL,
  UNIQUE (tenant_id, id),
  FOREIGN KEY (tenant_id, application_id) REFERENCES applications(tenant_id, id) ON DELETE RESTRICT
);
COMMENT ON TABLE application_notes IS 'TBL-WRK-048 — tenant-scoped DERIVED_SENSITIVE ATS note.';
CREATE INDEX application_notes_tenant_application_created_idx ON application_notes (tenant_id, application_id, created_at DESC);

CREATE TABLE interviews (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL REFERENCES enterprise_tenants(id) ON DELETE RESTRICT,
  application_id uuid NOT NULL,
  status interview_status NOT NULL DEFAULT 'PROPOSED',
  current_schedule_version integer NOT NULL DEFAULT 1 CHECK (current_schedule_version >= 1),
  title varchar(200) NOT NULL,
  interview_type varchar(24) NOT NULL CHECK (interview_type IN ('PHONE', 'VIDEO', 'ONSITE')),
  location_text varchar(500),
  meeting_url varchar(2048),
  timezone varchar(64) NOT NULL,
  created_by_subject_id uuid NOT NULL,
  cancelled_at timestamptz,
  completed_at timestamptz,
  no_show_party varchar(16),
  UNIQUE (tenant_id, id),
  FOREIGN KEY (tenant_id, application_id) REFERENCES applications(tenant_id, id) ON DELETE RESTRICT,
  CHECK (meeting_url IS NULL OR (interview_type = 'VIDEO' AND meeting_url ~ '^https://')),
  CHECK (status <> 'CANCELLED' OR cancelled_at IS NOT NULL),
  CHECK (status <> 'COMPLETED' OR completed_at IS NOT NULL),
  CHECK (status <> 'NO_SHOW' OR no_show_party IS NOT NULL)
);
COMMENT ON TABLE interviews IS 'TBL-WRK-049 — tenant-scoped interview aggregate.';
CREATE INDEX interviews_tenant_application_created_idx ON interviews (tenant_id, application_id, created_at DESC);
CREATE INDEX interviews_tenant_status_updated_idx ON interviews (tenant_id, status, updated_at);

CREATE TABLE interview_schedule_versions (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  tenant_id uuid NOT NULL,
  interview_id uuid NOT NULL,
  version_no integer NOT NULL CHECK (version_no >= 1),
  starts_at timestamptz NOT NULL,
  ends_at timestamptz NOT NULL,
  timezone varchar(64) NOT NULL,
  proposed_by_subject_id uuid NOT NULL,
  change_reason varchar(1000),
  supersedes_version_id uuid REFERENCES interview_schedule_versions(id) ON DELETE RESTRICT,
  created_ics_sequence integer NOT NULL,
  content_hash char(64) NOT NULL,
  UNIQUE (tenant_id, id),
  UNIQUE (interview_id, version_no),
  FOREIGN KEY (tenant_id, interview_id) REFERENCES interviews(tenant_id, id) ON DELETE RESTRICT,
  CHECK (ends_at > starts_at)
);
COMMENT ON TABLE interview_schedule_versions IS 'TBL-WRK-050 — immutable interview schedule version.';
CREATE INDEX interview_schedule_versions_interview_version_idx ON interview_schedule_versions (interview_id, version_no DESC);
CREATE INDEX interview_schedule_versions_tenant_time_idx ON interview_schedule_versions (tenant_id, starts_at, ends_at);

CREATE TABLE interview_participants (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL REFERENCES enterprise_tenants(id) ON DELETE RESTRICT,
  interview_id uuid NOT NULL,
  identity_subject_id uuid NOT NULL,
  participant_role varchar(24) NOT NULL CHECK (participant_role IN ('CANDIDATE', 'INTERVIEWER', 'ORGANIZER')),
  response varchar(24) NOT NULL DEFAULT 'PENDING' CHECK (response IN ('PENDING', 'ACCEPTED', 'DECLINED', 'TENTATIVE')),
  responded_at timestamptz,
  last_notified_schedule_version integer NOT NULL DEFAULT 0 CHECK (last_notified_schedule_version >= 0),
  UNIQUE (tenant_id, id),
  UNIQUE (interview_id, identity_subject_id),
  FOREIGN KEY (tenant_id, interview_id) REFERENCES interviews(tenant_id, id) ON DELETE RESTRICT
);
COMMENT ON TABLE interview_participants IS 'TBL-WRK-051 — interview participant and response.';
CREATE INDEX interview_participants_subject_response_updated_idx ON interview_participants (identity_subject_id, response, updated_at DESC);
CREATE INDEX interview_participants_tenant_interview_idx ON interview_participants (tenant_id, interview_id);

CREATE TABLE interview_status_history (
  id uuid PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  tenant_id uuid NOT NULL,
  interview_id uuid NOT NULL,
  from_status interview_status,
  to_status interview_status NOT NULL,
  schedule_version integer NOT NULL CHECK (schedule_version >= 1),
  actor_subject_id uuid NOT NULL,
  reason_code varchar(80) NOT NULL,
  trace_id varchar(64) NOT NULL,
  FOREIGN KEY (tenant_id, interview_id) REFERENCES interviews(tenant_id, id) ON DELETE RESTRICT
);
COMMENT ON TABLE interview_status_history IS 'TBL-WRK-052 — append-only interview lifecycle history.';
CREATE INDEX interview_status_history_interview_occurred_idx ON interview_status_history (interview_id, occurred_at, id);

CREATE TABLE conversations (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL REFERENCES enterprise_tenants(id) ON DELETE RESTRICT,
  application_id uuid NOT NULL UNIQUE,
  status conversation_status NOT NULL DEFAULT 'ACTIVE',
  candidate_subject_id uuid NOT NULL,
  recruiter_subject_id uuid NOT NULL,
  opened_at timestamptz NOT NULL,
  read_only_at timestamptz,
  last_message_at timestamptz,
  last_message_id uuid,
  UNIQUE (tenant_id, id),
  FOREIGN KEY (tenant_id, application_id) REFERENCES applications(tenant_id, id) ON DELETE RESTRICT,
  CHECK (status <> 'READ_ONLY' OR read_only_at IS NOT NULL)
);
COMMENT ON TABLE conversations IS 'TBL-WRK-053 — exactly one conversation per application.';
CREATE INDEX conversations_candidate_last_message_idx ON conversations (candidate_subject_id, last_message_at DESC);
CREATE INDEX conversations_tenant_recruiter_last_message_idx ON conversations (tenant_id, recruiter_subject_id, last_message_at DESC);
CREATE INDEX conversations_application_idx ON conversations (application_id);

CREATE TABLE messages (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  tenant_id uuid NOT NULL,
  conversation_id uuid NOT NULL,
  sender_subject_id uuid,
  client_message_id uuid NOT NULL,
  message_type varchar(16) NOT NULL DEFAULT 'TEXT' CHECK (message_type IN ('TEXT', 'SYSTEM')),
  body text NOT NULL CHECK (length(btrim(body)) BETWEEN 1 AND 5000),
  sent_at timestamptz NOT NULL,
  server_sequence bigint NOT NULL CHECK (server_sequence >= 1),
  deleted_for_all_at timestamptz,
  moderation_status varchar(24) NOT NULL DEFAULT 'CLEAR',
  content_hash char(64) NOT NULL,
  UNIQUE (tenant_id, id),
  UNIQUE (conversation_id, client_message_id),
  UNIQUE (conversation_id, server_sequence),
  FOREIGN KEY (tenant_id, conversation_id) REFERENCES conversations(tenant_id, id) ON DELETE RESTRICT,
  CHECK (
    (message_type = 'TEXT' AND sender_subject_id IS NOT NULL)
    OR (message_type = 'SYSTEM' AND sender_subject_id IS NULL)
  )
);
COMMENT ON TABLE messages IS 'TBL-WRK-054 — immutable TEXT or SYSTEM message; V1 has no chat attachments.';
CREATE INDEX messages_conversation_sequence_idx ON messages (conversation_id, server_sequence DESC);
CREATE INDEX messages_sender_sent_idx ON messages (sender_subject_id, sent_at DESC);

CREATE TABLE conversation_read_cursors (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL,
  conversation_id uuid NOT NULL,
  identity_subject_id uuid NOT NULL,
  last_read_sequence bigint NOT NULL DEFAULT 0 CHECK (last_read_sequence >= 0),
  last_read_at timestamptz,
  UNIQUE (tenant_id, id),
  UNIQUE (conversation_id, identity_subject_id),
  FOREIGN KEY (tenant_id, conversation_id) REFERENCES conversations(tenant_id, id) ON DELETE RESTRICT
);
COMMENT ON TABLE conversation_read_cursors IS 'TBL-WRK-055 — per-participant monotonic conversation cursor.';
CREATE INDEX conversation_read_cursors_subject_updated_idx ON conversation_read_cursors (identity_subject_id, updated_at DESC);

CREATE TABLE websocket_connection_leases (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  identity_subject_id uuid NOT NULL,
  connection_id uuid NOT NULL UNIQUE,
  node_id varchar(120) NOT NULL,
  connected_at timestamptz NOT NULL,
  last_heartbeat_at timestamptz NOT NULL,
  expires_at timestamptz NOT NULL,
  revoked_at timestamptz,
  CHECK (expires_at > last_heartbeat_at)
);
COMMENT ON TABLE websocket_connection_leases IS 'TBL-WRK-056 — PostgreSQL fallback registry for transient WebSocket leases.';
CREATE INDEX websocket_connection_leases_subject_expires_idx ON websocket_connection_leases (identity_subject_id, expires_at);
CREATE INDEX websocket_connection_leases_expires_idx ON websocket_connection_leases (expires_at);

-- TBL-AIX-001 through TBL-AIX-008: auditable AI configuration and human review.
CREATE TABLE ai_model_versions (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  provider varchar(40) NOT NULL,
  model_key varchar(160) NOT NULL,
  version varchar(120) NOT NULL,
  capability varchar(40) NOT NULL,
  endpoint_config_ref varchar(300) NOT NULL,
  data_residency varchar(80) NOT NULL,
  enabled boolean NOT NULL DEFAULT false,
  activated_at timestamptz,
  retired_at timestamptz,
  risk_class varchar(24) NOT NULL,
  UNIQUE (provider, model_key, version, capability),
  CHECK (NOT enabled OR activated_at IS NOT NULL)
);
COMMENT ON TABLE ai_model_versions IS 'TBL-AIX-001 — AI model configuration reference; no secret is stored.';
CREATE INDEX ai_model_versions_capability_enabled_idx ON ai_model_versions (capability, enabled, activated_at DESC);

CREATE TABLE ai_prompt_versions (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  prompt_code varchar(80) NOT NULL,
  version_no integer NOT NULL CHECK (version_no >= 1),
  capability varchar(40) NOT NULL,
  system_prompt text NOT NULL,
  input_schema jsonb NOT NULL,
  output_schema jsonb NOT NULL,
  excluded_fields varchar(120)[] NOT NULL,
  injection_policy_version integer NOT NULL CHECK (injection_policy_version >= 1),
  created_by_subject_id uuid NOT NULL,
  approved_by_subject_id uuid NOT NULL,
  activated_at timestamptz,
  retired_at timestamptz,
  content_hash char(64) NOT NULL,
  UNIQUE (prompt_code, version_no),
  CHECK (created_by_subject_id <> approved_by_subject_id),
  CHECK (cardinality(excluded_fields) > 0)
);
COMMENT ON TABLE ai_prompt_versions IS 'TBL-AIX-002 — immutable prompt version with maker-checker approval.';
CREATE INDEX ai_prompt_versions_prompt_activated_idx ON ai_prompt_versions (prompt_code, activated_at DESC);

CREATE TABLE ai_policy_versions (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  policy_code varchar(80) NOT NULL,
  version_no integer NOT NULL CHECK (version_no >= 1),
  capability varchar(40) NOT NULL,
  rules jsonb NOT NULL,
  allowed_input_fields varchar(120)[] NOT NULL,
  forbidden_actions varchar(120)[] NOT NULL,
  approved_by_subject_id uuid NOT NULL,
  activated_at timestamptz NOT NULL,
  retired_at timestamptz,
  content_hash char(64) NOT NULL,
  UNIQUE (policy_code, version_no),
  CHECK (
    forbidden_actions @> ARRAY['ATS_STATUS_CHANGE', 'AUTO_REJECT', 'AUTO_HIRE']::varchar(120)[]
  )
);
COMMENT ON TABLE ai_policy_versions IS 'TBL-AIX-003 — immutable policy version that forbids ATS automation.';
CREATE INDEX ai_policy_versions_capability_activated_idx ON ai_policy_versions (capability, activated_at DESC);

CREATE TABLE ai_jobs (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid REFERENCES enterprise_tenants(id) ON DELETE RESTRICT,
  actor_subject_id uuid NOT NULL,
  capability varchar(40) NOT NULL CHECK (capability IN (
    'CV_DRAFT', 'JD_DRAFT', 'MATCH_EXPLANATION', 'SHORTLIST_SUGGESTION'
  )),
  resource_type varchar(40) NOT NULL,
  resource_id uuid NOT NULL,
  model_version_id uuid NOT NULL REFERENCES ai_model_versions(id) ON DELETE RESTRICT,
  prompt_version_id uuid NOT NULL REFERENCES ai_prompt_versions(id) ON DELETE RESTRICT,
  policy_version_id uuid NOT NULL REFERENCES ai_policy_versions(id) ON DELETE RESTRICT,
  status ai_job_status NOT NULL DEFAULT 'QUEUED',
  input_snapshot_redacted jsonb NOT NULL,
  input_hash char(64) NOT NULL,
  queued_at timestamptz NOT NULL,
  started_at timestamptz,
  completed_at timestamptz,
  attempt_count integer NOT NULL DEFAULT 0 CHECK (attempt_count >= 0),
  last_error_code varchar(80),
  kill_switch_snapshot boolean NOT NULL,
  trace_id varchar(64) NOT NULL,
  CHECK (input_hash ~ '^[0-9a-fA-F]{64}$')
);
COMMENT ON TABLE ai_jobs IS 'TBL-AIX-004 — asynchronous, policy-bound AI job.';
CREATE INDEX ai_jobs_status_created_idx ON ai_jobs (status, created_at, id);
CREATE INDEX ai_jobs_actor_created_idx ON ai_jobs (actor_subject_id, created_at DESC);
CREATE INDEX ai_jobs_tenant_resource_created_idx ON ai_jobs (tenant_id, resource_type, resource_id, created_at DESC);

CREATE TABLE ai_outputs (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  ai_job_id uuid NOT NULL UNIQUE REFERENCES ai_jobs(id) ON DELETE RESTRICT,
  output_json jsonb NOT NULL,
  output_text text,
  output_hash char(64) NOT NULL,
  safety_flags varchar(80)[] NOT NULL DEFAULT '{}',
  provider_request_id varchar(160),
  latency_ms integer NOT NULL CHECK (latency_ms >= 0),
  token_usage jsonb,
  generated_at timestamptz NOT NULL,
  CHECK (output_hash ~ '^[0-9a-fA-F]{64}$')
);
COMMENT ON TABLE ai_outputs IS 'TBL-AIX-005 — immutable DERIVED_SENSITIVE AI output.';
CREATE INDEX ai_outputs_generated_idx ON ai_outputs (generated_at);

CREATE TABLE ai_human_reviews (
  id uuid PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  ai_job_id uuid NOT NULL REFERENCES ai_jobs(id) ON DELETE RESTRICT,
  output_id uuid NOT NULL REFERENCES ai_outputs(id) ON DELETE RESTRICT,
  reviewer_subject_id uuid NOT NULL,
  decision ai_review_decision NOT NULL,
  edited_output_snapshot jsonb,
  reason_codes varchar(80)[] NOT NULL DEFAULT '{}',
  comment varchar(2000),
  applied_to_resource_at timestamptz,
  trace_id varchar(64) NOT NULL,
  CHECK (decision <> 'EDITED_ACCEPT' OR edited_output_snapshot IS NOT NULL),
  CHECK (decision <> 'REJECTED' OR cardinality(reason_codes) > 0)
);
COMMENT ON TABLE ai_human_reviews IS 'TBL-AIX-006 — append-only human review of AI output.';
CREATE INDEX ai_human_reviews_job_occurred_idx ON ai_human_reviews (ai_job_id, occurred_at DESC);
CREATE INDEX ai_human_reviews_reviewer_occurred_idx ON ai_human_reviews (reviewer_subject_id, occurred_at DESC);

CREATE TABLE match_score_snapshots (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  tenant_id uuid NOT NULL,
  job_revision_id uuid NOT NULL,
  candidate_id uuid NOT NULL REFERENCES candidate_profiles(id) ON DELETE RESTRICT,
  application_id uuid,
  algorithm_version varchar(80) NOT NULL,
  feature_policy_version integer NOT NULL CHECK (feature_policy_version >= 1),
  allowed_feature_snapshot jsonb NOT NULL,
  score numeric(5,2) NOT NULL CHECK (score BETWEEN 0 AND 100),
  explanation jsonb NOT NULL,
  ai_job_id uuid REFERENCES ai_jobs(id) ON DELETE RESTRICT,
  calculated_at timestamptz NOT NULL,
  expires_at timestamptz NOT NULL,
  UNIQUE (tenant_id, id),
  FOREIGN KEY (tenant_id, job_revision_id) REFERENCES job_revisions(tenant_id, id) ON DELETE RESTRICT,
  FOREIGN KEY (tenant_id, application_id) REFERENCES applications(tenant_id, id) ON DELETE RESTRICT,
  CHECK (expires_at > calculated_at)
);
COMMENT ON TABLE match_score_snapshots IS 'TBL-AIX-007 — immutable, non-authoritative match score snapshot.';
CREATE INDEX match_score_snapshots_tenant_revision_score_idx ON match_score_snapshots (tenant_id, job_revision_id, score DESC);
CREATE INDEX match_score_snapshots_application_calculated_idx ON match_score_snapshots (application_id, calculated_at DESC);

CREATE TABLE ai_kill_switches (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  capability varchar(40) NOT NULL UNIQUE,
  disabled boolean NOT NULL DEFAULT false,
  reason varchar(1000),
  changed_by_subject_id uuid NOT NULL,
  changed_at timestamptz NOT NULL,
  expires_at timestamptz,
  CHECK (NOT disabled OR reason IS NOT NULL)
);
COMMENT ON TABLE ai_kill_switches IS 'TBL-AIX-008 — audit-backed AI capability kill switch.';
CREATE INDEX ai_kill_switches_disabled_capability_idx ON ai_kill_switches (disabled, capability);

-- TBL-PAY-001 through TBL-PAY-014: products, payment and financial evidence.
CREATE TABLE products (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  code varchar(80) NOT NULL UNIQUE,
  buyer_type varchar(20) NOT NULL CHECK (buyer_type IN ('CANDIDATE', 'ENTERPRISE')),
  name varchar(200) NOT NULL,
  description varchar(2000) NOT NULL,
  product_type varchar(32) NOT NULL CHECK (product_type IN (
    'PACKAGE', 'CREDIT_PACK', 'PREMIUM_TEMPLATE', 'SPONSORED_PLACEMENT'
  )),
  entitlement_code varchar(80) NOT NULL,
  credit_amount bigint CHECK (credit_amount >= 0),
  validity_days integer NOT NULL CHECK (validity_days BETWEEN 1 AND 3650),
  active_from timestamptz NOT NULL,
  active_until timestamptz,
  CHECK (active_until IS NULL OR active_until > active_from)
);
COMMENT ON TABLE products IS 'TBL-PAY-001 — published product catalogue.';
CREATE INDEX products_buyer_active_idx ON products (buyer_type, active_from, active_until);

CREATE TABLE product_prices (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  product_id uuid NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
  version_no integer NOT NULL CHECK (version_no >= 1),
  currency char(3) NOT NULL DEFAULT 'VND' CHECK (currency = 'VND'),
  amount_vnd bigint NOT NULL CHECK (amount_vnd > 0),
  tax_rate numeric(5,2) NOT NULL DEFAULT 0 CHECK (tax_rate BETWEEN 0 AND 100),
  valid_from timestamptz NOT NULL,
  valid_until timestamptz,
  created_by_subject_id uuid NOT NULL,
  UNIQUE (product_id, version_no),
  CHECK (valid_until IS NULL OR valid_until > valid_from),
  EXCLUDE USING gist (
    product_id WITH =,
    tstzrange(valid_from, COALESCE(valid_until, 'infinity'::timestamptz), '[)') WITH &&
  )
);
COMMENT ON TABLE product_prices IS 'TBL-PAY-002 — immutable, non-overlapping VND price version.';
CREATE INDEX product_prices_product_valid_from_idx ON product_prices (product_id, valid_from DESC);

CREATE TABLE orders (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  order_no varchar(40) NOT NULL UNIQUE,
  buyer_subject_id uuid NOT NULL,
  buyer_type varchar(20) NOT NULL CHECK (buyer_type IN ('CANDIDATE', 'ENTERPRISE')),
  tenant_id uuid REFERENCES enterprise_tenants(id) ON DELETE RESTRICT,
  status order_status NOT NULL DEFAULT 'CREATED',
  currency char(3) NOT NULL DEFAULT 'VND' CHECK (currency = 'VND'),
  subtotal_vnd bigint NOT NULL CHECK (subtotal_vnd >= 0),
  tax_vnd bigint NOT NULL CHECK (tax_vnd >= 0),
  total_vnd bigint NOT NULL CHECK (total_vnd >= 0),
  pricing_snapshot jsonb NOT NULL,
  created_at_client timestamptz,
  expires_at timestamptz NOT NULL,
  settled_at timestamptz,
  failed_at timestamptz,
  cancelled_at timestamptz,
  idempotency_key_hash char(64) NOT NULL,
  UNIQUE (buyer_subject_id, idempotency_key_hash),
  CHECK (total_vnd = subtotal_vnd + tax_vnd),
  CHECK ((buyer_type = 'ENTERPRISE') = (tenant_id IS NOT NULL)),
  CHECK (idempotency_key_hash ~ '^[0-9a-fA-F]{64}$')
);
COMMENT ON TABLE orders IS 'TBL-PAY-003 — payment order; checkout return cannot settle it.';
CREATE INDEX orders_buyer_created_idx ON orders (buyer_subject_id, created_at DESC);
CREATE INDEX orders_tenant_status_created_idx ON orders (tenant_id, status, created_at DESC);
CREATE INDEX orders_status_expires_idx ON orders (status, expires_at);

CREATE TABLE order_items (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  order_id uuid NOT NULL REFERENCES orders(id) ON DELETE RESTRICT,
  product_id uuid NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
  price_version_id uuid NOT NULL REFERENCES product_prices(id) ON DELETE RESTRICT,
  quantity integer NOT NULL CHECK (quantity BETWEEN 1 AND 10000),
  unit_amount_vnd bigint NOT NULL CHECK (unit_amount_vnd > 0),
  tax_vnd bigint NOT NULL CHECK (tax_vnd >= 0),
  line_total_vnd bigint NOT NULL CHECK (line_total_vnd >= 0),
  product_snapshot jsonb NOT NULL,
  UNIQUE (order_id, product_id, price_version_id),
  CHECK (line_total_vnd = quantity * unit_amount_vnd + tax_vnd)
);
COMMENT ON TABLE order_items IS 'TBL-PAY-004 — immutable order line and price snapshot.';
CREATE INDEX order_items_order_idx ON order_items (order_id);

CREATE TABLE payment_attempts (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  order_id uuid NOT NULL REFERENCES orders(id) ON DELETE RESTRICT,
  attempt_no integer NOT NULL CHECK (attempt_no >= 1),
  provider payment_provider NOT NULL,
  status payment_status NOT NULL DEFAULT 'CREATED',
  amount_vnd bigint NOT NULL CHECK (amount_vnd > 0),
  provider_order_id varchar(160) NOT NULL,
  provider_transaction_id varchar(160),
  request_payload_hash char(64) NOT NULL,
  response_code varchar(80),
  checkout_url_ciphertext bytea,
  return_seen_at timestamptz,
  settled_at timestamptz,
  failed_at timestamptz,
  expires_at timestamptz NOT NULL,
  last_provider_occurred_at timestamptz,
  UNIQUE (order_id, attempt_no),
  UNIQUE (provider, provider_order_id),
  CHECK (request_payload_hash ~ '^[0-9a-fA-F]{64}$')
);
COMMENT ON TABLE payment_attempts IS 'TBL-PAY-005 — provider payment attempt; only verified events/reconciliation settle it.';
CREATE UNIQUE INDEX payment_attempts_provider_transaction_idx
  ON payment_attempts (provider, provider_transaction_id)
  WHERE provider_transaction_id IS NOT NULL;
CREATE INDEX payment_attempts_order_attempt_idx ON payment_attempts (order_id, attempt_no DESC);
CREATE INDEX payment_attempts_provider_status_idx ON payment_attempts (provider, status, updated_at);
CREATE INDEX payment_attempts_status_expires_idx ON payment_attempts (status, expires_at);

CREATE TABLE payment_webhook_events (
  id uuid PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  provider payment_provider NOT NULL,
  provider_event_id varchar(200) NOT NULL,
  provider_order_id varchar(160) NOT NULL,
  provider_transaction_id varchar(160),
  provider_occurred_at timestamptz,
  received_at timestamptz NOT NULL,
  signature_valid boolean NOT NULL,
  source_ip_hash char(64),
  headers_redacted jsonb NOT NULL,
  payload_ciphertext bytea NOT NULL,
  payload_hash char(64) NOT NULL,
  processing_status varchar(24) NOT NULL DEFAULT 'RECEIVED',
  processed_at timestamptz,
  result_code varchar(80),
  trace_id varchar(64) NOT NULL,
  UNIQUE (provider, provider_event_id),
  UNIQUE (provider, payload_hash),
  CHECK (payload_hash ~ '^[0-9a-fA-F]{64}$')
);
COMMENT ON TABLE payment_webhook_events IS 'TBL-PAY-006 — append-only encrypted payment webhook evidence.';
CREATE INDEX payment_webhook_events_processing_received_idx ON payment_webhook_events (processing_status, received_at, id);
CREATE INDEX payment_webhook_events_provider_order_received_idx ON payment_webhook_events (provider, provider_order_id, received_at DESC);

CREATE TABLE payment_reconciliations (
  id uuid PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  provider payment_provider NOT NULL,
  payment_attempt_id uuid REFERENCES payment_attempts(id) ON DELETE RESTRICT,
  reconciliation_date date NOT NULL,
  provider_status varchar(80) NOT NULL,
  local_status payment_status,
  amount_vnd bigint NOT NULL CHECK (amount_vnd >= 0),
  matched boolean NOT NULL,
  discrepancy_code varchar(80),
  provider_payload_hash char(64) NOT NULL,
  resolved_at timestamptz,
  resolved_by_subject_id uuid,
  resolution_note varchar(1000),
  CHECK (matched OR discrepancy_code IS NOT NULL),
  CHECK ((resolved_at IS NULL AND resolved_by_subject_id IS NULL AND resolution_note IS NULL)
     OR (resolved_at IS NOT NULL AND resolved_by_subject_id IS NOT NULL AND resolution_note IS NOT NULL))
);
COMMENT ON TABLE payment_reconciliations IS 'TBL-PAY-007 — append-only payment reconciliation evidence.';
CREATE INDEX payment_reconciliations_provider_date_matched_idx ON payment_reconciliations (provider, reconciliation_date, matched);
CREATE INDEX payment_reconciliations_attempt_occurred_idx ON payment_reconciliations (payment_attempt_id, occurred_at DESC);

CREATE TABLE refunds (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  order_id uuid NOT NULL REFERENCES orders(id) ON DELETE RESTRICT,
  payment_attempt_id uuid NOT NULL REFERENCES payment_attempts(id) ON DELETE RESTRICT,
  refund_no varchar(60) NOT NULL UNIQUE,
  amount_vnd bigint NOT NULL CHECK (amount_vnd > 0),
  reason_code varchar(80) NOT NULL,
  reason_text varchar(1000),
  status varchar(24) NOT NULL DEFAULT 'REQUESTED'
    CHECK (status IN ('REQUESTED', 'APPROVED', 'PROCESSING', 'SETTLED', 'FAILED', 'REJECTED')),
  requested_by_subject_id uuid NOT NULL,
  approved_by_subject_id uuid,
  provider_refund_id varchar(160),
  requested_at timestamptz NOT NULL,
  processed_at timestamptz,
  failed_at timestamptz,
  CHECK (approved_by_subject_id IS NULL OR approved_by_subject_id <> requested_by_subject_id)
);
COMMENT ON TABLE refunds IS 'TBL-PAY-008 — refund request with maker-checker fields.';
CREATE UNIQUE INDEX refunds_provider_refund_idx ON refunds (provider_refund_id) WHERE provider_refund_id IS NOT NULL;
CREATE INDEX refunds_order_created_idx ON refunds (order_id, created_at DESC);
CREATE INDEX refunds_status_created_idx ON refunds (status, created_at);

CREATE TABLE chargebacks (
  id uuid PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  payment_attempt_id uuid NOT NULL REFERENCES payment_attempts(id) ON DELETE RESTRICT,
  provider_case_id varchar(160) NOT NULL,
  amount_vnd bigint NOT NULL CHECK (amount_vnd > 0),
  reason_code varchar(80) NOT NULL,
  status varchar(24) NOT NULL CHECK (status IN ('OPEN', 'WON', 'LOST', 'CLOSED')),
  opened_at timestamptz NOT NULL,
  resolved_at timestamptz,
  resolution varchar(80),
  provider_payload_hash char(64) NOT NULL,
  UNIQUE (payment_attempt_id, provider_case_id)
);
COMMENT ON TABLE chargebacks IS 'TBL-PAY-009 — append-only payment chargeback evidence.';
CREATE INDEX chargebacks_status_opened_idx ON chargebacks (status, opened_at);

CREATE TABLE entitlements (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  owner_subject_id uuid NOT NULL,
  owner_type varchar(20) NOT NULL CHECK (owner_type IN ('CANDIDATE', 'ENTERPRISE')),
  tenant_id uuid REFERENCES enterprise_tenants(id) ON DELETE RESTRICT,
  order_item_id uuid NOT NULL REFERENCES order_items(id) ON DELETE RESTRICT,
  code varchar(80) NOT NULL,
  status entitlement_status NOT NULL DEFAULT 'ACTIVE',
  quantity_total bigint NOT NULL CHECK (quantity_total >= 0),
  quantity_consumed bigint NOT NULL DEFAULT 0 CHECK (quantity_consumed >= 0),
  valid_from timestamptz NOT NULL,
  valid_until timestamptz,
  activated_at timestamptz NOT NULL,
  frozen_at timestamptz,
  revoked_at timestamptz,
  revoke_reason varchar(500),
  UNIQUE (order_item_id, code),
  CHECK (quantity_consumed <= quantity_total),
  CHECK ((owner_type = 'ENTERPRISE') = (tenant_id IS NOT NULL)),
  CHECK (valid_until IS NULL OR valid_until > valid_from)
);
COMMENT ON TABLE entitlements IS 'TBL-PAY-010 — settled-payment entitlement only; no pending entitlement state.';
CREATE INDEX entitlements_owner_code_status_idx ON entitlements (owner_subject_id, code, status, valid_until);
CREATE INDEX entitlements_tenant_code_status_idx ON entitlements (tenant_id, code, status, valid_until);

CREATE TABLE credit_ledger_entries (
  id uuid PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  entitlement_id uuid NOT NULL REFERENCES entitlements(id) ON DELETE RESTRICT,
  owner_subject_id uuid NOT NULL,
  tenant_id uuid REFERENCES enterprise_tenants(id) ON DELETE RESTRICT,
  entry_type ledger_entry_type NOT NULL,
  quantity_delta bigint NOT NULL CHECK (quantity_delta <> 0),
  balance_after bigint NOT NULL CHECK (balance_after >= 0),
  reference_type varchar(40) NOT NULL,
  reference_id uuid NOT NULL,
  idempotency_key varchar(180) NOT NULL,
  actor_subject_id uuid,
  reason varchar(500),
  UNIQUE (entitlement_id, idempotency_key),
  CHECK (
    (entry_type IN ('GRANT', 'REFUND') AND quantity_delta > 0)
    OR (entry_type IN ('SPEND', 'EXPIRE') AND quantity_delta < 0)
    OR entry_type IN ('REVERSAL', 'ADJUSTMENT')
  )
);
COMMENT ON TABLE credit_ledger_entries IS 'TBL-PAY-011 — append-only entitlement ledger.';
CREATE INDEX credit_ledger_entries_entitlement_occurred_idx ON credit_ledger_entries (entitlement_id, occurred_at, id);
CREATE INDEX credit_ledger_entries_tenant_occurred_idx ON credit_ledger_entries (tenant_id, occurred_at DESC);

CREATE TABLE promotion_campaigns (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  code varchar(80) NOT NULL UNIQUE,
  name varchar(200) NOT NULL,
  promotion_type varchar(32) NOT NULL CHECK (promotion_type IN ('SPONSORED_PROFILE', 'SPONSORED_JOB')),
  sponsor_subject_id uuid NOT NULL,
  sponsor_tenant_id uuid REFERENCES enterprise_tenants(id) ON DELETE RESTRICT,
  status promotion_status NOT NULL DEFAULT 'SCHEDULED',
  starts_at timestamptz NOT NULL,
  ends_at timestamptz NOT NULL,
  budget_vnd bigint CHECK (budget_vnd >= 0),
  label_text varchar(120) NOT NULL DEFAULT 'Được tài trợ' CHECK (length(btrim(label_text)) > 0),
  targeting_rules jsonb NOT NULL,
  created_by_subject_id uuid NOT NULL,
  approved_by_subject_id uuid NOT NULL,
  CHECK (ends_at > starts_at),
  CHECK (created_by_subject_id <> approved_by_subject_id)
);
COMMENT ON TABLE promotion_campaigns IS 'TBL-PAY-012 — sponsored campaign, isolated from organic matching and ATS.';
CREATE INDEX promotion_campaigns_status_time_idx ON promotion_campaigns (status, starts_at, ends_at);
CREATE INDEX promotion_campaigns_sponsor_status_idx ON promotion_campaigns (sponsor_tenant_id, status);

CREATE TABLE sponsored_placements (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  campaign_id uuid NOT NULL REFERENCES promotion_campaigns(id) ON DELETE RESTRICT,
  resource_type varchar(24) NOT NULL CHECK (resource_type IN ('CANDIDATE_PROFILE', 'JOB')),
  resource_id uuid NOT NULL,
  entitlement_id uuid NOT NULL REFERENCES entitlements(id) ON DELETE RESTRICT,
  starts_at timestamptz NOT NULL,
  ends_at timestamptz NOT NULL,
  status promotion_status NOT NULL,
  label_text varchar(120) NOT NULL CHECK (length(btrim(label_text)) > 0),
  targeting_snapshot jsonb NOT NULL,
  impression_count bigint NOT NULL DEFAULT 0 CHECK (impression_count >= 0),
  click_count bigint NOT NULL DEFAULT 0 CHECK (click_count >= 0),
  CHECK (ends_at > starts_at)
);
COMMENT ON TABLE sponsored_placements IS 'TBL-PAY-013 — isolated sponsored placement.';
CREATE INDEX sponsored_placements_resource_status_time_idx ON sponsored_placements (resource_type, status, starts_at, ends_at);
CREATE INDEX sponsored_placements_campaign_status_idx ON sponsored_placements (campaign_id, status);

CREATE TABLE invoices (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  order_id uuid NOT NULL UNIQUE REFERENCES orders(id) ON DELETE RESTRICT,
  invoice_no varchar(60) NOT NULL UNIQUE,
  buyer_snapshot jsonb NOT NULL,
  tax_snapshot jsonb NOT NULL,
  amount_vnd bigint NOT NULL CHECK (amount_vnd >= 0),
  issued_at timestamptz NOT NULL,
  file_id uuid NOT NULL REFERENCES file_objects(id) ON DELETE RESTRICT,
  content_hash char(64) NOT NULL,
  voided_at timestamptz,
  void_reason varchar(500),
  replacement_invoice_id uuid REFERENCES invoices(id) ON DELETE RESTRICT,
  CHECK (voided_at IS NOT NULL OR void_reason IS NULL)
);
COMMENT ON TABLE invoices IS 'TBL-PAY-014 — immutable financial invoice with replacement-only correction.';
CREATE INDEX invoices_issued_idx ON invoices (issued_at DESC);

-- TBL-WRK-057 through TBL-WRK-076: notifications, operations and later pilot tables.
CREATE TABLE notification_preferences (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  identity_subject_id uuid NOT NULL,
  category varchar(40) NOT NULL,
  in_app_enabled boolean NOT NULL DEFAULT true,
  email_enabled boolean NOT NULL DEFAULT true,
  quiet_hours_start time,
  quiet_hours_end time,
  timezone varchar(64) NOT NULL,
  consent_source varchar(40) NOT NULL,
  UNIQUE (identity_subject_id, category),
  CHECK (
    category NOT IN ('TRANSACTIONAL', 'SECURITY')
    OR (in_app_enabled OR email_enabled)
  )
);
COMMENT ON TABLE notification_preferences IS 'TBL-WRK-057 — per-subject notification preference.';
CREATE INDEX notification_preferences_subject_category_idx ON notification_preferences (identity_subject_id, category);

CREATE TABLE notifications (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  identity_subject_id uuid NOT NULL,
  tenant_id uuid,
  category varchar(40) NOT NULL,
  template_code varchar(80) NOT NULL,
  template_version integer NOT NULL CHECK (template_version >= 1),
  title varchar(200) NOT NULL,
  body varchar(4000) NOT NULL,
  action_url varchar(1000),
  dedupe_key varchar(180) NOT NULL,
  read_at timestamptz,
  expires_at timestamptz NOT NULL,
  payload jsonb NOT NULL DEFAULT '{}',
  UNIQUE (identity_subject_id, dedupe_key),
  CHECK (action_url IS NULL OR action_url ~ '^https?://')
);
COMMENT ON TABLE notifications IS 'TBL-WRK-058 — redacted, expiring notification.';
CREATE INDEX notifications_subject_cursor_idx
  ON notifications (identity_subject_id, read_at, created_at DESC, id DESC);
CREATE INDEX notifications_expires_idx ON notifications (expires_at);

CREATE TABLE notification_deliveries (
  id uuid PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  notification_id uuid NOT NULL REFERENCES notifications(id) ON DELETE RESTRICT,
  channel varchar(16) NOT NULL CHECK (channel IN ('IN_APP', 'EMAIL')),
  status notification_status NOT NULL,
  provider_message_id varchar(160),
  attempt_no integer NOT NULL CHECK (attempt_no >= 1),
  error_code varchar(80),
  next_retry_at timestamptz,
  dedupe_key varchar(180) NOT NULL,
  UNIQUE (notification_id, channel, attempt_no),
  UNIQUE (dedupe_key)
);
COMMENT ON TABLE notification_deliveries IS 'TBL-WRK-059 — append-only notification delivery attempt.';
CREATE INDEX notification_deliveries_status_retry_idx ON notification_deliveries (status, next_retry_at);

CREATE TABLE moderation_reports (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  reporter_subject_id uuid NOT NULL,
  tenant_id uuid,
  resource_type varchar(40) NOT NULL,
  resource_id uuid NOT NULL,
  reason_code varchar(80) NOT NULL,
  description varchar(2000),
  evidence_file_ids uuid[] NOT NULL DEFAULT '{}',
  status varchar(24) NOT NULL DEFAULT 'OPEN'
    CHECK (status IN ('OPEN', 'IN_REVIEW', 'RESOLVED', 'DISMISSED')),
  assigned_to_subject_id uuid,
  decision varchar(80),
  resolved_at timestamptz,
  CHECK (status NOT IN ('RESOLVED', 'DISMISSED') OR (decision IS NOT NULL AND resolved_at IS NOT NULL))
);
COMMENT ON TABLE moderation_reports IS 'TBL-WRK-060 — moderation report; referenced files must be CLEAN at application boundary.';
CREATE INDEX moderation_reports_status_created_idx ON moderation_reports (status, created_at);
CREATE INDEX moderation_reports_resource_created_idx ON moderation_reports (resource_type, resource_id, created_at DESC);

CREATE TABLE audit_events (
  id uuid PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  actor_subject_id uuid,
  action varchar(120) NOT NULL,
  resource_type varchar(80) NOT NULL,
  resource_id uuid,
  outcome audit_outcome NOT NULL,
  business_code varchar(80) NOT NULL,
  trace_id varchar(64) NOT NULL,
  tenant_context jsonb,
  changes jsonb,
  metadata jsonb NOT NULL DEFAULT '{}',
  prev_hash char(64),
  event_hash char(64) NOT NULL UNIQUE,
  legal_hold_until timestamptz,
  CHECK (event_hash ~ '^[0-9a-fA-F]{64}$')
);
COMMENT ON TABLE audit_events IS 'TBL-WRK-061 — append-only, hash-chained work service audit event.';
CREATE INDEX audit_events_resource_occurred_idx ON audit_events (resource_type, resource_id, occurred_at DESC);
CREATE INDEX audit_events_actor_occurred_idx ON audit_events (actor_subject_id, occurred_at DESC);
CREATE INDEX audit_events_trace_idx ON audit_events (trace_id);
CREATE INDEX audit_events_occurred_brin_idx ON audit_events USING brin (occurred_at);

CREATE TABLE idempotency_keys (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  actor_subject_id uuid,
  operation varchar(120) NOT NULL,
  key_hash char(64) NOT NULL,
  request_hash char(64) NOT NULL,
  response_status integer,
  response_body jsonb,
  locked_until timestamptz,
  completed_at timestamptz,
  expires_at timestamptz NOT NULL,
  UNIQUE NULLS NOT DISTINCT (actor_subject_id, operation, key_hash),
  CHECK (key_hash ~ '^[0-9a-fA-F]{64}$'),
  CHECK (request_hash ~ '^[0-9a-fA-F]{64}$')
);
COMMENT ON TABLE idempotency_keys IS 'TBL-WRK-062 — masked response/idempotency record.';
CREATE INDEX idempotency_keys_expires_idx ON idempotency_keys (expires_at);

CREATE TABLE outbox_events (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  aggregate_type varchar(80) NOT NULL,
  aggregate_id uuid NOT NULL,
  event_type varchar(120) NOT NULL,
  event_version integer NOT NULL CHECK (event_version >= 1),
  payload jsonb NOT NULL,
  available_at timestamptz NOT NULL DEFAULT now(),
  dedupe_key varchar(180) NOT NULL UNIQUE,
  trace_id varchar(64) NOT NULL
);
COMMENT ON TABLE outbox_events IS 'TBL-WRK-063 — immutable transactional outbox event.';
CREATE INDEX outbox_events_available_idx ON outbox_events (available_at, id);
CREATE INDEX outbox_events_aggregate_created_idx ON outbox_events (aggregate_type, aggregate_id, created_at);

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
  UNIQUE (consumer, event_id),
  CHECK (payload_hash ~ '^[0-9a-fA-F]{64}$')
);
COMMENT ON TABLE consumer_inbox IS 'TBL-WRK-064 — immutable signed-event inbox/deduplication record.';
CREATE INDEX consumer_inbox_consumer_processed_received_idx ON consumer_inbox (consumer, processed_at, received_at);

CREATE TABLE admin_adjustments (
  id uuid PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  tenant_id uuid,
  target_type varchar(32) NOT NULL,
  target_id uuid NOT NULL,
  action varchar(80) NOT NULL,
  before_snapshot jsonb NOT NULL,
  after_snapshot jsonb NOT NULL,
  reason varchar(1000) NOT NULL,
  approved_by_subject_id uuid NOT NULL,
  performed_by_subject_id uuid NOT NULL,
  trace_id varchar(64) NOT NULL,
  CHECK (
    target_type NOT IN ('PAYMENT', 'CREDIT')
    OR approved_by_subject_id <> performed_by_subject_id
  )
);
COMMENT ON TABLE admin_adjustments IS 'TBL-WRK-065 — append-only admin adjustment audit evidence.';
CREATE INDEX admin_adjustments_target_occurred_idx ON admin_adjustments (target_type, target_id, occurred_at DESC);
CREATE INDEX admin_adjustments_tenant_occurred_idx ON admin_adjustments (tenant_id, occurred_at DESC);

CREATE TABLE tenant_roles (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_type varchar(20) NOT NULL CHECK (tenant_type IN ('ENTERPRISE', 'UNIVERSITY')),
  code varchar(40) NOT NULL,
  name varchar(120) NOT NULL,
  description varchar(500) NOT NULL,
  is_system boolean NOT NULL DEFAULT true,
  is_privileged boolean NOT NULL DEFAULT false,
  disabled_at timestamptz,
  UNIQUE (tenant_type, code)
);
COMMENT ON TABLE tenant_roles IS 'TBL-WRK-066 — tenant role catalogue.';
CREATE INDEX tenant_roles_type_disabled_code_idx ON tenant_roles (tenant_type, disabled_at, code);

CREATE TABLE tenant_permissions (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  code varchar(120) NOT NULL UNIQUE,
  tenant_type varchar(20) NOT NULL CHECK (tenant_type IN ('ENTERPRISE', 'UNIVERSITY', 'BOTH')),
  description varchar(500) NOT NULL,
  risk_level smallint NOT NULL DEFAULT 1 CHECK (risk_level BETWEEN 1 AND 5),
  disabled_at timestamptz
);
COMMENT ON TABLE tenant_permissions IS 'TBL-WRK-067 — tenant permission catalogue.';
CREATE INDEX tenant_permissions_type_disabled_code_idx ON tenant_permissions (tenant_type, disabled_at, code);

CREATE TABLE tenant_role_permissions (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  role_id uuid NOT NULL REFERENCES tenant_roles(id) ON DELETE RESTRICT,
  permission_id uuid NOT NULL REFERENCES tenant_permissions(id) ON DELETE RESTRICT,
  granted_by_subject_id uuid NOT NULL,
  valid_from timestamptz NOT NULL DEFAULT now(),
  valid_until timestamptz,
  revoked_at timestamptz,
  revoked_by_subject_id uuid,
  reason varchar(500) NOT NULL,
  CHECK (valid_until IS NULL OR valid_until > valid_from),
  CHECK ((revoked_at IS NULL AND revoked_by_subject_id IS NULL) OR revoked_at IS NOT NULL)
);
COMMENT ON TABLE tenant_role_permissions IS 'TBL-WRK-068 — immutable role permission grant with one-way revocation.';
CREATE UNIQUE INDEX tenant_role_permissions_active_idx
  ON tenant_role_permissions (role_id, permission_id) WHERE revoked_at IS NULL;
CREATE INDEX tenant_role_permissions_role_active_idx ON tenant_role_permissions (role_id, revoked_at, valid_until);
CREATE INDEX tenant_role_permissions_permission_active_idx ON tenant_role_permissions (permission_id, revoked_at);

CREATE TABLE application_evidence_state_events (
  id uuid PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  tenant_id uuid NOT NULL,
  application_id uuid NOT NULL,
  study_evidence_id uuid NOT NULL,
  from_status evidence_export_status,
  to_status evidence_export_status NOT NULL,
  source varchar(32) NOT NULL,
  actor_subject_id uuid,
  source_event_id uuid,
  reason_code varchar(80) NOT NULL,
  trace_id varchar(64) NOT NULL,
  FOREIGN KEY (tenant_id, application_id) REFERENCES applications(tenant_id, id) ON DELETE RESTRICT,
  CHECK (
    (from_status IS NULL AND to_status = 'PENDING')
    OR (from_status = 'PENDING' AND to_status IN ('READY', 'UNAVAILABLE'))
    OR (from_status = 'READY' AND to_status IN ('REVOKED', 'HIDDEN'))
    OR (from_status = 'UNAVAILABLE' AND to_status IN ('PENDING', 'HIDDEN'))
    OR (from_status = 'HIDDEN' AND to_status = 'REVOKED')
  ),
  CHECK (to_status <> 'HIDDEN' OR reason_code = 'CONSENT_WITHDRAWN')
);
COMMENT ON TABLE application_evidence_state_events IS 'TBL-WRK-069 — append-only study evidence state event; snapshot rows never mutate.';
CREATE UNIQUE INDEX application_evidence_state_events_source_event_idx
  ON application_evidence_state_events (source, source_event_id) WHERE source_event_id IS NOT NULL;
CREATE INDEX application_evidence_state_events_effective_idx
  ON application_evidence_state_events (application_id, study_evidence_id, occurred_at DESC, id DESC);
CREATE INDEX application_evidence_state_events_evidence_occurred_idx
  ON application_evidence_state_events (study_evidence_id, occurred_at DESC);

CREATE TABLE outbox_delivery_attempts (
  id uuid PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  outbox_event_id uuid NOT NULL REFERENCES outbox_events(id) ON DELETE RESTRICT,
  attempt_no integer NOT NULL CHECK (attempt_no >= 1),
  status outbox_status NOT NULL,
  worker_id varchar(120) NOT NULL,
  broker_message_id varchar(180),
  error_code varchar(80),
  next_retry_at timestamptz,
  payload_hash char(64) NOT NULL,
  UNIQUE (outbox_event_id, attempt_no),
  CHECK (payload_hash ~ '^[0-9a-fA-F]{64}$')
);
COMMENT ON TABLE outbox_delivery_attempts IS 'TBL-WRK-070 — append-only outbox publication attempt.';
CREATE INDEX outbox_delivery_attempts_event_latest_idx ON outbox_delivery_attempts (outbox_event_id, occurred_at DESC);
CREATE INDEX outbox_delivery_attempts_status_retry_idx ON outbox_delivery_attempts (status, next_retry_at);

CREATE TABLE internship_program_participants (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL,
  program_id uuid NOT NULL,
  affiliation_id uuid NOT NULL,
  status varchar(24) NOT NULL DEFAULT 'ENROLLED'
    CHECK (status IN ('ENROLLED', 'COMPLETED', 'WITHDRAWN', 'REMOVED')),
  enrolled_at timestamptz NOT NULL,
  completed_at timestamptz,
  withdrawn_at timestamptz,
  outcome_code varchar(80),
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, program_id, affiliation_id),
  FOREIGN KEY (tenant_id, program_id) REFERENCES internship_programs(tenant_id, id) ON DELETE RESTRICT,
  FOREIGN KEY (tenant_id, affiliation_id) REFERENCES student_affiliations(tenant_id, id) ON DELETE RESTRICT,
  CHECK (status <> 'COMPLETED' OR completed_at IS NOT NULL),
  CHECK (status NOT IN ('WITHDRAWN', 'REMOVED') OR withdrawn_at IS NOT NULL)
);
COMMENT ON TABLE internship_program_participants IS 'TBL-WRK-071 — university program participant.';
CREATE INDEX internship_program_participants_program_status_idx ON internship_program_participants (tenant_id, program_id, status);
CREATE INDEX internship_program_participants_affiliation_created_idx ON internship_program_participants (tenant_id, affiliation_id, created_at DESC);

CREATE TABLE application_offer_versions (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  tenant_id uuid NOT NULL,
  application_id uuid NOT NULL,
  version_no integer NOT NULL CHECK (version_no >= 1),
  title varchar(200) NOT NULL,
  terms_snapshot jsonb NOT NULL,
  salary_vnd bigint CHECK (salary_vnd >= 0),
  starts_on date,
  expires_at timestamptz NOT NULL,
  created_by_subject_id uuid NOT NULL,
  approved_by_subject_id uuid NOT NULL,
  issued_at timestamptz NOT NULL,
  supersedes_version_id uuid REFERENCES application_offer_versions(id) ON DELETE RESTRICT,
  content_hash char(64) NOT NULL,
  UNIQUE (tenant_id, id),
  UNIQUE (application_id, version_no),
  FOREIGN KEY (tenant_id, application_id) REFERENCES applications(tenant_id, id) ON DELETE RESTRICT,
  CHECK (expires_at > issued_at),
  CHECK (created_by_subject_id <> approved_by_subject_id)
);
COMMENT ON TABLE application_offer_versions IS 'TBL-WRK-072 — immutable offer version with maker-checker approval.';
CREATE INDEX application_offer_versions_application_version_idx ON application_offer_versions (application_id, version_no DESC);

CREATE TABLE application_offer_state_events (
  id uuid PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  tenant_id uuid NOT NULL,
  application_id uuid NOT NULL,
  offer_version_id uuid NOT NULL,
  from_status varchar(24),
  to_status varchar(24) NOT NULL CHECK (to_status IN (
    'ISSUED', 'VIEWED', 'ACCEPTED', 'DECLINED', 'EXPIRED', 'WITHDRAWN'
  )),
  actor_subject_id uuid NOT NULL,
  reason_code varchar(80) NOT NULL,
  trace_id varchar(64) NOT NULL,
  FOREIGN KEY (tenant_id, application_id) REFERENCES applications(tenant_id, id) ON DELETE RESTRICT,
  FOREIGN KEY (tenant_id, offer_version_id) REFERENCES application_offer_versions(tenant_id, id) ON DELETE RESTRICT
);
COMMENT ON TABLE application_offer_state_events IS 'TBL-WRK-073 — append-only offer lifecycle event.';
CREATE INDEX application_offer_state_events_application_idx ON application_offer_state_events (application_id, occurred_at, id);
CREATE INDEX application_offer_state_events_offer_occurred_idx ON application_offer_state_events (offer_version_id, occurred_at DESC);

CREATE TABLE job_screening_questions (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  tenant_id uuid NOT NULL,
  job_revision_id uuid NOT NULL,
  question_type varchar(24) NOT NULL CHECK (question_type IN (
    'TEXT', 'SINGLE_CHOICE', 'MULTIPLE_CHOICE', 'YES_NO', 'NUMBER'
  )),
  prompt varchar(1000) NOT NULL,
  is_required boolean NOT NULL DEFAULT false,
  options jsonb,
  validation_rule jsonb,
  position integer NOT NULL,
  UNIQUE (job_revision_id, position),
  FOREIGN KEY (tenant_id, job_revision_id) REFERENCES job_revisions(tenant_id, id) ON DELETE RESTRICT
);
COMMENT ON TABLE job_screening_questions IS 'TBL-WRK-074 — immutable-after-submission screening question.';
CREATE INDEX job_screening_questions_tenant_revision_position_idx
  ON job_screening_questions (tenant_id, job_revision_id, position);

CREATE TABLE interview_feedback (
  id uuid PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  tenant_id uuid NOT NULL,
  interview_id uuid NOT NULL,
  reviewer_subject_id uuid NOT NULL,
  recommendation varchar(24) NOT NULL CHECK (recommendation IN (
    'STRONG_NO', 'NO', 'NEUTRAL', 'YES', 'STRONG_YES'
  )),
  score numeric(5,2) CHECK (score BETWEEN 0 AND 100),
  rubric_snapshot jsonb NOT NULL,
  comment text,
  submitted_at timestamptz NOT NULL,
  trace_id varchar(64) NOT NULL,
  UNIQUE (interview_id, reviewer_subject_id),
  FOREIGN KEY (tenant_id, interview_id) REFERENCES interviews(tenant_id, id) ON DELETE RESTRICT
);
COMMENT ON TABLE interview_feedback IS 'TBL-WRK-075 — append-only DERIVED_SENSITIVE interview feedback.';
CREATE INDEX interview_feedback_tenant_interview_submitted_idx ON interview_feedback (tenant_id, interview_id, submitted_at);

CREATE TABLE file_upload_sessions (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1 CHECK (row_version >= 1),
  file_id uuid NOT NULL UNIQUE REFERENCES file_objects(id) ON DELETE RESTRICT,
  owner_subject_id uuid NOT NULL,
  tenant_id uuid,
  upload_id varchar(200) NOT NULL UNIQUE,
  expected_size_bytes bigint NOT NULL CHECK (expected_size_bytes > 0),
  expected_sha256 char(64) NOT NULL,
  part_count integer NOT NULL DEFAULT 1 CHECK (part_count BETWEEN 1 AND 10000),
  status varchar(24) NOT NULL DEFAULT 'CREATED'
    CHECK (status IN ('CREATED', 'UPLOADING', 'COMPLETED', 'ABORTED', 'EXPIRED')),
  expires_at timestamptz NOT NULL,
  completed_at timestamptz,
  aborted_at timestamptz,
  CHECK (expected_sha256 ~ '^[0-9a-fA-F]{64}$')
);
COMMENT ON TABLE file_upload_sessions IS 'TBL-WRK-076 — file upload session; completed file is queued for malware scanning.';
CREATE INDEX file_upload_sessions_owner_status_created_idx ON file_upload_sessions (owner_subject_id, status, created_at DESC);
CREATE INDEX file_upload_sessions_tenant_status_created_idx ON file_upload_sessions (tenant_id, status, created_at DESC);
CREATE INDEX file_upload_sessions_status_expires_idx ON file_upload_sessions (status, expires_at);

-- Aggregate pointer FKs are added after both sides exist.  They prevent a
-- pointer from crossing aggregate ownership while avoiding creation-order cycles.
ALTER TABLE cv_versions ADD CONSTRAINT cv_versions_cv_id_id_key UNIQUE (cv_id, id);
ALTER TABLE cvs
  ADD CONSTRAINT cvs_current_draft_version_fk
    FOREIGN KEY (id, current_draft_version_id) REFERENCES cv_versions(cv_id, id) ON DELETE RESTRICT,
  ADD CONSTRAINT cvs_latest_published_version_fk
    FOREIGN KEY (id, latest_published_version_id) REFERENCES cv_versions(cv_id, id) ON DELETE RESTRICT;
ALTER TABLE job_revisions ADD CONSTRAINT job_revisions_job_id_id_key UNIQUE (job_id, id);
ALTER TABLE jobs
  ADD CONSTRAINT jobs_current_draft_revision_fk
    FOREIGN KEY (id, current_draft_revision_id) REFERENCES job_revisions(job_id, id) ON DELETE RESTRICT,
  ADD CONSTRAINT jobs_published_revision_fk
    FOREIGN KEY (id, published_revision_id) REFERENCES job_revisions(job_id, id) ON DELETE RESTRICT;
ALTER TABLE messages ADD CONSTRAINT messages_conversation_id_id_key UNIQUE (conversation_id, id);
ALTER TABLE conversations
  ADD CONSTRAINT conversations_last_message_fk
    FOREIGN KEY (id, last_message_id) REFERENCES messages(conversation_id, id) ON DELETE RESTRICT;
ALTER TABLE saved_jobs
  ADD CONSTRAINT saved_jobs_job_fk FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE RESTRICT;
ALTER TABLE campus_job_distributions
  ADD CONSTRAINT campus_job_distributions_job_fk FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE RESTRICT;
ALTER TABLE candidate_referrals
  ADD CONSTRAINT candidate_referrals_job_fk FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE RESTRICT;

CREATE FUNCTION app_private.cv_version_draft_only()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF OLD.status <> 'DRAFT' THEN
    RAISE EXCEPTION 'cv_versions % is immutable after leaving DRAFT', OLD.id USING ERRCODE = '55000';
  END IF;
  RETURN NEW;
END;
$$;

CREATE FUNCTION app_private.job_revision_draft_only()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF OLD.status <> 'DRAFT' THEN
    RAISE EXCEPTION 'job_revisions % is immutable after leaving DRAFT', OLD.id USING ERRCODE = '55000';
  END IF;
  RETURN NEW;
END;
$$;

CREATE FUNCTION app_private.prevent_cursor_regression()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF NEW.last_read_sequence < OLD.last_read_sequence THEN
    RAISE EXCEPTION 'conversation read cursor may only increase' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END;
$$;

CREATE FUNCTION app_private.require_payment_attempt_amount()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  required_amount bigint;
BEGIN
  SELECT total_vnd INTO required_amount FROM orders WHERE id = NEW.order_id;
  IF required_amount IS NULL OR NEW.amount_vnd <> required_amount THEN
    RAISE EXCEPTION 'payment attempt amount must equal its order total' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END;
$$;

CREATE FUNCTION app_private.require_settled_order_item()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM order_items oi
    JOIN orders o ON o.id = oi.order_id
    WHERE oi.id = NEW.order_item_id AND o.status = 'SETTLED'
  ) THEN
    RAISE EXCEPTION 'entitlement requires a SETTLED order item' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END;
$$;

CREATE FUNCTION app_private.require_published_application_revision()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM job_revisions r
    WHERE r.id = NEW.job_revision_id
      AND r.tenant_id = NEW.tenant_id
      AND r.job_id = NEW.job_id
      AND r.status = 'PUBLISHED'
  ) THEN
    RAISE EXCEPTION 'application requires a PUBLISHED revision of the same tenant and job'
      USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END;
$$;

CREATE FUNCTION app_private.require_verified_payment_settlement()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF NEW.status = 'SETTLED'
     AND (TG_OP = 'INSERT' OR OLD.status <> 'SETTLED') THEN
    IF NOT EXISTS (
      SELECT 1
      FROM payment_webhook_events w
      WHERE w.provider = NEW.provider
        AND w.provider_order_id = NEW.provider_order_id
        AND w.signature_valid
    )
    AND NOT EXISTS (
      SELECT 1
      FROM payment_reconciliations r
      WHERE r.payment_attempt_id = NEW.id
        AND r.matched
    ) THEN
      RAISE EXCEPTION 'payment attempt may settle only from verified webhook or reconciliation'
        USING ERRCODE = '23514';
    END IF;
  END IF;
  RETURN NEW;
END;
$$;

CREATE FUNCTION app_private.require_settled_payment_for_order()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF NEW.status = 'SETTLED'
     AND (TG_OP = 'INSERT' OR OLD.status <> 'SETTLED')
     AND NOT EXISTS (
       SELECT 1 FROM payment_attempts p
       WHERE p.order_id = NEW.id AND p.status = 'SETTLED'
     ) THEN
    RAISE EXCEPTION 'order may settle only after a settled payment attempt' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END;
$$;

CREATE FUNCTION app_private.validate_settled_refund_total()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  settled_refunds bigint;
  payment_amount bigint;
BEGIN
  SELECT amount_vnd INTO payment_amount
  FROM payment_attempts
  WHERE id = NEW.payment_attempt_id
  FOR UPDATE;
  SELECT COALESCE(sum(amount_vnd), 0) INTO settled_refunds
  FROM refunds
  WHERE payment_attempt_id = NEW.payment_attempt_id
    AND status = 'SETTLED'
    AND id <> COALESCE(NEW.id, '00000000-0000-0000-0000-000000000000'::uuid);
  IF NEW.status = 'SETTLED' AND settled_refunds + NEW.amount_vnd > payment_amount THEN
    RAISE EXCEPTION 'settled refunds may not exceed the payment amount' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END;
$$;

CREATE FUNCTION app_private.ensure_active_owner()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  checked_tenant uuid;
BEGIN
  IF TG_OP = 'DELETE' THEN
    checked_tenant := OLD.tenant_id;
  ELSE
    checked_tenant := NEW.tenant_id;
  END IF;
  IF TG_TABLE_NAME = 'enterprise_memberships' THEN
    IF NOT EXISTS (
      SELECT 1 FROM enterprise_memberships m
      WHERE m.tenant_id = checked_tenant
        AND m.role_code = 'OWNER'
        AND m.status = 'ACTIVE'
        AND (m.valid_until IS NULL OR m.valid_until > now())
    ) THEN
      RAISE EXCEPTION 'enterprise tenant % must retain an active OWNER', checked_tenant USING ERRCODE = '23514';
    END IF;
  ELSIF TG_TABLE_NAME = 'university_memberships' THEN
    IF NOT EXISTS (
      SELECT 1 FROM university_memberships m
      WHERE m.tenant_id = checked_tenant
        AND m.role_code = 'OWNER'
        AND m.status = 'ACTIVE'
        AND (m.valid_until IS NULL OR m.valid_until > now())
    ) THEN
      RAISE EXCEPTION 'university tenant % must retain an active OWNER', checked_tenant USING ERRCODE = '23514';
    END IF;
  END IF;
  RETURN NULL;
END;
$$;

DO $$
DECLARE
  table_name text;
BEGIN
  FOREACH table_name IN ARRAY ARRAY[
    'identity_projections', 'file_objects', 'candidate_profiles', 'candidate_search_preferences',
    'skills', 'candidate_skills', 'candidate_experiences', 'candidate_educations', 'cvs',
    'cv_versions', 'portfolio_items', 'enterprise_tenants', 'enterprise_verification_cases',
    'enterprise_memberships', 'enterprise_invites', 'university_tenants',
    'university_verification_cases', 'university_memberships', 'university_invites',
    'student_affiliations', 'cohorts', 'cohort_memberships', 'internship_programs',
    'campus_job_distributions', 'partnerships', 'candidate_referrals', 'university_report_runs',
    'jobs', 'job_revisions', 'job_skill_requirements', 'candidate_search_documents',
    'candidate_invitations', 'talent_lists', 'talent_list_items', 'applications',
    'evidence_export_requests', 'application_notes', 'interviews', 'interview_participants',
    'conversations', 'conversation_read_cursors', 'websocket_connection_leases',
    'ai_model_versions', 'ai_jobs', 'ai_kill_switches', 'products', 'orders',
    'payment_attempts', 'refunds', 'entitlements', 'promotion_campaigns',
    'sponsored_placements', 'notification_preferences', 'notifications', 'moderation_reports',
    'idempotency_keys', 'tenant_roles', 'tenant_permissions', 'internship_program_participants',
    'job_screening_questions', 'file_upload_sessions'
  ]
  LOOP
    EXECUTE format(
      'CREATE TRIGGER a_touch_entity BEFORE UPDATE ON public.%I FOR EACH ROW EXECUTE FUNCTION app_private.touch_entity()',
      table_name
    );
  END LOOP;
END;
$$;

DO $$
DECLARE
  table_name text;
BEGIN
  FOREACH table_name IN ARRAY ARRAY[
    'malware_scan_results', 'job_review_decisions', 'job_status_history',
    'application_status_history', 'interview_status_history', 'ai_human_reviews',
    'payment_webhook_events', 'payment_reconciliations', 'chargebacks',
    'credit_ledger_entries', 'notification_deliveries', 'audit_events',
    'admin_adjustments', 'application_evidence_state_events', 'outbox_delivery_attempts',
    'application_offer_state_events', 'interview_feedback'
  ]
  LOOP
    EXECUTE format(
      'CREATE TRIGGER append_only BEFORE UPDATE OR DELETE ON public.%I FOR EACH ROW EXECUTE FUNCTION app_private.reject_append_mutation()',
      table_name
    );
  END LOOP;
END;
$$;

CREATE TRIGGER cv_versions_draft_only
  BEFORE UPDATE ON cv_versions FOR EACH ROW EXECUTE FUNCTION app_private.cv_version_draft_only();
CREATE TRIGGER job_revisions_draft_only
  BEFORE UPDATE ON job_revisions FOR EACH ROW EXECUTE FUNCTION app_private.job_revision_draft_only();
CREATE TRIGGER conversation_read_cursors_monotonic
  BEFORE UPDATE ON conversation_read_cursors FOR EACH ROW EXECUTE FUNCTION app_private.prevent_cursor_regression();
CREATE TRIGGER payment_attempts_amount_matches_order
  BEFORE INSERT OR UPDATE OF order_id, amount_vnd ON payment_attempts
  FOR EACH ROW EXECUTE FUNCTION app_private.require_payment_attempt_amount();
CREATE TRIGGER entitlements_require_settled_order
  BEFORE INSERT ON entitlements FOR EACH ROW EXECUTE FUNCTION app_private.require_settled_order_item();
CREATE TRIGGER applications_require_published_revision
  BEFORE INSERT OR UPDATE ON applications
  FOR EACH ROW EXECUTE FUNCTION app_private.require_published_application_revision();
CREATE TRIGGER payment_attempts_require_verified_settlement
  BEFORE INSERT OR UPDATE OF status ON payment_attempts
  FOR EACH ROW EXECUTE FUNCTION app_private.require_verified_payment_settlement();
CREATE TRIGGER orders_require_settled_payment
  BEFORE INSERT OR UPDATE OF status ON orders
  FOR EACH ROW EXECUTE FUNCTION app_private.require_settled_payment_for_order();
CREATE TRIGGER refunds_total_within_payment
  BEFORE INSERT OR UPDATE OF status, amount_vnd, payment_attempt_id ON refunds
  FOR EACH ROW EXECUTE FUNCTION app_private.validate_settled_refund_total();

CREATE CONSTRAINT TRIGGER enterprise_memberships_owner_continuity
  AFTER INSERT OR UPDATE OR DELETE ON enterprise_memberships
  DEFERRABLE INITIALLY DEFERRED
  FOR EACH ROW EXECUTE FUNCTION app_private.ensure_active_owner();
CREATE CONSTRAINT TRIGGER university_memberships_owner_continuity
  AFTER INSERT OR UPDATE OR DELETE ON university_memberships
  DEFERRABLE INITIALLY DEFERRED
  FOR EACH ROW EXECUTE FUNCTION app_private.ensure_active_owner();

CREATE TRIGGER immutable_saved_jobs
  BEFORE UPDATE OR DELETE ON saved_jobs FOR EACH ROW
  EXECUTE FUNCTION app_private.immutable_columns_only('removed_at');
CREATE TRIGGER immutable_trusted_publisher_grants
  BEFORE UPDATE OR DELETE ON trusted_publisher_grants FOR EACH ROW
  EXECUTE FUNCTION app_private.immutable_columns_only('revoked_at', 'revoked_by_subject_id', 'revoke_reason');
CREATE TRIGGER immutable_data_consent_grants
  BEFORE UPDATE OR DELETE ON data_consent_grants FOR EACH ROW
  EXECUTE FUNCTION app_private.immutable_columns_only('withdrawn_at', 'withdrawal_reason');
CREATE TRIGGER immutable_application_snapshots
  BEFORE UPDATE OR DELETE ON application_snapshots FOR EACH ROW
  EXECUTE FUNCTION app_private.immutable_columns_only();
CREATE TRIGGER immutable_application_evidence_selections
  BEFORE UPDATE OR DELETE ON application_evidence_selections FOR EACH ROW
  EXECUTE FUNCTION app_private.immutable_columns_only();
CREATE TRIGGER immutable_application_evidence_snapshots
  BEFORE UPDATE OR DELETE ON application_evidence_snapshots FOR EACH ROW
  EXECUTE FUNCTION app_private.immutable_columns_only();
CREATE TRIGGER immutable_application_assignments
  BEFORE UPDATE OR DELETE ON application_assignments FOR EACH ROW
  EXECUTE FUNCTION app_private.immutable_columns_only('unassigned_at', 'unassigned_by_subject_id', 'reason');
CREATE TRIGGER immutable_interview_schedule_versions
  BEFORE UPDATE OR DELETE ON interview_schedule_versions FOR EACH ROW
  EXECUTE FUNCTION app_private.immutable_columns_only();
CREATE TRIGGER immutable_messages
  BEFORE UPDATE OR DELETE ON messages FOR EACH ROW
  EXECUTE FUNCTION app_private.immutable_columns_only('deleted_for_all_at');
CREATE TRIGGER immutable_ai_prompt_versions
  BEFORE UPDATE OR DELETE ON ai_prompt_versions FOR EACH ROW
  EXECUTE FUNCTION app_private.immutable_columns_only('activated_at', 'retired_at');
CREATE TRIGGER immutable_ai_policy_versions
  BEFORE UPDATE OR DELETE ON ai_policy_versions FOR EACH ROW
  EXECUTE FUNCTION app_private.immutable_columns_only('retired_at');
CREATE TRIGGER immutable_ai_outputs
  BEFORE UPDATE OR DELETE ON ai_outputs FOR EACH ROW
  EXECUTE FUNCTION app_private.immutable_columns_only();
CREATE TRIGGER immutable_match_score_snapshots
  BEFORE UPDATE OR DELETE ON match_score_snapshots FOR EACH ROW
  EXECUTE FUNCTION app_private.immutable_columns_only();
CREATE TRIGGER immutable_product_prices
  BEFORE UPDATE OR DELETE ON product_prices FOR EACH ROW
  EXECUTE FUNCTION app_private.immutable_columns_only();
CREATE TRIGGER immutable_order_items
  BEFORE UPDATE OR DELETE ON order_items FOR EACH ROW
  EXECUTE FUNCTION app_private.immutable_columns_only();
CREATE TRIGGER immutable_invoices
  BEFORE UPDATE OR DELETE ON invoices FOR EACH ROW
  EXECUTE FUNCTION app_private.immutable_columns_only('voided_at', 'void_reason', 'replacement_invoice_id');
CREATE TRIGGER immutable_outbox_events
  BEFORE UPDATE OR DELETE ON outbox_events FOR EACH ROW
  EXECUTE FUNCTION app_private.immutable_columns_only();
CREATE TRIGGER immutable_consumer_inbox
  BEFORE UPDATE OR DELETE ON consumer_inbox FOR EACH ROW
  EXECUTE FUNCTION app_private.immutable_columns_only('processed_at', 'result_code');
CREATE TRIGGER immutable_tenant_role_permissions
  BEFORE UPDATE OR DELETE ON tenant_role_permissions FOR EACH ROW
  EXECUTE FUNCTION app_private.immutable_columns_only('revoked_at', 'revoked_by_subject_id');
CREATE TRIGGER immutable_application_offer_versions
  BEFORE UPDATE OR DELETE ON application_offer_versions FOR EACH ROW
  EXECUTE FUNCTION app_private.immutable_columns_only();

CREATE TRIGGER candidate_profiles_avatar_must_be_clean
  BEFORE INSERT OR UPDATE OF avatar_file_id ON candidate_profiles
  FOR EACH ROW EXECUTE FUNCTION app_private.require_clean_file('avatar_file_id');
CREATE TRIGGER cv_versions_rendered_must_be_clean
  BEFORE INSERT OR UPDATE OF rendered_file_id ON cv_versions
  FOR EACH ROW EXECUTE FUNCTION app_private.require_clean_file('rendered_file_id');
CREATE TRIGGER portfolio_items_file_must_be_clean
  BEFORE INSERT OR UPDATE OF file_id ON portfolio_items
  FOR EACH ROW EXECUTE FUNCTION app_private.require_clean_file('file_id');
CREATE TRIGGER enterprise_tenants_logo_must_be_clean
  BEFORE INSERT OR UPDATE OF logo_file_id ON enterprise_tenants
  FOR EACH ROW EXECUTE FUNCTION app_private.require_clean_file('logo_file_id');
CREATE TRIGGER university_tenants_logo_must_be_clean
  BEFORE INSERT OR UPDATE OF logo_file_id ON university_tenants
  FOR EACH ROW EXECUTE FUNCTION app_private.require_clean_file('logo_file_id');
CREATE TRIGGER invoices_file_must_be_clean
  BEFORE INSERT OR UPDATE OF file_id ON invoices
  FOR EACH ROW EXECUTE FUNCTION app_private.require_clean_file('file_id');

-- RLS context helpers.  The service sets these transaction-locally only after
-- verifying JWT/membership: SET LOCAL app.subject_id = '...'; SET LOCAL
-- app.tenant_id = '...'.  Worker jobs must also set app.tenant_id.
CREATE FUNCTION app_private.context_uuid(setting_name text)
RETURNS uuid
LANGUAGE plpgsql
STABLE
SET search_path = pg_catalog
AS $$
DECLARE
  setting_value text;
BEGIN
  setting_value := current_setting(setting_name, true);
  IF setting_value IS NULL OR setting_value = '' THEN
    RETURN NULL;
  END IF;
  RETURN setting_value::uuid;
EXCEPTION WHEN invalid_text_representation THEN
  RAISE EXCEPTION '% must contain a UUID', setting_name USING ERRCODE = '22023';
END;
$$;

CREATE FUNCTION app_private.current_subject_id()
RETURNS uuid
LANGUAGE sql
STABLE
SET search_path = pg_catalog
AS $$
  SELECT app_private.context_uuid('app.subject_id');
$$;

CREATE FUNCTION app_private.current_tenant_id()
RETURNS uuid
LANGUAGE sql
STABLE
SET search_path = pg_catalog
AS $$
  SELECT app_private.context_uuid('app.tenant_id');
$$;

CREATE FUNCTION app_private.is_worker()
RETURNS boolean
LANGUAGE sql
STABLE
SET search_path = pg_catalog
AS $$
  SELECT pg_has_role(session_user, 's2w_work_worker', 'member');
$$;

CREATE FUNCTION app_private.is_service()
RETURNS boolean
LANGUAGE sql
STABLE
SET search_path = pg_catalog
AS $$
  SELECT pg_has_role(session_user, 's2w_work_app', 'member')
      OR pg_has_role(session_user, 's2w_work_worker', 'member');
$$;

CREATE FUNCTION app_private.has_active_tenant_access(check_tenant_id uuid)
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
  SELECT app_private.is_worker()
      OR EXISTS (
        SELECT 1
        FROM public.enterprise_memberships m
        WHERE m.tenant_id = check_tenant_id
          AND m.identity_subject_id = app_private.current_subject_id()
          AND m.status = 'ACTIVE'
          AND (m.valid_until IS NULL OR m.valid_until > now())
      )
      OR EXISTS (
        SELECT 1
        FROM public.university_memberships m
        WHERE m.tenant_id = check_tenant_id
          AND m.identity_subject_id = app_private.current_subject_id()
          AND m.status = 'ACTIVE'
          AND (m.valid_until IS NULL OR m.valid_until > now())
      );
$$;

CREATE FUNCTION app_private.tenant_scope(row_tenant_id uuid)
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
  SELECT row_tenant_id IS NOT NULL
     AND row_tenant_id = app_private.current_tenant_id()
     AND app_private.has_active_tenant_access(row_tenant_id);
$$;

CREATE FUNCTION app_private.owns_candidate(check_candidate_id uuid)
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
  SELECT EXISTS (
    SELECT 1
    FROM public.candidate_profiles c
    WHERE c.id = check_candidate_id
      AND c.identity_subject_id = app_private.current_subject_id()
      AND c.deleted_at IS NULL
  );
$$;

CREATE FUNCTION app_private.owns_cv(check_cv_id uuid)
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
  SELECT EXISTS (
    SELECT 1
    FROM public.cvs cv
    JOIN public.candidate_profiles c ON c.id = cv.candidate_id
    WHERE cv.id = check_cv_id
      AND c.identity_subject_id = app_private.current_subject_id()
      AND c.deleted_at IS NULL
  );
$$;

CREATE FUNCTION app_private.application_scope(row_tenant_id uuid, check_application_id uuid)
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
  SELECT app_private.tenant_scope(row_tenant_id)
      OR EXISTS (
        SELECT 1
        FROM public.applications a
        JOIN public.candidate_profiles c ON c.id = a.candidate_id
        WHERE a.id = check_application_id
          AND a.tenant_id = row_tenant_id
          AND c.identity_subject_id = app_private.current_subject_id()
          AND c.deleted_at IS NULL
      );
$$;

CREATE FUNCTION app_private.interview_scope(row_tenant_id uuid, check_interview_id uuid)
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
  SELECT app_private.tenant_scope(row_tenant_id)
      OR EXISTS (
        SELECT 1
        FROM public.interviews i
        JOIN public.applications a ON a.id = i.application_id
        JOIN public.candidate_profiles c ON c.id = a.candidate_id
        WHERE i.id = check_interview_id
          AND i.tenant_id = row_tenant_id
          AND c.identity_subject_id = app_private.current_subject_id()
          AND c.deleted_at IS NULL
      );
$$;

CREATE FUNCTION app_private.conversation_scope(row_tenant_id uuid, check_conversation_id uuid)
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
  SELECT app_private.tenant_scope(row_tenant_id)
      OR EXISTS (
        SELECT 1
        FROM public.conversations c
        WHERE c.id = check_conversation_id
          AND c.tenant_id = row_tenant_id
          AND c.candidate_subject_id = app_private.current_subject_id()
      );
$$;

CREATE FUNCTION app_private.subject_or_tenant_scope(row_subject_id uuid, row_tenant_id uuid)
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
  SELECT row_subject_id = app_private.current_subject_id()
      OR app_private.tenant_scope(row_tenant_id);
$$;

CREATE FUNCTION app_private.candidate_or_tenant_scope(
  check_candidate_id uuid,
  row_tenant_id uuid
)
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
  SELECT app_private.owns_candidate(check_candidate_id)
      OR app_private.tenant_scope(row_tenant_id);
$$;

CREATE FUNCTION app_private.search_document_scope(
  check_candidate_id uuid,
  check_visibility candidate_visibility
)
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
  SELECT app_private.owns_candidate(check_candidate_id)
      OR (
        check_visibility = 'SEARCHABLE'
        AND app_private.current_tenant_id() IS NOT NULL
        AND app_private.has_active_tenant_access(app_private.current_tenant_id())
      );
$$;

CREATE FUNCTION app_private.grantee_or_candidate_scope(
  check_candidate_id uuid,
  check_grantee_tenant_id uuid
)
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
  SELECT app_private.owns_candidate(check_candidate_id)
      OR app_private.tenant_scope(check_grantee_tenant_id);
$$;

ALTER TABLE identity_projections ENABLE ROW LEVEL SECURITY;
CREATE POLICY identity_projection_subject_scope ON identity_projections
  FOR ALL
  USING (identity_subject_id = app_private.current_subject_id())
  WITH CHECK (identity_subject_id = app_private.current_subject_id());

ALTER TABLE candidate_profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY candidate_profile_subject_scope ON candidate_profiles
  FOR ALL
  USING (identity_subject_id = app_private.current_subject_id())
  WITH CHECK (identity_subject_id = app_private.current_subject_id());

DO $$
DECLARE
  table_name text;
BEGIN
  FOREACH table_name IN ARRAY ARRAY[
    'candidate_search_preferences', 'candidate_skills', 'candidate_experiences',
    'candidate_educations', 'cvs', 'portfolio_items', 'saved_jobs'
  ]
  LOOP
    EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', table_name);
    EXECUTE format(
      'CREATE POLICY candidate_owner_scope ON public.%I FOR ALL USING (app_private.owns_candidate(candidate_id)) WITH CHECK (app_private.owns_candidate(candidate_id))',
      table_name
    );
  END LOOP;
END;
$$;

ALTER TABLE cv_versions ENABLE ROW LEVEL SECURITY;
CREATE POLICY cv_versions_candidate_scope ON cv_versions
  FOR ALL
  USING (app_private.owns_cv(cv_id))
  WITH CHECK (app_private.owns_cv(cv_id));

ALTER TABLE candidate_search_documents ENABLE ROW LEVEL SECURITY;
CREATE POLICY candidate_search_document_scope ON candidate_search_documents
  FOR ALL
  USING (app_private.search_document_scope(candidate_id, visibility))
  WITH CHECK (app_private.owns_candidate(candidate_id));

ALTER TABLE file_objects ENABLE ROW LEVEL SECURITY;
CREATE POLICY file_objects_subject_or_tenant_scope ON file_objects
  FOR ALL
  USING (app_private.subject_or_tenant_scope(owner_subject_id, tenant_id))
  WITH CHECK (app_private.subject_or_tenant_scope(owner_subject_id, tenant_id));

ALTER TABLE file_upload_sessions ENABLE ROW LEVEL SECURITY;
CREATE POLICY file_upload_sessions_subject_or_tenant_scope ON file_upload_sessions
  FOR ALL
  USING (app_private.subject_or_tenant_scope(owner_subject_id, tenant_id))
  WITH CHECK (app_private.subject_or_tenant_scope(owner_subject_id, tenant_id));

ALTER TABLE websocket_connection_leases ENABLE ROW LEVEL SECURITY;
CREATE POLICY websocket_connection_leases_subject_scope ON websocket_connection_leases
  FOR ALL
  USING (identity_subject_id = app_private.current_subject_id())
  WITH CHECK (identity_subject_id = app_private.current_subject_id());

ALTER TABLE data_consent_grants ENABLE ROW LEVEL SECURITY;
CREATE POLICY data_consent_grants_scope ON data_consent_grants
  FOR ALL
  USING (app_private.grantee_or_candidate_scope(candidate_id, grantee_tenant_id))
  WITH CHECK (app_private.owns_candidate(candidate_id));

ALTER TABLE enterprise_tenants ENABLE ROW LEVEL SECURITY;
CREATE POLICY enterprise_tenant_scope ON enterprise_tenants
  FOR ALL
  USING (app_private.tenant_scope(id))
  WITH CHECK (app_private.tenant_scope(id) OR app_private.is_service());
ALTER TABLE university_tenants ENABLE ROW LEVEL SECURITY;
CREATE POLICY university_tenant_scope ON university_tenants
  FOR ALL
  USING (app_private.tenant_scope(id))
  WITH CHECK (app_private.tenant_scope(id) OR app_private.is_service());

ALTER TABLE enterprise_memberships ENABLE ROW LEVEL SECURITY;
CREATE POLICY enterprise_memberships_scope ON enterprise_memberships
  FOR ALL
  USING (app_private.tenant_scope(tenant_id))
  WITH CHECK (
    app_private.tenant_scope(tenant_id)
    OR (
      app_private.is_service()
      AND role_code = 'OWNER'
      AND identity_subject_id = app_private.current_subject_id()
      AND status = 'ACTIVE'
    )
  );
ALTER TABLE university_memberships ENABLE ROW LEVEL SECURITY;
CREATE POLICY university_memberships_scope ON university_memberships
  FOR ALL
  USING (app_private.tenant_scope(tenant_id))
  WITH CHECK (
    app_private.tenant_scope(tenant_id)
    OR (
      app_private.is_service()
      AND role_code = 'OWNER'
      AND identity_subject_id = app_private.current_subject_id()
      AND status = 'ACTIVE'
    )
  );

DO $$
DECLARE
  table_name text;
BEGIN
  FOREACH table_name IN ARRAY ARRAY[
    'enterprise_verification_cases', 'enterprise_invites',
    'university_verification_cases', 'university_invites',
    'cohorts', 'cohort_memberships', 'internship_programs', 'campus_job_distributions',
    'partnerships', 'university_report_runs', 'jobs', 'job_revisions',
    'job_skill_requirements', 'job_review_decisions', 'job_status_history',
    'trusted_publisher_grants', 'talent_lists', 'talent_list_items', 'application_evidence_state_events',
    'internship_program_participants', 'job_screening_questions'
  ]
  LOOP
    EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', table_name);
    EXECUTE format(
      'CREATE POLICY tenant_context_scope ON public.%I FOR ALL USING (app_private.tenant_scope(tenant_id)) WITH CHECK (app_private.tenant_scope(tenant_id))',
      table_name
    );
  END LOOP;
END;
$$;

ALTER TABLE student_affiliations ENABLE ROW LEVEL SECURITY;
CREATE POLICY student_affiliations_scope ON student_affiliations
  FOR ALL
  USING (app_private.candidate_or_tenant_scope(candidate_id, tenant_id))
  WITH CHECK (app_private.candidate_or_tenant_scope(candidate_id, tenant_id));
ALTER TABLE candidate_referrals ENABLE ROW LEVEL SECURITY;
CREATE POLICY candidate_referrals_scope ON candidate_referrals
  FOR ALL
  USING (app_private.candidate_or_tenant_scope(candidate_id, tenant_id))
  WITH CHECK (app_private.tenant_scope(tenant_id));
ALTER TABLE candidate_invitations ENABLE ROW LEVEL SECURITY;
CREATE POLICY candidate_invitations_scope ON candidate_invitations
  FOR ALL
  USING (app_private.candidate_or_tenant_scope(candidate_id, tenant_id))
  WITH CHECK (app_private.tenant_scope(tenant_id));

ALTER TABLE applications ENABLE ROW LEVEL SECURITY;
CREATE POLICY applications_scope ON applications
  FOR ALL
  USING (app_private.application_scope(tenant_id, id))
  WITH CHECK (app_private.application_scope(tenant_id, id));

DO $$
DECLARE
  table_name text;
BEGIN
  FOREACH table_name IN ARRAY ARRAY[
    'application_snapshots', 'application_evidence_selections', 'evidence_export_requests',
    'application_evidence_snapshots', 'application_status_history', 'application_assignments',
    'application_notes', 'application_offer_versions', 'application_offer_state_events'
  ]
  LOOP
    EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', table_name);
    EXECUTE format(
      'CREATE POLICY application_context_scope ON public.%I FOR ALL USING (app_private.application_scope(tenant_id, application_id)) WITH CHECK (app_private.application_scope(tenant_id, application_id))',
      table_name
    );
  END LOOP;
END;
$$;

ALTER TABLE interviews ENABLE ROW LEVEL SECURITY;
CREATE POLICY interviews_scope ON interviews
  FOR ALL
  USING (app_private.application_scope(tenant_id, application_id))
  WITH CHECK (app_private.application_scope(tenant_id, application_id));

DO $$
DECLARE
  table_name text;
BEGIN
  FOREACH table_name IN ARRAY ARRAY[
    'interview_schedule_versions', 'interview_participants', 'interview_status_history',
    'interview_feedback'
  ]
  LOOP
    EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', table_name);
    EXECUTE format(
      'CREATE POLICY interview_context_scope ON public.%I FOR ALL USING (app_private.interview_scope(tenant_id, interview_id)) WITH CHECK (app_private.interview_scope(tenant_id, interview_id))',
      table_name
    );
  END LOOP;
END;
$$;

ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
CREATE POLICY conversations_scope ON conversations
  FOR ALL
  USING (app_private.conversation_scope(tenant_id, id))
  WITH CHECK (app_private.conversation_scope(tenant_id, id));
DO $$
DECLARE
  table_name text;
BEGIN
  FOREACH table_name IN ARRAY ARRAY['messages', 'conversation_read_cursors']
  LOOP
    EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', table_name);
    EXECUTE format(
      'CREATE POLICY conversation_context_scope ON public.%I FOR ALL USING (app_private.conversation_scope(tenant_id, conversation_id)) WITH CHECK (app_private.conversation_scope(tenant_id, conversation_id))',
      table_name
    );
  END LOOP;
END;
$$;

ALTER TABLE ai_jobs ENABLE ROW LEVEL SECURITY;
CREATE POLICY ai_jobs_scope ON ai_jobs
  FOR ALL
  USING (app_private.subject_or_tenant_scope(actor_subject_id, tenant_id))
  WITH CHECK (app_private.subject_or_tenant_scope(actor_subject_id, tenant_id));
ALTER TABLE match_score_snapshots ENABLE ROW LEVEL SECURITY;
CREATE POLICY match_score_snapshots_scope ON match_score_snapshots
  FOR ALL
  USING (app_private.candidate_or_tenant_scope(candidate_id, tenant_id))
  WITH CHECK (app_private.tenant_scope(tenant_id));

ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY orders_scope ON orders
  FOR ALL
  USING (app_private.subject_or_tenant_scope(buyer_subject_id, tenant_id))
  WITH CHECK (app_private.subject_or_tenant_scope(buyer_subject_id, tenant_id));
ALTER TABLE entitlements ENABLE ROW LEVEL SECURITY;
CREATE POLICY entitlements_scope ON entitlements
  FOR ALL
  USING (app_private.subject_or_tenant_scope(owner_subject_id, tenant_id))
  WITH CHECK (app_private.subject_or_tenant_scope(owner_subject_id, tenant_id));
ALTER TABLE credit_ledger_entries ENABLE ROW LEVEL SECURITY;
CREATE POLICY credit_ledger_entries_scope ON credit_ledger_entries
  FOR ALL
  USING (app_private.subject_or_tenant_scope(owner_subject_id, tenant_id))
  WITH CHECK (app_private.subject_or_tenant_scope(owner_subject_id, tenant_id));
ALTER TABLE promotion_campaigns ENABLE ROW LEVEL SECURITY;
CREATE POLICY promotion_campaigns_scope ON promotion_campaigns
  FOR ALL
  USING (app_private.subject_or_tenant_scope(sponsor_subject_id, sponsor_tenant_id))
  WITH CHECK (app_private.subject_or_tenant_scope(sponsor_subject_id, sponsor_tenant_id));

ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
CREATE POLICY notifications_scope ON notifications
  FOR ALL
  USING (app_private.subject_or_tenant_scope(identity_subject_id, tenant_id))
  WITH CHECK (app_private.subject_or_tenant_scope(identity_subject_id, tenant_id));
ALTER TABLE moderation_reports ENABLE ROW LEVEL SECURITY;
CREATE POLICY moderation_reports_scope ON moderation_reports
  FOR ALL
  USING (app_private.subject_or_tenant_scope(reporter_subject_id, tenant_id))
  WITH CHECK (app_private.subject_or_tenant_scope(reporter_subject_id, tenant_id));
ALTER TABLE admin_adjustments ENABLE ROW LEVEL SECURITY;
CREATE POLICY admin_adjustments_scope ON admin_adjustments
  FOR ALL
  USING (app_private.tenant_scope(tenant_id))
  WITH CHECK (app_private.tenant_scope(tenant_id));

DO $$
DECLARE
  table_name text;
BEGIN
  FOREACH table_name IN ARRAY ARRAY[
    'malware_scan_results', 'ai_model_versions', 'ai_prompt_versions', 'ai_policy_versions',
    'ai_outputs', 'ai_human_reviews', 'ai_kill_switches', 'products', 'product_prices',
    'order_items', 'payment_attempts', 'payment_webhook_events', 'payment_reconciliations',
    'refunds', 'chargebacks', 'sponsored_placements', 'invoices', 'notification_preferences',
    'notification_deliveries', 'audit_events', 'idempotency_keys', 'outbox_events',
    'consumer_inbox', 'tenant_roles', 'tenant_permissions', 'tenant_role_permissions',
    'outbox_delivery_attempts'
  ]
  LOOP
    EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', table_name);
    EXECUTE format(
      'CREATE POLICY service_only_scope ON public.%I FOR ALL USING (app_private.is_service()) WITH CHECK (app_private.is_service())',
      table_name
    );
  END LOOP;
END;
$$;

REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO s2w_work_app, s2w_work_worker, s2w_work_readonly;
GRANT USAGE ON SCHEMA app_private TO s2w_work_app, s2w_work_worker, s2w_work_readonly;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO s2w_work_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO s2w_work_worker;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO s2w_work_readonly;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA app_private
  TO s2w_work_app, s2w_work_worker, s2w_work_readonly;
ALTER DEFAULT PRIVILEGES FOR ROLE s2w_work_owner IN SCHEMA public
  REVOKE ALL ON TABLES FROM PUBLIC;
ALTER DEFAULT PRIVILEGES FOR ROLE s2w_work_owner IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO s2w_work_app, s2w_work_worker;
ALTER DEFAULT PRIVILEGES FOR ROLE s2w_work_owner IN SCHEMA public
  GRANT SELECT ON TABLES TO s2w_work_readonly;
ALTER DEFAULT PRIVILEGES FOR ROLE s2w_work_owner IN SCHEMA app_private
  REVOKE ALL ON FUNCTIONS FROM PUBLIC;
ALTER DEFAULT PRIVILEGES FOR ROLE s2w_work_owner IN SCHEMA app_private
  GRANT EXECUTE ON FUNCTIONS TO s2w_work_app, s2w_work_worker, s2w_work_readonly;

RESET ROLE;
COMMIT;
