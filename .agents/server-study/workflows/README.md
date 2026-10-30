# Study workflow

## Study API DD deliverables

For Web/API DDs in the `server-study` scope, deliver the Markdown folder with
its required sheets and reports. Do not create a new ZIP for the DD output.
This scope rule overrides the shared `createDD-markdown` skill's ZIP output
requirements, including its delivery checklist and packaging step. Validate
the Markdown files, examples and relative links without requiring a ZIP.

This rule applies only to Study API DD output. Keep the skill's source-archive
inspection rules, and keep the existing ZIP policy for Work, AI and Web scopes.

For coding/fix tasks:

```text
classify task -> worklog preflight/read same-type logs
->
scope AGENTS
-> affected API/core page
-> exact source
-> import/caller/callee trace
-> requirement/contract for missing business behavior
-> smallest implementation
-> focused tests
-> full Study tests when app can collect
-> update affected context
-> context validator
```

For API implementation, keep the module flow explicit:

```text
requirement / DD / schema
-> models.py: declarative model classes, fields/types/defaults and data conversion
-> app/utils/validate.py: shared input validation/normalization helpers
-> app/utils/auth.py: shared authentication and token helpers
-> API-specific validate.py when request input rules exist; invalid input returns `error_response(...)`
-> query.py when SQL is needed: SQL statement constants only
-> view.py: main API flow, DB/provider calls, business checks, side effects, transaction and response orchestration
-> api/v1.py: route and dependency injection
-> focused tests
```

`app/utils/validate.py` contains shared input normalization helpers.
`app/utils/auth.py` owns shared Bearer/JWT/refresh-token helpers and the
role-aware `validate_current_user_request` guard used by APIs #4, #13, #14,
#46 and #68–#79 with an explicit required role. API #3 uses the token helpers for
login/refresh, not this access-JWT guard. An API has a module-local
`validate.py` when it has request-specific rules; API #4 calls the shared guard
directly. Validators return normalized input or `error_response(...)` for
invalid input. They do not raise response errors, construct alternate errors,
query DB or perform side effects. Do not use built-in `ValueError` in Study
Server source or tests. Shared pure helpers return `ErrorDetail`, a sentinel or
another typed result carrying validation failure; API validators/views map it
through the existing `error_response(...)` builders in
`app/core/responses.py`. Non-HTTP errors retain internal error handling and do
not become `JSONResponse`.
API #2 does not have `query.py` because it dispatches through a provider without
DB access.

`models.py` contains model classes, field declarations, types, defaults,
configuration and data conversion only. It does not own runtime validation,
normalization or business rules. If a module needs SQL, `query.py` contains SQL
string constants only; parameter binding and `query_one`/`query_many` calls
belong in `view.py`.

`view.py` owns the main API flow: DB/provider operations, business checks,
transaction boundaries, failure mapping and response construction. Add a short
Vietnamese comment for each meaningful operation in every handler/helper;
consecutive statements that form one operation may share a comment, while
simple assignments do not need individual comments. Keep the API header
comment immediately before each API-facing handler and omit it for internal
helpers.

The current register source normalizes email/password/full_name in
`api_01_auth_register/validate.py`; its model only declares the body fields.
Route OpenAPI metadata retains the prior email and length constraints without
executing them during model parsing.

For API source comments, explain each meaningful operation in `view.py` and
place a short API header immediately before each API-facing handler. Comments
may group consecutive statements in one operation and may use concise DD step
labels when useful. A comment-only task must not change executable statements;
verify this from the diff, then run focused tests, full scope tests and static
checks as available. Do not use comments to reconcile a DD/current-source
discrepancy.

## Implementation checklist

Before edit:

1. Identify endpoint → module → caller/callee/core/service dependencies.
2. Read current source, tests and authoritative contract/schema evidence.
3. Separate expected behavior from current behavior; record `DISCREPANCY` when
   they differ.

After edit:

1. Recheck imports, router/view signatures and query placeholders.
2. Recheck commit/rollback, response/error/trace and secret safety.
3. Run focused verification, then full scope checks when collection is possible.
4. Update the affected `.agents/<scope>/` page and run the context validator.

Do not declare a test or runtime flow verified from source reading alone.

Special rule: because Study has multiple independent import mismatches, a fix for the first exception is not enough evidence that the app is runnable. Re-import the composition root and continue until the approved task boundary is satisfied.

