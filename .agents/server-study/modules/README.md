# Study Server module index

## Module layout

```text
app/modules/<feature>/
├── models.py   # declarative request/response model classes and data conversion
├── validate.py # input validation and normalization for this API
├── query.py    # optional: SQL statement constants when this API queries a DB
└── view.py     # main API flow, side effects and response orchestration
```

`models.py` contains model class declarations only: fields, types, defaults,
model configuration and data/type conversion. Do not put standalone constants,
helpers, input validation, normalization or business rules there. Runtime input
rules belong in the API's `validate.py`.

An API validator returns normalized model/data when valid and uses only
`return error_response(...)` to return invalid-input errors. It must not raise
an API response, construct an alternate error response, query DB or perform
side effects. Do not use built-in `ValueError` in Study Server source or tests.
A shared pure helper returns `ErrorDetail`, a sentinel or
another typed result that carries validation failure; the API validator/view
maps it through `error_response(...)` at the HTTP boundary. `error_response(errors=...)`
accepts `ErrorDetail` instances and serializes the canonical `meta.fieldErrors`
shape. Errors outside HTTP keep their internal error handling and do not become
`JSONResponse`. Keep schema-only request metadata in route declarations. Do not
apply a rule such as `@gmail.com` unless the current API contract confirms it.

Module-local `validate.py` files contain API-specific request rules where
needed; API #4 uses the shared current-user guard directly and has no
module-local validator. Shared email, blank-value, sort and search helpers live
in `app/utils/validate.py`; Bearer/JWT and token helpers live in
`app/utils/auth.py`. APIs #4, #13 and #14 use `STUDENT`; APIs #46–#67 use
`MENTOR`; API #34 passes both roles then checks purpose. Each calls
`validate_current_user_request(...)` with an explicit accepted-role value rather
than implementing Bearer/JWT checks in module code.

`query.py` is present only when the module needs SQL. It contains SQL statement
string constants only: no functions, classes, helpers, application/DB imports,
parameter preparation or database calls. Put parameter binding and
`query_one`/`query_many` calls in `view.py`. Modules without DB access should not
add an empty `query.py`; API #2 currently dispatches through an email provider
and has no query file.

`view.py` is the primary API flow: it calls validators and query/provider
helpers, performs DB-backed business checks, owns side effects and transaction
boundaries, maps failures, and builds the response. Add a concise Vietnamese
comment for every meaningful operation in each handler and helper, including
validation, external/DB calls, branches, rollback/commit, data mapping and
response construction. One comment may cover consecutive statements in one
cohesive operation; simple variable assignments do not need separate comments.
API-facing functions keep a short API header comment immediately before the
function; internal helpers do not. Comments explain the purpose of the step and
describe current source behavior when a DD differs.

The router remains thin and delegates the API flow to `view.py`.

## Current modules

