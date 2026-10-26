# Source status và discrepancy

Repository deep-context được đối chiếu tại source commit
`9a70eb6764a6587093a92d3bd7e4cc0bea1651c4` ngày 2026-09-18; phần Study server
dưới đây được refresh theo source và test local ngày 2026-10-26.

## Tài liệu thiết kế

```text
DD_STATUS: NOT_FOUND
CANONICAL_BD_STATUS: NOT_FOUND
BUSINESS_CODE_STATUS: CREATED_FROM_CURRENT_RUNTIME
DIAGRAM_API_CONTRACT_STATUS: APPROVED_DESIGN_CONTRACT
```

- Root README/contract README có chỗ trỏ `docs/BD/`, nhưng directory đó không có trong source snapshot.
- Không dùng template, diagram hoặc Git history để tự hoàn thiện request/response/business rule/database mapping thiếu.
- `docs/lists/list_api.md` và `apps/study-server/docs/diagrams/AC_UNICA/` là
  approved V1 design contract theo yêu cầu được phê duyệt; các schema và
  `DESIGN_*` code ở đó vẫn là `DESIGN_PROPOSAL`, không phải runtime/OpenAPI
  evidence.
- Study DD và business-code artifacts hiện có dưới
  `apps/study-server/docs/dd/` và `apps/study-server/docs/business_code/`.
  Chúng là design/documentation evidence, không tự biến thành runtime wiring.
- Work có hai contract file nhưng runtime source hiện tại khớp
  `contracts/openapi/work/legacy-web.openapi.json`; `openapi.json`/README mô tả
  target health/domain surface chưa được Express route đăng ký.
- Study OpenAPI chỉ có placeholder README; AI không có OpenAPI hiện hành.

## Context system

```text
ROOT_ROUTER: AGENTS.md
CONTEXT_REGISTRY: .agents/AGENTS.md
MANIFEST: .agents/context-manifest.json
VALIDATOR: scripts/validate-agent-context.mjs
STUDY_LEGACY_AGENT_CONTEXT: REMOVED; canonical context is under `.agents/server-study/`
```

Deep scopes:

- `server-study`: `.agents/server-study/AGENTS.md`
- `server-work`: `.agents/server-work/AGENTS.md`
- `server-ai`: `.agents/server-ai/AGENTS.md`
- `db-admin`: `.agents/db-admin/AGENTS.md`
- `web-work`: `.agents/web-work/AGENTS.md`
- `mobile-work`: `.agents/mobile-work/AGENTS.md`

Mọi project context phải nằm dưới `.agents/`; `apps/` không chứa `.agent/` hoặc
`AGENTS.md`.

## Study server

```text
RUNTIME_STATUS: SOURCE_BACKED_API_01_09_12_14_34_46_97; 57_API_V1_PATHS_68_OPERATIONS
TEST_STATUS: VERIFIED_1315_LOCAL_STUDY_TESTS
BUSINESS_MODULE_STATUS: SOURCE_BACKED_GUEST_UPLOAD_MENTOR_CONTENT_SUBMISSIONS_SUPPORT_ROSTER_NOTIFICATION_PROGRESS_ANALYTICS_ADMIN_68_97
DATABASE_SCHEMA_STATUS: PILOT_AND_LOCAL_MIGRATIONS_CHECKED_IN; LIVE_STATUS_NOT_VERIFIED_HERE
```

Current evidence:

- `apps/study-server/app/main.py` imports and composes `app.api.v1`; current
  OpenAPI exposes 57 unique `/api/v1` path templates and 68 operations,
  including Admin quiz list/create/update/delete/statistics APIs #87–#91,
  notification list/create/update/delete/status #92–#96 and reported-discussion
  queue #97. Local HTTP/source tests pass as part of the full Study suite
  (`1315 passed`, one upstream Starlette/httpx warning).
- `infra/postgres/` contains V1-PILOT schema artifacts and the local Study
  migrations. Checked-in SQL is not evidence of live schema or migration
  deployment.
