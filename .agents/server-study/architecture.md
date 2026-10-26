# Study Server architecture

## Intended composition visible in current source

```text
app/main.py:create_app
  -> app/api/v1.py:router
  -> app/core/config.py
  -> app/core/database.py
  -> app/core/middleware.py
  -> app/core/responses.py
  -> app/core/trace.py
```

Current composition, API #1 register flow, API #2 verify-email dispatch stub,
API #3 login/refresh flow, API #4 current-user flow, API #5 category flow,
API #6 public course flow, API #7 course-search flow, API #08 course detail,
API #09 curriculum, API #12 resource detail, API #13 avatar upload, API #14
profile update, API #34 upload metadata, API #46 Mentor course list, API #47
Mentor lecture create, API #48 Mentor lecture detail, API #49 Mentor content
list, API #50 Mentor content create, API #51 Mentor content update, API #52
Mentor Content publish/unpublish, API #53 Mentor Content delete, APIs #54–#57
cover submissions list/detail/grade/feedback, APIs #58–#61 cover support-request
list/detail/reply/resolve, API #62 reads the course-student roster, and API #63
creates notifications with queued delivery outbox rows, API #64 reads
notification delivery status, API #65 reads course progress, API #66 reads
course activity from legacy progress-state timestamps, and API #67 reads
selected-Student course progress, Admin APIs #68–#94 user/course/content,
lesson, quiz management/statistics and notification list/create/update; all are wired locally.
The current full Study suite result is recorded in `tests.md`; routes
without a current implementation remain unwired.

## Verified ownership

- `app/main.py`: FastAPI composition root, CORS, middleware/exception-handler registration, root/health routes.
- `app/api/v1.py`: declared `/api/v1` routes; exposes health-adjacent utility
  routes, API #1 register, API #2 verification dispatch, API #3 auth, API #4
  current-user profile, API #5 categories, API #6 courses, API #7 course search,
  API #12 resource detail, API #13 avatar upload, API #14 profile update,
  API #34 upload metadata, API #46 Mentor course list, API #47 Mentor lecture
  create, API #48 Mentor lecture detail, API #49 Mentor content list, API #50
  Mentor content create, API #51 update, API #52 publish/unpublish, API #53
  soft-delete, API #54 Mentor submissions list, API #55 Mentor submission detail and API
  #56 Mentor submission grade, API #57 Mentor submission feedback, API #58 Mentor support-request list, API #59 Mentor support-request detail, API #60 Mentor support reply, API #61 Mentor support resolve, API #62 Mentor course-student roster, API #63 Mentor notification dispatch, API #64 notification status, API #65 course progress, API #66 course activity analytics API #67 selected-Student course progress, APIs #68–#91 Admin user/course/Content, lesson and quiz management, and API #92 notification list.
