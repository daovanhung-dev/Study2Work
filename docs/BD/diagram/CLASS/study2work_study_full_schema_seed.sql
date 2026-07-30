-- ============================================================================
-- Study2Work - Study Module: Full Schema, Authentication and Seed Data
-- PostgreSQL DDL rebuilt from the business class diagram.
-- Target: PostgreSQL 15+
-- WARNING: Development/demo script. It drops schema study_dev0 and recreates it.
-- Demo passwords are listed in the SEED DATA section; never reuse them in production.
-- ============================================================================

-- Clear a failed transaction left open by a previous execution in the VS Code client.
-- PostgreSQL may emit only a harmless warning when no transaction is active.
ROLLBACK;

BEGIN;

-- PostgreSQL 15+ provides gen_random_uuid() directly.
-- Do not create pgcrypto here because some VS Code clients execute statements
-- independently and may report: "no schema has been selected to create in".

-- Rebuild the development schema so this DDL can be executed repeatedly.
-- WARNING: CASCADE removes all existing objects and data inside study_dev0.
DROP SCHEMA IF EXISTS study_dev0 CASCADE;
CREATE SCHEMA study_dev0 AUTHORIZATION CURRENT_USER;

-- Restrict the search path to this transaction.
SET LOCAL search_path TO study_dev0, public;

-- --------------------------------------------------------------------------
-- ENUM TYPES
-- Values explicitly present in the class diagram are preserved.
-- Values for the remaining business enums are inferred for implementation.
-- --------------------------------------------------------------------------

CREATE TYPE account_status AS ENUM (
    'REGISTERED_PENDING_VERIFICATION',
    'VERIFIED',
    'ONBOARDING_IN_PROGRESS',
    'READY_TO_LEARN',
    'ACTIVE',
    'SUSPENDED'
);

CREATE TYPE programming_level AS ENUM (
    'BEGINNER',
    'BASIC',
    'INTERMEDIATE',
    'ADVANCED'
);

CREATE TYPE onboarding_status AS ENUM (
    'NOT_STARTED',
    'IN_PROGRESS',
    'COMPLETED'
);

CREATE TYPE role_scope AS ENUM (
    'SYSTEM',
    'STUDY',
    'CONTENT',
    'LEARNER_SUPPORT',
    'COMMUNITY',
    'REPORTING'
);

CREATE TYPE difficulty_level AS ENUM (
    'BEGINNER',
    'INTERMEDIATE',
    'ADVANCED'
);

CREATE TYPE publish_status AS ENUM (
    'DRAFT',
    'IN_REVIEW',
    'PUBLISHED',
    'UPDATED',
    'ARCHIVED'
);

CREATE TYPE unlock_mode AS ENUM (
    'SEQUENTIAL',
    'FREE',
    'ADMIN_ONLY'
);

CREATE TYPE enrollment_status AS ENUM (
    'NOT_STARTED',
    'ACTIVE',
    'COMPLETED',
    'CANCELLED_BY_ADMIN',
    'RESET_BY_ADMIN'
);

CREATE TYPE course_enrollment_status AS ENUM (
    'NOT_STARTED',
    'ACTIVE',
    'COMPLETED',
    'CANCELLED'
);

CREATE TYPE unlock_condition AS ENUM (
    'ALWAYS',
    'PREVIOUS_CHAPTER_COMPLETED',
    'REQUIRED_ITEMS_COMPLETED',
    'MANUAL'
);

CREATE TYPE completion_condition AS ENUM (
    'VIEW_CONTENT',
    'VIDEO_PERCENT',
    'REQUIRED_MATERIALS_READ',
    'SELF_MARKED_DONE',
    'REQUIRED_EXERCISE_PASSED',
    'ALL_REQUIRED_CONDITIONS'
);

CREATE TYPE material_type AS ENUM (
    'VIDEO',
    'PDF',
    'SLIDE',
    'MARKDOWN',
    'LINK',
    'CODE',
    'FILE'
);

CREATE TYPE usage_right_status AS ENUM (
    'OWNED',
    'LICENSED',
    'PUBLIC_DOMAIN',
    'PERMISSION_GRANTED',
    'RESTRICTED',
    'UNKNOWN'
);

CREATE TYPE exercise_type AS ENUM (
    'QUIZ',
    'CODING',
    'ESSAY',
    'FILE_UPLOAD',
    'LINK_SUBMISSION',
    'PROJECT'
);

CREATE TYPE submission_status AS ENUM (
    'NOT_STARTED',
    'DRAFT',
    'SUBMITTED',
    'UNDER_REVIEW',
    'PASSED',
    'NEEDS_REVISION',
    'FAILED'
);

CREATE TYPE progress_status AS ENUM (
    'NOT_STARTED',
    'IN_PROGRESS',
    'COMPLETED',
    'BLOCKED'
);

CREATE TYPE notification_type AS ENUM (
    'LEARNING_REMINDER',
    'MANDATORY_NOTICE',
    'SECURITY',
    'ASSIGNMENT',
    'REVIEW_RESULT',
    'CONTENT_UPDATE',
    'COMMUNITY',
    'SYSTEM',
    'ADMIN_MANUAL'
);

CREATE TYPE notification_priority AS ENUM (
    'LOW',
    'NORMAL',
    'HIGH',
    'URGENT'
);

CREATE TYPE read_status AS ENUM (
    'UNREAD',
    'READ',
    'HIDDEN'
);

CREATE TYPE community_scope_type AS ENUM (
    'GLOBAL',
    'LEARNING_PATH',
    'COURSE',
    'TOPIC'
);

CREATE TYPE community_status AS ENUM (
    'ACTIVE',
    'PAUSED',
    'FULL',
    'ARCHIVED'
);

CREATE TYPE support_request_type AS ENUM (
    'CHANGE_PATH',
    'RESET_PATH',
    'CANCEL_PATH',
    'PROGRESS_RESET',
    'OTHER'
);

CREATE TYPE support_request_status AS ENUM (
    'OPEN',
    'IN_REVIEW',
    'APPROVED',
    'REJECTED',
    'RESOLVED',
    'CANCELLED'
);

CREATE TYPE audit_action AS ENUM (
    'CREATE',
    'UPDATE',
    'DELETE',
    'PUBLISH',
    'ARCHIVE',
    'ASSIGN_ROLE',
    'REVOKE_ROLE',
    'SUSPEND_ACCOUNT',
    'UNSUSPEND_ACCOUNT',
    'ACTIVATE_PATH',
    'CANCEL_PATH',
    'TRANSFER_PATH',
    'RESET_PROGRESS',
    'SEND_NOTIFICATION',
    'REVIEW_SUBMISSION',
    'OTHER'
);

-- --------------------------------------------------------------------------
-- CORE ACCOUNT AND RBAC
-- --------------------------------------------------------------------------

CREATE TABLE users (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    display_name        VARCHAR(150) NOT NULL,
    email               VARCHAR(320),
    phone               VARCHAR(30),
    account_status      account_status NOT NULL DEFAULT 'REGISTERED_PENDING_VERIFICATION',
    contact_verified    BOOLEAN NOT NULL DEFAULT FALSE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ck_users_contact_required CHECK (email IS NOT NULL OR phone IS NOT NULL)
);

CREATE UNIQUE INDEX uq_users_email_ci
    ON users (LOWER(email))
    WHERE email IS NOT NULL;

CREATE UNIQUE INDEX uq_users_phone
    ON users (phone)
    WHERE phone IS NOT NULL;


CREATE TABLE auth_credentials (
    id                          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                     UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    password_hash               TEXT NOT NULL,
    password_algorithm          VARCHAR(30) NOT NULL DEFAULT 'ARGON2ID',
    password_login_enabled      BOOLEAN NOT NULL DEFAULT TRUE,
    must_change_password        BOOLEAN NOT NULL DEFAULT FALSE,
    failed_login_attempts       INTEGER NOT NULL DEFAULT 0,
    locked_until                TIMESTAMPTZ,
    password_changed_at         TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login_at               TIMESTAMPTZ,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at                  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ck_auth_credentials_hash_length CHECK (char_length(password_hash) >= 50),
    CONSTRAINT ck_auth_credentials_algorithm CHECK (
        password_algorithm IN ('ARGON2ID', 'BCRYPT')
    ),
    CONSTRAINT ck_auth_credentials_failed_attempts CHECK (failed_login_attempts >= 0),
    CONSTRAINT ck_auth_credentials_lock_state CHECK (
        locked_until IS NULL OR failed_login_attempts > 0
    )
);

CREATE INDEX ix_auth_credentials_locked_until
    ON auth_credentials (locked_until)
    WHERE locked_until IS NOT NULL;

CREATE TABLE user_profiles (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                 UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    avatar_url              TEXT,
    city                    VARCHAR(150),
    school_or_company       VARCHAR(255),
    current_major_or_job    VARCHAR(255),
    learning_goal           TEXT,
    known_technologies      TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
    weekly_study_hours      INTEGER,
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ck_user_profiles_weekly_hours CHECK (
        weekly_study_hours IS NULL OR weekly_study_hours BETWEEN 0 AND 168
    )
);

