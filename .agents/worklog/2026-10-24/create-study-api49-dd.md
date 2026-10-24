---
task_id: "2026-10-24-create-study-api49-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #49

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3` (Node không có trong PATH)
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ contract catalog; không gộp Content với Lecture; ghi candidate `DERIVED`, source/schema gap và Mentor identity rõ ràng; Study chỉ giao Markdown.
  - path: `.agents/worklog/2026-10-23/create-study-api41-dd.md`
    - carry_forward: Không invent table/column/business code; giữ expected/current tách biệt và ma trận theo field.
  - path: `.agents/worklog/2026-10-23/create-study-api42-dd.md`
    - carry_forward: Dùng status `UNWIRED`, `NOT_FOUND`, `SOURCE_REQUIRED`; giữ pagination/response semantics theo catalog.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD Markdown tiếng Việt cho API #49 sau khi lập plan; giữ nguyên catalog contract và AC-22 flow, công khai discrepancy/gap; static verify ngay sau authoring.
- Canonical contract/approved DD: `docs/lists/list_api.md` row #49 và reusable `Content`; `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md` AC-22; `AC_03_MENTOR_TEACHING.drawio` page AC22; registered `createDD-markdown` skill; Study `docs-dd` workflow Markdown-only.

## CURRENT_BEHAVIOR

- Source/config: API #49 không có route, module `view.py`, hoặc test tương ứng trong Study source. Router hiện có route API ID #01–#09, #12–#14. AC-22 diễn tả GET rồi đọc `sections/lessons/content`; reusable schema trả `ApiEnvelope<Content>` với 8 thuộc tính top-level nhưng không định nghĩa cấu trúc `payload` hay enum members. Current `error_response` defaults absent `data` to `{}`; middleware allowlist `DESIGN_CONTRACT_PATHS` chưa có path #49, nên future wiring không cập nhật allowlist sẽ dùng fallback `VALIDATION_ERROR`/`INTERNAL_SERVER_ERROR`. Đây là conditional future discrepancy, không phải runtime behavior API #49 hiện tại.
- Runnable tests: Không chạy; task tạo tài liệu. Không có test source API #49.
- Runtime wiring: `UNWIRED / NOT_FOUND`. Mentor guard và identity mapping chưa có trong Study runtime.

## SOURCE_TRACE

```text
Mentor Bearer principal -> GET course content bằng path course_id -> kiểm tra quyền quản lý course -> đọc cây sections/lessons/content -> map response Content -> 200 RESOURCE_RETRIEVED hoặc catalog errors -> UI chọn CRUD/publish action tiếp theo
```

## PLAN BEFORE DD AUTHORING

1. Giữ nguyên `GET /api/v1/mentor/courses/{course_id}/content`, Bearer JWT, role Mentor, `course_id:int64!`, không body/query, `ApiEnvelope<Content>`, HTTP 200 và đúng 4 error codes 401/403/404/500.
2. Theo AC-22 chỉ mô tả GET đọc course content trước nhánh CRUD. Không trộn API #49 với POST/PUT/DELETE/PATCH #50–#53; không tự đổi `Content` thành `Page<Content>` hoặc cấu trúc cây lồng nhau.
3. Ghi discrepancy: tên/purpose là “Lấy cây nội dung course” và diagram đọc `sections/lessons/content`, nhưng response contract chỉ là một `Content`; chưa có quy tắc empty tree, root, children, pagination hay wrapper.
4. Candidate Q1 kiểm tra course tồn tại và direct-owner theo legacy `courses.id/mentor_id`, theo precedent #46/#47; đánh dấu `DERIVED`, không tuyên bố hỗ trợ assigned course. Mentor principal→numeric ID chưa có source.
5. Không thiết kế query content tree: legacy DB guide/ERD có 16 bảng nhưng không có `Content`, `sections` hoặc generic parent-content table. V1-PILOT có `chapters`, `lessons`, `content_blocks` với UUID và mô hình/version khác; không map ngầm sang contract BIGINT.
6. Tạo Request Usage Matrix, Query Matrix (Q1 candidate + Q2 SOURCE_REQUIRED), Mutation Matrix read-only/N/A và Response Source Matrix cho mọi envelope/Content field. `payload`, Content enums, status/parent mapping và tree cardinality giữ `SOURCE_REQUIRED`.
7. Giữ đúng set lỗi. 404 course/tree-empty meaning, 403 access mapping và malformed path behavior cần xác nhận; không tự thêm 422/409/503.
8. Tạo 8 sheets và 3 reports dưới `apps/study-server/docs/dd/49_mentor_content_list/`; appendix của 8 sheet phải khớp template registry. Không tạo ZIP, schema, code, test hay catalog edits.
9. Static verify exact contract/error set, diagram trace, all response fields, schema gap, JSON examples, template appendix/front matter, links, tables, whitespace and exact 11-file set. Ghi AC-22 macro-review pending cho nhóm #49–#53 đến khi các DD khác tồn tại.

### API Requirement Matrix

| API ID | Method/path | Actor/auth | Input | Response/success | Errors | Basis/status |
|---|---|---|---|---|---|---|
| #49 | `GET /api/v1/mentor/courses/{course_id}/content` | Bearer JWT; Mentor | `course_id:int64!`; no body/query | `ApiEnvelope<Content>`; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR` | Catalog + AC-22; DIRECT contract, data-access semantics partially unresolved |

