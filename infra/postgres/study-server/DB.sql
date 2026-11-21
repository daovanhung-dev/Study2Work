-- 01. ACCOUNT & USER

CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    avatar_url TEXT NULL,
    phone VARCHAR(20) NULL,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE refresh_tokens (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(64) NOT NULL UNIQUE,
    expires_at TIMESTAMPTZ NOT NULL,
    revoked_at TIMESTAMPTZ NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_expires_at ON refresh_tokens(expires_at);

-- 02. COURSE & DISCOVERY

CREATE TABLE categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(200) NOT NULL,
    description TEXT NULL,
    locale VARCHAR(20) NOT NULL DEFAULT 'vi-VN',
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
);

CREATE INDEX idx_categories_status_locale
    ON categories(status, locale);

-- 03. COURSE & LEARNING

CREATE TABLE courses (
    id BIGSERIAL PRIMARY KEY,
    mentor_id BIGINT REFERENCES users(id),
    name VARCHAR(200) NOT NULL,
    description TEXT NULL,
    thumbnail_url TEXT NULL,
    price NUMERIC(12,2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'DRAFT',
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- API #76 DERIVED fallback: the AC-32 diagram requires course status + audit.
-- This legacy BIGINT candidate does not prove the live schema or deployment.
CREATE TABLE course_status_audit_logs (
    id BIGSERIAL PRIMARY KEY,
    course_id BIGINT NOT NULL REFERENCES courses(id) ON DELETE RESTRICT,
    actor_user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    previous_status VARCHAR(20) NULL,
    new_status VARCHAR(20) NOT NULL,
    changed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_course_status_audit_logs_course_changed
    ON course_status_audit_logs(course_id, changed_at DESC, id DESC);

CREATE INDEX idx_course_status_audit_logs_actor_changed
    ON course_status_audit_logs(actor_user_id, changed_at DESC, id DESC);

CREATE TABLE lessons (
    id BIGSERIAL PRIMARY KEY,
    course_id BIGINT REFERENCES courses(id),
    name VARCHAR(200) NOT NULL,
    content TEXT NULL,
    video_url TEXT NULL,
    sort_order INT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'DRAFT',
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE resources (
    id BIGSERIAL PRIMARY KEY,
    lesson_id BIGINT REFERENCES lessons(id),
    name VARCHAR(200) NOT NULL,
    resource_type VARCHAR(20) NOT NULL,
    url TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE enrollments (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    course_id BIGINT REFERENCES courses(id),
    status VARCHAR(20) DEFAULT 'ACTIVE',
    enrolled_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP NULL
);

CREATE TABLE uploads (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES users(id),
    purpose VARCHAR(20) NOT NULL CHECK (purpose IN ('SUBMISSION', 'LECTURE')),
    course_id BIGINT REFERENCES courses(id),
    storage_key TEXT NOT NULL UNIQUE,
    file_name TEXT NOT NULL,
    url TEXT NOT NULL,
    content_type TEXT NOT NULL,
    size_bytes BIGINT NOT NULL CHECK (size_bytes >= 0),
    status VARCHAR(20) NOT NULL DEFAULT 'UPLOADED' CHECK (status = 'UPLOADED')
);

CREATE INDEX idx_uploads_owner_purpose_course
    ON uploads(owner_id, purpose, course_id);

CREATE TABLE lesson_uploads (
    lesson_id BIGINT NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    upload_id BIGINT NOT NULL REFERENCES uploads(id),
    asset_position BIGINT NOT NULL CHECK (asset_position >= 0),
    PRIMARY KEY (lesson_id, upload_id),
    UNIQUE (lesson_id, asset_position)
);

CREATE TABLE contents (
    id BIGSERIAL PRIMARY KEY,
    course_id BIGINT NOT NULL REFERENCES courses(id),
    content_type TEXT NOT NULL,
    title TEXT NOT NULL,
    payload JSONB NOT NULL CHECK (jsonb_typeof(payload) = 'object'),
    status TEXT NOT NULL,
    parent_id BIGINT NULL,
    content_order INTEGER NOT NULL,
    deleted_at TIMESTAMP NULL,
    UNIQUE (id, course_id),
    FOREIGN KEY (parent_id, course_id) REFERENCES contents(id, course_id)
);

CREATE INDEX idx_contents_course_tree
    ON contents(course_id, parent_id, content_order, id)
    WHERE deleted_at IS NULL;

CREATE TABLE content_versions (
    content_id BIGINT NOT NULL,
    version_no BIGINT NOT NULL CHECK (version_no > 0),
    course_id BIGINT NOT NULL,
    content_type TEXT NOT NULL,
    title TEXT NOT NULL,
    payload JSONB NOT NULL CHECK (jsonb_typeof(payload) = 'object'),
    status TEXT NOT NULL,
    parent_id BIGINT NULL,
    content_order INTEGER NOT NULL,
    archived_by BIGINT NOT NULL REFERENCES users(id),
    archived_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (content_id, version_no),
    FOREIGN KEY (content_id, course_id) REFERENCES contents(id, course_id),
    FOREIGN KEY (parent_id, course_id) REFERENCES contents(id, course_id)
);

-- API #80 DERIVED fallback: append review outcomes for legacy BIGINT Content rows.
-- This source artifact does not prove the live schema or migration deployment.
CREATE TABLE content_review_audit_logs (
    id BIGSERIAL PRIMARY KEY,
    content_id BIGINT NOT NULL REFERENCES contents(id) ON DELETE RESTRICT,
    actor_user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    previous_status TEXT NOT NULL,
    new_status TEXT NOT NULL,
    reason TEXT NULL,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_content_review_audit_logs_content_recorded
    ON content_review_audit_logs(content_id, recorded_at DESC, id DESC);

CREATE INDEX idx_content_review_audit_logs_actor_recorded
    ON content_review_audit_logs(actor_user_id, recorded_at DESC, id DESC);

CREATE TABLE lesson_progress (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    lesson_id BIGINT REFERENCES lessons(id),
    status VARCHAR(20) DEFAULT 'NOT_STARTED',
    progress_percent SMALLINT DEFAULT 0,
    last_accessed_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL
);

-- 04. ASSESSMENT

CREATE TABLE quizzes (
    id BIGSERIAL PRIMARY KEY,
    course_id BIGINT REFERENCES courses(id),
    name VARCHAR(200) NOT NULL,
    description TEXT NULL,
    passing_score NUMERIC(5,2) DEFAULT 0,
    time_limit_minutes INT NULL,
    status VARCHAR(20) DEFAULT 'DRAFT',
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE quiz_questions (
    id BIGSERIAL PRIMARY KEY,
    quiz_id BIGINT REFERENCES quizzes(id),
    question_text TEXT NOT NULL,
    question_type VARCHAR(24) NULL CONSTRAINT ck_quiz_questions_question_type CHECK (
        question_type IS NULL
        OR question_type IN ('SINGLE_CHOICE', 'MULTIPLE_CHOICE', 'TRUE_FALSE')
    ),
    sort_order INT DEFAULT 0,
    score NUMERIC(5,2) DEFAULT 1
);

CREATE TABLE quiz_choices (
    id BIGSERIAL PRIMARY KEY,
    question_id BIGINT REFERENCES quiz_questions(id),
    choice_text TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT FALSE,
    sort_order INT NOT NULL DEFAULT 0
);

CREATE TABLE quiz_attempts (
    id BIGSERIAL PRIMARY KEY,
    quiz_id BIGINT REFERENCES quizzes(id),
    user_id BIGINT REFERENCES users(id),
    started_at TIMESTAMP NOT NULL,
    submitted_at TIMESTAMP NULL,
    score NUMERIC(6,2) NULL,
    status VARCHAR(20) DEFAULT 'IN_PROGRESS'
);

CREATE TABLE quiz_answers (
    id BIGSERIAL PRIMARY KEY,
    attempt_id BIGINT REFERENCES quiz_attempts(id),
    question_id BIGINT REFERENCES quiz_questions(id),
    choice_id BIGINT REFERENCES quiz_choices(id),
    is_correct BOOLEAN NOT NULL,
    score_received NUMERIC(5,2) DEFAULT 0
);

CREATE TABLE assignments (
    id BIGSERIAL PRIMARY KEY,
    course_id BIGINT REFERENCES courses(id),
    name VARCHAR(200) NOT NULL,
    description TEXT NULL,
    due_at TIMESTAMP NULL,
    max_score NUMERIC(6,2) DEFAULT 10,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE assignment_submissions (
    id BIGSERIAL PRIMARY KEY,
    assignment_id BIGINT REFERENCES assignments(id),
    user_id BIGINT REFERENCES users(id),
    content TEXT NULL,
    file_url TEXT NULL,
    submitted_at TIMESTAMP NOT NULL,
    score NUMERIC(6,2) NULL,
    feedback TEXT NULL,
    status VARCHAR(20) DEFAULT 'SUBMITTED'
);

-- 05. INTERACTION & SYSTEM

CREATE TABLE discussions (
    id BIGSERIAL PRIMARY KEY,
    course_id BIGINT REFERENCES courses(id),
    user_id BIGINT REFERENCES users(id),
    parent_id BIGINT NULL REFERENCES discussions(id),
    content TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- API #97 DERIVED fallback: keep report records in the Study database and link by BIGINT.
-- This legacy DDL candidate does not prove live schema, report ingestion, or deployment.
CREATE TABLE discussion_reports (
    id BIGSERIAL PRIMARY KEY,
    discussion_id BIGINT NOT NULL REFERENCES discussions(id) ON DELETE RESTRICT,
    reporter_user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    reason_code VARCHAR(80) NOT NULL,
    severity VARCHAR(24) NOT NULL,
    status VARCHAR(24) NOT NULL DEFAULT 'OPEN'
        CHECK (status IN ('OPEN', 'IN_REVIEW', 'RESOLVED', 'DISMISSED')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_discussion_reports_queue_filter_created
    ON discussion_reports(status, reason_code, severity, created_at DESC, discussion_id);

CREATE INDEX idx_discussion_reports_discussion_status_created
    ON discussion_reports(discussion_id, status, created_at DESC, id DESC);

CREATE TABLE notifications (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NULL REFERENCES users(id),
    sender_id BIGINT NULL REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    type VARCHAR(30) NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL,
    operation_id UUID NULL
);

-- API #63 fallback: one delivery-outbox row per notification/channel.
-- This checked-in BIGINT schema does not prove live deployment or worker availability.
CREATE TABLE notification_deliveries (
    id BIGSERIAL PRIMARY KEY,
    notification_id BIGINT NOT NULL REFERENCES notifications(id) ON DELETE CASCADE,
    channel VARCHAR(16) NOT NULL CHECK (channel IN ('PUSH', 'EMAIL')),
    status VARCHAR(16) NOT NULL DEFAULT 'QUEUED'
        CHECK (status IN ('QUEUED', 'SENT', 'FAILED')),
    queued_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (notification_id, channel)
);

CREATE INDEX idx_notification_deliveries_status_queued
    ON notification_deliveries(status, queued_at, id);

CREATE TABLE payments (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    course_id BIGINT REFERENCES courses(id),
    amount NUMERIC(12,2) NOT NULL,
    provider VARCHAR(50) NOT NULL,
    transaction_code VARCHAR(100) UNIQUE,
    status VARCHAR(20) DEFAULT 'PENDING',
    paid_at TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL
);

-- API #58 fallback: BIGINT support model aligned with the legacy Study Server
-- users/courses/uploads keys. This checked-in schema does not prove live deployment.
CREATE TABLE support_requests (
    id BIGSERIAL PRIMARY KEY,
    course_id BIGINT NOT NULL REFERENCES courses(id) ON DELETE RESTRICT,
    student_id BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    status VARCHAR(24) NOT NULL DEFAULT 'OPEN'
        CHECK (status IN ('OPEN', 'IN_PROGRESS', 'WAITING_LEARNER', 'RESOLVED', 'CANCELLED')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMPTZ NULL
);

CREATE INDEX idx_support_requests_course_status_created
    ON support_requests(course_id, status, created_at DESC, id DESC);

CREATE TABLE support_messages (
    id BIGSERIAL PRIMARY KEY,
    request_id BIGINT NOT NULL REFERENCES support_requests(id) ON DELETE RESTRICT,
    author_id BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_support_messages_request_created
    ON support_messages(request_id, created_at, id);

CREATE TABLE support_message_uploads (
    message_id BIGINT NOT NULL REFERENCES support_messages(id) ON DELETE RESTRICT,
    upload_id BIGINT NOT NULL REFERENCES uploads(id) ON DELETE RESTRICT,
    asset_position BIGINT NOT NULL CHECK (asset_position >= 0),
    PRIMARY KEY (message_id, upload_id),
    UNIQUE (message_id, asset_position)
);

CREATE INDEX idx_support_message_uploads_message_position
    ON support_message_uploads(message_id, asset_position);
