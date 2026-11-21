# Study database + security core

## Database — `app/core/database.py`

### `build_database_url(config)`
Parses `Settings.database_url` from `constants.URL_DATABASE`, converts the
driver to `postgresql+psycopg`, and preserves Neon query options such as SSL
and channel binding. The URL stays a `SecretStr` until URL construction.

### `build_engine(config)`
- `pool_pre_ping=True`.
- pool size/max overflow from settings.
- PostgreSQL engines register a SQLAlchemy `begin` listener that applies only
  `Settings.db_schema` with `SELECT set_config('search_path', quote_ident(:schema), true)`.
- The setting is transaction-local and is applied at every transaction begin,
  which supports Neon transaction pooling. Schema setup errors propagate and
  prevent the transaction from continuing to business queries.
- Schema is not sent through connection startup options. No `public` fallback
  is appended and the listener does not create or verify the schema.

### `build_session_factory(engine)`
Sync `Session`, `autoflush=False`, `expire_on_commit=False`.

### `get_engine()` / `get_session_factory()`
Process-cached factories (`lru_cache(maxsize=1)`).

### `SessionLocal()`
Legacy compatibility wrapper returning a new Session.

### `get_db_from_factory(factory)` / `get_db()`
Yield request-scoped Session and always close. No implicit commit/rollback policy beyond Session close.

### `execute_query(db, query, params=None)`
Executes `text(query)` with dictionary/named parameters. **Does not commit.**

### `query_one` / `query_many`
Return mapping rows as plain dict(s). Transaction ownership remains with caller.

## Config — `app/core/config.py`

`Settings` lấy default từ `app/core/constants.py`, dùng `URL_DATABASE` làm DB
connection chính và validates app env, docs, CORS, schema/pool, optional Redis,
JWT keys/algorithm/expiry/issuer/audience and refresh pepper. Các field DB rời
được giữ optional để tương thích constructor cũ nhưng không được engine dùng.
Model không tự đọc `.env` hoặc process environment; caller vẫn có thể truyền
override tường minh khi khởi tạo `Settings(...)`.

Important validators:
- CORS accepts list or comma-separated string.
- DB schema only alphanumeric/underscore.
- HS256 requires secret; ES256 requires private and public key at settings validation time.
- `get_settings()` is cached/lazy; `_LazySettings` preserves legacy uppercase-style access.
- Settings field validators use Pydantic's custom validation errors;
  construction sanitizes Pydantic validation failures as a generic
  `RuntimeError`. Configuration is checked outside an HTTP request and does
  not produce an `error_response(...)` or `JSONResponse`.

## Password — `app/core/security/password.py`

- `hash_password`: Argon2id (`time_cost=3`, 64 MiB, parallelism 1).
- `verify_password`: Argon2 hashes or legacy bcrypt `$2a/$2b/$2y`; unknown formats false.
- An optional legacy algorithm argument remains accepted for older callers; new
  password creation always uses Argon2id.
- `needs_password_rehash`: true for non-Argon2 or invalid/outdated Argon2 params.

## Access token — `security/access_token.py`

### `create_access_token`
Creates signed JWT with `sub`, `type=access`, `roles`, `jti`, `iat`, `exp`, `iss`, `aud`; custom claims cannot overwrite reserved claims.

### `decode_access_token`
Verifies configured algorithm, issuer/audience and required claims. Non-ASCII
input is rejected as an authentication 401. PyJWT validation errors are caught
by the decoder and mapped to its existing authentication 401 response. A
`TypeError` from JWT claim decoding propagates to the application auth facade,
which maps it through the existing authentication `error_response(...)` path
with 401. Missing signing/verification configuration remains a safe internal
`error_response`.

Signing/verification key selection:
- ES256: private key signs, public key verifies.
- HS256: shared secret.

## Refresh token — `security/refresh_token.py`

- `generate_refresh_token`: `secrets.token_urlsafe(48)` opaque token.
- `hash_refresh_token`: HMAC-SHA256 with configured pepper before DB storage.
- `compare_refresh_token`: constant-time `hmac.compare_digest`.
- Missing refresh pepper becomes a safe internal `error_response`.