- API #63 `POST /api/v1/mentor/notifications` keeps the direct catalog body,
  parses recipients/channels as CSV under a DERIVED local rule, checks a common
  ACTIVE roster in a directly owned course, and atomically writes one legacy
  notification per recipient plus `QUEUED` per-channel outbox rows. Its
  Operation UUID and `meta.notification_ids` provide the local #64 handoff.
  Focused tests use fake DB rows; migration 009 is checked-in only, and live
  schema/deployment plus Push/Email worker delivery remain unverified.
- API #64 `GET /api/v1/mentor/notifications/{notification_id}/status` reads
  the local #63 notification and delivery outbox, checks sender ownership, and
  maps channel states to Operation with a DERIVED policy. Focused and full HTTP
  tests pass; live schema/deployment and worker delivery remain unverified.
- API #67 `GET /api/v1/mentor/courses/{course_id}/students/{student_id}/progress`
  reads a selected Student's current lesson progress using the local #65 owner,
  active-roster, latest-row and floor-average patterns. Its singular response
  remains DERIVED against diagram/catalog `Page<Course>`; focused/full HTTP
  tests pass, while live schema and deployment remain unverified.
- APIs #58–#61 share the local support table/projection fallback. API #58's
  collection-shape and schema choices remain DERIVED and documented in its DD.
- API #68 `GET /api/v1/admin/users` is source-backed with a shared ADMIN JWT guard, read-only legacy `users` queries and safe `Page<UserProfile>` projection. Its list/pagination/filter rules are DERIVED and synchronized in catalog/AC-31; the DD remains Draft pending live schema, permission, PII/audit and lifecycle visibility decisions. Focused/full HTTP tests use fake DB rows and do not establish deployment.
- API #69 `GET /api/v1/admin/users/{user_id}` is source-backed with the shared ADMIN guard, raw signed-int64 path, safe single-user legacy `users` projection and catalog 404 for invalid/no-row. Its source/path/permission mappings remain DERIVED; focused/full HTTP tests use fake DB rows and do not prove live schema/deployment.
- API #78 `GET /api/v1/admin/content/pending` is source-backed locally with shared ADMIN auth, read-only active `PENDING_REVIEW` reads from the checked-in legacy `contents` candidate, exact type/course filters, and `Page<Content>` mapping. The direct catalog/diagram declare a singular Content response; collection cardinality, page rules, exact filters and deleted-row exclusion remain DERIVED in the Draft DD. Focused tests (23), linked regression (160), full suite (933), Ruff and OpenAPI pass; fake DB rows do not prove live schema/deployment or moderation permission.
- API #70 `PUT /api/v1/admin/users/{user_id}` is source-backed with shared ADMIN auth, a strict DERIVED full-replacement body, signed-int64 validation, one legacy `users` update and safe profile response; the body/role rules and target mapping remain DERIVED, and fake DB tests do not prove live schema, authorization policy or deployment.
- At the API #73 checkpoint, `GET /api/v1/admin/courses` had source-backed shared ADMIN auth, read-only legacy `courses/users` candidate queries, matching status/mentor filters, shared Course mapping and fixed Page metadata. Valid `category` returns a 422 fallback because no category relation is source-backed. Focused tests (24), linked #06/#68/#73 regression (60) and full suite (830) passed at that historical checkpoint. API #74 passed at its checkpoint with 845 full tests; current API #76 verification is recorded below.
- Context validation may report pre-existing missing DB Admin context/source
  paths outside the Study scope; report those separately from Study verification.
- `apps/study-server/docs/codebase/README.md` and design DD remain secondary to
  current source, verified tests and executable contracts.