### Request Usage Matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Header; authenticate Bearer and Mentor role | Principal for course-management permission | Contract DIRECT; Mentor guard and principal ID mapping `SOURCE_REQUIRED` |
| `course_id` | Required path int64 | Candidate Q1 course lookup; intended scope for Q2 content read | Type DIRECT; physical schema/live mapping unresolved |
| Body/query | None | None | DIRECT from catalog |

### Query Matrix

| Query | Type | Candidate source | Columns/predicate | Purpose/status |
|---|---|---|---|---|
| Q1 | SELECT | Legacy `courses AS c` | `c.id`, `c.mentor_id`; `c.id = :course_id` | Candidate existence/direct-owner check, `DERIVED`; identity/assignment/live schema unresolved |
| Q2 | SELECT | No approved content-tree relation | Base table, joins, fields, filters and order not established | `SOURCE_REQUIRED`; do not write SQL against guessed tables |

### Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | API #49 is read-only | No INSERT/UPDATE/DELETE | `N/A — READ-ONLY API` |

### Response Source Matrix

| Field | Contract type | Candidate source/transform | Gap/status |
|---|---|---|---|
| `success` | boolean | Envelope branch | Envelope convention; exact Study helper serialization is current-source evidence |
| `businessCode` | string | Catalog literal | DIRECT: `DESIGN_RESOURCE_RETRIEVED` |
| `message` | string | Application message | Exact text unspecified; `DERIVED` |
| `data.id` | int64 | No approved generic Content table | `SOURCE_REQUIRED` |
| `data.course_id` | int64 | Path or stored row | Whether echoing path or reading per row unresolved; `SOURCE_REQUIRED` |
| `data.content_type` | ContentType | No approved source/enum list | `SOURCE_REQUIRED` |
| `data.title` | string | No approved generic Content source | `SOURCE_REQUIRED` |
| `data.payload` | object | No approved structure/source | `SOURCE_REQUIRED`; do not invent keys |
| `data.status` | ContentStatus | No approved source/enum list | `SOURCE_REQUIRED` |
| `data.parent_id` | int64? | No generic parent relation | `SOURCE_REQUIRED` |
| `data.order` | int32 | No approved generic ordering column | `SOURCE_REQUIRED` |
| `meta` | object | Envelope convention | No pagination contract; empty/null policy needs Study helper alignment |
| `traceId` | uuid | Request trace | Envelope convention; runtime route absent |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #49 runtime | No route/module/test source | `UNWIRED / NOT_FOUND` | DD is design-only. |
| Error dispatch | `app/core/responses.py` uses `{}` for absent error data; `middleware.py` only uses design codes for paths in `DESIGN_CONTRACT_PATHS`, which excludes API #49 | `DISCREPANCY / CONDITIONAL_FUTURE_WIRING` | Preserve catalog codes and settle malformed-path behavior when implementing the route. |
| Tree vs response shape | AC-22 purpose/diagram says course content tree; catalog says singular `Content`, with optional `parent_id` but no children collection | `DISCREPANCY / SOURCE_REQUIRED` | Do not change response into a collection or guess root semantics. |
| Content persistence | Legacy DB guide/ERD has no Content/sections table; pilot `chapters`/`lessons`/`content_blocks` uses UUID and versioned structure | `DISCREPANCY / SOURCE_REQUIRED` | Cannot define content query/mapping until schema owner selects model. |
| Mentor access | AC-22 requires permission to manage course; legacy `courses.mentor_id` is only direct-owner candidate; assignment and identity binding absent | `DERIVED / SOURCE_REQUIRED` | Candidate does not claim assigned-course support. |
| Content enums/payload | `ContentType`, `ContentStatus`, and `payload` object members are not defined | `SOURCE_REQUIRED` | Full response mapping and validation cannot be finalized. |

