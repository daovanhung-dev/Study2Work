-- Study2Work V1-PILOT / study_db
-- PostgreSQL 16 initial schema. Run only against an empty, provisioned study_db.
-- Source: docs/BD/03_THIET_KE_CO_SO_DU_LIEU.md, sections 1--5 and 7--14.
--
-- Deliberately excluded source gaps: authVersion, MFA pending enrollment,
-- onboarding draft, candidate-search consent history, public job slug,
-- payment entitlement reservation/refund, promotion metrics, and AI
-- evaluation/kill-switch. This script creates only TBL-STU-001..060.

BEGIN;

DO $$
BEGIN
  IF current_database() <> 'study_db' THEN
    RAISE EXCEPTION '001_initial_schema.sql must run against study_db, got %', current_database();
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 's2w_study_owner') THEN
    CREATE ROLE s2w_study_owner NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 's2w_study_app') THEN
    CREATE ROLE s2w_study_app NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 's2w_study_worker') THEN
    CREATE ROLE s2w_study_worker NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 's2w_study_readonly') THEN
    CREATE ROLE s2w_study_readonly NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT;
  END IF;
END
$$;

REVOKE ALL ON DATABASE study_db FROM PUBLIC;
GRANT CONNECT ON DATABASE study_db TO s2w_study_owner, s2w_study_app, s2w_study_worker, s2w_study_readonly;
ALTER SCHEMA public OWNER TO s2w_study_owner;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
CREATE SCHEMA IF NOT EXISTS app_private AUTHORIZATION s2w_study_owner;
REVOKE ALL ON SCHEMA app_private FROM PUBLIC;

CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS btree_gist;

GRANT s2w_study_owner TO CURRENT_USER;
SET ROLE s2w_study_owner;
SET search_path = public, app_private;

-- Locally owned enum copies. They are intentionally not shared with the
-- identity_db or work_db clusters.
CREATE TYPE account_status AS ENUM (
  'PENDING_EMAIL_VERIFICATION', 'ACTIVE', 'SUSPENDED', 'DELETION_PENDING', 'ANONYMIZED'
);
CREATE TYPE audit_outcome AS ENUM ('SUCCESS', 'DENIED', 'FAILURE');
CREATE TYPE content_version_status AS ENUM ('DRAFT', 'PUBLISHED', 'SUPERSEDED', 'DISCARDED');
CREATE TYPE primary_path_status AS ENUM ('ACTIVE', 'SWITCHED_OUT', 'COMPLETED', 'CANCELLED_BY_ADMIN');
CREATE TYPE enrollment_status AS ENUM ('ENROLLED', 'IN_PROGRESS', 'COMPLETED');
CREATE TYPE progress_status AS ENUM ('NOT_STARTED', 'IN_PROGRESS', 'COMPLETED');
CREATE TYPE assessment_type AS ENUM ('QUIZ', 'TEXT', 'LINK', 'FILE');
CREATE TYPE attempt_status AS ENUM ('SUBMITTED', 'UNDER_REVIEW', 'PASSED', 'NEEDS_REVISION', 'FAILED');
CREATE TYPE review_decision AS ENUM ('PASSED', 'NEEDS_REVISION', 'FAILED');
CREATE TYPE file_asset_status AS ENUM (
  'CREATED', 'UPLOADING', 'UPLOADED', 'SCANNING', 'CLEAN', 'INFECTED',
  'SCAN_FAILED', 'ATTACHED', 'EXPIRED', 'DELETED'
);
CREATE TYPE evidence_status AS ENUM ('ISSUED', 'REVOKED');
CREATE TYPE notification_status AS ENUM ('QUEUED', 'SENT', 'DELIVERED', 'FAILED', 'SUPPRESSED');
CREATE TYPE outbox_status AS ENUM ('PENDING', 'PUBLISHED', 'FAILED', 'DEAD_LETTER');

CREATE FUNCTION app_private.touch_entity()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  NEW.updated_at := now();
  NEW.row_version := OLD.row_version + 1;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.prevent_append_mutation()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  RAISE EXCEPTION '% is append-only; % is not permitted', TG_TABLE_NAME, TG_OP
    USING ERRCODE = '55000';
END
$$;

CREATE FUNCTION app_private.prevent_delete()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  RAISE EXCEPTION '% records are retained and cannot be deleted', TG_TABLE_NAME
    USING ERRCODE = '55000';
END
$$;

CREATE FUNCTION app_private.current_subject_id()
RETURNS uuid
LANGUAGE sql
STABLE
AS $$
  SELECT NULLIF(current_setting('app.subject_id', true), '')::uuid
$$;

CREATE FUNCTION app_private.current_tenant_id()
RETURNS uuid
LANGUAGE sql
STABLE
AS $$
  SELECT NULLIF(current_setting('app.tenant_id', true), '')::uuid
$$;

CREATE FUNCTION app_private.uuid_array_is_distinct(value uuid[])
RETURNS boolean
LANGUAGE sql
IMMUTABLE
STRICT
AS $$
  SELECT cardinality(value) = (SELECT count(DISTINCT item) FROM unnest(value) AS item)
$$;

CREATE FUNCTION app_private.require_published_path_version()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  version_status content_version_status;
BEGIN
  SELECT status INTO version_status FROM learning_path_versions WHERE id = NEW.path_version_id;
  IF version_status IS DISTINCT FROM 'PUBLISHED' THEN
    RAISE EXCEPTION 'path_version_id must reference a PUBLISHED learning path version'
      USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.require_published_course_version()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  version_status content_version_status;
BEGIN
  SELECT status INTO version_status FROM course_versions WHERE id = NEW.course_version_id;
  IF version_status IS DISTINCT FROM 'PUBLISHED' THEN
    RAISE EXCEPTION 'course_version_id must reference a PUBLISHED course version'
      USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.guard_content_version()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF OLD.status <> 'DRAFT' AND NEW IS DISTINCT FROM OLD THEN
    RAISE EXCEPTION '% version % is immutable after it leaves DRAFT', TG_TABLE_NAME, OLD.id
      USING ERRCODE = '55000';
  END IF;
  IF NEW.status = 'PUBLISHED' AND NEW.published_at IS NULL THEN
    RAISE EXCEPTION 'PUBLISHED content version requires published_at'
      USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.guard_sealed_assessment_draft()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF OLD.state = 'SEALED' AND NEW IS DISTINCT FROM OLD THEN
    RAISE EXCEPTION 'SEALED assessment draft % is immutable', OLD.id USING ERRCODE = '55000';
  END IF;
  IF NEW.state = 'SEALED' AND (NEW.sealed_at IS NULL OR NEW.sealed_attempt_id IS NULL) THEN
    RAISE EXCEPTION 'SEALED assessment draft requires sealed_at and sealed_attempt_id'
      USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END
$$;

-- TBL-STU-001 .. TBL-STU-008
CREATE TABLE identity_projections (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  identity_subject_id uuid NOT NULL UNIQUE,
  account_status account_status NOT NULL,
  email_verified boolean NOT NULL DEFAULT false,
  display_name varchar(120),
  identity_version bigint NOT NULL,
  last_event_id uuid NOT NULL UNIQUE,
  projected_at timestamptz NOT NULL,
  CONSTRAINT ck_identity_projections_identity_version CHECK (identity_version >= 1)
);

CREATE TABLE learner_profiles (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  identity_subject_id uuid NOT NULL UNIQUE,
  full_name varchar(160),
  avatar_file_id uuid,
  headline varchar(200),
  bio varchar(2000),
  birth_year smallint,
  city_code varchar(20),
  onboarding_completed_at timestamptz,
  profile_visibility varchar(20) NOT NULL DEFAULT 'PRIVATE',
  deleted_at timestamptz,
  CONSTRAINT ck_learner_profiles_birth_year
    CHECK (birth_year IS NULL OR birth_year BETWEEN 1900 AND (extract(year FROM current_date)::smallint - 13)),
  CONSTRAINT ck_learner_profiles_visibility CHECK (profile_visibility IN ('PRIVATE', 'PLATFORM'))
);

CREATE TABLE service_roles (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  code varchar(80) NOT NULL UNIQUE,
  name varchar(120) NOT NULL,
  description varchar(500) NOT NULL,
  is_privileged boolean NOT NULL DEFAULT false,
  disabled_at timestamptz,
  CONSTRAINT ck_service_roles_code CHECK (code = upper(code) AND code ~ '^[A-Z0-9_]+$')
);

CREATE TABLE service_permissions (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  code varchar(120) NOT NULL UNIQUE,
  description varchar(500) NOT NULL,
  risk_level smallint NOT NULL DEFAULT 1,
  CONSTRAINT ck_service_permissions_risk_level CHECK (risk_level BETWEEN 1 AND 5)
);

CREATE TABLE service_role_permissions (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  role_id uuid NOT NULL REFERENCES service_roles(id) ON DELETE RESTRICT,
  permission_id uuid NOT NULL REFERENCES service_permissions(id) ON DELETE RESTRICT,
  granted_by_subject_id uuid NOT NULL,
  revoked_at timestamptz,
  revoked_by_subject_id uuid,
  CONSTRAINT ck_service_role_permissions_revoker CHECK (
    (revoked_at IS NULL AND revoked_by_subject_id IS NULL)
    OR (revoked_at IS NOT NULL AND revoked_by_subject_id IS NOT NULL)
  )
);

CREATE TABLE service_role_assignments (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  identity_subject_id uuid NOT NULL,
  role_id uuid NOT NULL REFERENCES service_roles(id) ON DELETE RESTRICT,
  valid_from timestamptz NOT NULL DEFAULT now(),
  valid_until timestamptz,
  granted_by_subject_id uuid NOT NULL,
  reason varchar(500) NOT NULL,
  revoked_at timestamptz,
  revoked_by_subject_id uuid,
  CONSTRAINT ck_service_role_assignments_validity CHECK (valid_until IS NULL OR valid_until > valid_from),
  CONSTRAINT ck_service_role_assignments_revoker CHECK (
    (revoked_at IS NULL AND revoked_by_subject_id IS NULL)
    OR (revoked_at IS NOT NULL AND revoked_by_subject_id IS NOT NULL)
  )
);

CREATE TABLE onboarding_submissions (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  learner_id uuid NOT NULL REFERENCES learner_profiles(id) ON DELETE RESTRICT,
  schema_version integer NOT NULL,
  answers jsonb NOT NULL,
  submitted_at timestamptz NOT NULL,
  supersedes_id uuid REFERENCES onboarding_submissions(id) ON DELETE RESTRICT,
  is_current boolean NOT NULL DEFAULT true,
  CONSTRAINT ck_onboarding_submissions_schema_version CHECK (schema_version >= 1)
);

CREATE TABLE path_recommendation_runs (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  learner_id uuid NOT NULL REFERENCES learner_profiles(id) ON DELETE RESTRICT,
  onboarding_submission_id uuid NOT NULL REFERENCES onboarding_submissions(id) ON DELETE RESTRICT,
  algorithm_version varchar(40) NOT NULL,
  input_snapshot jsonb NOT NULL,
  ranked_path_version_ids uuid[] NOT NULL,
  reason_snapshot jsonb NOT NULL,
  generated_at timestamptz NOT NULL,
  expires_at timestamptz NOT NULL,
  CONSTRAINT ck_path_recommendation_runs_ranked_paths CHECK (
    cardinality(ranked_path_version_ids) > 0
    AND app_private.uuid_array_is_distinct(ranked_path_version_ids)
  ),
  CONSTRAINT ck_path_recommendation_runs_expiry CHECK (expires_at > generated_at)
);

-- TBL-STU-009 .. TBL-STU-019
CREATE TABLE learning_paths (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  slug varchar(120) NOT NULL UNIQUE,
  owner_subject_id uuid NOT NULL,
  current_draft_version_id uuid,
  latest_published_version_id uuid,
  archived_at timestamptz,
  CONSTRAINT ck_learning_paths_slug CHECK (slug ~ '^[a-z0-9]+(?:-[a-z0-9]+)*$')
);