CREATE TABLE roles (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code        VARCHAR(80) NOT NULL UNIQUE,
    name        VARCHAR(150) NOT NULL,
    scope       role_scope NOT NULL,
    active      BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE user_roles (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_id         UUID NOT NULL REFERENCES roles(id) ON DELETE RESTRICT,
    assigned_at     TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_user_roles_user_role UNIQUE (user_id, role_id)
);

-- --------------------------------------------------------------------------
-- LEARNING PATHS AND COURSES
-- --------------------------------------------------------------------------

CREATE TABLE learning_paths (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug                VARCHAR(180) NOT NULL UNIQUE,
    title               VARCHAR(255) NOT NULL,
    summary             TEXT,
    description         TEXT,
    level               difficulty_level NOT NULL,
    estimated_hours     INTEGER NOT NULL DEFAULT 0,
    publish_status      publish_status NOT NULL DEFAULT 'DRAFT',
    unlock_mode         unlock_mode NOT NULL DEFAULT 'SEQUENTIAL',
    published_at        TIMESTAMPTZ,
    CONSTRAINT ck_learning_paths_estimated_hours CHECK (estimated_hours >= 0),
    CONSTRAINT ck_learning_paths_published_at CHECK (
        publish_status NOT IN ('PUBLISHED', 'UPDATED') OR published_at IS NOT NULL
    )
);

CREATE TABLE onboarding_records (
    id                          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                     UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    programming_level           programming_level,
    known_technologies          TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
    main_goal                   TEXT,
    sub_goals                   TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
    weekly_study_hours          INTEGER,
    selected_learning_path_id   UUID REFERENCES learning_paths(id) ON DELETE SET NULL,
    status                      onboarding_status NOT NULL DEFAULT 'NOT_STARTED',
    current_step                INTEGER NOT NULL DEFAULT 0,
    confirmed_at                TIMESTAMPTZ,
    CONSTRAINT ck_onboarding_weekly_hours CHECK (
        weekly_study_hours IS NULL OR weekly_study_hours BETWEEN 0 AND 168
    ),
    CONSTRAINT ck_onboarding_current_step CHECK (current_step >= 0),
    CONSTRAINT ck_onboarding_confirmed_at CHECK (
        status <> 'COMPLETED' OR confirmed_at IS NOT NULL
    )
);

CREATE TABLE courses (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug                VARCHAR(180) NOT NULL UNIQUE,
    title               VARCHAR(255) NOT NULL,
    summary             TEXT,
    level               difficulty_level NOT NULL,
    estimated_minutes   INTEGER NOT NULL DEFAULT 0,
    publish_status      publish_status NOT NULL DEFAULT 'DRAFT',
    published_at        TIMESTAMPTZ,
    CONSTRAINT ck_courses_estimated_minutes CHECK (estimated_minutes >= 0),
    CONSTRAINT ck_courses_published_at CHECK (
        publish_status NOT IN ('PUBLISHED', 'UPDATED') OR published_at IS NOT NULL
    )
);

CREATE TABLE learning_path_courses (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learning_path_id    UUID NOT NULL REFERENCES learning_paths(id) ON DELETE CASCADE,
    course_id           UUID NOT NULL REFERENCES courses(id) ON DELETE RESTRICT,
    order_index         INTEGER NOT NULL,
    required            BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT ck_learning_path_courses_order CHECK (order_index >= 0),
    CONSTRAINT uq_learning_path_courses_pair UNIQUE (learning_path_id, course_id),
    CONSTRAINT uq_learning_path_courses_order UNIQUE (learning_path_id, order_index)
);

CREATE TABLE learning_path_enrollments (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    learning_path_id    UUID NOT NULL REFERENCES learning_paths(id) ON DELETE RESTRICT,
    status              enrollment_status NOT NULL DEFAULT 'NOT_STARTED',
    progress_percent    NUMERIC(5,2) NOT NULL DEFAULT 0,
    started_at          TIMESTAMPTZ,
    completed_at        TIMESTAMPTZ,
    admin_reason        TEXT,
    CONSTRAINT ck_path_enrollments_progress CHECK (progress_percent BETWEEN 0 AND 100),
    CONSTRAINT ck_path_enrollments_started_at CHECK (
        status = 'NOT_STARTED' OR started_at IS NOT NULL
    ),
    CONSTRAINT ck_path_enrollments_completed_at CHECK (
        status <> 'COMPLETED' OR completed_at IS NOT NULL
    )
);

-- Business rule: a learner may have at most one ACTIVE learning path.
CREATE UNIQUE INDEX uq_path_enrollments_one_active_per_user
    ON learning_path_enrollments (user_id)
    WHERE status = 'ACTIVE';

CREATE INDEX ix_path_enrollments_user_history
    ON learning_path_enrollments (user_id, started_at DESC);

CREATE INDEX ix_path_enrollments_path_status
    ON learning_path_enrollments (learning_path_id, status);

CREATE TABLE course_enrollments (
    id                              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    course_id                       UUID NOT NULL REFERENCES courses(id) ON DELETE RESTRICT,
    learning_path_enrollment_id     UUID REFERENCES learning_path_enrollments(id) ON DELETE SET NULL,
    status                          course_enrollment_status NOT NULL DEFAULT 'NOT_STARTED',
    progress_percent                NUMERIC(5,2) NOT NULL DEFAULT 0,
    started_at                      TIMESTAMPTZ,
    completed_at                    TIMESTAMPTZ,
    CONSTRAINT ck_course_enrollments_progress CHECK (progress_percent BETWEEN 0 AND 100),
    CONSTRAINT ck_course_enrollments_started_at CHECK (
        status = 'NOT_STARTED' OR started_at IS NOT NULL
    ),
    CONSTRAINT ck_course_enrollments_completed_at CHECK (
        status <> 'COMPLETED' OR completed_at IS NOT NULL
    ),
    CONSTRAINT uq_course_enrollment_context UNIQUE (
        user_id,
        course_id,
        learning_path_enrollment_id
    )
);

CREATE INDEX ix_course_enrollments_user_status
    ON course_enrollments (user_id, status);

-- --------------------------------------------------------------------------
-- CURRICULUM, MATERIALS, EXERCISES AND PROGRESS
-- --------------------------------------------------------------------------

CREATE TABLE chapters (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id           UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    title               VARCHAR(255) NOT NULL,
    objective           TEXT,
    order_index         INTEGER NOT NULL,
    required            BOOLEAN NOT NULL DEFAULT TRUE,
    unlock_condition    unlock_condition NOT NULL DEFAULT 'ALWAYS',
    CONSTRAINT ck_chapters_order CHECK (order_index >= 0),
    CONSTRAINT uq_chapters_course_order UNIQUE (course_id, order_index)
);

CREATE TABLE lessons (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chapter_id              UUID NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    title                   VARCHAR(255) NOT NULL,
    objective               TEXT,
    order_index             INTEGER NOT NULL,
    sample_public           BOOLEAN NOT NULL DEFAULT FALSE,
    required                BOOLEAN NOT NULL DEFAULT TRUE,
    completion_condition    completion_condition NOT NULL DEFAULT 'ALL_REQUIRED_CONDITIONS',
    publish_status          publish_status NOT NULL DEFAULT 'DRAFT',
    CONSTRAINT ck_lessons_order CHECK (order_index >= 0),
    CONSTRAINT uq_lessons_chapter_order UNIQUE (chapter_id, order_index)
);

CREATE TABLE course_materials (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lesson_id           UUID NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    title               VARCHAR(255) NOT NULL,
    type                material_type NOT NULL,
    resource_url        TEXT NOT NULL,
    required            BOOLEAN NOT NULL DEFAULT FALSE,
    source              TEXT,
    usage_right_status  usage_right_status NOT NULL DEFAULT 'UNKNOWN'
);

CREATE INDEX ix_course_materials_lesson_required
    ON course_materials (lesson_id, required);

CREATE TABLE exercises (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id           UUID REFERENCES courses(id) ON DELETE CASCADE,
    chapter_id          UUID REFERENCES chapters(id) ON DELETE CASCADE,
    lesson_id           UUID REFERENCES lessons(id) ON DELETE CASCADE,
    title               VARCHAR(255) NOT NULL,
    type                exercise_type NOT NULL,
    required            BOOLEAN NOT NULL DEFAULT TRUE,
    due_at              TIMESTAMPTZ,
    allow_resubmit      BOOLEAN NOT NULL DEFAULT FALSE,
    max_score           INTEGER NOT NULL DEFAULT 100,
    rubric              TEXT,
    publish_status      publish_status NOT NULL DEFAULT 'DRAFT',
    CONSTRAINT ck_exercises_scope CHECK (num_nonnulls(course_id, chapter_id, lesson_id) >= 1),
    CONSTRAINT ck_exercises_max_score CHECK (max_score > 0)
);

CREATE INDEX ix_exercises_course ON exercises (course_id) WHERE course_id IS NOT NULL;
CREATE INDEX ix_exercises_chapter ON exercises (chapter_id) WHERE chapter_id IS NOT NULL;
CREATE INDEX ix_exercises_lesson ON exercises (lesson_id) WHERE lesson_id IS NOT NULL;
CREATE INDEX ix_exercises_due_at ON exercises (due_at) WHERE due_at IS NOT NULL;

CREATE TABLE exercise_submissions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exercise_id     UUID NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status          submission_status NOT NULL DEFAULT 'NOT_STARTED',
    attempt_no      INTEGER NOT NULL DEFAULT 1,
    text_answer     TEXT,
    file_url        TEXT,
    link_url        TEXT,
    score           INTEGER,
    feedback        TEXT,
    submitted_at    TIMESTAMPTZ,
    reviewed_at     TIMESTAMPTZ,
    CONSTRAINT ck_exercise_submissions_attempt CHECK (attempt_no >= 1),
    CONSTRAINT ck_exercise_submissions_score CHECK (score IS NULL OR score >= 0),
    CONSTRAINT ck_exercise_submissions_submitted_at CHECK (
        status IN ('NOT_STARTED', 'DRAFT') OR submitted_at IS NOT NULL
    ),
    CONSTRAINT ck_exercise_submissions_reviewed_at CHECK (
        status NOT IN ('PASSED', 'NEEDS_REVISION', 'FAILED') OR reviewed_at IS NOT NULL
    ),
    CONSTRAINT uq_exercise_submission_attempt UNIQUE (exercise_id, user_id, attempt_no)
);

CREATE INDEX ix_exercise_submissions_user_status
    ON exercise_submissions (user_id, status);

CREATE INDEX ix_exercise_submissions_review_queue
    ON exercise_submissions (status, submitted_at)
    WHERE status = 'UNDER_REVIEW';

CREATE TABLE lesson_progress (
    id                          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    lesson_id                   UUID NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    status                      progress_status NOT NULL DEFAULT 'NOT_STARTED',
    video_watch_percent         NUMERIC(5,2) NOT NULL DEFAULT 0,
    required_materials_read     BOOLEAN NOT NULL DEFAULT FALSE,
    self_marked_done            BOOLEAN NOT NULL DEFAULT FALSE,
    required_exercise_passed    BOOLEAN NOT NULL DEFAULT FALSE,
    last_accessed_at            TIMESTAMPTZ,
    completed_at                TIMESTAMPTZ,
    CONSTRAINT ck_lesson_progress_video CHECK (video_watch_percent BETWEEN 0 AND 100),
    CONSTRAINT ck_lesson_progress_completed_at CHECK (
        status <> 'COMPLETED' OR completed_at IS NOT NULL
    ),
    CONSTRAINT uq_lesson_progress_user_lesson UNIQUE (user_id, lesson_id)
);

CREATE INDEX ix_lesson_progress_user_status
    ON lesson_progress (user_id, status);

