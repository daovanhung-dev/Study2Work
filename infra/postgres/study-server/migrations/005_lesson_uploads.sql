CREATE TABLE IF NOT EXISTS lesson_uploads (
    lesson_id BIGINT NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    upload_id BIGINT NOT NULL REFERENCES uploads(id),
    asset_position BIGINT NOT NULL CHECK (asset_position >= 0),
    PRIMARY KEY (lesson_id, upload_id),
    UNIQUE (lesson_id, asset_position)
);