- `app/core/config.py`: typed settings backed by `app/core/constants.py`.
- `app/core/database.py`: sync SQLAlchemy engine/session/query primitives.
- `app/core/middleware.py`: trace middleware and shared FastAPI exception handlers.
- `app/core/security/*`: password, access token, refresh token primitives.
- `app/utils/auth.py`: shared Bearer/JWT parsing and claim checks, role-aware `validate_current_user_request` guard, refresh-token input validation, access/refresh token issuance, expiry metadata and public auth payload mapping. It delegates cryptographic operations to `app/core/security`.
- `app/utils/validate.py`: shared pure input normalization/validation helpers used by API validators, such as email, blank-value, sort and search handling; it does not own Bearer/JWT/token helpers.
- `app/modules/guest/api_03_auth_login/models.py`: login and refresh request contracts.
- `app/modules/guest/api_03_auth_login/query.py`: SQL constants for user lookup and refresh-token persistence.
- `app/modules/guest/api_03_auth_login/view.py`: login credential flow, refresh rotation, transaction and response mapping.
- `app/modules/guest/api_04_users_me/models.py`: safe current-user profile response model.
- `app/modules/guest/api_04_users_me/query.py`: parameterized public profile lookup by user ID.
- `app/modules/guest/api_04_users_me/view.py`: Student role check, profile lookup and canonical response/error mapping.
- `app/modules/guest/api_05_categories/models.py`: API #5 query and public category page model classes.
- `app/modules/guest/api_05_categories/query.py`: parameterized active-category lookup by exact locale.
- `app/modules/guest/api_05_categories/view.py`: default-locale resolution, category mapping and canonical response/error mapping.
- `app/modules/guest/api_06_courses/models.py`: API #6 list query contract.
- `app/modules/guest/api_06_courses/query.py`: parameterized published-course/count queries.
- `app/modules/guest/api_06_courses/view.py`: public course list filtering, mentor-integrity checks and response mapping.
- `app/modules/guest/api_07_courses_search/models.py`: API #7 search query contract.
- `app/modules/guest/api_07_courses_search/query.py`: parameterized published-course search/count queries.
- `app/modules/guest/api_07_courses_search/view.py`: public course search filtering and response mapping.
- `app/modules/guest/api_12_resources_detail/view.py`: public resource metadata retrieval and published-parent check; current response returns the stored resource URL directly.
- `app/modules/guest/api_13_users_me_avatar/models.py`: strict JSON Data URL request and `AvatarUploadResult` response model.
- `app/modules/guest/api_13_users_me_avatar/validate.py`: Student Bearer guard plus strict Base64, MIME/signature and decoded-size validation.
- `app/modules/guest/api_13_users_me_avatar/view.py`: upload orchestration and safe storage-failure mapping without database access.
- `app/service/object_storage/avatar.py`: lazy, injectable S3-compatible avatar provider backed by process environment and public URL base.
- `app/modules/guest/api_14_users_me_profile/view.py`: Student profile update; consumes `avatar_url` submitted in the follow-up request.
- `app/modules/mentor/api_46_mentor_courses/`: API #46 Mentor query, role validation, direct-owner SQL and course-list response orchestration. It requires numeric JWT `sub` with role `MENTOR`; the query scopes `courses.mentor_id` to that subject and optionally filters `DRAFT`/`PUBLISHED`.
- `app/modules/mentor/api_47_mentor_lectures_create/`: API #47 Mentor lecture creation; shared `MENTOR` JWT guard, direct `courses.mentor_id` ownership check without course-status filtering, scoped `uploads` metadata resolution, decimal-string content mapping, `PUBLISHED` insert and caller-owned transaction. Local tests cover the HTTP contract; live DB schema remains unverified.
- `app/modules/mentor/api_48_mentor_lecture_detail/`: API #48 Mentor lecture detail; shared `MENTOR` JWT guard, direct course-owner check, nullable Lecture content mapping, ordered `lesson_uploads`/`uploads` projection and catalog 401/403/404/500 outcomes. Local tests cover the HTTP contract; live DB/migration state remains unverified.
- `app/modules/mentor/api_49_mentor_content_list/`: API #49 Mentor content-tree read; shared `MENTOR` guard, direct `courses.mentor_id` access, legacy `contents` projection, active-row filtering and tree integrity validation. Local DDL/migration and TestClient tests are source evidence; live DB/migration deployment remains unverified.
- `app/modules/mentor/api_50_mentor_content_create/`: API #50 Mentor content creation; shared `MENTOR` guard, direct course ownership, per-course row lock, derived root ordering/status defaults, JSONB payload insert and caller-owned transaction. Focused tests and local DDL are evidence only; live DB/migration deployment remains unverified.
- `app/modules/mentor/api_51_mentor_content_update/`: API #51 direct-owner Content update; locks Content and Course, snapshots the prior row into legacy `content_versions`, updates current `contents` and commits atomically. Body, history schema and `PENDING_REVIEW` transition are DERIVED; tests use fake DB and migration 007/live schema are unverified.
- `app/modules/mentor/api_52_mentor_content_publish/`: API #52 direct-owner Content publication status mutation; locks Content/Course and updates only `contents.status` for DERIVED APPROVED↔PUBLISHED transitions. Target body, readiness gate and live schema/deployment remain unverified; local tests use fake DB.
- `app/modules/mentor/api_53_mentor_content_delete/`: API #53 direct-owner Content soft-delete; locks active Content and Course, checks active direct children, blocks PUBLISHED Content under a DERIVED guard, writes `contents.deleted_at = CURRENT_TIMESTAMP` and returns the catalog `DeleteResult`. Child/PUBLISHED/retry policy remains DERIVED; tests use fake DB and live schema/deployment are unverified.
- `app/modules/mentor/api_54_mentor_submissions_list/`: API #54 read-only page of Mentor-owned submissions; uses explicit MENTOR auth, direct `courses.mentor_id` scope, fixed page size 20, stable submitted-time/ID order, and a DERIVED URL/owner/purpose/course match to API #34 upload metadata. Focused tests use fake DB; assignment/upload relation and live schema remain unverified; 409 is declared without a trigger.
- `app/modules/mentor/api_55_mentor_submissions_detail/`: API #55 read-only Submission detail; uses shared MENTOR auth, raw signed-int64 path parsing, LEFT JOIN parent integrity checks, direct course-owner access, and the same DERIVED URL/owner/purpose/course UploadAsset fallback as API #54. It reuses API #54's `SubmissionResponse` model. AC-23 rubric projection remains a diagram/schema discrepancy; focused tests use fake DB and live schema is unverified.
- `app/modules/mentor/api_56_mentor_submissions_grade/`: API #56 grade mutation; shared MENTOR guard, locked direct-owner submission, DERIVED score bounds, score/status update, preserved feedback and constrained UploadAsset projection. Required rubric_items is not persisted because the checked-in schema has no supported target; fake-DB tests and checked-in DDL do not verify live schema.
- `app/modules/mentor/api_57_mentor_submissions_feedback/`: API #57 feedback mutation; shared MENTOR guard, locked direct-owner submission, feedback-only update, preserved score/status and constrained UploadAsset projection. `feedback_text` is a DERIVED wire key; required `attachments` is accepted opaquely but not persisted because no target is supported. Fake-DB tests and checked-in DDL do not verify live schema.
- `app/modules/mentor/api_58_mentor_support_requests/`: API #58 read-only Mentor support-request collection; shared MENTOR guard, direct `courses.mentor_id` scope, no pagination, AND-combined exact filters, full chronological message threads and constrained linked UploadAsset projection. The legacy BIGINT schema/migration, collection cardinality and support detail projection are DERIVED fallbacks; focused HTTP tests use fake DB rows and do not verify live schema or deployment.
- `app/modules/mentor/api_59_mentor_support_request_detail/`: API #59 read-only Mentor support-request detail; reuses API #58 response models, shared MENTOR auth, raw signed-int64 parsing, direct course-owner check, full ordered thread and constrained UploadAsset projection. The BIGINT support schema and detail policies are DERIVED from API #58; focused tests use fake DB rows and do not verify live schema or deployment.
- `app/modules/student/api_34_uploads/`: API #34 role/purpose validation, ACTIVE-enrollment/direct-owner checks, S3 object upload, legacy `uploads` metadata INSERT and transaction orchestration for Student submissions and Mentor lectures.
- `app/service/object_storage/upload.py`: lazy injectable S3-compatible stream uploader and best-effort delete adapter for API #34; uses the existing Object Storage environment configuration.
- `app/modules/guest/_shared/course_catalog/models.py`: shared course, mentor and pagination response contracts.
- `app/modules/guest/_shared/course_catalog/helpers.py`: shared sort, course mapping and safe error helpers.
- `app/modules/guest/api_02_auth_verify_email_send/models.py`: strict public `user_id` and `email` request contract.
- `app/modules/guest/api_02_auth_verify_email_send/view.py`: provider dispatch orchestration and canonical response/error mapping without DB access.
- `app/service/email/provider.py`: injectable verification-email provider Protocol, result type and development stub.
- `app/modules/guest/api_01_auth_register/models.py`: API #1 register request
  model fields and type conversion.
