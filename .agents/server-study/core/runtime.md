# Study core runtime contracts

Status: source-backed; `app.main` imports and composes the current routes,
including public API #2 verify-email dispatch, API #5 categories, API #6
courses, API #7 course search, API #46 Mentor courses, API #47 Mentor lecture
creation, API #48 lecture detail, API #49–#53 Content routes, API #54 Mentor
submissions, API #55 submission detail, API #56 grade, API #57 feedback and
API #58 support requests, API #59 support-request detail, API #60 reply, API #61 resolve, API #62 course-student roster, API #63 notification dispatch, API #64 notification status, API #65 course progress, API #66 course activity analytics, API #67 Student progress and Admin APIs #68–#92. Mentor routes #46–#67 and Admin routes #68–#92 have current HTTP test modules;
the full suite result is recorded in `tests.md` (1217 local tests passed; 54 API paths / 63 operations).

The local Study API startup address is `127.0.0.1:3003`. Containerized startup
binds internally to `0.0.0.0:3003` and publishes the host address separately.

## `app/main.py`

### `_settings_for_request(request)`
- Purpose: prefer `request.app.state.settings`, fallback to cached `get_settings()`.
- Return: `Settings`.
- Side effect: none.
- Caller: health handlers.

### `create_app(app_settings=None)`
- Purpose: compose FastAPI instance; optionally inject test/runtime settings and DB factory.
- Calls: `build_engine`, `build_session_factory`, CORS middleware, `TraceIdMiddleware`, exception handlers, router.
- Side effects: creates engine/session factory when explicit settings supplied; installs dependency override for `get_db`.
- Declared routes: `/`, `/health/live`, `/health/ready` plus `/api/v1/*` router.
- Runtime status: source-backed/import-verified for current routes, including API
  #1 register, API #2 verify-email dispatch, API #5 categories, API #6 courses
  and API #7 course search.

### root/health handlers
- Intended return: standard success envelope via `success_response`.
- `health_live`: reports service + environment only.
- `health_ready`: reports database as `configured`; it does **not** execute a DB probe. Redis is only `configured/not_configured` from settings.
- Runtime status: source-backed; full Study test suite is collectable in the
  Study virtual environment.

## `app/core/responses.py`

### `ErrorDetail`
Pydantic model `{field?, code, message}`, `extra=forbid`.

### `error_response(...)`
Public function that directly returns `JSONResponse` with HTTP status, business
code, safe message, trace ID, data/meta, field errors and optional headers.
Views/validators return the response to the route; no custom API exception is
raised. Calling `error_response()` with no arguments creates a safe internal 500 and
uses the current trace context or generates a trace ID.

`success_response` directly builds the canonical success envelope with keys
`success`, `businessCode`, `message`, `data`, `meta`, and `traceId`.
`error_response(...)` builds the canonical six-key error envelope directly; supplied
`ErrorDetail` values are serialized under `meta.fieldErrors`. Omitted error
`data` is serialized as JSON `null`. `JSONResponse` provides the status and
headers, including `X-Trace-Id`.

## `app/core/middleware.py` exception handlers

The FastAPI exception handlers live beside `TraceIdMiddleware`; `create_app`
registers them with the app. `TraceIdMiddleware` manages trace state and the
response header, while unexpected exceptions propagate to Starlette's outer
`ServerErrorMiddleware` and use the registered `Exception` handler.

- `_validation_field(loc)`: removes protocol location prefixes (`body/query/path/header/cookie`) and joins remaining field path.
- `http_exception_handler`: converts HTTP exceptions through `error_response(...)`, preserving status and safe envelope fields; otherwise maps to `HTTP_ERROR`.
- `request_validation_exception_handler`: converts Pydantic errors to `ErrorDetail` values and `JSONResponse` through `error_response(...)`, using
  `DESIGN_VALIDATION_ERROR` for API #1 register, API #2 verify-email dispatch,
  auth login/refresh, API #5 categories, API #6 courses, API #7 course
  search, API #46–#57 Mentor endpoints, and
  `VALIDATION_ERROR` elsewhere. Parameterized routes are classified by their
  FastAPI route template as well as fixed request paths.
- `unhandled_exception_handler`: logs internal exception with trace ID and builds
  a safe response through `error_response(...)`; it uses `DESIGN_INTERNAL_ERROR` for API #1 register, API #2 verify-email dispatch,
  auth login/refresh, API #5 categories, API #6 courses, API #7 course
  search, API #46–#57 Mentor endpoints, and
  `INTERNAL_SERVER_ERROR` elsewhere. It reads the trace ID from
  `request.state`; `error_response` returns it in both body and `X-Trace-Id` header.

## API #2 verification dispatch

- `app/service/email/provider.py` defines the injectable provider boundary and the
  default stub used by the current runtime.
- `app.modules.guest.api_02_auth_verify_email_send.view` calls the provider without resolving
  a DB session, then maps acceptance to HTTP `202`.
- The stub does not send real email; token/link generation, provider integration
  and retry worker remain outside the current runtime boundary.

## API #6 public courses

- `app.modules.guest.api_06_courses` exposes public `GET /api/v1/courses` without
  authorization or mutation.
- Query defaults are `page=1`, `size=20`; size is limited to `1..100`.
- Sort is an allow-listed `field:direction` expression over `id`, `name`,
  `price` and `created_at`; default order is `created_at DESC, id ASC`.
- Only `PUBLISHED` courses are selected. Mentor data is read through a left
  join and missing mentor integrity is mapped to `DESIGN_INTERNAL_ERROR`.
- `category` is parsed but rejected with `DESIGN_VALIDATION_ERROR` until a
  course-category relation is source-backed. Price is serialized as a decimal
  string; no live DB metadata verification is claimed.

