# Study database status

```text
SCHEMA_ARTIFACT_STATUS: PILOT_DDL_CHECKED_IN; LIVE_STATUS: NOT_VERIFIED_HERE
MIGRATION_DIRECTORY_STATUS: SOURCE_BACKED (refresh token, categories, uploads, lecture-upload relation, Content/version and course/content/lesson status-audit candidates)
RUNTIME_DB_HELPER: VERIFIED
```

Current source establishes a Neon PostgreSQL connection URL in
`app/core/constants.py` and sync SQLAlchemy helpers. Register references
`users`; login/refresh references `users` and the source-backed
`refresh_tokens` table. Live metadata is still not verified here.

At each PostgreSQL transaction begin, `build_engine()` applies only the
validated `Settings.db_schema` using transaction-local
`set_config('search_path', quote_ident(:schema), true)`. This is repeated for
each transaction on the pooled engine; setup errors propagate. The engine does
not append `public`, create the schema, or check live schema existence or
permissions. Schema is not sent in Neon startup options.

`infra/postgres/02_study_db.sql` is part of the checked-in V1-PILOT bootstrap
artifact. `migrations/002_refresh_tokens.sql`, `migrations/003_categories.sql`,
and legacy migrations `004_uploads.sql` and `005_lesson_uploads.sql` plus `006_contents.sql` are
migration artifacts; none establishes live application status by source
inspection alone.
The merged API
#08/#09 queries reference `courses` and `lessons`, but do not establish that
those relations exist in the configured live schema. Do not treat the pilot DDL
as proof that every described table is available to the current runtime.

Current runtime details:
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

API #34 reads `courses.mentor_id` for Mentor LECTURE uploads and `enrollments`
for Student SUBMISSION uploads with a course. It writes legacy BIGINT
`uploads` metadata after S3-compatible object upload and commits the database
transaction in the API view. `uploads` has a checked-in bootstrap definition
and migration 004; neither proves that the live schema has been updated.

API #47 reads `courses.id/mentor_id` and requires direct Mentor ownership without
filtering course status. It resolves API #34 `uploads` rows by ID, `owner_id`,
`purpose='LECTURE'` and the path `course_id`, then inserts a legacy `lessons`
row with decimal-string `content`, explicit `PUBLISHED` status and
`CURRENT_TIMESTAMP` for both required timestamps. For non-empty refs it writes
`lesson_uploads(lesson_id, upload_id, asset_position)` in the same transaction;
empty refs skip relation writes. The local source and fake-DB HTTP tests do not
verify that the live database has these legacy columns or migrations 004/005.

API #48 reads non-`DELETED` `lessons` with their `courses` parent, checks direct
`mentor_id` ownership, then reads ordered `lesson_uploads` links and resolves
matching `uploads` metadata under the same owner, `LECTURE` purpose and course.
It returns SQL NULL content as JSON null. It does not write or commit. Local API
tests do not verify live migration, schema or assignment support.

API #54 reads candidate `assignment_submissions` through `assignments`, `courses`
and `users`, scoping every row to the authenticated direct `courses.mentor_id`.
Its DERIVED file fallback matches the legacy `file_url` to `uploads.url` under
the same owner, `SUBMISSION` purpose and course; no submission-upload FK exists
in the inspected DDL. Inner joins omit null/orphan relations permitted by the
legacy DDL. Focused fake-DB tests do not verify the live assignment tables,
upload URL persistence or query plan.

API #55 reads one candidate `assignment_submissions` row by ID and uses LEFT
JOINs to `assignments`/`courses` so null or orphan parent relations remain
observable. It requires direct `courses.mentor_id` ownership under a DERIVED
fallback and resolves at most one `uploads` row with the same URL/owner/
`SUBMISSION` purpose/course predicates as API #54. Fake-row tests verify
application mapping only; no live schema, rubric relation, API #35 URL
persistence or query plan is verified.

API #49 reads `courses.id/mentor_id` then `contents` for the course, requiring direct Mentor ownership. The local `contents` DDL/migration 006 defines BIGINT course/parent keys, object JSONB payload, open text type/status, order and `deleted_at`; the query filters deleted rows and returns all statuses. The route returns a flat tree projection and does not write/commit. Fake-session tests and checked-in SQL do not verify live schema or migration deployment.