- API #92 `GET /api/v1/admin/notifications` is wired with shared ADMIN auth, count/page queries over checked-in legacy BIGINT notifications and migration-009 delivery candidates, and a local `Page<Notification>` aggregate. The Page response, page size/order, status/channel projection, global visibility and 422/503 mapping remain DERIVED against catalog/AC-36 open questions.
- API #93 `POST /api/v1/admin/notifications` shares that path template. It keeps direct `ApiEnvelope<Notification>` at 202, verifies explicit recipients, fans out one legacy BIGINT notification per recipient with shared UUID and one `QUEUED` delivery row per recipient/channel, and commits before acceptance. The first Notification is `data`; batch UUID/IDs are derived metadata. Focused tests (26), linked #63/#64/#87/#92/#93 regression (111), and full suite (1243) pass; Ruff passes and OpenAPI exposes 54 paths / 64 operations. Fake DB tests do not establish live schema, migration deployment, provider delivery, fine-grained permission, or owner approval; DD remains Draft.
- API #94 `PUT /api/v1/admin/notifications/{notification_id}` is wired with shared ADMIN auth before custom path/body parsing. Its DERIVED strict `{title, content}` fallback locks one recipient-level legacy BIGINT row and its delivery rows, updates title/content only when every delivery remains QUEUED, and preserves audience, channels, schedule, read state, delivery rows and created_at. It returns the #92 Notification projection; no provider/scheduler is called. Focused tests (20), linked #92–#94 regression (66), full Study suite (1263), Ruff, and OpenAPI (55 paths / 65 operations) pass. Fake DB tests do not establish live schema, PostgreSQL locks, deployment, fine-grained permission or owner approval; DD remains Draft.
- API #95 `DELETE /api/v1/admin/notifications/{notification_id}` is wired with shared ADMIN auth before raw positive-int64 parsing. Its DERIVED fallback locks one recipient-level legacy BIGINT notification and its deliveries, requires at least one all-QUEUED delivery, deletes only the path-selected row, and uses the checked-in FK cascade plus DB `CURRENT_TIMESTAMP` for DeleteResult. Repeat DELETE returns 404; no scheduler/provider is called. Focused tests (21), linked #92–#95 regression (87), full suite (1284), Ruff check/scoped format and OpenAPI (55 paths / 66 operations) pass. Fake DB tests do not prove live schema/deployment/PostgreSQL locking/cascade, external cancellation, fine-grained permission or owner approval; DD remains Draft.
- API #96 `GET /api/v1/admin/notifications/{notification_id}/status` is wired with shared ADMIN auth before positive signed-int64 parsing and a single read-only aggregate query over the same legacy notification/outbox candidate as #92. It reuses the existing `Notification` schema and #92's ordered channels plus QUEUED/FAILED/SENT precedence; malformed ID/no delivery result maps to catalog 404 and SQL/projection errors to 500. Focused tests (16), linked #92–#96 regression (103), full suite (1300), Ruff and OpenAPI (56 paths / 67 operations) pass. Fake DB tests do not prove live schema/deployment, approved aggregate/enum policy, retry grain or fine-grained permission; DD remains Draft.
- API #97 `GET /api/v1/admin/discussions/reported` is wired with shared ADMIN auth before signed-int32 page parsing. It queries a Study-local DERIVED `discussion_reports` candidate linked to legacy BIGINT Discussions, deduplicates the queue by Discussion, filters exact reason/severity on active reports and returns Page<Discussion> with a derived title snippet and empty comments. Focused tests (15), linked #92–#95/#97 regression (102), full Study suite (1315), Ruff check/scoped format and OpenAPI (57 paths / 68 operations) pass. Fake DB tests do not establish live schema, migration deployment or report ingestion; DD remains Draft.

## Work server

```text
RUNTIME_STATUS: SOURCE_CHANGED_STUDY_STYLE_COMPATIBILITY_API
OPENAPI_STATUS: LEGACY_WEB_ALIGNED; SYSTEM_ROUTES_VERIFIED; TARGET_DOMAIN_DISCREPANCY
DATABASE_SCHEMA_STATUS: VERIFIED_PRISMA_12_MODELS
HEALTH_ROUTE_STATUS: VERIFIED_INJECTED_PROBE
```

- `src/main.ts` loads typed config from the tracked static
  `src/utils/constants.ts`, binds the local listener to `127.0.0.1:3002`,
  creates injected dependencies, connects Prisma before listening and gracefully
  disconnects on shutdown; `src/app.ts` exposes `createApp(options)` for
  fake-dependency HTTP tests. `.env` and `process.env` are not runtime config
  sources.
- `src/core/` owns typed config, Prisma factory, trace context, response/error
  envelopes, centralized exception mapping and HS256 security helpers.
- `src/api/v1.ts` only composes route modules. Auth, students, businesses, jobs,
  CV and applications use `models/validate/view/query`; `src/routes/api_routes.ts`
  is a compatibility re-export.
