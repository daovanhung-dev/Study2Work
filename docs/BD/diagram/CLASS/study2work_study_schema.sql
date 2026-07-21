-- ============================================================================
-- Study2Work - Study Module
-- PostgreSQL DDL generated from the business class diagram.
-- Target: PostgreSQL 15+
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