| Module | Status | Context |
|---|---|---|
| `guest/api_01_auth_register` | `SOURCE_BACKED` | `register-account.md` |
| `guest/api_03_auth_login` | `SOURCE_BACKED` | Login and refresh-token flow in current source |
| `guest/api_04_users_me` | `SOURCE_BACKED` | API #4 current Student profile read flow |
| `guest/api_12_resources_detail` | `SOURCE_BACKED` | API #12 public resource metadata read with published-parent check; response returns stored URL |
| `guest/api_13_users_me_avatar` | `SOURCE_BACKED` | Student JSON Data URL upload through injectable S3-compatible storage; no DB access |
| `guest/api_14_users_me_profile` | `SOURCE_BACKED` | Student profile update; reuses `validate_current_user_request(..., role="STUDENT")` from `app/utils/auth.py` |
| `guest/api_05_categories` | `SOURCE_BACKED` | API #5 public active-category read flow |
| `guest/api_02_auth_verify_email_send` | `SOURCE_BACKED` | API #2 public verification dispatch through injectable stub provider |
| `guest/api_06_courses` | `SOURCE_BACKED` | API #6 public course list with pagination |
| `guest/api_07_courses_search` | `SOURCE_BACKED` | API #7 public course search with pagination |
| `guest/api_08_courses_detail` | `SOURCE_BACKED` | API #08 public published-course detail; composition and HTTP tests pass in the current full suite |
| `guest/api_09_courses_curriculum` | `SOURCE_BACKED` | API #09 public published-course curriculum; composition and HTTP tests pass in the current full suite |
| `mentor/api_46_mentor_courses` | `SOURCE_BACKED` | API #46 Mentor-owned course list with optional status and pagination; numeric `sub`/`MENTOR` authorization |
| `mentor/api_47_mentor_lectures_create` | `SOURCE_BACKED` | API #47 Mentor direct-owner lecture creation; validates ordered uploads metadata, stores content as decimal text and inserts `PUBLISHED` lesson |
| `mentor/api_48_mentor_lecture_detail` | `SOURCE_BACKED` | API #48 Mentor direct-owner lecture read; resolves ordered assets from `lesson_uploads` and `uploads`, preserves nullable content, and uses catalog errors |
| `mentor/api_49_mentor_content_list` | `SOURCE_BACKED` | API #49 Mentor direct-owner content list; reads active `contents` rows, preserves hierarchy with `parent_id`, validates tree integrity and uses catalog errors |
| `mentor/api_50_mentor_content_create` | `SOURCE_BACKED` | API #50 Mentor direct-owner Content create; locks course, assigns derived root status/order defaults, inserts JSONB payload and owns the transaction |
| `mentor/api_51_mentor_content_update` | `SOURCE_BACKED` | API #51 Mentor direct-owner Content update; locks Content/Course, inserts pre-update history snapshot and updates current Content atomically; body/version/status are DERIVED |
| `mentor/api_52_mentor_content_publish` | `SOURCE_BACKED` | API #52 Mentor Content publication-status mutation; locks Content/Course and updates status only; request body, transition/readiness rules and direct-owner mapping are DERIVED |
| `mentor/api_53_mentor_content_delete` | `SOURCE_BACKED` | API #53 Mentor Content soft-delete; locks Content/Course, checks active direct children, rejects PUBLISHED under a DERIVED guard, writes local `contents.deleted_at` and returns DeleteResult |
| `mentor/api_54_mentor_submissions_list` | `SOURCE_BACKED_WITH_DERIVED_PROJECTIONS` | API #54 paged Mentor-owned submissions; direct course owner scope, fixed page size 20, and constrained UploadAsset URL match; live assignment/upload relation unverified |
| `mentor/api_55_mentor_submissions_detail` | `SOURCE_BACKED_WITH_DERIVED_PROJECTIONS` | API #55 single Submission detail; direct course owner, signed-int64 raw-path parser, LEFT JOIN integrity checks, and constrained UploadAsset URL match; rubric relation and live schema unverified |
| mentor/api_56_mentor_submissions_grade | SOURCE_BACKED_WITH_DERIVED_PROJECTIONS | API #56 score/status mutation; row lock, direct course owner, DERIVED score range, feedback preserved, rubric input not persisted; live schema unverified |
| mentor/api_57_mentor_submissions_feedback | SOURCE_BACKED_WITH_DERIVED_PROJECTIONS | API #57 feedback mutation; row lock, direct course owner, feedback-only update, opaque attachments not persisted, constrained student-file lookup; live schema unverified |
| `mentor/api_58_mentor_support_requests` | `SOURCE_BACKED_WITH_DERIVED_PROJECTIONS` | API #58 read-only collection with full thread; direct course owner; legacy BIGINT support tables, no-pagination shape and attachment links are DERIVED; live schema unverified |
| `mentor/api_59_mentor_support_request_detail` | `SOURCE_BACKED_WITH_DERIVED_PROJECTIONS` | API #59 read-only request detail with full thread; reuses #58 models; direct course owner; detail projection and support schema are DERIVED; live schema unverified |
| `mentor/api_60_mentor_support_reply` | `SOURCE_BACKED_WITH_DERIVED_PROJECTIONS` | API #60 Mentor reply; row lock, scoped attachments, ordered message links, shared thread projection and caller-owned transaction; local support schema is DERIVED |
| `mentor/api_61_mentor_support_resolve` | `SOURCE_BACKED_WITH_DERIVED_PROJECTIONS` | API #61 Mentor resolve; row lock, direct course owner, active-state transition, idempotent retry, shared thread projection and caller-owned transaction; lifecycle/schema are DERIVED |
| `mentor/api_62_mentor_course_students` | `SOURCE_BACKED_WITH_DERIVED_CONTRACT` | API #62 read-only Student recipient roster; direct course owner, ACTIVE enrollment + STUDENT role, distinct UserSummary[]; response/schema/access choices remain DERIVED |
| `mentor/api_63_mentor_notifications_create` | `SOURCE_BACKED_WITH_DERIVED_SCHEMA` | API #63 accepts a Mentor notification batch, checks common owned-course roster, atomically inserts notifications and QUEUED delivery outbox; CSV/body mapping and local outbox are DERIVED |
| `mentor/api_64_mentor_notification_status` | `SOURCE_BACKED_WITH_DERIVED_SCHEMA` | API #64 reads notification delivery status, checks sender against Mentor JWT, and maps the local #63 notification/outbox rows into Operation; ownership and aggregation policy are DERIVED |
| `mentor/api_65_mentor_course_progress` | `SOURCE_BACKED_WITH_DERIVED_CONTRACT` | API #65 read-only course progress roster; direct course owner, ACTIVE Student roster, PUBLISHED lesson denominator, latest progress row/floor average and unbounded page are DERIVED; catalog still declares Page<Course> |
| `mentor/api_66_mentor_course_analytics` | `SOURCE_BACKED_WITH_DERIVED_CONTRACT` | API #66 read-only course activity summary; direct owner and PUBLISHED lesson scope, tracked Student/lesson pairs from last_accessed_at, distinct Student count and latest timestamp are DERIVED proxies; not event history; catalog still declares Page<Course> |
| `mentor/api_67_mentor_student_progress` | `SOURCE_BACKED_WITH_DERIVED_CONTRACT` | API #67 read-only selected Student detail; direct owner + ACTIVE Student roster, PUBLISHED lesson detail, deterministic latest progress and #65-compatible summary are DERIVED; diagram/catalog still declare Page<Course> |
| `admin/api_68_admin_users_list` | `SOURCE_BACKED_WITH_DERIVED_CONTRACT` | API #68 Admin user list; shared ADMIN guard, legacy `users` candidate, safe API #04 profile, fixed page/filter rules DERIVED; catalog/diagram now use Page<UserProfile>; live schema/policy unverified |
| `admin/api_69_admin_user_detail` | `SOURCE_BACKED_WITH_DERIVED_CONTRACT` | API #69 read-only Admin user detail; shared ADMIN guard, signed-int64 path, safe legacy `users` projection and 404 invalid/no-row mapping; source/policy remain unverified |
| `admin/api_70_admin_user_update` | `SOURCE_BACKED_WITH_DERIVED_CONTRACT` | API #70 Admin profile/role update; shared ADMIN guard, strict DERIVED replacement body, signed-int64 path, safe legacy `users` UPDATE/projection and caller-owned transaction; live schema/policy unverified |
| `admin/api_71_admin_user_status` | `SOURCE_BACKED_WITH_DERIVED_CONTRACT` | API #71 Admin status transition; shared ADMIN guard, strict DERIVED ACTIVE/SUSPENDED body, locked legacy `users` update, conditional refresh-token revoke and safe profile projection; live schema/policy unverified |
| `admin/api_72_admin_user_delete` | `SOURCE_BACKED_WITH_DERIVED_CONTRACT` | API #72 Admin soft-delete; shared ADMIN guard, conditional legacy `users.status='DELETED'` update, response timestamp aliases `updated_at`, linked rows preserved; policy/schema approval unverified |
| `admin/api_73_admin_courses_list` | `SOURCE_BACKED_WITH_DERIVED_CONTRACT` | API #73 read-only Admin course list; shared ADMIN guard, legacy `courses/users` candidate, status/mentor filters, fixed page/order and shared Course mapping; category 422 fallback and permission/pagination/schema choices remain DERIVED |
| `admin/api_91_admin_quizzes_statistics` | `SOURCE_BACKED_WITH_DERIVED_CONTRACT` | API #91 read-only Quiz attempt aggregate; shared ADMIN guard and legacy BIGINT candidate; QuizStatistics DTO, metric and invalid-path rules remain DERIVED against direct ApiEnvelope<Quiz> |
| `admin/api_92_admin_notifications_list` | `SOURCE_BACKED_WITH_DERIVED_CONTRACT` | API #92 Admin notification list; shared ADMIN guard and legacy BIGINT notifications/outbox candidate; Page cardinality, delivery status projection, filters and visibility remain DERIVED |
| `admin/api_93_admin_notifications_create` | `SOURCE_BACKED_WITH_DERIVED_CONTRACT` | API #93 Admin notification create/send; shared ADMIN guard, explicit recipients, legacy BIGINT notifications/outbox candidates and atomic batch; audience/channel/validation/response metadata/operation bridge remain DERIVED |
| `admin/api_94_admin_notifications_update` | `SOURCE_BACKED_WITH_DERIVED_CONTRACT` | API #94 Admin notification update; shared ADMIN guard, title/content-only legacy candidate update, locked QUEUED outbox eligibility and Notification projection are DERIVED; live schema and fine-grained permission unverified |
| `admin/api_95_admin_notifications_delete` | `SOURCE_BACKED_WITH_DERIVED_CONTRACT` | API #95 Admin notification delete; shared ADMIN guard, queued-only legacy candidate deletion and DeleteResult timestamp mapping are DERIVED; live schema/cascade and provider cancellation unverified |
| `admin/api_96_admin_notifications_status` | `SOURCE_BACKED_WITH_DERIVED_CONTRACT` | API #96 Admin notification status; shared ADMIN guard, legacy BIGINT notification/outbox aggregate and status precedence are DERIVED; live schema/retry grain unverified |
| `admin/api_97_admin_discussions_reported` | `SOURCE_BACKED_WITH_DERIVED_CONTRACT` | API #97 read-only Admin report queue; shared ADMIN guard and Study-local `discussion_reports` BIGINT candidate; queue grain, filters, Page, title/comments and invalid-page 422 are DERIVED; live schema and report ingestion unverified |
| `student/api_34_uploads` | `SOURCE_BACKED` | API #34 multipart Student/Mentor upload; purpose-bound role/course checks, S3-compatible UUID object key and legacy BIGINT `uploads` metadata transaction |