- `app/modules/guest/api_01_auth_register/validate.py`: active request validator
  for email, password and full name; returns `error_response(...)` for invalid
  input and normalized model data otherwise.
- `app/modules/guest/api_01_auth_register/query.py`: duplicate lookup and users
  insert SQL constants; query execution is owned by `view.py`.
- `app/modules/guest/api_01_auth_register/view.py`: register orchestration,
  business check, password hashing, transaction and response mapping.
- `app/service/ai/ollama_service.py`: Ollama adapter copied/shared with Study codebase; no live Study caller after business modules disappeared.

## Unwired ownership

No current source establishes:

- chat log business flow;
- real Email Provider delivery, verification token/link generation or retry worker;
- catalog endpoints not listed in `apis/declared-routes.md`; this includes AC-16
  quiz/attempt APIs #28–#32 and Admin APIs #93–#103. The route inventory is the
  source of truth for exact unwired paths.

## Runtime compatibility repairs

1. `app.api.v1` imports the existing `app.modules.guest` package.
2. `responses.py` exposes `success_response` and `error_response(...)`; the latter directly builds an error `JSONResponse`.
3. `TraceIdMiddleware` uses the current trace helper names.

Together these repairs restore the current composition; future fix tasks must
re-evaluate the complete import chain rather than stop at the first error.

## Validation workflow boundary

```text
models.py: declarative model classes, fields/types/defaults and data conversion
→ app/utils/validate.py: shared pure input validation/normalization helpers
→ app/utils/auth.py: shared authentication and token helpers used by API #3, #4, #13, #14, #34 and #46–#53
→ API-specific validate.py when request input rules exist; invalid input returns `error_response(...)`
→ query.py (only when SQL is needed): SQL statement constants
→ view.py: main API flow, query/provider calls, business checks, transactions and response mapping
```

Examples such as no whitespace or an allowed email domain are only applicable
when the API contract confirms them. Current API #1, #2, #3, #4, #6 and #7
validators map invalid input only through `error_response(...)`; API #5's
locale resolver currently only supplies a default and has no invalid-input
branch. API #2 calls an email provider without database access, so it has no
`query.py`. The current API #5 source still declares `DEFAULT_LOCALE` in
`models.py`; this is a placement discrepancy from the model-only rule and must
not be treated as the pattern for new code. No runtime relocation is implied by
this context note.

Auth login/refresh uses shared token helpers from `app/utils/auth.py` and input
normalization from `app/utils/validate.py`. APIs #4, #13 and #14 call
`validate_current_user_request(..., role="STUDENT")`; APIs #46–#63 call the same
guard with `role="MENTOR"`. The guard owns
Bearer parsing, JWT decoding, claim validation and required-role enforcement.
API #13 validates its
Data URL before calling the injectable storage provider and does not access DB.
API #4 has no separate validator module. Module validators handle API-specific input rules before
business/DB operations; DB-backed business checks and transaction ownership
stay in `view.py`. Comments in `view.py` must explain
each meaningful operation in handlers and helpers; cohesive consecutive
statements may share a comment.


## API #60 Mentor support reply

API #60 writes one Mentor reply and ordered UploadAsset links within the caller-owned transaction, then reuses the pure projection in `mentor/_shared/support_request_projection.py` to return the same full SupportRequest shape as API #59. API #59 also calls that shared mapper, so thread validation and projection remain consistent. The local support schema is the API #58 migration 008 fallback; direct course ownership, JSON-array refs and post-resolve permissiveness are DERIVED. Fake-DB HTTP tests do not verify live schema or deployment.

## API #61 Mentor support resolve

`app/modules/mentor/api_61_mentor_support_resolve/` owns `PATCH /api/v1/mentor/support/{request_id}/resolve`. The view uses the shared MENTOR guard, locks the BIGINT request row, repeats direct course-owner scope in the update, transitions OPEN/IN_PROGRESS/WAITING_LEARNER to RESOLVED, and keeps an already resolved timestamp unchanged. It reuses the API #59 message thread query and shared SupportRequest projection, then commits after envelope validation. The transition matrix and local schema mapping are DERIVED; fake-DB tests do not verify live schema or migration deployment.

## API #62 Mentor course-student roster