Application-level auth ownership is `app/utils/auth.py`: it parses Bearer
headers, validates access claims, applies the shared
`validate_current_user_request(...)` guard for one role or a sequence of
accepted roles, and rejects blank refresh-token input. APIs #4/#13/#14 require
`STUDENT`; APIs #46–#63 require `MENTOR`; API #34 accepts `STUDENT` or `MENTOR` and
then matches the role to upload purpose. APIs #47–#50 bind the numeric subject to
`courses.mentor_id` and do not include assigned courses. Existing single-role callers retain
their behavior. It delegates JWT signing/decoding and
refresh-token generation/hashing to the primitives above. Authentication
failures retain the existing `error_response(...)` mappings. Shared input
helpers return `ErrorDetail` or a typed failure result for their API
validator/view to map through `error_response(...)`. Request parsing and type
failures use FastAPI's registered request-validation handler, which serializes
them through the existing response helpers. Study Server source and tests do
not use built-in `ValueError`; errors outside HTTP retain internal error
handling rather than becoming `JSONResponse`.

## Critical absence

Current register and auth SQL reference `users`; login/refresh also reference
`refresh_tokens`; APIs #08/#09 also query `courses` and `lessons`; API #34 reads
`courses`/`enrollments` and writes `uploads`; API #47 reads `courses`/`uploads`,
writes `lessons`, and writes ordered `lesson_uploads` links in the same
transaction; API #48 reads `lessons`, `courses`, `lesson_uploads` and scoped
`uploads` metadata; API #49 reads `courses`/`contents` and validates the active
Content tree without writing; API #50 locks its `courses` row, reads active root
order and inserts one `contents` row in its caller-owned transaction; API #55
reads candidate `assignment_submissions` through LEFT JOINs to assignments/
courses and a constrained UploadAsset lookup without writing/committing. Legacy
BIGINT migrations 004–006 are checked-in artifacts only; source inspection does
not verify live schema, migration application or table metadata.
`infra/postgres/02_study_db.sql`, migration artifacts and DD pages are not
sufficient runtime evidence when they conflict with live metadata. Register and auth views own
their lookup, password checks, token persistence and commit/rollback behavior.
API #3, API #4, API #13, API #14 and API #46 use app-level token/auth helpers
from `app/utils/auth.py`; all access-JWT protected APIs use the shared
role-aware guard.

API #53 also uses the shared `MENTOR` guard, locks active `contents` and its
`courses` row, and sets the checked-in legacy `contents.deleted_at` tombstone.
API #54 uses the same guard and reads candidate submissions through assignments
and directly owned courses; its upload lookup is a DERIVED URL/owner/purpose/course
match. These are local source behaviors only; live schema and migration state are
unverified.

API #55 uses the same explicit `MENTOR` guard, checks the direct `courses.mentor_id`
fallback after reading one submission, and maps null/orphan required relations to
a safe 500. Its file metadata fallback matches API #54; no rubric query or
legacy assignment-rubric relation is source-backed. The view owns read
orchestration and rollback-on-error; it never commits.

API #56 owns its write transaction: it locks the submission, checks the direct owner,
validates the derived score range, updates only score/status, resolves the response,
and commits after projection validation. Failure branches roll back. Its query uses
checked-in legacy DDL candidates; live schema and rubric persistence remain unverified.

API #57 also owns its write transaction. It locks the submission with LEFT JOINs to
assignment/course, validates the direct `courses.mentor_id` owner, and repeats that
owner predicate while updating only `assignment_submissions.feedback`. It validates
the shared Submission and constrained UploadAsset projection before commit; query,
relation, projection and commit failures roll back. `feedback_text` is DERIVED from
the catalog descriptor; required `attachments` is accepted but unused because there
is no supported target. The checked-in DDL and fake-DB tests do not verify live schema.

API #58 is read-only. It authenticates with the shared `MENTOR` guard before DB
access, checks a supplied course for direct ownership, and repeats
`courses.mentor_id = :mentor_id` in the collection and nested-message queries.
Its derived support schema links requests to courses/students, messages to
authors, and ordered uploads to messages. Upload resolution also constrains
author, course, role-purpose and `UPLOADED` status. No commit is issued; errors
roll back the read transaction. Fake-DB tests do not verify live constraints or
schema deployment. API #59 reuses that local schema and performs read-only request/thread
queries with the direct owner predicate repeated; it has no commit path.