API #50 requires direct Mentor ownership, locks the `courses` row within its
transaction, allocates the next non-negative order among active root rows and
inserts one `contents` row. Initial `PENDING_REVIEW`, root placement, and
zero-based order are derived implementation choices; the view validates the
INSERT/RETURNING projection before commit. Focused tests use fake DB queries;
checked-in DDL/migration 006 do not verify live schema or deployment.

Before any future migration/query task, require authoritative table/column/PK/FK/unique/index/status/delete/timestamp/tenant rules. Query helpers do not commit; transaction ownership belongs to the future/current business use case that performs the write.


API #51 locks an active legacy `contents` row joined to its `courses` owner, archives the pre-update fields into `content_versions`, then updates `content_type`, `title`, `payload` and `status='PENDING_REVIEW'` in one caller-owned transaction. Migration 007 and the legacy `DB.sql` define the snapshot table with `(content_id, version_no)` primary key and `archived_by`; this is a DERIVED fallback, not an approved schema or live migration. The current row is treated as the implicit next version. `archived_by` is the updater who superseded the snapshot, not original-author provenance. AC-33 author and API #52/public published-version selection remain unresolved.

API #52 locks active `contents` and its `courses` row, then updates only `contents.status` for the DERIVED APPROVED↔PUBLISHED transitions; it does not write `content_versions`. Local fake-session tests verify the caller-owned transaction boundary, not live schema or deployment. Readiness beyond APPROVED, current revision selection, and AC-33 approval semantics remain unresolved.

API #53 locks the active Content and owning Course, checks for active direct
children, then sets `contents.deleted_at = CURRENT_TIMESTAMP` and returns the
tombstone timestamp through `DeleteResult`. The current child-block and
PUBLISHED guards are DERIVED; tests use fake DB rows and do not verify live
PostgreSQL behavior, timestamp interpretation, or migration deployment.

## API #56 Mentor submission grade

The endpoint reads/locks candidate assignment_submissions joined to assignments and courses, checks direct course ownership, then updates only score and status=GRADED. The request score is cast to candidate NUMERIC(6,2) after DERIVED validation against assignments.max_score; existing feedback is returned unchanged. A non-null file_url can resolve at most one uploads row by exact URL, owner, SUBMISSION purpose and course. The query/view owns the transaction and commits after response validation. rubric_items has no supported persistence target. DDL and fake-DB tests do not establish live schema or migration deployment.

## API #57 Mentor submission feedback

The endpoint locks candidate `assignment_submissions` and LEFT JOINs assignments/courses to validate required relations, checks direct `courses.mentor_id`, and updates only `feedback`. The owner condition is repeated in the UPDATE. `feedback_text` is a DERIVED wire key; repeated calls overwrite the single nullable feedback candidate. `attachments` is required by the catalog and accepted as an opaque string but has no persistence binding. A non-null `file_url` resolves at most one `uploads` row by exact URL, owner, `SUBMISSION` purpose and course for the reusable Submission response. The view commits after mapping validation and rolls back failures. DDL and fake-DB tests do not prove live schema or migration deployment.

## API #58 Mentor support requests

The current source adds a legacy BIGINT fallback in `infra/postgres/study-server/DB.sql` and migration 008: `support_requests` links a course and student, `support_messages` links a request and author, and `support_message_uploads` stores ordered message-to-upload links. The API scopes through `courses.mentor_id`; asset reads also constrain owner, course, role-appropriate purpose and `UPLOADED` status. The collection/detail shapes, these tables/columns, lifecycle values, ownership policy and attachment link are DERIVED implementation choices because the current runtime schema and live DB were not inspected. API #59 reads the same request/message/upload tables and does not add a migration. Migration 008 is a checked-in artifact only and was not applied to a live database.


## API #59 Mentor support-request detail

The endpoint reads `support_requests` with `courses` and `users`, then reads `support_messages`, `support_message_uploads` and `uploads`. It repeats direct course ownership in the thread query, orders messages by creation time/ID and assets by link position, and performs no write. These relations are the API #58 DERIVED local fallback backed by migration 008; live schema and migration application remain unverified.


## API #60 Mentor support reply

The endpoint locks `support_requests`, resolves `attachment_refs` against `uploads` by ID, Mentor owner, request course, `LECTURE` purpose and `UPLOADED` status, inserts `support_messages`, and writes ordered `support_message_uploads` rows with zero-based `asset_position`. It reloads the complete API #59 thread projection and commits only after response validation. It does not update request status. These tables are the API #58 migration 008 local fallback; no migration or live DB operation was performed by #60. Direct course-owner policy and JSON-array reference encoding remain DERIVED.

