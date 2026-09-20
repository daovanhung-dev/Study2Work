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

-- 02. COURSE & LEARNING

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

CREATE TABLE lesson_progress (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    lesson_id BIGINT REFERENCES lessons(id),
    status VARCHAR(20) DEFAULT 'NOT_STARTED',
    progress_percent SMALLINT DEFAULT 0,
    last_accessed_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL
);

-- 03. ASSESSMENT

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
    sort_order INT DEFAULT 0,
    score NUMERIC(5,2) DEFAULT 1
);

CREATE TABLE quiz_choices (
    id BIGSERIAL PRIMARY KEY,
    question_id BIGINT REFERENCES quiz_questions(id),
    choice_text TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT FALSE
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

-- 04. INTERACTION & SYSTEM

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

CREATE TABLE notifications (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NULL REFERENCES users(id),
    sender_id BIGINT NULL REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    type VARCHAR(30) NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL
);

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