## API #7 course search

- `app.modules.guest.api_07_courses_search` exposes public `GET /api/v1/courses/search`.
- `q` is trimmed/lowercased and bound into `LOWER(c.name) LIKE :q_pattern`;
  blank `q` removes the text predicate.
- `page` defaults to `1`; page size is fixed at `20`; `sort` reuses the
  allow-listed `field:direction` convention and default order from API #6.
- `category` is parsed but rejected with `DESIGN_VALIDATION_ERROR` before DB
  access because the course-category relation is not source-backed.
- Page and count queries share `PUBLISHED` and search predicates. Mentor
  integrity, query and mapping failures map to `DESIGN_INTERNAL_ERROR`; price
  is serialized as a decimal string and no live DB verification is claimed.

## API #46 Mentor courses

- `app/modules/mentor/api_46_mentor_courses` is composed at
  `GET /api/v1/mentor/courses` and registered in `DESIGN_CONTRACT_PATHS` for
  framework validation and unexpected-error business codes.
- The validator calls `validate_current_user_request(...)` with role `MENTOR`
  and preserves the API-specific internal-error message before any query.
  Invalid authentication returns
  `401`; another role returns `403`.
- `status` is optional and limited to `DRAFT`/`PUBLISHED`; page/size defaults and
  bounds follow API #6. The count and page SQL are owner-scoped to the JWT
  subject and share the optional status condition; results use fixed
  `created_at DESC, id ASC` ordering.
- The view reuses shared `Course`, `CoursePage`, mentor mapping and decimal-price
  serialization. It checks missing mentor integrity, rolls back SQL failures,
  and maps failures to a safe `DESIGN_INTERNAL_ERROR` response. No live schema
  check is claimed.

## API #47/#48 Mentor lecture flow

- API #47 `POST /api/v1/mentor/courses/{course_id}/lectures` requires direct
  `courses.mentor_id` ownership, resolves uploads under the same owner,
  `LECTURE` purpose and course, inserts `lessons`, and writes ordered
  `lesson_uploads` rows in the same transaction for non-empty `asset_refs`.
- API #48 `GET /api/v1/mentor/lectures/{lecture_id}` is registered in
  `DESIGN_CONTRACT_PATHS`, uses the shared Mentor guard and the same direct-owner
  predicate, then maps the lesson with linked uploads in `asset_position`
  order. It has no status filter; nullable content returns JSON null.
- API #48 exposes `lecture_id` as integer/int64 in OpenAPI while parsing the raw
  path in the view so malformed values map to catalog 404 instead of 422.
- Focused HTTP tests use fake database queries. Checked-in legacy DDL/migration
  005 do not establish live schema or assigned-course support.


## API #49 Mentor content tree

- `GET /api/v1/mentor/courses/{course_id}/content` is registered in
  `DESIGN_CONTRACT_PATHS`. The raw path is parsed in the view and exposed as
  signed int64 in OpenAPI; malformed/out-of-range values map to catalog 404.
- The shared Mentor JWT guard supplies a numeric user ID; course access requires
  direct `courses.mentor_id` ownership.
- The view reads legacy `contents` rows for the course, filters only
  `deleted_at IS NULL`, returns every status, and orders by parent/order/id.
  The response is flat `Content[]` linked by `parent_id`; an empty active tree
  returns `[]` with HTTP 200.
- Mapping rejects duplicate IDs, missing parents, cross-course rows and cycles;
  query/mapping errors roll back and return safe `DESIGN_INTERNAL_ERROR`.
  The endpoint is read-only and does not commit.
- Legacy `DB.sql` and migration 006 are checked-in artifacts only. Live schema,
  assigned-course access, type/status enums, payload subtypes and version
  selection remain unverified/open.

## API #50 Mentor content create

- `POST /api/v1/mentor/content` is registered in `DESIGN_CONTRACT_PATHS`; the
  route returns HTTP 201 and uses the shared Content response model from API #49.
- The request model enforces required strict signed-int64 `course_id`, strict
  string `content_type`/`title`, JSON object `payload`, and forbids extra fields.
  Closed ContentType members, title normalization/length and payload subtype
  rules are not source-backed.
- The shared auth guard requires `MENTOR`; the view locks the course row and
  compares its `mentor_id` with numeric JWT `sub`. Missing and non-owned courses
  both map to `403 DESIGN_ACCESS_DENIED` as a derived choice because API #50
  does not declare 404. Course status is not filtered.
- The view assigns root `parent_id=NULL`, status `PENDING_REVIEW` and the next
  active-root `content_order` starting at 0. These are DERIVED implementation
  choices from request shape/AC-33; the course row lock serializes #50 order
  allocation for a course. SQL constants live in the API module `query.py`;
  `view.py` owns JSONB binding, INSERT/RETURNING validation, commit and rollback.
- Focused TestClient tests cover auth, request validation, ownership/error
  mapping, insert projection, rollback, trace and OpenAPI. Full suite result is
  in `tests.md`. Fake DB and migration 006 do not verify live schema/deployment.

## `app/core/trace.py`

- `TRACE_HEADER = "X-Trace-Id"`.
- `create_trace_id()`: UUID4 string.
- `validate_trace_id(value)`: valid UUID normalized to string else `None`.
- `get_trace_id(request)`: read validated `request.state.trace_id`, otherwise generate/store one.
- `set_trace_id(value)` / `reset_trace_id(token)`: manage ContextVar.
- `get_current_trace_id()`: read ContextVar without Request.