## API #61 Mentor support resolve

API #61 locks `support_requests` joined to its course/student projection, checks `courses.mentor_id`, then conditionally updates active statuses to `RESOLVED` and sets `resolved_at = COALESCE(resolved_at, CURRENT_TIMESTAMP)`. `RESOLVED` retries skip UPDATE; cancelled/unsupported state is rejected. It reads the full message and ordered upload projection using API #59's query in the same caller-owned transaction, validating before commit. BIGINT mapping and lifecycle rules are DERIVED from migration 008 and APIs #58–#60. Fake-DB tests and checked-in DDL do not prove live schema or deployment.

API #62 checks `courses.id/mentor_id`, then reads `users.id/full_name/avatar_url` through legacy `enrollments`, requiring `status='ACTIVE'` and `users.role='STUDENT'`. The roster query repeats direct Mentor ownership and returns distinct user rows ordered by `users.id`; it performs no writes or commit. The response cardinality, legacy schema/status and direct-owner rule are DERIVED from AC-25 and current Mentor conventions. Fake-DB tests and checked-in DDL do not prove live schema/deployment.

## API #63 Mentor notifications

API #63 checks one common directly owned course with ACTIVE enrollments for all parsed Student IDs, then writes one row per recipient to legacy `notifications` with shared UUID `operation_id` and the int64 `content` stored as decimal text. It inserts one `notification_deliveries` row per notification/channel with initial `QUEUED` status. Migration 009 is a local checked-in artifact only; it was not applied to a database. The operation grouping, CSV interpretation, common-course scope and delivery schema are DERIVED; no worker/provider is wired, and fake-DB tests do not verify PostgreSQL behavior or deployment.

## API #64 Mentor notification status

API #64 reads a `notifications` row and aggregates its `notification_deliveries`
rows by the notification's legacy BIGINT ID. The local query projects the
notification `operation_id`, `sender_id`, `created_at`, delivery row count,
counts by `QUEUED`/`SENT`/`FAILED`, and maximum `updated_at`; it performs no
mutation. This relies on API #63's checked-in migration 009 source, which has
not been applied or live-verified. Projection and status rules are DERIVED;
fake DB rows do not establish PostgreSQL behavior or deployment.

## API #65 Mentor course progress

API #65 checks `courses.id/mentor_id`, then reads distinct `users` rows through
legacy `enrollments` where status is `ACTIVE` and role is `STUDENT`. It counts
`PUBLISHED` lessons and reads `lesson_progress` only for those lessons. Because
the checked-in legacy DDL has no unique `(user_id, lesson_id)` constraint, the
query selects the latest row by `last_accessed_at DESC NULLS LAST`, then `id
DESC`. It aggregates completed count, percent sum and invalid status/range
count; the view treats missing/NULL percent as zero, uses floor division, and
returns zero for an empty lesson denominator. These schema/business choices are
DERIVED local fallbacks. No migration was added; live metadata, constraints and
deployment remain unverified, and V1-PILOT UUID/versioned tables are not used.

## API #66 Mentor course activity analytics

API #66 checks the same legacy `courses.id/mentor_id` owner relation, then
joins `lessons.course_id/status`, `users.id/role` and
`lesson_progress.user_id/lesson_id/last_accessed_at`. It counts distinct
Student/lesson pairs with a non-null access timestamp over PUBLISHED lessons,
distinct Student IDs in those pairs, and their maximum timestamp. This is a
DERIVED proxy over current progress state, not learning-event history; repeated
accesses may have been overwritten. No event ledger or migration was found in
the checked-in legacy DDL. V1-PILOT `last_event_id`, progress facts/snapshots,
`audit_events` and `outbox_events` are not used. Fake-DB tests do not verify live
schema or deployment.

## API #67 Mentor Student progress