API #34 uses the shared auth guard with accepted roles `STUDENT` and `MENTOR`,
then validates Student→`SUBMISSION` and Mentor→`LECTURE`. A supplied Student
course requires ACTIVE enrollment; Mentor LECTURE requires direct
`courses.mentor_id` ownership. The route uses a separate injectable Object
Storage provider. Its migration is not evidence of a live DB update.

API #47 uses the shared `MENTOR` guard, requires direct `courses.mentor_id`
ownership regardless of course status, resolves only same-owner `LECTURE`
uploads for the path course, and writes a `PUBLISHED` `lessons` row. Its source
targets the checked-in legacy BIGINT schema; it inserts ordered `lesson_uploads`
rows in the same transaction when refs are present. Live schema/migration 005
remains unverified.

API #48 uses the same Mentor guard and direct-owner predicate, then reads the
lesson and parent course and resolves linked uploads in `asset_position` order.
It returns stored status without a publish filter, JSON null for SQL NULL
content, and `assets: []` when no links exist. Focused HTTP tests use fake DB
queries; assigned-course access and live schema are not verified.

API #49 uses the same Mentor guard and direct-owner predicate, then reads local legacy `contents` rows with `deleted_at IS NULL` and no status filter. It returns a flat ordered `Content[]` and rejects malformed tree projections. Focused TestClient cases use fake DB queries; migration 006/live schema and assigned-course access are not verified.

API #50 uses the same guard and direct-owner predicate, then locks the course
row, allocates order among active roots and inserts a `PENDING_REVIEW` root
Content row. The initial status, root placement and order rule are DERIVED from
AC-33/request shape; focused tests use fake DB queries, so migration
006/live-schema state is not verified.

Shared course catalog boundary:
`guest/_shared/course_catalog` contains only response models and pure helpers
used by APIs #6–#8.
| Other Study domain modules | `NOT_FOUND`/`UNWIRED` except individually indexed APIs through #97 | Require source/contract before implementation |


## API #51 Mentor Content update

- `app/modules/mentor/api_51_mentor_content_update` is composed at `PUT /api/v1/mentor/content/{content_id}` and is registered for design-contract middleware error mapping.
- The route exposes signed int64 path metadata and a strict full-replacement body `content_type`, `title`, `payload`; body fields are DERIVED from API #50 because catalog/diagram omit them.
- The view authenticates `MENTOR`, locks the active Content and Course, checks direct owner, archives the pre-update row into `content_versions`, updates current editable fields and sets `PENDING_REVIEW`; one caller-owned transaction commits both mutations.
- Response reuses API #49 `ContentResponse`. Focused tests use fake DB; migration 007 is not live evidence. Original author, public published-version serving and API #52/AC-33 integration remain unresolved.

## API #52 Mentor Content publish/unpublish

- `app/modules/mentor/api_52_mentor_content_publish` composes `PATCH /api/v1/mentor/content/{content_id}/publish` with strict int64 path metadata and a strict `{published: boolean}` body. The body is DERIVED because catalog/AC-22 omit it.
- The view uses the shared `MENTOR` guard, locks the active Content and owning Course, applies direct-owner access, changes only `contents.status`, and commits after validating the shared Content response. Only APPROVED→PUBLISHED and PUBLISHED→APPROVED are implemented; APPROVED is the limited status readiness gate and same-target requests are no-ops.
- Focused HTTP tests use fake DB. Transition/readiness/request semantics remain DERIVED; live schema/deployment, AC-33 approval behavior and revision selection are unverified/open.

## API #53 Mentor Content delete

- `app/modules/mentor/api_53_mentor_content_delete` composes `DELETE /api/v1/mentor/content/{content_id}` and returns `DeleteResult(id, status="deleted", deleted_at)` without a request body or query.
- The view uses the shared `MENTOR` guard, locks active Content and its owning Course, checks direct-owner access, blocks active direct children and PUBLISHED status under DERIVED guards, then sets `contents.deleted_at = CURRENT_TIMESTAMP` and commits after validating `RETURNING` data.
- API #50 also locks the Course before current Content creation; the shared Course lock serializes those current operations. Fake-DB HTTP tests do not verify concurrency against live PostgreSQL or live schema. Queue withdrawal, complete dependency rules, repeat-delete and assigned-Mentor policies remain open.

## API #54 Mentor submissions list

- `app/modules/mentor/api_54_mentor_submissions_list` composes `GET /api/v1/mentor/submissions`; it requires explicit `MENTOR` role and direct `courses.mentor_id` ownership.
- The response uses a fixed page size of 20 and stable `submitted_at DESC, id DESC` ordering. Candidate `assignment_submissions.file_url` is resolved against API #34 upload metadata by URL, Student owner, SUBMISSION purpose and course. This relationship is DERIVED; no FK or live DB inspection proves it.
- Focused tests exercise the HTTP route with fake database results. API #55 detail and APIs #56/#57 mutations remain separate; the 409 error has no current trigger.

## API #55 Mentor submission detail