`app/modules/mentor/api_62_mentor_course_students/` owns `GET /api/v1/mentor/courses/{course_id}/students`. The view uses the shared MENTOR guard, parses a raw signed-int64 path, checks direct `courses.mentor_id`, then reads distinct `ACTIVE` enrollments joined to `STUDENT` users. It returns `UserSummary[]` without pagination and performs no writes. The list response, legacy BIGINT schema, active predicate and direct-owner policy are DERIVED fallbacks kept `Draft — Needs Confirmation`; fake-DB tests do not verify live schema/deployment. API #63 consumes the numeric IDs with a separately documented DERIVED CSV contract.

## API #63 Mentor notification dispatch

`app/modules/mentor/api_63_mentor_notifications_create/` owns
`POST /api/v1/mentor/notifications`. It uses the shared MENTOR guard, parses
CSV Student IDs/channels, requires the recipient set to share an ACTIVE roster
in a directly owned course, inserts one legacy BIGINT notification per Student
and one QUEUED delivery outbox row per channel, and commits the batch once.
The Operation UUID groups notification rows; `meta.notification_ids` provides
the int64 IDs for API #64. CSV/scope/channel/status rules and migration 009 are
DERIVED. The content int64-to-text mapping remains a contract discrepancy. No
worker/provider consumes the outbox; fake-session tests and local DDL do not
verify live schema/deployment or delivery.

## API #64 Mentor notification status

`app/modules/mentor/api_64_mentor_notification_status/` owns
`GET /api/v1/mentor/notifications/{notification_id}/status`. It authenticates
MENTOR before DB access, parses raw signed-int64 path text, reads one
notification/outbox aggregate, and compares its sender to JWT `sub`. It maps
the local API #63 UUID/owner/timestamps and channel states into the direct
`Operation` envelope; status precedence is queued, then failed, then all sent.
The GET is read-only. This response mapping, ownership relation and aggregate
policy are DERIVED and the DD remains Draft. Local fake-session tests and
migration 009 do not verify live schema or worker/provider delivery.

## API #65 Mentor course progress

`app/modules/mentor/api_65_mentor_course_progress/` owns
`GET /api/v1/mentor/courses/{course_id}/progress`. It authenticates MENTOR,
checks direct `courses.mentor_id` ownership, then aggregates active Student
enrollments over published lessons. A latest-row rule resolves duplicate
legacy progress rows; completed count and floor-average percent are returned
in a local `Page<MentorStudentProgress>`. Because catalog #65 declares
`Page<Course>`, that response and the owner/eligibility/formula/latest-row/
unbounded-page rules are DERIVED local choices; the DD remains Draft. Focused
HTTP tests use fake DB results and do not verify live schema/deployment.

## API #66 Mentor course activity analytics

`app/modules/mentor/api_66_mentor_course_analytics/` owns
`GET /api/v1/mentor/courses/{course_id}/analytics`. It authenticates MENTOR,
checks direct `courses.mentor_id` ownership, then aggregates distinct
Student/lesson pairs with `lesson_progress.last_accessed_at` on PUBLISHED
lessons. The response counts those pairs and distinct Students and returns the
latest timestamp. This is a current-state activity proxy because checked-in
DDL has no learner event ledger; it does not represent event frequency. The
local summary response also conflicts with catalog `Page<Course>` and remains
DERIVED/Draft. Fake-session HTTP tests do not verify live schema/deployment.

## API #67 Mentor Student progress

`app/modules/mentor/api_67_mentor_student_progress/` owns
`GET /api/v1/mentor/courses/{course_id}/students/{student_id}/progress`. It
authenticates MENTOR, checks direct course ownership, requires the selected
Student in the ACTIVE Student roster, and reads PUBLISHED lesson progress in
curriculum order. Missing progress maps to NOT_STARTED/0; duplicate legacy
rows use the #65 timestamp/ID selection rule; response summary uses the #65
floor-average rule. The singular response is DERIVED for AC-26 and conflicts
with diagram/catalog `Page<Course>`. Focused HTTP tests use fake DB results;
live schema/deployment are unverified and DD #67 remains Draft.


## API #68 Admin user list

`app/modules/admin/api_68_admin_users_list/` owns the read-only `GET /api/v1/admin/users` route. The view authenticates the `ADMIN` claim before querying, the query module holds SQL constants only, and the response reuses API #04 `UserProfile` inside `Page` with fixed page size 20. Catalog and AC-31 diagram now expose the list shape; page, filter and order semantics are DERIVED. The implementation targets the legacy BIGINT `users` candidate and remains Draft pending live-schema and Admin policy confirmation.


## API #69 Admin user detail

`app/modules/admin/api_69_admin_user_detail/` owns the read-only `GET /api/v1/admin/users/{user_id}` flow. The route passes raw path/header input; the module's shared ADMIN guard precedes signed-int64 parsing and the bound safe profile SELECT. The view maps malformed/no-row to catalog 404 and maps query/projection errors to safe 500 with rollback. It reuses API #04 `UserProfile`. Legacy target, Admin permission mapping and invalid-path 404 are DERIVED; live schema/deployment remain unverified.

## API #70 Admin user update

`app/modules/admin/api_70_admin_user_update/` owns `PUT /api/v1/admin/users/{user_id}`. It uses the shared ADMIN guard, strict DERIVED full-replacement body, signed-int64 path parsing, a bound legacy `users` UPDATE, safe API #04 profile projection and caller-owned transaction. Invalid IDs return catalog 422, missing rows 404, and failed query/projection/commit paths roll back. Local fake-session tests and the checked-in legacy DDL do not verify live schema or policy; the DD remains Draft — Needs Confirmation.

## API #71 Admin user status