API #67 checks the same legacy `courses.id/mentor_id` relation used by #65,
then requires an ACTIVE `enrollments` row joining a `users` row with
`role='STUDENT'`. It reads `lessons.id/course_id/name/sort_order/status` and
`lesson_progress.user_id/lesson_id/status/progress_percent/last_accessed_at/
completed_at`, filtering PUBLISHED lessons. Duplicate current-state rows use
`last_accessed_at DESC NULLS LAST`, then `id DESC`; a missing row maps to
NOT_STARTED/0 and the summary floors the average lesson percent with zero for
an empty set. This legacy BIGINT mapping and its rules are DERIVED from current
#65/#9 source and checked-in DDL. V1-PILOT UUID facts are not used. Fake DB
tests do not verify live metadata or deployment.


## API #68 Admin user list

API #68 queries the checked-in legacy `users` candidate: `id`, `full_name`, `email`, `role`, `avatar_url`, `phone`, `status`, `created_at` and `updated_at`. COUNT and page SELECT share optional role/status and keyword predicates; the page sorts by `id ASC` with fixed size 20. `password_hash` is not selected and there is no `bio` or deletion predicate. The query uses BIGINT legacy user IDs and does not join the structurally different V1-PILOT UUID identity/profile tables. These target/filter/order choices are DERIVED from local sources; fake-session tests do not prove live metadata, migration state or deployment.


## API #69 Admin user detail

API #69 reads a single row from the checked-in legacy BIGINT `users` candidate using `users.id = :user_id`, selecting `id`, `full_name`, `email`, `role`, `avatar_url`, `phone`, `status`, `created_at` and `updated_at`. It does not select `password_hash`, join the UUID V1-PILOT model, filter status or create a migration. This query target is a local candidate only; fake-session tests do not verify live metadata or deployment.

## API #70 Admin user update

API #70 updates `full_name`, `phone`, `avatar_url`, `role` and `updated_at` on the checked-in legacy BIGINT `users` candidate by `id`; it returns only `id`, `full_name`, `email`, `role`, `avatar_url`, `phone`, `status`, `created_at` and `updated_at`. It neither selects nor changes `password_hash`, `email`, `status` or `created_at`, and introduces no migration. The body fields, known role allowlist and target table selection are DERIVED from AC-31's update intent, current API #14 profile rules, application role usage and the legacy candidate. V1-PILOT UUID identity is incompatible; fake-session tests do not prove live schema or deployment.

## API #71 Admin user status

API #71 reads/locks and updates `status` and `updated_at` on the checked-in legacy BIGINT `users` candidate by ID, returning only the API #04 safe profile columns. When the target state is `SUSPENDED`, a second statement revokes unrevoked, unexpired rows from legacy `refresh_tokens` in the same transaction; `ACTIVE` does not restore prior tokens. The body enum and current-state transition gate are DERIVED; V1-PILOT UUID identity tables are not used. No migration is added, and fake-session tests do not verify live metadata, deployment or constraints.


## API #72 Admin user delete

API #72 updates `status='DELETED'` and `updated_at=CURRENT_TIMESTAMP` on the checked-in legacy BIGINT `users` candidate by ID. `DeleteResult.deleted_at` is a response alias of the returned `updated_at`; no dedicated column or migration is added. The conditional update leaves all user-linked FK rows and token rows intact. This is a DERIVED fallback over local DDL, not verified live metadata or an approved retention policy; V1-PILOT UUID identity remains separate.

## API #73 Admin course list

API #73 reads candidate legacy BIGINT `courses` and `users`. Count and page queries use the same optional exact status and mentor predicates; count also detects courses whose required mentor cannot be joined. The page projection selects course ID/name/description/thumbnail/price/status plus mentor ID/full name/avatar, ordered by course ID ascending with bound limit 20 and offset. No category relation or join is added; a valid category query is rejected before DB access with a DERIVED 422 fallback. No migration/write occurs. The source and fake-session tests do not verify the live schema or query plan.


## API #74 Admin course detail

The read query uses the checked-in legacy BIGINT candidate `courses LEFT JOIN users` by `courses.id`, with no status filter and no category/counter relation. It performs no mutation or commit. V1-PILOT UUID/versioned course DDL is not interchangeable with this API int64 projection. Local fake-session tests and checked-in DDL do not verify live schema, grants, or deployment.

## API #75 Admin course update

API #75 targets the checked-in legacy BIGINT `courses` candidate, updating `name`, `description`, `thumbnail_url`, `price` and `updated_at` by ID, then reading the same Course/mentor projection used by API #74. It adds no table, migration or DDL change; V1-PILOT UUID/versioned courses remain separate. `NUMERIC(12,2)` and `VARCHAR(200)` constraints are local validation fallbacks, not live metadata evidence. Fake-session tests do not verify schema, grants, migration state or deployment.

