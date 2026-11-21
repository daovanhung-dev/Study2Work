---
task_id: "2026-10-24-create-study-api75-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "PARTIAL"
---

# Worklog: Tạo DD Study API #75

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ contract direct, tách `DERIVED` và `SOURCE_REQUIRED`, đọc AC diagram toàn node/edge; không tạo schema/asset giả; Study DD Markdown-only.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Phân biệt AC-22 Content với các module khác; không bịa field/table; dùng ma trận Request/Query/Mutation/Response trước authoring.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Giữ chính xác catalog error set; proposal ngoài nguồn phải gắn `DERIVED`; physical schema/live state và runtime wiring là bằng chứng riêng.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD tiếng Việt cho API #75 sau khi đọc AC-32 và DD #73/#74/#70; hoàn tất plan và các ma trận trước khi tạo folder; kiểm tra tĩnh ngay sau authoring; giữ macro-review AC-32 pending đến khi #77 tồn tại.
- Canonical contract/approved DD: Catalog `docs/lists/list_api.md` row #75 khai báo `PUT /api/v1/admin/courses/{course_id}`, Bearer JWT/role Admin, `path{course_id:int64!}`, `ApiEnvelope<Page<Course>>`, HTTP 200 `DESIGN_RESOURCE_UPDATED`, và đúng errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`. Catalog không khai báo body/query. AC-32 diagram lặp lại contract và node thao tác chỉ ghi `UPDATE course metadata`; #76 là API đổi status riêng. Reusable `Course`, `Page<Course>`, `PageMeta`, `UserSummary` định nghĩa response fields.
- Body proposal: `title`, `description`, `thumbnail_url`, `price` là `DERIVED` từ ý “UPDATE course metadata”, reusable `Course`, legacy `courses` candidate và việc #76 sở hữu status. Đề xuất PUT full replacement với đủ bốn key; `description` và `thumbnail_url` nhận `null` để xóa; không đưa `status`, `mentor`, `category`, counters hoặc `id` vào body. Proposal không phải contract đã phê duyệt; giữ requiredness/null/validation và giá trị field trong `OPEN_QUESTIONS`.

## CURRENT_BEHAVIOR

- Source/config: `app/api/v1.py` không khai báo Admin courses; không có module `api_75_*`/Admin courses hay test API #75. `app/utils/auth.py` chỉ có guard Student và kiểm tra `sub` số dương + `roles`; `DESIGN_CONTRACT_PATHS` trong `app/core/middleware.py` không có path Admin courses. Nếu route được nối mà không cập nhật allowlist, framework 422/500 hiện map sang `VALIDATION_ERROR`/`INTERNAL_SERVER_ERROR`, khác contract #75. `error_response` serializes `data:{}` khi không có data; API guideline mong `data:null`.
- DB/config: Legacy `infra/postgres/study-server/DB.sql` có candidate BIGINT `courses` với `name`, `description`, `thumbnail_url`, `price`, `status`, `mentor_id`, `updated_at`; live schema chưa xác minh. `infra/postgres/02_study_db.sql` là V1-PILOT UUID `courses` + `course_versions`, khác contract BIGINT; không map ngầm. Course response `mentor` là required nhưng legacy `mentor_id` nullable; category relation không source-backed.
- Runnable tests: Không có test API #75; không chạy app tests vì task chỉ tạo tài liệu.
- Runtime wiring: `UNWIRED / NOT_FOUND`; Admin JWT/permission, path, body validation, DB mutation và response projection chưa tồn tại trong current Study runtime.

## SOURCE_TRACE

```text
Admin có Bearer JWT/course-management permission -> PUT path course_id + metadata body -> validate -> UPDATE candidate legacy courses -> đọc Course + UserSummary -> Page<Course> singleton proposal -> ApiEnvelope/DESIGN_RESOURCE_UPDATED -> AC-32 reload course management
```

## PLAN BEFORE DD AUTHORING