- `app/modules/mentor/api_55_mentor_submissions_detail` composes `GET /api/v1/mentor/submissions/{submission_id}` and returns the reusable `SubmissionResponse` from API #54 inside `ApiEnvelope<Submission>`.
- The view authenticates `MENTOR`, parses raw signed-int64 path input (malformed/out-of-range → 404), reads the candidate submission with LEFT JOINs to assignments/courses, returns 500 for broken required relation projections, and returns 403 for a different direct course owner under a DERIVED policy.
- It resolves zero or one UploadAsset by the same exact URL, owner, `SUBMISSION` purpose and course fallback as API #54. It does not query or return rubric because the response schema has no rubric field and legacy assignment tables have no approved relation to the V1-PILOT rubric model.
- Focused tests use fake DB results and verify the HTTP contract/read-only behavior; live schema, API #35 URL compatibility, assigned-Mentor access and rubric remain unresolved.

## API #56 Mentor submission grade

- The API #56 view authenticates MENTOR, locks one submission, checks direct course ownership, applies the DERIVED score range, updates only score/status and preserves feedback.
- It accepts required opaque rubric_items under a DERIVED key but does not persist it because no supported target exists in the checked-in legacy model.
- It validates the reusable Submission projection and constrained UploadAsset mapping before commit; failures roll back. Focused fake-DB HTTP tests do not verify live schema or deployment.

## API #57 Mentor submission feedback

- `app/modules/mentor/api_57_mentor_submissions_feedback` composes `POST /api/v1/mentor/submissions/{submission_id}/feedback` and returns the reusable API #54 `SubmissionResponse` inside `ApiEnvelope<Submission>`.
- The view authenticates MENTOR before DB access, parses signed-int64 path input (malformed/overflow → 422), locks the candidate row, checks direct course ownership, and repeats the owner predicate while updating only `assignment_submissions.feedback`.
- `feedback_text` is a DERIVED wire key from catalog descriptor `feedback text`; `attachments` is required and accepted as an opaque string but is not persisted or echoed because no target/format is supported. Score/status remain unchanged; direct calls do not require GRADED.
- The view resolves zero or one student UploadAsset by exact URL, owner, SUBMISSION purpose and course, validates the projection before commit, and rolls back failures. Focused fake-DB tests do not verify live schema/deployment; overwrite, owner mapping and wire-key decisions remain DERIVED pending approval.

## API #58 Mentor support requests

- `app/modules/mentor/api_58_mentor_support_requests` composes `GET /api/v1/mentor/support/requests` and returns `ApiEnvelope<SupportRequest[]>` with full message threads.
- The view authenticates MENTOR before DB access, checks a supplied course against direct `courses.mentor_id` ownership, and repeats that predicate in list and message queries. `course_id` and exact `status` filters combine with AND; there is no pagination, and empty results return `[]`.
- The DD, legacy BIGINT DDL/migration 008, and local HTTP tests document a DERIVED fallback for support tables, lifecycle values, collection shape, and message-upload links. Uploads are constrained by author, course, role-purpose and `UPLOADED` status. Tests use fake DB results; live schema and migration deployment remain unverified.


## API #59 Mentor support-request detail

- `app/modules/mentor/api_59_mentor_support_request_detail` composes `GET /api/v1/mentor/support/{request_id}` and returns one API #58 `SupportRequestResponse` inside `ApiEnvelope<SupportRequest>`.
- The view authenticates MENTOR, parses signed-int64 path text, validates request/course/student relations, distinguishes missing 404 from other-owner 403, and repeats direct owner scope while loading the full thread.
- Messages are chronological, assets follow `asset_position`, and upload metadata is constrained by author, course, role-appropriate purpose and `UPLOADED` status. Empty threads return `[]`; a broken linked asset fails safely.
- The support schema/projection are DERIVED from API #58 migration 008. Focused HTTP tests use fake DB results; live schema, migration deployment and endpoint behavior remain unverified.


## API #60 Mentor support reply

- `mentor/api_60_mentor_support_reply` composes `POST /api/v1/mentor/support/{request_id}/reply`, uses the shared MENTOR guard and writes one support message plus optional ordered upload links in one caller-owned transaction.
- `mentor/_shared/support_request_projection.py` contains the pure SupportRequest/thread mapper used by both APIs #59 and #60.
- The local fallback uses migration 008 and API #34 `uploads`; JSON-array `attachment_refs`, direct `courses.mentor_id` scope, blank-message validation and no status gate are DERIVED.
- Focused HTTP tests use fake DB data. Live schema, migration deployment, concurrency and post-resolve policy remain unverified/open.

## API #61 Mentor support resolve

- `mentor/api_61_mentor_support_resolve` composes `PATCH /api/v1/mentor/support/{request_id}/resolve` and returns one API #58 `SupportRequestResponse` in `ApiEnvelope<SupportRequest>`.
- It authenticates Mentor before DB access, parses signed-int64 path text, locks the request, distinguishes missing 404 from other-owner 403, and conditionally updates an active request under a repeated direct owner predicate.
- OPEN, IN_PROGRESS and WAITING_LEARNER transition to RESOLVED; RESOLVED retries preserve the existing nullable timestamp; CANCELLED/unsupported state returns 422. The transition matrix is DERIVED from migration 008 and AC-24.
- It reloads the full API #59 thread through the shared mapper and commits only after response validation. Focused HTTP tests use fake DB rows; live schema and migration deployment remain unverified.

## API #62 Mentor course students

- `mentor/api_62_mentor_course_students` composes `GET /api/v1/mentor/courses/{course_id}/students` and returns a plain `UserSummary[]` without PageMeta.
- It authenticates `MENTOR`, parses signed-int64 path text, checks `courses.mentor_id`, then reads distinct Student users through legacy `ACTIVE` enrollments ordered by user ID.
- Catalog/diagram initially declared `Page<Course>` despite the AC-25 recipient flow and no pagination inputs; the array contract, legacy schema choice and direct-owner policy are DERIVED and documented in API #62 DD.
- Focused TestClient tests verify local route/error/OpenAPI behavior with fake DB rows. Live schema/deployment remains unverified.

## API #63 Mentor notifications

- `mentor/api_63_mentor_notifications_create` composes `POST /api/v1/mentor/notifications` with strict direct fields `recipients:string`, `title:string`, `content:int64`, and `channels:string`, returning HTTP 202 `ApiEnvelope<Operation>`.
- The view authenticates MENTOR, parses positive Student IDs and allowed channels from CSV, requires a common ACTIVE roster in a directly owned course, inserts per-recipient Notification rows and per-channel `QUEUED` delivery rows, then commits once. Operation UUID and `meta.notification_ids` represent the batch/handoff.
- CSV encoding, common-course policy, int64-to-text content conversion, local legacy schema and outbox are DERIVED fallbacks documented in DD #63. Focused tests use fake DB rows; no live schema/deployment or worker/provider delivery is verified.

## API #64 Mentor notification status