- `GET /api/v1`, `/health/live`, and `/health/ready` are wired. Ready probes the
  injected Prisma dependency and returns `503 DEPENDENCY_UNAVAILABLE` on failure.
- Current API routes cover student/business login, student registration, public
  jobs, `/me`, student CV/applications and business jobs/applications/CV detail.
  Chat, notifications, interviews, university, TopCV/TopJD and Admin routes are
  not wired.
- JWT Bearer parsing is optional at app level; protected routes use
  `ensureAuthenticated`/`checkRole` and always return JSON `401/403`. There is no
  cookie/session auth or HTML redirect.
- Prisma source is the 12-model legacy Work schema. Supabase config/dependency,
  callback auth helper and empty chat/notification/top services are declared but
  not used by the current route graph.
- `test/app.test.ts` provides injected Supertest coverage; normal npm/pnpm
  scripts are declared, while this shell uses a Deno fallback because Node is
  unavailable.

## Work web

```text
RUNTIME_STATUS: VERIFIED_REACT_VITE_SOURCE
API_STATUS: VERIFIED_RELATIVE_API_CLIENT
TEST_STATUS: SOURCE_TESTS_PRESENT; TYPECHECK_TEST_BUILD_PASS_VIA_DENO_FALLBACK
DESIGN_STATUS: SOURCE_BACKED_COBALT_BASELINE_IMPLEMENTED
```

- `src/app/router.tsx` owns public, student and business routes with role guards;
  unsupported workspace destinations render static/placeholder pages.
- `src/shared/api/work.ts` uses relative `/api/v1`, Zod envelope parsing,
  React Query consumers and Zustand `access_token` persistence. Requests omit
  cookies and send a single optional Bearer header.
- Vite development binds Work Web to `127.0.0.2:3001` and proxies `/api`,
  `/uploads` and `/img` to Work server `127.0.0.1:3002`. Current tests cover
  role access and the Bearer/401 token boundary.
- The presentation layer now has Cobalt semantic tokens, shared UI primitives,
  responsive public/workspace menus and reduced-motion/focus rules. This is a
  presentation-only change; route, API, auth and page-local data flow remain
  unchanged.

## Work mobile

```text
RUNTIME_STATUS: SOURCE_BACKED_DIRECT_NEON
CLIENT_SERVER_STATUS: NOT_HTTP_WIRED_TO_WORK_SERVER
TEST_STATUS: UNIT_TESTS_PRESENT; FLUTTER_TOOLCHAIN_UNAVAILABLE; NETWORK_SMOKE_OPT_IN
DESIGN_STATUS: SOURCE_BACKED_COBALT_BASELINE_IMPLEMENTED
```

- Student and business are Android flavors of one Flutter project with package
  name `study2work_mobile`. Both start at role-specific `DangNhap` through the
  shared flavor router, use direct Neon PostgreSQL through a singleton
  `NeonDatabase`, and keep account/lookup data in SQLite.
- Chat reads/writes `Chat` and `DoanChat` directly, polls every three seconds,
  deduplicates by message `id`, and cancels screen timers in `dispose()`.
- The shared core calls Gemini directly from `AIService`; this is independent of the
  Work server and `apps/ai-server`. URL/row/model normalization and polling
  tests exist; connection smoke tests require an explicit Dart define.
- The unified app owns a shared Material 3 Cobalt theme and UI primitives under
  `lib/app/theme/`. The merge preserves direct
  Neon/SQLite/Gemini boundaries and chat polling semantics are preserved.

## AI server

```text
RUNTIME_STATUS: VERIFIED_MINIMAL_CHAT
COPIED_CORE_STATUS: UNWIRED
DATABASE_RUNTIME_USAGE: NONE
TEST_STATUS: NOT_FOUND
```

- Runtime flow: FastAPI -> `/api/v1/chat_log_ai` -> `chat_log_ai()` -> `OllamaService.generate()`.
- `app/core/*` phần lớn là copied infrastructure và không được đăng ký từ `app/main.py`.
- `pyproject.toml` chỉ khai báo FastAPI/httpx/uvicorn; copied DB/security/config code cần package ngoài dependency set hiện tại.
- `query.py` và `validate.py` của chat là empty placeholders.
- Không có schema/migration/business-code catalog/OpenAPI/test cho AI server.