## `app/core/middleware.py:TraceIdMiddleware.dispatch`
Flow: validate incoming header -> create if invalid -> attach request/context -> call next -> set response header -> reset context. Unexpected exceptions propagate to Starlette's `ServerErrorMiddleware`, which calls the registered `unhandled_exception_handler`; that handler reads the still-present `request.state.trace_id` after the middleware resets its ContextVar. Route/business errors that already return `error_response(...)` remain direct responses.

Middleware uses `validate_trace_id`, `set_trace_id` and `reset_trace_id` from the
current trace module.

## API #80 Admin Content approval

- `PATCH /api/v1/admin/content/{content_id}/approve` is an explicit design-contract path and documents only the catalog path/header inputs; it has no request body.
- The shared `ADMIN` guard runs before the raw signed-int64 parser. Parse/state validation returns catalog `422`; errors use the current shared envelope (`data:null` and trace ID).
- API #80 is exposed in OpenAPI with the direct `Content` response and 401/403/404/422/500 set. After API #81, OpenAPI has 47 `/api/v1` path templates and 52 operations.
- The route acts on the active row locked at request time; #79's request does not provide a revision token, so same-revision behavior is not guaranteed.

## API #81 Admin Content rejection

- `PATCH /api/v1/admin/content/{content_id}/reject` is a distinct design-contract path with required JSON `{reason: string}`; OpenAPI documents signed-int64 path, Authorization, the required request body and catalog 401/403/404/422/500 responses.
- Shared `ADMIN` auth runs before raw signed-int64 parsing or DB access. Invalid/out-of-range path and non-pending state map to catalog 422; absent/soft-deleted Content maps to 404.
- The view changes active `PENDING_REVIEW` to `REJECTED`, writes the reason in one migration 011 audit-candidate row, validates the Content projection and commits. `RequestValidationError` uses the DESIGN envelope because the path is registered; `error_response()` emits `data:null`.
- Reason storage, state gate and one-row decision/audit transaction are DERIVED; fake DB tests do not verify live schema, migration deployment or dedicated moderation permission. The empty-string rule is intentionally left as the catalog's required-string behavior.


## API #51 Mentor content update

- `PUT /api/v1/mentor/content/{content_id}` is registered in `DESIGN_CONTRACT_PATHS`; it returns HTTP 200 and uses the API #49 Content response model.
- The required strict body (`content_type`, `title`, object `payload`) is a DERIVED full-replacement fallback because catalog/diagram omit it. Framework body errors map to `422 DESIGN_VALIDATION_ERROR`; raw path IDs parse as signed int64 and invalid values map to 404.
- The shared Mentor guard runs before DB access. The view locks active `contents` and its parent `courses`, requires direct `courses.mentor_id` ownership, snapshots the previous state into `content_versions`, sets current status to `PENDING_REVIEW`, validates the returned projection and commits both writes together.
- Catalog error set remains 401/403/404/422/500; no 409 is added. Focused tests use fake DB queries. Body/history/lifecycle are DERIVED; original author, API #52/AC-33 revision selection, live schema and migration deployment remain unverified.

## API #52 Mentor content publish/unpublish

- `PATCH /api/v1/mentor/content/{content_id}/publish` is registered in `DESIGN_CONTRACT_PATHS` and uses the API #49 Content response model.
- The strict `{published: boolean}` body is a DERIVED target-state fallback because catalog/AC-22 declare path only. Malformed/out-of-range path IDs return 404; framework body errors return `422 DESIGN_VALIDATION_ERROR`.
- The shared Mentor guard runs before DB access. The view locks active Content and its Course, checks direct owner, permits only APPROVED→PUBLISHED and PUBLISHED→APPROVED, treats same target as a no-op, updates status only, validates the response projection and commits.
- APPROVED is the only available status readiness gate; payload/assets are not checked. Focused tests use fake DB queries. Request body, transition/readiness rules, live schema and deployment remain unverified; AC-33 approval and revision selection remain open.

## API #53 Mentor Content delete

- `DELETE /api/v1/mentor/content/{content_id}` shares the existing route-template entry in `DESIGN_CONTRACT_PATHS` with API #51's PUT and returns HTTP 200 with the catalog `DeleteResult`.
- The route documents signed-int64 path metadata and accepts no body/query. The view authenticates `MENTOR` before DB access, locks active Content and its owning Course, and uses the current direct `courses.mentor_id` owner fallback.
- Active direct children and `PUBLISHED` status return `422 DESIGN_VALIDATION_ERROR` under DERIVED guards. A successful mutation sets only `contents.deleted_at = CURRENT_TIMESTAMP`; `RETURNING id, deleted_at` is validated before the view commits. It does not change Content status or write history/audit rows.
- Malformed/out-of-range IDs and already-deleted rows return `404 DESIGN_RESOURCE_NOT_FOUND`. Focused tests use fake DB queries and do not establish live schema/deployment. Child, publication, pending-review queue, retry, timestamp/timezone and assigned-Mentor policies remain open.

## API #56 Mentor submission grade

- POST /api/v1/mentor/submissions/{submission_id}/grade is registered in DESIGN_CONTRACT_PATHS; the route declares signed-int64 metadata while the view parses the raw value so malformed/overflow path input maps to catalog 404.
- The explicit MENTOR guard runs before path parsing and database access. The handler locks the submission, checks direct courses.mentor_id ownership and repeats that predicate in UPDATE.
- The DERIVED score fallback requires 0 <= score <= assignments.max_score; UPDATE writes only score and status=GRADED, preserving existing feedback. The handler allows repeat grading because no current-state 409 rule is source-backed.
- The required rubric_items string is accepted as opaque input under a DERIVED key but discarded; no legacy rubric persistence relation is source-backed.
- API #54's Submission projection and constrained exact URL/owner/SUBMISSION-purpose/course lookup are reused. The handler validates the response projection before commit and rolls back failures.
- Focused TestClient tests use fake DB queries. Checked-in legacy DDL is only candidate evidence; live schema, deployment, API #35 URL compatibility and rubric persistence are unverified.