## CHANGES

- Files changed: `apps/study-server/docs/dd/49_mentor_content_list/` (8 sheets + 3 reports); this worklog; `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md` refreshed to the post-#49 count.
- CONTEXT_UPDATES: None planned; no runtime/schema/catalog/diagram change.
- Context pages changed: None planned.
- Assumptions: Simple direct-owner proposal is explicitly `DERIVED`; unresolved behavior remains open, not silently chosen.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector/review | Selected/read #48, #41, #42; no shortage. | `VERIFIED` |
| Catalog/diagram | Read API #49 row, Content reusable schema, AC-22 index and page nodes/edges; confirmed GET reads tree before CRUD branch. | `VERIFIED_STATIC_ONLY` |
| DB artifacts | Read legacy DB table guide/ERD evidence and pilot DDL for chapters/lessons/content_blocks; schemas are distinct and live schema not verified. | `VERIFIED_STATIC_ONLY` |
| Current source | Router and module inventory has no API #49 route/view/test. | `VERIFIED_STATIC_ONLY` |
| Template/skill | Registry wires `createDD-markdown` to `server-study`; eight registered Markdown templates available; Study workflow forbids ZIP output. | `VERIFIED_STATIC_ONLY` |
| Template/authoring | Eight registered Markdown templates used; appendix suffixes match exactly; Study workflow has no ZIP output. | `VERIFIED` |
| Static Markdown/contract validation | 11-file set, front matter, exact catalog/error set, all Content fields, JSON, local links, table widths, code fences, whitespace and `git diff --check` passed. | `VERIFIED` |
| Current response/error source | Read runtime page plus `responses.py` and `middleware.py`; absent error data becomes `{}` and API #49 is outside design-code allowlist. | `VERIFIED_STATIC_ONLY` |
| Runtime tests | Not run; docs-only and API #49 remains unwired. | `NOT_RUN` |
| AC-22/AC-33 macro-review #49–#53 | Linked DDs reviewed; open questions retained. | `VERIFIED_WITH_OPEN_QUESTIONS` |

## HANDOFF

- Remaining blockers: API #49 content schema/response shape/enum definitions, Mentor principal binding, and conditional middleware path mapping remain open for implementation approval.
- Next owner/action: API #49 DD and the #49–#53 AC-22/AC-33 macro-review are statically verified with open questions. Continue the one-API-per-session sequence at API #54.

## GROUP_MACRO_REVIEW

- Status: VERIFIED_WITH_OPEN_QUESTIONS after API #53 was created.
- Cross-API findings: #49 tree cardinality/visibility remains unresolved; #50/#51 PENDING_REVIEW and tree placement are DERIVED; #52 publication transitions remain DERIVED and AC-33 APPROVED/PUBLISHED is ambiguous; #53 proposes direct-child blocking, no cascade, unpublish-first for PUBLISHED, and history-preserving soft delete.
- Shared blockers: generic Content/version schema, payload/enums/readiness, Mentor principal/assignment, dependency coverage, soft-delete/audit storage, and filtering deleted items from active tree/review queue.
- Application tests were not run; this records document-level macro-review only.