- `mentor/api_64_mentor_notification_status` composes the read-only GET status route. It uses the MENTOR guard, parses a raw int64 notification ID, checks the persisted sender against JWT `sub`, aggregates delivery rows, and returns `ApiEnvelope<Operation>`.
- Local mapping uses API #63's `operation_id`, `sender_id`, `created_at` and outbox statuses/timestamps. Any queued channel maps to `QUEUED`; otherwise any failed channel maps to `FAILED`; all sent maps to `SENT`. These choices are DERIVED and DD #64 remains Draft.
- Focused tests cover auth, ownership, malformed/missing path/resource, count/projection integrity, safe DB errors, trace, no commit, and OpenAPI. Fake DB tests do not verify live schema, migration deployment, or provider delivery.

## API #65 Mentor course progress

- `mentor/api_65_mentor_course_progress` composes `GET /api/v1/mentor/courses/{course_id}/progress` with a local `Page<MentorStudentProgress>` response. It uses raw signed-int64 path/header input and the shared MENTOR guard.
- The view checks direct course ownership, then returns distinct ACTIVE Student enrollments with published-lesson progress. Duplicate progress rows select the latest timestamp then ID; completed count and floor-average percent are DERIVED.
- The request has no pagination inputs; the implementation returns one full roster page. Catalog `Page<Course>` remains the direct contract and conflicts with the local AC-26 shape. DD #65 stays Draft; local schema and business rules are not approved/live-verified.
- Focused tests cover auth, owner/missing paths, aggregation/formula, empty roster/denominator, invalid DB projections, read-only behavior, trace and OpenAPI. Fake DB rows do not verify PostgreSQL or deployment.

## API #66 Mentor course activity analytics

- `mentor/api_66_mentor_course_analytics` composes `GET /api/v1/mentor/courses/{course_id}/analytics`, uses raw signed-int64 path/header input and the shared MENTOR guard.
- The view checks direct course ownership, then counts distinct Student/lesson pairs with a non-null last-access timestamp on PUBLISHED lessons. It returns pair count, distinct Student count and latest known timestamp; it does not claim historical event counts.
- No learner event ledger exists in reviewed legacy/V1-PILOT DDL. This current-state proxy and summary response are DERIVED; diagram/catalog still say `Page<Course>`. DD stays Draft; live schema/deployment is unverified.

## API #67 Mentor Student progress

- `mentor/api_67_mentor_student_progress` composes `GET /api/v1/mentor/courses/{course_id}/students/{student_id}/progress` with a singular lesson-level progress response for AC-26. It uses raw signed-int64 paths and the shared MENTOR guard.
- The view checks direct course ownership, requires an ACTIVE enrollment and STUDENT role, then reads PUBLISHED lessons ordered by `sort_order,id`. Duplicate progress selects latest `last_accessed_at DESC NULLS LAST, id DESC`; absent progress maps to NOT_STARTED/0; summary uses #65's completed count and floor-average rule.
- Singular response, access/roster policy, legacy schema, missing-row handling and formula are DERIVED; diagram/catalog still declare `Page<Course>`. DD remains Draft. Focused HTTP tests use fake DB rows and do not verify live schema/deployment.


## API #68 Admin user list

- `admin/api_68_admin_users_list` composes `GET /api/v1/admin/users`; it authenticates the shared ADMIN JWT role before any user query.
- SQL constants in `query.py` apply identical optional exact role/status and literal case-insensitive keyword predicates to COUNT and page reads. The view orders by `users.id ASC`, fixes page size at 20 and reuses the API #04 safe `UserProfile` projection. It never selects `password_hash`; unsupported `bio` is omitted.
- `ApiEnvelope<Page<UserProfile>>`, page defaults/range, filter normalization and id ordering are DERIVED and synchronized in the API catalog/AC-31 node. Focused HTTP tests use fake DB sessions. The DD remains Draft; live schema, Admin permission policy, PII/audit and lifecycle visibility are unverified.


## API #69 Admin user detail

- `admin/api_69_admin_user_detail` composes `GET /api/v1/admin/users/{user_id}`. The route passes raw path/header values; the shared ADMIN guard runs before signed-int64 parsing or DB access.
- `query.py` contains one bound SELECT over the legacy `users` candidate and only selects API #04 safe profile fields. `view.py` owns lookup, projection validation and response; no row or invalid/out-of-int64 path returns catalog 404, query/mapping failure returns safe 500 with rollback.
- Response reuses API #04 `UserProfile`, preserves nullable avatar/phone as null and omits unsupported bio and credentials. Guard mapping and path fallback are DERIVED; fake-session tests do not establish live schema or deployment.

## API #70 Admin user update

- `admin/api_70_admin_user_update` composes `PUT /api/v1/admin/users/{user_id}`. The shared ADMIN guard runs before raw signed-int64 path/body checks and DB access.
- The strict replacement body and role allowlist are DERIVED because direct catalog/diagram sources omit the body. Profile normalization follows API #14; no status, delete, audit or token side effect is added.
- `query.py` holds one bound UPDATE against the legacy BIGINT `users` candidate; `view.py` validates only the safe API #04 profile projection, commits on success and rolls back failures. Invalid ID is 422, no row is 404.
- Focused tests use fake DB sessions. Live schema, Admin authorization policy, role-transition policy and access-token invalidation are unverified; DD stays Draft.

## API #71 Admin user status

- `admin/api_71_admin_user_status` composes `PATCH /api/v1/admin/users/{user_id}/status`. The shared ADMIN guard precedes raw signed-int64 parsing and database access.
- The strict `{status}` body and ACTIVE/SUSPENDED allowlist are DERIVED because the direct catalog/diagram omit the body. The view locks the current legacy `users` status, rejects states outside ACTIVE/SUSPENDED, updates the row, and revokes eligible refresh tokens when suspending.
- `query.py` contains SQL constants only. `view.py` owns projection, side effects and commit/rollback; errors use catalog codes and successful data uses API #04 `UserProfile`.
- The focused suite has 21 passing HTTP tests. Fake DB sessions do not verify live schema/deployment or authorization policy; the DD remains Draft.


## API #72 Admin user delete

- `admin/api_72_admin_user_delete` composes `DELETE /api/v1/admin/users/{user_id}` on the existing Admin detail path template. It authenticates ADMIN before signed-int64 parsing and DB access.
- `query.py` holds one conditional UPDATE for the legacy BIGINT `users` candidate; `view.py` validates the returned id/timestamp, maps missing or already-DELETED rows to 404, commits after response validation and rolls back failures.
- `DeleteResult.deleted_at` is returned from `updated_at`; there is no dedicated deletion timestamp or migration. Dependent records are retained. Status marker, timestamp alias and retry behavior are DERIVED; fake-session tests do not prove live schema/deployment or policy approval.