## API #57 Mentor submission feedback

- `POST /api/v1/mentor/submissions/{submission_id}/feedback` is registered in `DESIGN_CONTRACT_PATHS`; raw signed-int64 parsing maps malformed/overflow values to catalog 422.
- The shared MENTOR guard runs before ID parsing and database access. The view locks the submission, checks direct `courses.mentor_id` ownership and repeats that predicate in the feedback-only UPDATE.
- Required strict strings are `feedback_text` (DERIVED from the catalog descriptor) and `attachments`; attachments are accepted as opaque input and unused because no persistence/response target is supported.
- The update preserves score/status and has no direct-call GRADED precondition. Repeated calls overwrite the single legacy feedback candidate as DERIVED behavior.
- The view reuses #54 `SubmissionResponse` and the constrained URL/owner/purpose/course UploadAsset lookup; it commits after validation and rolls back failures. Tests use fake DB; live schema/deployment are unverified.

## API #55 Mentor submission detail

- `GET /api/v1/mentor/submissions/{submission_id}` is registered in `DESIGN_CONTRACT_PATHS` and exposes a signed-int64 path in OpenAPI while parsing the raw path in the view; malformed/out-of-range values map to catalog 404 following API #48.
- The view authenticates `MENTOR` before path/database work, reads one legacy BIGINT candidate with LEFT JOINs to assignments/courses, maps missing rows to 404, broken required relations to 500 and non-owned courses to 403 under DERIVED direct-owner policy.
- It reuses API #54's `SubmissionResponse` schema and constrained 0/1 UploadAsset URL/owner/purpose/course fallback. The endpoint is read-only and does not commit. AC-23 rubric remains absent because no linked response field or legacy assignment-rubric relation is source-backed.
- Focused TestClient tests use fake DB results. Live schema, assigned-Mentor access, API #35 URL compatibility and rubric mapping remain unverified/open.

## API #58 Mentor support-request list

- `GET /api/v1/mentor/support/requests` uses the shared `MENTOR` guard and direct `courses.mentor_id` scope. The response is a collection without pagination; `course_id` and exact `status` filters combine with AND, and requests/messages use deterministic ordering.
- API #58's collection shape, legacy BIGINT tables, status constraint, and ordered message-upload relation are DERIVED fallbacks recorded in the DD and migration 008. Full message threads are included; asset links are checked against author, course, role-appropriate purpose and `UPLOADED` status.
- Invalid `course_id` maps to 422. The route is read-only and does not commit. Focused/full tests use fake DB rows; live schema and migration deployment remain unverified.


## API #59 Mentor support-request detail

- `GET /api/v1/mentor/support/{request_id}` is composed after the static API #58 collection route and registered in `DESIGN_CONTRACT_PATHS`.
- The route preserves raw path text for signed-int64 parsing; malformed/overflow IDs map to catalog 404. The shared MENTOR guard runs before request lookup.
- The view reads one request with course/student LEFT JOIN projections, distinguishes missing 404 from other-owner 403, then loads the full chronologically ordered message thread with ordered UploadAssets. The request and thread queries both enforce direct `courses.mentor_id` ownership.
- The response reuses API #58 models. This support schema and detail behavior are DERIVED local fallbacks; tests use fake DB rows. Live migration/schema/deployment remain unverified.


## API #60 Mentor support reply

- `POST /api/v1/mentor/support/{request_id}/reply` is registered in `DESIGN_CONTRACT_PATHS`; its raw path is documented as signed int64 and malformed/overflow input maps to catalog 422. Framework body errors also map to `422 DESIGN_VALIDATION_ERROR`.
- The shared MENTOR guard runs before DB access. The view locks the support request and checks direct `courses.mentor_id` ownership. Missing request is 404, another owner is 403, and broken required parent projection is safe 500.
- Required strict strings are `message` and `attachment_refs`; the latter contains ordered unique int64 IDs encoded as a JSON array string, with `[]` for none. This key/encoding and nonblank-only message check are DERIVED local choices.
- The view scopes each upload to the Mentor, request course, `LECTURE` purpose and `UPLOADED` status; inserts the message and zero-based ordered links; reuses API #59's thread query and shared pure projection; and commits only after validating the full response. Failures roll back. Request status is preserved.
- Focused tests cover validation, auth, owner/missing requests, scoped uploads, link ordering, response hydration and rollback; the full Study suite passed 584 tests. Tests use fake DB data. Migration 008/live schema, deployment, concurrency, storage reachability, and post-resolve policy remain unverified/open.

## API #61 Mentor support resolve

`PATCH /api/v1/mentor/support/{request_id}/resolve` is registered in the design-contract path set. The raw path is parsed as signed int64 so malformed/overflow values return `422 DESIGN_VALIDATION_ERROR`. The view locks `support_requests`, checks the direct course owner, updates an active state to RESOLVED, or returns the already resolved request unchanged. CANCELLED/unsupported states return 422. It hydrates the chronological #59 thread and commits only after response validation; failures roll back. Error envelopes use `data: null` and `meta.fieldErrors`. Local tests use fake DB results; migration 008/live deployment remain unverified.

## API #62 Mentor course students

`GET /api/v1/mentor/courses/{course_id}/students` is registered in the design-contract path set. The route accepts raw `course_id` text while OpenAPI declares signed int64; malformed/overflow values map to catalog 404. The view checks direct course ownership and returns a distinct `UserSummary[]` from ACTIVE Student enrollments with no pagination or writes. This response correction and legacy schema/access choices are DERIVED; fake-DB tests do not verify live DB/deployment.