Mọi task phải tạo/cập nhật worklog theo `.agents/worklog/TEMPLATE.md`, tách
`EXPECTED_BEHAVIOR` khỏi `CURRENT_BEHAVIOR` và ghi blocker collection bằng
`DECLARED_NOT_RUNNABLE` khi chưa chạy được.


- API #74 Admin course detail is locally wired with the shared `ADMIN` guard, raw signed-int64 path parsing, a read-only legacy `courses/users` candidate query and a singleton `Page<Course>` response. These query/cardinality/path choices are `DERIVED`; the course-management permission policy and counters remain open, and live schema/deployment are unverified. DD remains `Draft — Needs Confirmation`.

- API #75 Admin course update reuses the #74 path template, but owns a separate PUT handler and transaction. It applies only the shared `ADMIN` role, writes legacy candidate metadata, maps the shared Course projection before commit and leaves status/audit to #76. Body/schema/Page choices remain DERIVED; live schema and dedicated permission remain unverified.

- API #76 Admin course status follows AC-32's direct status + audit flow. Because catalog body and physical audit schema are absent, local code chooses a strict `{status}` body, uppercase target values and a minimal legacy BIGINT `course_status_audit_logs` relation as DERIVED fallbacks. The view locks the row and writes status/audit atomically; a same-status request is a no-op. Preserve Draft status, keep V1-PILOT UUID audit separate, and do not claim live migration/deployment from fake DB tests.
- API #77 Admin course delete follows AC-32 soft-delete intent. The local DERIVED fallback uses legacy `courses.status='DELETED'`, maps DB `updated_at` to `DeleteResult.deleted_at` by API #72 precedent, and blocks enrollment plus active learning-content candidates with catalog 422. It adds no migration, child mutation or #76 audit write. Keep Draft status and state clearly that linked #76/Mentor writer behavior and live schema remain unverified.
- API #78 Admin pending Content uses the current legacy `contents` candidate and shared ADMIN guard; it reads active `PENDING_REVIEW` rows, exact type/course filters, count-matched pagination and stable ID ordering. Because the direct catalog/diagram response is singular while queue/page imply a collection, local `Page<Content>` and page/filter/deleted-row behavior are DERIVED and must remain marked in the Draft DD. No live schema/deployment is inferred from fake DB tests.
- API #79 Admin Content detail reads one active legacy `contents` candidate and returns the direct `Content` schema after shared ADMIN auth. It keeps AC-33 version/author and revision identity unresolved, adds no schema/migration, and does not claim live DB behavior from fake-session tests.
- API #80 Admin Content approval uses shared ADMIN auth, a raw signed-int64 path, row lock, `PENDING_REVIEW` → `APPROVED` update and atomic audit append. The legacy BIGINT audit table/migration 011 and state transition are DERIVED; keep live deployment, dedicated permission and revision continuity open. Focused tests: 22; linked regression: 189; full Study suite at that checkpoint: 968.
- API #81 rejection reuses the nullable reason column in migration 011's audit candidate: it locks active pending Content, changes status to `REJECTED`, and writes one reason-bearing decision row atomically. This mapping/state gate are DERIVED; keep live deployment, dedicated permission, empty-reason owner policy and #79 revision continuity open. Focused tests: 29; linked regression: 200; full Study suite: 997; Ruff passes. The Draft DD and fake-session evidence do not prove deployment.

- API #82 Admin lesson list uses the shared ADMIN guard and the legacy BIGINT `lessons` candidate. The local list response, exact `course`/`status` filters, stable order, malformed-course 422, unsupported-type 422 and exclusion of API #86 tombstones are DERIVED; no pagination or mutation is introduced. Focused suite: 15; full Study suite at implementation checkpoint: 1012; Ruff passes. Fake DB tests do not prove live schema/deployment; dedicated lesson-management permission and catalog cardinality remain open.
- API #84 Admin lesson update uses shared ADMIN auth and a strict four-field full-replacement body because the catalog/diagram specify path only. A single legacy BIGINT `lessons` UPDATE/RETURNING changes metadata plus `updated_at`; view commits after Lesson mapping and rolls back no-row/query/mapping/commit failures. This request/schema/timestamp choice is DERIVED; course association, status, child dependencies and audit remain unchanged. Focused tests: 23; linked #09/#47/#48/#82–#84 regression: 104; full Study suite: 1050; Ruff passes. Fake DB tests do not prove live schema/deployment, trigger ownership or dedicated permission; DD remains Draft.

