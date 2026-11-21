---
task_id: "2026-10-24-create-study-api83-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #83 — Lấy lesson detail

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3` (`node` không có trong PATH)
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ catalog contract; tách direct/derived/source-required; không bịa schema hoặc asset/payload; read-only mapping ghi N/A.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Giữ API boundaries trong flow; không tự sửa response cardinality; ghi rõ khi diagram và response schema chưa tương thích.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Giữ current source status riêng với DD; chọn đúng behavior từ AC; không tạo ZIP; xác thực template parity và nhóm DD sau khi đủ API.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD Markdown tiếng Việt cho API #83, lập plan và ma trận trước khi tạo thư mục, đọc kỹ AC-34, tham khảo các DD detail/list trước đó, kiểm tra ngay sau authoring.
- Canonical contract/approved DD: Catalog `docs/lists/list_api.md` row #83: `GET /api/v1/admin/lessons/{lesson_id}`, Bearer JWT/role Admin, `path{lesson_id:int64!}`, response `ApiEnvelope<Lesson>`, 200 `DESIGN_RESOURCE_RETRIEVED`, errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`. Reusable `Lesson`: `id`, `course_id`, `title`, optional `content`, optional `video_url`, `order`, `status`.
- AC-34: Admin with lesson-management permission; #83 reads selected lesson, followed by diagram step “Đọc lesson + dependencies”, then the user chooses update/status/delete and list reloads.

## CURRENT_BEHAVIOR

- Source/config: Current `app/api/v1.py` declares API #01–#09 and #12–#14 only. Grep/current inventory found no #83 route, Admin lesson module or focused test. `app/utils/auth.py` has a Student-only guard; `DESIGN_CONTRACT_PATHS` excludes the Admin lesson detail path. Current middleware would map unallowlisted validation/unhandled failures to generic `VALIDATION_ERROR`/`INTERNAL_SERVER_ERROR`; this is a future integration gap, not behavior of an absent route. `error_response` defaults absent error `data` to `{}` while API guidelines expect `null`.
- Schema: Legacy `DB.sql` provides a candidate BIGINT `lessons` table; its `course_id` is nullable while `Lesson.course_id` is required. Legacy `resources.lesson_id` and `lesson_progress.lesson_id` reference lessons. V1-PILOT lessons use UUID `id`, `chapter_id`, `course_version_id`, `title`, `summary`, `position`, `estimated_minutes`, `is_preview`; not interchangeable with catalog Lesson. Live schema is not verified.
- Runnable tests: Docs-only; không chạy application tests.
- Runtime wiring: `UNWIRED / NOT_FOUND` by current source/module/test scan; no runtime request was made.

## SOURCE_TRACE

```text
Admin Bearer principal -> GET lesson detail by `lesson_id` -> check Admin lesson-management permission -> Q1 candidate lookup by lesson ID -> map seven reusable Lesson fields -> 200 or exact catalog errors -> AC-34 continues to choose update/status/delete and reload list
```

## PLAN BEFORE DD AUTHORING

### Sources and coverage reviewed before authoring

- Catalog: exact #83 row and reusable `ApiEnvelope<T>`/`Lesson` schema in `docs/lists/list_api.md`.
- AC: AC-34 actor/precondition/API sequence in `00_AC_API_INDEX.md`; parsed all AC-34 nodes and edges from `AC_04_ADMIN_MANAGEMENT.drawio`; read AC delivery README (30 AC, 103 unique API IDs). No other AC diagram contains this endpoint.
- DB: full relevant `lessons`, `resources`, and `lesson_progress` sections in `DB_UNICA_TABLES.md`; matching ERD relations; legacy `DB.sql`; V1-PILOT `02_study_db.sql` lesson definition. These are design/DDL artifacts; live DB not verified.
- Current source: router, auth helper, middleware allowlist/exception behavior, response helper, API #09 `Lesson` model/query/view; relevant #09 test fixture shows nullable `content`/`video_url` serialized. Search of `app/` and `tests/` for #83/admin lesson detail found no #83 route/module/test.
- Prior DDs: #82 Admin lesson list; #74 Admin course detail (single-item detail and path/error proposals); API #09 curriculum field aliases/status filter precedent. #82's public-only `PUBLISHED` predicate is not copied into Admin detail.
- Skill/template: manifest confirms `createDD-markdown` `SOURCE_BACKED` and wired to `server-study`; Study workflow requires Markdown folder and overrides generic ZIP packaging. Read skill and all eight registered templates; template inventory is 8 files/927 lines, fingerprints recorded in current session output, no archive found under `apps/study-server/docs` or skill DD resources.

### API Requirement Matrix