1. Giữ nguyên direct catalog contract: method/path/actor/path type/response/success/error set; không thêm query, code lỗi, role, table hay field vào direct contract.
2. Ghi rõ body đang thiếu trong catalog và diagram. Đề xuất bốn metadata field (`title`, `description`, `thumbnail_url`, `price`) theo `DERIVED`; status do #76 quản lý, còn owner/category/counters không được tự thêm.
3. Đề xuất PUT full replacement với đủ key; nullable `description` và `thumbnail_url` dùng `null` để xóa. Requiredness, blank/URI/decimal constraints, null-vs-omit và PUT semantics vẫn là câu hỏi cần xác nhận; legacy length/precision chỉ là candidate.
4. Dùng legacy BIGINT `courses`/`users` làm candidate duy nhất cho mapping đề xuất; không gộp V1-PILOT UUID/versioned `courses`/`course_versions`. Không tuyên bố live schema.
5. Candidate transaction: UPDATE theo `courses.id`, set metadata và `updated_at`; không sửa `mentor_id`/`status`; zero updated rows → candidate 404. Đọc updated course + mentor projection trong cùng transaction; map Page một item theo #74 precedent. Owner join, orphan mentor handling, commit/rollback và page metadata là `DERIVED`.
6. Không thêm audit log: AC-32 gắn “audit log” với status branch #76. Không thêm enrollment/content checks hay delete semantics thuộc #77. Category/counter mapping không có source.
7. Tạo 8 template-backed sheets + `OPEN_QUESTIONS.md`, `PLAN_RESULT.md`, `VERIFICATION_REPORT.md` trong `75_admin_course_update/`; không ZIP hoặc sửa code/catalog/schema/diagram.
8. Static verify exact file set, appendix-template parity, direct contract/errors, response field coverage, JSON, Markdown links/anchors/tables/fences/whitespace và `git diff --check`; ghi macro-review AC-32 pending cho #73–#77.

### API Requirement Matrix

| API | Contract item | Giá trị | Basis/status |
|---|---|---|---|
| #75 | Method/path | `PUT /api/v1/admin/courses/{course_id}` | Catalog + AC-32 node; DIRECT |
| #75 | Actor/auth | Bearer JWT; role Admin; course-management permission precondition | Catalog + AC-32; DIRECT |
| #75 | Path | `course_id:int64!` | Catalog + diagram; DIRECT |
| #75 | Body/query | Catalog/diagram chỉ nêu path; không khai báo body/query | DIRECT absence; metadata body proposal ở dưới là DERIVED |
| #75 | Proposed body | Full replacement `title`, `description`, `thumbnail_url`, `price` | DERIVED từ “UPDATE course metadata” + Course + legacy candidate; needs confirmation |
| #75 | Success | HTTP 200 `DESIGN_RESOURCE_UPDATED`; `ApiEnvelope<Page<Course>>` | Catalog + diagram; DIRECT; singleton cardinality DERIVED theo #74 |
| #75 | Errors | 401/403/404/422/500 với đúng `DESIGN_*` codes tại catalog | Catalog + diagram; DIRECT |
| #75 | Workflow | API #73 list → #74 detail → #75 metadata update → reload; #76 status và #77 delete là nhánh khác | AC-32 index/diagram; DIRECT flow |

### Request Usage Matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| `Authorization` | Header Bearer JWT; xác thực Admin + course-management permission | Principal authorizes mutation | Catalog/AC-32 DIRECT; Study Admin guard/permission claims `SOURCE_REQUIRED` |
| `course_id` | Path required int64 | `courses.id` candidate update predicate; identifies response item | Type DIRECT; legacy BIGINT mapping DERIVED; live schema unresolved |
| `title` | JSON body proposal, required string | `courses.name` candidate | DERIVED; max 200 only legacy DDL candidate; blank rule unresolved |
| `description` | JSON body proposal, required key; string or null | `courses.description` candidate; null clears field | DERIVED; null/omit and length unresolved |
| `thumbnail_url` | JSON body proposal, required key; URI or null | `courses.thumbnail_url` candidate; null clears field | DERIVED; URI rules/allowlist unresolved |
| `price` | JSON body proposal, required decimal-string | `courses.price` candidate; Course output remains decimal-string | DERIVED; precision/scale/nonnegative validation unresolved |
| `status`, `mentor`, `category`, counters | Not included in proposed body | Status belongs to #76; other fields lack update contract/source | Excluded from proposal; confirm boundaries |
| Query parameters | None declared | None | DIRECT from catalog/diagram |

### Query Matrix