`app/modules/admin/api_71_admin_user_status/` owns `PATCH /api/v1/admin/users/{user_id}/status`. It uses the shared ADMIN guard, strict DERIVED status body, signed-int64 path validation, a locked legacy `users` update, conditional refresh-token revocation on suspension, safe API #04 profile projection and caller-owned transaction. Unsupported current states return catalog 422; missing users return 404; query/projection/revoke/commit failures roll back. Focused tests use fake sessions; live schema and policy are unverified, and the DD remains Draft — Needs Confirmation.


## API #72 Admin user delete

`app/modules/admin/api_72_admin_user_delete/` owns `DELETE /api/v1/admin/users/{user_id}`. It uses the shared ADMIN guard, validates signed-int64 path text, conditionally soft-deletes the legacy `users` candidate with `status='DELETED'`, maps the update timestamp to `DeleteResult.deleted_at`, and owns commit/rollback. The route reuses the API #69 path template. Focused tests pass; the status marker/retry mapping are DERIVED, live schema/policy are unverified, and the DD remains Draft — Needs Confirmation.

## API #73 Admin course list

`app/modules/admin/api_73_admin_courses_list/` owns read-only `GET /api/v1/admin/courses`. `query.py` contains SQL constants for matching count/page reads against legacy candidate `courses LEFT JOIN users`; `validate.py` applies the shared ADMIN JWT guard before raw query parsing and rejects category before DB while the relation is absent. `view.py` maps through the shared Course/Page models, rolls back query/mapping failures, and never commits. Page size 20, ID ordering, exact filters, category fallback and Admin permission mapping remain DERIVED; fake DB tests do not prove live schema/deployment. The DD remains Draft.


## API #74 Admin course detail

The route uses the shared `ADMIN` role guard, route-template middleware matching, a read-only legacy BIGINT course/mentor candidate query and shared `CoursePage` mapping. It returns one item without filtering course status and does not commit. Role-to-dedicated-permission mapping, counters, legacy live schema and deployment remain unverified; see `modules/README.md` and `tests.md`.

## API #75 Admin course update

`app/modules/admin/api_75_admin_course_update/` owns the metadata-only `PUT /api/v1/admin/courses/{course_id}` operation. It reuses the API #74 FastAPI route template and Course projection, uses the shared `ADMIN` JWT guard, and owns its update transaction in `view.py`. The strict full-replacement body and legacy BIGINT mapping are DERIVED; status, owner, category, counters and audit remain outside this endpoint. Local focused/full HTTP tests pass, but fake DB rows do not verify live schema, dedicated permission policy or deployment.

## API #76 Admin course status

`app/modules/admin/api_76_admin_course_status/` owns `PATCH /api/v1/admin/courses/{course_id}/status`. It uses the shared `ADMIN` JWT guard, strict DERIVED target status body, signed-int64 path parsing and the shared Course mapper. Status update and `course_status_audit_logs` append share a transaction; same-status is a no-op. Migration 010 and its actor/course BIGINT keys are DERIVED candidates aligned to the legacy model, not live-schema evidence. AC-32's dedicated course-management permission and live deployment remain unverified.

## API #77 Admin course delete

`app/modules/admin/api_77_admin_course_delete/` owns `DELETE /api/v1/admin/courses/{course_id}`. The shared `ADMIN` guard runs before signed-int64 parsing and DB access. The view locks a non-`DELETED` legacy BIGINT candidate and checks enrollment plus active Content/lesson/quiz/assignment dependencies; any candidate blocker returns catalog 422. On success it sets `courses.status='DELETED'`, updates `updated_at`, maps that DB timestamp to `DeleteResult.deleted_at`, then commits. Marker, timestamp, dependency and repeat-404 rules are DERIVED; no child deletion, audit, new column or migration is added. Fake-session tests do not prove live schema. DD stays Draft; linked restore/visibility/writer policy remains open.

## API #78 Admin pending Content queue

`app/modules/admin/api_78_admin_content_pending/` owns read-only `GET /api/v1/admin/content/pending`. It uses the shared ADMIN guard before query parsing, reads active legacy-candidate `contents` rows in `PENDING_REVIEW`, applies exact optional type/course filters to matching count/page queries, and orders by `id ASC` with fixed page size 20. The route returns a Page of the reusable API #49 Content projection. Catalog/diagram cardinality is singular, so Page shape, pagination, exact filters and soft-delete exclusion are DERIVED local behavior; live schema and moderation permission remain unverified. Focused and linked HTTP tests pass, and DD remains Draft.

## API #79 Admin Content detail
`app/modules/admin/api_79_admin_content_detail/` owns read-only `GET /api/v1/admin/content/{content_id}`. The static API #78 pending path remains registered first. The route uses the shared ADMIN guard, then reads one active checked-in legacy `contents` candidate by bound ID and returns the exact reusable Content projection. It does not query `content_versions`, infer author, filter `PENDING_REVIEW`, or mutate state. AC-33 version/author metadata and revision identity remain unresolved; checked-in schema and fake DB tests do not prove live deployment. Focused tests: 13 passed; full suite: 946 passed; DD stays Draft.