CREATE TABLE completion_rules (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    target_type             VARCHAR(40) NOT NULL,
    target_id               UUID NOT NULL,
    required_items_only     BOOLEAN NOT NULL DEFAULT TRUE,
    minimum_score           INTEGER,
    minimum_video_percent   NUMERIC(5,2),
    description             TEXT,
    CONSTRAINT ck_completion_rules_target_type CHECK (
        target_type IN ('LEARNING_PATH', 'COURSE')
    ),
    CONSTRAINT ck_completion_rules_minimum_score CHECK (
        minimum_score IS NULL OR minimum_score >= 0
    ),
    CONSTRAINT ck_completion_rules_video_percent CHECK (
        minimum_video_percent IS NULL OR minimum_video_percent BETWEEN 0 AND 100
    )
);

CREATE INDEX ix_completion_rules_target
    ON completion_rules (target_type, target_id);

-- --------------------------------------------------------------------------
-- NOTIFICATIONS
-- --------------------------------------------------------------------------

CREATE TABLE notification_settings (
    id                                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                             UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    optional_reminder_enabled           BOOLEAN NOT NULL DEFAULT TRUE,
    email_learning_reminder_enabled     BOOLEAN NOT NULL DEFAULT TRUE,
    mandatory_notice_enabled            BOOLEAN NOT NULL DEFAULT TRUE,
    updated_at                          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ck_notification_settings_mandatory CHECK (mandatory_notice_enabled = TRUE)
);

CREATE TABLE notifications (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type            notification_type NOT NULL,
    title           VARCHAR(255) NOT NULL,
    body            TEXT NOT NULL,
    priority        notification_priority NOT NULL DEFAULT 'NORMAL',
    read_status     read_status NOT NULL DEFAULT 'UNREAD',
    action_url      TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    read_at         TIMESTAMPTZ,
    CONSTRAINT ck_notifications_read_at CHECK (
        read_status <> 'READ' OR read_at IS NOT NULL
    )
);

CREATE INDEX ix_notifications_user_unread
    ON notifications (user_id, created_at DESC)
    WHERE read_status = 'UNREAD';

CREATE INDEX ix_notifications_user_created
    ON notifications (user_id, created_at DESC);

-- --------------------------------------------------------------------------
-- COMMUNITY
-- --------------------------------------------------------------------------

CREATE TABLE community_groups (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(255) NOT NULL,
    scope_type      community_scope_type NOT NULL,
    scope_id        UUID,
    join_link       TEXT NOT NULL,
    status          community_status NOT NULL DEFAULT 'ACTIVE',
    rules           TEXT,
    moderator_id    UUID REFERENCES users(id) ON DELETE SET NULL,
    CONSTRAINT ck_community_groups_scope CHECK (
        (scope_type = 'GLOBAL' AND scope_id IS NULL)
        OR
        (scope_type <> 'GLOBAL' AND scope_id IS NOT NULL)
    )
);

CREATE INDEX ix_community_groups_scope
    ON community_groups (scope_type, scope_id, status);

CREATE TABLE community_join_events (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                 UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    community_group_id      UUID NOT NULL REFERENCES community_groups(id) ON DELETE CASCADE,
    confirmed_rules         BOOLEAN NOT NULL,
    source_screen           VARCHAR(255),
    opened_at               TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ck_community_join_events_rules CHECK (confirmed_rules = TRUE)
);

CREATE INDEX ix_community_join_events_group_opened
    ON community_join_events (community_group_id, opened_at DESC);

CREATE INDEX ix_community_join_events_user_opened
    ON community_join_events (user_id, opened_at DESC);

-- --------------------------------------------------------------------------
-- SUPPORT REQUESTS AND AUDIT
-- --------------------------------------------------------------------------

CREATE TABLE support_requests (
    id                                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                             UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type                                support_request_type NOT NULL,
    reason                              TEXT NOT NULL,
    current_learning_path_id            UUID REFERENCES learning_paths(id) ON DELETE SET NULL,
    target_learning_path_id             UUID REFERENCES learning_paths(id) ON DELETE SET NULL,
    current_learning_path_enrollment_id UUID REFERENCES learning_path_enrollments(id) ON DELETE SET NULL,
    status                              support_request_status NOT NULL DEFAULT 'OPEN',
    admin_decision                      TEXT,
    resolved_at                         TIMESTAMPTZ,
    CONSTRAINT ck_support_requests_target_diff CHECK (
        target_learning_path_id IS NULL
        OR current_learning_path_id IS NULL
        OR target_learning_path_id <> current_learning_path_id
    ),
    CONSTRAINT ck_support_requests_resolved_at CHECK (
        status NOT IN ('APPROVED', 'REJECTED', 'RESOLVED', 'CANCELLED')
        OR resolved_at IS NOT NULL
    )
);

CREATE INDEX ix_support_requests_queue
    ON support_requests (status, id)
    WHERE status IN ('OPEN', 'IN_REVIEW');

CREATE INDEX ix_support_requests_user
    ON support_requests (user_id, status);

CREATE TABLE audit_logs (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    actor_id            UUID REFERENCES users(id) ON DELETE SET NULL,
    actor_role          VARCHAR(100),
    action              audit_action NOT NULL,
    target_type         VARCHAR(100) NOT NULL,
    target_id           UUID,
    support_request_id  UUID REFERENCES support_requests(id) ON DELETE SET NULL,
    before_value        JSONB,
    after_value         JSONB,
    reason              TEXT,
    channel             VARCHAR(100) NOT NULL DEFAULT 'API',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ck_audit_logs_change_snapshot CHECK (
        before_value IS NOT NULL OR after_value IS NOT NULL OR action IN (
            'ASSIGN_ROLE',
            'REVOKE_ROLE',
            'SUSPEND_ACCOUNT',
            'UNSUSPEND_ACCOUNT',
            'ACTIVATE_PATH',
            'CANCEL_PATH',
            'TRANSFER_PATH',
            'RESET_PROGRESS',
            'SEND_NOTIFICATION',
            'REVIEW_SUBMISSION',
            'OTHER'
        )
    )
);

CREATE INDEX ix_audit_logs_target
    ON audit_logs (target_type, target_id, created_at DESC);

CREATE INDEX ix_audit_logs_actor
    ON audit_logs (actor_id, created_at DESC);

CREATE INDEX ix_audit_logs_support_request
    ON audit_logs (support_request_id, created_at DESC)
    WHERE support_request_id IS NOT NULL;

CREATE INDEX ix_audit_logs_created_at
    ON audit_logs (created_at DESC);

-- --------------------------------------------------------------------------
-- UPDATED_AT TRIGGER
-- --------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_users_set_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


CREATE TRIGGER trg_auth_credentials_set_updated_at
BEFORE UPDATE ON auth_credentials
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_user_profiles_set_updated_at
BEFORE UPDATE ON user_profiles
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_notification_settings_set_updated_at
BEFORE UPDATE ON notification_settings
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

-- --------------------------------------------------------------------------
-- TABLE COMMENTS
-- --------------------------------------------------------------------------

COMMENT ON SCHEMA study_dev0 IS 'Study2Work Study module business schema.';
COMMENT ON TABLE users IS 'Learner/admin account identity and lifecycle status.';
COMMENT ON TABLE auth_credentials IS 'Password authentication state; stores only password hashes, never plaintext passwords.';
COMMENT ON TABLE user_profiles IS 'Extended learner profile and learning preferences.';
COMMENT ON TABLE onboarding_records IS 'Latest onboarding state and selected learning path.';
COMMENT ON TABLE roles IS 'Business roles used by Study module RBAC.';
COMMENT ON TABLE user_roles IS 'Many-to-many assignment between users and roles.';
COMMENT ON TABLE learning_paths IS 'Published or draft learning paths.';
COMMENT ON TABLE learning_path_courses IS 'Ordered course composition of each learning path.';
COMMENT ON TABLE learning_path_enrollments IS 'Historical learner enrollments in learning paths.';
COMMENT ON TABLE courses IS 'Course catalog entity.';
COMMENT ON TABLE course_enrollments IS 'Course progress within a learning path enrollment.';
COMMENT ON TABLE chapters IS 'Ordered course chapters.';
COMMENT ON TABLE lessons IS 'Ordered lessons inside chapters.';
COMMENT ON TABLE course_materials IS 'Lesson materials; course relation is derived through lesson -> chapter -> course.';
COMMENT ON TABLE exercises IS 'Assignments linked to course, chapter, lesson, or a combination of scopes.';
COMMENT ON TABLE exercise_submissions IS 'Immutable attempt history for learner submissions.';
COMMENT ON TABLE lesson_progress IS 'System-calculated learner progress for each lesson.';
COMMENT ON TABLE completion_rules IS 'Polymorphic completion rules for learning paths and courses.';
COMMENT ON TABLE notifications IS 'In-app notifications for learners.';
COMMENT ON TABLE notification_settings IS 'Learner notification preferences; mandatory notices cannot be disabled.';
COMMENT ON TABLE community_groups IS 'External community groups such as Zalo groups.';
COMMENT ON TABLE community_join_events IS 'Tracks opening a community link, not confirmed group membership.';
COMMENT ON TABLE support_requests IS 'Learner requests for path change, reset, cancellation, or exceptions.';
COMMENT ON TABLE audit_logs IS 'Administrative and high-risk business operation audit trail.';


-- ============================================================================
-- DEVELOPMENT SEED DATA
-- ============================================================================
-- Demo login accounts. Passwords are for local development only:
--   admin@study2work.local      / Admin@123
--   content@study2work.local    / Content@123
--   support@study2work.local    / Support@123
--   moderator@study2work.local  / Moderator@123
--   hung@example.com            / Learner@123
--   lan@example.com             / Learner2@123
--   minh@example.com            / Pending@123
-- Hashes below use Argon2id: m=65536 KiB, t=3, p=4.

-- --------------------------------------------------------------------------
-- Users and authentication
-- --------------------------------------------------------------------------