## API #76 Admin course status

API #76 targets the checked-in legacy BIGINT `courses/users` candidate. Migration 010 adds `course_status_audit_logs` with `course_id`/`actor_user_id` BIGINT foreign keys, nullable `previous_status`, required `new_status`, and a database timestamp; indexes support course/actor history lookup. The view updates `courses.status/updated_at`, inserts the audit row, and reads Course projection in one transaction. This is a `DERIVED` physical fallback for AC-32's audit intent. V1-PILOT `audit_events` and versioned courses use UUID IDs and are not used. Checked-in DDL/migration and fake DB tests do not prove live schema, constraints, migration state, grants or deployment.

## API #77 Admin course delete

API #77 targets the checked-in legacy BIGINT `courses` candidate. It locks a non-`DELETED` row, checks all matching `enrollments`, active `contents`, `lessons`, `quizzes` and `assignments`, then updates only `courses.status='DELETED'` and `updated_at`. `DeleteResult.deleted_at` maps from the returned timestamp, following #72. The blocker set, `DELETED` marker and timestamp alias are DERIVED; no DDL, migration, cascade or audit relation is added. V1-PILOT UUID courses/`archived_at` are not used. Fake DB tests do not prove live tables, locks, FK metadata or deployment.

## API #78 Admin pending Content queue

API #78 reads the checked-in legacy BIGINT `contents` candidate; its query requires `status='PENDING_REVIEW'` and `deleted_at IS NULL`, with optional exact `content_type` and `course_id` predicates. The count and page use identical predicates; page order is `id ASC`, limit 20 and a derived 1-based offset. No join to `content_versions` is made because current #50/#51 writers place the pending state on the logical `contents` row and the catalog gives no revision selector. Checked-in DDL and fake DB tests do not prove live schema or deployment.

## API #79 Admin Content detail
API #79 reads `contents.id`, `course_id`, `content_type`, `title`, `payload`, `status`, `parent_id`, and `content_order` from the checked-in legacy BIGINT candidate, constrained by `id=:content_id AND deleted_at IS NULL`. It does not query `content_versions` or join a user/course to infer author. The query is read-only and bound; no schema/migration change is introduced. DDL and fake DB tests do not prove live schema/deployment.
## API #80 Admin Content approval

API #80 reads and updates one active legacy BIGINT `contents` row. It locks by ID with `deleted_at IS NULL`, requires current status `PENDING_REVIEW`, then updates to `APPROVED` and returns the eight Content fields. It appends `content_review_audit_logs` in the same transaction. Migration 011 and the matching `DB.sql` table define BIGINT Content/Admin FKs, previous/new status, nullable `reason`, timestamp, and indexes by Content/actor plus time. This is a DERIVED candidate; fake-session tests and checked-in SQL do not verify live schema or deployment. The V1-PILOT UUID review decisions remain a separate model.

## API #81 Admin Content rejection

API #81 reuses the legacy BIGINT `contents` candidate and migration 011's `content_review_audit_logs`; it makes no schema change. The row lock requires an active `PENDING_REVIEW` Content, then the status update returns the eight Content fields. One audit-candidate insert stores `content_id`, authenticated `actor_user_id`, `previous_status`, `new_status='REJECTED'` and the request `reason`; this single row is the DERIVED physical destination for both review reason and decision record. The local fake-session tests and DDL do not verify deployed relations, FKs, grants or migration state. V1-PILOT UUID decisions remain separate, and exact revision continuity with #79 is unavailable.

## API #82 Admin lessons list

API #82 reads only the checked-in legacy BIGINT `lessons` candidate: `id`, `course_id`, `name AS title`, `content`, `video_url`, `sort_order AS order`, and `status`. Optional `course` and `status` are bound exact-match filters; order is `course_id ASC NULLS LAST, sort_order ASC NULLS LAST, id ASC`. There is no `type` mapping, join, count, pagination or mutation. The legacy DDL allows `course_id`, `sort_order`, and `status` to be NULL even though the reusable Lesson projection requires them; local mapping failure returns safe 500. V1-PILOT UUID lesson/chapter/course-version fields are not interchangeable. The checked-in DDL and fake DB HTTP tests do not prove deployed schema or live behavior.