- API #85 Admin lesson status adds the DERIVED strict `{status}` body with `DRAFT/PUBLISHED/SUSPENDED`, locks only non-`DELETED` legacy BIGINT Lessons, and atomically updates status/updated_at plus migration 012's `lesson_status_audit_logs` record. Same-status requests are no-op without duplicate audit. Shared ADMIN auth is enforced; AC-34's fine-grained permission and live migration/schema remain unverified. Focused tests: 28; full Study suite at API #85 checkpoint: 1078 passed; Ruff passes; OpenAPI after API #86: 50 paths / 57 operations. DD remains Draft.
- API #86 Admin lesson delete uses the local DERIVED legacy `status='DELETED'` tombstone. It locks the Lesson, blocks `lesson_progress`, `resources` and `lesson_uploads` references with catalog 422, and maps database `updated_at` to `DeleteResult.deleted_at` by API #77 precedent. It preserves dependency and #85 audit rows. Admin #82–#85, Mentor #48 and Resource #12 hide/reject the tombstone. Focused tests: 15; linked #09/#12/#47/#48/#77/#82–#86 regression: 180; full Study suite: 1093; Ruff passes; live schema/FK behavior and fine-grained permission remain unverified. DD remains Draft.

- API #87 Admin quiz list is locally wired with shared ADMIN auth before parsing, count-matched page SQL and a metadata-only Quiz projection. Page response, page defaults, exact filters, tombstone exclusion and query 422 are DERIVED against the direct catalog response; `questions=[]` avoids inventing missing QuestionType/QuizChoice fields. Focused tests: 20; linked #07/#78/#82/#86/#87 regression: 93; full Study suite: 1113; Ruff and OpenAPI pass. Live schema/deployment and fine-grained quiz permission remain unverified; DD stays Draft.

- API #88 Admin quiz creation follows the direct catalog’s outer body and 201 envelope, while embedded config/questions schema, QuestionType labels, local answer-key choice shape, course-missing 422 and ordered transactional inserts are DERIVED. Migration 013 adds candidate legacy BIGINT `question_type`/`sort_order`; Student #28 must omit `is_correct`. Focused tests: 21; linked #87/#88 regression: 41; full Study suite: 1134; Ruff/OpenAPI pass. Live schema/deployment, owner approval and fine-grained permission remain unverified; DD is Draft.

- API #89 Admin quiz update has a wired PUT route, shared ADMIN guard, and an atomic parent/child replacement transaction. Its #88-compatible request body, full-replacement semantics, history refusal, tombstone/course rules and lock order are DERIVED because the catalog/AC-35 diagram do not define them. Focused tests: 26; linked #87–#89 regression: 67; full Study suite: 1160; Ruff and OpenAPI (52 paths / 60 operations) pass. Fake DB tests do not prove live schema, migration deployment, or PostgreSQL locking; fine-grained AC-35 permission remains unavailable and DD stays Draft.
- API #90 Admin quiz delete has a path-only DELETE route with ADMIN-before-path/DB validation. It locks Quiz → questions → choices and checks attempts plus linked answers; history uses the local `DELETED`/`updated_at` soft branch, while no history uses child-first hard delete. The hard-delete branch, answer-only safeguard, marker/time mapping and idempotency remain DERIVED. Focused tests: 18; linked #86–#90: 100; full Study suite: 1178; Ruff and OpenAPI (52 paths / 61 operations) pass. Fake sessions do not prove live schema, PostgreSQL FK/lock behavior or API #29 race safety; AC-35 fine-grained permission is unresolved and DD stays Draft.
- API #91 Admin quiz statistics uses shared ADMIN auth before raw positive-int64 path parsing and one read-only LEFT JOIN aggregate over the checked-in legacy BIGINT Quiz/attempt candidate. It returns a separate `QuizStatistics` proposal with DERIVED counts/score metrics, no answer or Student data, no status filter, and no tombstone exclusion. Direct diagram/catalog `ApiEnvelope<Quiz>` remains discrepant; malformed path→404 and metrics remain DERIVED, and the DD stays Draft. Focused tests: 19; linked #87–#91: 104; full suite: 1197; Ruff passes; OpenAPI: 53 paths / 62 operations. Fake DB tests do not prove PostgreSQL/live schema/deployment or AC-35 fine-grained permission.