## API #63 Mentor notifications

`POST /api/v1/mentor/notifications` is registered in the design-contract path set with HTTP 202. It authenticates MENTOR, validates the strict direct catalog body, parses recipient and channel CSVs, then requires all Student IDs to share an ACTIVE roster in a directly owned course because the body has no course ID. The view inserts per-recipient legacy notification rows and per-channel `QUEUED` outbox rows in one caller-owned transaction; the response Operation UUID groups the batch and `meta.notification_ids` hands IDs to API #64. Error responses use the catalog 401/403/422/503/500 mappings and rollback on write/projection/commit failure. The schema and business interpretation are DERIVED; HTTP tests use fake DB sessions and do not verify migration deployment or actual Push/Email delivery. No worker/provider is wired.

## API #64 Mentor notification status

`GET /api/v1/mentor/notifications/{notification_id}/status` is registered in
the design-contract path set. The route reads raw path/header values so the
signed-int64 OpenAPI path does not produce an automatic 422; malformed or
overflow values map to catalog 404. The view authenticates MENTOR before DB
access, checks local `notifications.sender_id` against JWT `sub`, aggregates
persisted channel states, and returns the direct Operation envelope without
committing or calling a provider. API #63's local `operation_id`, sender and
timestamps are projected into Operation; queued takes precedence over failed,
then all-sent maps to SENT. These mappings are DERIVED. Focused and full tests
use fake DB rows; live schema, migration 009 and delivery remain unverified.

## API #65 Mentor course progress

`GET /api/v1/mentor/courses/{course_id}/progress` is registered in the
design-contract path set. The route reads raw path/header values, declares the
catalog int64 path and auth header in OpenAPI, and avoids a synthetic 422. The
view authenticates MENTOR before DB access, checks direct course ownership,
then performs one roster/progress aggregate query scoped again to the owner.
It returns the local DERIVED `Page<MentorStudentProgress>` shape: active
Student enrollments, PUBLISHED lessons, latest progress row by timestamp/ID,
completed count and floor-average percent. The full roster is one unbounded
page because request has no page/size. The GET performs no writes. Focused and
full tests use fake DB rows; catalog response mismatch, live schema and
deployment remain unresolved/unverified.

## API #66 Mentor course activity analytics

`GET /api/v1/mentor/courses/{course_id}/analytics` is registered in the
design-contract path set. It accepts a raw signed-int64 path and Authorization
header, authenticates MENTOR before DB access, checks direct course ownership,
then reads distinct Student/lesson pairs with non-null last-access timestamps
for PUBLISHED lessons. It returns tracked pair count, distinct Student count
and latest timestamp; empty input returns zero/zero/null. The projection is a
DERIVED current-state proxy because no event ledger is present in reviewed
DDL. Catalog `Page<Course>` differs from this local summary response. The GET
performs no writes; fake-DB tests do not verify live schema/deployment.

## API #67 Mentor Student progress

`GET /api/v1/mentor/courses/{course_id}/students/{student_id}/progress` is
registered in the design-contract path set. It reads both raw signed-int64
path values, authenticates MENTOR before DB access, checks direct course
ownership, and requires the requested user in the ACTIVE Student roster. It
then reads PUBLISHED lesson progress in `sort_order,id` order, selecting the
latest duplicate row by timestamp then ID. The singular response contains
student identity, completed/total/floor-average summary, and per-lesson state;
missing state maps to NOT_STARTED/0. These choices are DERIVED and conflict
with diagram/catalog `Page<Course>`. The GET is read-only; focused HTTP tests
use fake DB results and do not verify live schema/deployment.


## API #68 Admin user list, API #69 Admin user detail

`GET /api/v1/admin/users` is registered and included in `DESIGN_CONTRACT_PATHS`. The route requires the shared `ADMIN` JWT role before DB access, validates positive int32 `page`, normalizes keyword, and reads the legacy `users` candidate through matching count/page predicates. It returns `ApiEnvelope<Page<UserProfile>>`, fixed size 20, `id ASC`; invalid page maps to 422. The response reuses API #04's safe profile model and does not include password hashes or unsupported bio. Contract/cardinality, filters, page rules and the legacy target are DERIVED; focused tests use fake DB sessions and do not establish live schema/deployment.


## API #69 Admin user detail

`GET /api/v1/admin/users/{user_id}` is registered and included through its route template in `DESIGN_CONTRACT_PATHS`. It requires the shared `ADMIN` JWT claim before parsing the raw signed-int64 path or querying. Invalid/out-of-range path and no-row both return catalog 404; SQL/projection failures roll back and return safe 500. The read-only response reuses API #04 `UserProfile`, keeps nullable avatar/phone and omits bio/credentials. Legacy schema and invalid-path fallback remain DERIVED; tests use fake DB rows and do not prove deployment.

## API #70 Admin user update

`PUT /api/v1/admin/users/{user_id}` is registered on the existing API #69 path template. It uses the shared `ADMIN` guard before parsing the raw signed-int64 path or accessing the DB. The candidate strict body requires a full profile replacement: nonblank `full_name`, nullable `phone`/`avatar_url`, and role `STUDENT`, `MENTOR` or `ADMIN`; this body/enum is DERIVED because catalog and diagram do not declare it. The view runs one bound UPDATE against the checked-in legacy `users` candidate, returns API #04 safe `UserProfile`, maps malformed/out-of-range ID to catalog 422 and no row to 404, and owns commit/rollback. It preserves email/status/created_at and has no audit, status, delete or token-revocation side effects. Focused tests use fake DB sessions; live schema and Admin/role-transition policy remain unverified.