INSERT INTO users (
    id, display_name, email, phone, account_status, contact_verified, created_at, updated_at
) VALUES
    ('00000000-0000-0000-0000-000000000001', 'System Admin', 'admin@study2work.local', '0900000001', 'ACTIVE', TRUE, '2026-06-01 08:00:00+07', '2026-07-20 08:00:00+07'),
    ('00000000-0000-0000-0000-000000000002', 'Content Manager', 'content@study2work.local', '0900000002', 'ACTIVE', TRUE, '2026-06-01 08:05:00+07', '2026-07-20 08:05:00+07'),
    ('00000000-0000-0000-0000-000000000003', 'Learner Support', 'support@study2work.local', '0900000003', 'ACTIVE', TRUE, '2026-06-01 08:10:00+07', '2026-07-20 08:10:00+07'),
    ('00000000-0000-0000-0000-000000000004', 'Community Moderator', 'moderator@study2work.local', '0900000004', 'ACTIVE', TRUE, '2026-06-01 08:15:00+07', '2026-07-20 08:15:00+07'),
    ('00000000-0000-0000-0000-000000000101', 'Đào Văn Hùng', 'hung@example.com', '0911000101', 'ACTIVE', TRUE, '2026-07-01 09:00:00+07', '2026-07-25 21:00:00+07'),
    ('00000000-0000-0000-0000-000000000102', 'Nguyễn Thị Lan', 'lan@example.com', '0911000102', 'ACTIVE', TRUE, '2026-06-20 10:00:00+07', '2026-07-22 19:30:00+07'),
    ('00000000-0000-0000-0000-000000000103', 'Trần Minh', 'minh@example.com', '0911000103', 'ONBOARDING_IN_PROGRESS', TRUE, '2026-07-24 14:00:00+07', '2026-07-26 14:30:00+07');

INSERT INTO auth_credentials (
    id, user_id, password_hash, password_algorithm, password_login_enabled,
    must_change_password, failed_login_attempts, locked_until,
    password_changed_at, last_login_at, created_at, updated_at
) VALUES
    ('10000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001', '$argon2id$v=19$m=65536,t=3,p=4$gPNNdB5AfwwoA0EZRi31zw$Xf7vQJnirHnEGTZvs2+JrZvuEi4V52oj0RbQYbPBds4', 'ARGON2ID', TRUE, FALSE, 0, NULL, '2026-07-01 08:00:00+07', '2026-07-27 19:40:00+07', '2026-06-01 08:00:00+07', '2026-07-27 19:40:00+07'),
    ('10000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000002', '$argon2id$v=19$m=65536,t=3,p=4$wirul1+aA9hcIV5Ay7fY7w$vdKGgvT1FFUS6oFGYQj6h5tnbCiY/UgSSHbMKv4P3Po', 'ARGON2ID', TRUE, FALSE, 0, NULL, '2026-07-01 08:05:00+07', '2026-07-26 15:20:00+07', '2026-06-01 08:05:00+07', '2026-07-26 15:20:00+07'),
    ('10000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000003', '$argon2id$v=19$m=65536,t=3,p=4$jWPXCK37++Hy0XtYXjgjmw$VyklEQb1dXesD1GafeLI+H/INMMVPbhdLqOnontO7MA', 'ARGON2ID', TRUE, FALSE, 0, NULL, '2026-07-01 08:10:00+07', '2026-07-27 09:10:00+07', '2026-06-01 08:10:00+07', '2026-07-27 09:10:00+07'),
    ('10000000-0000-0000-0000-000000000004', '00000000-0000-0000-0000-000000000004', '$argon2id$v=19$m=65536,t=3,p=4$cO7w6MGRjN5+GrstqJ7dRQ$AHpA4ik+7vWnGPl3Nyc48YRPTDhRDmmqlQ0UvEPwjm4', 'ARGON2ID', TRUE, FALSE, 0, NULL, '2026-07-01 08:15:00+07', '2026-07-25 20:00:00+07', '2026-06-01 08:15:00+07', '2026-07-25 20:00:00+07'),
    ('10000000-0000-0000-0000-000000000101', '00000000-0000-0000-0000-000000000101', '$argon2id$v=19$m=65536,t=3,p=4$ioJyH/U+AzHNZv8HLC0fRA$5TfoTioOR6DAGaqDYtS1+etdCn6GqipTNpcVeHNbedA', 'ARGON2ID', TRUE, FALSE, 0, NULL, '2026-07-01 09:05:00+07', '2026-07-27 20:10:00+07', '2026-07-01 09:05:00+07', '2026-07-27 20:10:00+07'),
    ('10000000-0000-0000-0000-000000000102', '00000000-0000-0000-0000-000000000102', '$argon2id$v=19$m=65536,t=3,p=4$Ddo8owBWggfdV5QFVJUyIg$t4jhh09FjJHd0I80TzEo8KvSCJ38fYNU2OB0q2Mjcm4', 'ARGON2ID', TRUE, FALSE, 0, NULL, '2026-06-20 10:05:00+07', '2026-07-26 21:00:00+07', '2026-06-20 10:05:00+07', '2026-07-26 21:00:00+07'),
    ('10000000-0000-0000-0000-000000000103', '00000000-0000-0000-0000-000000000103', '$argon2id$v=19$m=65536,t=3,p=4$v86q2d45mv5yDHU3QIqpuw$wa1SUsaT/Co4MBmzs+KGbLl3iXNEKnQbuI/OV/oCGJA', 'ARGON2ID', TRUE, TRUE, 2, '2026-07-27 21:00:00+07', '2026-07-24 14:05:00+07', '2026-07-26 14:00:00+07', '2026-07-24 14:05:00+07', '2026-07-26 14:30:00+07');

INSERT INTO user_profiles (
    id, user_id, avatar_url, city, school_or_company, current_major_or_job,
    learning_goal, known_technologies, weekly_study_hours, updated_at
) VALUES
    ('12000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001', NULL, 'Hà Nội', 'Study2Work', 'System Administrator', 'Vận hành và bảo mật hệ thống', ARRAY['PostgreSQL','Docker','Linux'], 8, '2026-07-20 08:00:00+07'),
    ('12000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000002', NULL, 'Hà Nội', 'Study2Work', 'Content Manager', 'Xây dựng nội dung đào tạo chất lượng', ARRAY['Python','Technical Writing'], 10, '2026-07-20 08:05:00+07'),
    ('12000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000003', NULL, 'Hà Nội', 'Study2Work', 'Learner Support Specialist', 'Hỗ trợ người học hoàn thành lộ trình', ARRAY['Customer Support','SQL'], 6, '2026-07-20 08:10:00+07'),
    ('12000000-0000-0000-0000-000000000004', '00000000-0000-0000-0000-000000000004', NULL, 'Hà Nội', 'Study2Work', 'Community Moderator', 'Xây dựng cộng đồng học tập an toàn', ARRAY['Community Management'], 6, '2026-07-20 08:15:00+07'),
    ('12000000-0000-0000-0000-000000000101', '00000000-0000-0000-0000-000000000101', 'https://cdn.example.com/avatar/hung.png', 'Hà Nội', 'VNUA', 'Sinh viên CNTT / Full-stack Developer', 'Thành thạo FastAPI và triển khai backend', ARRAY['Python','FastAPI','PostgreSQL','Vue.js','Docker'], 24, '2026-07-25 21:00:00+07'),
    ('12000000-0000-0000-0000-000000000102', '00000000-0000-0000-0000-000000000102', 'https://cdn.example.com/avatar/lan.png', 'Bắc Ninh', 'Đại học Công nghệ', 'Sinh viên CNTT', 'Trở thành Full-stack Developer', ARRAY['HTML','CSS','JavaScript','Vue.js'], 18, '2026-07-22 19:30:00+07'),
    ('12000000-0000-0000-0000-000000000103', '00000000-0000-0000-0000-000000000103', NULL, 'Hải Phòng', 'Cao đẳng Công nghệ', 'Sinh viên năm nhất', 'Học nền tảng lập trình', ARRAY['HTML'], 10, '2026-07-26 14:30:00+07');

-- --------------------------------------------------------------------------
-- RBAC
-- --------------------------------------------------------------------------

INSERT INTO roles (id, code, name, scope, active) VALUES
    ('20000000-0000-0000-0000-000000000001', 'SYSTEM_ADMIN', 'System Administrator', 'SYSTEM', TRUE),
    ('20000000-0000-0000-0000-000000000002', 'LEARNER', 'Learner', 'STUDY', TRUE),
    ('20000000-0000-0000-0000-000000000003', 'CONTENT_MANAGER', 'Content Manager', 'CONTENT', TRUE),
    ('20000000-0000-0000-0000-000000000004', 'LEARNER_SUPPORT', 'Learner Support', 'LEARNER_SUPPORT', TRUE),
    ('20000000-0000-0000-0000-000000000005', 'COMMUNITY_MODERATOR', 'Community Moderator', 'COMMUNITY', TRUE),
    ('20000000-0000-0000-0000-000000000006', 'REPORT_VIEWER', 'Report Viewer', 'REPORTING', TRUE);

INSERT INTO user_roles (id, user_id, role_id, assigned_at) VALUES
    ('21000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001', '2026-06-01 08:00:00+07'),
    ('21000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000006', '2026-06-01 08:00:00+07'),
    ('21000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000002', '20000000-0000-0000-0000-000000000003', '2026-06-01 08:05:00+07'),
    ('21000000-0000-0000-0000-000000000004', '00000000-0000-0000-0000-000000000003', '20000000-0000-0000-0000-000000000004', '2026-06-01 08:10:00+07'),
    ('21000000-0000-0000-0000-000000000005', '00000000-0000-0000-0000-000000000004', '20000000-0000-0000-0000-000000000005', '2026-06-01 08:15:00+07'),
    ('21000000-0000-0000-0000-000000000101', '00000000-0000-0000-0000-000000000101', '20000000-0000-0000-0000-000000000002', '2026-07-01 09:10:00+07'),
    ('21000000-0000-0000-0000-000000000102', '00000000-0000-0000-0000-000000000102', '20000000-0000-0000-0000-000000000002', '2026-06-20 10:10:00+07'),
    ('21000000-0000-0000-0000-000000000103', '00000000-0000-0000-0000-000000000103', '20000000-0000-0000-0000-000000000002', '2026-07-24 14:10:00+07');

-- --------------------------------------------------------------------------
-- Learning catalog and onboarding
-- --------------------------------------------------------------------------

INSERT INTO learning_paths (
    id, slug, title, summary, description, level, estimated_hours,
    publish_status, unlock_mode, published_at
) VALUES
    ('30000000-0000-0000-0000-000000000001', 'backend-python-fastapi', 'Backend Python với FastAPI', 'Lộ trình từ Python đến REST API và triển khai.', 'Học Python, PostgreSQL, FastAPI và Docker qua các bài học và bài tập thực hành.', 'INTERMEDIATE', 120, 'PUBLISHED', 'SEQUENTIAL', '2026-06-15 08:00:00+07'),
    ('30000000-0000-0000-0000-000000000002', 'fullstack-vue-fastapi', 'Full-stack Vue và FastAPI', 'Xây dựng ứng dụng web hoàn chỉnh.', 'Kết hợp Vue.js, TypeScript, FastAPI, PostgreSQL và Docker.', 'INTERMEDIATE', 180, 'PUBLISHED', 'SEQUENTIAL', '2026-06-18 08:00:00+07'),
    ('30000000-0000-0000-0000-000000000003', 'cyber-security-foundations', 'Nền tảng An ninh mạng', 'Kiến thức nền về Linux, mạng và bảo mật ứng dụng.', 'Lộ trình đang xây dựng cho người học định hướng an ninh mạng.', 'BEGINNER', 90, 'DRAFT', 'ADMIN_ONLY', NULL);