API #60 applies caller-owned transaction rules to the local support fallback: it authenticates MENTOR before DB access, locks `support_requests`, checks direct course owner, validates ordered uploads, inserts `support_messages` and `support_message_uploads`, then reloads the full thread through the API #59 query/projection. It commits after the envelope projection is valid and rolls back query, link, mapping or commit failures. Its attachment encoding and direct-owner policy are DERIVED; fake-DB tests do not establish live constraints/schema.

## API #61 Mentor support resolve

API #61 authenticates through `validate_current_user_request(..., role="MENTOR")` before DB access and maps numeric JWT `sub` to the local direct owner predicate `courses.mentor_id`. It locks the support request row, repeats the owner predicate on UPDATE, and owns the commit/rollback boundary. The local BIGINT support schema and active-state transition matrix are DERIVED fallbacks; tests use fake sessions and do not verify live schema or migration 008 deployment.

## API #62 Mentor course students

API #62 authenticates through the same MENTOR guard, parses the raw course path as signed-int64, checks the local direct-owner predicate and reads distinct Student rows through `ACTIVE` enrollments. It is read-only and does not commit. The `UserSummary[]` contract, legacy schema/status and direct-owner policy are DERIVED; fake-session tests do not verify live schema/deployment.

## API #63 Mentor notifications

API #63 authenticates with the shared MENTOR guard before parsing or database work. Because the catalog body omits `course_id`, its DERIVED scope query requires the complete Student recipient set to share an ACTIVE enrollment roster in a course owned by the JWT `sub`; each notification insert is still keyed to the authenticated sender. Notification rows and all channel outbox rows are written in one transaction, and failures roll back before returning. CSV encodings, common-course policy and local outbox tables are DERIVED; fake-session tests do not establish live schema, migration deployment, or delivery worker/provider behavior.

## API #64 Mentor notification status

API #64 authenticates MENTOR before querying and scopes the persisted
notification by its `sender_id` against numeric JWT `sub`. Its SQL reads the
local API #63 legacy BIGINT notification and channel-outbox rows and performs
no writes. Sender mismatch returns 403; absent notification/dispatch returns
404; malformed projections and query failures return safe 500 with rollback.
The owner relation, aggregation policy and migration 009 source are DERIVED;
fake-session tests do not verify live schema or deployment.

## API #65 Mentor course progress

API #65 authenticates through the shared MENTOR guard before DB access, parses
raw signed-int64 path text, checks `courses.mentor_id` against JWT `sub`, and
repeats that owner predicate in the read-only roster aggregate. It exposes no
progress data for another owner's course. ACTIVE enrollment, STUDENT role,
PUBLISHED lesson set, latest progress row, formula and one-page response are
DERIVED. Focused HTTP tests use fake sessions and do not prove live schema or
deployment; catalog `Page<Course>` remains inconsistent with the local progress
response.


## API #68 Admin user list

API #68 uses the shared JWT guard with role `ADMIN` before any DB access. The list is read-only and never commits; SQL only selects the safe API #04 profile columns and excludes `password_hash`. Query/mapping failures roll back and return a safe `DESIGN_INTERNAL_ERROR`. Mapping the Admin user-management permission to the `ADMIN` claim is DERIVED because checked-in DDL has no dedicated permission relation or tenant policy. PII visibility/audit policy, live schema and deletion visibility remain unverified; tests use fake DB sessions.


## API #69 Admin user detail

API #69 runs the shared `ADMIN` JWT guard before raw path parsing and before user lookup. It is read-only and does not commit; no-row/invalid path return catalog 404, while query or profile projection failures roll back and return safe `DESIGN_INTERNAL_ERROR`. SQL selects only the API #04 profile allowlist and excludes password/token credentials. The role-claim-to-user-management mapping is DERIVED from #68; separate permission/tenant/MFA and PII/audit policy remain unverified.

## API #70 Admin user update