## API #85 Admin lesson status

Migration 012 adds `lesson_status_audit_logs` with BIGINT foreign keys to the checked-in legacy `lessons` and `users` candidates, nullable `previous_status`, required `new_status`, a database timestamp and lesson/actor history indexes. API #85 inserts the row only when `lessons.status` changes, in the same Session transaction as the status/updated_at update. The table and status enum are DERIVED local fallbacks; migration source plus fake DB tests do not prove live schema, migration application, grants or deployment. V1-PILOT UUID Lesson/audit records remain separate.

## API #86 Admin lesson delete

API #86 uses the checked-in legacy BIGINT `lessons` candidate. It locks a non-`DELETED` Lesson, checks `lesson_progress`, `resources`, and `lesson_uploads` with EXISTS predicates, then sets `lessons.status='DELETED'` and `updated_at=CURRENT_TIMESTAMP` when there are no blockers. The DB-returned `updated_at` maps to `DeleteResult.deleted_at` by API #77 precedent. These blocker/marker/timestamp choices are DERIVED; no child or #85 audit row is deleted and no migration is added. Admin #82–#85 and the direct Mentor #48/Resource #12 readers hide or reject the tombstone. Fake-session tests do not prove live FK metadata, SQL execution, lock behavior, migration state or deployment; V1-PILOT UUID Lesson relations remain separate.


## API #87 Admin quiz list

The local API reads only the checked-in legacy BIGINT `quizzes` candidate (`id`, `course_id`, `name`, `time_limit_minutes`, `passing_score`, and `status`). Migration 013 adds nullable `quiz_questions.question_type` and `quiz_choices.sort_order` to the local legacy BIGINT candidate for API #88. API #87 still does not query child tables and returns `questions=[]` as a metadata-only projection. The UUID V1-PILOT `assessments`/question/options model is not interchangeable with int64 quiz IDs. Checked-in DDL/migration and fake DB tests do not verify live schema or deployment.

## API #88 Admin quiz create

Migration 013 adds `quiz_questions.question_type VARCHAR(32)` (nullable for legacy rows, checked against the local candidate labels) and `quiz_choices.sort_order INT NOT NULL DEFAULT 0` to the checked-in legacy BIGINT schema. Bootstrap `DB.sql`, DB table guide and ERD carry the same candidate fields; API #88 always writes `question_type` and preserves zero-based question/choice input order. These fields and labels are DERIVED from the logical nested Quiz contract plus V1-PILOT vocabulary, without mixing UUID rows or IDs. Existing rows are not backfilled. Local migration/DDL does not prove live schema, application, grants or deployment.

## API #89 Admin quiz update

API #89 uses the same checked-in legacy BIGINT `quizzes`, `quiz_questions`,
`quiz_choices`, `quiz_attempts` and `quiz_answers` candidates as #87/#88. It
locks the quiz and existing child rows, checks attempt/answer references, then
updates the quiz and replaces choices/questions in the caller-owned transaction.
It adds no table, column or migration. The body, history refusal, lock strategy,
course move and tombstone handling are DERIVED; neither the candidate DDL nor
fake-session tests verify deployed schema, foreign-key enforcement or live
PostgreSQL concurrency behavior. V1-PILOT UUID assessment tables remain separate.

## API #90 Admin quiz delete

API #90 queries the checked-in legacy BIGINT candidates `quizzes`,
`quiz_questions`, `quiz_choices`, `quiz_attempts` and `quiz_answers`; it adds no
schema or migration. It locks Quiz → questions → choices and checks attempt
rows plus answers referencing those child IDs. With any history it updates
Quiz `status`/`updated_at`; without history it deletes choices → questions →
Quiz. The `DELETED` value, timestamp meaning, answer-only safeguard and
hard-delete branch are DERIVED. Legacy DDL has no `deleted_at` and does not
prove deployed constraints, live schema or PostgreSQL locking behavior;
V1-PILOT UUID assessment tables remain separate.

## API #91 Admin quiz statistics