| API ID | Contract item | Value | Basis/status | DD treatment |
|---|---|---|---|---|
| #83 | Method/path | `GET /api/v1/admin/lessons/{lesson_id}` | Catalog + AC-34; DIRECT | Retain exactly. |
| #83 | Actor/auth | Bearer JWT; role Admin | Catalog/diagram; DIRECT | Require Admin authentication; current guard is Student-only. |
| #83 | Management permission | lesson-management permission | AC-34; DIRECT | Check before any lesson lookup; concrete policy/claim SOURCE_REQUIRED. |
| #83 | Path | `lesson_id:int64!` | Catalog; DIRECT | One required path parameter; no additional body/query. |
| #83 | Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | Catalog/diagram; DIRECT | Exact code. |
| #83 | Errors | 401/403/404/500 with declared `DESIGN_*` codes | Catalog/diagram; DIRECT | Keep exact set; do not add 422/409. |
| #83 | Response | `ApiEnvelope<Lesson>` | Catalog/diagram; DIRECT | Map exactly reusable Lesson, not Page or dependency fields. |
| #83 | Dependency read | Diagram step n5 says “Đọc lesson + dependencies” | AC-34; direct activity label, semantics incomplete | Record conflict: no dependency fields in Lesson response and no defined dependency output; do not add unconsumed query/fields. |
| #83 | Schema | BIGINT legacy vs UUID/versioned V1-PILOT | DDL artifacts; DISCREPANCY | Treat legacy only as candidate mapping, not active/live schema. |

### Request Usage Matrix

| Request item | Source/use | Validation | Query/response use | Status |
|---|---|---|---|---|
| `Authorization` | Header | Valid Bearer JWT; Admin role and lesson-management permission | Authorization before Q1 | Role/auth DIRECT; Admin policy SOURCE_REQUIRED |
| `lesson_id` | Required path int64 | Preserve int64 type; no extra range rule | Bind as `:lesson_id` in Q1; maps to `data.id` | Field/type DIRECT; malformed-ID -> 404 is DERIVED proposal following #74/#09 |
| Request body | None declared | N/A | No use | DIRECT absence |
| Query parameters | None declared | N/A | No use | DIRECT absence |

### Query Matrix

| Query ID | Operation | Candidate table/column | Predicate/join | Purpose/result | Status |
|---|---|---|---|---|---|
| Q1 | SELECT | Legacy `lessons.id` | `id = :lesson_id` | Read at most one Lesson row; no row -> 404 candidate | DERIVED physical candidate; live schema unverified |
| Q1 | SELECT | Legacy `lessons.course_id` | Same row | Map required `Lesson.course_id` | Nullable DDL vs required contract discrepancy |
| Q1 | SELECT | Legacy `lessons.name` | Same row | Map to `Lesson.title` | API #09 alias precedent |
| Q1 | SELECT | Legacy `lessons.content` | Same row | Optional Lesson content | Null/omit serialization to confirm |
| Q1 | SELECT | Legacy `lessons.video_url` | Same row | Optional Lesson video URI | Null/omit serialization to confirm |
| Q1 | SELECT | Legacy `lessons.sort_order` | Same row | Map to `Lesson.order` | API #09 alias precedent |
| Q1 | SELECT | Legacy `lessons.status` | Same row; no status predicate | Map Lesson status for admin lifecycle management | Enum/casing unresolved; do not filter `PUBLISHED` |
| Q-dependencies | Not specified | Legacy `resources.lesson_id`, `lesson_progress.lesson_id` relations exist | No approved selection/output/branch rule | AC diagram dependency label vs response only Lesson; no query added pending resolution | SOURCE_REQUIRED / DISCREPANCY |

### Mutation Matrix

| Mutation ID | Operation | Target | Reason/status |
|---|---|---|---|
| N/A | None — READ ONLY | N/A | GET detail; update/status/delete are separate APIs #84–#86. |

### Response Source Matrix

| Response field | Type | Candidate source | Transform | Null/empty rule | Status |
|---|---|---|---|---|---|
| `success` | boolean | Envelope branch | true on success, false on error | Required | DIRECT envelope convention |
| `businessCode` | string | Catalog | Exact code by branch | Required | DIRECT |
| `message` | string | Application | Safe localized text | Exact wording unspecified | DERIVED wording |
| `data.id` | int64 | Legacy `lessons.id` | Direct | Required | BIGINT candidate |
| `data.course_id` | int64 | Legacy `lessons.course_id` | Direct | Required by API; physical NULL is unresolved | DISCREPANCY |
| `data.title` | string | Legacy `lessons.name` | Alias `name -> title` | Required | API #09 precedent |
| `data.content` | string? | Legacy `lessons.content` | Direct | Optional; NULL vs omit unresolved | Candidate |
| `data.video_url` | uri? | Legacy `lessons.video_url` | Direct | Optional; NULL vs omit unresolved | Candidate |
| `data.order` | int32 | Legacy `lessons.sort_order` | Alias `sort_order -> order` | Required | API #09 precedent |
| `data.status` | LessonStatus | Legacy `lessons.status` | Preserve source value | Required; enum member/case unknown | Candidate + SOURCE_REQUIRED enum |
| `meta` | object | Envelope helper | Empty object candidate | `{}` for success | Current success convention |
| `traceId` | uuid | Trace middleware | Propagate/generate trace | Required | Current Study convention |
| Dependency fields | Not in Lesson | No approved source/contract output | None | Do not add | SOURCE_REQUIRED |