- API #92 Admin notification list is wired with shared ADMIN auth before query validation, matching count/page SQL and delivery aggregate mapping from the checked-in legacy BIGINT candidates. It returns `Page<Notification>` despite catalog `ApiEnvelope<Notification>`; page defaults/order, recipient-row grain, `PUSH`/`EMAIL`, QUEUED/FAILED/SENT aggregate, DB connection→503 and invalid-page 422 are DERIVED. Focused tests: 20; linked #63/#64/#87/#92: 85; full Study suite: 1217; Ruff passes; OpenAPI: 54 paths / 63 operations. Fake DB tests do not verify live schema, migration deployment, worker or Admin permission; DD remains Draft.


- API #93 Admin notification create/send keeps the direct 202 `ApiEnvelope<Notification>` contract and uses raw-body ADMIN auth. Its local DERIVED fallback requires explicit existing recipients, `PUSH`/`EMAIL`, nonblank title/content and the candidate title limit; it writes one legacy notification per recipient and one QUEUED outbox row per recipient/channel, then commits before 202. The first row is `data`; derived UUID and all IDs are in `meta`. No worker/provider is called. Focused tests: 26; linked #63/#64/#87/#92/#93: 111; full suite: 1243; Ruff passes; OpenAPI: 54 paths / 64 operations. Live schema, deployment, Admin permission, enum approval, and Operation bridge remain unverified; DD stays Draft.


- API #94 Admin notification update adds a raw-body PUT route with shared ADMIN auth before validation. Its local DERIVED fallback updates only title/content and allows rows only while every locked outbox delivery is QUEUED; it preserves recipient/channel/schedule/read/delivery data and created_at. Focused tests: 20; linked #92–#94: 66; full Study suite: 1263; Ruff passes; OpenAPI: 55 paths / 65 operations. DD remains Draft; live schema, deployment and fine-grained permission are unverified.

- API #95 Admin notification delete/cancel preserves path-only `DeleteResult` and exact catalog errors. Its local DERIVED fallback uses shared ADMIN auth, positive signed-int64 validation, parent-then-delivery locks, at-least-one/all-QUEUED eligibility, and hard-deletes only the selected legacy recipient row; the checked-in FK candidate cascades its outbox. `deleted_at` is DB `CURRENT_TIMESTAMP`; repeated DELETE returns 404. No scheduler/provider cancellation is called. Focused tests: 21; linked #92–#95: 87; full suite: 1284; Ruff check/scoped format pass; OpenAPI: 55 paths / 66 operations. Fake DB tests do not establish live schema/deployment/PostgreSQL locks/cascade or external cancellation; fine-grained permission and lifecycle/retention approval remain open; DD stays Draft.

- API #96 Admin notification status keeps the direct singleton `Notification` response and reads one delivery aggregate in one query. The local DERIVED fallback reuses #92's legacy BIGINT/outbox candidate, ordered channels and QUEUED/FAILED/SENT precedence; invalid positive-int64 path or absent delivery rows map to catalog 404. Counts are not added, GET does not commit or call a provider, and SQL/projection failures safely return 500. Focused tests: 16; linked #92–#96 regression: 103; full suite: 1300; Ruff passes; OpenAPI: 56 paths / 67 operations. Fake DB tests do not verify live schema/deployment, aggregate/retry policy, enum approval, fine-grained permission or Operation bridge; DD stays Draft.

- API #97 Admin reported discussions uses the shared ADMIN guard, read-only count/list SQL, and a Study-local DERIVED `discussion_reports` migration candidate keyed by BIGINT Discussion ID. Queue grain is one Discussion across OPEN/IN_REVIEW reports; reason/severity exact-match on the same report. Page 1/20, title snippet, empty comments and invalid-page 422 are local fallbacks. Focused tests: 15; linked #92–#95/#97: 102; full Study suite: 1315; Ruff check/scoped format pass; OpenAPI: 57 paths / 68 operations. The context validator exits with existing DB Admin path omissions and an unavailable drift baseline commit; no API #97 missing path was reported. Live schema, migration deployment and report ingestion remain unverified; DD stays Draft.