CREATE TABLE learning_path_versions (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  path_id uuid NOT NULL REFERENCES learning_paths(id) ON DELETE RESTRICT,
  version_no integer NOT NULL,
  status content_version_status NOT NULL DEFAULT 'DRAFT',
  title varchar(200) NOT NULL,
  summary varchar(1000) NOT NULL,
  description_markdown text NOT NULL,
  estimated_hours integer NOT NULL,
  cover_file_id uuid,
  content_hash char(64) NOT NULL,
  created_by_subject_id uuid NOT NULL,
  published_at timestamptz,
  superseded_at timestamptz,
  discarded_at timestamptz,
  source_version_id uuid,
  CONSTRAINT uq_learning_path_versions_path_version UNIQUE (path_id, version_no),
  CONSTRAINT uq_learning_path_versions_path_id UNIQUE (path_id, id),
  CONSTRAINT ck_learning_path_versions_version_no CHECK (version_no >= 1),
  CONSTRAINT ck_learning_path_versions_estimated_hours CHECK (estimated_hours BETWEEN 1 AND 10000),
  CONSTRAINT ck_learning_path_versions_published CHECK (
    status <> 'PUBLISHED' OR (published_at IS NOT NULL AND content_hash IS NOT NULL)
  ),
  CONSTRAINT fk_learning_path_versions_source_same_path
    FOREIGN KEY (path_id, source_version_id)
    REFERENCES learning_path_versions(path_id, id) DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE courses (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  slug varchar(120) NOT NULL UNIQUE,
  owner_subject_id uuid NOT NULL,
  current_draft_version_id uuid,
  latest_published_version_id uuid,
  archived_at timestamptz,
  CONSTRAINT ck_courses_slug CHECK (slug ~ '^[a-z0-9]+(?:-[a-z0-9]+)*$')
);

CREATE TABLE course_versions (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  course_id uuid NOT NULL REFERENCES courses(id) ON DELETE RESTRICT,
  version_no integer NOT NULL,
  status content_version_status NOT NULL DEFAULT 'DRAFT',
  title varchar(200) NOT NULL,
  summary varchar(1000) NOT NULL,
  description_markdown text NOT NULL,
  level varchar(24) NOT NULL,
  estimated_minutes integer NOT NULL,
  thumbnail_file_id uuid,
  content_hash char(64) NOT NULL,
  created_by_subject_id uuid NOT NULL,
  published_at timestamptz,
  superseded_at timestamptz,
  discarded_at timestamptz,
  source_version_id uuid,
  CONSTRAINT uq_course_versions_course_version UNIQUE (course_id, version_no),
  CONSTRAINT uq_course_versions_course_id UNIQUE (course_id, id),
  CONSTRAINT ck_course_versions_version_no CHECK (version_no >= 1),
  CONSTRAINT ck_course_versions_level CHECK (level IN ('BEGINNER', 'INTERMEDIATE', 'ADVANCED')),
  CONSTRAINT ck_course_versions_estimated_minutes CHECK (estimated_minutes BETWEEN 1 AND 600000),
  CONSTRAINT ck_course_versions_published CHECK (
    status <> 'PUBLISHED' OR (published_at IS NOT NULL AND content_hash IS NOT NULL)
  ),
  CONSTRAINT fk_course_versions_source_same_course
    FOREIGN KEY (course_id, source_version_id)
    REFERENCES course_versions(course_id, id) DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE path_course_items (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  path_version_id uuid NOT NULL REFERENCES learning_path_versions(id) ON DELETE RESTRICT,
  course_version_id uuid NOT NULL REFERENCES course_versions(id) ON DELETE RESTRICT,
  position integer NOT NULL,
  is_required boolean NOT NULL DEFAULT true,
  unlock_rule jsonb NOT NULL DEFAULT '{}'::jsonb,
  CONSTRAINT uq_path_course_items_position UNIQUE (path_version_id, position),
  CONSTRAINT uq_path_course_items_course UNIQUE (path_version_id, course_version_id),
  CONSTRAINT ck_path_course_items_position CHECK (position >= 1)
);

CREATE TABLE chapters (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  course_version_id uuid NOT NULL REFERENCES course_versions(id) ON DELETE RESTRICT,
  title varchar(200) NOT NULL,
  summary varchar(1000),
  position integer NOT NULL,
  CONSTRAINT uq_chapters_course_position UNIQUE (course_version_id, position),
  CONSTRAINT uq_chapters_id_course_version UNIQUE (id, course_version_id),
  CONSTRAINT ck_chapters_position CHECK (position >= 1)
);

CREATE TABLE lessons (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  chapter_id uuid NOT NULL,
  course_version_id uuid NOT NULL,
  title varchar(200) NOT NULL,
  summary varchar(1000),
  position integer NOT NULL,
  estimated_minutes integer NOT NULL,
  is_preview boolean NOT NULL DEFAULT false,
  CONSTRAINT fk_lessons_chapter_same_course_version
    FOREIGN KEY (chapter_id, course_version_id)
    REFERENCES chapters(id, course_version_id) ON DELETE RESTRICT,
  CONSTRAINT uq_lessons_chapter_position UNIQUE (chapter_id, position),
  CONSTRAINT uq_lessons_id_course_version UNIQUE (id, course_version_id),
  CONSTRAINT ck_lessons_position CHECK (position >= 1),
  CONSTRAINT ck_lessons_estimated_minutes CHECK (estimated_minutes BETWEEN 1 AND 1440)
);

CREATE TABLE content_blocks (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  lesson_id uuid NOT NULL REFERENCES lessons(id) ON DELETE RESTRICT,
  block_type varchar(24) NOT NULL,
  position integer NOT NULL,
  content_json jsonb NOT NULL,
  plain_text text,
  estimated_seconds integer NOT NULL DEFAULT 0,
  content_hash char(64) NOT NULL,
  CONSTRAINT uq_content_blocks_lesson_position UNIQUE (lesson_id, position),
  CONSTRAINT ck_content_blocks_type CHECK (block_type IN ('MARKDOWN', 'VIDEO', 'IMAGE', 'EMBED', 'DOWNLOAD')),
  CONSTRAINT ck_content_blocks_position CHECK (position >= 1),
  CONSTRAINT ck_content_blocks_estimated_seconds CHECK (estimated_seconds >= 0)
);

CREATE TABLE content_rights_attestations (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  resource_type varchar(24) NOT NULL,
  resource_version_id uuid NOT NULL,
  publisher_subject_id uuid NOT NULL,
  rights_basis varchar(40) NOT NULL,
  source_url varchar(2048),
  license_code varchar(80),
  attestation_text_hash char(64) NOT NULL,
  attested_at timestamptz NOT NULL,
  expires_at timestamptz,
  revoked_at timestamptz,
  CONSTRAINT ck_content_rights_attestations_resource_type CHECK (resource_type IN ('PATH_VERSION', 'COURSE_VERSION')),
  CONSTRAINT ck_content_rights_attestations_basis CHECK (rights_basis IN ('OWNED', 'LICENSED', 'OPEN_LICENSE', 'AUTHORIZED')),
  CONSTRAINT ck_content_rights_attestations_expiry CHECK (expires_at IS NULL OR expires_at > attested_at)
);

CREATE TABLE content_review_decisions (
  id uuid PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  resource_type varchar(24) NOT NULL,
  resource_version_id uuid NOT NULL,
  reviewer_subject_id uuid NOT NULL,
  decision varchar(24) NOT NULL,
  reason_codes varchar(80)[] NOT NULL,
  comment varchar(2000),
  expected_row_version bigint NOT NULL,
  trace_id varchar(64) NOT NULL,
  CONSTRAINT ck_content_review_decisions_resource_type CHECK (resource_type IN ('PATH_VERSION', 'COURSE_VERSION')),
  CONSTRAINT ck_content_review_decisions_decision CHECK (decision IN ('APPROVE', 'REJECT', 'REQUEST_CHANGES')),
  CONSTRAINT ck_content_review_decisions_reason_required CHECK (
    decision = 'APPROVE' OR cardinality(reason_codes) > 0
  ),
  CONSTRAINT ck_content_review_decisions_expected_version CHECK (expected_row_version >= 1)
);

CREATE TABLE trusted_publisher_grants (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  publisher_subject_id uuid NOT NULL,
  scope varchar(24) NOT NULL,
  valid_from timestamptz NOT NULL,
  valid_until timestamptz NOT NULL,
  granted_by_subject_id uuid NOT NULL,
  grant_reason varchar(1000) NOT NULL,
  eligibility_snapshot jsonb NOT NULL,
  revoked_at timestamptz,
  revoked_by_subject_id uuid,
  revoke_reason varchar(1000),
  CONSTRAINT ck_trusted_publisher_grants_scope CHECK (scope = 'STUDY_CONTENT'),
  CONSTRAINT ck_trusted_publisher_grants_validity CHECK (valid_until > valid_from),
  CONSTRAINT ck_trusted_publisher_grants_revocation CHECK (
    (revoked_at IS NULL AND revoked_by_subject_id IS NULL AND revoke_reason IS NULL)
    OR (revoked_at IS NOT NULL AND revoked_by_subject_id IS NOT NULL AND revoke_reason IS NOT NULL)
  )
);

-- TBL-STU-020 .. TBL-STU-030
CREATE TABLE assessments (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  course_version_id uuid NOT NULL REFERENCES course_versions(id) ON DELETE RESTRICT,
  type assessment_type NOT NULL,
  title varchar(200) NOT NULL,
  instructions_markdown text NOT NULL,
  max_attempts integer,
  passing_score numeric(5,2),
  due_rule jsonb,
  content_hash char(64) NOT NULL,
  CONSTRAINT ck_assessments_max_attempts CHECK (max_attempts IS NULL OR max_attempts BETWEEN 1 AND 100),
  CONSTRAINT ck_assessments_passing_score CHECK (passing_score IS NULL OR passing_score BETWEEN 0 AND 100),
  CONSTRAINT ck_assessments_quiz_passing_score CHECK (type <> 'QUIZ' OR passing_score IS NOT NULL)
);

CREATE TABLE assessment_placements (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  assessment_id uuid NOT NULL UNIQUE REFERENCES assessments(id) ON DELETE RESTRICT,
  path_version_id uuid REFERENCES learning_path_versions(id) ON DELETE RESTRICT,
  course_version_id uuid REFERENCES course_versions(id) ON DELETE RESTRICT,
  chapter_id uuid REFERENCES chapters(id) ON DELETE RESTRICT,
  lesson_id uuid REFERENCES lessons(id) ON DELETE RESTRICT,
  position integer NOT NULL,
  is_required boolean NOT NULL DEFAULT true,
  CONSTRAINT ck_assessment_placements_exactly_one_scope CHECK (
    num_nonnulls(path_version_id, course_version_id, chapter_id, lesson_id) = 1
  ),
  CONSTRAINT ck_assessment_placements_position CHECK (position >= 1)
);

CREATE TABLE quiz_questions (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  assessment_id uuid NOT NULL REFERENCES assessments(id) ON DELETE RESTRICT,
  question_type varchar(24) NOT NULL,
  prompt_markdown text NOT NULL,
  explanation_markdown text,
  position integer NOT NULL,
  points numeric(7,2) NOT NULL,
  shuffle_options boolean NOT NULL DEFAULT false,
  CONSTRAINT uq_quiz_questions_assessment_position UNIQUE (assessment_id, position),
  CONSTRAINT ck_quiz_questions_type CHECK (question_type IN ('SINGLE_CHOICE', 'MULTIPLE_CHOICE', 'TRUE_FALSE')),
  CONSTRAINT ck_quiz_questions_position CHECK (position >= 1),
  CONSTRAINT ck_quiz_questions_points CHECK (points > 0)
);

CREATE TABLE quiz_options (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  question_id uuid NOT NULL REFERENCES quiz_questions(id) ON DELETE RESTRICT,
  label_markdown text NOT NULL,
  position integer NOT NULL,
  is_correct boolean NOT NULL,
  weight numeric(7,4) NOT NULL DEFAULT 1,
  CONSTRAINT uq_quiz_options_question_position UNIQUE (question_id, position),
  CONSTRAINT ck_quiz_options_position CHECK (position >= 1),
  CONSTRAINT ck_quiz_options_weight CHECK (weight BETWEEN 0 AND 1)
);

CREATE TABLE rubrics (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  assessment_id uuid NOT NULL UNIQUE REFERENCES assessments(id) ON DELETE RESTRICT,
  title varchar(200) NOT NULL,
  total_points numeric(7,2) NOT NULL,
  passing_points numeric(7,2) NOT NULL,
  version_no integer NOT NULL DEFAULT 1,
  CONSTRAINT ck_rubrics_points CHECK (passing_points > 0 AND passing_points <= total_points),
  CONSTRAINT ck_rubrics_version_no CHECK (version_no >= 1)
);

CREATE TABLE rubric_criteria (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  rubric_id uuid NOT NULL REFERENCES rubrics(id) ON DELETE RESTRICT,
  name varchar(160) NOT NULL,
  description varchar(1000) NOT NULL,
  max_points numeric(7,2) NOT NULL,
  position integer NOT NULL,
  CONSTRAINT uq_rubric_criteria_position UNIQUE (rubric_id, position),
  CONSTRAINT ck_rubric_criteria_max_points CHECK (max_points > 0),
  CONSTRAINT ck_rubric_criteria_position CHECK (position >= 1)
);

CREATE TABLE primary_path_periods (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  learner_id uuid NOT NULL REFERENCES learner_profiles(id) ON DELETE RESTRICT,
  path_version_id uuid NOT NULL REFERENCES learning_path_versions(id) ON DELETE RESTRICT,
  status primary_path_status NOT NULL,
  started_at timestamptz NOT NULL,
  ended_at timestamptz,
  end_reason varchar(80),
  supersedes_period_id uuid REFERENCES primary_path_periods(id) ON DELETE RESTRICT,
  switch_request_id uuid,
  selected_from_recommendation_id uuid REFERENCES path_recommendation_runs(id) ON DELETE RESTRICT,
  CONSTRAINT ck_primary_path_periods_end_state CHECK (
    (status = 'ACTIVE' AND ended_at IS NULL AND end_reason IS NULL)
    OR (status <> 'ACTIVE' AND ended_at IS NOT NULL)
  ),
  CONSTRAINT ck_primary_path_periods_end_time CHECK (ended_at IS NULL OR ended_at >= started_at)
);

CREATE TABLE course_enrollments (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  learner_id uuid NOT NULL REFERENCES learner_profiles(id) ON DELETE RESTRICT,
  course_version_id uuid NOT NULL REFERENCES course_versions(id) ON DELETE RESTRICT,
  source_type varchar(24) NOT NULL,
  source_path_period_id uuid REFERENCES primary_path_periods(id) ON DELETE RESTRICT,
  status enrollment_status NOT NULL DEFAULT 'ENROLLED',
  enrolled_at timestamptz NOT NULL,
  first_started_at timestamptz,
  completed_at timestamptz,
  last_activity_at timestamptz,
  hidden_from_my_courses_at timestamptz,
  CONSTRAINT uq_course_enrollments_learner_course UNIQUE (learner_id, course_version_id),
  CONSTRAINT ck_course_enrollments_source_type CHECK (source_type IN ('STANDALONE', 'PRIMARY_PATH', 'ADMIN')),
  CONSTRAINT ck_course_enrollments_source_path CHECK (
    (source_type = 'PRIMARY_PATH' AND source_path_period_id IS NOT NULL)
    OR (source_type <> 'PRIMARY_PATH' AND source_path_period_id IS NULL)
  ),
  CONSTRAINT ck_course_enrollments_completion CHECK (
    (status = 'COMPLETED' AND completed_at IS NOT NULL)
    OR (status <> 'COMPLETED' AND completed_at IS NULL)
  )
);

CREATE TABLE block_progress_facts (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  enrollment_id uuid NOT NULL REFERENCES course_enrollments(id) ON DELETE RESTRICT,
  block_id uuid NOT NULL REFERENCES content_blocks(id) ON DELETE RESTRICT,
  status progress_status NOT NULL DEFAULT 'NOT_STARTED',
  first_started_at timestamptz,
  completed_at timestamptz,
  last_position_seconds integer,
  last_event_id uuid NOT NULL UNIQUE,
  CONSTRAINT uq_block_progress_facts_enrollment_block UNIQUE (enrollment_id, block_id),
  CONSTRAINT ck_block_progress_facts_position CHECK (last_position_seconds IS NULL OR last_position_seconds >= 0)
);

CREATE TABLE lesson_progress_facts (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  enrollment_id uuid NOT NULL REFERENCES course_enrollments(id) ON DELETE RESTRICT,
  lesson_id uuid NOT NULL REFERENCES lessons(id) ON DELETE RESTRICT,
  status progress_status NOT NULL DEFAULT 'NOT_STARTED',
  first_started_at timestamptz,
  completed_at timestamptz,
  completion_source varchar(24),
  CONSTRAINT uq_lesson_progress_facts_enrollment_lesson UNIQUE (enrollment_id, lesson_id),
  CONSTRAINT ck_lesson_progress_facts_completion_source CHECK (
    completion_source IS NULL OR completion_source IN ('BLOCKS', 'ASSESSMENT', 'ADMIN')
  ),
  CONSTRAINT ck_lesson_progress_facts_completed CHECK (
    status <> 'COMPLETED' OR completion_source IS NOT NULL
  )
);

CREATE TABLE progress_snapshots (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  learner_id uuid NOT NULL REFERENCES learner_profiles(id) ON DELETE RESTRICT,
  scope_type varchar(24) NOT NULL,
  scope_id uuid NOT NULL,
  completed_units integer NOT NULL,
  total_units integer NOT NULL,
  percent numeric(5,2) NOT NULL,
  source_high_watermark timestamptz NOT NULL,
  rebuilt_at timestamptz NOT NULL,
  calculation_version integer NOT NULL,
  CONSTRAINT uq_progress_snapshots_scope UNIQUE (learner_id, scope_type, scope_id),
  CONSTRAINT ck_progress_snapshots_scope_type CHECK (scope_type IN ('COURSE_VERSION', 'PATH_VERSION')),
  CONSTRAINT ck_progress_snapshots_units CHECK (
    completed_units >= 0 AND total_units >= 0 AND completed_units <= total_units
  ),
  CONSTRAINT ck_progress_snapshots_percent CHECK (percent BETWEEN 0 AND 100),
  CONSTRAINT ck_progress_snapshots_calculation_version CHECK (calculation_version >= 1)
);

-- TBL-STU-031 .. TBL-STU-041
CREATE TABLE course_completions (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  learner_id uuid NOT NULL REFERENCES learner_profiles(id) ON DELETE RESTRICT,
  course_version_id uuid NOT NULL REFERENCES course_versions(id) ON DELETE RESTRICT,
  enrollment_id uuid NOT NULL UNIQUE REFERENCES course_enrollments(id) ON DELETE RESTRICT,
  completed_at timestamptz NOT NULL,
  rule_version integer NOT NULL,
  facts_hash char(64) NOT NULL,
  revoked_at timestamptz,
  revocation_reason varchar(500),
  CONSTRAINT uq_course_completions_learner_course UNIQUE (learner_id, course_version_id),
  CONSTRAINT ck_course_completions_rule_version CHECK (rule_version >= 1),
  CONSTRAINT ck_course_completions_revocation CHECK (
    (revoked_at IS NULL AND revocation_reason IS NULL)
    OR (revoked_at IS NOT NULL AND revocation_reason IS NOT NULL)
  )
);

CREATE TABLE path_completions (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  learner_id uuid NOT NULL REFERENCES learner_profiles(id) ON DELETE RESTRICT,
  path_version_id uuid NOT NULL REFERENCES learning_path_versions(id) ON DELETE RESTRICT,
  primary_path_period_id uuid NOT NULL REFERENCES primary_path_periods(id) ON DELETE RESTRICT,
  completed_at timestamptz NOT NULL,
  rule_version integer NOT NULL,
  course_completion_ids uuid[] NOT NULL,
  facts_hash char(64) NOT NULL,
  revoked_at timestamptz,
  revocation_reason varchar(500),
  CONSTRAINT uq_path_completions_period UNIQUE (learner_id, path_version_id, primary_path_period_id),
  CONSTRAINT ck_path_completions_rule_version CHECK (rule_version >= 1),
  CONSTRAINT ck_path_completions_course_completions CHECK (
    cardinality(course_completion_ids) > 0
    AND app_private.uuid_array_is_distinct(course_completion_ids)
  ),
  CONSTRAINT ck_path_completions_revocation CHECK (
    (revoked_at IS NULL AND revocation_reason IS NULL)
    OR (revoked_at IS NOT NULL AND revocation_reason IS NOT NULL)
  )
);

CREATE TABLE assessment_attempts (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  learner_id uuid NOT NULL REFERENCES learner_profiles(id) ON DELETE RESTRICT,
  enrollment_id uuid NOT NULL REFERENCES course_enrollments(id) ON DELETE RESTRICT,
  assessment_id uuid NOT NULL REFERENCES assessments(id) ON DELETE RESTRICT,
  attempt_no integer NOT NULL,
  status attempt_status NOT NULL DEFAULT 'SUBMITTED',
  submitted_payload_snapshot jsonb NOT NULL,
  submitted_at timestamptz NOT NULL,
  auto_score numeric(7,2),
  final_score numeric(7,2),
  graded_at timestamptz,
  grader_subject_id uuid,
  content_hash char(64) NOT NULL,
  CONSTRAINT uq_assessment_attempts_learner_assessment_attempt UNIQUE (learner_id, assessment_id, attempt_no),
  CONSTRAINT ck_assessment_attempts_attempt_no CHECK (attempt_no >= 1),
  CONSTRAINT ck_assessment_attempts_auto_score CHECK (auto_score IS NULL OR auto_score >= 0),
  CONSTRAINT ck_assessment_attempts_final_score CHECK (final_score IS NULL OR final_score >= 0)
);

CREATE TABLE assessment_answers (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  attempt_id uuid NOT NULL REFERENCES assessment_attempts(id) ON DELETE RESTRICT,
  question_id uuid REFERENCES quiz_questions(id) ON DELETE RESTRICT,
  answer_type assessment_type NOT NULL,
  answer_text text,
  answer_url varchar(2048),
  selected_option_ids uuid[],
  answer_hash char(64) NOT NULL,
  position integer NOT NULL,
  CONSTRAINT uq_assessment_answers_attempt_position UNIQUE (attempt_id, position),
  CONSTRAINT ck_assessment_answers_position CHECK (position >= 1),
  CONSTRAINT ck_assessment_answers_payload CHECK (
    (answer_type = 'QUIZ' AND cardinality(selected_option_ids) > 0 AND answer_text IS NULL AND answer_url IS NULL)
    OR (answer_type = 'TEXT' AND length(answer_text) BETWEEN 1 AND 20000 AND answer_url IS NULL)
    OR (answer_type = 'LINK' AND answer_url ~ '^https://')
    OR (answer_type = 'FILE' AND answer_text IS NULL AND answer_url IS NULL)
  )
);

CREATE TABLE file_objects (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  owner_subject_id uuid NOT NULL,
  purpose varchar(40) NOT NULL,
  storage_key varchar(700) NOT NULL UNIQUE,
  original_name varchar(255) NOT NULL,
  declared_mime varchar(120) NOT NULL,
  detected_mime varchar(120),
  size_bytes bigint NOT NULL,
  sha256 char(64) NOT NULL,
  scan_status file_asset_status NOT NULL DEFAULT 'CREATED',
  uploaded_at timestamptz,
  available_at timestamptz,
  quarantined_at timestamptz,
  expires_at timestamptz,
  deleted_at timestamptz,
  CONSTRAINT ck_file_objects_size_bytes CHECK (size_bytes >= 1),
  CONSTRAINT ck_file_objects_storage_key_no_filename CHECK (storage_key !~ '[[:space:]]')
);

CREATE TABLE malware_scan_results (
  id uuid PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  file_id uuid NOT NULL REFERENCES file_objects(id) ON DELETE RESTRICT,
  scanner varchar(40) NOT NULL DEFAULT 'CLAMAV',
  engine_version varchar(80) NOT NULL,
  signature_version varchar(80) NOT NULL,
  result file_asset_status NOT NULL,
  detected_mime varchar(120),
  threat_name varchar(200),
  error_code varchar(80),
  scan_duration_ms integer NOT NULL,
  worker_id varchar(120) NOT NULL,
  CONSTRAINT ck_malware_scan_results_status CHECK (result IN ('CLEAN', 'INFECTED', 'SCAN_FAILED')),
  CONSTRAINT ck_malware_scan_results_duration CHECK (scan_duration_ms >= 0),
  CONSTRAINT ck_malware_scan_results_threat CHECK (
    result <> 'INFECTED' OR threat_name IS NOT NULL
  )
);

CREATE TABLE attempt_files (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  attempt_id uuid NOT NULL REFERENCES assessment_attempts(id) ON DELETE RESTRICT,
  answer_id uuid NOT NULL REFERENCES assessment_answers(id) ON DELETE RESTRICT,
  file_id uuid NOT NULL REFERENCES file_objects(id) ON DELETE RESTRICT,
  attached_at timestamptz NOT NULL,
  CONSTRAINT uq_attempt_files_attempt_file UNIQUE (attempt_id, file_id)
);

CREATE TABLE assessment_reviews (
  id uuid PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  attempt_id uuid NOT NULL REFERENCES assessment_attempts(id) ON DELETE RESTRICT,
  review_round integer NOT NULL,
  reviewer_subject_id uuid NOT NULL,
  decision review_decision NOT NULL,
  score numeric(7,2),
  feedback_markdown text NOT NULL,
  expected_attempt_version bigint NOT NULL,
  supersedes_review_id uuid REFERENCES assessment_reviews(id) ON DELETE RESTRICT,
  trace_id varchar(64) NOT NULL,
  CONSTRAINT uq_assessment_reviews_round UNIQUE (attempt_id, review_round),
  CONSTRAINT ck_assessment_reviews_round CHECK (review_round >= 1),
  CONSTRAINT ck_assessment_reviews_score CHECK (score IS NULL OR score >= 0),
  CONSTRAINT ck_assessment_reviews_feedback CHECK (
    decision = 'PASSED' OR length(feedback_markdown) > 0
  ),
  CONSTRAINT ck_assessment_reviews_expected_version CHECK (expected_attempt_version >= 1)
);

CREATE TABLE assessment_review_scores (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  review_id uuid NOT NULL REFERENCES assessment_reviews(id) ON DELETE RESTRICT,
  criterion_id uuid NOT NULL REFERENCES rubric_criteria(id) ON DELETE RESTRICT,
  points numeric(7,2) NOT NULL,
  comment varchar(1000),
  CONSTRAINT uq_assessment_review_scores_review_criterion UNIQUE (review_id, criterion_id),
  CONSTRAINT ck_assessment_review_scores_points CHECK (points >= 0)
);

CREATE TABLE evidence_records (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  learner_id uuid NOT NULL REFERENCES learner_profiles(id) ON DELETE RESTRICT,
  evidence_type varchar(32) NOT NULL,
  source_type varchar(32) NOT NULL,
  source_id uuid NOT NULL,
  source_version_id uuid NOT NULL,
  status evidence_status NOT NULL DEFAULT 'ISSUED',
  title varchar(200) NOT NULL,
  description varchar(1000) NOT NULL,
  issued_at timestamptz NOT NULL,
  expires_at timestamptz,
  revoked_at timestamptz,
  revocation_reason varchar(500),
  claims_snapshot jsonb NOT NULL,
  claims_hash char(64) NOT NULL,
  issuer_key_id varchar(80) NOT NULL,
  signature varchar(512) NOT NULL,
  schema_version integer NOT NULL,
  CONSTRAINT uq_evidence_records_source UNIQUE (
    learner_id, source_type, source_id, source_version_id, evidence_type
  ),
  CONSTRAINT ck_evidence_records_schema_version CHECK (schema_version >= 1),
  CONSTRAINT ck_evidence_records_status CHECK (
    (status = 'ISSUED' AND revoked_at IS NULL AND revocation_reason IS NULL)
    OR (status = 'REVOKED' AND revoked_at IS NOT NULL AND revocation_reason IS NOT NULL)
  )
);

CREATE TABLE evidence_export_requests (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  request_id uuid NOT NULL UNIQUE,
  application_id uuid NOT NULL,
  learner_identity_subject_id uuid NOT NULL,
  requested_evidence_ids uuid[] NOT NULL,
  consent_id uuid NOT NULL,
  requester_service varchar(20) NOT NULL DEFAULT 'WORK',
  request_signature_hash char(64) NOT NULL,
  requested_at timestamptz NOT NULL,
  processed_at timestamptz,
  result_code varchar(80),
  response_hash char(64),
  trace_id varchar(64) NOT NULL,
  CONSTRAINT ck_evidence_export_requests_ids CHECK (
    cardinality(requested_evidence_ids) > 0
    AND app_private.uuid_array_is_distinct(requested_evidence_ids)
  ),
  CONSTRAINT ck_evidence_export_requests_service CHECK (requester_service = 'WORK')
);

-- TBL-STU-042 .. TBL-STU-055
CREATE TABLE notification_preferences (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  learner_id uuid NOT NULL REFERENCES learner_profiles(id) ON DELETE RESTRICT,
  category varchar(40) NOT NULL,
  in_app_enabled boolean NOT NULL DEFAULT true,
  email_enabled boolean NOT NULL DEFAULT true,
  quiet_hours_start time,
  quiet_hours_end time,
  timezone varchar(64) NOT NULL,
  consent_source varchar(40) NOT NULL,
  CONSTRAINT uq_notification_preferences_learner_category UNIQUE (learner_id, category)
);

CREATE TABLE notifications (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  learner_id uuid NOT NULL REFERENCES learner_profiles(id) ON DELETE RESTRICT,
  category varchar(40) NOT NULL,
  template_code varchar(80) NOT NULL,
  template_version integer NOT NULL,
  title varchar(200) NOT NULL,
  body varchar(4000) NOT NULL,
  action_url varchar(1000),
  dedupe_key varchar(180) NOT NULL,
  read_at timestamptz,
  expires_at timestamptz NOT NULL,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  CONSTRAINT uq_notifications_learner_dedupe UNIQUE (learner_id, dedupe_key),
  CONSTRAINT ck_notifications_action_url CHECK (action_url IS NULL OR action_url ~ '^/'),
  CONSTRAINT ck_notifications_template_version CHECK (template_version >= 1)
);

CREATE TABLE notification_deliveries (
  id uuid PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  notification_id uuid NOT NULL REFERENCES notifications(id) ON DELETE RESTRICT,
  channel varchar(16) NOT NULL,
  status notification_status NOT NULL,
  provider_message_id varchar(160),
  attempt_no integer NOT NULL,
  error_code varchar(80),
  next_retry_at timestamptz,
  dedupe_key varchar(180) NOT NULL,
  CONSTRAINT uq_notification_deliveries_attempt UNIQUE (notification_id, channel, attempt_no),
  CONSTRAINT uq_notification_deliveries_dedupe UNIQUE (dedupe_key),
  CONSTRAINT ck_notification_deliveries_channel CHECK (channel IN ('IN_APP', 'EMAIL')),
  CONSTRAINT ck_notification_deliveries_attempt_no CHECK (attempt_no >= 1)
);

CREATE TABLE community_channels (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  scope_type varchar(24) NOT NULL,
  scope_id uuid NOT NULL,
  provider varchar(20) NOT NULL DEFAULT 'ZALO',
  name varchar(160) NOT NULL,
  join_url_ciphertext bytea NOT NULL,
  url_fingerprint char(64) NOT NULL,
  rules_version integer NOT NULL,
  active_from timestamptz NOT NULL,
  active_until timestamptz,
  disabled_at timestamptz,
  CONSTRAINT ck_community_channels_scope CHECK (scope_type IN ('PLATFORM', 'PATH_VERSION', 'COURSE_VERSION')),
  CONSTRAINT ck_community_channels_provider CHECK (provider = 'ZALO'),
  CONSTRAINT ck_community_channels_rules_version CHECK (rules_version >= 1),
  CONSTRAINT ck_community_channels_active_range CHECK (active_until IS NULL OR active_until > active_from)
);

CREATE TABLE community_acceptances (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  learner_id uuid NOT NULL REFERENCES learner_profiles(id) ON DELETE RESTRICT,
  channel_id uuid NOT NULL REFERENCES community_channels(id) ON DELETE RESTRICT,
  rules_version integer NOT NULL,
  accepted_at timestamptz NOT NULL,
  ip_hash char(64),
  revoked_at timestamptz,
  CONSTRAINT ck_community_acceptances_rules_version CHECK (rules_version >= 1)
);

CREATE TABLE support_tickets (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  learner_id uuid NOT NULL REFERENCES learner_profiles(id) ON DELETE RESTRICT,
  category varchar(40) NOT NULL,
  status varchar(24) NOT NULL DEFAULT 'OPEN',
  subject varchar(200) NOT NULL,
  description text NOT NULL,
  priority varchar(16) NOT NULL DEFAULT 'NORMAL',
  assigned_to_subject_id uuid,
  resolved_at timestamptz,
  cancelled_at timestamptz,
  resolution_code varchar(80),
  CONSTRAINT ck_support_tickets_status CHECK (
    status IN ('OPEN', 'IN_PROGRESS', 'WAITING_LEARNER', 'RESOLVED', 'CANCELLED')
  ),
  CONSTRAINT ck_support_tickets_priority CHECK (priority IN ('LOW', 'NORMAL', 'HIGH', 'URGENT')),
  CONSTRAINT ck_support_tickets_finished_at CHECK (
    (status = 'RESOLVED' AND resolved_at IS NOT NULL AND cancelled_at IS NULL)
    OR (status = 'CANCELLED' AND cancelled_at IS NOT NULL AND resolved_at IS NULL)
    OR (status NOT IN ('RESOLVED', 'CANCELLED') AND resolved_at IS NULL AND cancelled_at IS NULL)
  )
);

CREATE TABLE support_messages (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  ticket_id uuid NOT NULL REFERENCES support_tickets(id) ON DELETE RESTRICT,
  author_subject_id uuid NOT NULL,
  author_type varchar(16) NOT NULL,
  body text NOT NULL,
  attachment_file_ids uuid[] NOT NULL DEFAULT '{}'::uuid[],
  is_internal boolean NOT NULL DEFAULT false,
  sent_at timestamptz NOT NULL,
  CONSTRAINT ck_support_messages_author_type CHECK (author_type IN ('LEARNER', 'STAFF')),
  CONSTRAINT ck_support_messages_internal_author CHECK (NOT is_internal OR author_type = 'STAFF')
);

CREATE TABLE admin_adjustments (
  id uuid PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  target_type varchar(32) NOT NULL,
  target_id uuid NOT NULL,
  action varchar(80) NOT NULL,
  before_snapshot jsonb NOT NULL,
  after_snapshot jsonb NOT NULL,
  reason varchar(1000) NOT NULL,
  approved_by_subject_id uuid NOT NULL,
  performed_by_subject_id uuid NOT NULL,
  trace_id varchar(64) NOT NULL
);

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
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
  prev_hash char(64),
  event_hash char(64) NOT NULL UNIQUE,
  legal_hold_until timestamptz
);

CREATE TABLE idempotency_keys (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  actor_subject_id uuid,
  operation varchar(120) NOT NULL,
  key_hash char(64) NOT NULL,
  request_hash char(64) NOT NULL,
  response_status integer,
  response_body jsonb,
  locked_until timestamptz,
  completed_at timestamptz,
  expires_at timestamptz NOT NULL,
  CONSTRAINT uq_idempotency_keys_actor_operation_key UNIQUE NULLS NOT DISTINCT (actor_subject_id, operation, key_hash)
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
  CONSTRAINT ck_outbox_events_version CHECK (event_version >= 1),
  CONSTRAINT ck_outbox_events_payload CHECK (
    payload ? 'schemaVersion' AND payload ? 'occurredAt' AND payload ? 'producer' AND payload ? 'traceId'
  )
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

CREATE TABLE report_snapshots (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  report_code varchar(80) NOT NULL,
  period_start timestamptz NOT NULL,
  period_end timestamptz NOT NULL,
  dimension_hash char(64) NOT NULL,
  dimensions jsonb NOT NULL,
  metrics jsonb NOT NULL,
  source_high_watermark timestamptz NOT NULL,
  calculation_version integer NOT NULL,
  generated_at timestamptz NOT NULL,
  CONSTRAINT uq_report_snapshots_unique UNIQUE (
    report_code, period_start, period_end, dimension_hash, calculation_version
  ),
  CONSTRAINT ck_report_snapshots_period CHECK (period_end > period_start),
  CONSTRAINT ck_report_snapshots_calculation_version CHECK (calculation_version >= 1)
);

CREATE TABLE outbox_delivery_attempts (
  id uuid PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  outbox_event_id uuid NOT NULL REFERENCES outbox_events(id) ON DELETE RESTRICT,
  attempt_no integer NOT NULL,
  status outbox_status NOT NULL,
  worker_id varchar(120) NOT NULL,
  broker_message_id varchar(180),
  error_code varchar(80),
  next_retry_at timestamptz,
  payload_hash char(64) NOT NULL,
  CONSTRAINT uq_outbox_delivery_attempts_event_attempt UNIQUE (outbox_event_id, attempt_no),
  CONSTRAINT ck_outbox_delivery_attempts_attempt_no CHECK (attempt_no >= 1)
);

-- TBL-STU-056 .. TBL-STU-060
CREATE TABLE study_skills (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  code varchar(80) NOT NULL UNIQUE,
  name varchar(160) NOT NULL,
  normalized_name varchar(160) NOT NULL UNIQUE,
  category varchar(80),
  description varchar(1000),
  status varchar(16) NOT NULL DEFAULT 'ACTIVE',
  aliases varchar(160)[] NOT NULL DEFAULT '{}'::varchar[],
  CONSTRAINT ck_study_skills_status CHECK (status IN ('ACTIVE', 'ARCHIVED'))
);

CREATE TABLE course_skill_outcomes (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  course_version_id uuid NOT NULL REFERENCES course_versions(id) ON DELETE RESTRICT,
  skill_id uuid NOT NULL REFERENCES study_skills(id) ON DELETE RESTRICT,
  outcome_level smallint NOT NULL,
  description varchar(1000) NOT NULL,
  position integer NOT NULL,
  CONSTRAINT uq_course_skill_outcomes_skill UNIQUE (course_version_id, skill_id),
  CONSTRAINT uq_course_skill_outcomes_position UNIQUE (course_version_id, position),
  CONSTRAINT ck_course_skill_outcomes_level CHECK (outcome_level BETWEEN 1 AND 5),
  CONSTRAINT ck_course_skill_outcomes_position CHECK (position >= 1)
);

CREATE TABLE course_prerequisites (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  course_version_id uuid NOT NULL REFERENCES course_versions(id) ON DELETE RESTRICT,
  required_course_version_id uuid NOT NULL REFERENCES course_versions(id) ON DELETE RESTRICT,
  require_completion boolean NOT NULL DEFAULT true,
  position integer NOT NULL,
  CONSTRAINT uq_course_prerequisites_required UNIQUE (course_version_id, required_course_version_id),
  CONSTRAINT uq_course_prerequisites_position UNIQUE (course_version_id, position),
  CONSTRAINT ck_course_prerequisites_not_self CHECK (course_version_id <> required_course_version_id),
  CONSTRAINT ck_course_prerequisites_position CHECK (position >= 1)
);

CREATE TABLE file_upload_sessions (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  file_id uuid NOT NULL UNIQUE REFERENCES file_objects(id) ON DELETE RESTRICT,
  owner_subject_id uuid NOT NULL,
  upload_id varchar(200) NOT NULL UNIQUE,
  expected_size_bytes bigint NOT NULL,
  expected_sha256 char(64) NOT NULL,
  part_count integer NOT NULL DEFAULT 1,
  status varchar(24) NOT NULL DEFAULT 'CREATED',
  expires_at timestamptz NOT NULL,
  completed_at timestamptz,
  aborted_at timestamptz,
  CONSTRAINT ck_file_upload_sessions_size CHECK (expected_size_bytes > 0),
  CONSTRAINT ck_file_upload_sessions_part_count CHECK (part_count BETWEEN 1 AND 10000),
  CONSTRAINT ck_file_upload_sessions_status CHECK (status IN ('CREATED', 'UPLOADING', 'COMPLETED', 'ABORTED', 'EXPIRED')),
  CONSTRAINT ck_file_upload_sessions_finalized CHECK (
    (status = 'COMPLETED' AND completed_at IS NOT NULL AND aborted_at IS NULL)
    OR (status = 'ABORTED' AND aborted_at IS NOT NULL AND completed_at IS NULL)
    OR (status IN ('CREATED', 'UPLOADING', 'EXPIRED') AND completed_at IS NULL AND aborted_at IS NULL)
  )
);

CREATE TABLE assessment_drafts (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  row_version bigint NOT NULL DEFAULT 1,
  learner_id uuid NOT NULL REFERENCES learner_profiles(id) ON DELETE RESTRICT,
  enrollment_id uuid NOT NULL REFERENCES course_enrollments(id) ON DELETE RESTRICT,
  assessment_id uuid NOT NULL REFERENCES assessments(id) ON DELETE RESTRICT,
  answer_type assessment_type NOT NULL,
  payload jsonb NOT NULL,
  file_id uuid REFERENCES file_objects(id) ON DELETE RESTRICT,
  state varchar(16) NOT NULL DEFAULT 'DRAFT',
  last_saved_at timestamptz NOT NULL,
  sealed_at timestamptz,
  sealed_attempt_id uuid REFERENCES assessment_attempts(id) ON DELETE RESTRICT,
  content_hash char(64) NOT NULL,
  CONSTRAINT uq_assessment_drafts_learner_assessment UNIQUE (learner_id, assessment_id),
  CONSTRAINT ck_assessment_drafts_state CHECK (state IN ('DRAFT', 'SEALED')),
  CONSTRAINT ck_assessment_drafts_sealed CHECK (
    (state = 'DRAFT' AND sealed_at IS NULL AND sealed_attempt_id IS NULL)
    OR (state = 'SEALED' AND sealed_at IS NOT NULL AND sealed_attempt_id IS NOT NULL)
  )
);

-- Deferred references that are intentionally created after their targets.
ALTER TABLE learner_profiles
  ADD CONSTRAINT fk_learner_profiles_avatar_file
  FOREIGN KEY (avatar_file_id) REFERENCES file_objects(id)
  ON DELETE RESTRICT DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE learning_path_versions
  ADD CONSTRAINT fk_learning_path_versions_cover_file
  FOREIGN KEY (cover_file_id) REFERENCES file_objects(id)
  ON DELETE RESTRICT DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE course_versions
  ADD CONSTRAINT fk_course_versions_thumbnail_file
  FOREIGN KEY (thumbnail_file_id) REFERENCES file_objects(id)
  ON DELETE RESTRICT DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE learning_paths
  ADD CONSTRAINT fk_learning_paths_current_draft_same_path
  FOREIGN KEY (id, current_draft_version_id)
  REFERENCES learning_path_versions(path_id, id)
  ON DELETE RESTRICT DEFERRABLE INITIALLY DEFERRED,
  ADD CONSTRAINT fk_learning_paths_latest_published_same_path
  FOREIGN KEY (id, latest_published_version_id)
  REFERENCES learning_path_versions(path_id, id)
  ON DELETE RESTRICT DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE courses
  ADD CONSTRAINT fk_courses_current_draft_same_course
  FOREIGN KEY (id, current_draft_version_id)
  REFERENCES course_versions(course_id, id)
  ON DELETE RESTRICT DEFERRABLE INITIALLY DEFERRED,
  ADD CONSTRAINT fk_courses_latest_published_same_course
  FOREIGN KEY (id, latest_published_version_id)
  REFERENCES course_versions(course_id, id)
  ON DELETE RESTRICT DEFERRABLE INITIALLY DEFERRED;

-- Required indexes from the BD query matrix and each table definition.
CREATE INDEX ix_identity_projections_account_status ON identity_projections (account_status);
CREATE INDEX ix_learner_profiles_onboarding_completed_at ON learner_profiles (onboarding_completed_at);
CREATE INDEX ix_learner_profiles_deleted_at ON learner_profiles (deleted_at);
CREATE INDEX ix_service_roles_disabled_code ON service_roles (disabled_at, code);
CREATE INDEX ix_service_permissions_risk_code ON service_permissions (risk_level, code);
CREATE UNIQUE INDEX ux_service_role_permissions_active
  ON service_role_permissions (role_id, permission_id) WHERE revoked_at IS NULL;
CREATE INDEX ix_service_role_permissions_role_active ON service_role_permissions (role_id, revoked_at);
CREATE INDEX ix_service_role_permissions_permission_active ON service_role_permissions (permission_id, revoked_at);
CREATE UNIQUE INDEX ux_service_role_assignments_active
  ON service_role_assignments (identity_subject_id, role_id) WHERE revoked_at IS NULL;
CREATE INDEX ix_service_role_assignments_subject_active
  ON service_role_assignments (identity_subject_id, revoked_at, valid_until);
CREATE UNIQUE INDEX ux_onboarding_submissions_current
  ON onboarding_submissions (learner_id) WHERE is_current;
CREATE INDEX ix_onboarding_submissions_learner_submitted
  ON onboarding_submissions (learner_id, submitted_at DESC);
CREATE INDEX ix_path_recommendation_runs_learner_generated
  ON path_recommendation_runs (learner_id, generated_at DESC);
CREATE INDEX ix_learning_paths_archived_updated ON learning_paths (archived_at, updated_at DESC);
CREATE INDEX ix_learning_path_versions_path_status_version
  ON learning_path_versions (path_id, status, version_no DESC);
CREATE INDEX ix_learning_path_versions_status_published
  ON learning_path_versions (status, published_at DESC);
CREATE INDEX ix_courses_archived_updated ON courses (archived_at, updated_at DESC);
CREATE INDEX ix_course_versions_course_status_version
  ON course_versions (course_id, status, version_no DESC);
CREATE INDEX ix_course_versions_status_published ON course_versions (status, published_at DESC);
CREATE INDEX ix_course_versions_catalog_fts
  ON course_versions USING gin (to_tsvector('simple', title || ' ' || summary));
CREATE INDEX ix_path_course_items_course_path ON path_course_items (course_version_id, path_version_id);
CREATE INDEX ix_chapters_course_position ON chapters (course_version_id, position);
CREATE INDEX ix_lessons_course_chapter_position ON lessons (course_version_id, chapter_id, position);
CREATE INDEX ix_content_blocks_lesson_position ON content_blocks (lesson_id, position);
CREATE INDEX ix_content_blocks_admin_fts
  ON content_blocks USING gin (to_tsvector('simple', coalesce(plain_text, '')));
CREATE INDEX ix_content_rights_attestations_resource_active
  ON content_rights_attestations (resource_type, resource_version_id, revoked_at);
CREATE INDEX ix_content_review_decisions_resource_time
  ON content_review_decisions (resource_type, resource_version_id, occurred_at DESC);
CREATE UNIQUE INDEX ux_trusted_publisher_grants_active
  ON trusted_publisher_grants (publisher_subject_id, scope) WHERE revoked_at IS NULL;
CREATE INDEX ix_trusted_publisher_grants_publisher_scope
  ON trusted_publisher_grants (publisher_subject_id, scope, revoked_at, valid_until);
CREATE INDEX ix_assessments_course_type ON assessments (course_version_id, type);
CREATE UNIQUE INDEX ux_assessment_placements_path_position
  ON assessment_placements (path_version_id, position) WHERE path_version_id IS NOT NULL;
CREATE UNIQUE INDEX ux_assessment_placements_course_position
  ON assessment_placements (course_version_id, position) WHERE course_version_id IS NOT NULL;
CREATE UNIQUE INDEX ux_assessment_placements_chapter_position
  ON assessment_placements (chapter_id, position) WHERE chapter_id IS NOT NULL;
CREATE UNIQUE INDEX ux_assessment_placements_lesson_position
  ON assessment_placements (lesson_id, position) WHERE lesson_id IS NOT NULL;
CREATE INDEX ix_quiz_questions_assessment_position ON quiz_questions (assessment_id, position);
CREATE INDEX ix_quiz_options_question_position ON quiz_options (question_id, position);
CREATE INDEX ix_rubric_criteria_rubric_position ON rubric_criteria (rubric_id, position);
CREATE UNIQUE INDEX ux_primary_path_periods_active
  ON primary_path_periods (learner_id) WHERE status = 'ACTIVE';
CREATE INDEX ix_primary_path_periods_learner_started ON primary_path_periods (learner_id, started_at DESC);
CREATE INDEX ix_primary_path_periods_path_status ON primary_path_periods (path_version_id, status);
CREATE INDEX ix_course_enrollments_learner_status_activity
  ON course_enrollments (learner_id, status, last_activity_at DESC);
CREATE INDEX ix_course_enrollments_course_status ON course_enrollments (course_version_id, status);
CREATE INDEX ix_block_progress_facts_enrollment_status ON block_progress_facts (enrollment_id, status);
CREATE INDEX ix_block_progress_facts_block_status ON block_progress_facts (block_id, status);
CREATE INDEX ix_lesson_progress_facts_enrollment_status ON lesson_progress_facts (enrollment_id, status);
CREATE INDEX ix_progress_snapshots_scope_percent ON progress_snapshots (scope_type, scope_id, percent);
CREATE INDEX ix_progress_snapshots_learner_rebuilt ON progress_snapshots (learner_id, rebuilt_at DESC);
CREATE INDEX ix_course_completions_learner_completed ON course_completions (learner_id, completed_at DESC);
CREATE INDEX ix_course_completions_course_completed ON course_completions (course_version_id, completed_at);
CREATE INDEX ix_path_completions_learner_completed ON path_completions (learner_id, completed_at DESC);
CREATE INDEX ix_assessment_attempts_learner_assessment_attempt
  ON assessment_attempts (learner_id, assessment_id, attempt_no DESC);
CREATE INDEX ix_assessment_attempts_review_queue ON assessment_attempts (status, submitted_at);
CREATE INDEX ix_assessment_answers_attempt_position ON assessment_answers (attempt_id, position);
CREATE UNIQUE INDEX ux_file_objects_sha_owner_purpose_live
  ON file_objects (sha256, owner_subject_id, purpose) WHERE deleted_at IS NULL;
CREATE INDEX ix_file_objects_owner_purpose_created ON file_objects (owner_subject_id, purpose, created_at DESC);
CREATE INDEX ix_file_objects_scan_created ON file_objects (scan_status, created_at);
CREATE INDEX ix_file_objects_expires ON file_objects (expires_at) WHERE expires_at IS NOT NULL;
CREATE INDEX ix_malware_scan_results_file_occurred ON malware_scan_results (file_id, occurred_at DESC);
CREATE INDEX ix_malware_scan_results_result_occurred ON malware_scan_results (result, occurred_at);
CREATE INDEX ix_attempt_files_answer ON attempt_files (answer_id);
CREATE INDEX ix_assessment_reviews_attempt_round ON assessment_reviews (attempt_id, review_round DESC);
CREATE INDEX ix_assessment_reviews_reviewer_occurred ON assessment_reviews (reviewer_subject_id, occurred_at DESC);
CREATE INDEX ix_assessment_review_scores_review ON assessment_review_scores (review_id);
CREATE INDEX ix_evidence_records_learner_status_issued ON evidence_records (learner_id, status, issued_at DESC);
CREATE INDEX ix_evidence_records_source ON evidence_records (source_type, source_id);
CREATE INDEX ix_evidence_records_expires ON evidence_records (expires_at);
CREATE INDEX ix_evidence_export_requests_learner_requested
  ON evidence_export_requests (learner_identity_subject_id, requested_at DESC);
CREATE INDEX ix_evidence_export_requests_application ON evidence_export_requests (application_id);
CREATE INDEX ix_notification_preferences_learner_category ON notification_preferences (learner_id, category);
CREATE INDEX ix_notifications_inbox_cursor ON notifications (learner_id, read_at, created_at DESC, id DESC);
CREATE INDEX ix_notifications_expires ON notifications (expires_at);
CREATE INDEX ix_notification_deliveries_retry ON notification_deliveries (status, next_retry_at);
CREATE UNIQUE INDEX ux_community_channels_active
  ON community_channels (scope_type, scope_id, provider) WHERE disabled_at IS NULL;
CREATE INDEX ix_community_channels_scope_active ON community_channels (scope_type, scope_id, disabled_at);
CREATE UNIQUE INDEX ux_community_acceptances_active
  ON community_acceptances (learner_id, channel_id, rules_version) WHERE revoked_at IS NULL;
CREATE INDEX ix_community_acceptances_learner_accepted ON community_acceptances (learner_id, accepted_at DESC);
CREATE INDEX ix_support_tickets_learner_created ON support_tickets (learner_id, created_at DESC);
CREATE INDEX ix_support_tickets_status_priority_created ON support_tickets (status, priority, created_at);
CREATE INDEX ix_support_messages_ticket_sent ON support_messages (ticket_id, sent_at, id);
CREATE INDEX ix_admin_adjustments_target_occurred ON admin_adjustments (target_type, target_id, occurred_at DESC);
CREATE INDEX ix_audit_events_resource_occurred ON audit_events (resource_type, resource_id, occurred_at DESC);
CREATE INDEX ix_audit_events_actor_occurred ON audit_events (actor_subject_id, occurred_at DESC);
CREATE INDEX ix_audit_events_trace_id ON audit_events (trace_id);
CREATE INDEX ix_audit_events_occurred_brin ON audit_events USING brin (occurred_at);
CREATE INDEX ix_idempotency_keys_expires ON idempotency_keys (expires_at);
CREATE INDEX ix_outbox_events_available ON outbox_events (available_at, id);
CREATE INDEX ix_outbox_events_aggregate_created ON outbox_events (aggregate_type, aggregate_id, created_at);
CREATE INDEX ix_consumer_inbox_processing ON consumer_inbox (consumer, processed_at, received_at);
CREATE INDEX ix_report_snapshots_code_period_end ON report_snapshots (report_code, period_end DESC);
CREATE INDEX ix_outbox_delivery_attempts_event_latest ON outbox_delivery_attempts (outbox_event_id, attempt_no DESC);
CREATE INDEX ix_outbox_delivery_attempts_retry ON outbox_delivery_attempts (status, next_retry_at);
CREATE INDEX ix_study_skills_normalized_name_trgm ON study_skills USING gin (normalized_name gin_trgm_ops);
CREATE INDEX ix_study_skills_aliases ON study_skills USING gin (aliases);
CREATE INDEX ix_study_skills_status_category ON study_skills (status, category);
CREATE INDEX ix_course_skill_outcomes_skill_course ON course_skill_outcomes (skill_id, course_version_id);
CREATE INDEX ix_course_skill_outcomes_course_position ON course_skill_outcomes (course_version_id, position);
CREATE INDEX ix_course_prerequisites_required_course ON course_prerequisites (required_course_version_id, course_version_id);
CREATE INDEX ix_course_prerequisites_course_position ON course_prerequisites (course_version_id, position);
CREATE INDEX ix_file_upload_sessions_owner_status_created ON file_upload_sessions (owner_subject_id, status, created_at DESC);
CREATE INDEX ix_file_upload_sessions_status_expires ON file_upload_sessions (status, expires_at);
CREATE INDEX ix_assessment_drafts_learner_assessment_state ON assessment_drafts (learner_id, assessment_id, state);
CREATE INDEX ix_assessment_drafts_enrollment_saved ON assessment_drafts (enrollment_id, last_saved_at DESC);

-- Cross-row and cross-tree integrity that cannot be expressed as a CHECK.
CREATE FUNCTION app_private.assert_clean_avatar_file()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  file_status file_asset_status;
BEGIN
  IF NEW.avatar_file_id IS NULL THEN
    RETURN NEW;
  END IF;
  SELECT scan_status INTO file_status FROM file_objects WHERE id = NEW.avatar_file_id;
  IF file_status IS DISTINCT FROM 'CLEAN' THEN
    RAISE EXCEPTION 'avatar file % must be CLEAN', NEW.avatar_file_id USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.assert_entity_file_clean()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  file_id uuid;
  file_status file_asset_status;
BEGIN
  IF TG_TABLE_NAME = 'learning_path_versions' THEN
    file_id := NEW.cover_file_id;
  ELSIF TG_TABLE_NAME = 'course_versions' THEN
    file_id := NEW.thumbnail_file_id;
  ELSE
    file_id := NEW.file_id;
  END IF;
  IF file_id IS NOT NULL AND NEW.status = 'PUBLISHED' THEN
    SELECT scan_status INTO file_status FROM file_objects WHERE id = file_id;
    IF file_status IS DISTINCT FROM 'CLEAN' THEN
      RAISE EXCEPTION 'published content requires CLEAN file %', file_id USING ERRCODE = '23514';
    END IF;
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.assert_path_or_course_pointers()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  draft_status content_version_status;
  published_status content_version_status;
BEGIN
  IF TG_TABLE_NAME = 'learning_paths' THEN
    IF NEW.current_draft_version_id IS NOT NULL THEN
      SELECT status INTO draft_status FROM learning_path_versions WHERE id = NEW.current_draft_version_id;
    END IF;
    IF NEW.latest_published_version_id IS NOT NULL THEN
      SELECT status INTO published_status FROM learning_path_versions WHERE id = NEW.latest_published_version_id;
    END IF;
  ELSE
    IF NEW.current_draft_version_id IS NOT NULL THEN
      SELECT status INTO draft_status FROM course_versions WHERE id = NEW.current_draft_version_id;
    END IF;
    IF NEW.latest_published_version_id IS NOT NULL THEN
      SELECT status INTO published_status FROM course_versions WHERE id = NEW.latest_published_version_id;
    END IF;
  END IF;
  IF NEW.current_draft_version_id IS NOT NULL AND draft_status IS DISTINCT FROM 'DRAFT' THEN
    RAISE EXCEPTION 'current_draft_version_id must reference DRAFT version' USING ERRCODE = '23514';
  END IF;
  IF NEW.latest_published_version_id IS NOT NULL AND published_status IS DISTINCT FROM 'PUBLISHED' THEN
    RAISE EXCEPTION 'latest_published_version_id must reference PUBLISHED version' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.assert_assessment_placement_scope()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  assessment_course_version_id uuid;
  scope_course_version_id uuid;
BEGIN
  SELECT course_version_id INTO assessment_course_version_id FROM assessments WHERE id = NEW.assessment_id;
  IF NEW.course_version_id IS NOT NULL THEN
    scope_course_version_id := NEW.course_version_id;
  ELSIF NEW.chapter_id IS NOT NULL THEN
    SELECT course_version_id INTO scope_course_version_id FROM chapters WHERE id = NEW.chapter_id;
  ELSIF NEW.lesson_id IS NOT NULL THEN
    SELECT course_version_id INTO scope_course_version_id FROM lessons WHERE id = NEW.lesson_id;
  ELSIF NEW.path_version_id IS NOT NULL THEN
    IF NOT EXISTS (
      SELECT 1 FROM path_course_items
      WHERE path_version_id = NEW.path_version_id
        AND course_version_id = assessment_course_version_id
    ) THEN
      RAISE EXCEPTION 'assessment placement path scope must contain the assessment course version'
        USING ERRCODE = '23514';
    END IF;
    RETURN NEW;
  END IF;
  IF scope_course_version_id IS DISTINCT FROM assessment_course_version_id THEN
    RAISE EXCEPTION 'assessment placement scope must be in the same course version'
      USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.assert_assessment_attempt_integrity()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  enrollment_learner_id uuid;
  enrollment_course_version_id uuid;
  assessment_course_version_id uuid;
BEGIN
  SELECT learner_id, course_version_id
    INTO enrollment_learner_id, enrollment_course_version_id
    FROM course_enrollments WHERE id = NEW.enrollment_id;
  SELECT course_version_id INTO assessment_course_version_id FROM assessments WHERE id = NEW.assessment_id;
  IF enrollment_learner_id IS DISTINCT FROM NEW.learner_id
     OR enrollment_course_version_id IS DISTINCT FROM assessment_course_version_id THEN
    RAISE EXCEPTION 'assessment attempt learner, enrollment and assessment must share a course version'
      USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.assert_assessment_draft_integrity()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  enrollment_learner_id uuid;
  enrollment_course_version_id uuid;
  assessment_course_version_id uuid;
  file_status file_asset_status;
BEGIN
  SELECT learner_id, course_version_id
    INTO enrollment_learner_id, enrollment_course_version_id
    FROM course_enrollments WHERE id = NEW.enrollment_id;
  SELECT course_version_id INTO assessment_course_version_id FROM assessments WHERE id = NEW.assessment_id;
  IF enrollment_learner_id IS DISTINCT FROM NEW.learner_id
     OR enrollment_course_version_id IS DISTINCT FROM assessment_course_version_id THEN
    RAISE EXCEPTION 'assessment draft learner, enrollment and assessment must share a course version'
      USING ERRCODE = '23514';
  END IF;
  IF NEW.file_id IS NOT NULL THEN
    SELECT scan_status INTO file_status FROM file_objects WHERE id = NEW.file_id;
    IF file_status IS DISTINCT FROM 'CLEAN' THEN
      RAISE EXCEPTION 'assessment draft file must be CLEAN' USING ERRCODE = '23514';
    END IF;
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.assert_progress_block_integrity()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  enrollment_course_version_id uuid;
  block_course_version_id uuid;
BEGIN
  SELECT course_version_id INTO enrollment_course_version_id FROM course_enrollments WHERE id = NEW.enrollment_id;
  SELECT lesson.course_version_id INTO block_course_version_id
    FROM content_blocks block
    JOIN lessons lesson ON lesson.id = block.lesson_id
   WHERE block.id = NEW.block_id;
  IF enrollment_course_version_id IS DISTINCT FROM block_course_version_id THEN
    RAISE EXCEPTION 'progress block must belong to enrollment course version' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.assert_progress_lesson_integrity()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  enrollment_course_version_id uuid;
  lesson_course_version_id uuid;
BEGIN
  SELECT course_version_id INTO enrollment_course_version_id FROM course_enrollments WHERE id = NEW.enrollment_id;
  SELECT course_version_id INTO lesson_course_version_id FROM lessons WHERE id = NEW.lesson_id;
  IF enrollment_course_version_id IS DISTINCT FROM lesson_course_version_id THEN
    RAISE EXCEPTION 'progress lesson must belong to enrollment course version' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.assert_course_completion_integrity()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  enrollment_learner_id uuid;
  enrollment_course_version_id uuid;
BEGIN
  SELECT learner_id, course_version_id
    INTO enrollment_learner_id, enrollment_course_version_id
    FROM course_enrollments WHERE id = NEW.enrollment_id;
  IF enrollment_learner_id IS DISTINCT FROM NEW.learner_id
     OR enrollment_course_version_id IS DISTINCT FROM NEW.course_version_id THEN
    RAISE EXCEPTION 'course completion must match its enrollment' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.assert_path_completion_integrity()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  period_learner_id uuid;
  period_path_version_id uuid;
BEGIN
  SELECT learner_id, path_version_id
    INTO period_learner_id, period_path_version_id
    FROM primary_path_periods WHERE id = NEW.primary_path_period_id;
  IF period_learner_id IS DISTINCT FROM NEW.learner_id
     OR period_path_version_id IS DISTINCT FROM NEW.path_version_id THEN
    RAISE EXCEPTION 'path completion must match its primary path period' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.assert_attempt_file_integrity()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  attempt_subject_id uuid;
  answer_attempt_id uuid;
  file_subject_id uuid;
  file_purpose varchar(40);
  file_status file_asset_status;
BEGIN
  SELECT learner.identity_subject_id
    INTO attempt_subject_id
    FROM assessment_attempts attempt
    JOIN learner_profiles learner ON learner.id = attempt.learner_id
   WHERE attempt.id = NEW.attempt_id;
  SELECT attempt_id INTO answer_attempt_id FROM assessment_answers WHERE id = NEW.answer_id;
  SELECT owner_subject_id, purpose, scan_status
    INTO file_subject_id, file_purpose, file_status
    FROM file_objects WHERE id = NEW.file_id;
  IF answer_attempt_id IS DISTINCT FROM NEW.attempt_id
     OR file_subject_id IS DISTINCT FROM attempt_subject_id
     OR file_purpose <> 'ASSESSMENT'
     OR file_status IS DISTINCT FROM 'CLEAN' THEN
    RAISE EXCEPTION 'attempt file must belong to its learner, answer and a CLEAN ASSESSMENT file'
      USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.assert_review_score_limit()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  max_allowed numeric(7,2);
BEGIN
  SELECT max_points INTO max_allowed FROM rubric_criteria WHERE id = NEW.criterion_id;
  IF NEW.points > max_allowed THEN
    RAISE EXCEPTION 'review score cannot exceed rubric criterion maximum' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.assert_rubric_assessment_type()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  assessment_kind assessment_type;
BEGIN
  SELECT type INTO assessment_kind FROM assessments WHERE id = NEW.assessment_id;
  IF assessment_kind NOT IN ('TEXT', 'LINK', 'FILE') THEN
    RAISE EXCEPTION 'rubric is only valid for TEXT, LINK, or FILE assessments' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.assert_file_upload_session_integrity()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  actual_owner uuid;
  actual_size bigint;
  actual_hash char(64);
BEGIN
  SELECT owner_subject_id, size_bytes, sha256
    INTO actual_owner, actual_size, actual_hash
    FROM file_objects WHERE id = NEW.file_id;
  IF actual_owner IS DISTINCT FROM NEW.owner_subject_id THEN
    RAISE EXCEPTION 'upload session owner must match file owner' USING ERRCODE = '23514';
  END IF;
  IF NEW.status = 'COMPLETED'
     AND (actual_size IS DISTINCT FROM NEW.expected_size_bytes
          OR actual_hash IS DISTINCT FROM NEW.expected_sha256) THEN
    RAISE EXCEPTION 'completed upload must match expected size and SHA-256' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.require_draft_course_version()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  version_id uuid;
  version_status content_version_status;
BEGIN
  version_id := CASE WHEN TG_OP = 'DELETE' THEN OLD.course_version_id ELSE NEW.course_version_id END;
  SELECT status INTO version_status FROM course_versions WHERE id = version_id;
  IF version_status IS DISTINCT FROM 'DRAFT' THEN
    RAISE EXCEPTION '% can only change while its course version is DRAFT', TG_TABLE_NAME
      USING ERRCODE = '55000';
  END IF;
  IF TG_OP = 'DELETE' THEN RETURN OLD; END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.require_draft_path_version()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  version_id uuid;
  version_status content_version_status;
BEGIN
  version_id := CASE WHEN TG_OP = 'DELETE' THEN OLD.path_version_id ELSE NEW.path_version_id END;
  SELECT status INTO version_status FROM learning_path_versions WHERE id = version_id;
  IF version_status IS DISTINCT FROM 'DRAFT' THEN
    RAISE EXCEPTION '% can only change while its path version is DRAFT', TG_TABLE_NAME
      USING ERRCODE = '55000';
  END IF;
  IF TG_OP = 'DELETE' THEN RETURN OLD; END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.require_draft_lesson_course_version()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  target_lesson_id uuid;
  version_status content_version_status;
BEGIN
  target_lesson_id := CASE WHEN TG_OP = 'DELETE' THEN OLD.lesson_id ELSE NEW.lesson_id END;
  SELECT version.status INTO version_status
    FROM lessons lesson
    JOIN course_versions version ON version.id = lesson.course_version_id
   WHERE lesson.id = target_lesson_id;
  IF version_status IS DISTINCT FROM 'DRAFT' THEN
    RAISE EXCEPTION '% can only change while its course version is DRAFT', TG_TABLE_NAME
      USING ERRCODE = '55000';
  END IF;
  IF TG_OP = 'DELETE' THEN RETURN OLD; END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.require_draft_assessment_course_version()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  target_assessment_id uuid;
  version_status content_version_status;
BEGIN
  target_assessment_id := CASE WHEN TG_OP = 'DELETE' THEN OLD.assessment_id ELSE NEW.assessment_id END;
  SELECT version.status INTO version_status
    FROM assessments assessment
    JOIN course_versions version ON version.id = assessment.course_version_id
   WHERE assessment.id = target_assessment_id;
  IF version_status IS DISTINCT FROM 'DRAFT' THEN
    RAISE EXCEPTION '% can only change while its assessment course version is DRAFT', TG_TABLE_NAME
      USING ERRCODE = '55000';
  END IF;
  IF TG_OP = 'DELETE' THEN RETURN OLD; END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.require_draft_question_course_version()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  target_question_id uuid;
  version_status content_version_status;
BEGIN
  target_question_id := CASE WHEN TG_OP = 'DELETE' THEN OLD.question_id ELSE NEW.question_id END;
  SELECT version.status INTO version_status
    FROM quiz_questions question
    JOIN assessments assessment ON assessment.id = question.assessment_id
    JOIN course_versions version ON version.id = assessment.course_version_id
   WHERE question.id = target_question_id;
  IF version_status IS DISTINCT FROM 'DRAFT' THEN
    RAISE EXCEPTION '% can only change while its course version is DRAFT', TG_TABLE_NAME
      USING ERRCODE = '55000';
  END IF;
  IF TG_OP = 'DELETE' THEN RETURN OLD; END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.require_draft_rubric_course_version()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  target_rubric_id uuid;
  version_status content_version_status;
BEGIN
  target_rubric_id := CASE WHEN TG_OP = 'DELETE' THEN OLD.rubric_id ELSE NEW.rubric_id END;
  SELECT version.status INTO version_status
    FROM rubrics rubric
    JOIN assessments assessment ON assessment.id = rubric.assessment_id
    JOIN course_versions version ON version.id = assessment.course_version_id
   WHERE rubric.id = target_rubric_id;
  IF version_status IS DISTINCT FROM 'DRAFT' THEN
    RAISE EXCEPTION '% can only change while its course version is DRAFT', TG_TABLE_NAME
      USING ERRCODE = '55000';
  END IF;
  IF TG_OP = 'DELETE' THEN RETURN OLD; END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.assert_active_study_skill()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  skill_status varchar(16);
BEGIN
  SELECT status INTO skill_status FROM study_skills WHERE id = NEW.skill_id;
  IF skill_status IS DISTINCT FROM 'ACTIVE' THEN
    RAISE EXCEPTION 'ARCHIVED skill cannot be added to a course draft' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.assert_no_course_prerequisite_cycle()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF EXISTS (
    WITH RECURSIVE prerequisites(course_version_id) AS (
      SELECT NEW.required_course_version_id
      UNION
      SELECT dependency.required_course_version_id
        FROM course_prerequisites dependency
        JOIN prerequisites current_node
          ON dependency.course_version_id = current_node.course_version_id
    )
    SELECT 1 FROM prerequisites WHERE course_version_id = NEW.course_version_id
  ) THEN
    RAISE EXCEPTION 'course prerequisite graph cannot contain a cycle' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.assert_course_version_publishable()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF NEW.status = 'PUBLISHED' AND OLD.status <> 'PUBLISHED' THEN
    IF EXISTS (
      SELECT 1
        FROM assessments assessment
        JOIN quiz_questions question ON question.assessment_id = assessment.id
       WHERE assessment.course_version_id = NEW.id
         AND assessment.type = 'QUIZ'
         AND NOT EXISTS (
           SELECT 1 FROM quiz_options option
            WHERE option.question_id = question.id AND option.is_correct
         )
    ) THEN
      RAISE EXCEPTION 'cannot publish course version with quiz questions that have no correct option'
        USING ERRCODE = '23514';
    END IF;
    IF EXISTS (
      SELECT 1
        FROM rubrics rubric
       WHERE rubric.assessment_id IN (
               SELECT id FROM assessments WHERE course_version_id = NEW.id
             )
         AND rubric.total_points IS DISTINCT FROM (
           SELECT coalesce(sum(criterion.max_points), 0)
             FROM rubric_criteria criterion
            WHERE criterion.rubric_id = rubric.id
         )
    ) THEN
      RAISE EXCEPTION 'cannot publish course version with rubric criteria total different from rubric total'
        USING ERRCODE = '23514';
    END IF;
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.assert_path_version_publishable()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF NEW.status = 'PUBLISHED' AND OLD.status <> 'PUBLISHED'
     AND EXISTS (
       SELECT 1
         FROM path_course_items item
         JOIN course_versions version ON version.id = item.course_version_id
        WHERE item.path_version_id = NEW.id
          AND version.status <> 'PUBLISHED'
     ) THEN
    RAISE EXCEPTION 'published learning path requires every included course version to be PUBLISHED'
      USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.guard_assessment_attempt_payload()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF NEW.learner_id IS DISTINCT FROM OLD.learner_id
     OR NEW.enrollment_id IS DISTINCT FROM OLD.enrollment_id
     OR NEW.assessment_id IS DISTINCT FROM OLD.assessment_id
     OR NEW.attempt_no IS DISTINCT FROM OLD.attempt_no
     OR NEW.submitted_payload_snapshot IS DISTINCT FROM OLD.submitted_payload_snapshot
     OR NEW.submitted_at IS DISTINCT FROM OLD.submitted_at
     OR NEW.content_hash IS DISTINCT FROM OLD.content_hash THEN
    RAISE EXCEPTION 'assessment attempt submission payload and identity are immutable'
      USING ERRCODE = '55000';
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.guard_attempt_status_transition()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  assessment_kind assessment_type;
BEGIN
  IF NEW.status = OLD.status THEN
    RETURN NEW;
  END IF;
  SELECT type INTO assessment_kind FROM assessments WHERE id = NEW.assessment_id;
  IF assessment_kind = 'QUIZ' THEN
    IF OLD.status <> 'SUBMITTED' OR NEW.status NOT IN ('PASSED', 'FAILED') THEN
      RAISE EXCEPTION 'QUIZ attempt transition is invalid' USING ERRCODE = '23514';
    END IF;
  ELSIF NOT (
    (OLD.status = 'SUBMITTED' AND NEW.status = 'UNDER_REVIEW')
    OR (OLD.status = 'UNDER_REVIEW' AND NEW.status IN ('PASSED', 'NEEDS_REVISION', 'FAILED'))
  ) THEN
    RAISE EXCEPTION 'assessment attempt transition is invalid' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.guard_progress_status_transition()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF NEW.status < OLD.status THEN
    RAISE EXCEPTION 'progress status cannot move backwards without an audited administrative adjustment'
      USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.guard_consumer_inbox_payload()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF NEW.consumer IS DISTINCT FROM OLD.consumer
     OR NEW.event_id IS DISTINCT FROM OLD.event_id
     OR NEW.event_type IS DISTINCT FROM OLD.event_type
     OR NEW.payload_hash IS DISTINCT FROM OLD.payload_hash
     OR NEW.received_at IS DISTINCT FROM OLD.received_at
     OR NEW.trace_id IS DISTINCT FROM OLD.trace_id THEN
    RAISE EXCEPTION 'consumer inbox event identity and payload hash are immutable'
      USING ERRCODE = '55000';
  END IF;
  RETURN NEW;
END
$$;

CREATE FUNCTION app_private.prevent_immutable_update()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  RAISE EXCEPTION '% is immutable and cannot be updated', TG_TABLE_NAME USING ERRCODE = '55000';
END
$$;

-- IMMUTABLE records may only make the one-way state transition expressly
-- represented by their BD columns. The original payload is never mutable.
CREATE FUNCTION app_private.guard_immutable_state_transition()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  old_row jsonb := to_jsonb(OLD);
  new_row jsonb := to_jsonb(NEW);
BEGIN
  CASE TG_TABLE_NAME
    WHEN 'onboarding_submissions' THEN
      IF (new_row - 'is_current') IS DISTINCT FROM (old_row - 'is_current')
         OR old_row->>'is_current' <> 'true'
         OR new_row->>'is_current' <> 'false' THEN
        RAISE EXCEPTION 'onboarding submission payload is immutable; is_current can only change true to false'
          USING ERRCODE = '55000';
      END IF;

    WHEN 'service_role_permissions' THEN
      IF (new_row - ARRAY['revoked_at', 'revoked_by_subject_id'])
           IS DISTINCT FROM (old_row - ARRAY['revoked_at', 'revoked_by_subject_id'])
         OR old_row->>'revoked_at' IS NOT NULL
         OR old_row->>'revoked_by_subject_id' IS NOT NULL
         OR new_row->>'revoked_at' IS NULL
         OR new_row->>'revoked_by_subject_id' IS NULL THEN
        RAISE EXCEPTION 'service role permission payload is immutable; revocation is one-way'
          USING ERRCODE = '55000';
      END IF;

    WHEN 'service_role_assignments' THEN
      IF (new_row - ARRAY['revoked_at', 'revoked_by_subject_id'])
           IS DISTINCT FROM (old_row - ARRAY['revoked_at', 'revoked_by_subject_id'])
         OR old_row->>'revoked_at' IS NOT NULL
         OR old_row->>'revoked_by_subject_id' IS NOT NULL
         OR new_row->>'revoked_at' IS NULL
         OR new_row->>'revoked_by_subject_id' IS NULL THEN
        RAISE EXCEPTION 'service role assignment payload is immutable; revocation is one-way'
          USING ERRCODE = '55000';
      END IF;

    WHEN 'content_rights_attestations' THEN
      IF (new_row - 'revoked_at') IS DISTINCT FROM (old_row - 'revoked_at')
         OR old_row->>'revoked_at' IS NOT NULL
         OR new_row->>'revoked_at' IS NULL THEN
        RAISE EXCEPTION 'content rights attestation payload is immutable; revocation is one-way'
          USING ERRCODE = '55000';
      END IF;

    WHEN 'trusted_publisher_grants' THEN
      IF (new_row - ARRAY['revoked_at', 'revoked_by_subject_id', 'revoke_reason'])
           IS DISTINCT FROM (old_row - ARRAY['revoked_at', 'revoked_by_subject_id', 'revoke_reason'])
         OR old_row->>'revoked_at' IS NOT NULL
         OR old_row->>'revoked_by_subject_id' IS NOT NULL
         OR old_row->>'revoke_reason' IS NOT NULL
         OR new_row->>'revoked_at' IS NULL
         OR new_row->>'revoked_by_subject_id' IS NULL
         OR new_row->>'revoke_reason' IS NULL THEN
        RAISE EXCEPTION 'trusted publisher grant payload is immutable; revocation is one-way'
          USING ERRCODE = '55000';
      END IF;

    WHEN 'primary_path_periods' THEN
      IF (new_row - ARRAY['status', 'ended_at', 'end_reason'])
           IS DISTINCT FROM (old_row - ARRAY['status', 'ended_at', 'end_reason'])
         OR old_row->>'status' <> 'ACTIVE'
         OR old_row->>'ended_at' IS NOT NULL
         OR new_row->>'status' NOT IN ('SWITCHED_OUT', 'COMPLETED', 'CANCELLED_BY_ADMIN')
         OR new_row->>'ended_at' IS NULL THEN
        RAISE EXCEPTION 'primary path period is immutable except for closing an ACTIVE period once'
          USING ERRCODE = '55000';
      END IF;

    WHEN 'course_completions', 'path_completions' THEN
      IF (new_row - ARRAY['revoked_at', 'revocation_reason'])
           IS DISTINCT FROM (old_row - ARRAY['revoked_at', 'revocation_reason'])
         OR old_row->>'revoked_at' IS NOT NULL
         OR old_row->>'revocation_reason' IS NOT NULL
         OR new_row->>'revoked_at' IS NULL
         OR new_row->>'revocation_reason' IS NULL THEN
        RAISE EXCEPTION '% payload is immutable; revocation is one-way', TG_TABLE_NAME
          USING ERRCODE = '55000';
      END IF;

    WHEN 'evidence_records' THEN
      IF (new_row - ARRAY['status', 'revoked_at', 'revocation_reason'])
           IS DISTINCT FROM (old_row - ARRAY['status', 'revoked_at', 'revocation_reason'])
         OR old_row->>'status' <> 'ISSUED'
         OR old_row->>'revoked_at' IS NOT NULL
         OR old_row->>'revocation_reason' IS NOT NULL
         OR new_row->>'status' <> 'REVOKED'
         OR new_row->>'revoked_at' IS NULL
         OR new_row->>'revocation_reason' IS NULL THEN
        RAISE EXCEPTION 'evidence payload is immutable; ISSUED to REVOKED is one-way'
          USING ERRCODE = '55000';
      END IF;

    WHEN 'evidence_export_requests' THEN
      IF (new_row - ARRAY['processed_at', 'result_code', 'response_hash'])
           IS DISTINCT FROM (old_row - ARRAY['processed_at', 'result_code', 'response_hash'])
         OR old_row->>'processed_at' IS NOT NULL
         OR new_row->>'processed_at' IS NULL THEN
        RAISE EXCEPTION 'evidence export request payload is immutable; processing can be recorded once'
          USING ERRCODE = '55000';
      END IF;

    WHEN 'community_acceptances' THEN
      IF (new_row - 'revoked_at') IS DISTINCT FROM (old_row - 'revoked_at')
         OR old_row->>'revoked_at' IS NOT NULL
         OR new_row->>'revoked_at' IS NULL THEN
        RAISE EXCEPTION 'community acceptance payload is immutable; revocation is one-way'
          USING ERRCODE = '55000';
      END IF;

    WHEN 'consumer_inbox' THEN
      IF (new_row - ARRAY['processed_at', 'result_code'])
           IS DISTINCT FROM (old_row - ARRAY['processed_at', 'result_code'])
         OR old_row->>'processed_at' IS NOT NULL
         OR new_row->>'processed_at' IS NULL THEN
        RAISE EXCEPTION 'consumer inbox payload is immutable; processing result can be recorded once'
          USING ERRCODE = '55000';
      END IF;

    ELSE
      RAISE EXCEPTION 'unexpected immutable-state guard target: %', TG_TABLE_NAME
        USING ERRCODE = '55000';
  END CASE;
  RETURN NEW;
END
$$;

-- ENTITY convention: updates always advance row_version and updated_at.
DO $$
DECLARE
  table_name text;
BEGIN
  FOREACH table_name IN ARRAY ARRAY[
    'identity_projections', 'learner_profiles', 'service_roles', 'service_permissions',
    'learning_paths', 'learning_path_versions', 'courses', 'course_versions',
    'path_course_items', 'chapters', 'lessons', 'content_blocks', 'assessments',
    'assessment_placements', 'quiz_questions', 'quiz_options', 'rubrics',
    'rubric_criteria', 'course_enrollments', 'block_progress_facts',
    'lesson_progress_facts', 'progress_snapshots', 'assessment_attempts',
    'file_objects', 'notification_preferences', 'notifications', 'community_channels',
    'support_tickets', 'idempotency_keys', 'study_skills', 'course_skill_outcomes',
    'course_prerequisites', 'file_upload_sessions', 'assessment_drafts'
  ]
  LOOP
    EXECUTE format(
      'CREATE TRIGGER trg_touch_entity BEFORE UPDATE ON public.%I '
      || 'FOR EACH ROW EXECUTE FUNCTION app_private.touch_entity()',
      table_name
    );
  END LOOP;
END
$$;

-- Append-only tables cannot be updated or deleted.
DO $$
DECLARE
  table_name text;
BEGIN
  FOREACH table_name IN ARRAY ARRAY[
    'content_review_decisions', 'malware_scan_results', 'assessment_reviews',
    'notification_deliveries', 'admin_adjustments', 'audit_events', 'outbox_delivery_attempts'
  ]
  LOOP
    EXECUTE format(
      'CREATE TRIGGER trg_prevent_append_mutation BEFORE UPDATE OR DELETE ON public.%I '
      || 'FOR EACH ROW EXECUTE FUNCTION app_private.prevent_append_mutation()',
      table_name
    );
  END LOOP;
END
$$;

-- Immutable records are never deleted; the listed audit/snapshot payloads also
-- reject updates entirely. Tables with explicit revocation/processing fields
-- retain those state changes while keeping their original payload columns.
DO $$
DECLARE
  table_name text;
BEGIN
  FOREACH table_name IN ARRAY ARRAY[
    'service_role_permissions', 'service_role_assignments', 'onboarding_submissions',
    'path_recommendation_runs', 'content_rights_attestations', 'trusted_publisher_grants',
    'primary_path_periods', 'course_completions', 'path_completions', 'assessment_answers',
    'attempt_files', 'assessment_review_scores', 'evidence_records',
    'evidence_export_requests', 'community_acceptances', 'support_messages',
    'outbox_events', 'consumer_inbox', 'report_snapshots'
  ]
  LOOP
    EXECUTE format(
      'CREATE TRIGGER trg_prevent_immutable_delete BEFORE DELETE ON public.%I '
      || 'FOR EACH ROW EXECUTE FUNCTION app_private.prevent_delete()',
      table_name
    );
  END LOOP;
  FOREACH table_name IN ARRAY ARRAY[
    'path_recommendation_runs', 'assessment_answers', 'attempt_files',
    'assessment_review_scores', 'support_messages', 'outbox_events', 'report_snapshots'
  ]
  LOOP
    EXECUTE format(
      'CREATE TRIGGER trg_prevent_immutable_update BEFORE UPDATE ON public.%I '
      || 'FOR EACH ROW EXECUTE FUNCTION app_private.prevent_immutable_update()',
      table_name
    );
  END LOOP;
END
$$;

DO $$
DECLARE
  table_name text;
BEGIN
  FOREACH table_name IN ARRAY ARRAY[
    'onboarding_submissions', 'service_role_permissions',
    'service_role_assignments', 'content_rights_attestations',
    'trusted_publisher_grants', 'primary_path_periods', 'course_completions',
    'path_completions', 'evidence_records', 'evidence_export_requests',
    'community_acceptances', 'consumer_inbox'
  ]
  LOOP
    EXECUTE format(
      'CREATE TRIGGER trg_guard_immutable_state BEFORE UPDATE ON public.%I '
      || 'FOR EACH ROW EXECUTE FUNCTION app_private.guard_immutable_state_transition()',
      table_name
    );
  END LOOP;
END
$$;

CREATE TRIGGER trg_guard_learning_path_version
  BEFORE UPDATE ON learning_path_versions
  FOR EACH ROW EXECUTE FUNCTION app_private.guard_content_version();
CREATE TRIGGER trg_guard_course_version
  BEFORE UPDATE ON course_versions
  FOR EACH ROW EXECUTE FUNCTION app_private.guard_content_version();
CREATE TRIGGER trg_publishable_learning_path_version
  BEFORE UPDATE ON learning_path_versions
  FOR EACH ROW EXECUTE FUNCTION app_private.assert_path_version_publishable();
CREATE TRIGGER trg_publishable_course_version
  BEFORE UPDATE ON course_versions
  FOR EACH ROW EXECUTE FUNCTION app_private.assert_course_version_publishable();
CREATE TRIGGER trg_published_path_file_clean
  BEFORE INSERT OR UPDATE ON learning_path_versions
  FOR EACH ROW EXECUTE FUNCTION app_private.assert_entity_file_clean();
CREATE TRIGGER trg_published_course_file_clean
  BEFORE INSERT OR UPDATE ON course_versions
  FOR EACH ROW EXECUTE FUNCTION app_private.assert_entity_file_clean();
CREATE TRIGGER trg_assessment_draft_sealed
  BEFORE UPDATE ON assessment_drafts
  FOR EACH ROW EXECUTE FUNCTION app_private.guard_sealed_assessment_draft();
CREATE TRIGGER trg_assessment_attempt_payload
  BEFORE UPDATE ON assessment_attempts
  FOR EACH ROW EXECUTE FUNCTION app_private.guard_assessment_attempt_payload();
CREATE TRIGGER trg_assessment_attempt_status
  BEFORE UPDATE OF status ON assessment_attempts
  FOR EACH ROW EXECUTE FUNCTION app_private.guard_attempt_status_transition();
CREATE TRIGGER trg_block_progress_status
  BEFORE UPDATE OF status ON block_progress_facts
  FOR EACH ROW EXECUTE FUNCTION app_private.guard_progress_status_transition();
CREATE TRIGGER trg_lesson_progress_status
  BEFORE UPDATE OF status ON lesson_progress_facts
  FOR EACH ROW EXECUTE FUNCTION app_private.guard_progress_status_transition();
CREATE TRIGGER trg_consumer_inbox_payload
  BEFORE UPDATE ON consumer_inbox
  FOR EACH ROW EXECUTE FUNCTION app_private.guard_consumer_inbox_payload();

CREATE TRIGGER trg_path_course_items_draft_parent
  BEFORE INSERT OR UPDATE OR DELETE ON path_course_items
  FOR EACH ROW EXECUTE FUNCTION app_private.require_draft_path_version();
CREATE TRIGGER trg_chapters_draft_parent
  BEFORE INSERT OR UPDATE OR DELETE ON chapters
  FOR EACH ROW EXECUTE FUNCTION app_private.require_draft_course_version();
CREATE TRIGGER trg_lessons_draft_parent
  BEFORE INSERT OR UPDATE OR DELETE ON lessons
  FOR EACH ROW EXECUTE FUNCTION app_private.require_draft_course_version();
CREATE TRIGGER trg_content_blocks_draft_parent
  BEFORE INSERT OR UPDATE OR DELETE ON content_blocks
  FOR EACH ROW EXECUTE FUNCTION app_private.require_draft_lesson_course_version();
CREATE TRIGGER trg_assessments_draft_parent
  BEFORE INSERT OR UPDATE OR DELETE ON assessments
  FOR EACH ROW EXECUTE FUNCTION app_private.require_draft_course_version();
CREATE TRIGGER trg_assessment_placements_draft_parent
  BEFORE INSERT OR UPDATE OR DELETE ON assessment_placements
  FOR EACH ROW EXECUTE FUNCTION app_private.require_draft_assessment_course_version();
CREATE TRIGGER trg_quiz_questions_draft_parent
  BEFORE INSERT OR UPDATE OR DELETE ON quiz_questions
  FOR EACH ROW EXECUTE FUNCTION app_private.require_draft_assessment_course_version();
CREATE TRIGGER trg_quiz_options_draft_parent
  BEFORE INSERT OR UPDATE OR DELETE ON quiz_options
  FOR EACH ROW EXECUTE FUNCTION app_private.require_draft_question_course_version();
CREATE TRIGGER trg_rubrics_draft_parent
  BEFORE INSERT OR UPDATE OR DELETE ON rubrics
  FOR EACH ROW EXECUTE FUNCTION app_private.require_draft_assessment_course_version();
CREATE TRIGGER trg_rubric_criteria_draft_parent
  BEFORE INSERT OR UPDATE OR DELETE ON rubric_criteria
  FOR EACH ROW EXECUTE FUNCTION app_private.require_draft_rubric_course_version();
CREATE TRIGGER trg_course_skill_outcomes_draft_parent
  BEFORE INSERT OR UPDATE OR DELETE ON course_skill_outcomes
  FOR EACH ROW EXECUTE FUNCTION app_private.require_draft_course_version();
CREATE TRIGGER trg_course_prerequisites_draft_parent
  BEFORE INSERT OR UPDATE OR DELETE ON course_prerequisites
  FOR EACH ROW EXECUTE FUNCTION app_private.require_draft_course_version();
CREATE TRIGGER trg_course_skill_outcomes_active_skill
  BEFORE INSERT OR UPDATE OF skill_id ON course_skill_outcomes
  FOR EACH ROW EXECUTE FUNCTION app_private.assert_active_study_skill();
CREATE TRIGGER trg_course_prerequisites_no_cycle
  BEFORE INSERT OR UPDATE OF course_version_id, required_course_version_id ON course_prerequisites
  FOR EACH ROW EXECUTE FUNCTION app_private.assert_no_course_prerequisite_cycle();

CREATE CONSTRAINT TRIGGER ctr_learner_profiles_avatar_clean
  AFTER INSERT OR UPDATE OF avatar_file_id ON learner_profiles
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW
  EXECUTE FUNCTION app_private.assert_clean_avatar_file();
CREATE CONSTRAINT TRIGGER ctr_learning_paths_pointers
  AFTER INSERT OR UPDATE OF current_draft_version_id, latest_published_version_id ON learning_paths
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW
  EXECUTE FUNCTION app_private.assert_path_or_course_pointers();
CREATE CONSTRAINT TRIGGER ctr_courses_pointers
  AFTER INSERT OR UPDATE OF current_draft_version_id, latest_published_version_id ON courses
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW
  EXECUTE FUNCTION app_private.assert_path_or_course_pointers();
CREATE CONSTRAINT TRIGGER ctr_assessment_placements_scope
  AFTER INSERT OR UPDATE ON assessment_placements
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW
  EXECUTE FUNCTION app_private.assert_assessment_placement_scope();
CREATE CONSTRAINT TRIGGER ctr_primary_path_periods_published
  AFTER INSERT OR UPDATE OF path_version_id ON primary_path_periods
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW
  EXECUTE FUNCTION app_private.require_published_path_version();
CREATE CONSTRAINT TRIGGER ctr_course_enrollments_published
  AFTER INSERT OR UPDATE OF course_version_id ON course_enrollments
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW
  EXECUTE FUNCTION app_private.require_published_course_version();
CREATE CONSTRAINT TRIGGER ctr_block_progress_integrity
  AFTER INSERT OR UPDATE OF enrollment_id, block_id ON block_progress_facts
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW
  EXECUTE FUNCTION app_private.assert_progress_block_integrity();
CREATE CONSTRAINT TRIGGER ctr_lesson_progress_integrity
  AFTER INSERT OR UPDATE OF enrollment_id, lesson_id ON lesson_progress_facts
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW
  EXECUTE FUNCTION app_private.assert_progress_lesson_integrity();
CREATE CONSTRAINT TRIGGER ctr_course_completions_integrity
  AFTER INSERT OR UPDATE OF learner_id, course_version_id, enrollment_id ON course_completions
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW
  EXECUTE FUNCTION app_private.assert_course_completion_integrity();
CREATE CONSTRAINT TRIGGER ctr_path_completions_integrity
  AFTER INSERT OR UPDATE OF learner_id, path_version_id, primary_path_period_id ON path_completions
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW
  EXECUTE FUNCTION app_private.assert_path_completion_integrity();
CREATE CONSTRAINT TRIGGER ctr_assessment_attempt_integrity
  AFTER INSERT OR UPDATE OF learner_id, enrollment_id, assessment_id ON assessment_attempts
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW
  EXECUTE FUNCTION app_private.assert_assessment_attempt_integrity();
CREATE CONSTRAINT TRIGGER ctr_assessment_draft_integrity
  AFTER INSERT OR UPDATE OF learner_id, enrollment_id, assessment_id, file_id ON assessment_drafts
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW
  EXECUTE FUNCTION app_private.assert_assessment_draft_integrity();
CREATE CONSTRAINT TRIGGER ctr_attempt_files_integrity
  AFTER INSERT OR UPDATE ON attempt_files
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW
  EXECUTE FUNCTION app_private.assert_attempt_file_integrity();
CREATE CONSTRAINT TRIGGER ctr_assessment_review_scores_limit
  AFTER INSERT OR UPDATE OF criterion_id, points ON assessment_review_scores
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW
  EXECUTE FUNCTION app_private.assert_review_score_limit();
CREATE CONSTRAINT TRIGGER ctr_rubrics_assessment_type
  AFTER INSERT OR UPDATE OF assessment_id ON rubrics
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW
  EXECUTE FUNCTION app_private.assert_rubric_assessment_type();
CREATE CONSTRAINT TRIGGER ctr_file_upload_sessions_integrity
  AFTER INSERT OR UPDATE ON file_upload_sessions
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW
  EXECUTE FUNCTION app_private.assert_file_upload_session_integrity();

-- RLS subject context. study_db contains no TENANT_ENTITY tables in BD03;
-- app.tenant_id remains required context for shared service infrastructure but
-- intentionally has no fabricated tenant_id column or policy in this database.
CREATE FUNCTION app_private.owns_learner(target_learner_id uuid)
RETURNS boolean
LANGUAGE sql
STABLE
AS $$
  SELECT EXISTS (
    SELECT 1
      FROM learner_profiles
     WHERE id = target_learner_id
       AND identity_subject_id = app_private.current_subject_id()
  )
$$;

CREATE FUNCTION app_private.owns_enrollment(target_enrollment_id uuid)
RETURNS boolean
LANGUAGE sql
STABLE
AS $$
  SELECT EXISTS (
    SELECT 1 FROM course_enrollments WHERE id = target_enrollment_id
      AND app_private.owns_learner(learner_id)
  )
$$;

CREATE FUNCTION app_private.owns_attempt(target_attempt_id uuid)
RETURNS boolean
LANGUAGE sql
STABLE
AS $$
  SELECT EXISTS (
    SELECT 1 FROM assessment_attempts WHERE id = target_attempt_id
      AND app_private.owns_learner(learner_id)
  )
$$;

CREATE FUNCTION app_private.owns_notification(target_notification_id uuid)
RETURNS boolean
LANGUAGE sql
STABLE
AS $$
  SELECT EXISTS (
    SELECT 1 FROM notifications WHERE id = target_notification_id
      AND app_private.owns_learner(learner_id)
  )
$$;

CREATE FUNCTION app_private.owns_support_ticket(target_ticket_id uuid)
RETURNS boolean
LANGUAGE sql
STABLE
AS $$
  SELECT EXISTS (
    SELECT 1 FROM support_tickets WHERE id = target_ticket_id
      AND app_private.owns_learner(learner_id)
  )
$$;

DO $$
DECLARE
  table_name text;
BEGIN
  FOREACH table_name IN ARRAY ARRAY[
    'identity_projections', 'learner_profiles', 'onboarding_submissions',
    'path_recommendation_runs', 'primary_path_periods', 'course_enrollments',
    'block_progress_facts', 'lesson_progress_facts', 'progress_snapshots',
    'course_completions', 'path_completions', 'assessment_attempts',
    'assessment_answers', 'attempt_files', 'assessment_reviews',
    'assessment_review_scores', 'evidence_records', 'evidence_export_requests',
    'notification_preferences', 'notifications', 'notification_deliveries',
    'community_acceptances', 'support_tickets', 'support_messages',
    'file_objects', 'file_upload_sessions', 'assessment_drafts'
  ]
  LOOP
    EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', table_name);
    EXECUTE format('ALTER TABLE public.%I FORCE ROW LEVEL SECURITY', table_name);
  END LOOP;
END
$$;

CREATE POLICY rls_identity_projections_subject
  ON identity_projections FOR ALL TO s2w_study_app, s2w_study_worker
  USING (identity_subject_id = app_private.current_subject_id())
  WITH CHECK (identity_subject_id = app_private.current_subject_id());
CREATE POLICY rls_learner_profiles_subject
  ON learner_profiles FOR ALL TO s2w_study_app, s2w_study_worker
  USING (identity_subject_id = app_private.current_subject_id())
  WITH CHECK (identity_subject_id = app_private.current_subject_id());
CREATE POLICY rls_onboarding_submissions_subject
  ON onboarding_submissions FOR ALL TO s2w_study_app, s2w_study_worker
  USING (app_private.owns_learner(learner_id))
  WITH CHECK (app_private.owns_learner(learner_id));
CREATE POLICY rls_path_recommendation_runs_subject
  ON path_recommendation_runs FOR ALL TO s2w_study_app, s2w_study_worker
  USING (app_private.owns_learner(learner_id))
  WITH CHECK (app_private.owns_learner(learner_id));
CREATE POLICY rls_primary_path_periods_subject
  ON primary_path_periods FOR ALL TO s2w_study_app, s2w_study_worker
  USING (app_private.owns_learner(learner_id))
  WITH CHECK (app_private.owns_learner(learner_id));
CREATE POLICY rls_course_enrollments_subject
  ON course_enrollments FOR ALL TO s2w_study_app, s2w_study_worker
  USING (app_private.owns_learner(learner_id))
  WITH CHECK (app_private.owns_learner(learner_id));
CREATE POLICY rls_block_progress_facts_subject
  ON block_progress_facts FOR ALL TO s2w_study_app, s2w_study_worker
  USING (app_private.owns_enrollment(enrollment_id))
  WITH CHECK (app_private.owns_enrollment(enrollment_id));
CREATE POLICY rls_lesson_progress_facts_subject
  ON lesson_progress_facts FOR ALL TO s2w_study_app, s2w_study_worker
  USING (app_private.owns_enrollment(enrollment_id))
  WITH CHECK (app_private.owns_enrollment(enrollment_id));
CREATE POLICY rls_progress_snapshots_subject
  ON progress_snapshots FOR ALL TO s2w_study_app, s2w_study_worker
  USING (app_private.owns_learner(learner_id))
  WITH CHECK (app_private.owns_learner(learner_id));
CREATE POLICY rls_course_completions_subject
  ON course_completions FOR ALL TO s2w_study_app, s2w_study_worker
  USING (app_private.owns_learner(learner_id))
  WITH CHECK (app_private.owns_learner(learner_id));
CREATE POLICY rls_path_completions_subject
  ON path_completions FOR ALL TO s2w_study_app, s2w_study_worker
  USING (app_private.owns_learner(learner_id))
  WITH CHECK (app_private.owns_learner(learner_id));
CREATE POLICY rls_assessment_attempts_subject
  ON assessment_attempts FOR ALL TO s2w_study_app, s2w_study_worker
  USING (app_private.owns_learner(learner_id))
  WITH CHECK (app_private.owns_learner(learner_id));
CREATE POLICY rls_assessment_answers_subject
  ON assessment_answers FOR ALL TO s2w_study_app, s2w_study_worker
  USING (app_private.owns_attempt(attempt_id))
  WITH CHECK (app_private.owns_attempt(attempt_id));
CREATE POLICY rls_attempt_files_subject
  ON attempt_files FOR ALL TO s2w_study_app, s2w_study_worker
  USING (app_private.owns_attempt(attempt_id))
  WITH CHECK (app_private.owns_attempt(attempt_id));
CREATE POLICY rls_assessment_reviews_subject_read
  ON assessment_reviews FOR SELECT TO s2w_study_app, s2w_study_worker
  USING (app_private.owns_attempt(attempt_id));
CREATE POLICY rls_assessment_review_scores_subject_read
  ON assessment_review_scores FOR SELECT TO s2w_study_app, s2w_study_worker
  USING (EXISTS (
    SELECT 1 FROM assessment_reviews
     WHERE assessment_reviews.id = review_id
       AND app_private.owns_attempt(assessment_reviews.attempt_id)
  ));
CREATE POLICY rls_evidence_records_subject
  ON evidence_records FOR ALL TO s2w_study_app, s2w_study_worker
  USING (app_private.owns_learner(learner_id))
  WITH CHECK (app_private.owns_learner(learner_id));
CREATE POLICY rls_evidence_export_requests_subject
  ON evidence_export_requests FOR ALL TO s2w_study_app, s2w_study_worker
  USING (learner_identity_subject_id = app_private.current_subject_id())
  WITH CHECK (learner_identity_subject_id = app_private.current_subject_id());
CREATE POLICY rls_notification_preferences_subject
  ON notification_preferences FOR ALL TO s2w_study_app, s2w_study_worker
  USING (app_private.owns_learner(learner_id))
  WITH CHECK (app_private.owns_learner(learner_id));
CREATE POLICY rls_notifications_subject
  ON notifications FOR ALL TO s2w_study_app, s2w_study_worker
  USING (app_private.owns_learner(learner_id))
  WITH CHECK (app_private.owns_learner(learner_id));
CREATE POLICY rls_notification_deliveries_subject
  ON notification_deliveries FOR SELECT TO s2w_study_app, s2w_study_worker
  USING (app_private.owns_notification(notification_id));
CREATE POLICY rls_community_acceptances_subject
  ON community_acceptances FOR ALL TO s2w_study_app, s2w_study_worker
  USING (app_private.owns_learner(learner_id))
  WITH CHECK (app_private.owns_learner(learner_id));
CREATE POLICY rls_support_tickets_subject
  ON support_tickets FOR ALL TO s2w_study_app, s2w_study_worker
  USING (app_private.owns_learner(learner_id))
  WITH CHECK (app_private.owns_learner(learner_id));
CREATE POLICY rls_support_messages_subject
  ON support_messages FOR ALL TO s2w_study_app, s2w_study_worker
  USING (app_private.owns_support_ticket(ticket_id))
  WITH CHECK (app_private.owns_support_ticket(ticket_id));
CREATE POLICY rls_file_objects_subject
  ON file_objects FOR ALL TO s2w_study_app, s2w_study_worker
  USING (owner_subject_id = app_private.current_subject_id())
  WITH CHECK (owner_subject_id = app_private.current_subject_id());
CREATE POLICY rls_file_upload_sessions_subject
  ON file_upload_sessions FOR ALL TO s2w_study_app, s2w_study_worker
  USING (owner_subject_id = app_private.current_subject_id())
  WITH CHECK (owner_subject_id = app_private.current_subject_id());
CREATE POLICY rls_assessment_drafts_subject
  ON assessment_drafts FOR ALL TO s2w_study_app, s2w_study_worker
  USING (app_private.owns_learner(learner_id))
  WITH CHECK (app_private.owns_learner(learner_id));

COMMENT ON SCHEMA app_private IS
  'Study internal helper functions. app.subject_id and app.tenant_id must be SET LOCAL from verified service context.';

DO $$
DECLARE
  table_names text[] := ARRAY[
    'identity_projections', 'learner_profiles', 'service_roles', 'service_permissions',
    'service_role_permissions', 'service_role_assignments', 'onboarding_submissions',
    'path_recommendation_runs', 'learning_paths', 'learning_path_versions', 'courses',
    'course_versions', 'path_course_items', 'chapters', 'lessons', 'content_blocks',
    'content_rights_attestations', 'content_review_decisions', 'trusted_publisher_grants',
    'assessments', 'assessment_placements', 'quiz_questions', 'quiz_options', 'rubrics',
    'rubric_criteria', 'primary_path_periods', 'course_enrollments',
    'block_progress_facts', 'lesson_progress_facts', 'progress_snapshots',
    'course_completions', 'path_completions', 'assessment_attempts', 'assessment_answers',
    'file_objects', 'malware_scan_results', 'attempt_files', 'assessment_reviews',
    'assessment_review_scores', 'evidence_records', 'evidence_export_requests',
    'notification_preferences', 'notifications', 'notification_deliveries',
    'community_channels', 'community_acceptances', 'support_tickets', 'support_messages',
    'admin_adjustments', 'audit_events', 'idempotency_keys', 'outbox_events',
    'consumer_inbox', 'report_snapshots', 'outbox_delivery_attempts', 'study_skills',
    'course_skill_outcomes', 'course_prerequisites', 'file_upload_sessions',
    'assessment_drafts'
  ];
  table_name text;
  table_number integer := 0;
BEGIN
  FOREACH table_name IN ARRAY table_names LOOP
    table_number := table_number + 1;
    EXECUTE format(
      'COMMENT ON TABLE public.%I IS %L',
      table_name,
      'TBL-STU-' || lpad(table_number::text, 3, '0') || ' — Study service V1-PILOT'
    );
  END LOOP;
END
$$;

REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA app_private FROM PUBLIC;
GRANT USAGE ON SCHEMA public, app_private TO s2w_study_app, s2w_study_worker, s2w_study_readonly;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO s2w_study_app, s2w_study_worker;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO s2w_study_readonly;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO s2w_study_app, s2w_study_worker, s2w_study_readonly;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA app_private TO s2w_study_app, s2w_study_worker, s2w_study_readonly;

ALTER DEFAULT PRIVILEGES FOR ROLE s2w_study_owner IN SCHEMA public
  REVOKE ALL ON TABLES FROM PUBLIC;
ALTER DEFAULT PRIVILEGES FOR ROLE s2w_study_owner IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO s2w_study_app, s2w_study_worker;
ALTER DEFAULT PRIVILEGES FOR ROLE s2w_study_owner IN SCHEMA public
  GRANT SELECT ON TABLES TO s2w_study_readonly;
ALTER DEFAULT PRIVILEGES FOR ROLE s2w_study_owner IN SCHEMA app_private
  REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;
ALTER DEFAULT PRIVILEGES FOR ROLE s2w_study_owner IN SCHEMA app_private
  GRANT EXECUTE ON FUNCTIONS TO s2w_study_app, s2w_study_worker, s2w_study_readonly;

COMMIT;
