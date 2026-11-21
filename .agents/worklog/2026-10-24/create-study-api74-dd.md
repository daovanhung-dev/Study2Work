---
task_id: "2026-10-24-create-study-api74-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #74

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Tách candidate `DERIVED` khỏi source; giữ schema legacy/pilot, assignment và live-schema gap riêng; dùng ma trận trước khi authoring; Study DD là Markdown-only.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Giữ đúng catalog contract; không invent Content/tree/schema; dùng `SOURCE_REQUIRED` cho quan hệ hoặc field chưa có nguồn.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Tách AC-22/AC-33 evidence khỏi physical schema; ghi proposal đơn giản là `DERIVED`; API status/wiring không suy ra từ DD.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD tiếng Việt cho API #74; đọc toàn bộ node/edge AC-32 và DD liên quan; ghi plan và ma trận trước khi tạo folder; kiểm tra ngay sau khi authoring; giữ macro-review AC-32 pending đến khi hoàn tất #77.
- Canonical contract/approved DD: `docs/lists/list_api.md` row #74: `GET /api/v1/admin/courses/{course_id}`, Bearer JWT, role Admin, `path{course_id:int64!}`, response `ApiEnvelope<Page<Course>>`, HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, errors 401/403/404/500 với đúng business code trong catalog. Reusable schemas: `Page<T>={items:T[],pagination:PageMeta}`, `PageMeta={page:int32,size:int32,total:int64,total_pages:int32}`, `Course={id,title,description?,thumbnail_url?,price,status,mentor:UserSummary,category?}`, `UserSummary={id,full_name,avatar_url?}`.

## CURRENT_BEHAVIOR

- Source/config: Không có route API #74 hoặc `/api/v1/admin/courses/{course_id}` trong `apps/study-server/app/api/v1.py`; không có module `api_74_*`, Admin course-detail module hay test #74. Router có source API #01–#09 và #12–#14. `app/utils/auth.py` chỉ có guard Student; không có Admin/course-management permission guard. `DESIGN_CONTRACT_PATHS` chưa gồm endpoint #74. API #08 hiện có `GET /api/v1/courses/{course_id}` dùng `courses LEFT JOIN users`, map Course/Page singleton, nhưng chỉ truy vấn `PUBLISHED`; không áp dụng status filter đó vào AC-32 Admin.
- Schema artifacts: Legacy `infra/postgres/study-server/DB.sql` có `courses` BIGSERIAL với `mentor_id`, `name`, `description`, `thumbnail_url`, `price`, `status`; `mentor_id` và `price` cho phép NULL trong DDL. Legacy `users` có `id`, `full_name`, `avatar_url`. `DB_UNICA_TABLES.md` ghi mapping `courses` là `DESIGN_ONLY` và mô tả `mentor_id` bắt buộc, lệch nullability DDL; live schema chưa xác minh. Không có quan hệ `courses`–`categories` trong legacy DDL. V1-PILOT dùng UUID `courses.owner_subject_id` và `course_versions`, khác contract BIGINT; không map ngầm.
- Runnable tests: Không có test API #74. API #08 có source/tests cho path invalid → 404, missing/unpublished → 404, query/mapping error → 500, Course mapping và response Page singleton; không chạy tests trong task docs-only.
- Runtime wiring: API #74 `UNWIRED / NOT_FOUND`. Current `error_response` đổi `data=None` thành `{}`, lệch `contracts/api-guidelines/README.md` yêu cầu `data:null`; nếu API #74 được wire mà chưa thêm path vào `DESIGN_CONTRACT_PATHS`, framework validation/unhandled exception sẽ dùng business code generic thay vì `DESIGN_*`.

## SOURCE_TRACE