## API #71 Admin user status

`PATCH /api/v1/admin/users/{user_id}/status` is registered in `DESIGN_CONTRACT_PATHS`. The shared `ADMIN` guard runs before raw signed-int64 path validation and DB access; the strict required `{status}` body is a DERIVED fallback with `ACTIVE`/`SUSPENDED` literals. The view locks the legacy `users` candidate, permits transitions only from those two current states, updates status and timestamp, and conditionally revokes unexpired, unrevoked refresh tokens when suspending in the same transaction. It returns the API #04 safe `UserProfile`; errors are limited to catalog 401/403/404/422/500 and failed query/projection/revoke/commit paths roll back. Login/refresh reject non-ACTIVE users, but an already-issued access JWT can remain usable until expiry. Focused API #71 tests: 21 passed; linked API #03/#68–#71 regression: 80 passed. Fake DB sessions do not verify live schema/deployment or authorization policy; the DD remains Draft.


## API #72 Admin user delete

`DELETE /api/v1/admin/users/{user_id}` is registered on the existing API #69 path template. The shared `ADMIN` guard runs before raw signed-int64 validation and database access. One conditional UPDATE sets legacy `users.status='DELETED'`, updates `updated_at`, and returns that timestamp as `DeleteResult.deleted_at`; missing or already-DELETED maps to 404. The view commits only after validating the response projection and rolls back query/projection/commit failures. The marker, timestamp mapping and repeat behavior are DERIVED; DD remains Draft. API #03 blocks new login/refresh for non-ACTIVE status, but an already-issued access JWT can remain usable until expiry. Focused #72 tests: 11 passed; API #03 + #68–#72 regression: 95 passed; full Study suite: 806 passed. Fake DB sessions do not establish live schema/deployment.

## API #73 Admin course list

`GET /api/v1/admin/courses` is registered with `GetAdminCoursesEnvelope` and a static `DESIGN_CONTRACT_PATHS` entry. The route passes raw query/header strings so the shared `ADMIN` guard runs before parsing or DB access. It exact-matches optional `status` and signed-int64 `mentor`, rejects valid `category` before DB because no course-category relation is source-backed, and validates positive int32 `page` (default 1). It reads count/integrity then the fixed-size-20 page, with identical status/mentor predicates and `c.id ASC`, through the legacy BIGINT `courses/users` candidate. Shared Course mapping serializes Decimal price exactly; missing mentor/invalid projection and SQL failures return safe 500 with rollback. The route never commits. Focused tests: 24 passed; linked #06/#68/#73 regression: 60 passed; full Study suite: 830 passed; Ruff passes. OpenAPI exposes 41 `/api/v1` templates and 44 operations. Fake DB tests do not verify live schema/deployment; category behavior, page/filter choices, ADMIN-to-course-management mapping and orphan recovery remain DERIVED/open. DD stays Draft.


## API #74 Admin course detail

`GET /api/v1/admin/courses/{course_id}` is registered with a raw signed-int64 path and route-template entry in `DESIGN_CONTRACT_PATHS`. The shared `ADMIN` guard runs before path parsing and DB access; invalid/out-of-range IDs and missing rows map to catalog 404. One bound SELECT reads the legacy BIGINT `courses LEFT JOIN users` candidate without a status predicate, then shared `map_course` and `CoursePage` return a singleton page. The read never commits; SQL/projection failures return safe 500 with rollback. Focused tests: 15 passed; linked #06/#08/#69/#73 regression: 80 passed; full Study suite: 845 passed; Ruff passes. Fake DB tests do not establish live schema/deployment or a dedicated course-management permission; counters remain undefined, and the DD stays Draft.

## API #75 Admin course update

`PUT /api/v1/admin/courses/{course_id}` shares the registered #74 FastAPI route template, so request validation continues to use `DESIGN_VALIDATION_ERROR`. The route declares int64 path/header/body OpenAPI metadata and passes raw path/header plus the strict `AdminCourseUpdateRequest` to the view. The shared ADMIN guard and path/body candidate checks run before SQL. The view updates metadata, reads the shared Course projection, validates singleton `CoursePage`, then commits; query/projection/commit failures roll back and return safe 500. Focused tests: 27 passed; linked #06/#08/#70/#73/#74/#75 regression: 113 passed; full Study suite: 872 passed; Ruff passes. These local fake-session results do not verify live schema/deployment or dedicated course-management permission.

## API #76 Admin course status

`PATCH /api/v1/admin/courses/{course_id}/status` is wired in `app/api/v1.py`. Its separate route template is in `DESIGN_CONTRACT_PATHS`, so request validation and unhandled errors use the Study DESIGN envelope. The route passes typed body, raw path, Authorization and Session to the view. The view authenticates shared ADMIN, locks status, applies target + audit in one transaction, reads the #74 Course projection and commits after mapping. Same-status requests do not update timestamp or append audit. Focused HTTP suite: 18 passed; full-suite and Ruff results are in `tests.md`. Fake DB tests do not prove migration application, live schema or deployment.

## API #77 Admin course delete

`DELETE /api/v1/admin/courses/{course_id}` reuses the existing course path template; middleware emits the standard DESIGN envelope. The route passes raw path/header and Session to the view and documents signed-int64 path, no body, Authorization and catalog 401/403/404/422/500 errors. The view authenticates shared ADMIN, locks a course not marked `DELETED`, checks candidate enrollment/content relations, then sets `status='DELETED'` and DB `updated_at`. The returned timestamp maps to `DeleteResult.deleted_at`; dependency/marker/repeat-404 choices are DERIVED. Focused tests: 20 passed; full Study suite: 910 passed. Fake sessions do not verify live PostgreSQL, deployment or dedicated permission. DD remains Draft; linked status restore and Mentor writer behavior remain open.