| Query | Type | Candidate source | Fields/condition | Purpose/status |
|---|---|---|---|---|
| Q1 | UPDATE | Legacy `courses AS c` | Set `name`, `description`, `thumbnail_url`, `price`, `updated_at`; `c.id = :course_id`; return updated base fields | DERIVED mapping only; physical schema/live DB unresolved |
| Q1 result | Check | UPDATE row count/RETURNING | No updated row | Candidate 404 `DESIGN_RESOURCE_NOT_FOUND`; DERIVED |
| Q2 | SELECT | Legacy `courses AS c` LEFT JOIN `users AS m` | `m.id = c.mentor_id`; course predicate by ID; select Course + UserSummary fields | Candidate post-update response projection; DERIVED; orphan mentor policy unresolved |
| Q3 | N/A | N/A | No category/counter relation or source | Do not query; `SOURCE_REQUIRED` |

### Mutation Matrix

| Target | Column | Input/source | Operation/rule | Status |
|---|---|---|---|---|
| `courses` | `name` | body `title` | Replace with full-request title | DERIVED; legacy physical candidate |
| `courses` | `description` | body `description` | Replace; null clears | DERIVED; legacy physical candidate |
| `courses` | `thumbnail_url` | body `thumbnail_url` | Replace; null clears | DERIVED; legacy physical candidate |
| `courses` | `price` | body `price` | Replace decimal value without float rounding | DERIVED; candidate precision unresolved |
| `courses` | `updated_at` | server timestamp | Set on successful update | DERIVED from legacy column/update intent |
| `courses` | `status`, `mentor_id` | N/A | Do not update in #75 | Status belongs to #76; owner changes lack contract |
| Transaction | Candidate legacy row | Q1 + Q2 | Commit after response projection succeeds; rollback on missing row or DB/mapping failure | DERIVED from API #14 pattern; API #75 source absent |

### Response Source Matrix

| Response field | Contract type | Candidate source/mapping | Evidence/status |
|---|---|---|---|
| `success` | boolean | Envelope success branch | Current helper convention; direct envelope schema |
| `businessCode` | string | Catalog | DIRECT `DESIGN_RESOURCE_UPDATED` |
| `message` | string | Safe application message | Exact text unspecified; DERIVED |
| `data.items[].id` | int64 | `courses.id` | Legacy candidate |
| `data.items[].title` | string | `courses.name` → `title` | Legacy candidate; max/nonnull schema candidate |
| `data.items[].description` | string? | `courses.description` | Nullable candidate; null-vs-omit unresolved |
| `data.items[].thumbnail_url` | uri? | `courses.thumbnail_url` | Nullable candidate; URI validity unresolved |
| `data.items[].price` | decimal-string | `courses.price` | Legacy numeric candidate; nullable DDL discrepancy |
| `data.items[].status` | CourseStatus | `courses.status` unchanged | Metadata update must preserve status; enum/casing unresolved |
| `data.items[].mentor.id` | int64 | joined `users.id` | Required response field; source candidate only |
| `data.items[].mentor.full_name` | string | joined `users.full_name` | Required response field; source candidate only |
| `data.items[].mentor.avatar_url` | uri? | joined `users.avatar_url` | Optional field; null/omit unresolved |
| `data.items[].category` | Category? | No approved course-category relation | Omit proposal; `SOURCE_REQUIRED` |
| `data.pagination.page` | int32 | fixed singleton page | `1`, DERIVED from #74 precedent |
| `data.pagination.size` | int32 | fixed singleton page | `1`, DERIVED from #74 precedent |
| `data.pagination.total` | int64 | one updated course | `1`, DERIVED |
| `data.pagination.total_pages` | int32 | fixed singleton page | `1`, DERIVED |
| `meta` | object | Envelope convention | `{}` candidate; error data `{}` vs guideline `null` discrepancy |
| `traceId` | uuid | Request trace | Current runtime convention; future route must preserve trace |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Request body | Catalog/diagram contain only path; node says `UPDATE course metadata` | `DISCREPANCY / DERIVED` | Four-field body stays proposal, not direct contract. |
| Admin runtime | Router/module/test scan has no Admin course or API #75 source; shared guard is Student-only | `UNWIRED / NOT_FOUND / SOURCE_REQUIRED` | DD is design-only; Admin identity/permission remains unresolved. |
| Middleware error mapping | Admin course path absent from `DESIGN_CONTRACT_PATHS` | `DISCREPANCY / CONDITIONAL_FUTURE_WIRING` | A future route needs path-aware design codes for 422/500. |
| Schema | Legacy BIGINT `courses` candidate vs V1-PILOT UUID `courses` + versioned `course_versions`; live schema unknown | `DISCREPANCY / SOURCE_REQUIRED` | Candidate mutation cannot be called runtime-ready. |
| Course fields | Legacy `mentor_id` and `price` nullable; response requires `mentor` and `price`; no course-category relation | `DISCREPANCY / SOURCE_REQUIRED` | Orphan/NULL handling and category projection remain open. |
| Status/audit | AC-32 assigns status + audit log to separate #76 branch | `DIRECT BOUNDARY` | #75 proposal leaves `status` and audit unchanged. |
| Response cardinality | Direct response is `Page<Course>` for a PUT by ID; #74 proposes singleton page | `DIRECT TYPE / DERIVED CARDINALITY` | Return one updated item proposal; owner confirmation remains open. |