```text
Admin Bearer principal -> kiểm tra Admin + course-management permission theo AC-32 -> nhận path course_id -> Q1 candidate đọc 1 course và mentor từ legacy courses/users theo id, không lọc status -> không có course: 404 -> map Course và Page<Course> singleton -> trả 200 hoặc exact catalog 401/403/404/500 -> UI chọn #75/#76/#77 rồi quay về #73.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #74 endpoint | Catalog #74; AC-32 page and diagram | `UNWIRED / NOT_FOUND` | DD is design-only. |
| `Page<Course>` on detail path | Catalog/diagram direct; API #08 current source returns one-item CoursePage | `DIRECT + DERIVED pagination` | Preserve contract and propose a singleton page; do not change response type. |
| Diagram counters | AC-32 node `Đọc course + owner + counters`; no counter fields in Page/Course contract | `DISCREPANCY / SOURCE_REQUIRED` | Do not invent fields or aggregate queries; open for AC-32 macro-review. |
| Admin permission | AC-32 precondition requires course-management permission; current source has Student guard only | `DIRECT requirement / SOURCE_REQUIRED mechanism` | Document gate; do not invent Admin claims/tables. |
| Course data source | Legacy BIGINT DDL vs V1-PILOT UUID/versioned model; live schema unknown | `DISCREPANCY / NOT_VERIFIED` | Legacy columns are query candidates only; keep pilot separate. |
| Mentor nullability | Legacy DDL allows `courses.mentor_id` NULL; table guide marks required; current API #08 fails mapping if mentor absent | `DISCREPANCY` | Required Course.mentor cannot be built for orphan course; candidate safe 500 stays open. |
| Course category | Contract has optional `category`; legacy has separate categories but no relationship | `SOURCE_REQUIRED` | Omit optional field; no guessed join. |
| Status visibility | API #08 filters `PUBLISHED`; AC-32 manages lifecycle via #75/#76 and #73 list proposes all statuses | `DERIVED` | #74 reads all stored statuses without PUBLISHED filter. |
| Error integration | Current error helper emits `{}` for absent data; guidelines require null; admin path not allowlisted | `DISCREPANCY / CONDITIONAL_FUTURE_WIRING` | Keep catalog code set direct; flag allowlist/envelope integration before implementation. |

## CHANGES

- Files changed: `apps/study-server/docs/dd/74_admin_course_detail/` (8 sheets + 3 reports); `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md`; this worklog.
- CONTEXT_UPDATES: None expected unless current context pages are materially stale.
- Context pages changed: None.
- Assumptions: Preserve all pre-existing worktree changes; create only the API #74 Markdown DD folder after the complete plan is recorded here.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog preflight | Selected #48/#49/#50; each was read in full. | `VERIFIED` |
| Scope/skill/template | Loaded server-study entry/index/workflow, skills index, manifest wiring and `createDD-markdown` authoring, reconciliation and quality-gate rules; opened all 8 registered template sheets and fingerprints. | `VERIFIED_STATIC_ONLY` |
| AC-32 | Parsed every cell and edge on page AC32 in `AC_04_ADMIN_MANAGEMENT.drawio`; confirmed #73 → #74 course/owner/counters → decision #75/#76/#77 → reload. | `VERIFIED_STATIC_ONLY` |
| Catalog/schema/source | Read #74 and reusable schema, AC-32 index, ERD/table guide, legacy and pilot DDL, Admin/detail precedents #69/#73, current APIs #06/#08 and #08 tests; API #74 route/module/test absence and auth/error boundary confirmed. | `VERIFIED_STATIC_ONLY` |
| Plan-before-folder gate | Full requirement, request usage, query, mutation and response-source matrices were written here before creating `74_admin_course_detail/`. | `VERIFIED` |
| DD package/template | Exact 11-file manifest; 8/8 front matter and appendix suffixes byte-match registered templates; no ZIP. | `VERIFIED_STATIC_ONLY` |
| Contract/field coverage | Exact API #74 success/error set; Course/UserSummary/PageMeta response fields listed. Category remains optional/omitted; counters remain `SOURCE_REQUIRED`. | `VERIFIED_WITH_OPEN_GAPS` |
| Static Markdown verification | 32 tables, 39 local links/anchors, balanced code fences, 2 valid JSON examples, exact manifest and no whitespace errors. | `VERIFIED` |
| Output fingerprint | SHA-256 `8b267a0f66c8d77a7f18c7e74a46768a2f021140a254a0fe1c155509e6460ea5` over 8 sheets + PLAN_RESULT + OPEN_QUESTIONS, excluding VERIFICATION_REPORT. | `RECORDED` |
| Inventory refresh | 103 catalog APIs; 74 complete core DD folders; 62 full 11-file packages; 29 folders still missing; source-wired count stays 12/103. | `VERIFIED_STATIC_ONLY` |
| Git whitespace | `git diff --check` completed without diagnostics; untracked DD markdown whitespace was also checked by the custom verifier. | `VERIFIED` |
| Runtime tests | Not run; docs-only. API #74 remains `UNWIRED / NOT_FOUND`. | `NOT_RUN` |
| AC-32 macro-review | Review deferred until #75–#77 DDs exist; retain counter/schema/auth and lifecycle questions. | `PENDING` |

## PLAN BEFORE DD AUTHORING

1. Preserve exact contract: `GET /api/v1/admin/courses/{course_id}`, Bearer JWT/Admin, required int64 path, `ApiEnvelope<Page<Course>>`, 200 `DESIGN_RESOURCE_RETRIEVED`, errors exactly 401/403/404/500; no body/query and no extra code.
2. Follow AC-32: Admin opens #73 list, #74 returns course detail and owner projection, UI selects #75 update, #76 status, or #77 delete, then reloads. Require course-management permission before data access; its implementation/claim source remains unresolved.
3. Interpret the direct detail response as a one-item `Page<Course>` because catalog/diagram require the Page wrapper and current API #08 returns CoursePage singleton: `items=[course]`, `page=1`, `size=1`, `total=1`, `total_pages=1`. Mark this pagination construction `DERIVED`; preserve catalog type.
4. Candidate Q1 reads one legacy `courses` row by `c.id=:course_id` and LEFT JOINs legacy `users` on `m.id=c.mentor_id`, selecting only Course fields and UserSummary fields. Use bound course_id and LIMIT 1. No `PUBLISHED` predicate: AC-32 manages courses across lifecycle and #76 changes status. Treat legacy BIGINT mapping as candidate only; do not blend V1-PILOT UUID/course_versions.
5. Map `c.name → Course.title`; preserve `description`, `thumbnail_url`, `status`; convert NUMERIC `price` to decimal string without float; map mentor id/full_name/avatar. Current #08 model serializes optional source-null fields as null. Preserve stored status; enum members/casing remain open. If required mentor or price is absent, propose 500 as current #06/#08 integrity precedent and keep owner confirmation open.
6. Keep `Course.category?` omitted: no approved course-category relation. AC-32 diagram says read “counters,” but the response schema exposes no counter field or definition; do not add fields, `meta` content, COUNT query or data mapping. Raise as group open question.
7. Use exact catalog errors: 401 authentication; 403 Admin/permission denied; 404 absent/invalid course ID (invalid path mapping follows API #08 precedent); 500 safe query/data-mapping failure. No 422. Do not treat API #08's public PUBLISHED visibility as Admin behavior.
8. API is read-only: no DB mutation/transaction; retain `07_table.md` as `N/A — READ-ONLY API`, and create no mutation mapping file. Create 8 template sheets + `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`; no ZIP under Study workflow.
9. Before folder creation, keep the complete matrices below in this worklog. After authoring, verify exact 11-file manifest, template appendices/front matter, direct contract/error set, all Course/Page fields, JSON, Markdown tables/fences, links/anchors, whitespace, fingerprint and scope; no application tests.

### API Requirement Matrix

| API ID | Method/path | Actor/auth | Input | Response/success | Errors | Basis/status |
|---|---|---|---|---|---|---|
| #74 | `GET /api/v1/admin/courses/{course_id}` | Admin; Bearer JWT; AC-32 course-management permission | `path{course_id:int64!}`; no body/query | `ApiEnvelope<Page<Course>>`; 200 `DESIGN_RESOURCE_RETRIEVED` | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR` | Contract DIRECT; singleton Page and query semantics DERIVED; counters unresolved |

