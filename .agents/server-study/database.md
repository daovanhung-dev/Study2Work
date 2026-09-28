# Study database status

```text
SCHEMA_STATUS: SOURCE_BACKED; LIVE_STATUS: NOT_VERIFIED_HERE
MIGRATION_DIRECTORY_STATUS: SOURCE_BACKED (refresh token and categories artifacts)
RUNTIME_DB_HELPER: VERIFIED
```

Current source establishes a Neon PostgreSQL connection URL in
`app/core/constants.py` and sync SQLAlchemy helpers. Register references
`users`; login/refresh references `users` and the source-backed
`refresh_tokens` table. Live metadata is still not verified here.

`infra/postgres/study-server/DB.sql` is a checked-in schema/design artifact and
`migrations/002_refresh_tokens.sql` and `migrations/003_categories.sql` are
idempotent migration artifacts; their
live application status is not established by source inspection alone.
Do not treat it as proof that every described table is available to the current
runtime.

Known discrepancy:
- current `constants.py` contains a user-specific `DB_SCHEMA` value, while the
  current engine path does not send `search_path` in the pooled startup package;
- runtime core parses `constants.URL_DATABASE`, uses `postgresql+psycopg` and
  preserves Neon SSL/channel-binding query options;
- `alembic.ini` references migration setup/directory that is absent and is not sufficient schema evidence.

`/api/v1/test/db` only declares `SELECT NOW()`; health readiness only reports configuration label and does not probe the DB.

`refresh_tokens` stores `user_id`, an HMAC `token_hash`, `expires_at`,
`revoked_at` and `created_at`. The raw refresh token is returned only to the
client during login/rotation and is never persisted. Rotation revokes the old
row and inserts the new row in the caller-owned transaction.

`categories` stores the public API #5 fields `id`, `name`, `slug`,
`description`, `locale` and `status`. API #5 reads rows where `status = 'ACTIVE'`
and `locale` exactly matches the requested locale; missing locale resolves to
`vi-VN`. The migration adds no seed data and has not been applied to live DB.

API #6 reads the source-backed `courses` columns `id`, `mentor_id`, `name`,
`description`, `thumbnail_url`, `price` and `status`, joined to the public mentor
projection in `users`. It filters `status = 'PUBLISHED'`, performs a separate
count/integrity read, and does not add a migration. The checked-in schema permits
nullable `mentor_id`; runtime treats any published course without a valid mentor
as an internal integrity failure. Course-category relation is not source-backed,
so the API rejects the `category` query rather than inventing a join.

Before any future migration/query task, require authoritative table/column/PK/FK/unique/index/status/delete/timestamp/tenant rules. Query helpers do not commit; transaction ownership belongs to the future/current business use case that performs the write.