## API #80 Admin Content approval
`app/modules/admin/api_80_admin_content_approve/` owns `PATCH /api/v1/admin/content/{content_id}/approve`. Shared `ADMIN` auth precedes signed-int64 path parsing and database access. The view locks an active legacy BIGINT `contents` row, requires `PENDING_REVIEW`, updates it to `APPROVED`, appends actor/status audit in migration 011's `content_review_audit_logs`, validates the exact API #49 Content projection, then commits. Approval state, eligibility, audit schema and atomicity are DERIVED; live schema and dedicated moderation permission are unverified. Focused tests: 22; linked AC-33/#52/#76 regression: 189; full suite: 968; Ruff passes. Revision continuity with #79 remains open; DD stays Draft.

## API #81 Admin Content rejection
`app/modules/admin/api_81_admin_content_reject/` owns `PATCH /api/v1/admin/content/{content_id}/reject`. It validates the required reason string, authenticates shared `ADMIN`, locks an active pending legacy Content row, sets `REJECTED`, and writes one reason-bearing decision row to the existing migration 011 audit candidate before commit. The single audit row both persists the logical reason and records the decision; this physical mapping and pending-state gate are DERIVED. Response reuses API #49 Content fields. Focused tests: 29; linked #49–#53/#78–#81 regression: 200; full suite: 997; Ruff passes. Live schema, dedicated moderation permission, blank-reason policy and #79 revision continuity remain open; DD stays Draft.

## API #82 Admin lessons list

`app/modules/admin/api_82_admin_lessons_list/` owns read-only `GET /api/v1/admin/lessons`. Shared `ADMIN` authentication runs before signed-int64 query parsing and DB access. It reads the legacy BIGINT `lessons` candidate with exact optional `course -> course_id` and `status` filters, excludes `status='DELETED'`, rejects supplied `type` with a field-level 422 because no compatible type source exists, and maps rows through API #09's reusable Lesson model. The array response follows list intent as a DERIVED fallback against catalog `ApiEnvelope<Lesson>`; no page/count is declared. Required projection nulls become safe 500 with rollback; empty results return `[]`. Focused tests: 15; full Study suite: 1012; Ruff passes. Fake DB tests do not verify live schema/deployment or AC-34's dedicated lesson-management permission; DD remains Draft.

## API #83 Admin lesson detail

`app/modules/admin/api_83_admin_lesson_detail/` owns read-only `GET /api/v1/admin/lessons/{lesson_id}`. Shared `ADMIN` authentication precedes custom signed-int64 path parsing and DB access. One bound SELECT reads only non-`DELETED` rows from the legacy BIGINT `lessons` candidate, then maps through API #09's direct reusable `Lesson`; optional content/video nulls are preserved and no dependency join is added. Malformed/out-of-range IDs, missing rows and tombstones return catalog 404; query/projection failures return safe 500 with rollback. Focused tests: 15; linked #09/#74/#82 regression: 54; full suite: 1027; Ruff passes; OpenAPI: 49 paths / 54 operations. Fake DB tests do not verify live schema/deployment or AC-34's fine-grained lesson-management permission; dependency output and nullable `course_id` policy remain open. DD stays Draft.

## API #84 Admin lesson update

`app/modules/admin/api_84_admin_lesson_update/` owns `PUT /api/v1/admin/lessons/{lesson_id}` and shares the #83 dynamic route template. The catalog/AC-34 diagram declare only the path; the strict full-replacement body `{title, content, video_url, order}` is a DERIVED fallback. One bound `UPDATE ... RETURNING` targets only non-`DELETED` rows in the legacy BIGINT `lessons` candidate, sets `updated_at`, and returns the API #09 `Lesson` projection. It preserves course association/status and does not touch upload/resource/progress/audit rows. The view commits after response mapping and rolls back on no-row, query, mapping or commit failure. Focused tests: 23; linked #09/#47/#48/#82–#84 regression: 104; full Study suite: 1050; Ruff passes; OpenAPI: 49 paths / 55 operations. Fake DB sessions do not verify live schema, deployment, timestamp triggers or AC-34 fine-grained permission; nullable `course_id` still produces safe 500. DD stays Draft.

## API #85 Admin lesson status

`app/modules/admin/api_85_admin_lesson_status/` owns `PATCH /api/v1/admin/lessons/{lesson_id}/status`. The strict one-field `{status}` body and `DRAFT/PUBLISHED/SUSPENDED` values are DERIVED from the adjacent API #76 status candidate because catalog/diagram omit a Lesson body/enum. Shared ADMIN auth and signed-int64 parsing run before DB access. The view locks only a non-`DELETED` legacy BIGINT Lesson; an actual change updates status/updated_at and appends migration 012's `lesson_status_audit_logs` actor/lesson/old/new record in one transaction. Same-status is a no-op without duplicate audit. It returns the reusable API #09 Lesson and rolls back query/audit/projection/commit errors. Focused tests: 28; full Study suite: 1078; Ruff passes. Migration/live schema and dedicated AC-34 permission are unverified; DD remains Draft.

## API #86 Admin lesson delete

`app/modules/admin/api_86_admin_lesson_delete/` owns `DELETE /api/v1/admin/lessons/{lesson_id}`. Shared ADMIN auth precedes signed-int64 path parsing and DB access. The view locks a non-`DELETED` legacy BIGINT Lesson, checks `lesson_progress`, `resources`, and `lesson_uploads` with bounded EXISTS predicates, and returns catalog 422 without mutation if any relation exists. Otherwise it sets `status='DELETED'` and `updated_at=CURRENT_TIMESTAMP`, maps the returned DB timestamp to `DeleteResult.deleted_at` by API #77 precedent, then commits. Query, projection, or commit failures roll back; repeat delete maps to 404. Admin #82–#85, Mentor #48, and Resource #12 queries hide/reject the tombstone. Blocker set, marker, timestamp alias and repeat-delete policy are DERIVED; no migration or child/audit mutation is added. Focused tests: 15; linked #09/#12/#47/#48/#77/#82–#86 regression: 180; full Study suite: 1093; Ruff passes; OpenAPI: 50 paths / 57 operations. Fake DB tests do not prove live schema/FK behavior or fine-grained lesson-management permission; DD stays Draft.