API #70 authenticates with the shared `ADMIN` claim before path/body validation and DB access. It performs one profile/role UPDATE and commits after safe response projection validation; query, mapping and commit failures roll back and return safe `DESIGN_INTERNAL_ERROR`. The SQL excludes credentials and leaves status/session rows unchanged. Role values and permission mapping are DERIVED; no audit, tenant/MFA, self-role-change or last-Admin policy is source-backed. Existing access JWT role claims are not revoked by this update. Tests use fake DB sessions; live schema and security policy are unverified.

## API #71 Admin user status

API #71 authenticates the shared `ADMIN` claim before DB access, then locks and updates the legacy `users` candidate. Suspending revokes only rows in `refresh_tokens` that are unrevoked and unexpired, within the same transaction. API #03 login/refresh also require ACTIVE status, while the current access-JWT guard validates token claims/roles without querying account status or revocation; existing access tokens may therefore work until expiry. The body/status allowlist, role-to-permission mapping and token policy are DERIVED; no tenant/MFA, self/last-admin, audit or access-token blacklist rule is source-backed. Fake-session tests do not prove live schema or policy.


## API #72 Admin user delete

API #72 uses the shared `ADMIN` claim before DB access, then sets the candidate legacy `users.status` to `DELETED`; no dependent row or refresh-token row is deleted. API #03 login/refresh require ACTIVE and therefore reject new sessions after the marker. The access-JWT guard does not query current user status or revoke access tokens, so existing access JWTs may remain usable until expiry. The marker, Admin permission mapping and lack of immediate token revocation are local DERIVED/current-source behavior; tenant/MFA, self/last-admin, PII/audit and owner approval remain unverified.

## API #73 Admin course list

API #73 applies the shared `ADMIN` JWT guard before raw query parsing or DB access. The endpoint is read-only and does not commit; query/count/course projection failures roll back and return safe `DESIGN_INTERNAL_ERROR`. SQL only selects the Course projection and mentor `id/full_name/avatar_url`, without other user PII. The shared role establishes role enforcement only; mapping `ADMIN` to AC-32's course-management permission is DERIVED, and separate permission/scope policy remains open. Valid category IDs receive a 422 fallback before DB due to absent relation. Tests use fake sessions; live schema and authorization policy are unverified.


## API #74 Admin course detail

API #74 uses `validate_current_user_request(..., role="ADMIN")` before path parsing or query, matching APIs #68–#75. The catalog/AC-32 phrase “course-management permission” has no dedicated policy source; enforcing only the shared role is a `DERIVED` local fallback, not proof of the finer permission. The read selects only Course and `UserSummary` candidate fields, maps through the shared allowlist, and rolls back query/projection failures without committing.

## API #75 Admin course update

API #75 calls `validate_current_user_request(..., role="ADMIN")` before raw signed-int64 parsing and DB access. This confirms the shared role only; the catalog phrase “course-management permission” has no dedicated policy source. The view owns its UPDATE/readback transaction and rolls back on missing projection or DB/commit failure. SQL values are bound parameters and only metadata/timestamp columns are written. Body and numeric validation are DERIVED from the DD/legacy DDL candidate; fake-session tests do not establish live schema or authorization policy.

## API #76 Admin course status

API #76 calls `validate_current_user_request(..., role="ADMIN")`; shared auth returns numeric JWT `sub`, which is bound as the audit `actor_user_id` candidate. This enforces the role only; AC-32's separate course-management permission, tenant/scope and current-account-status checks have no policy source. It locks the course before mutation, and the status update plus audit INSERT are atomic in the caller-owned transaction. Audit data is limited to course, actor, previous/new status and timestamp; no token or unrelated user PII is recorded. Migration/schema and DB-level immutability remain unverified.

## API #77 Admin course delete

API #77 authenticates shared role `ADMIN` before path parsing, dependency checks or mutation; the separate AC-32 course-management permission remains unverified. It locks one candidate legacy course and uses `EXISTS` checks without loading enrollment identities, learner data or content payloads. Any enrollment or active learning content blocks with catalog 422; otherwise the view writes the `DELETED` marker and DB timestamp in the same transaction. Failures roll back and return safe catalog errors. Marker/dependency policy is DERIVED; fake sessions do not verify live FK/locking behavior or deployment. Linked API #76 can still replace the status, and Mentor writer behavior was not changed in this one-API task.

## API #78 Admin pending Content queue