## DB Admin

```text
WEB_STATUS: VERIFIED_LOCAL_ANGULAR_APP_WITH_ONE_COMMAND_LAUNCHER
API_STATUS: VERIFIED_LOCAL_FASTAPI_APP_WITH_INTERNAL_DEV_LAUNCHER
DATABASE_STATUS: CONFIGURED_BY_LOCAL_CORE_CONSTANTS_ONLY
AUTH_STATUS: JWKS_IMPLEMENTED; LOCAL_DEV_AUTH_TEST_ONLY
AUDIT_STATUS: DURABLE_CONTROL_PLANE_WITH_BOUNDED_FALLBACK
```

- `apps/db-admin-web/` is an Angular app in the pnpm workspace. Its local
  `dev`/`start` launcher starts FastAPI and proxies same-origin `/api` calls.
- `apps/db-admin-server/` remains a separate FastAPI runtime/security boundary
  and is not mounted by Study/Work/AI. Its routes, response envelope,
  permission dependencies and transaction safety are verified by its local test
  suite.
- `apps/db-admin-server/sql/db_admin/001_bootstrap.sql` và
  `scripts/bootstrap_access.py` là control-plane bootstrap độc lập; không phải
  Study/Work business migration. Catalog vẫn đọc metadata từ target runtime.
- `app/services/audit.py` có durable `db_admin.admin_audit_events` path khi
  target đã có control-plane schema, cùng bounded in-memory/structured-log
  fallback. Việc live bootstrap đã được apply chưa được xác minh ở đây.
- `apps/study-server/docs/business_code/code_http.md` và
  `code_event_server.md` tồn tại cho Study; chúng phải được phân biệt với
  runtime business-code evidence của Work/AI/DB Admin.
- DB Admin business codes hiện được sở hữu bởi API source/README và local
  contract; không suy diễn chúng từ Study catalog.

## Drift rule

Nếu tracked source của deep scope thay đổi sau `sourceCommit`, validator báo `CONTEXT_STALE`. Khi đó phải đọc source mới và cập nhật context; không chỉ đổi commit trong manifest để làm validator xanh.

### API #71 status transition

API #71 `PATCH /api/v1/admin/users/{user_id}/status` is source-backed with the shared ADMIN JWT guard, strict DERIVED ACTIVE/SUSPENDED request body, signed-int64 validation, locked legacy `users` update, conditional active refresh-token revoke on suspension and safe API #04 profile response. Focused and linked HTTP tests pass locally. Live schema, authorization policy and deployment are not verified; the DD remains Draft — Needs Confirmation.


### API #72 soft-delete

API #72 `DELETE /api/v1/admin/users/{user_id}` is source-backed locally with the shared ADMIN JWT guard and a conditional `users.status='DELETED'` update. Its local DERIVED fallback returns `updated_at` as `DeleteResult.deleted_at`, preserves linked rows and does not revoke issued access JWTs. Focused, linked and full local tests pass. Owner policy, live schema and deployment remain unverified; the DD remains Draft — Needs Confirmation.

- API #74 `GET /api/v1/admin/courses/{course_id}` is source-backed locally with shared ADMIN auth, a read-only legacy `courses/users` candidate query, all-status visibility, shared Course mapping and singleton Page metadata. Focused tests (15), linked #06/#08/#69/#73/#74 regression (80), full suite (845), Ruff and OpenAPI checks pass. Fake DB tests do not establish live schema/deployment or dedicated course-management permission; counters remain undefined and DD remains Draft.

- API #75 `PUT /api/v1/admin/courses/{course_id}` is source-backed locally as a metadata-only update over the legacy BIGINT `courses` candidate. It uses shared ADMIN auth, strict DERIVED full replacement, int64/decimal validation, Course projection readback, singleton Page and caller-owned commit/rollback. Focused tests (27), linked #06/#08/#70/#73/#74/#75 regression (113), full suite (872), Ruff and OpenAPI checks pass. No catalog/diagram/DDL/migration/live DB change was made; body/schema/permission choices remain DERIVED and DD stays Draft — Needs Confirmation.