## API #87 Admin quiz list

`app/modules/admin/api_87_admin_quizzes_list/` owns `GET /api/v1/admin/quizzes`. Shared `ADMIN` auth runs before raw `course`, `status`, and `page` parsing/DB access; the path is registered in `DESIGN_CONTRACT_PATHS`. The view reads the checked-in legacy BIGINT `quizzes` candidate using exact optional filters, hides `status='DELETED'`, pairs count/page predicates, defaults to page 1 and size 20, and orders by `id ASC`. It returns local `ApiEnvelope<Page<Quiz>>`; this differs from catalog `ApiEnvelope<Quiz>`. Quiz metadata maps legacy `name/time_limit_minutes/passing_score`; API #87 keeps `questions=[]` as its metadata-only list projection. API #88 adds local DERIVED question-type/choice-order candidates, but #87 does not load child rows. Invalid/out-of-range course/page returns local 422 outside catalog errors. At the API #87 checkpoint: 20 focused tests, 93 linked regressions, 1113 full-suite tests, Ruff, and 51 paths / 58 operations. At the API #88 checkpoint, the full Study suite had 1134 tests and OpenAPI had 51 paths / 59 operations. Fake DB tests do not verify live schema/deployment or fine-grained quiz-management permission; DD stays Draft.

## API #88 Admin quiz create

`app/modules/admin/api_88_admin_quizzes_create/` owns `POST /api/v1/admin/quizzes` on the shared `/admin/quizzes` path template. The route accepts raw `Request` bytes and passes them to the view; shared `ADMIN` authentication runs before outer or embedded JSON validation and database access. The direct outer `{config:string, questions:string}` body, HTTP 201, `DESIGN_RESOURCE_CREATED`, and `ApiEnvelope<Quiz>` response remain catalog-backed. Embedded shapes, three QuestionType labels, Admin choice `{id,text,is_correct}`, course-existence→422, input ordering and transactional behavior are DERIVED. Migration 013 adds nullable `quiz_questions.question_type` and `quiz_choices.sort_order` to the local BIGINT candidate; API #88 writes both. Question/choice rows and response mapping are completed before commit; failures roll back. Focused tests: 21; linked #87/#88 regression: 41; full Study suite: 1134; Ruff passes; OpenAPI: 51 paths / 59 operations. Fake sessions and checked-in DDL do not verify live schema/migration/deployment or AC-35 fine-grained permission; DD remains Draft.

## API #89 Admin quiz update

`app/modules/admin/api_89_admin_quizzes_update/` owns `PUT /api/v1/admin/quizzes/{quiz_id}` and shares the #87–#90 path template. The raw route forwards path text, body bytes and Authorization; shared ADMIN auth runs before path/body validation and DB. It reuses API #88's nested request validator and INSERT SQL as a DERIVED full-replacement proposal. The view locks active Quiz, question and choice rows; any attempt or answer history returns catalog 422 before writes. It key-share-locks an existing target Course, updates only course/title/passing_score/duration/updated_at, deletes choices before questions, inserts replacement children in input order, validates the complete response, then commits. `status`, `description`, `created_at`, answer/attempt rows and audit relations are unchanged. Focused tests: 26; linked #87–#89 regression: 67; full Study suite: 1160; Ruff passes; OpenAPI: 52 paths / 60 operations. Body, replacement, history, tombstone, course-move and lock semantics remain DERIVED; fake sessions do not verify live schema/deployment or PostgreSQL locking; fine-grained AC-35 permission is unavailable; DD stays Draft.

## API #90 Admin quiz delete

`app/modules/admin/api_90_admin_quizzes_delete/` owns the raw path-only DELETE
route and transaction. Shared ADMIN auth runs before positive signed-int64
path parsing and DB access. The view locks Quiz → questions → choices, checks
attempts and answer references, then soft-deletes with `DELETED`/`updated_at`
when history exists or hard-deletes choices → questions → Quiz when none exists.
Those persistence branches, answer-only protection and repeat-delete behavior
are DERIVED; AC-35's soft-delete intent is direct. Response projections and
returned child ID sets are validated before commit, and failures roll back.
Focused tests: 18; linked #86–#90 tests: 100; full Study suite: 1178; Ruff
passes; OpenAPI: 52 route templates / 61 operations. Fake sessions do not
prove live schema, migration deployment, PostgreSQL locking/FKs or the #29
cross-API race. Fine-grained AC-35 permission remains unavailable; DD is Draft.

## API #91 Admin quiz statistics

`app/modules/admin/api_91_admin_quizzes_statistics/` owns the local read-only
aggregate for `GET /api/v1/admin/quizzes/{quiz_id}/statistics`. The shared
ADMIN guard runs before raw positive-int64 parsing and DB access. One SQL
constant reads a legacy BIGINT Quiz with a LEFT JOIN to attempts; it counts all
linked attempts, submitted timestamps and non-NULL scores, then maps average,
passed count and pass-rate candidates. It does not filter tombstones/status,
join answers or return Student identifiers. The runtime DTO and metric/error
fallbacks are DERIVED because AC-35 diagram/catalog declare `ApiEnvelope<Quiz>`
without statistics fields. Focused tests: 19; linked #87–#91: 104; full Study
suite: 1197; Ruff passes; OpenAPI: 53 paths / 62 operations. Tests use fake DB
rows and do not prove live schema, query execution/deployment or fine-grained
quiz-management permission; DD remains Draft.