INSERT INTO onboarding_records (
    id, user_id, programming_level, known_technologies, main_goal, sub_goals,
    weekly_study_hours, selected_learning_path_id, status, current_step, confirmed_at
) VALUES
    ('31000000-0000-0000-0000-000000000101', '00000000-0000-0000-0000-000000000101', 'INTERMEDIATE', ARRAY['Python','PostgreSQL','Vue.js'], 'Backend Developer', ARRAY['FastAPI','Docker','System Design'], 24, '30000000-0000-0000-0000-000000000001', 'COMPLETED', 5, '2026-07-01 09:30:00+07'),
    ('31000000-0000-0000-0000-000000000102', '00000000-0000-0000-0000-000000000102', 'BASIC', ARRAY['HTML','CSS','JavaScript'], 'Full-stack Developer', ARRAY['Vue.js','REST API','Deployment'], 18, '30000000-0000-0000-0000-000000000002', 'COMPLETED', 5, '2026-06-20 10:40:00+07'),
    ('31000000-0000-0000-0000-000000000103', '00000000-0000-0000-0000-000000000103', 'BEGINNER', ARRAY['HTML'], 'Học lập trình từ đầu', ARRAY['Python cơ bản','SQL cơ bản'], 10, '30000000-0000-0000-0000-000000000001', 'IN_PROGRESS', 3, NULL);

INSERT INTO courses (
    id, slug, title, summary, level, estimated_minutes, publish_status, published_at
) VALUES
    ('40000000-0000-0000-0000-000000000001', 'python-foundations', 'Nền tảng Python', 'Cú pháp, kiểu dữ liệu, điều kiện, vòng lặp và hàm.', 'BEGINNER', 900, 'PUBLISHED', '2026-06-10 08:00:00+07'),
    ('40000000-0000-0000-0000-000000000002', 'postgresql-foundations', 'PostgreSQL căn bản', 'Thiết kế bảng, ràng buộc và truy vấn SQL.', 'BEGINNER', 780, 'PUBLISHED', '2026-06-11 08:00:00+07'),
    ('40000000-0000-0000-0000-000000000003', 'fastapi-rest-api', 'Xây dựng REST API với FastAPI', 'Router, schema, dependency và xử lý lỗi.', 'INTERMEDIATE', 1200, 'PUBLISHED', '2026-06-12 08:00:00+07'),
    ('40000000-0000-0000-0000-000000000004', 'vue-typescript', 'Vue.js với TypeScript', 'Component, state và tích hợp API.', 'INTERMEDIATE', 1050, 'PUBLISHED', '2026-06-13 08:00:00+07'),
    ('40000000-0000-0000-0000-000000000005', 'docker-deployment', 'Docker và triển khai', 'Đóng gói backend, database và frontend.', 'INTERMEDIATE', 720, 'UPDATED', '2026-07-15 08:00:00+07');

INSERT INTO learning_path_courses (
    id, learning_path_id, course_id, order_index, required
) VALUES
    ('41000000-0000-0000-0000-000000000001', '30000000-0000-0000-0000-000000000001', '40000000-0000-0000-0000-000000000001', 0, TRUE),
    ('41000000-0000-0000-0000-000000000002', '30000000-0000-0000-0000-000000000001', '40000000-0000-0000-0000-000000000002', 1, TRUE),
    ('41000000-0000-0000-0000-000000000003', '30000000-0000-0000-0000-000000000001', '40000000-0000-0000-0000-000000000003', 2, TRUE),
    ('41000000-0000-0000-0000-000000000004', '30000000-0000-0000-0000-000000000001', '40000000-0000-0000-0000-000000000005', 3, TRUE),
    ('41000000-0000-0000-0000-000000000005', '30000000-0000-0000-0000-000000000002', '40000000-0000-0000-0000-000000000001', 0, TRUE),
    ('41000000-0000-0000-0000-000000000006', '30000000-0000-0000-0000-000000000002', '40000000-0000-0000-0000-000000000003', 1, TRUE),
    ('41000000-0000-0000-0000-000000000007', '30000000-0000-0000-0000-000000000002', '40000000-0000-0000-0000-000000000004', 2, TRUE),
    ('41000000-0000-0000-0000-000000000008', '30000000-0000-0000-0000-000000000002', '40000000-0000-0000-0000-000000000005', 3, TRUE),
    ('41000000-0000-0000-0000-000000000009', '30000000-0000-0000-0000-000000000003', '40000000-0000-0000-0000-000000000001', 0, TRUE),
    ('41000000-0000-0000-0000-000000000010', '30000000-0000-0000-0000-000000000003', '40000000-0000-0000-0000-000000000002', 1, TRUE);

-- --------------------------------------------------------------------------
-- Enrollments and progress
-- --------------------------------------------------------------------------

INSERT INTO learning_path_enrollments (
    id, user_id, learning_path_id, status, progress_percent,
    started_at, completed_at, admin_reason
) VALUES
    ('50000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000101', '30000000-0000-0000-0000-000000000001', 'ACTIVE', 45.00, '2026-07-02 08:00:00+07', NULL, NULL),
    ('50000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000102', '30000000-0000-0000-0000-000000000002', 'COMPLETED', 100.00, '2026-06-21 08:00:00+07', '2026-07-21 18:00:00+07', NULL),
    ('50000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000103', '30000000-0000-0000-0000-000000000001', 'NOT_STARTED', 0.00, NULL, NULL, NULL),
    ('50000000-0000-0000-0000-000000000004', '00000000-0000-0000-0000-000000000101', '30000000-0000-0000-0000-000000000002', 'CANCELLED_BY_ADMIN', 12.50, '2026-06-10 08:00:00+07', NULL, 'Người học chuyển sang lộ trình Backend phù hợp hơn.');

INSERT INTO course_enrollments (
    id, user_id, course_id, learning_path_enrollment_id,
    status, progress_percent, started_at, completed_at
) VALUES
    ('51000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000101', '40000000-0000-0000-0000-000000000001', '50000000-0000-0000-0000-000000000001', 'COMPLETED', 100.00, '2026-07-02 08:00:00+07', '2026-07-10 20:00:00+07'),
    ('51000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000101', '40000000-0000-0000-0000-000000000002', '50000000-0000-0000-0000-000000000001', 'ACTIVE', 60.00, '2026-07-11 08:00:00+07', NULL),
    ('51000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000101', '40000000-0000-0000-0000-000000000003', '50000000-0000-0000-0000-000000000001', 'NOT_STARTED', 0.00, NULL, NULL),
    ('51000000-0000-0000-0000-000000000004', '00000000-0000-0000-0000-000000000101', '40000000-0000-0000-0000-000000000005', '50000000-0000-0000-0000-000000000001', 'NOT_STARTED', 0.00, NULL, NULL),
    ('51000000-0000-0000-0000-000000000005', '00000000-0000-0000-0000-000000000102', '40000000-0000-0000-0000-000000000001', '50000000-0000-0000-0000-000000000002', 'COMPLETED', 100.00, '2026-06-21 08:00:00+07', '2026-06-27 18:00:00+07'),
    ('51000000-0000-0000-0000-000000000006', '00000000-0000-0000-0000-000000000102', '40000000-0000-0000-0000-000000000003', '50000000-0000-0000-0000-000000000002', 'COMPLETED', 100.00, '2026-06-28 08:00:00+07', '2026-07-08 18:00:00+07'),
    ('51000000-0000-0000-0000-000000000007', '00000000-0000-0000-0000-000000000102', '40000000-0000-0000-0000-000000000004', '50000000-0000-0000-0000-000000000002', 'COMPLETED', 100.00, '2026-07-09 08:00:00+07', '2026-07-16 18:00:00+07'),
    ('51000000-0000-0000-0000-000000000008', '00000000-0000-0000-0000-000000000102', '40000000-0000-0000-0000-000000000005', '50000000-0000-0000-0000-000000000002', 'COMPLETED', 100.00, '2026-07-17 08:00:00+07', '2026-07-21 18:00:00+07'),
    ('51000000-0000-0000-0000-000000000009', '00000000-0000-0000-0000-000000000103', '40000000-0000-0000-0000-000000000001', '50000000-0000-0000-0000-000000000003', 'NOT_STARTED', 0.00, NULL, NULL);

-- --------------------------------------------------------------------------
-- Curriculum
-- --------------------------------------------------------------------------

INSERT INTO chapters (
    id, course_id, title, objective, order_index, required, unlock_condition
) VALUES
    ('60000000-0000-0000-0000-000000000001', '40000000-0000-0000-0000-000000000001', 'Cú pháp và luồng điều khiển', 'Viết được chương trình Python cơ bản.', 0, TRUE, 'ALWAYS'),
    ('60000000-0000-0000-0000-000000000002', '40000000-0000-0000-0000-000000000001', 'Hàm và module', 'Tổ chức mã nguồn thành các đơn vị tái sử dụng.', 1, TRUE, 'PREVIOUS_CHAPTER_COMPLETED'),
    ('60000000-0000-0000-0000-000000000003', '40000000-0000-0000-0000-000000000002', 'Mô hình dữ liệu quan hệ', 'Tạo bảng và ràng buộc dữ liệu.', 0, TRUE, 'ALWAYS'),
    ('60000000-0000-0000-0000-000000000004', '40000000-0000-0000-0000-000000000002', 'Truy vấn SQL', 'Đọc và tổng hợp dữ liệu bằng SQL.', 1, TRUE, 'PREVIOUS_CHAPTER_COMPLETED'),
    ('60000000-0000-0000-0000-000000000005', '40000000-0000-0000-0000-000000000003', 'Cấu trúc ứng dụng FastAPI', 'Tạo ứng dụng và tổ chức router.', 0, TRUE, 'ALWAYS'),
    ('60000000-0000-0000-0000-000000000006', '40000000-0000-0000-0000-000000000003', 'Schema và REST API', 'Validate dữ liệu và thiết kế endpoint.', 1, TRUE, 'PREVIOUS_CHAPTER_COMPLETED'),
    ('60000000-0000-0000-0000-000000000007', '40000000-0000-0000-0000-000000000004', 'Vue Component', 'Xây dựng giao diện bằng component.', 0, TRUE, 'ALWAYS'),
    ('60000000-0000-0000-0000-000000000008', '40000000-0000-0000-0000-000000000004', 'State và API', 'Quản lý trạng thái và gọi backend.', 1, TRUE, 'PREVIOUS_CHAPTER_COMPLETED'),
    ('60000000-0000-0000-0000-000000000009', '40000000-0000-0000-0000-000000000005', 'Docker cơ bản', 'Đóng gói và chạy dịch vụ bằng container.', 0, TRUE, 'ALWAYS');