- API #76 `PATCH /api/v1/admin/courses/{course_id}/status` is source-backed locally with shared ADMIN auth, strict DERIVED target body, legacy BIGINT status/audit transaction, #74 Course projection and singleton Page. Its audit relation/migration are DERIVED artifacts; V1-PILOT UUID audit is not used. Focused tests (18), linked regression (134), full Study suite (890), Ruff and OpenAPI verification are recorded in Study worklog/context. Fake DB tests do not prove live schema/migration/deployment or dedicated permission policy; DD remains Draft.

- API #77 `DELETE /api/v1/admin/courses/{course_id}` is source-backed locally with shared ADMIN auth, signed-int64 path parsing, enrollment/content dependency checks and a soft-delete marker on the legacy BIGINT `courses` candidate. It maps DB `updated_at` to `DeleteResult.deleted_at` by API #72 precedent; dependency/marker/repeat behavior are DERIVED. Focused tests (20), linked regression (143), full Study suite (910), Ruff and OpenAPI verification pass. No migration/cascade/audit write; fake DB tests do not prove live schema/deployment or dedicated permission. DD remains Draft, and linked #76/Mentor writer behavior is still open.

- API #79 `GET /api/v1/admin/content/{content_id}` is source-backed locally with shared ADMIN auth, one read-only active-row query against checked-in legacy `contents`, and the direct eight-field `Content` response. Invalid/missing/deleted IDs map to catalog 404; safe query/projection failures map to 500. AC-33 version/author metadata and revision identity remain unresolved; fake DB tests do not prove live schema/deployment or moderation permission. Focused tests (13), full Study suite (946), Ruff and OpenAPI route counts (45 templates / 50 operations) pass.
- API #80 `PATCH /api/v1/admin/content/{content_id}/approve` is source-backed locally with shared ADMIN auth, raw int64 validation, locked active Content, `PENDING_REVIEW` → `APPROVED`, atomic audit insert and direct eight-field Content response. Focused tests (22), linked #49–#53/#76/#78–#80 regression (189), full Study suite (968), Ruff and OpenAPI (46 templates / 51 operations) pass. The target state, eligibility gate, legacy BIGINT audit table and migration 011 are DERIVED; fake DB tests do not prove live schema/deployment, dedicated moderation permission or exact revision continuity with #79. DD remains Draft.
- API #81 `PATCH /api/v1/admin/content/{content_id}/reject` is source-backed locally with shared ADMIN auth, raw int64 validation, required reason string, locked active Content, `PENDING_REVIEW` → `REJECTED`, atomic reason-bearing decision row in migration 011's audit candidate, and direct eight-field Content response. Focused tests (29), linked #49–#53/#78–#81 regression (200), full Study suite (997), Ruff and OpenAPI (47 templates / 52 operations) pass. The physical reason/audit mapping and pending gate are DERIVED; fake DB tests do not prove live schema/deployment, dedicated moderation permission, blank-reason policy or exact revision continuity with #79. DD remains Draft.

- API #82 `GET /api/v1/admin/lessons` is source-backed locally with shared ADMIN auth, exact course/status filters against the legacy BIGINT `lessons` candidate, stable ordering, `Lesson[]` response, and explicit 422 for malformed `course` or unsupported `type`. Focused tests (15), full Study suite (1012), Ruff and OpenAPI (48 templates / 53 operations) pass. The array shape conflicts with catalog `ApiEnvelope<Lesson>`; fake DB tests do not prove live schema/deployment or dedicated lesson-management permission. No pagination/result cap is declared; DD remains Draft.
- API #83 `GET /api/v1/admin/lessons/{lesson_id}` is source-backed locally with shared ADMIN role auth, custom signed-int64 path parsing, one read-only lookup against non-`DELETED` rows in the legacy BIGINT `lessons` candidate and direct reusable `Lesson` mapping. Malformed/missing/tombstoned IDs return catalog 404; query/projection failures return safe 500 with rollback. Focused tests (15), linked #09/#74/#82 regression (54), Ruff and OpenAPI pass. Fake DB tests do not prove live schema/deployment or AC-34 fine-grained permission; dependency output and nullable `course_id` policy remain open; DD stays Draft.
- API #86 `DELETE /api/v1/admin/lessons/{lesson_id}` uses a DERIVED legacy soft-delete fallback: lock a non-`DELETED` BIGINT Lesson, block progress/resources/lesson-upload references with catalog 422, then set `status='DELETED'` and `updated_at`; return persisted `updated_at` as `DeleteResult.deleted_at`. Repeat delete is 404. APIs #82–#85, Mentor #48 and Resource #12 hide/reject tombstones. Focused tests (15), linked #09/#12/#47/#48/#77/#82–#86 regression (180), full Study suite (1093), Ruff and OpenAPI (50 templates / 57 operations) pass. Fake DB tests do not verify live schema/FKs/locking, owner approval or fine-grained AC-34 permission; DD remains Draft.