## API #92 Admin notification list

`app/modules/admin/api_92_admin_notifications_list/` owns the local read-only `GET /api/v1/admin/notifications` fallback. `models.py` declares notification query/page/envelope classes, `validate.py` authenticates ADMIN before raw page parsing, `query.py` contains matching count/list SQL constants, and `view.py` owns query, aggregate mapping and safe errors. The route is in `DESIGN_CONTRACT_PATHS`. Runtime returns `Page<Notification>` and maps `channels/status` from the legacy delivery outbox; these response/schema/aggregate choices are DERIVED against the catalog singleton and unresolved AC-36 model. Focused tests: 20; linked #63/#64/#87/#92: 85; full Study suite: 1217; Ruff passes; OpenAPI: 54 paths / 63 operations. Fake sessions do not verify live schema, migration deployment, worker delivery or fine-grained notification permission.


## API #93 Admin notification create/send

API #93 shares `/api/v1/admin/notifications` with the #92 GET. The raw route delegates to the shared ADMIN guard before body parsing. The local DERIVED persistence fallback fans out one legacy BIGINT notification row per explicit recipient and one `QUEUED` `notification_deliveries` row per requested channel, grouped by a UUID and written atomically. The 202 response keeps the direct Notification data shape, using the first row, and includes derived batch metadata. No Push/Email provider is called; live schema, Admin permission, and the Operation bridge remain unverified.


## API #94 Admin notification update

`app/modules/admin/api_94_admin_notifications_update/` owns `PUT /api/v1/admin/notifications/{notification_id}`. The raw route uses the shared ADMIN guard before custom path/body parsing and DB access. Its strict `{title, content}` body and all-QUEUED editability rule are DERIVED because catalog/diagram declare path-only input and no lifecycle state. SQL locks one legacy BIGINT notification and its outbox rows, updates only title/content, validates an API #92 Notification projection, and commits last. It preserves recipient/channels/schedule/read state/deliveries/created_at, and it does not call a provider or scheduler. Focused tests: 20; linked #92–#94: 66; full Study suite: 1263; Ruff passes; OpenAPI: 55 paths / 65 operations. Fake DB tests do not verify live schema/deployment/PostgreSQL locking or fine-grained permission; DD stays Draft.

## API #95 Admin notification delete/cancel

`app/modules/admin/api_95_admin_notifications_delete/` owns `DELETE /api/v1/admin/notifications/{notification_id}` on the #94 path template, adding one operation and no path. The raw route uses the shared ADMIN guard before positive signed-int64 parsing. The view locks one recipient-level legacy BIGINT notification then its delivery rows; the local DERIVED rule requires one or more rows and all statuses QUEUED. It deletes only the selected parent, relies on the checked-in `ON DELETE CASCADE` candidate, maps DB `CURRENT_TIMESTAMP` to DeleteResult, validates the envelope and commits last. Repeated DELETE returns 404; no scheduler/provider call occurs. Focused tests: 21; linked #92–#95: 87; full Study suite: 1284; Ruff check and scoped format pass; OpenAPI: 55 paths / 66 operations. Fake DB tests do not prove live schema, deployment, PostgreSQL lock/cascade behavior, provider cancellation or dedicated permission; DD remains Draft.

## API #96 Admin notification delivery status

`app/modules/admin/api_96_admin_notifications_status/` owns a SQL-only single-notification aggregate query, raw positive-int64 parser, and read-only view. The GET route uses shared ADMIN auth before path parsing, and the exact catalog response remains `ApiEnvelope<Notification>`. The view reads the candidate legacy BIGINT notification plus grouped outbox rows in one query and reuses API #92's channel ordering and QUEUED/FAILED/SENT precedence; counts are not exposed. Invalid ID or no row/no deliveries maps to catalog 404; SQL/projection failures map to 500. The chosen schema, aggregate precedence, positive-ID/no-delivery behavior and role-only permission are DERIVED/SOURCE_REQUIRED. Focused tests: 16; linked #92–#96: 103; full Study suite: 1300; OpenAPI: 56 paths / 67 operations. Fake DB tests do not verify live schema, migration deployment, enum approval, retry grain or fine-grained permission; DD stays Draft.

## API #97 Admin reported discussions

`app/modules/admin/api_97_admin_discussions_reported/` owns the read-only reported-discussion queue. The GET route uses shared ADMIN auth before page parsing and queries; the `query.py` module contains only count/list SQL. The local DERIVED migration candidate `discussion_reports` links to legacy BIGINT `discussions.id`; each queue item represents one Discussion with at least one OPEN/IN_REVIEW report. Optional `reason` and `severity` exact-match together on the same active report, and order follows latest matching report then discussion ID. Page defaults to 1/20; invalid page returns local DERIVED 422. The existing `Discussion` response requires a title, so the queue derives a 120-character normalized content snippet and returns `comments=[]`. Focused tests: 15; linked #92–#95/#97 regression: 102; full Study suite: 1315; Ruff check and scoped format pass; OpenAPI: 57 paths / 68 operations. Live schema, deployment, report ingestion and fine-grained permission remain unverified; DD stays Draft.