## API #73 Admin course list

- `admin/api_73_admin_courses_list` composes `GET /api/v1/admin/courses` with a typed Page<Course> envelope. The route passes raw query strings; shared ADMIN auth precedes parsing and DB access.
- `query.py` holds count/page SQL constants over legacy `courses LEFT JOIN users`, with identical optional status/mentor predicates, missing-mentor count and stable `c.id ASC`; `view.py` maps decimal price through the shared Course mapper and never commits.
- Valid category IDs return 422 before DB because no physical relation is available. This reuses API #06's unsupported-category precedent as a DERIVED fallback; the catalog's filter is not yet implemented. Page size/order, ADMIN-to-permission mapping and missing-mentor policy are also DERIVED.
- Focused API #73 tests: 24 passed. Linked #06/#68/#73 regression: 60 passed; full Study suite: 830 passed. Fake DB tests do not verify live schema/deployment; DD stays Draft.


## API #74 Admin course detail

- `admin/api_74_admin_course_detail` composes read-only `GET /api/v1/admin/courses/{course_id}` with shared `ADMIN` JWT auth before raw signed-int64 parsing and DB access.
- The SQL constant reads one legacy candidate course and mentor; the view maps through shared `Course`, wraps one item in `CoursePage`, and never commits. Invalid/missing IDs return 404; mapping/query failures return safe 500 with rollback.
- At the API #74 checkpoint: focused tests 15 passed; linked #06/#08/#69/#73 regression 80 passed; full suite 845 passed; Ruff passed. API #76 checkpoint was 890 tests; API #77 is current at 910 tests. Fake DB tests do not verify live schema/deployment or dedicated permission; counters remain undefined and DD stays Draft.

## API #75 Admin course update

- `admin/api_75_admin_course_update` composes `PUT /api/v1/admin/courses/{course_id}` on the existing #74 detail path template. The shared `ADMIN` guard precedes raw path/body validation and mutation.
- `models.py` declares a strict full-replacement candidate body; `query.py` contains only the bound metadata UPDATE SQL constant; `validate.py` applies signed-int64, title-length and exact decimal candidate checks; `view.py` owns UPDATE, #74 Course projection readback, response mapping and transaction.
- Only metadata plus `updated_at` are changed; status, mentor, category, counters and audit remain outside #75. The body, numeric limits, legacy schema target and singleton Page are DERIVED. Focused tests: 27 passed; linked regression: 113 passed; full suite: 872 passed. Fake DB tests do not prove live schema/deployment or dedicated permission; DD stays Draft.

## API #76 Admin course status

- `admin/api_76_admin_course_status` composes `PATCH /api/v1/admin/courses/{course_id}/status`; body `{status}` and uppercase DRAFT/PUBLISHED/SUSPENDED are strict DERIVED fallbacks because catalog/diagram omit the body and the reusable enum members.
- `query.py` contains row-lock, status-update and audit-insert SQL constants; `view.py` owns the transaction, shared Course projection, singleton Page and rollback. A changed target updates status/timestamp and writes course/actor/old/new audit data atomically; an identical target is a no-op.
- Migration 010 and legacy DDL add a minimal BIGINT audit relation matching current legacy IDs; it is not live-schema proof. Shared ADMIN role does not establish the finer AC-32 course-management permission. Focused tests use fake DB rows; DD remains Draft.

## API #77 Admin course delete

- `admin/api_77_admin_course_delete` composes `DELETE /api/v1/admin/courses/{course_id}` with no body or query. The shared ADMIN guard precedes signed-int64 parsing and DB access.
- `query.py` contains lock, dependency EXISTS and soft-delete SQL constants only; `view.py` owns the transaction and rollback. It blocks any enrollment and active generic Content/lesson/quiz/assignment row, then sets `courses.status='DELETED'` and `updated_at`; the response maps that DB timestamp to `DeleteResult.deleted_at`.
- Dependency set, marker, timestamp alias and repeat-delete 404 are DERIVED from catalog plus API #72/checked-in legacy candidates. No migration/audit/cascade is added. Focused tests: 20 passed; full suite: 910 passed. Fake sessions do not prove live schema/deployment; DD remains Draft.

## API #78 Admin pending Content queue

- `admin/api_78_admin_content_pending` composes read-only `GET /api/v1/admin/content/pending`. Shared ADMIN authentication runs before raw query parsing and DB access.
- `query.py` contains count/list SQL constants against active `contents` rows with `PENDING_REVIEW`; `view.py` applies matching exact filters, maps through API #49 `ContentResponse`, and returns `Page<Content>` without committing.
- Page cardinality, 1-based page default, fixed size 20, `id ASC`, exact filter semantics and soft-delete exclusion are DERIVED because catalog/diagram declare a singular Content response and omit those rules. The DD remains Draft; fake DB tests do not verify live schema/deployment or moderation permission.
- Focused tests: 23 passed; linked #49–#53/#73/#78 regression: 160 passed; full suite: 933 passed; Ruff and OpenAPI checks pass.

## API #79 Admin Content detail
- `admin/api_79_admin_content_detail` composes read-only `GET /api/v1/admin/content/{content_id}` after the fixed #78 queue route and returns one API #49 `ContentResponse` inside `ApiEnvelope<Content>`.

## API #80 Admin Content approval
- `admin/api_80_admin_content_approve` owns `PATCH /api/v1/admin/content/{content_id}/approve`; `query.py` holds only lock/update/audit SQL constants and `view.py` owns the transaction.
- It uses the shared `ADMIN` guard, transitions active `PENDING_REVIEW` Content to `APPROVED`, appends a BIGINT audit candidate and returns the direct Content schema. These state/schema choices are DERIVED; migration/live deployment and the exact revision shown in #79 remain unverified.
- Focused suite: 22 passed; linked #49–#53/#76/#78–#80 regression: 189 passed; full Study suite: 968 passed; Ruff passes.