- API #87 `GET /api/v1/admin/quizzes` is source-backed locally with shared ADMIN auth before raw query parsing, exact course/status filters, `DELETED` exclusion, count-matched page size 20, and `id ASC`. It returns `ApiEnvelope<Page<Quiz>>` despite the direct catalog singleton `ApiEnvelope<Quiz>` and leaves nested questions empty as a metadata-only list projection; API #88 adds local DERIVED child-column candidates but #87 does not load child rows. Invalid course/page returns a local 422 outside the catalog errors. Focused tests (20), linked #07/#78/#82/#86/#87 regression (93), full Study suite (1134), Ruff and OpenAPI (51 templates / 59 operations) pass. Fake DB tests do not verify live schema/deployment or fine-grained quiz-management permission; DD remains Draft.

- API #88 `POST /api/v1/admin/quizzes` is source-backed locally with raw-body handling, shared ADMIN auth before parse/DB, and an atomic Quiz → question → choice create flow. The catalog outer strings/201 envelope remain direct; embedded JSON, type vocabulary, answer-key choice shape, course-missing 422 and order are DERIVED. Migration 013 adds local legacy BIGINT `question_type` and `sort_order` candidates; old rows are not backfilled. Focused tests (21), linked #87/#88 regression (41), full Study suite (1134), Ruff and OpenAPI (51 templates / 59 operations) pass. Fake DB tests do not verify live schema/migration/deployment or fine-grained AC-35 permission; DD remains Draft.
- API #89 `PUT /api/v1/admin/quizzes/{quiz_id}` is source-backed locally with shared ADMIN auth before raw path/body parsing and one transactional full replacement of Quiz questions/choices. The body reuses #88's nested JSON validator; tombstone/missing 404, attempt/answer history 422, target-course validation and row-lock policy are DERIVED. Focused tests (26), linked #87–#89 regression (67), full Study suite (1160), Ruff and OpenAPI (52 paths / 60 operations) pass. Fake DB tests do not verify live schema, migrations, PostgreSQL locking/FKs or fine-grained AC-35 permission; DD remains Draft.
- API #90 `DELETE /api/v1/admin/quizzes/{quiz_id}` is source-backed locally with shared ADMIN auth before positive signed-int64 parsing, parent/child row locks, attempt plus linked-answer history checks, and one transaction. History takes the local `DELETED`/`updated_at` soft branch; no history takes choices → questions → Quiz hard delete. Those deletion policies, answer-only safeguard and repeat/timestamp semantics are DERIVED. Focused tests (18), linked #86–#90 regression (100), full Study suite (1178), Ruff and OpenAPI (52 paths / 61 operations) pass. Fake DB tests do not prove live schema, PostgreSQL constraints/locking, deployment or API #29 race safety; fine-grained AC-35 permission remains unavailable and DD stays Draft.
- API #91 `GET /api/v1/admin/quizzes/{quiz_id}/statistics` is source-backed locally with ADMIN-before-path/DB validation and one read-only legacy BIGINT Quiz/attempt aggregate. It counts all attempts, submitted timestamps and non-NULL scores, then derives average, passed count and pass rate without status filtering, answer reads or Student identifiers. The separate `QuizStatistics` DTO, metrics, retained-tombstone visibility and malformed-path-to-404 mapping are DERIVED against diagram/catalog `ApiEnvelope<Quiz>`; DD remains Draft. Focused tests (19), linked #87–#91 regression (104), full suite (1197), Ruff and OpenAPI (53 paths / 62 operations) pass. Fake DB tests do not prove live schema, PostgreSQL execution/deployment or fine-grained AC-35 permission.
