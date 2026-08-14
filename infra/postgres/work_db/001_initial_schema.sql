-- Study2Work V1-PILOT: work_db initial schema (PostgreSQL 16)
-- Source of truth: docs/BD/03_THIET_KE_CO_SO_DU_LIEU.md, sections 1--14.
-- This script intentionally creates no database, LOGIN role, seed data, or
-- cross-database foreign key.  Execute it against an empty work_db as a
-- principal permitted to create roles, extensions, schemas, and objects.

BEGIN;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 's2w_work_owner') THEN
    CREATE ROLE s2w_work_owner NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 's2w_work_app') THEN
    CREATE ROLE s2w_work_app NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 's2w_work_worker') THEN
    CREATE ROLE s2w_work_worker NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 's2w_work_readonly') THEN
    CREATE ROLE s2w_work_readonly NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION;
  END IF;
END
$$;

GRANT s2w_work_owner TO CURRENT_USER;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS btree_gist;
REVOKE ALL ON DATABASE work_db FROM PUBLIC;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
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
  old_document jsonb := to_jsonb(OLD);
  new_document jsonb := to_jsonb(NEW);
BEGIN
  IF TG_OP = 'DELETE' THEN
    RAISE EXCEPTION '% is immutable and cannot be deleted', TG_TABLE_NAME USING ERRCODE = '55000';
  END IF;
  FOR changed_column IN
    SELECT n.key
    FROM jsonb_each(new_document) AS n
    WHERE (old_document -> n.key) IS DISTINCT FROM n.value
  LOOP
    IF changed_column <> ALL (TG_ARGV) THEN
      RAISE EXCEPTION '% column % is immutable', TG_TABLE_NAME, changed_column USING ERRCODE = '55000';
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
  CHECK ((revoked_at IS NULL AND revoked_by_subject_id IS NULL) OR revoked_at IS NOT NULL)
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
  CHECK (valid_until > valid_from)
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