## API #81 Admin Content rejection
- `admin/api_81_admin_content_reject` owns the required-reason PATCH and reuses API #49 `ContentResponse`; `query.py` contains only lock/update/decision SQL constants, while `view.py` owns the transaction.
- It requires shared `ADMIN`, locks an active `PENDING_REVIEW` row, changes it to `REJECTED`, and writes the reason plus actor/old/new status into one row of migration 011's BIGINT audit candidate. This is a DERIVED physical mapping; no second audit write or response reason field is added.
- Focused suite: 29 passed; linked #49–#53/#78–#81 regression: 200 passed; full Study suite: 997 passed; Ruff passes. Live migration/schema, dedicated permission, empty-reason policy and revision continuity remain unverified; DD stays Draft.
- Shared ADMIN authentication runs before raw signed-int64 path parsing or DB access. `query.py` contains one bound SELECT of the eight reusable Content fields from active `contents`; invalid/missing/deleted IDs return catalog 404 and query/projection failures safely roll back to 500.
- The endpoint does not query version history, infer author, gate on `PENDING_REVIEW`, or mutate/commit. AC-33 version/author intent conflicts with the direct response schema; revision identity and live schema remain unresolved.
- Focused tests: 13 passed; full Study suite: 946 passed; Ruff passes. Fake DB sessions do not verify live schema/deployment or moderation permission; DD remains Draft.

## API #82 Admin lessons list

- `admin/api_82_admin_lessons_list` composes read-only `GET /api/v1/admin/lessons`; models reuse API #09 `Lesson`, `query.py` holds a single SQL constant, `validate.py` calls the shared `ADMIN` guard and handles course/type input, and `view.py` owns query/mapping/error orchestration. List SQL excludes API #86 `status='DELETED'` tombstones.
- The local DERIVED contract returns `Lesson[]`, applies exact optional `course`/`status` filters, uses stable legacy candidate ordering and rejects `type` explicitly with 422. No pagination/count/write is added; live schema and the dedicated AC-34 permission remain unverified.
- Focused tests: 15 passed; full Study suite: 1012 passed; Ruff passes. Fake DB HTTP tests do not verify live DB schema or deployment; the DD remains Draft.

## API #83 Admin lesson detail

- `admin/api_83_admin_lesson_detail` composes read-only `GET /api/v1/admin/lessons/{lesson_id}` and returns one reusable API #09 `Lesson` inside the direct envelope.
- Shared `ADMIN` auth runs before custom signed-int64 path parsing and a single bound SELECT against non-`DELETED` rows in the legacy BIGINT `lessons` candidate. Malformed/missing/tombstoned IDs map to 404; invalid required projections and query errors map to safe 500 with rollback. Dependency output and live schema remain unresolved; fine-grained AC-34 permission is not implemented.
- Focused tests: 15 passed; linked #09/#74/#82 regression: 54 passed; full Study suite: 1027 passed; Ruff passes; OpenAPI: 49 paths / 54 operations. Fake DB tests do not verify deployment; DD remains Draft.

## API #84 Admin lesson update

- `admin/api_84_admin_lesson_update` owns `PUT /api/v1/admin/lessons/{lesson_id}` and shares the #83 route template. `models.py` declares the strict full-replacement DERIVED body; `query.py` contains the one legacy `lessons` UPDATE/RETURNING statement; `validate.py` applies shared ADMIN auth and signed-int64 path validation; `view.py` owns transaction, mapping and response.
- The body fallback updates only title/content/video_url/order plus `updated_at`, only while Lesson is not `DELETED`; course association/status and child dependency rows remain untouched. The view commits only after valid Lesson mapping and rolls back no-row/query/mapping/commit failures.
- Focused tests: 23 passed; linked #09/#47/#48/#82–#84 regression: 104 passed; full Study suite: 1050 passed; Ruff passes. Fake DB tests do not verify live schema/deployment or AC-34 fine-grained permission; DD remains Draft.


## API #85 Admin lesson status

- `admin/api_85_admin_lesson_status` composes `PATCH /api/v1/admin/lessons/{lesson_id}/status`. `models.py` declares strict `{status}` using DERIVED `DRAFT/PUBLISHED/SUSPENDED`; `query.py` contains lock/update/audit SQL only; `validate.py` uses shared ADMIN auth and signed-int64 path parsing; `view.py` owns atomic status/audit, Lesson mapping, commit/rollback and response.
- Migration 012's BIGINT `lesson_status_audit_logs` and same-status no-op policy are DERIVED; V1-PILOT UUID schema is not mixed in. Status lock/update excludes `DELETED` tombstones. Shared ADMIN role works, but AC-34 fine-grained lesson-management permission remains unimplemented/unverified.
- Focused suite: 28 passed. Full Study suite: 1078 passed; Ruff passes; OpenAPI: 50 paths / 57 operations. Live DB/migration deployment is not verified. DD remains Draft.

## API #86 Admin lesson delete

- `admin/api_86_admin_lesson_delete` composes `DELETE /api/v1/admin/lessons/{lesson_id}` on the shared #83/#84 path template with no body. `models.py` declares the catalog `DeleteResult`; `validate.py` runs shared ADMIN auth before signed-int64 path parsing; `query.py` holds lock/dependency/soft-delete SQL constants; `view.py` owns the transaction and response.
- The local DERIVED fallback blocks any `lesson_progress`, `resources`, or `lesson_uploads` reference with catalog 422. Otherwise it sets legacy `lessons.status='DELETED'`, maps returned `updated_at` to `deleted_at` by API #77 precedent, and commits; no child, audit or migration write is added. Repeat delete returns 404.
- Admin #82–#85, Mentor #48 and Resource #12 exclude/reject the tombstone. Focused tests: 15; linked #09/#12/#47/#48/#77/#82–#86 regression: 180; full Study suite: 1093; Ruff passes; OpenAPI: 50 paths / 57 operations. Fake-session tests do not prove live schema/FK behavior or AC-34 fine-grained permission; DD remains Draft.


## API #87 Admin quiz list

- `admin/api_87_admin_quizzes_list` composes read-only `GET /api/v1/admin/quizzes`. `models.py` declares query, metadata, Page and envelope classes; `query.py` contains count/page SQL constants; `validate.py` uses the shared ADMIN guard before parsing raw values; `view.py` owns count/page execution, mapping, rollback and response construction.
- Current fallback uses legacy BIGINT `quizzes`, exact optional filters, `DELETED` exclusion, page 1 / fixed size 20 / `id ASC`, and `ApiEnvelope<Page<Quiz>>`; catalog response is `ApiEnvelope<Quiz>`. Nested `questions` are empty because type/choice schema is unresolved. Fine-grained AC-35 permission and live schema remain unverified.
- At the API #87 checkpoint: 20 focused tests, 93 linked regressions, 1113 full-suite tests and 51 paths / 58 operations. At the API #88 checkpoint, the full suite had 1134 tests and OpenAPI had 51 paths / 59 operations. DD remains Draft — Needs Confirmation.

## API #88 Admin quiz create