## API #78 Admin pending Content queue

`GET /api/v1/admin/content/pending` is registered in `app/api/v1.py` and `DESIGN_CONTRACT_PATHS`. The route passes raw query/header values to the view, which authenticates shared ADMIN before parsing or DB access. The query returns current active `PENDING_REVIEW` Content as `Page<Content>` with fixed size 20 and `id ASC`; count and page filters match. Page cardinality conflicts with the singular catalog/diagram response and is a DERIVED fallback. Focused tests: 23 passed; linked regression: 160 passed; full Study suite: 933 passed. Fake DB tests do not establish live schema or deployment.

## API #79 Admin Content detail
`GET /api/v1/admin/content/{content_id}` is registered in `app/api/v1.py` after fixed #78 `/admin/content/pending` and in `DESIGN_CONTRACT_PATHS`; OpenAPI exposes 45 `/api/v1` templates and 50 operations. The route passes raw path/header values so shared ADMIN auth precedes signed-int64 parsing and DB access. One active-row SELECT maps the eight reusable Content fields; invalid/no-row IDs return catalog 404, query/projection failures return safe 500 with rollback, and success does not commit. Focused tests: 13 passed; full Study suite: 946 passed; Ruff passes. AC-33 version/author metadata, revision identity, live schema and deployment remain unverified.

## API #82 Admin lessons list

`GET /api/v1/admin/lessons` is registered in `app/api/v1.py` and `DESIGN_CONTRACT_PATHS`; its OpenAPI documents optional `course:int64`, `status:string`, `type:string`, Authorization, and 401/403/422/500 outcomes. The route forwards raw query values so the shared `ADMIN` guard runs before parse/query. The view returns an unpaginated `Lesson[]`, exact course/status filters, stable candidate ordering, 422 for malformed int64 or unsupported `type`, and safe 500 with rollback for SQL/projection failure. Errors use `data:null`; empty results return 200 with `[]`. Array cardinality and query semantics are DERIVED against the catalog singleton schema; focused tests use fake DB rows and do not prove live schema/deployment or dedicated lesson-management permission.


## API #85 Admin lesson status

`PATCH /api/v1/admin/lessons/{lesson_id}/status` has its own route template and DESIGN middleware allowlist entry. Typed body validation runs before the endpoint's ADMIN guard; for valid requests, shared ADMIN auth precedes signed-int64 parsing and database access. The view locks a legacy BIGINT Lesson, updates status/updated_at and appends the migration 012 audit candidate atomically when status changes; same-status requests skip UPDATE/audit. It returns API #09 `Lesson`. Body/enum/audit table are DERIVED; live schema/migration deployment and fine-grained AC-34 permission remain unverified. See `tests.md` for verified test counts.


## API #87 Admin quiz list

`GET /api/v1/admin/quizzes` is wired in `app/api/v1.py` and `DESIGN_CONTRACT_PATHS`. The route forwards raw `course`, `status`, `page`, and Authorization values, so the shared `ADMIN` guard runs first. The local fallback returns a count-matched `Page<Quiz>` (page 1, size 20, `id ASC`), exact filters, and hides `DELETED`; these choices differ from the direct singleton catalog type and remain DERIVED. Quiz items return metadata with `questions=[]` as the API #87 list projection. API #88 defines local DERIVED `question_type`/`sort_order` candidates, but #87 does not load child rows. Invalid course/page returns local 422 outside the catalog error list. At the API #87 checkpoint, its focused suite had 20 tests and the linked regression had 93; at the API #88 checkpoint, the full Study suite had 1134 tests and OpenAPI exposed 51 paths / 59 operations. Fake DB tests do not verify live schema/deployment or fine-grained AC-35 permission.

## API #89 Admin quiz update

`PUT /api/v1/admin/quizzes/{quiz_id}` is wired in `app/api/v1.py` and
`DESIGN_CONTRACT_PATHS`. It authenticates the shared `ADMIN` role before
parsing raw path/body input. The local DERIVED request reuses API #88's
`config`/`questions` JSON strings and validator, then replaces the full child
set in one transaction. The view locks the active Quiz and existing question
and choice rows, rejects tombstones/missing quizzes with 404 and attempt/answer
history with 422, checks the target course, updates parent metadata, replaces
choices/questions and validates the complete Admin Quiz response before commit.
Focused HTTP tests: 26; linked #87–#89 regression: 67; full Study suite: 1160;
Ruff passes; OpenAPI exposes 52 `/api/v1` paths / 60 operations. These body,
history, lock, course-move and tombstone rules are DERIVED; fake sessions do not
verify PostgreSQL lock behavior, live schema/migration, deployment or the
fine-grained AC-35 permission. The DD remains Draft — Needs Confirmation.

## API #88 Admin quiz create

`POST /api/v1/admin/quizzes` reads the raw body so the shared `validate_current_user_request(..., role="ADMIN")` guard runs before JSON parsing, validation or DB access. The direct catalog only fixes outer `config` and `questions` strings. The local validator’s embedded JSON shape, `SINGLE_CHOICE`/`MULTIPLE_CHOICE`/`TRUE_FALSE` vocabulary, optional `is_correct=false`, and Admin choice answer-key projection are DERIVED. The view checks the legacy BIGINT course candidate, writes parent and ordered children in one transaction, maps the Quiz response before commit, and rolls back all failures. Student API #28 must omit `is_correct`. Fine-grained AC-35 permission remains unavailable; fake DB tests do not establish live grants/schema/deployment.

## API #90 Admin quiz delete