### Pre-authoring decisions

1. Keep DD `Draft — Needs Confirmation`; preserve exact method, path, request, response and error set.
2. Read exactly one legacy candidate row by ID; do not apply public API #09 `PUBLISHED` filtering because AC-34 lets Admin proceed to status management.
3. Keep query limited to Lesson's seven fields. AC-34 dependency read is recorded as a blocking design clarification because it has no response field or use rule; API #86 separately checks progress/reference before deletion.
4. Do not join `courses`, `resources`, `lesson_progress`, student or user fields into this response without a defined purpose/contract.
5. Invalid path conversion -> 404 is a labeled DERIVED proposal, not source-confirmed. Keep catalog error set unchanged.
6. Explicitly retain `course_id` nullability, status enum/casing, Admin guard, soft-delete visibility, error `data` and middleware allowlist gaps.
7. After this plan is written, create `83_admin_lesson_detail` with the 8 registered sheets, `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md`. No ZIP.
8. Defer AC-34 macro-review #82–#86 until #86 DD exists.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| AC detail dependencies | AC-34 n5 says “Đọc lesson + dependencies”; response is only `Lesson` | `DISCREPANCY / SOURCE_REQUIRED` | Do not add uncontracted dependency fields or useless query. |
| Schema/nullability | Legacy BIGINT `lessons.course_id` nullable; reusable `Lesson.course_id` required; pilot is UUID/versioned | `DISCREPANCY / SOURCE_REQUIRED` | Legacy query remains a candidate; NULL row handling and active schema need confirmation. |
| Admin authorization | Catalog/AC requires Admin + lesson permission; current helper is Student-only | `SOURCE_REQUIRED` | No source-backed Admin guard/policy. |
| Path validation | int64 required; catalog has 404 but no 422; middleware generic path behavior exists | `DERIVED / DISCREPANCY` | Propose malformed path -> 404 to fit catalog, requires custom integration. |
| Deleted lesson visibility | API #86 says delete/soft delete by policy; no legacy delete marker | `SOURCE_REQUIRED` | API #83 behavior after delete cannot be fixed. |
| Error integration | #83 path absent from middleware allowlist; helper emits `{}` for absent error data | `DISCREPANCY / CONDITIONAL_FUTURE_WIRING` | Future route must reconcile exact codes and `data:null` guideline. |
| Runtime implementation | Current router/module/test scan | `UNWIRED / NOT_FOUND` | No API #83 route/module/focused test found. |

## CHANGES

- Files changed: `apps/study-server/docs/dd/83_admin_lesson_detail/` (11 Markdown files), this worklog, and `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md`.
- CONTEXT_UPDATES: None planned; no runtime/schema/catalog/diagram changes.
- Context pages changed: None planned.
- Assumptions: Keep behavior outside catalog/diagram labeled `DERIVED` or `SOURCE_REQUIRED`; keep draft status while material contract gaps remain.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog preflight | Deno selector selected #48/#49/#50; all three read fully; no shortage. | VERIFIED |
| Catalog/diagram/source/schema review | Catalog #83 and Lesson schema, complete AC-34 node/edge flow, current router/auth/middleware, #82/#74/#09 precedents, legacy/Pilot schema and lesson dependency ERD reviewed. | VERIFIED_STATIC |
| Template/archive gates | Registry confirmed skill; read complete skill/eight sheets; no archive in Study docs or skill DD resources. | VERIFIED_STATIC |
| Pre-authoring matrices | Requirement, Request Usage, Query, Mutation, Response Source matrices and decisions recorded above before DD directory creation. | VERIFIED |
| Static DD validation | Exact 11-file package; 8/8 template appendix suffixes match byte-for-byte; 3 JSON examples parse; 29 tables consistent; 12 fences balanced; 35 local links/anchors resolve; final newlines/trailing whitespace clean; `git diff --check` clean. | PASS — STATIC |
| Current inventory | 103 catalog IDs; 83 DD folders / 20 missing; 71 full 11-file packages / 12 core-only; 12 route-plus-view pairs / 91 without. | VERIFIED_STATIC_ONLY |
| Application tests | Not planned; documentation-only. | NOT_RUN |

## HANDOFF

- Remaining blockers: AC-34 dependency semantics, active schema/live DB, `course_id` nullability, Admin guard, status enum, malformed path mapping, soft-delete visibility and error-envelope integration need owner/source confirmation.
- Next owner/action: AC-34 macro-review is complete; continue the DD sequence at API #87 in the next API-DD session.

## GROUP_MACRO_REVIEW — AC-34 #82–#86

- Status: `VERIFIED_WITH_OPEN_QUESTIONS`; see `apps/study-server/docs/dd/86_admin_lesson_delete/VERIFICATION_REPORT.md`.
- Findings carried into #83: keep AC-34 dependency output unresolved because `Lesson` has no dependency fields; #86 rechecks current references/progress before delete. Soft-delete visibility across #82/#83/#84/#85 remains open pending a physical marker and owner policy.
- No API approval, route implementation, live schema check or application test is implied by this review.