- `admin/api_88_admin_quizzes_create` composes `POST /api/v1/admin/quizzes`. `models.py` declares local embedded request and Quiz response projections; `query.py` contains SQL constants for course lookup and Quiz/question/choice inserts; `validate.py` authenticates ADMIN before decoding raw request JSON; `view.py` owns ordered writes, response mapping and transaction commit/rollback.
- Outer body/status/envelope follow the catalog. Embedded JSON, QuestionType candidates, `{id,text,is_correct}` Admin choices, course-check mapping and answer booleans are DERIVED. The Student #28 response must omit the answer key.
- Migration 013 adds local legacy BIGINT `question_type` and `sort_order` candidates; old rows remain nullable/unbackfilled. Focused tests: 21; linked #87/#88 regression: 41; full Study suite: 1134; Ruff passes; OpenAPI: 51 paths / 59 operations. Live migration/schema and fine-grained AC-35 permission remain unverified; DD stays Draft.

## API #89 Admin quiz update

`admin/api_89_admin_quizzes_update/` owns raw-path/body validation, SQL
constants and update orchestration. `query.py` remains SQL-only; `view.py`
authenticates before parsing, locks parent/children, checks attempt/answer
history, updates quiz metadata and performs child-first delete plus ordered
replacement inserts in one transaction. The full Admin Quiz projection is
validated before commit. The request/replacement/history/course/tombstone/lock
policies are DERIVED local choices; shared ADMIN role does not prove a separate
AC-35 permission, and fake sessions do not prove live PostgreSQL behavior.

## API #90 Admin quiz delete

`admin/api_90_admin_quizzes_delete/` owns positive-int64 validation, SQL
constants and ADMIN delete orchestration. The view locks Quiz and child rows,
checks attempts plus linked answers, preserves rows through the soft-delete
branch or removes choices → questions → Quiz when there is no history. It
validates returned ID sets and DeleteResult before commit; query, projection,
mutation and commit failures roll back. The no-history hard delete, answer-only
protection, `DELETED`/`updated_at` mapping and repeat-delete behavior are
DERIVED. Focused tests: 18; linked #86–#90: 100; full Study suite: 1178.
Fake-session tests do not prove live PostgreSQL behavior or API #29 race safety.

## API #91 Admin quiz statistics

`admin/api_91_admin_quizzes_statistics` composes a read-only aggregate route.
`models.py` declares a separate `QuizStatistics` fallback envelope;
`query.py` contains only the aggregate SQL constant; `validate.py` applies the
shared ADMIN guard before positive-int64 path parsing; `view.py` executes the
query and validates counts/nullable decimals before returning a response.
The response and metrics are DERIVED because diagram/catalog `ApiEnvelope<Quiz>`
has no statistics fields. Focused tests: 19; linked #87–#91: 104; full Study
suite: 1197; Ruff passes; OpenAPI: 53 paths / 62 operations. Fake DB rows do
not prove live schema/deployment or fine-grained AC-35 permission; DD remains
Draft.

## API #92 Admin notification list

`admin/api_92_admin_notifications_list` composes a read-only ADMIN list route. The route uses the shared guard before page parsing; SQL constants count and list legacy notification rows with delivery outbox aggregates; the view maps `Page<Notification>`, rollback and 500/503 responses. The list/Page response, fixed page size, delivery status projection and global role scope are DERIVED. Focused tests: 20; linked #63/#64/#87/#92: 85; full Study suite: 1217. Fake DB rows do not prove live schema, migration, worker behavior or owner approval; the DD remains Draft.


## API #93 Admin notification create/send

`admin/api_93_admin_notifications_create` composes `POST /api/v1/admin/notifications`, sharing the `/admin/notifications` path template with API #92. The raw body lets shared ADMIN authentication precede JSON parsing and DB reads. The local fallback verifies explicit IDs exist, writes one legacy notification per recipient with a shared UUID, writes one `QUEUED` delivery row per recipient/channel, and commits after response projection. It returns the first Notification with derived batch metadata. Segment expansion and provider delivery are not wired. Focused tests: 26; linked #63/#64/#87/#92/#93: 111; full suite: 1243; Ruff and OpenAPI pass. Fake DB tests do not verify live schema/deployment or fine-grained permission; DD remains Draft.


## API #94 Admin notification update

`admin/api_94_admin_notifications_update` owns models, SQL constants, raw input validation and transactional view for the PUT route. It reuses API #92's `AdminNotificationResponse`. Only `title/content` are updated on the legacy candidate; delivery rows are locked and must all be QUEUED. The body, editability condition and legacy target grain remain DERIVED; audience/channel/schedule changes and provider calls are not implemented. The 20 focused and 66 linked fake-DB HTTP tests do not prove live schema/deployment or fine-grained permission.


## API #95 Admin notification delete/cancel

`admin/api_95_admin_notifications_delete` owns the raw-path DELETE route, strict signed-int64 validator, SQL-only parent/delivery locks and DELETE RETURNING constants, and transactional view. It uses shared ADMIN auth before path parsing, locks parent before deliveries, and applies a DERIVED rule requiring at least one all-QUEUED delivery. The view deletes exactly one recipient-level legacy BIGINT row; the checked-in FK candidate cascades its outbox rows. It maps the database timestamp to direct DeleteResult and commits after envelope validation. It does not delete sibling rows sharing `operation_id` or call a scheduler/provider. Focused tests: 21; linked #92–#95: 87; full suite: 1284; Ruff check/scoped format pass; OpenAPI: 55 paths / 66 operations. Fake DB tests do not prove live schema, PostgreSQL lock/cascade behavior, deployment, external cancellation or dedicated permission; DD remains Draft.

## API #96 Admin notification status

`admin/api_96_admin_notifications_status` owns the SQL-only aggregate query,
raw signed-int64 parser and read-only view for the GET status route. It reuses
API #92's `AdminNotificationResponse`, validates ordered `EMAIL`/`PUSH`
channels and the local QUEUED/FAILED/SENT projection, and returns no delivery
count fields. Shared ADMIN auth precedes path parsing; invalid ID and absent
notification/delivery status return catalog 404. It never commits or calls a
provider. The physical schema, projection and status-resource 404 semantics
are DERIVED; fine-grained permission and live schema remain unverified.

## API #97 Admin reported-discussion queue

`admin/api_97_admin_discussions_reported` owns the models, shared ADMIN/query
validation, SQL-only count/list constants, and read-only page orchestration.
It returns one Discussion per matching OPEN/IN_REVIEW report group, with
exact-match reason/severity filters on the same report and stable latest-report
ordering. The local `discussion_reports` relation links by BIGINT Discussion
ID. Page 1/size 20, invalid-page 422, normalized content-derived title and
empty comments are DERIVED to satisfy the current response shape. Focused HTTP
tests cover filtering, ordering bindings, auth order, projection and failures;
they use fake DB queries and do not prove migration deployment or report
ingestion.