API #78 authenticates shared role `ADMIN` before raw query validation or DB access; no dedicated moderation permission is source-backed. The endpoint is read-only, binds exact type/course filters, uses matching count/page predicates, and rolls back read or projection failures before returning a safe error. SQL selects only the reusable Content projection from active rows. Tests use fake DB sessions and do not establish live schema, grants, deployment or policy. Page cardinality/pagination are DERIVED against the singular catalog response.

## API #79 Admin Content detail
API #79 authenticates shared role `ADMIN` before parsing the raw signed-int64 path or accessing the database. It issues one parameterized read against active `contents` and selects only the eight catalog Content fields. Missing/soft-deleted and invalid/out-of-range IDs map to 404; SQL or malformed projection errors roll back and return a safe 500. The view does not commit or mutate. Fake DB tests do not establish live schema, grants, deployment, or moderation-specific permission; AC-33 author/version reads remain unimplemented pending a supported source/contract.
## API #80 review transaction and actor

- API #80 requires `validate_current_user_request(..., role="ADMIN")` before path parsing or database access. The numeric JWT `sub` is the audit actor; it is never accepted from request data.
- The view locks the active Content row, validates `PENDING_REVIEW`, updates to `APPROVED`, inserts the review audit candidate and commits only after response projection validation. Query, audit, projection or commit errors trigger rollback and safe 500.
- Migration 011's BIGINT `content_review_audit_logs` is a DERIVED local schema candidate, not live DB evidence. The reason column is nullable for the bodyless approval and is only a possible future #81 destination.

## API #81 rejection transaction and reason

- API #81 uses the explicit shared `ADMIN` guard before raw signed-int64 path parsing or DB access; actor identity comes from numeric JWT `sub`, never the request body.
- The view locks active Content, requires `PENDING_REVIEW`, updates status to `REJECTED`, and inserts one `content_review_audit_logs` row with actor, previous/new status and required request reason. Status and reason commit atomically after the Content projection validates; failures roll back and return safe 500.
- Reusing the migration 011 nullable reason column for this decision row is a DERIVED physical mapping. Fake-session tests do not establish live FK/schema/deployment or dedicated moderation permission; #79 revision identity remains open.


## API #87 Admin quiz read boundary

API #87 authenticates through the shared `ADMIN` guard before query parsing or database access. SQL is bound and selects only quiz metadata; it does not read answer-key data. AC-35's separate quiz-management permission has no source-backed claim/policy and is not enforced. The view is read-only and rolls back query/projection failures before returning a safe envelope. Fake DB tests do not establish live grants/schema or deployment.

## API #88 Admin quiz create

API #88 authenticates shared role `ADMIN` before reading or validating the raw request body; the numeric JWT `sub` is not accepted from the body. Parameterized course lookup and parent/question/choice inserts execute in the caller-owned transaction. The view builds and validates the full response before commit, and query, returned-row, projection or commit failures trigger rollback and a safe error envelope. Migration 013’s question-type and choice-order columns are DERIVED local candidates, not live schema evidence. The Admin response may include `is_correct`; Student API #28 must not expose it. AC-35 fine-grained permission and live schema/grants/deployment remain unverified.

## API #89 Admin quiz update

API #89 authenticates the shared `ADMIN` role before raw path/body parsing or
database access; no separate AC-35 quiz-management permission is source-backed.
The view owns one transaction and locks the active Quiz plus existing question
and choice rows before its attempt/answer history check. It refuses replacement
when history exists, then updates the parent and replaces children, validating
the complete response before commit. Errors after transaction start roll back.
The body, row-lock order, tombstone/history policy and course move are DERIVED;
fake-session tests do not establish PostgreSQL lock/FK behavior, live schema,
grants, migration deployment or authorization policy.

## API #90 Admin quiz delete

API #90 uses `validate_current_user_request(..., role="ADMIN")` before raw
positive-int64 path parsing or database access. It uses bound SQL constants
and one caller-owned transaction; row locks cover Quiz, questions and choices.
Attempt/answer history selects soft delete; the no-history branch deletes
children before parent. Exact returned child ID sets and response identity/time
are checked before commit. Query, mapping, mutation and commit failures roll
back and return safe catalog errors. Shared ADMIN does not establish AC-35's
fine-grained permission. Fake DB tests do not verify live PostgreSQL grants,
constraints, schema or the coordinated API #29 create-attempt race.