INSERT INTO lessons (
    id, chapter_id, title, objective, order_index, sample_public,
    required, completion_condition, publish_status
) VALUES
    ('61000000-0000-0000-0000-000000000001', '60000000-0000-0000-0000-000000000001', 'Biến và kiểu dữ liệu', 'Khai báo và sử dụng các kiểu dữ liệu cơ bản.', 0, TRUE, TRUE, 'ALL_REQUIRED_CONDITIONS', 'PUBLISHED'),
    ('61000000-0000-0000-0000-000000000002', '60000000-0000-0000-0000-000000000001', 'Điều kiện và vòng lặp', 'Sử dụng if, for và while.', 1, FALSE, TRUE, 'REQUIRED_EXERCISE_PASSED', 'PUBLISHED'),
    ('61000000-0000-0000-0000-000000000003', '60000000-0000-0000-0000-000000000002', 'Hàm trong Python', 'Khai báo hàm, tham số và giá trị trả về.', 0, FALSE, TRUE, 'ALL_REQUIRED_CONDITIONS', 'PUBLISHED'),
    ('61000000-0000-0000-0000-000000000004', '60000000-0000-0000-0000-000000000002', 'Module và package', 'Tách mã nguồn thành module.', 1, FALSE, TRUE, 'SELF_MARKED_DONE', 'PUBLISHED'),
    ('61000000-0000-0000-0000-000000000005', '60000000-0000-0000-0000-000000000003', 'Bảng và kiểu dữ liệu PostgreSQL', 'Tạo bảng với kiểu dữ liệu phù hợp.', 0, TRUE, TRUE, 'REQUIRED_MATERIALS_READ', 'PUBLISHED'),
    ('61000000-0000-0000-0000-000000000006', '60000000-0000-0000-0000-000000000003', 'Primary key và foreign key', 'Thiết kế quan hệ và ràng buộc tham chiếu.', 1, FALSE, TRUE, 'ALL_REQUIRED_CONDITIONS', 'PUBLISHED'),
    ('61000000-0000-0000-0000-000000000007', '60000000-0000-0000-0000-000000000004', 'SELECT, JOIN và GROUP BY', 'Viết truy vấn nhiều bảng.', 0, FALSE, TRUE, 'REQUIRED_EXERCISE_PASSED', 'PUBLISHED'),
    ('61000000-0000-0000-0000-000000000008', '60000000-0000-0000-0000-000000000005', 'Khởi tạo ứng dụng FastAPI', 'Chạy ứng dụng và tạo health check.', 0, TRUE, TRUE, 'VIEW_CONTENT', 'PUBLISHED'),
    ('61000000-0000-0000-0000-000000000009', '60000000-0000-0000-0000-000000000006', 'Pydantic schema', 'Validate request và response.', 0, FALSE, TRUE, 'ALL_REQUIRED_CONDITIONS', 'PUBLISHED'),
    ('61000000-0000-0000-0000-000000000010', '60000000-0000-0000-0000-000000000007', 'Component và props', 'Tạo component tái sử dụng.', 0, TRUE, TRUE, 'VIDEO_PERCENT', 'PUBLISHED'),
    ('61000000-0000-0000-0000-000000000011', '60000000-0000-0000-0000-000000000008', 'Gọi REST API từ Vue', 'Tích hợp frontend với backend.', 0, FALSE, TRUE, 'REQUIRED_EXERCISE_PASSED', 'PUBLISHED'),
    ('61000000-0000-0000-0000-000000000012', '60000000-0000-0000-0000-000000000009', 'Dockerfile và Docker Compose', 'Đóng gói ứng dụng nhiều dịch vụ.', 0, TRUE, TRUE, 'ALL_REQUIRED_CONDITIONS', 'PUBLISHED');

INSERT INTO course_materials (
    id, lesson_id, title, type, resource_url, required, source, usage_right_status
) VALUES
    ('62000000-0000-0000-0000-000000000001', '61000000-0000-0000-0000-000000000001', 'Video: Biến và kiểu dữ liệu', 'VIDEO', 'https://cdn.example.com/python/variables.mp4', TRUE, 'Study2Work', 'OWNED'),
    ('62000000-0000-0000-0000-000000000002', '61000000-0000-0000-0000-000000000002', 'Tài liệu điều kiện và vòng lặp', 'MARKDOWN', 'https://content.example.com/python/control-flow.md', TRUE, 'Study2Work', 'OWNED'),
    ('62000000-0000-0000-0000-000000000003', '61000000-0000-0000-0000-000000000003', 'Slide: Hàm trong Python', 'SLIDE', 'https://cdn.example.com/python/functions.pdf', TRUE, 'Study2Work', 'OWNED'),
    ('62000000-0000-0000-0000-000000000004', '61000000-0000-0000-0000-000000000004', 'Python Modules Documentation', 'LINK', 'https://docs.python.org/3/tutorial/modules.html', FALSE, 'Python Documentation', 'PUBLIC_DOMAIN'),
    ('62000000-0000-0000-0000-000000000005', '61000000-0000-0000-0000-000000000005', 'PostgreSQL Data Types', 'PDF', 'https://cdn.example.com/postgresql/data-types.pdf', TRUE, 'Study2Work', 'OWNED'),
    ('62000000-0000-0000-0000-000000000006', '61000000-0000-0000-0000-000000000006', 'Ví dụ khóa ngoại', 'CODE', 'https://code.example.com/sql/foreign-key.sql', TRUE, 'Study2Work', 'OWNED'),
    ('62000000-0000-0000-0000-000000000007', '61000000-0000-0000-0000-000000000007', 'SQL JOIN Practice Dataset', 'FILE', 'https://cdn.example.com/postgresql/join-dataset.csv', TRUE, 'Study2Work', 'OWNED'),
    ('62000000-0000-0000-0000-000000000008', '61000000-0000-0000-0000-000000000008', 'FastAPI First Steps', 'LINK', 'https://fastapi.tiangolo.com/tutorial/first-steps/', TRUE, 'FastAPI Documentation', 'PUBLIC_DOMAIN'),
    ('62000000-0000-0000-0000-000000000009', '61000000-0000-0000-0000-000000000009', 'Pydantic Schema Example', 'CODE', 'https://code.example.com/fastapi/schema.py', TRUE, 'Study2Work', 'OWNED'),
    ('62000000-0000-0000-0000-000000000010', '61000000-0000-0000-0000-000000000010', 'Vue Component Video', 'VIDEO', 'https://cdn.example.com/vue/component.mp4', TRUE, 'Study2Work', 'OWNED'),
    ('62000000-0000-0000-0000-000000000011', '61000000-0000-0000-0000-000000000011', 'Axios Integration Guide', 'MARKDOWN', 'https://content.example.com/vue/axios.md', TRUE, 'Study2Work', 'OWNED'),
    ('62000000-0000-0000-0000-000000000012', '61000000-0000-0000-0000-000000000012', 'Docker Compose Sample', 'CODE', 'https://code.example.com/docker/docker-compose.yml', TRUE, 'Study2Work', 'OWNED');

INSERT INTO exercises (
    id, course_id, chapter_id, lesson_id, title, type, required, due_at,
    allow_resubmit, max_score, rubric, publish_status
) VALUES
    ('63000000-0000-0000-0000-000000000001', '40000000-0000-0000-0000-000000000001', '60000000-0000-0000-0000-000000000001', '61000000-0000-0000-0000-000000000001', 'Quiz biến và kiểu dữ liệu', 'QUIZ', TRUE, '2026-08-01 23:59:00+07', TRUE, 100, 'Đúng mỗi câu được 10 điểm.', 'PUBLISHED'),
    ('63000000-0000-0000-0000-000000000002', '40000000-0000-0000-0000-000000000001', '60000000-0000-0000-0000-000000000001', '61000000-0000-0000-0000-000000000002', 'Bài tập vòng lặp', 'CODING', TRUE, '2026-08-03 23:59:00+07', TRUE, 100, 'Đúng kết quả 60; cấu trúc 20; chất lượng mã 20.', 'PUBLISHED'),
    ('63000000-0000-0000-0000-000000000003', '40000000-0000-0000-0000-000000000002', '60000000-0000-0000-0000-000000000003', '61000000-0000-0000-0000-000000000006', 'Thiết kế schema cửa hàng', 'FILE_UPLOAD', TRUE, '2026-08-08 23:59:00+07', TRUE, 100, 'Đúng quan hệ 40; ràng buộc 40; trình bày 20.', 'PUBLISHED'),
    ('63000000-0000-0000-0000-000000000004', '40000000-0000-0000-0000-000000000002', '60000000-0000-0000-0000-000000000004', '61000000-0000-0000-0000-000000000007', 'SQL JOIN Challenge', 'CODING', TRUE, '2026-08-10 23:59:00+07', TRUE, 100, 'Mỗi truy vấn đúng 20 điểm.', 'PUBLISHED'),
    ('63000000-0000-0000-0000-000000000005', '40000000-0000-0000-0000-000000000003', '60000000-0000-0000-0000-000000000005', '61000000-0000-0000-0000-000000000008', 'Tạo Health Check API', 'LINK_SUBMISSION', TRUE, '2026-08-15 23:59:00+07', TRUE, 100, 'Endpoint 40; cấu trúc 30; README 30.', 'PUBLISHED'),
    ('63000000-0000-0000-0000-000000000006', '40000000-0000-0000-0000-000000000003', '60000000-0000-0000-0000-000000000006', '61000000-0000-0000-0000-000000000009', 'CRUD API Mini Project', 'PROJECT', TRUE, '2026-08-20 23:59:00+07', TRUE, 100, 'API 50; validation 20; test 20; tài liệu 10.', 'PUBLISHED'),
    ('63000000-0000-0000-0000-000000000007', '40000000-0000-0000-0000-000000000004', '60000000-0000-0000-0000-000000000008', '61000000-0000-0000-0000-000000000011', 'Tích hợp Vue với REST API', 'PROJECT', TRUE, '2026-08-25 23:59:00+07', TRUE, 100, 'UI 30; API 40; xử lý lỗi 30.', 'PUBLISHED'),
    ('63000000-0000-0000-0000-000000000008', '40000000-0000-0000-0000-000000000005', '60000000-0000-0000-0000-000000000009', '61000000-0000-0000-0000-000000000012', 'Dockerize Full-stack App', 'PROJECT', TRUE, '2026-08-30 23:59:00+07', TRUE, 100, 'Dockerfile 30; Compose 40; vận hành 30.', 'PUBLISHED');