## CHANGES

- Files changed: `apps/study-server/docs/dd/75_admin_course_update/` (8 sheets + 3 reports) and this worklog; complete source trace, plan and matrices were recorded before creating the DD folder.
- CONTEXT_UPDATES: None expected unless current context pages are materially stale.
- Context pages changed: None.
- Assumptions: Preserve pre-existing worktree changes; create only the API #75 Markdown folder after recording the complete plan here.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog preflight | Selected #48/#49/#50; each was read in full. | `VERIFIED` |
| Context routing | Read root/global router, context map, `server-study` entry/index/pages, docs-DD workflow, skill index/manifest and `createDD-markdown` entry. | `VERIFIED_STATIC_ONLY` |
| AC-32/catalog/schema | Read catalog #75/reusable schemas, AC-32 index and all page nodes/edges, legacy course DDL/table guide and V1-PILOT courses/course_versions. | `VERIFIED_STATIC_ONLY` |
| Current source boundary | Inspected API router, current auth helper, middleware/error response, DB helper context; no Admin route/module/test source. | `VERIFIED_STATIC_ONLY` |
| Prior DD patterns | Read relevant #70 update, #73 list, #74 detail sheets/reports and API #14 mutation query/view pattern. | `VERIFIED_STATIC_ONLY` |
| Template gate/archive search | Registry confirms SOURCE_BACKED skill/resource; opened all 8 registered Markdown templates; no ZIP/7Z/RAR/XLSX archive found under Study docs or registered skill resource; Study workflow is Markdown-only. | `VERIFIED_STATIC_ONLY` |
| Static DD verification | Exact 11-file set, 8/8 appendix parity, JSON, local links/anchors, table widths, fences, whitespace, and required contract/response field coverage passed. | `VERIFIED` |
| Output fingerprint | Template manifest `ef4e457d840129719d47303e4cd326ac4637e65f02f27b44ec91f9e925bb402f`; DD payload `23f997be3b1df127bebcdf20843a725b67637b2503a7afd7425045cb04a8bfb6`. | `RECORDED` |
| `git diff --check` | No diagnostics in the current worktree. | `VERIFIED` |
| Agent context validator | `node` is unavailable. Deno fallback with read/env permissions failed repo-wide: db-admin context/source roots are absent and snapshot commit `9a70eb6764a6587093a92d3bd7e4cc0bea1651c4` is unavailable in Git object database. | `FAIL_OUT_OF_SCOPE` |

## HANDOFF

- Remaining blockers: Body fields/PUT semantics/validation, Admin JWT permission policy, chosen/live schema, owner/category/counter projection, NULL serialization, CourseStatus enum, and error envelope policy need confirmation. AC-32 macro-review remains pending through #77.
- Next owner/action: Continue one-API-per-session sequence at #76; review the complete AC-32 group after #77 exists.

## CURRENT GROUP REVIEW UPDATE — 2026-10-24

- AC-32 macro-review #73–#77 đã hoàn tất sau khi API #77 có DD. Đã cập nhật open questions, plan và verification report của #75.
- Giữ #75 metadata-only, #76 status + audit intent, #77 soft-delete-only; response wrapper đúng catalog. Deleted-target behavior, visibility, dependency/delete policy, schema và Admin guard còn mở.
- Review tĩnh tài liệu-only; không chạy application tests. Trạng thái worklog lịch sử `PARTIAL` được giữ nguyên do context-validator blocker đã ghi ở lượt tạo #75. Next API DD: #78.