## API #91 Admin quiz statistics

API #91 calls `validate_current_user_request(..., role="ADMIN")` before
positive-int64 path parsing or database access. Fine-grained AC-35
quiz-management permission has no source-backed policy. The view performs one
read-only aggregate query; it rolls back missing-row, SQL and projection
failures and never commits. The `QuizStatistics` DTO, metrics, tombstone
visibility and invalid-path-to-404 mapping are DERIVED. Tests use fake database
rows and do not verify live schema, grants, deployment or PostgreSQL execution.

## API #92 Admin notification list

The read-only view calls `validate_current_user_request(..., role="ADMIN")` before parsing `page` or executing queries. No fine-grained notification-management permission or sender/tenant predicate is source-backed; shared ADMIN is a documented DERIVED fallback. Count and page query the legacy BIGINT `notifications` candidate joined to migration-009 `notification_deliveries`, do not select recipient/sender identifiers, and return `Page<Notification>`. Successful reads do not commit; query/projection failures rollback. Connection unavailability maps to 503 and other query failures to 500. Fake-session tests and checked-in migration do not prove live authorization, schema, grants or deployment.


## API #93 Admin notification create/send

The endpoint authenticates with `validate_current_user_request(..., role="ADMIN")` before body validation or recipient SQL and uses the authenticated principal ID as the candidate `sender_id`. It verifies requested `users.id` values without role/status/course filtering. There is no source-backed fine-grained notification-management permission or tenant scope. Notification and delivery inserts use bound SQL constants and one caller-owned transaction. SQL operational/invalidated-connection errors map to 503; other SQL/projection/commit failures map to 500. These persistence/permission choices are DERIVED, and fake DB tests do not prove live grants/schema or delivery-worker behavior.


## API #94 notification update security/transaction boundary

API #94 calls `validate_current_user_request(..., role="ADMIN")` before parsing the raw positive-int64 path/body or querying the target. AC-36's notification-management permission has no source-backed policy, so the shared ADMIN role is only a DERIVED fallback. The view locks the notification row and then matching delivery rows, updates only title/content in one caller-owned transaction, validates projection before commit, and rolls back SQL/projection/commit failures. Fake DB tests do not verify PostgreSQL row-lock behavior, live schema/grants or deployment.

## API #95 notification delete security/transaction boundary

API #95 calls `validate_current_user_request(..., role="ADMIN")` before positive signed-int64 path validation or DB lookup. AC-36's dedicated notification-management permission has no source-backed policy, so shared ADMIN remains a DERIVED fallback. The view locks the notification parent then matching delivery rows, requires at least one row and all QUEUED, DELETEs the parent, validates returned ID/time and the complete envelope, then commits in the caller-owned transaction. Checked-in FK cascade is the local candidate effect. Query/projection/commit failures rollback to safe 500; invalid/ineligible input uses the catalog 422. Tests use fake DB and do not verify live schema/grants, PostgreSQL locking/cascade, worker race or deployment.

## API #96 notification status read boundary

API #96 calls `validate_current_user_request(..., role="ADMIN")` before custom positive signed-int64 path parsing or query. AC-36 fine-grained notification-management permission has no source-backed policy, so role-only ADMIN is DERIVED. One bound, read-only query joins the candidate notification/outbox by `notification_id` and maps into the existing #92 Notification model; it does not select recipient/sender identifiers, mutate rows or commit. Invalid ID/no delivery result maps to catalog 404; SQL/projection failures rollback to safe 500 (no 503 is declared for #96). Fake-session tests do not verify live schema, grants, migration or deployment.

## API #97 Admin reported-discussion queue security/transaction boundary

API #97 calls `validate_current_user_request(..., role="ADMIN")` before
custom signed-int32 page parsing or either read query. AC-37 fine-grained
moderation permission is not source-backed, so shared ADMIN is the local
fallback. The count/list queries are read-only and do not commit; SQL or
projection failures rollback to safe 500, while invalid page returns local
DERIVED 422. Fake-session tests do not verify live schema, grants, migration or
deployment.