INSERT INTO exercise_submissions (
    id, exercise_id, user_id, status, attempt_no, text_answer, file_url,
    link_url, score, feedback, submitted_at, reviewed_at
) VALUES
    ('64000000-0000-0000-0000-000000000001', '63000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000101', 'PASSED', 1, 'Đáp án quiz được lưu dưới dạng JSON bởi backend.', NULL, NULL, 90, 'Nắm chắc kiểu dữ liệu; cần xem lại tuple.', '2026-07-03 20:00:00+07', '2026-07-03 20:01:00+07'),
    ('64000000-0000-0000-0000-000000000002', '63000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000101', 'PASSED', 1, 'Giải bài bằng for loop và list comprehension.', NULL, 'https://github.com/example/hung-python-loop', 85, 'Kết quả đúng; nên bổ sung test biên.', '2026-07-06 21:00:00+07', '2026-07-07 09:00:00+07'),
    ('64000000-0000-0000-0000-000000000003', '63000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000101', 'SUBMITTED', 1, NULL, 'https://cdn.example.com/submissions/hung-store-schema.sql', NULL, NULL, NULL, '2026-07-25 22:00:00+07', NULL),
    ('64000000-0000-0000-0000-000000000004', '63000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000102', 'PASSED', 1, 'Đáp án quiz.', NULL, NULL, 100, 'Hoàn thành xuất sắc.', '2026-06-22 19:00:00+07', '2026-06-22 19:01:00+07'),
    ('64000000-0000-0000-0000-000000000005', '63000000-0000-0000-0000-000000000006', '00000000-0000-0000-0000-000000000102', 'PASSED', 2, 'CRUD khóa học bằng FastAPI.', NULL, 'https://github.com/example/lan-fastapi-crud', 92, 'Thiết kế API rõ ràng; test tốt.', '2026-07-07 22:00:00+07', '2026-07-08 10:00:00+07'),
    ('64000000-0000-0000-0000-000000000006', '63000000-0000-0000-0000-000000000007', '00000000-0000-0000-0000-000000000102', 'NEEDS_REVISION', 1, 'Vue frontend tích hợp API.', NULL, 'https://github.com/example/lan-vue-api', 68, 'Cần xử lý loading và lỗi mạng.', '2026-07-14 21:00:00+07', '2026-07-15 09:00:00+07'),
    ('64000000-0000-0000-0000-000000000007', '63000000-0000-0000-0000-000000000007', '00000000-0000-0000-0000-000000000102', 'PASSED', 2, 'Đã bổ sung loading, retry và error state.', NULL, 'https://github.com/example/lan-vue-api', 88, 'Đạt yêu cầu sau chỉnh sửa.', '2026-07-16 20:00:00+07', '2026-07-16 21:00:00+07');

INSERT INTO lesson_progress (
    id, user_id, lesson_id, status, video_watch_percent,
    required_materials_read, self_marked_done, required_exercise_passed,
    last_accessed_at, completed_at
) VALUES
    ('65000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000101', '61000000-0000-0000-0000-000000000001', 'COMPLETED', 100.00, TRUE, TRUE, TRUE, '2026-07-03 20:01:00+07', '2026-07-03 20:01:00+07'),
    ('65000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000101', '61000000-0000-0000-0000-000000000002', 'COMPLETED', 100.00, TRUE, TRUE, TRUE, '2026-07-07 09:00:00+07', '2026-07-07 09:00:00+07'),
    ('65000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000101', '61000000-0000-0000-0000-000000000003', 'COMPLETED', 100.00, TRUE, TRUE, TRUE, '2026-07-09 21:00:00+07', '2026-07-09 21:00:00+07'),
    ('65000000-0000-0000-0000-000000000004', '00000000-0000-0000-0000-000000000101', '61000000-0000-0000-0000-000000000004', 'COMPLETED', 75.00, TRUE, TRUE, FALSE, '2026-07-10 20:00:00+07', '2026-07-10 20:00:00+07'),
    ('65000000-0000-0000-0000-000000000005', '00000000-0000-0000-0000-000000000101', '61000000-0000-0000-0000-000000000005', 'COMPLETED', 100.00, TRUE, TRUE, FALSE, '2026-07-20 21:00:00+07', '2026-07-20 21:00:00+07'),
    ('65000000-0000-0000-0000-000000000006', '00000000-0000-0000-0000-000000000101', '61000000-0000-0000-0000-000000000006', 'IN_PROGRESS', 70.00, TRUE, FALSE, FALSE, '2026-07-27 20:00:00+07', NULL),
    ('65000000-0000-0000-0000-000000000007', '00000000-0000-0000-0000-000000000102', '61000000-0000-0000-0000-000000000008', 'COMPLETED', 100.00, TRUE, TRUE, TRUE, '2026-07-01 19:00:00+07', '2026-07-01 19:00:00+07'),
    ('65000000-0000-0000-0000-000000000008', '00000000-0000-0000-0000-000000000102', '61000000-0000-0000-0000-000000000009', 'COMPLETED', 100.00, TRUE, TRUE, TRUE, '2026-07-08 18:00:00+07', '2026-07-08 18:00:00+07'),
    ('65000000-0000-0000-0000-000000000009', '00000000-0000-0000-0000-000000000102', '61000000-0000-0000-0000-000000000010', 'COMPLETED', 100.00, TRUE, TRUE, TRUE, '2026-07-12 20:00:00+07', '2026-07-12 20:00:00+07'),
    ('65000000-0000-0000-0000-000000000010', '00000000-0000-0000-0000-000000000102', '61000000-0000-0000-0000-000000000011', 'COMPLETED', 100.00, TRUE, TRUE, TRUE, '2026-07-16 21:00:00+07', '2026-07-16 21:00:00+07'),
    ('65000000-0000-0000-0000-000000000011', '00000000-0000-0000-0000-000000000103', '61000000-0000-0000-0000-000000000001', 'NOT_STARTED', 0.00, FALSE, FALSE, FALSE, NULL, NULL);

INSERT INTO completion_rules (
    id, target_type, target_id, required_items_only,
    minimum_score, minimum_video_percent, description
) VALUES
    ('66000000-0000-0000-0000-000000000001', 'LEARNING_PATH', '30000000-0000-0000-0000-000000000001', TRUE, 70, 80.00, 'Hoàn thành toàn bộ khóa học bắt buộc và đạt tối thiểu 70 điểm.'),
    ('66000000-0000-0000-0000-000000000002', 'LEARNING_PATH', '30000000-0000-0000-0000-000000000002', TRUE, 70, 80.00, 'Hoàn thành các khóa Backend, Frontend và Deployment.'),
    ('66000000-0000-0000-0000-000000000003', 'COURSE', '40000000-0000-0000-0000-000000000001', TRUE, 60, 80.00, 'Đạt bài tập bắt buộc và xem tối thiểu 80% video.'),
    ('66000000-0000-0000-0000-000000000004', 'COURSE', '40000000-0000-0000-0000-000000000003', TRUE, 70, 90.00, 'Đạt CRUD project và hoàn thành bài học bắt buộc.'),
    ('66000000-0000-0000-0000-000000000005', 'COURSE', '40000000-0000-0000-0000-000000000005', TRUE, 70, NULL, 'Chạy thành công ứng dụng bằng Docker Compose.');

-- --------------------------------------------------------------------------
-- Notifications
-- --------------------------------------------------------------------------

INSERT INTO notification_settings (
    id, user_id, optional_reminder_enabled, email_learning_reminder_enabled,
    mandatory_notice_enabled, updated_at
) VALUES
    ('70000000-0000-0000-0000-000000000101', '00000000-0000-0000-0000-000000000101', TRUE, TRUE, TRUE, '2026-07-20 08:00:00+07'),
    ('70000000-0000-0000-0000-000000000102', '00000000-0000-0000-0000-000000000102', FALSE, TRUE, TRUE, '2026-07-21 08:00:00+07'),
    ('70000000-0000-0000-0000-000000000103', '00000000-0000-0000-0000-000000000103', TRUE, FALSE, TRUE, '2026-07-25 08:00:00+07');

INSERT INTO notifications (
    id, user_id, type, title, body, priority, read_status,
    action_url, created_at, read_at
) VALUES
    ('71000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000101', 'LEARNING_REMINDER', 'Tiếp tục khóa PostgreSQL', 'Bạn đang hoàn thành 60% khóa PostgreSQL căn bản.', 'NORMAL', 'UNREAD', '/study/courses/postgresql-foundations', '2026-07-27 19:00:00+07', NULL),
    ('71000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000101', 'REVIEW_RESULT', 'Bài tập Python đã được chấm', 'Bài tập vòng lặp đạt 85/100 điểm.', 'NORMAL', 'READ', '/study/submissions/64000000-0000-0000-0000-000000000002', '2026-07-07 09:01:00+07', '2026-07-07 10:00:00+07'),
    ('71000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000102', 'CONTENT_UPDATE', 'Khóa Docker vừa được cập nhật', 'Nội dung Docker Compose đã được bổ sung.', 'LOW', 'READ', '/study/courses/docker-deployment', '2026-07-15 09:00:00+07', '2026-07-15 12:00:00+07'),
    ('71000000-0000-0000-0000-000000000004', '00000000-0000-0000-0000-000000000102', 'COMMUNITY', 'Mời tham gia cộng đồng Full-stack', 'Tham gia nhóm để trao đổi cùng người học khác.', 'NORMAL', 'UNREAD', '/community/groups/80000000-0000-0000-0000-000000000002', '2026-07-22 08:00:00+07', NULL),
    ('71000000-0000-0000-0000-000000000005', '00000000-0000-0000-0000-000000000103', 'SECURITY', 'Tài khoản tạm khóa đăng nhập', 'Tài khoản bị khóa đến 21:00 do đăng nhập sai nhiều lần.', 'HIGH', 'UNREAD', '/account/security', '2026-07-27 20:00:00+07', NULL),
    ('71000000-0000-0000-0000-000000000006', '00000000-0000-0000-0000-000000000101', 'MANDATORY_NOTICE', 'Bảo trì hệ thống', 'Hệ thống bảo trì từ 00:00 đến 01:00 ngày 28/07/2026.', 'URGENT', 'UNREAD', '/notices/maintenance-20260728', '2026-07-27 18:00:00+07', NULL);