### Request Usage Matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Header | Authenticate Bearer/Admin and course-management permission before Q1 | Auth/role DIRECT; permission mechanism `SOURCE_REQUIRED`; current helper is Student-only |
| `course_id` | Required path int64 | Bind to Q1 `c.id`; use returned row as `data.items[0]` | Type DIRECT; invalid string → 404 DERIVED from #08; no extra minimum/range rule |
| Request body | None | None | DIRECT from catalog |
| Query parameters | None | None | DIRECT from catalog |

### Query Matrix

| Query ID | Type | Base/source | Column | Predicate/condition | Purpose/status |
|---|---|---|---|---|---|
| Q1 | SELECT | Legacy candidate `courses AS c` | `c.id` | `c.id = :course_id` | Course identifier; legacy DDL artifact, live schema unknown |
| ↑ | SELECT | Legacy candidate `courses AS c` | `c.name` | Same row | Map to `Course.title`; API #06/#08 source precedent |
| ↑ | SELECT | Legacy candidate `courses AS c` | `c.description` | Same row | Nullable candidate |
| ↑ | SELECT | Legacy candidate `courses AS c` | `c.thumbnail_url` | Same row | Nullable candidate |
| ↑ | SELECT | Legacy candidate `courses AS c` | `c.price` | Same row | NUMERIC → decimal-string; NULL conflicts with required response |
| ↑ | SELECT | Legacy candidate `courses AS c` | `c.status` | Same row; no lifecycle filter | Return any stored status; DERIVED from AC-32 |
| Q1 | LEFT JOIN | Legacy candidate `users AS m` | `m.id` | `m.id = c.mentor_id` | Required UserSummary.id; missing mentor is integrity branch |
| ↑ | SELECT | Legacy candidate `users AS m` | `m.full_name` | Same join | Required UserSummary.full_name |
| ↑ | SELECT | Legacy candidate `users AS m` | `m.avatar_url` | Same join | Optional avatar; preserve null per #08 precedent |
| Q1 | WHERE | Legacy candidate | `c.id` | `c.id = :course_id` | No row → catalog 404; one row → map; primary key prevents multiple rows |
| Q1 | FILTER | N/A | No `c.status='PUBLISHED'` | Admin detail supports management of draft/published/suspended | DERIVED from AC-32/#76; public #08 filter not copied |
| Q-count | N/A | No approved response field | Counters | None | Diagram mentions counters but contract does not define them; `SOURCE_REQUIRED`, no aggregate query |
| Q-category | N/A | No approved course-category relation | Category | None | Optional response category omitted; no guessed JOIN |

### Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | API #74 is read-only | No INSERT/UPDATE/DELETE | `N/A — READ-ONLY API` |

### Response Source Matrix

| Response field | Type | Candidate source/transform | Null/empty rule | Evidence status |
|---|---|---|---|---|
| `HTTPStatus` | integer | Response branch | 200/401/403/404/500 | Direct catalog protocol mapping |
| `success` | boolean | Envelope branch | true on success; false on error | Direct envelope convention |
| `businessCode` | string | Catalog | Exact branch code | DIRECT |
| `message` | string | Safe application message | Exact text unspecified | DERIVED; no DB details |
| `data.items[]` | `Course[]` | Q1 row wrapped as singleton | Exactly one item on 200 | DIRECT Page<Course>; singleton construction DERIVED and precedent #08 |
| `data.items[].id` | int64 | `courses.id` | Required | Legacy candidate |
| `data.items[].title` | string | `courses.name` | Required; alias | #06/#08 source precedent |
| `data.items[].description` | string? | `courses.description` | Null when source NULL | #08 model precedent; null-vs-omit remains contract question |
| `data.items[].thumbnail_url` | uri? | `courses.thumbnail_url` | Null when source NULL | #08 model precedent |
| `data.items[].price` | decimal-string | `courses.price` using decimal formatting | Required; NULL → candidate 500 | #06/#08 source precedent |
| `data.items[].status` | CourseStatus | `courses.status` | Preserve stored value | Candidate; enum/casing open |
| `data.items[].mentor.id` | int64 | `users.id` via `courses.mentor_id` | Required; missing/orphan mentor → candidate 500 | Legacy candidate; DDL nullable discrepancy |
| `data.items[].mentor.full_name` | string | `users.full_name` | Required; missing → candidate 500 | Legacy candidate |
| `data.items[].mentor.avatar_url` | uri? | `users.avatar_url` | Null when source NULL | #08 model precedent |
| `data.items[].category` | Category? | No approved relation/source | Omit because optional | `SOURCE_REQUIRED` for mapping |
| `data.pagination.page` | int32 | Singleton page | `1` | DERIVED |
| `data.pagination.size` | int32 | Singleton page | `1` | DERIVED |
| `data.pagination.total` | int64 | Singleton page | `1` on successful detail | DERIVED |
| `data.pagination.total_pages` | int32 | Singleton page | `1` on successful detail | DERIVED |
| `data.counters` | Not in schema | Diagram phrase only | Not returned | `SOURCE_REQUIRED`; do not invent |
| `meta` | object | Envelope helper | `{}` candidate on success | Current convention |
| `traceId` | uuid | Current trace helper/middleware | Propagated/generated | Current source convention |
| Error `data` | null by guideline | Current helper converts absent/null to `{}` | Endpoint unwired; do not claim current endpoint behavior | `DISCREPANCY` |

## HANDOFF

- Remaining blockers: Admin/course-management guard and claim mapping; live DB/schema selection; counter definitions/response location; legacy mentor nullability; course-category relationship; CourseStatus and optional-field null rules; future error-path allowlist.
- Next owner/action: After #74 DD is verified, continue with API #75 in a separate session. Keep the complete AC-32 #73–#77 macro-review pending until #77 is present.

## CURRENT GROUP REVIEW UPDATE — 2026-10-24

- AC-32 macro-review #73–#77 đã hoàn tất sau khi API #77 có DD. Đã cập nhật open questions, plan và verification report của #74; counter fields/visibility không được tự thêm.
- #74 giữ `Page<Course>` theo catalog; singleton Page là proposal. #77 `DeleteResult` không làm thay đổi wrapper #74. Owner/counters, deleted-target behavior, Admin guard, category/schema/status và middleware/error gaps còn mở.
- Review tĩnh tài liệu-only; không chạy application tests. Next API DD: #78.