`DELETE /api/v1/admin/quizzes/{quiz_id}` shares the #89 path template and has
no body/query. The raw path reaches the view so shared ADMIN auth runs before
positive signed-int64 validation and DB access. One transaction locks Quiz,
question and choice rows, checks attempt/answer history, then either marks the
Quiz `DELETED` while preserving history or deletes choices, questions and Quiz
in order. Both branches validate `DeleteResult` before commit. Query,
projection, mutation and commit failures roll back and return the catalog 500.
Hard delete without history, answer-only preservation, the `DELETED` marker,
`updated_at` mapping and idempotency remain DERIVED; checked-in legacy DDL is
not live-schema evidence. API #29 has no matching approved lock/status policy.
Focused tests: 18; linked #86–#90: 100; full Study suite: 1178; Ruff passes;
OpenAPI: 52 paths / 61 operations. Fine-grained AC-35 permission and deployed
PostgreSQL behavior remain unverified; DD stays Draft.

## API #91 Admin quiz statistics

`GET /api/v1/admin/quizzes/{quiz_id}/statistics` uses the shared ADMIN guard
before raw positive-int64 parsing. The route has its own
`DESIGN_CONTRACT_PATHS` entry and declares catalog 401/403/404/500 errors.
The read-only view runs one legacy BIGINT Quiz/attempt aggregate, preserves
retained tombstone history, maps malformed/out-of-range IDs to catalog 404,
and returns a separate `QuizStatistics` DTO. That DTO/metric/path fallback is
DERIVED against direct diagram/catalog `ApiEnvelope<Quiz>`; live schema and
fine-grained permission remain unverified. Focused tests: 19; linked #87–#91:
104; full Study suite: 1197; Ruff passes; OpenAPI: 53 paths / 62 operations.

## API #92 Admin notification list

`GET /api/v1/admin/notifications` is composed through the main router and included in `DESIGN_CONTRACT_PATHS`. The route passes raw query/header values to the view so shared `ADMIN` authentication runs before page parsing. Invalid page is a local 422; unavailable DB connections map to the catalog 503, while other SQL/projection failures map to safe 500. Success returns a local `Page<Notification>` proposal with 20 fixed items per page, exact status/channel filters and stable creation-time/ID order. This differs from the direct singleton `Notification` response. Local HTTP tests use fake rows; live schema, migration 009, Admin permission scope and delivery worker are unverified.


## API #93 Admin notification create/send

`POST /api/v1/admin/notifications` shares API #92's route template and is included in the contract middleware allowlist. The route forwards raw body/header and runs the blocking view through the thread pool; shared ADMIN authentication precedes JSON parsing and database access. Success is HTTP 202 only after the view validates the full envelope and commits the notification/outbox batch. Safe catalog errors are 401/403/422/503/500. OpenAPI has 54 Study API templates and 64 operations after #93.


## API #94 Admin notification update

`PUT /api/v1/admin/notifications/{notification_id}` forwards raw path, body and Authorization so shared ADMIN auth runs before custom validation. The synchronous view runs through `run_in_threadpool`. OpenAPI keeps the direct 200 Notification response and catalog 401/403/404/422/500 set; `{title, content}` is a strict DERIVED local body. The view locks notification then delivery rows, permits update only with nonempty all-QUEUED rows, changes title/content only, validates the Notification response and commits last. Path/body failures and ineligible targets use 422; missing target uses 404; DB/projection/commit failures safely rollback to 500. Current OpenAPI has 55 templates / 65 operations. Tests use fake DB rows; live schema, deployment and dedicated permission are not verified.

## API #95 Admin notification DELETE route

`DELETE /api/v1/admin/notifications/{notification_id}` shares #94's registered path template and adds one OpenAPI operation, for 55 paths / 66 operations. The raw route forwards path/header and the blocking view runs through `run_in_threadpool`; no body/query is declared. Shared ADMIN auth precedes custom signed-int64 parsing. Success is HTTP 200 DeleteResult and catalog errors are 401/403/404/422/500. The local DERIVED eligibility gate locks parent then delivery rows and requires at least one all-QUEUED set; it deletes the selected parent and maps DB `CURRENT_TIMESTAMP` from DELETE RETURNING. Fake DB tests do not prove live schema, PostgreSQL locks/cascade, scheduler/provider cancellation or dedicated permission.

## API #96 Admin notification status

`GET /api/v1/admin/notifications/{notification_id}/status` adds a new route template and is included in `DESIGN_CONTRACT_PATHS`; current OpenAPI has 56 paths / 67 operations. The raw path/header are forwarded through `run_in_threadpool` so shared ADMIN auth runs before signed-int64 parsing. Success remains the direct `ApiEnvelope<Notification>`; exact errors are 401/403/404/500. A single read-only query joins one legacy candidate notification to grouped outbox rows and maps channels/status with API #92's local precedence. Invalid path or no delivery rows returns 404; SQL/projection errors rollback to safe 500. Fake-DB HTTP tests do not verify live schema/deployment, policy approval or fine-grained permission.

## API #97 Admin reported discussions

`GET /api/v1/admin/discussions/reported` adds one path and operation; current OpenAPI has 57 paths / 68 operations. The raw query parameters and Authorization are forwarded to the view so the shared ADMIN guard runs before custom signed-int32 page parsing or DB access. Success remains `ApiEnvelope<Page<Discussion>>`; exact catalog errors are 401/403/500, with a local DERIVED 422 for invalid page. Count and list use the local `discussion_reports` candidate and deduplicate at Discussion grain over OPEN/IN_REVIEW reports. The list projects the existing Discussion shape with a derived normalized content title and empty comments. Focused tests: 15; full Study suite: 1315. Fake-DB tests do not verify live schema, migration deployment, report ingestion or fine-grained permission.