-- --------------------------------------------------------------------------
-- Community
-- --------------------------------------------------------------------------

INSERT INTO community_groups (
    id, name, scope_type, scope_id, join_link, status, rules, moderator_id
) VALUES
    ('80000000-0000-0000-0000-000000000001', 'Study2Work Community', 'GLOBAL', NULL, 'https://zalo.me/g/study2work-global', 'ACTIVE', 'Tôn trọng thành viên; không spam; không chia sẻ nội dung vi phạm bản quyền.', '00000000-0000-0000-0000-000000000004'),
    ('80000000-0000-0000-0000-000000000002', 'Backend Python Learners', 'LEARNING_PATH', '30000000-0000-0000-0000-000000000001', 'https://zalo.me/g/backend-python', 'ACTIVE', 'Thảo luận đúng chủ đề; che thông tin nhạy cảm khi đăng lỗi.', '00000000-0000-0000-0000-000000000004'),
    ('80000000-0000-0000-0000-000000000003', 'FastAPI Course Support', 'COURSE', '40000000-0000-0000-0000-000000000003', 'https://zalo.me/g/fastapi-course', 'PAUSED', 'Đặt câu hỏi kèm mã lỗi và bước tái hiện.', '00000000-0000-0000-0000-000000000004');

INSERT INTO community_join_events (
    id, user_id, community_group_id, confirmed_rules, source_screen, opened_at
) VALUES
    ('81000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000101', '80000000-0000-0000-0000-000000000001', TRUE, 'community_home', '2026-07-03 20:10:00+07'),
    ('81000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000101', '80000000-0000-0000-0000-000000000002', TRUE, 'learning_path_detail', '2026-07-04 20:10:00+07'),
    ('81000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000102', '80000000-0000-0000-0000-000000000001', TRUE, 'community_home', '2026-06-22 20:10:00+07'),
    ('81000000-0000-0000-0000-000000000004', '00000000-0000-0000-0000-000000000102', '80000000-0000-0000-0000-000000000003', TRUE, 'course_detail', '2026-07-02 20:10:00+07');

-- --------------------------------------------------------------------------
-- Support and audit
-- --------------------------------------------------------------------------

INSERT INTO support_requests (
    id, user_id, type, reason, current_learning_path_id,
    target_learning_path_id, current_learning_path_enrollment_id,
    status, admin_decision, resolved_at
) VALUES
    ('90000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000101', 'CHANGE_PATH', 'Muốn học thêm frontend sau khi hoàn thành phần backend.', '30000000-0000-0000-0000-000000000001', '30000000-0000-0000-0000-000000000002', '50000000-0000-0000-0000-000000000001', 'OPEN', NULL, NULL),
    ('90000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000102', 'PROGRESS_RESET', 'Cần làm lại bài Vue để củng cố kiến thức.', '30000000-0000-0000-0000-000000000002', NULL, '50000000-0000-0000-0000-000000000002', 'RESOLVED', 'Đã mở lại bài tích hợp Vue API và giữ lịch sử lần nộp.', '2026-07-15 08:30:00+07'),
    ('90000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000103', 'OTHER', 'Cần hỗ trợ chọn lộ trình phù hợp cho người mới.', '30000000-0000-0000-0000-000000000001', NULL, '50000000-0000-0000-0000-000000000003', 'IN_REVIEW', 'Đang đánh giá kết quả onboarding.', NULL);

INSERT INTO audit_logs (
    id, actor_id, actor_role, action, target_type, target_id,
    support_request_id, before_value, after_value, reason, channel, created_at
) VALUES
    ('91000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001', 'SYSTEM_ADMIN', 'ASSIGN_ROLE', 'USER_ROLE', '21000000-0000-0000-0000-000000000003', NULL, NULL, NULL, 'Gán quyền quản lý nội dung.', 'ADMIN_PORTAL', '2026-06-01 08:05:00+07'),
    ('91000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000002', 'CONTENT_MANAGER', 'PUBLISH', 'LEARNING_PATH', '30000000-0000-0000-0000-000000000001', NULL, '{"publish_status":"IN_REVIEW"}'::JSONB, '{"publish_status":"PUBLISHED","published_at":"2026-06-15T08:00:00+07:00"}'::JSONB, 'Nội dung đã được duyệt.', 'ADMIN_PORTAL', '2026-06-15 08:00:00+07'),
    ('91000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000003', 'LEARNER_SUPPORT', 'RESET_PROGRESS', 'LESSON_PROGRESS', '65000000-0000-0000-0000-000000000010', '90000000-0000-0000-0000-000000000002', '{"status":"COMPLETED"}'::JSONB, '{"status":"IN_PROGRESS"}'::JSONB, 'Mở lại bài học theo yêu cầu người học.', 'ADMIN_PORTAL', '2026-07-15 08:30:00+07'),
    ('91000000-0000-0000-0000-000000000004', '00000000-0000-0000-0000-000000000001', 'SYSTEM_ADMIN', 'SEND_NOTIFICATION', 'NOTIFICATION', '71000000-0000-0000-0000-000000000006', NULL, NULL, NULL, 'Thông báo lịch bảo trì bắt buộc.', 'ADMIN_PORTAL', '2026-07-27 18:00:00+07'),
    ('91000000-0000-0000-0000-000000000005', '00000000-0000-0000-0000-000000000003', 'LEARNER_SUPPORT', 'REVIEW_SUBMISSION', 'EXERCISE_SUBMISSION', '64000000-0000-0000-0000-000000000007', NULL, '{"status":"UNDER_REVIEW","score":null}'::JSONB, '{"status":"PASSED","score":88}'::JSONB, 'Bài sửa đã đạt yêu cầu.', 'ADMIN_PORTAL', '2026-07-16 21:00:00+07'),
    ('91000000-0000-0000-0000-000000000006', '00000000-0000-0000-0000-000000000001', 'SYSTEM_ADMIN', 'UPDATE', 'AUTH_CREDENTIAL', '10000000-0000-0000-0000-000000000103', NULL, '{"failed_login_attempts":1,"locked_until":null}'::JSONB, '{"failed_login_attempts":2,"locked_until":"2026-07-27T21:00:00+07:00"}'::JSONB, 'Khóa tạm thời sau nhiều lần đăng nhập sai.', 'API', '2026-07-27 20:00:00+07');


COMMIT;

-- ============================================================================
-- POST-DEPLOYMENT VERIFICATION
-- These queries are read-only and run after the transaction is committed.
-- ============================================================================

SELECT
    current_database() AS database_name,
    current_user AS database_user,
    'study_dev0' AS deployed_schema;

SELECT COUNT(*) AS table_count
FROM information_schema.tables
WHERE table_schema = 'study_dev0'
  AND table_type = 'BASE TABLE';

SELECT COUNT(*) AS enum_type_count
FROM pg_type AS t
JOIN pg_namespace AS n ON n.oid = t.typnamespace
WHERE n.nspname = 'study_dev0'
  AND t.typtype = 'e';

-- Verify that every table has seed rows.
SELECT 'audit_logs' AS table_name, COUNT(*) AS row_count FROM study_dev0.audit_logs
UNION ALL SELECT 'auth_credentials', COUNT(*) FROM study_dev0.auth_credentials
UNION ALL SELECT 'chapters', COUNT(*) FROM study_dev0.chapters
UNION ALL SELECT 'community_groups', COUNT(*) FROM study_dev0.community_groups
UNION ALL SELECT 'community_join_events', COUNT(*) FROM study_dev0.community_join_events
UNION ALL SELECT 'completion_rules', COUNT(*) FROM study_dev0.completion_rules
UNION ALL SELECT 'course_enrollments', COUNT(*) FROM study_dev0.course_enrollments
UNION ALL SELECT 'course_materials', COUNT(*) FROM study_dev0.course_materials
UNION ALL SELECT 'courses', COUNT(*) FROM study_dev0.courses
UNION ALL SELECT 'exercise_submissions', COUNT(*) FROM study_dev0.exercise_submissions
UNION ALL SELECT 'exercises', COUNT(*) FROM study_dev0.exercises
UNION ALL SELECT 'learning_path_courses', COUNT(*) FROM study_dev0.learning_path_courses
UNION ALL SELECT 'learning_path_enrollments', COUNT(*) FROM study_dev0.learning_path_enrollments
UNION ALL SELECT 'learning_paths', COUNT(*) FROM study_dev0.learning_paths
UNION ALL SELECT 'lesson_progress', COUNT(*) FROM study_dev0.lesson_progress
UNION ALL SELECT 'lessons', COUNT(*) FROM study_dev0.lessons
UNION ALL SELECT 'notification_settings', COUNT(*) FROM study_dev0.notification_settings
UNION ALL SELECT 'notifications', COUNT(*) FROM study_dev0.notifications
UNION ALL SELECT 'onboarding_records', COUNT(*) FROM study_dev0.onboarding_records
UNION ALL SELECT 'roles', COUNT(*) FROM study_dev0.roles
UNION ALL SELECT 'support_requests', COUNT(*) FROM study_dev0.support_requests
UNION ALL SELECT 'user_profiles', COUNT(*) FROM study_dev0.user_profiles
UNION ALL SELECT 'user_roles', COUNT(*) FROM study_dev0.user_roles
UNION ALL SELECT 'users', COUNT(*) FROM study_dev0.users
ORDER BY table_name;

-- Demo account overview. Password hashes are intentionally excluded.
SELECT
    u.email,
    u.display_name,
    u.account_status,
    u.contact_verified,
    ac.password_algorithm,
    ac.password_login_enabled,
    ac.must_change_password,
    ac.failed_login_attempts,
    ac.locked_until,
    ARRAY_AGG(r.code ORDER BY r.code) AS roles
FROM study_dev0.users AS u
JOIN study_dev0.auth_credentials AS ac ON ac.user_id = u.id
LEFT JOIN study_dev0.user_roles AS ur ON ur.user_id = u.id
LEFT JOIN study_dev0.roles AS r ON r.id = ur.role_id
GROUP BY
    u.id,
    u.email,
    u.display_name,
    u.account_status,
    u.contact_verified,
    ac.password_algorithm,
    ac.password_login_enabled,
    ac.must_change_password,
    ac.failed_login_attempts,
    ac.locked_until
ORDER BY u.email;