API #91 reads the checked-in legacy BIGINT `quizzes` and `quiz_attempts`
candidate in one grouped LEFT JOIN aggregate over `quiz.id`, `passing_score`,
attempt `id`, `quiz_id`, `submitted_at` and `score`. It adds no schema or
migration, and does not read `quiz_answers`. The runtime does not filter quiz
status, preserving a retained tombstone's history. Metric definitions,
nullable-threshold handling, pass-rate calculation and the `QuizStatistics`
response are DERIVED against diagram/catalog `ApiEnvelope<Quiz>`. Legacy DDL
and fake DB tests do not prove live schema, PostgreSQL query execution,
deployment or grants; UUID V1-PILOT assessments remain separate.

## API #92 Admin notification list

API #92 reads the checked-in legacy BIGINT `notifications` and API #63/migration-009 `notification_deliveries` candidates. It groups delivery rows by notification ID, derives ordered channels plus QUEUED/FAILED/SENT counts, and includes only notifications with at least one delivery row so the required response fields can be projected. The response has one item per legacy notification row; no campaign grouping or recipient/sender fields are selected. No schema or migration was added. This Page/channel/status mapping is DERIVED; legacy DDL and fake-session HTTP tests do not verify live PostgreSQL schema, migration application, worker state or Admin campaign grain. V1-PILOT UUID learner notifications/deliveries remain separate.


## API #93 Admin notification create/send

API #93 checks explicit recipients against `users.id`, then writes one legacy BIGINT `notifications` candidate row per recipient with shared UUID `operation_id`. It inserts one `notification_deliveries` row per notification/channel with `QUEUED` status and commits the full batch before HTTP 202. `type` is NULL; channel is stored in the delivery table. The local source caps title at the candidate `VARCHAR(200)` limit and preserves content in TEXT. Migration 009 and checked-in DDL are not live-schema evidence; no provider/worker is wired. Audience/channel/validation rules, per-recipient grain, response metadata, and Operation linkage remain DERIVED/open.


## API #94 notification update candidate mapping

API #94 reads/locks legacy BIGINT `notifications` and `notification_deliveries` candidates, then updates only `notifications.title` and `notifications.content`. It preserves `user_id`, `sender_id`, `type`, `is_read`, `created_at`, and every delivery row. A target needs at least one delivery and every delivery must remain `QUEUED`; channels/status response projection comes from those locked rows. This is a DERIVED mapping from checked-in DDL, not proof of live schema. No migration is added, and V1-PILOT UUID notification tables are not used.

## API #95 notification delete candidate mapping

API #95 locks one legacy BIGINT `notifications` row and its `notification_deliveries`, requiring at least one delivery and all statuses `QUEUED` before deleting the path-selected parent. Migration 009/checked-in DDL declare `ON DELETE CASCADE`, so the local candidate removes that parent's delivery rows; `DELETE RETURNING id, CURRENT_TIMESTAMP AS deleted_at` supplies DeleteResult. The row-grain, queued-only rule, hard delete and response timestamp mapping are DERIVED. It leaves batch siblings sharing `operation_id` untouched and does not call a worker/provider. No schema change is added; live cascade/schema/deployment are unverified. V1-PILOT UUID learner tables are separate.

## API #96 notification status read

API #96 reads one legacy BIGINT `notifications` candidate and its grouped
`notification_deliveries` rows in a single SELECT keyed by `notification_id`.
It projects ordered channels and QUEUED/FAILED/SENT status using API #92's
local policy. Missing parent or no delivery rows produces an empty result and
the view returns 404. No DDL/migration is added. Table selection, row grain,
status precedence, retry semantics and no-delivery behavior remain DERIVED or
SOURCE_REQUIRED; checked-in migration/DDL and fake-DB tests do not establish
live schema or deployment. V1-PILOT UUID notification tables are not queried.

## API #97 reported-discussion queue

API #97 adds the local DERIVED `discussion_reports` migration candidate in
014, keyed by `discussion_id BIGINT` (FK to `discussions.id`, ON DELETE
RESTRICT) and `reporter_user_id BIGINT` (FK to `users.id`, ON DELETE RESTRICT).
This preserves report evidence; API #100 must reconcile this FK before any
hard delete. The queue reads legacy
`discussions` plus its author from `users`; the report relation contributes
OPEN/IN_REVIEW visibility, exact-match reason/severity filters and latest
matching report ordering. Count and page queries both use the same report
predicate and count distinct Discussion IDs. The status set, report grain,
legacy FK targets and required Discussion title/comments projection are local
fallbacks. Checked-in DDL/migration and fake-session tests do not establish
live schema, deployment or a producer that inserts reports.
