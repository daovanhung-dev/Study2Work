# Study declared API surface

Global status: current route source is `SOURCE_BACKED`; `app.main` import and
the full Study test suite cover current `guest`, `mentor` and `admin` modules (57 route templates / 68 operations after API #97). Current
auth login/refresh, verify-email dispatch, current-user,
category, course, course-search, course-detail, curriculum, resource-detail,
avatar-upload, upload-metadata, profile-update, API #46 Mentor course, API #47
Mentor lecture, #48 lecture detail, #49–#53 Content routes, #54 Mentor
submissions list, #55 submission detail, #56 grade, #57 feedback, #58–#61
support-request flows, #62 Mentor course-student roster and #63–#64 Mentor
notification dispatch/status, API #65 Mentor course progress, API #66 Mentor course activity analytics, API #67 Mentor Student progress, API #68 Admin user listing, API #69 Admin user detail, API #70 Admin user update, API #71 Admin user status, API #72 Admin user delete and API #73 Admin course listing, API #74 Admin course detail, API #75 Admin course update, API #76 Admin course status, API #77 Admin course delete, API #78–#81 Admin Content moderation and API #82–#86 Admin lesson list/detail/update/status/delete and API #87–#91 Admin quiz list/create/update/delete/statistics, API #92–#96 notification list/create/update/delete/status and API #97 reported-discussion queue are wired; the AI route remains `UNWIRED`. API
API #84 shares the existing lesson-detail route template; typed request-body validation runs in FastAPI before the endpoint's ADMIN guard. API #08/#09 route, import and HTTP
behavior pass in the current full Study test run.

## Composition-root routes

### `GET /`
Source: `app/main.py:create_app -> root`.
Result: `SYSTEM_ROOT_LOADED`, message `Welcome to Study2Work.`, data
`{service: study-api}` through `success_response`.

### `GET /health/live`
Intended result: `SYSTEM_HEALTH_LIVE`, service/environment. No dependency probe.

### `GET /health/ready`
Intended result: `SYSTEM_HEALTH_READY`, service/environment and labels `{database: configured, redis: configured|not_configured}`. **Database is not probed.**

## `/api/v1` declarations in `app/api/v1.py`

### `GET /api/v1/hello`
Body declaration: `{"message":"hello world!"}`. No auth dependency. Verified
through the current FastAPI composition.

### `GET /api/v1/test/db`
Calls `get_engine().connect()` then `SELECT NOW()` with SQLAlchemy `text`; returns
list of first-column values. No standard envelope. The route is composed, while
the separate health readiness endpoint does not probe the database.

### `POST /api/v1/auth/register`
Implemented input `RegisterRequest`; dependency `get_db`; calls
`app.modules.guest.api_01_auth_register.view.create_user(...)` with trace ID.
The flow checks duplicate email, hashes the password with Argon2id, inserts into
the `users` relation referenced by current SQL, commits the transaction and
returns the safe profile envelope. The active schema is not asserted here
without live metadata.
Verification dispatch is not part of the register transaction. Direct API #2
invocation uses the current injectable development stub and does not claim real
email delivery.

### `POST /api/v1/auth/login`
Implemented through `app.modules.guest.api_03_auth_login.view.login(...)`. It looks up
the user by email, verifies the stored password hash, requires `status=ACTIVE`,
creates a JWT access token, stores only the HMAC refresh-token hash, commits the
session and returns the profile plus token fields.
Success is HTTP `200` with `DESIGN_RESOURCE_RETRIEVED`. Unknown/wrong
credentials return `401 DESIGN_AUTHENTICATION_REQUIRED`; inactive accounts
return `403 DESIGN_ACCESS_DENIED`; database/token failures return
`500 DESIGN_INTERNAL_ERROR`.

### `POST /api/v1/auth/refresh`
Implemented through `app.modules.guest.api_03_auth_login.view.refresh(...)`. It hashes
the supplied opaque token, requires an unrevoked and unexpired DB row for an
active user, revokes that row and inserts a new hashed refresh token in the same
transaction, then returns a new access-token pair and profile.
Invalid, expired or already rotated tokens return
`401 DESIGN_AUTHENTICATION_REQUIRED`.

### `POST /api/v1/auth/verify-email/send`

Implemented through `app.modules.guest.api_02_auth_verify_email_send.view.send_verification_email(...)`.
The route is public, accepts JSON `{user_id, email}`, ignores any Authorization
header, does not resolve the database dependency and does not verify user
existence or email ownership because DD #2 does not provide that query contract.

The view calls the injectable `app.service.email.provider.VerificationEmailProvider`.
The current default is `StubVerificationEmailProvider`, which accepts the
dispatch without sending a real email. A successful response is HTTP `202` with
`DESIGN_OPERATION_ACCEPTED` and `data: {status: "accepted"}`. Provider failures
before acceptance map to `500 DESIGN_INTERNAL_ERROR`; raw provider details are
not returned or logged. No token/link/expiry/retry field, DB mutation or retry
worker is currently implemented.

### `GET /api/v1/users/me`
Implemented through `app.modules.guest.api_04_users_me.view.get_current_user(...)`.
The route requires one `Authorization: Bearer <jwt>` header and no request body,
path parameter or query parameter. It decodes the current API#3 JWT shape
(`sub` + `roles`), requires the normalized `STUDENT` role, then reads the
public profile columns from `users` by the numeric `sub` value. It returns
`DESIGN_RESOURCE_RETRIEVED` with `id`, `full_name`, `email`, `role`,
`avatar_url`, `phone`, `status`, `created_at` and `updated_at`; `bio` is omitted
because no current `users` column is source-backed.

Missing/malformed/invalid claims and a missing user return
`401 DESIGN_AUTHENTICATION_REQUIRED`; a non-Student role returns
`403 DESIGN_ACCESS_DENIED`; query or profile mapping failures return
`500 DESIGN_INTERNAL_ERROR`. The route never selects `password_hash` and does
not mutate the database.

### `GET /api/v1/categories`

Implemented through `app.modules.guest.api_05_categories.view.get_categories(...)`.
The route is public, accepts only optional query `locale` and has no request
body, path parameter, pagination, sort or authorization requirement. Missing
locale resolves to `vi-VN`; a provided locale is matched exactly. The query
selects `id`, `name`, `slug` and nullable `description` from `categories` where
`status = 'ACTIVE'` and `locale = :locale`, ordered by `id`.

Success is HTTP `200` with `DESIGN_RESOURCE_RETRIEVED` and
`data.items` plus implicit pagination `{page: 1, size: total, total,
total_pages: 1}`. An empty result is still a successful empty page. Request
validation maps to `422 DESIGN_VALIDATION_ERROR`; database or mapping failure
maps to `500 DESIGN_INTERNAL_ERROR`. No live schema/migration application is
claimed by source or tests.

### `GET /api/v1/courses`

Implemented through `app.modules.guest.api_06_courses.view.get_courses(...)`. The route
is public and accepts optional `category`, `page`, `size` and `sort` query
parameters. `page` defaults to `1`; `size` defaults to `20` and is limited to
`1..100`. `sort` accepts one allow-listed `field:direction` pair over `id`,
`name`, `price` or `created_at`; the default order is `created_at DESC, id ASC`.

The query reads only `courses.status = 'PUBLISHED'`, joins the public mentor
projection from `users`, and returns `CoursePage` items with decimal-string
prices. `category` is parsed but returns `422 DESIGN_VALIDATION_ERROR` until a
course-category relation is source-backed. A published course with a missing
mentor, query/mapping failure or database failure maps to safe
`500 DESIGN_INTERNAL_ERROR`. Empty and out-of-range pages return HTTP `200`;
`total_pages` is zero when `total` is zero. No migration or live schema
verification is claimed.

### `GET /api/v1/courses/search`

Implemented through `app.modules.guest.api_07_courses_search.view.search_courses(...)`. The
route is public and accepts optional `q`, `category`, `page` and `sort` query
parameters. `q` is trimmed/lowercased; blank input removes the text predicate.
`page` defaults to `1`, page size is fixed at `20`, and `sort` uses the
allow-listed `field:direction` format over `id`, `name`, `price` and
`created_at`, with default order `created_at DESC, c.id ASC`.

The query selects only `PUBLISHED` courses, searches `LOWER(c.name)` with a
bound `q_pattern`, reads mentor summary fields from `users`, and applies the
same predicates to the count query. A supplied `category` is rejected with
`422 DESIGN_VALIDATION_ERROR` before DB access because no source-backed
course-category relation exists. Missing mentor integrity, query failures and
mapping failures return safe `500 DESIGN_INTERNAL_ERROR`; empty results return
`200 DESIGN_RESOURCE_RETRIEVED` with fixed-size pagination. No schema or live DB
verification is claimed.

### `GET /api/v1/courses/{course_id}`

Implemented through `app.modules.guest.api_08_courses_detail.view.get_course_detail(...)`.
The route is public. It validates the path ID, selects one `PUBLISHED` course
with the public mentor projection from `users`, and returns a singleton
`CoursePage`. An invalid ID, missing course or unpublished course maps to
`404 DESIGN_RESOURCE_NOT_FOUND`; query or mapping failures map to
`500 DESIGN_INTERNAL_ERROR`. API #08 source and HTTP tests pass in the current
full suite; no live schema check is claimed.

### `GET /api/v1/courses/{course_id}/curriculum`

Implemented through `app.modules.guest.api_09_courses_curriculum.view.get_course_curriculum(...)`.
The route is public. It requires a `PUBLISHED` course, then reads its
`PUBLISHED` lessons ordered by `sort_order` and `id`, returning a `LessonPage`.
An invalid ID or missing/unpublished course maps to `404
DESIGN_RESOURCE_NOT_FOUND`; query or mapping failures map to
`500 DESIGN_INTERNAL_ERROR`. An empty result is a successful page with zero
items. API #09 source and HTTP tests pass in the current full suite; no live
schema check is claimed.

### `GET /api/v1/resources/{resource_id}`

Implemented through `app.modules.guest.api_12_resources_detail.view.get_resource_detail(...)`.
The route is public and reads the resource metadata. If a resource has a lesson,
the view also requires a published parent course; invalid, missing or
unpublished-parent resources return `404 DESIGN_RESOURCE_NOT_FOUND`. Success is
`200 DESIGN_RESOURCE_RETRIEVED` with the source-backed resource fields, including
the URL stored on the resource. The route does not inject a storage signer.

### `POST /api/v1/users/me/avatar`

Implemented through `app.modules.guest.api_13_users_me_avatar.view.upload_avatar(...)`.
The route has no database dependency and uses the shared Student Bearer guard.
JSON `{image}` must contain a strict Base64 Data URL for PNG, JPEG or WebP; the
decoded image is limited to 5 MiB and its signature must match the declared MIME.
Extra request fields are rejected.

`app.service.object_storage.avatar.S3AvatarStorageProvider` reads its required
configuration from process environment when upload is requested, so missing
storage configuration does not prevent app startup. It writes
`avatars/{user_id}` with the checked `Content-Type`, then returns a URL derived
from `OBJECT_STORAGE_PUBLIC_BASE_URL`. The client uses a five-second connect
timeout, 30-second read timeout and one attempt. Same-user uploads overwrite the
same key. Failures map to `500 DESIGN_INTERNAL_ERROR` without provider details.

Success is `201 DESIGN_RESOURCE_CREATED` with
`ApiEnvelope<AvatarUploadResult>`; `data` contains only `avatar_url`. API #13
does not update `users.avatar_url`; API #14 remains the profile update step in
AC-11. Route, parser, auth, storage failure and S3 stub behavior have local
tests; no remote storage call or credential check is claimed.

### `PUT /api/v1/users/me/profile`

Implemented through `app.modules.guest.api_14_users_me_profile.view.update_profile(...)`.
The route requires Student Bearer auth and owns the profile database update.
In AC-11 the client sends the URL returned by API #13 as `avatar_url` in this
follow-up request.

### `GET /api/v1/mentor/courses`

Implemented through `app.modules.mentor.api_46_mentor_courses.view.get_mentor_courses(...)`.
The route requires `Authorization: Bearer <jwt>`, a positive numeric JWT `sub`,
and a `roles` claim containing `MENTOR`. Missing/invalid authentication returns
`401 DESIGN_AUTHENTICATION_REQUIRED`; another role returns
`403 DESIGN_ACCESS_DENIED`. Authentication and role checks run before DB access.

Optional `status` accepts `DRAFT` or `PUBLISHED`. When omitted, the query has no
status predicate. `page` defaults to `1`, `size` to `20`, and size is limited to
`1..100`. Results are ordered by `created_at DESC, id ASC`. Both page and count
queries bind the numeric subject as `courses.mentor_id` and use the same
optional status predicate. The query reads `courses` and its public mentor
projection from `users`; assigned courses are not included.

Success is `200 DESIGN_RESOURCE_RETRIEVED` with the shared `CoursePage` shape,
decimal-string prices, and no category field. Empty and out-of-range pages are
successful. Invalid status/pagination returns `422 DESIGN_VALIDATION_ERROR`;
SQL errors or required course/mentor mapping failures return safe
`500 DESIGN_INTERNAL_ERROR`. Error envelopes use `data: null`. Local route tests
cover authentication, validation, query parameters, mapping, pagination and DB
failures. No live schema or deployment verification is claimed.

### `POST /api/v1/mentor/courses/{course_id}/lectures`

Implemented through `app.modules.mentor.api_47_mentor_lectures_create.view.create_lecture(...)`.
The route requires a Mentor Bearer JWT and uses the shared role guard before DB
access. `course_id` and body integers use signed 64-bit/32-bit bounds; `title`
is limited to 200 characters from the legacy `lessons.name` column. Request
`content` remains an integer and is converted to its decimal string for
`lessons.content` and response `data.content`.

Course access requires direct ownership through `courses.mentor_id`; course
status is not filtered. Missing course returns `404 DESIGN_RESOURCE_NOT_FOUND`,
and a different owner returns `403 DESIGN_ACCESS_DENIED`. `asset_refs` must be a
JSON string containing unique signed-int64 upload IDs; `[]` is valid. The query
resolves only rows with the same `owner_id`, `purpose='LECTURE'`, and path
`course_id`; every missing or out-of-scope ID returns the same
`404 DESIGN_RESOURCE_NOT_FOUND`. Assets are returned in request order.

Success is `201 DESIGN_RESOURCE_CREATED` with the Study envelope and
`LectureResponse`; the insert explicitly sets status `PUBLISHED` and both
required timestamp columns to `CURRENT_TIMESTAMP`. The view commits after
mapping the response and rolls back query/insert/commit failures to
`500 DESIGN_INTERNAL_ERROR`. Focused tests cover auth, integer/title validation,
JSON asset references, course ownership, scoped resolution, order and
transaction failures. Non-empty refs are inserted into `lesson_uploads` in the
same transaction, with zero-based order; an incomplete relation insert rolls
back the lesson. Tests use fake DB queries; checked-in migration 005 is not
proof of live schema deployment.

### `GET /api/v1/mentor/lectures/{lecture_id}`

Implemented through
`app.modules.mentor.api_48_mentor_lecture_detail.view.get_lecture(...)`.
The route requires Mentor Bearer auth, exposes `lecture_id` as integer/int64 in
OpenAPI, and maps malformed/out-of-range IDs to the catalog's
`404 DESIGN_RESOURCE_NOT_FOUND`. It reads a lesson with its parent course,
requires direct `courses.mentor_id` ownership, and does not filter lesson
status. It reads `lesson_uploads` in `asset_position` order and resolves
metadata from `uploads` scoped to the same Mentor, `LECTURE` purpose and course.
Unlinked lectures return `assets: []`; unresolved link metadata returns safe
`500 DESIGN_INTERNAL_ERROR`. SQL NULL content is returned as JSON null.

Success is `200 DESIGN_RESOURCE_RETRIEVED` with `LectureResponse`; catalog
errors remain limited to 401/403/404/500. Focused HTTP tests cover auth,
ownership, malformed/missing IDs, broken parent/link integrity, ordering,
nullable content, safe DB errors and OpenAPI. Tests use fake DB queries and do
not verify migration 005, live schema or assigned-course access.

### `GET /api/v1/mentor/courses/{course_id}/content`

Implemented through `app.modules.mentor.api_49_mentor_content_list.view.get_course_contents(...)`.
The route requires a Mentor Bearer JWT, documents `course_id` as signed int64 in
OpenAPI, and parses the raw path in the view so malformed/out-of-range IDs map
to catalog `404 DESIGN_RESOURCE_NOT_FOUND`. It reads the course and requires
direct `courses.mentor_id` ownership; missing course is 404 and a different
owner is 403.

The view reads `contents` rows for the course where `deleted_at IS NULL`, with
all statuses included and stable `parent_id NULLS FIRST, content_order, id`
ordering. It returns a flat `Content[]`; `parent_id` links nodes and null root
values are omitted. Duplicate IDs, missing parents, cross-course projections,
cycles or DB failures produce a safe `500 DESIGN_INTERNAL_ERROR` after rollback.
An existing course with no active nodes returns `200 DESIGN_RESOURCE_RETRIEVED`
with `data: []`; the endpoint does not commit. Focused HTTP tests cover auth,
owner access, malformed/missing IDs, empty tree, projection/tree integrity,
errors, trace and OpenAPI. Checked-in DDL/migration 006 do not prove live schema
or deployment; assigned-course access and Content enum/payload/version policy
remain unverified.

### `POST /api/v1/mentor/content`

Implemented through `app.modules.mentor.api_50_mentor_content_create.view.create_content(...)`.
The request requires Bearer JWT role `MENTOR` and body fields `course_id` as
strict signed int64, strict string `content_type`, strict string `title`, and
JSON object `payload`; undeclared body fields are rejected. The shared guard
resolves numeric JWT `sub`, and the view requires direct ownership through
`courses.mentor_id`; course status is not filtered. Missing and non-owned
courses both return `403 DESIGN_ACCESS_DENIED` (a derived choice because API
#50 does not declare 404).

The view locks the course row for the transaction, allocates the next order
among active root nodes starting at 0, then inserts `contents` with
`parent_id=NULL` and `status='PENDING_REVIEW'`. The initial status, root
placement, order rule and absent-course mapping are derived implementation
decisions; enum members and payload subtype validation remain unknown. A
validated INSERT/RETURNING row is committed before returning `201
DESIGN_RESOURCE_CREATED` with the shared Content projection. Local tests cover
validation, ownership, transaction failures, trace and OpenAPI. Checked-in
DDL/migration 006 and fake DB tests do not verify the live schema or deployment.

### `PUT /api/v1/mentor/content/{content_id}`

Implemented through `app.modules.mentor.api_51_mentor_content_update.view.update_content(...)`. The route requires Mentor Bearer auth and documents `content_id` as signed int64. The strict full-replacement body `{content_type, title, payload}` is DERIVED from API #50 because catalog #51 and AC-22 omit request fields; body validation returns `422 DESIGN_VALIDATION_ERROR`. Malformed/out-of-range path IDs return catalog 404.

The view locks active Content and its Course, checks direct `courses.mentor_id` ownership, snapshots prior Content in `content_versions`, updates the current `contents` row and moves it to `PENDING_REVIEW` in one transaction. Response is HTTP 200 `DESIGN_RESOURCE_UPDATED` with the shared Content projection. Catalog error codes remain 401/403/404/422/500; no 409 is added. Focused HTTP tests use fake DB queries. Migration 007/live schema are not verified; `archived_by` is not original-author provenance, and public published-version selection plus AC-33 review integration remain open.

### `PATCH /api/v1/mentor/content/{content_id}/publish`

Implemented through `app.modules.mentor.api_52_mentor_content_publish.view.publish_content(...)`. The route requires Mentor Bearer auth and documents signed-int64 `content_id`. Its strict `{published: boolean}` target body is DERIVED because catalog #52 and AC-22 declare path only; body shape errors return `422 DESIGN_VALIDATION_ERROR`.

The view locks active Content and its Course, checks direct `courses.mentor_id` ownership, and changes only `contents.status`: `APPROVED → PUBLISHED` or `PUBLISHED → APPROVED`. Same-target requests are no-ops. Other states return `422`; APPROVED is only the available status readiness gate, not a payload/asset completeness check. Response is HTTP 200 `DESIGN_RESOURCE_UPDATED` with the API #49 Content projection. Focused HTTP tests use fake DB queries; migration 006/live schema and deployment are unverified. Request body, transitions, readiness gate and direct-owner mapping remain DERIVED; AC-33 approval semantics and revision selection remain open.

### `DELETE /api/v1/mentor/content/{content_id}`

Implemented through `app.modules.mentor.api_53_mentor_content_delete.view.delete_content(...)`. The route exposes signed-int64 `content_id`, has no request body/query, and returns the catalog `DeleteResult(id, status="deleted", deleted_at)` with HTTP 200 `DESIGN_RESOURCE_DELETED`.

The view authenticates `MENTOR` before DB access, locks active Content and its Course, checks direct `courses.mentor_id` ownership, checks for active direct children, then soft-deletes with `contents.deleted_at = CURRENT_TIMESTAMP`. Active-child and PUBLISHED 422 guards are DERIVED; API #52 must first unpublish under the current fallback. Other statuses are currently deletable. Repeated DELETE of a tombstoned row returns 404 through the active-row lookup. Focused HTTP tests use fake DB queries; migration 006/live schema and deployment remain unverified. Moderation queue withdrawal, complete dependency coverage, retry policy and direct-owner assignment policy remain open.

### `GET /api/v1/mentor/submissions`

Implemented through `app.modules.mentor.api_54_mentor_submissions_list.view.get_mentor_submissions(...)`. Requires Bearer role `MENTOR` and returns `Page<Submission>` for courses directly owned by the numeric JWT subject. Optional `course_id` is owner-checked, `status` is an exact string filter, and `page` is 1-based with fixed size 20 and stable `submitted_at DESC, id DESC` ordering. Empty results return an empty page.

Submission file metadata is resolved only when legacy `assignment_submissions.file_url` exactly matches an `uploads.url` for the same `user_id`, `SUBMISSION` purpose and course. This association is DERIVED because no FK exists and API #35 file-ref encoding is unresolved. Inner joins exclude null/orphan assignment, course and student relations. Query range failures return 422; the catalog 409 has no implemented trigger. Focused TestClient tests use fake DB data; no live schema or deployment verification is claimed.

### `GET /api/v1/mentor/submissions/{submission_id}`

Implemented through `app.modules.mentor.api_55_mentor_submissions_detail.view.get_mentor_submission(...)`. Requires Bearer role `MENTOR`, exposes signed-int64 path metadata, and maps malformed/out-of-range raw IDs and missing submissions to catalog 404. The view reads the legacy BIGINT candidate through LEFT JOINs to assignments/courses, returns 500 for null/orphan required relations, and checks direct `courses.mentor_id` ownership before mapping a response; another owner returns 403.

The response reuses API #54's `SubmissionResponse` fields and constrained 0/1 UploadAsset URL/owner/purpose/course lookup. AC-23 says to read rubric, but the catalog `Submission` has no rubric field and the legacy assignment model has no relation to the V1-PILOT UUID rubric schema; API #55 does not query or return rubric. This remains a discrepancy requiring schema/contract confirmation. Focused TestClient tests use fake DB rows; live schema, assigned-Mentor access and API #35 URL compatibility remain unverified.

### POST /api/v1/mentor/submissions/{submission_id}/grade

Implemented through app.modules.mentor.api_56_mentor_submissions_grade.view.grade_mentor_submission(...). Requires Bearer role MENTOR; malformed signed-int64 path values map to catalog 404. The view locks the candidate submission row, validates direct courses.mentor_id ownership, enforces the DERIVED range 0 <= score <= assignments.max_score, and updates only score/status to GRADED. The request's required rubric_items string is accepted under a DERIVED wire key but is not persisted because no target is supported by the checked-in schema. Existing feedback is preserved.

The reusable API #54 Submission response is built before commit. A constrained exact URL/owner/SUBMISSION-purpose/course upload lookup returns zero or one asset. The transaction commits only after response projection validation and rolls back failures. Catalog 401/403/404/422/500 codes are retained; middleware recognizes the dynamic route template. Focused TestClient tests use fake DB results; live schema/deployment and rubric persistence remain unverified.

### `POST /api/v1/mentor/submissions/{submission_id}/feedback`

Implemented through `app.modules.mentor.api_57_mentor_submissions_feedback.view.save_mentor_submission_feedback(...)`. It requires Bearer role `MENTOR`, exposes signed-int64 path metadata and maps malformed/overflow IDs to catalog 422. The request uses required strict string fields `feedback_text` (DERIVED wire key from descriptor `feedback text`) and `attachments`; `attachments` is accepted as opaque input and is not persisted or returned because no target/format is supported.

The view locks the candidate submission and LEFT JOINs assignment/course, checks direct `courses.mentor_id` ownership, then updates only `assignment_submissions.feedback` with the owner predicate repeated in SQL. Repeated calls overwrite that one field under a DERIVED fallback. Score/status are preserved, with no `GRADED` direct-call precondition. The response reuses #54 `SubmissionResponse` and its constrained zero-or-one UploadAsset lookup. It validates the projection before commit and rolls back failures. Focused TestClient tests use fake DB data; live schema, attachment storage, assigned-Mentor access and deployment remain unverified.

### `GET /api/v1/mentor/support/requests`

Implemented through `app.modules.mentor.api_58_mentor_support_requests.view.get_mentor_support_requests(...)`. It requires Bearer role `MENTOR`, scopes every row through direct `courses.mentor_id`, and returns `ApiEnvelope<SupportRequest[]>`. Optional `course_id` and exact `status` filters combine with AND; there is no pagination, and an empty or missing-course result is `data: []`. Requests are ordered newest first; nested messages are chronological.

The collection cardinality, no-pagination behavior, legacy BIGINT `support_requests`/`support_messages`/`support_message_uploads` schema, status set and direct-course ownership are DERIVED fallbacks documented in API #58 DD. Attachment links must resolve to same-author/course `UPLOADED` metadata with role-appropriate purpose. Query validation returns 422 for invalid `course_id`; standard 401/403/500 errors remain. Focused and full HTTP tests use fake DB results; checked-in migration 008 does not prove live schema or deployment.

### `GET /api/v1/mentor/support/{request_id}`

Implemented through `app.modules.mentor.api_59_mentor_support_request_detail.view.get_mentor_support_request(...)`. It requires Bearer role `MENTOR`, documents a signed-int64 path, and maps malformed/overflow path input to the catalog 404. The response is one `SupportRequest` object reusing API #58 request, student, message and UploadAsset models. Missing request returns 404; an existing request owned by another Mentor returns 403 under the selected DERIVED policy.

The view checks the direct course owner, validates request/course/student parent projections, and reads the full thread in `created_at ASC, id ASC` order. Message uploads use API #58's owner/course/role-purpose/UPLOADED constraints and `asset_position` order. Empty threads return `[]`; unresolved links fail the response safely with 500. The API is read-only. Local tests use fake DB rows; migration 008, live schema and deployment remain unverified, and the support fallback is DERIVED.

### `POST /api/v1/uploads`

Implemented through `app.modules.student.api_34_uploads.view.create_upload(...)` and
uses an injectable provider from `app.service.object_storage.upload`. The
multipart request requires `file` and purpose `SUBMISSION` or `LECTURE`; an
optional `course_id` is accepted. The shared JWT guard accepts Student or
Mentor, then binds Student to SUBMISSION and Mentor to LECTURE. Student
SUBMISSION with course_id requires ACTIVE enrollment; Mentor LECTURE requires
course_id and direct `courses.mentor_id` ownership.

The view measures bytes from the received file spool, retains the provided
filename or uses `upload`, and retains the part Content-Type or uses
`application/octet-stream`. It streams to S3-compatible storage under a
server-generated UUID key and returns a public URL from
`OBJECT_STORAGE_PUBLIC_BASE_URL`. After object upload it inserts the metadata
row into the new legacy BIGINT `uploads` table with status `UPLOADED` and commits.
Storage failures return `503 DESIGN_DEPENDENCY_UNAVAILABLE`; DB failures return
`500 DESIGN_INTERNAL_ERROR` after rollback and best-effort object deletion.
Local HTTP tests cover role/purpose checks, enrollment/ownership, multipart
validation, metadata, fallbacks and failure cleanup. The migration is source
only; live DB, real S3 and deployment are not verified.

### `POST /api/v1/chat_log_ai`
Not currently exposed; implementation remains `UNWIRED`. This is **not** the
same runtime implementation as AI Server's `ChatLogRequest` route.

## Editing rule

Before implementing/fixing any future declared route, inspect current
`app/api/v1.py`, then require source/contract for every missing request
model/use-case/table. Do not copy AI Server chat implementation or legacy Study
auth code unless explicitly approved.


### `POST /api/v1/mentor/support/{request_id}/reply` — API #60
The route is composed after API #59 and registered in `DESIGN_CONTRACT_PATHS`. It exposes raw path text with signed-int64 OpenAPI metadata and a strict JSON body (`message`, `attachment_refs`). The shared MENTOR guard runs before DB access. The view locks the request, enforces direct course ownership, validates same-Mentor/course `LECTURE`/`UPLOADED` refs, inserts the message and ordered link rows, reloads the full API #59 thread projection, then commits. It returns `DESIGN_RESOURCE_UPDATED`; request status is unchanged. Focused tests use fake DB results; live schema, migration deployment, concurrency and post-resolve policy remain unverified.

### `PATCH /api/v1/mentor/support/{request_id}/resolve` — API #61
The route uses the shared MENTOR guard, raw signed-int64 path parsing and no request body. It locks the BIGINT `support_requests` row, checks direct course ownership, transitions active statuses to `RESOLVED`, and treats a repeated resolve as success without replacing `resolved_at`. `CANCELLED` is rejected with catalog 422. The full API #59 thread projection is validated before commit. These lifecycle/schema choices are DERIVED from local migration 008 and #58–#60; tests use fake DB results and do not prove live schema/deployment.

### `GET /api/v1/mentor/courses/{course_id}/students` — API #62
The route requires the shared MENTOR guard and a raw signed-int64 path. It checks `courses.id/mentor_id`, then reads distinct `users.id/full_name/avatar_url` through `ACTIVE` enrollments, filtered to `users.role='STUDENT'` and ordered by user ID. It returns `ApiEnvelope<UserSummary[]>` with no pagination; malformed/out-of-range path and missing course return 404, owner/role mismatch returns 403, and an empty roster returns 200 `data: []`. The array response, legacy BIGINT tables, ACTIVE predicate and direct-owner policy are DERIVED and remain `Draft — Needs Confirmation`; fake-DB tests do not prove live schema/deployment.

### `POST /api/v1/mentor/notifications` — API #63
The route requires the shared MENTOR guard and preserves the catalog body fields `recipients:string`, `title:string`, `content:int64`, and `channels:string`. Local validation parses ordered CSV positive Student IDs and `PUSH`/`EMAIL` channels, collapsing duplicates. Since the body has no course ID, a DERIVED scope check requires every recipient to share an ACTIVE roster in at least one directly owned course. Within one transaction it inserts one legacy BIGINT notification per recipient and one `QUEUED` delivery-outbox row per channel; the response is HTTP 202 `ApiEnvelope<Operation>` with an Operation UUID and `meta.notification_ids`. The local mapping, CSV encoding, common-course rule and outbox are DERIVED and the DD remains Draft. HTTP tests use fake DB sessions; live migration/schema and worker/provider delivery are unverified.

### `GET /api/v1/mentor/notifications/{notification_id}/status` — API #64
The route requires the shared MENTOR guard, parses the raw path as signed
int64, and reads the notification plus channel outbox in one query. It checks
`notifications.sender_id` against JWT `sub`, then returns the direct
`ApiEnvelope<Operation>` contract, mapping Operation identity/timestamps from
API #63's local rows and aggregate status from `QUEUED`/`SENT`/`FAILED` channel
states. Malformed/out-of-range path and absent dispatch rows return 404; a
different sender returns 403. The operation writes nothing and calls no
provider. This local mapping and owner rule are DERIVED and the DD stays Draft;
fake-session tests do not verify live schema, migration 009 deployment or
Push/Email delivery.

### `GET /api/v1/mentor/courses/{course_id}/progress` — API #65
The route reads raw path/header values, declares the required signed-int64 path
and auth header in OpenAPI, and exposes the catalog 200/401/403/404/500 set
without synthetic 422. It authenticates MENTOR, checks `courses.mentor_id`
against numeric JWT `sub`, then reads distinct ACTIVE Student enrollments and
aggregates progress over PUBLISHED lessons. Duplicate `(user_id, lesson_id)`
rows use latest `last_accessed_at DESC NULLS LAST, id DESC`; percent is the
floor average, with missing progress as zero. No page/size inputs exist, so the
route returns the entire roster in one page. These response, access, eligibility,
duplicate-row, formula and paging decisions are DERIVED; the catalog still says
`Page<Course>` while runtime returns `Page<MentorStudentProgress>`. The GET is
read-only. Focused tests use fake DB sessions; live schema/deployment and
catalog approval are unverified; DD #65 remains Draft.

### `GET /api/v1/mentor/courses/{course_id}/analytics` — API #66
The route reads raw path/header values and declares the required signed-int64 path plus auth header in OpenAPI. It authenticates MENTOR, checks direct `courses.mentor_id` ownership, then aggregates distinct Student/lesson pairs with non-null `lesson_progress.last_accessed_at` on PUBLISHED lessons. The response is a local DERIVED activity summary with pair count, distinct Student count, and latest timestamp; these are current-state proxies, not learning-event counts. The direct diagram/catalog still says `Page<Course>`, which has no analytics fields. DD #66 remains Draft. Focused tests use fake DB rows and do not verify live schema/deployment.

### `GET /api/v1/mentor/courses/{course_id}/students/{student_id}/progress` — API #67
The route reads raw path/header values, declares both required signed-int64 paths and Authorization in OpenAPI, and uses the shared MENTOR guard before DB access. It checks direct `courses.mentor_id` ownership, then requires the requested Student in an ACTIVE enrollment with `users.role='STUDENT'`. It reads PUBLISHED lessons in `sort_order,id` order and chooses the latest progress row by `last_accessed_at DESC NULLS LAST, id DESC`, matching #65. A missing row maps to NOT_STARTED/0; summary is completed count plus floor-average percent, zero for an empty lesson set. This singular response is a DERIVED fallback for AC-26 and conflicts with diagram/catalog `Page<Course>`; DD #67 remains Draft. Focused HTTP tests use fake DB rows and do not verify live schema/deployment.


### `GET /api/v1/admin/users` — API #68

The route requires the shared `ADMIN` JWT role before database access and accepts optional exact `role`/`status`, normalized keyword and positive int32 `page`. It runs matching COUNT and page queries against the checked-in legacy `users` candidate, orders by `id ASC`, and returns `ApiEnvelope<Page<UserProfile>>` with fixed size 20. Invalid page returns 422 `DESIGN_VALIDATION_ERROR`; the query never selects `password_hash` and reuses API #04's safe profile model, omitting unsupported `bio`. List cardinality and pagination/filter rules are DERIVED and reflected in the API #68 catalog and AC-31 diagram. The DD remains Draft because live schema, Admin permission scope, PII/audit and deletion visibility are unverified. Focused/full HTTP tests use fake DB rows and do not prove live schema/deployment.


### `GET /api/v1/admin/users/{user_id}` — API #69

The route reads raw `user_id` path text and exposes required int64 plus Authorization in OpenAPI. It uses the shared `ADMIN` JWT guard before parsing or querying, then reads one safe profile from the checked-in legacy `users` candidate. Invalid/out-of-int64 input and no matching row map to 404 `DESIGN_RESOURCE_NOT_FOUND` to preserve the catalog's 401/403/404/500 set; no 422 is added. The response reuses API #04 `UserProfile`, retains nullable avatar/phone as null and omits unsupported bio/password hash. The legacy target and invalid-path mapping are DERIVED; focused/full tests use fake DB sessions and do not prove live schema/deployment.

### `PUT /api/v1/admin/users/{user_id}` — API #70

The route declares the required Authorization header, signed-int64 `user_id` and strict JSON body. The shared `ADMIN` guard runs before path/body validation and DB access. Because the direct catalog/diagram omit the request body, the required full-replacement fields (`full_name`, nullable `phone`, nullable `avatar_url`, `role`) and the three known role labels are explicitly DERIVED. One bound UPDATE targets the checked-in legacy BIGINT `users` candidate and returns only API #04 safe profile fields; no row maps to 404 and malformed/out-of-range IDs map to the catalog 422. The view commits only after validating the returned projection and rolls back query/mapping/commit failures. Focused HTTP tests use fake DB sessions; live schema, role-transition policy, audit/PII policy and token invalidation are unverified.

### `PATCH /api/v1/admin/users/{user_id}/status` — API #71

The route requires the shared `ADMIN` JWT role, declares a required signed-int64 `user_id`, Authorization header, and strict JSON body `{status}`. The body is a DERIVED fallback because the catalog and AC-31 diagram do not define it; runtime accepts only `ACTIVE` or `SUSPENDED`, and only transitions rows currently in either state. It locks the legacy BIGINT `users` candidate, updates `status` and `updated_at`, and returns the API #04 safe `UserProfile`. Suspending also revokes unrevoked, unexpired refresh-token rows in the same transaction; activating does not restore them. Existing access JWTs can remain usable until expiry because the shared access-token guard does not query account state. Errors are exactly 401/403/404/422/500. Focused tests use fake DB sessions; live schema, policy approval and deployment are unverified; DD remains Draft — Needs Confirmation.


### `DELETE /api/v1/admin/users/{user_id}` — API #72

The route uses the shared `ADMIN` JWT guard before raw signed-int64 parsing or DB access and returns `ApiEnvelope<DeleteResult>`. Its DERIVED fallback conditionally sets legacy `users.status='DELETED'` and `updated_at=CURRENT_TIMESTAMP`, then maps `updated_at` to response `deleted_at`; missing/already-DELETED returns catalog 404. It preserves dependent rows and does not revoke existing access JWTs. Fake-session tests do not verify live schema/deployment; policy approval remains open.

### `GET /api/v1/admin/courses` — API #73

The route passes raw status/mentor/category/page/header values to the view, documents optional filters and a required Authorization header in OpenAPI, and is registered in `DESIGN_CONTRACT_PATHS`. The shared `ADMIN` JWT guard runs before query validation. Count and page SELECTs share exact status/mentor filters over the legacy BIGINT `courses` candidate and mentor projection; page size is fixed at 20 with `id ASC`. A valid signed-int64 `category` returns 422 before DB access because no course-category relation exists; this is a DERIVED fallback from API #06, not an approved implementation of the catalog filter. The response reuses shared `CoursePage`, omits optional `category` because the runtime Course model has no field, and returns safe 500 for query/count/mapping/integrity errors. The DD remains Draft; tests use fake DB rows and do not verify live schema, deployment or a dedicated course-management permission.


### `GET /api/v1/admin/courses/{course_id}` — API #74

The route authenticates with the shared `ADMIN` JWT guard before parsing the raw signed-int64 path or querying. Malformed/out-of-range IDs and missing rows map to catalog 404. A bound read uses the checked-in legacy BIGINT `courses LEFT JOIN users` candidate with no status filter; the shared Course mapper enforces the required mentor/price projection and decimal formatting. The endpoint returns a singleton `Page<Course>` and never commits; query/projection failures return safe 500 with rollback. The dynamic FastAPI route template is registered in `DESIGN_CONTRACT_PATHS`. Focused tests pass with fake DB rows; dedicated course-management permission, counters, live schema and deployment remain unverified, and the DD stays Draft.

### `PUT /api/v1/admin/courses/{course_id}` — API #75

The route shares the #74 path template and declares `course_id:int64`, Authorization, a strict four-field JSON body, and catalog errors 401/403/404/422/500. The shared `ADMIN` guard runs before raw path/field validation and mutation. It updates only `name`, `description`, `thumbnail_url`, `price` and `updated_at` on the checked-in legacy BIGINT `courses` candidate, then reads the Course/mentor projection in the same transaction. The shared Course mapper and singleton `CoursePage` are validated before commit; absent UPDATE rows return 404, while query/projection/commit failures return safe 500 with rollback. Body semantics, bounds, schema choice and Page cardinality are DERIVED; live schema, deployment and a separate course-management permission remain unverified. Focused tests: 27 passed; linked regression: 113 passed; full Study suite: 872 passed. DD remains Draft — Needs Confirmation.

### `PATCH /api/v1/admin/courses/{course_id}/status`

Implemented through `app.modules.admin.api_76_admin_course_status.view.update_admin_course_status(...)`. The route validates the strict candidate `{status}` body, documents signed-int64 `course_id`, and registers its distinct FastAPI template in the DESIGN error allowlist. The shared `ADMIN` role is checked before raw path parsing/DB access; AC-32's finer course-management permission remains unsupported by current policy source.

The view locks the legacy BIGINT candidate course. For an actual change it updates `status/updated_at`, inserts actor/course/previous/new status into `course_status_audit_logs`, reads the #74 Course projection and commits as one transaction. A same-status request is a DERIVED no-op. Focused HTTP tests use fake DB rows; migration 010/live schema/deployment remain unverified, and the DD remains Draft — Needs Confirmation.

### `DELETE /api/v1/admin/courses/{course_id}` — API #77

The route uses the shared `ADMIN` guard before raw signed-int64 parsing and DB access; malformed/overflow paths map to catalog 422. The view locks a non-`DELETED` legacy BIGINT candidate, checks for any enrollment and for active `contents`/lesson/quiz/assignment rows, then either returns 422 or sets `courses.status='DELETED'` and `updated_at=CURRENT_TIMESTAMP`. `DeleteResult.deleted_at` maps to the DB-returned `updated_at`, following API #72. These dependency/marker/timestamp/repeat-404 choices are DERIVED; no child rows, audit relation, new column or migration is changed. Focused tests: 20 passed; full suite: 910 passed. Fake DB sessions do not verify live schema/deployment. The DD remains Draft, and linked #75/#76/Mentor behavior for deleted courses is still open.

### `GET /api/v1/admin/content/pending` — API #78

The route authenticates with the shared `ADMIN` guard before raw query parsing or DB access. It selects current active legacy-candidate `contents` rows with `status='PENDING_REVIEW'`, exact optional `content_type`/`course_id` filters, count-matched page predicates and stable `id ASC`; page defaults to 1 with fixed size 20. It returns `ApiEnvelope<Page<Content>>`, including empty pages. The catalog and diagram declare singular `ApiEnvelope<Content>`, so collection cardinality, filters, deleted-row exclusion and pagination are DERIVED and remain visible in the Draft DD. Focused tests: 23 passed; linked regression: 160 passed; full Study suite: 933 passed. Fake DB tests do not prove live schema/deployment or moderation permission.


### `GET /api/v1/admin/content/{content_id}` — API #79

The route is registered after static API #78 `/admin/content/pending`, passes raw `content_id` and Authorization to the view, documents signed-int64 path/OpenAPI and catalog 401/403/404/500 errors, and is listed in `DESIGN_CONTRACT_PATHS`. The shared ADMIN guard runs before parsing or DB access. One bound SELECT reads the active checked-in legacy `contents` candidate; only the direct eight-field `ApiEnvelope<Content>` is returned. Invalid/out-of-range path and absent/soft-deleted row map to catalog 404; SQL/projection failures return safe 500 with rollback. AC-33 version/author metadata, revision identity and live schema remain unresolved. Focused tests: 13 passed; full Study suite: 946 passed; Ruff passes. Fake DB tests do not prove live schema/deployment or moderation permission; DD remains Draft.

### `PATCH /api/v1/admin/content/{content_id}/approve` — API #80

The route uses the shared `ADMIN` guard before raw signed-int64 parsing or DB access and is registered in `DESIGN_CONTRACT_PATHS`. It locks one active legacy BIGINT `contents` candidate; missing/soft-deleted rows return 404, while non-`PENDING_REVIEW` rows return 422. A pending row transitions to `APPROVED` and appends `content_review_audit_logs` with numeric JWT `sub`, old/new status and nullable reason in one transaction. It returns the exact eight-field Content response and commits only after projection validation. The status choice, eligibility rule and migration 011 physical schema are DERIVED; API #52 remains publication owner. Tests: 22 focused, 189 linked AC-33/#52/#76 regression, 968 full Study tests; Ruff passes. Fake DB sessions do not prove live schema/deployment or dedicated moderation permission. API #79/#80 do not bind the action to the revision shown earlier; DD remains Draft.

### `PATCH /api/v1/admin/content/{content_id}/reject` — API #81

The route accepts required strict JSON `{reason: string}`, documents raw signed-int64 `content_id` and Authorization, and is registered in `DESIGN_CONTRACT_PATHS`. Shared `ADMIN` auth precedes path parsing and database access. It locks an active legacy BIGINT `contents` candidate, requires `PENDING_REVIEW`, changes status to `REJECTED`, and inserts one `content_review_audit_logs` decision row carrying numeric JWT `sub`, old/new status and submitted reason. This row is the DERIVED persistence target for the direct logical reason effect; no second audit write or Content response field is added. It returns the eight-field Content response and commits after projection validation. Focused tests: 29; linked #49–#53/#78–#81 regression: 200; full Study suite: 997; Ruff passes. Migration 011/live schema, dedicated moderation permission, empty-reason policy and continuity with #79's viewed revision remain unverified; DD stays Draft.

## `GET /api/v1/admin/lessons` — API #82

The route passes raw `course`, `status`, `type` and Authorization values to the API #82 view and exposes all three query names in OpenAPI. Shared `ADMIN` auth runs before query validation or DB access. `course` parses as signed int64; `course` and `status` use exact bound equality against the legacy BIGINT `lessons` candidate. Every query excludes `status='DELETED'`; supplied `status=DELETED` therefore returns an empty list. A supplied `type` returns local DERIVED 422 `DESIGN_VALIDATION_ERROR` / `UNSUPPORTED_FILTER` because no compatible Lesson type field is source-backed. One read-only query orders by `course_id, sort_order, id`, with nulls last; the route returns `ApiEnvelope<Lesson[]>` and `data: []` for no rows. Catalog response is the conflicting singleton `ApiEnvelope<Lesson>`; list cardinality, filters, order and 422 behavior remain DERIVED in the Draft DD. Required Lesson projection failures return safe 500 with rollback. Focused tests: 15; fake DB tests do not prove live schema/deployment or dedicated lesson-management permission.

## `GET /api/v1/admin/lessons/{lesson_id}` — API #83

The route passes raw path ID and Authorization to the API #83 view and documents `lesson_id:int64` plus the exact catalog errors in OpenAPI. Shared `ADMIN` auth runs before raw signed-int64 parsing or DB access. One bound read-only query selects only non-`DELETED` rows from the legacy BIGINT `lessons` candidate and maps them through API #09's reusable direct `Lesson`. No `PUBLISHED` filter, dependency query, count or mutation is added. Malformed/out-of-range path IDs, absent rows and tombstones return 404; invalid required projection or query failure returns safe 500 with rollback. The malformed-path mapping, legacy schema target and optional-null behavior are DERIVED/local; live schema, fine-grained AC-34 permission and dependency output remain unverified. Focused API #83 tests: 15 passed; linked #09/#74/#82 regression: 54; full Ruff passes; OpenAPI: 50 paths / 57 operations. DD remains Draft.

## `PUT /api/v1/admin/lessons/{lesson_id}` — API #84

The PUT shares the #83 FastAPI path template. Its catalog/diagram request is path-only, so the strict JSON full-replacement body `{title, content, video_url, order}` is an explicit DERIVED fallback; typed body validation happens in FastAPI before endpoint auth. For valid requests, the view checks shared `ADMIN`, parses raw signed-int64 path text (422 if invalid), and runs one bound UPDATE/RETURNING against non-`DELETED` rows in the legacy BIGINT `lessons` candidate. The response maps the aliased row through API #09 `Lesson`, then commits. It leaves course_id/status/dependency/audit rows unchanged; missing/tombstoned rows return 404 and query/projection/commit errors return safe 500 with rollback. Focused tests: 23 passed; linked #09/#47/#48/#82–#84 regression: 104; Ruff passes; OpenAPI: 50 paths / 57 operations. Fake DB tests do not prove live schema/deployment or fine-grained AC-34 permission. DD remains Draft.


## `PATCH /api/v1/admin/lessons/{lesson_id}/status` — API #85

The route declares strict `{status}` body, int64 path, Authorization and catalog 401/403/404/422/500 errors; its distinct template is in `DESIGN_CONTRACT_PATHS`. Body/status values `DRAFT`, `PUBLISHED`, `SUSPENDED` are a DERIVED fallback from API #76 because catalog/diagram define no Lesson body or enum. Typed body validation runs before the shared ADMIN guard; for valid bodies the view authenticates ADMIN, parses raw signed-int64 path and then accesses DB. It locks only non-`DELETED` legacy BIGINT Lesson rows, returns 404 when absent/tombstoned, and on change updates status/updated_at plus migration 012 `lesson_status_audit_logs` in one transaction. Same-status requests return the locked Lesson without UPDATE/audit. Projection is checked through API #09 `Lesson` before commit; query/audit/map/commit failures return safe 500 with rollback. Focused tests: 28 passed. Full Study suite: 1078 passed; Ruff passes; OpenAPI: 50 paths / 57 operations. Fake DB tests do not establish live schema, migration deployment or fine-grained AC-34 permission; DD remains Draft.

## `DELETE /api/v1/admin/lessons/{lesson_id}` — API #86

The route shares the #83/#84 path template, so the existing DESIGN error allowlist entry covers all three methods. It passes raw signed-int64 path text and Authorization to the API #86 view and declares no request body. Shared ADMIN auth runs before path parsing/DB access. The view locks a non-`DELETED` legacy BIGINT Lesson, checks `lesson_progress`, `resources` and `lesson_uploads` with EXISTS, and returns catalog 422 without mutation if any exist. Otherwise it sets `status='DELETED'` plus `updated_at`; the returned DB timestamp maps to `DeleteResult.deleted_at` by API #77 precedent. The view commits after projection validation and rolls back query/projection/commit failures. Repeat delete returns 404. Admin #82–#85 and direct Mentor/resource readers #48/#12 hide or reject tombstones. Marker, blocker set, timestamp alias and repeat-delete policy are DERIVED; live schema/FKs and fine-grained lesson-management permission are unverified. Focused tests: 15; linked #82–#85/#48/#12 regression: 110; Ruff passes; OpenAPI: 50 paths / 57 operations. DD remains Draft.


## `GET /api/v1/admin/quizzes` — API #87

The route passes raw query/header values to the API #87 view and is registered in `DESIGN_CONTRACT_PATHS`; OpenAPI declares `course:int64`, `status:string`, `page:int32`, Authorization and 200/401/403/422/500 outcomes. Shared `ADMIN` authentication runs before query parsing or DB access. The view applies exact optional filters to the checked-in legacy BIGINT `quizzes` candidate, excludes `status='DELETED'`, runs count + fixed-size-20 page queries with identical predicates, defaults to page 1 and orders by `id ASC`. It returns local `ApiEnvelope<Page<Quiz>>`, while the catalog declares `ApiEnvelope<Quiz>`. Quiz metadata maps `name`, `time_limit_minutes`, and `passing_score`; `questions=[]` remains API #87’s metadata-only list projection. API #88 defines local DERIVED child-column candidates, but #87 does not load child rows. Invalid/out-of-range course/page returns local 422 `DESIGN_VALIDATION_ERROR`, outside the catalog error set. At the API #87 checkpoint: 20 focused tests, 93 linked regressions, 1113 full-suite tests and 51 templates / 58 operations. At the API #88 checkpoint, the full Study suite had 1134 tests and OpenAPI had 51 templates / 59 operations. Fake DB sessions do not establish live schema/deployment or dedicated quiz-management permission; DD remains Draft.

## `POST /api/v1/admin/quizzes` — API #88

The route shares the #87 `/admin/quizzes` path template, accepts raw request bytes and Authorization, and documents the catalog outer body `{config:string, questions:string}`, HTTP 201, `DESIGN_RESOURCE_CREATED`, `ApiEnvelope<Quiz>` and 401/403/422/500 outcomes. The shared `ADMIN` guard runs before body parsing or DB access. The DERIVED validator decodes `config` and `questions`, checks candidate fields and choice order, and does not enforce type-specific correct-answer counts. The view checks course existence, inserts Quiz → questions → choices using bound SQL, validates the full response projection, then commits; failures roll back. Migration 013 supplies local nullable `question_type` and `sort_order` candidates on legacy BIGINT child tables. Focused tests: 21; linked #87/#88 regression: 41; full Study suite: 1134; Ruff passes; OpenAPI: 51 templates / 59 operations. Checked-in DDL and fake sessions do not verify live schema/deployment or fine-grained AC-35 permission; DD remains Draft.

## `PUT /api/v1/admin/quizzes/{quiz_id}` — API #89

The route passes raw path/body/header to the view and is registered in `DESIGN_CONTRACT_PATHS`. Shared `ADMIN` authentication runs before positive signed-int64 path parsing, #88 outer/embedded body validation and DB access. Catalog/diagram define the method, path, response and 401/403/404/422/500 codes; the `{config:string, questions:string}` body, full replacement, course move, tombstone handling and history guard are DERIVED. The view locks Quiz, current questions and choices, rejects any attempt/answer history before writes, key-share-locks an existing target Course, updates only Quiz metadata/timestamp, deletes choices before questions and inserts ordered replacement children. It validates DELETE/INSERT projections and the complete Quiz response before commit; failures roll back. Focused tests: 26; linked #87–#89 regression: 67; full Study suite: 1160; Ruff passes; OpenAPI: 52 templates / 60 operations. Fake DB tests do not prove live schema/deployment or PostgreSQL FK-lock behavior; AC-35 fine-grained permission is unavailable; DD remains Draft.

## `DELETE /api/v1/admin/quizzes/{quiz_id}` — API #90

The DELETE route shares API #89's registered path template and declares path `quiz_id:int64`, Authorization, HTTP 200, `DeleteResult`, and the catalog 401/403/404/422/500 errors; it has no request body or query parameter. Shared ADMIN auth runs before raw path parsing or DB access. The positive signed-int64 rule is DERIVED. The view locks Quiz, then current questions and choices, and checks attempts plus linked answers. Existing tombstones return stored `updated_at` without mutation. Attempt or answer history sets `status='DELETED'` and updates `updated_at`; no history deletes choices, questions and Quiz in order. It validates locked/returned IDs and maps DB timestamps before commit; query/projection/mutation/commit failures roll back to a safe catalog 500. The answer-only safeguard, hard-delete branch, marker/timestamp and repeat semantics are DERIVED; #29 race/fine-grained AC-35 permission and live schema remain unresolved. Focused tests: 18; linked #86–#90: 100; full Study suite: 1178; Ruff passes; OpenAPI: 52 templates / 61 operations. Fake DB tests do not prove PostgreSQL locks/FKs or deployment; DD remains Draft.

## `GET /api/v1/admin/quizzes/{quiz_id}/statistics` — API #91

The route declares required `quiz_id:int64`, Authorization, HTTP 200 and the exact catalog 401/403/404/500 set; it accepts no body/query and registers the `/statistics` template in `DESIGN_CONTRACT_PATHS`. The shared ADMIN guard runs before raw path parsing and DB access. The view runs one read-only LEFT JOIN aggregate on the legacy BIGINT `quizzes`/`quiz_attempts` candidate and does not filter tombstones or attempt status, read `quiz_answers`, or expose Student identifiers. It returns a separate `QuizStatistics` DTO with attempt/submitted/graded counts, average, passed count and pass rate; those response/metric rules and malformed-ID-to-404 mapping are DERIVED and conflict with diagram/catalog `ApiEnvelope<Quiz>`. DD remains Draft and fine-grained permission/live schema are unresolved. Focused tests: 19; linked #87–#91: 104; full Study suite: 1197; Ruff passes; OpenAPI: 53 templates / 62 operations. Fake DB tests do not prove PostgreSQL query behavior or deployment.

### `GET /api/v1/admin/notifications` — API #92

The route passes raw `status`, `channel`, `page`, and Authorization values so the shared `ADMIN` guard runs before custom page parsing. It is registered in `DESIGN_CONTRACT_PATHS`; OpenAPI declares catalog 401/403/500/503 plus DERIVED page 422. The view reads a matching count and fixed 20-row page from checked-in legacy BIGINT `notifications`/`notification_deliveries` candidates, requiring a delivery row to map required channels/status. Status aggregation follows API #64's QUEUED → FAILED → SENT precedence; filters are exact and sort is `created_at DESC, id DESC`. Runtime returns `Page<Notification>` despite catalog `ApiEnvelope<Notification>`; permission scope, campaign grain, values and DB availability are unverified. Focused tests: 20; linked #63/#64/#87/#92: 85; full Study suite: 1217; OpenAPI: 54 paths / 63 operations. Fake DB tests do not prove live schema or migration deployment; DD remains Draft.


### `POST /api/v1/admin/notifications` — API #93

The route receives raw JSON and Authorization so the shared `ADMIN` guard runs before parsing the body or querying recipients. It shares API #92's path template and therefore adds one operation without adding a path. OpenAPI declares HTTP 202, `ApiEnvelope<Notification>`, the required title/content/channels body fields, and catalog 401/403/422/500/503 errors. The local DERIVED fallback accepts only explicit existing positive unique recipient IDs, unique `PUSH`/`EMAIL`, and nonblank title/content with a 200-character title cap from the legacy DDL candidate. It inserts one legacy BIGINT notification per recipient plus one `QUEUED` outbox row per recipient/channel in one transaction, returning the first Notification and derived batch IDs/UUID in metadata. The view commits before 202 and does not invoke a provider. Focused tests: 26; linked #63/#64/#87/#92/#93: 111; full Study suite: 1243; Ruff passes; OpenAPI: 54 paths / 64 operations. Fake DB tests do not prove live schema, migration deployment, worker delivery, or fine-grained permission; DD remains Draft.


### `PUT /api/v1/admin/notifications/{notification_id}` — API #94

The route receives raw path/body/header and runs the shared ADMIN guard before custom path/body validation or database queries. OpenAPI declares the direct response and catalog 401/403/404/422/500 set, plus a local DERIVED strict `{title, content}` body. The view locks the recipient-level legacy BIGINT notification, then its delivery rows; no delivery row or any status other than QUEUED returns catalog 422. It updates only title/content, preserving audience, channels, schedule, read state, deliveries and `created_at`; the response channels/status are projected from the locked delivery rows. Focused tests: 20; linked #92–#94: 66; full Study suite: 1263; Ruff passes; OpenAPI: 55 paths / 65 operations. Fake DB tests do not prove live schema, PostgreSQL locking, deployment or fine-grained notification permission; DD remains Draft.


### `DELETE /api/v1/admin/notifications/{notification_id}` — API #95

The raw route shares API #94's path template and adds one operation without adding a path. It forwards path/header to the synchronous view through the thread pool; there is no request body or query. Shared ADMIN auth precedes positive signed-int64 parsing. The local DERIVED fallback locks one recipient-level legacy BIGINT parent, then its deliveries, and requires at least one row with every status `QUEUED`; otherwise it returns catalog 422. It deletes only that path-selected parent, relies on the checked-in FK cascade for its outbox rows, and maps `CURRENT_TIMESTAMP` from DELETE RETURNING to DeleteResult before commit. A later repeat returns 404; no scheduler/provider call is made. Focused tests: 21; linked #92–#95: 87; full Study suite: 1284; Ruff check and scoped format pass; OpenAPI: 55 paths / 66 operations. Fake DB tests do not prove live schema/deployment/PostgreSQL locks/cascade or external cancellation; DD remains Draft.

### `GET /api/v1/admin/notifications/{notification_id}/status` — API #96

Adds one path and operation (OpenAPI: 56 `/api/v1` paths / 67 operations). The raw route forwards path/header through the thread pool; there is no body/query. Shared ADMIN auth precedes positive signed-int64 parsing; invalid ID maps to catalog 404. One read-only query reads the legacy candidate notification and grouped outbox rows, then reuses #92's ordered channels and QUEUED/FAILED/SENT precedence in the existing `Notification` response. No delivery counts are added; absent notification/no delivery maps to 404, SQL/projection failures to 500, and GET does not commit. Focused #96 tests: 16; linked #92–#96 regression: 103; full Study suite: 1300. Fake DB tests do not prove live schema/deployment, approved enum/aggregate policy or fine-grained permission; DD stays Draft.

### `GET /api/v1/admin/discussions/reported` — API #97

Adds one path and operation (OpenAPI: 57 `/api/v1` paths / 68 operations). The route accepts optional `reason`, `severity`, and signed-int32 `page`; shared ADMIN JWT auth runs before custom page parsing or DB access. One COUNT and one paged SELECT query `discussions` with the local DERIVED `discussion_reports` relation, counting one Discussion per matching OPEN/IN_REVIEW report group. `reason` and `severity` are exact-match AND filters on the same active report; results sort by latest matching report then discussion ID descending. Page defaults to 1 with size 20; invalid/non-positive page returns a local DERIVED 422. `Discussion.title` is a normalized content snippet capped at 120 characters and `comments` is empty for this queue summary. Focused tests: 15. Migration 014 is a checked-in Study schema candidate only; live schema/deployment and any report-ingest producer are unverified. DD remains Draft.
