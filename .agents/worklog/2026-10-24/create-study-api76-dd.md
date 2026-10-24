---
task_id: "2026-10-24-create-study-api76-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #76

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ DIRECT contract; đánh dấu suy luận `DERIVED`; không trộn schema candidate/live DB; đối chiếu toàn bộ nodes/edges AC trước khi chốt flow.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Không tạo query/table/field/business code thiếu nguồn; giữ `UNWIRED`, `SOURCE_REQUIRED`, error allowlist discrepancy; Study chỉ giao Markdown.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Giữ nguyên catalog error set; status transition, enum và persistence phải phân loại riêng; chưa đủ nguồn thì để open question.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD tiếng Việt cho API #76; ghi plan và 4 ma trận trước khi tạo DD folder; kiểm tra DD ngay sau authoring. AC-32 #73–#77 macro-review tiếp tục pending đến khi #77 tồn tại.
- Canonical direct contract: `PATCH /api/v1/admin/courses/{course_id}` với hậu tố `/status`; Bearer JWT, role Admin; `path{course_id:int64!}`; catalog không khai báo body/query; `ApiEnvelope<Page<Course>>`; HTTP 200 `DESIGN_RESOURCE_UPDATED`; errors đúng 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`.
- AC-32 direct behavior: Actor Admin có quyền course management; nhánh STATUS gọi API #76, sau đó backend “UPDATE status + audit log” rồi UI reload course management. Catalog mô tả các trạng thái draft/published/suspended.
- Canonical sources: `docs/lists/list_api.md` row #76/reusable schemas; `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md` AC-32; page AC-32 trong `AC_04_ADMIN_MANAGEMENT.drawio`; current Study source/middleware/auth; `DB_UNICA_TABLES.md`, legacy Study DDL và V1-PILOT DDL; DD #71/#73/#74/#75.

## CURRENT_BEHAVIOR

- Source/config: API #76 chưa có route/module/focused test. `app/api/v1.py` hiện chỉ đăng ký API IDs #01–#09 và #12–#14; không có Admin course path. `app/utils/auth.py` chỉ có guard Student; `DESIGN_CONTRACT_PATHS` chưa có Admin course paths; middleware so sánh `request.url.path` bằng exact membership. Nếu wire route mà không cập nhật dynamic path matching, request validation/internal exception có thể rơi về `VALIDATION_ERROR`/`INTERNAL_SERVER_ERROR`, lệch catalog.
- Database artifacts: Legacy `infra/postgres/study-server/DB.sql` có BIGINT `courses.id`, `status VARCHAR(20) DEFAULT 'DRAFT'`, `updated_at`; không có bảng audit. ERD guide mô tả 16 bảng nghiệp vụ và đánh dấu query design-only; live schema chưa xác minh. V1-PILOT `infra/postgres/02_study_db.sql` dùng UUID `courses`, `course_versions.status` enum `DRAFT/PUBLISHED/SUPERSEDED/DISCARDED`, không có `SUSPENDED`; pilot `audit_events.resource_id` và `actor_subject_id` là UUID. Không ghép hai schema; `audit_events` pilot không chứng minh tương thích với API int64 hay đã được deploy.
- Related source behavior: public API #06 chỉ lấy `courses.status = 'PUBLISHED'`; API #08/#09 cũng là public published-only theo scope context. Vì vậy status change có thể ảnh hưởng public visibility, nhưng enrollment/content access policy chưa được mô tả.
- Runnable tests: Không chạy app tests; docs-only. Không có focused test API #76.
- Runtime wiring: `UNWIRED / NOT_FOUND`; không tuyên bố Admin auth, status update hoặc audit log đã chạy.

## SOURCE_TRACE

```text
Admin Bearer principal + course-management permission
-> validate course_id và target status
-> khóa/đọc course hiện hữu (candidate legacy BIGINT)
-> UPDATE status + updated_at candidate
-> ghi một logical audit event (diagram bắt buộc; physical schema chưa tương thích/được chọn)
-> đọc Course + UserSummary projection
-> trả ApiEnvelope<Page<Course>> singleton (DERIVED theo #74/#75)
-> UI reload course management
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Request body | Catalog/diagram chỉ nêu path; thao tác status cần target value | `DERIVED / SOURCE_REQUIRED` | Đề xuất body `{status:CourseStatus!}`; owner cần duyệt. |
| Status members/casing | Catalog ghi draft/published/suspended; legacy/API #06 lưu/so sánh `DRAFT`/`PUBLISHED`; reusable CourseStatus không liệt kê enum; pilot enum thiếu SUSPENDED | `DISCREPANCY` | Đề xuất uppercase `DRAFT/PUBLISHED/SUSPENDED` để khớp legacy/current #06; chưa coi là contract. |
| Transition/readiness policy | Diagram chỉ có “UPDATE status + audit log”; không có transition matrix/readiness gate | `SOURCE_REQUIRED` | Đề xuất set trực tiếp một target hợp lệ; không tự thêm điều kiện duyệt hoặc transition code. |
| Audit persistence | AC-32 yêu cầu audit; legacy DDL/ERD không có audit relation; pilot audit_events dùng UUID actor/resource trong khi API IDs là int64 | `SOURCE_REQUIRED` | Chỉ đặc tả logical event; không bịa SQL/table/ID conversion. Chốt cùng transaction là proposal. |
| Schema selection | Legacy BIGINT model và V1-PILOT UUID/versioned model không tương đương; live schema chưa xác minh | `DISCREPANCY / NOT_VERIFIED` | Query/update chỉ là candidate; không tuyên bố triển khai. |
| Admin authorization | Catalog/AC yêu cầu Admin/course-management permission; current helper là Student-only | `SOURCE_REQUIRED` | Không tái sử dụng Student guard; policy/claim source chưa có. |
| Response cardinality | Catalog trả Page<Course> dù endpoint thao tác một course | `DERIVED` | Dùng Page singleton 1/1/1/1 nhất quán với #74/#75, chờ xác nhận wrapper. |
| Error envelope | Guidelines yêu cầu error `data:null`; current `error_response` mặc định `{}` | `DISCREPANCY` | Ghi rõ expected/current; không đổi helper trong docs task. |
| Error-code middleware | `DESIGN_CONTRACT_PATHS` thiếu Admin course path | `CONDITIONAL_FUTURE_DISCREPANCY` | Khi wire #76, thêm route-aware/dynamic path coverage (exact placeholder string không match numeric course_id) để giữ mã DESIGN_* catalog. |

## PLAN BEFORE DD AUTHORING

1. Giữ chính xác method/path, Bearer JWT/Admin, path `course_id:int64!`, direct no-query, response, success và năm error codes. Không thêm `409`, `503`, field output counter hoặc auth mechanism.
2. Đọc toàn bộ AC-32 graph. Diagram flow là list → detail + owner/counters → decision → update metadata (#75), status (#76) hoặc delete (#77) → reload. Nhánh #76 chỉ yêu cầu update status + audit log.
3. Lấy body `status` làm proposal `DERIVED` vì direct contract bỏ body nhưng operation không thể chọn target nếu không có input. Dùng target semantics draft/published/suspended từ catalog; minh họa uppercase `DRAFT/PUBLISHED/SUSPENDED` theo legacy status và API #06 nhưng đánh dấu casing chưa duyệt. Không đặt transition/readiness policy ngoài nguồn.
4. Thiết kế mutation candidate trên legacy BIGINT: Q1 đọc/lock `courses` theo id và status; M1 set status và `updated_at`; M2 ghi một logical audit event; Q2 lấy Course/UserSummary để trả response. Chỉ Q1/M1/Q2 có legacy columns candidate; không viết SQL cho audit event khi schema vật lý chưa tương thích. Gộp status/audit trong một transaction là `DERIVED` để tránh trạng thái đổi mà thiếu audit.
5. Giữ hai schema tách biệt: legacy `courses.status` VARCHAR/DRAFT; V1-PILOT versioned course có UUID, status ở `course_versions`, không có SUSPENDED; `audit_events` pilot UUID. Không map UUID sang int64 hoặc nhận pilot là live schema.
6. Public visibility proposal: `PUBLISHED` tiếp tục được đọc bởi các API public hiện lọc published; `DRAFT`/`SUSPENDED` không qua filter đó. Không tự quyết enrollment access, content readiness, hay dependency/soft-delete policy của #77.
7. Response dùng `ApiEnvelope<Page<Course>>`; candidate page có một Course và pagination `{page:1,size:1,total:1,total_pages:1}` theo #74/#75. Map đầy đủ Course và UserSummary; `category` optional được omit khi thiếu relation. Ghi field null/orphan gaps theo DD nhóm.
8. Tạo 8 template sheet + `OPEN_QUESTIONS.md`, `PLAN_RESULT.md`, `VERIFICATION_REPORT.md` tại `apps/study-server/docs/dd/76_admin_course_status/`. Giữ appendix suffix 8/8 byte-match template. Không tạo ZIP, sửa source, schema, catalog hay diagram.
9. Static-verify exact 11-file set, direct contract/error set, request/response fields, SQL placeholder consistency, JSON examples, template appendix, front matter, links/anchors, tables, code fences, whitespace, matrix cross-coverage, and `git diff --check`. Không chạy app tests. AC-32 #73–#77 macro-review chờ #77.

### API Requirement Matrix

| API ID | Contract item | Giá trị | Basis/status |
|---|---|---|---|
| #76 | Method/path | `PATCH /api/v1/admin/courses/{course_id}/status` | Catalog + AC-32; DIRECT |
| #76 | Actor/auth | Bearer JWT; role Admin | Catalog + AC-32; DIRECT; guard/policy source absent |
| #76 | Authorization precondition | Admin có quyền course management | AC-32 index; DIRECT requirement |
| #76 | Path | `course_id:int64!` | Catalog; DIRECT |
| #76 | Query | Không khai báo | Catalog; DIRECT |
| #76 | Body | Chưa khai báo trong catalog/diagram | DIRECT gap; body proposal nằm ở DERIVED matrix dưới |
| #76 | Target statuses | draft / published / suspended | Catalog label; DIRECT semantics, serialization/casing unresolved |
| #76 | Success | HTTP 200 `DESIGN_RESOURCE_UPDATED`; `ApiEnvelope<Page<Course>>` | Catalog; DIRECT |
| #76 | Error | 401 `DESIGN_AUTHENTICATION_REQUIRED` | Catalog; DIRECT |
| #76 | Error | 403 `DESIGN_ACCESS_DENIED` | Catalog; DIRECT |
| #76 | Error | 404 `DESIGN_RESOURCE_NOT_FOUND` | Catalog; DIRECT |
| #76 | Error | 422 `DESIGN_VALIDATION_ERROR` | Catalog; DIRECT |
| #76 | Error | 500 `DESIGN_INTERNAL_ERROR` | Catalog; DIRECT |
| #76 | Mutation intent | Update status + audit log, then reload management | AC-32 diagram; DIRECT intent, storage/details unresolved |

### Request Usage Matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Header; authenticate Bearer and Admin role/permission before course lookup | Principal supplies actor for authorization and logical audit event | Auth DIRECT; claims, permission source, actor ID format `SOURCE_REQUIRED` |
| Idempotency-Key | Optional only if contract owner classifies this endpoint as retryable | Prevent duplicate status/audit effects on retry | API guideline applies to retryable mutations; catalog omits header; semantics SOURCE_REQUIRED |
| `course_id` | Required path int64 | Q1 `courses.id`; used by M1 and Q2 | Type DIRECT; positive range/malformed mapping unspecified |
| Body `status` | Proposed required `CourseStatus` target | M1 target `courses.status`; returned in `data.items[0].status` | `DERIVED`; catalog/diagram omit body; proposed values uppercase `DRAFT/PUBLISHED/SUSPENDED`; exact casing/enum needs approval |
| Request body shape | Proposed `{"status":"PUBLISHED"}` | Validation before mutation | `DERIVED`; only one target field; no metadata/owner fields |
| Query parameters | None | None | DIRECT from catalog |

### Query Matrix

| Step | Type | Candidate source/target | Fields/condition | Purpose/status |
|---|---|---|---|---|
| Q1 | SELECT FOR UPDATE | Legacy `courses AS c` | `c.id`, `c.status`; `c.id = :course_id` | Read current status and lock target row; `DERIVED` candidate; legacy DDL only |
| M1 | UPDATE | Legacy `courses AS c` | Set `status = :status`, `updated_at = :updated_at`; filter `id = :course_id` | Status mutation; `DERIVED` candidate; exact timestamp/transaction owner unresolved |
| M2 | INSERT logical audit event | Physical target `SOURCE_REQUIRED` | One event after status update; actor/resource/old-new change fields not finalized | Direct diagram intent; legacy audit relation absent; pilot `audit_events` incompatible UUID model; no SQL invented |
| Q2 | SELECT + LEFT JOIN | Legacy `courses AS c`, `users AS m` | Course projection by `c.id`; `m.id = c.mentor_id` | Build updated Course/UserSummary Page singleton; candidate follows #74/#75; mentor relation may be NULL |
| Tx | BEGIN/COMMIT/ROLLBACK | Study transaction | Q1 → M1 → M2 → Q2 → commit; rollback on failure | Atomic update+audit proposal; Study DB helper does not own commit |

### Mutation Matrix

| Operation | Target | Condition | Fields/effect | Status |
|---|---|---|---|---|
| M1 UPDATE | Legacy `courses` candidate | `id = :course_id` | `status = :status`; candidate `updated_at = :updated_at`; preserve metadata, owner and category | `DERIVED`; legacy table/columns exist in artifact; live schema unknown |
| M2 INSERT | Audit event logical effect | Only after successful status update | Record course status change and Admin actor; exact old/new payload, action name, physical table and key mapping unresolved | Diagram intent DIRECT; persistence `SOURCE_REQUIRED` |
| Other relation changes | N/A | No source in #76 flow | No enrollment/content mutation or soft delete | N/A; #77 owns deletion policy |
| Transaction | Caller/use case | Include update + audit write | Commit only when both required effects succeed | `DERIVED`; owner/transaction runtime absent |

### Response Source Matrix

| Response field | Contract type | Candidate source/mapping | Null/omit rule and status |
|---|---|---|---|
| `success` | boolean | Envelope branch | true success / false error; envelope convention |
| `businessCode` | string | Catalog | Exact branch code; DIRECT |
| `message` | string | Application safe text | Exact wording unspecified; DERIVED |
| `data.items` | `Course[]` | Q2 updated course | Exactly one item on success; singleton Page DERIVED |
| `data.items[0].id` | int64 | `courses.id` | Direct candidate; legacy BIGSERIAL |
| `data.items[0].title` | string | `courses.name → title` | Candidate mapping per #06/#74/#75 |
| `data.items[0].description` | string? | `courses.description` | Optional; source NULL serialization follows #74/#75 candidate, needs confirmation |
| `data.items[0].thumbnail_url` | uri? | `courses.thumbnail_url` | Optional; source NULL serialization unresolved |
| `data.items[0].price` | decimal-string | `courses.price` | Exact decimal serialization; legacy permits NULL despite required contract |
| `data.items[0].status` | `CourseStatus` | Updated `courses.status` | Return target/current stored representation; enum members/casing unresolved |
| `data.items[0].mentor.id` | int64 | `users.id` via `courses.mentor_id` | Required UserSummary; missing/orphan mentor policy open |
| `data.items[0].mentor.full_name` | string | `users.full_name` | Required; candidate source |
| `data.items[0].mentor.avatar_url` | uri? | `users.avatar_url` | Optional; null-versus-omit unresolved |
| `data.items[0].category` | `Category?` | No approved course-category relation | Omit candidate; `SOURCE_REQUIRED` |
| `data.pagination.page` | int32 | Singleton page | Fixed `1`; DERIVED according to #74/#75 |
| `data.pagination.size` | int32 | Singleton page | Fixed `1`; DERIVED |
| `data.pagination.total` | int64 | Updated course exists | Fixed `1`; DERIVED |
| `data.pagination.total_pages` | int32 | Singleton page | Fixed `1`; DERIVED |
| `data` on error | null by API guideline | Current `error_response` defaults to `{}` | `DISCREPANCY`; helper behavior is not endpoint runtime |
| `meta` | object | Envelope | `{}` candidate; counters not in Course/Page schema |
| `traceId` | uuid | Request trace | Current shared trace convention; propagate/generate |

## SOURCE_COVERAGE

| Source | Coverage/result |
|---|---|
| Root/scope context | `AGENTS.md`, `.agents/AGENTS.md`, `context-map.md`, server-study entry/index/workflow and API route context loaded. |
| Worklogs | Selector returned #48/#49/#50; all read in full. |
| Registry/skill/template | Manifest confirms `createDD-markdown` and `docs-dd` wired; template folder contains 8 Markdown sheets; appendix suffixes in #75 were compared byte-for-byte and match 8/8. No in-scope zip/xlsx archives found. |
| Catalog | API #76 row, ApiEnvelope/Page/PageMeta/Course/UserSummary definitions read; CourseStatus members absent. |
| AC-32 | Index pre/postconditions and all nodes/edges on diagram page parsed. |
| Related DD | #71 status body/enum precedent; #73 list and open questions; #74 detail/singleton Page; #75 metadata-only boundary and open questions read. |
| Source/runtime | `v1.py`, Student-only auth helper, middleware DESIGN_CONTRACT_PATHS, response helper and API guidelines checked. |
| DB/schema | ERD table guide; legacy `DB.sql`; V1-PILOT `02_study_db.sql`, including course version status and audit_events fields checked. |

## CHANGES

- Files changed: `apps/study-server/docs/dd/76_admin_course_status/` (8 sheets + 3 reports) and this worklog. The API inventory worklog was refreshed for the user count request.
- CONTEXT_UPDATES: None; no server-wide convention/runtime changes.
- Context pages changed: None.
- Assumptions: Body `{status}` and uppercase candidate values are explicitly `DERIVED`; physical audit persistence remains `SOURCE_REQUIRED`; no live schema/runtime claims.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog preflight | Deno selector returned #48/#49/#50; all three read in full. | `VERIFIED` |
| AC-32 graph | Parsed all nodes and edges; #76 STATUS branch updates status + audit and reloads. | `VERIFIED_STATIC_ONLY` |
| Catalog/source/schema | Direct row and schema, absence of route/module/test, current auth/middleware, legacy/pilot schema split checked. | `VERIFIED_STATIC_ONLY` |
| Plan-before-authoring | Requirement, Request Usage, Query, Mutation, Response Source matrices now recorded before DD folder creation. | `VERIFIED` |
| Package/template | Exact 11-file package; all eight appendix suffixes byte-match registered templates. | `VERIFIED_STATIC_ONLY` |
| Static contract/Markdown | Catalog code set exact; response fields covered; 2 JSON examples, 32 tables, 8 code fences, 26 local links/10 anchors, final newlines and whitespace checked. | `VERIFIED_STATIC_ONLY` |
| Fingerprints | Template and DD payload SHA-256 recorded in `VERIFICATION_REPORT.md`; output excludes that report. | `VERIFIED` |
| AC-32 macro-review | #73–#77 group review awaits API #77 DD. | `PENDING` |
| Application tests | Not run; docs-only. | `NOT_RUN` |
| Context validator | No context page or registry changed. | `NOT_APPLICABLE` |

## HANDOFF

- Remaining blockers: Admin guard/permission, request body/status enum/casing, allowed transition/readiness policy, physical audit mapping/transaction support, live schema, course category and required mentor/price null policy, response singleton/error-envelope confirmation.
- Next owner/action: Continue with API #77 DD, then complete the document-level AC-32 macro-review across #73–#77. API #76 remains Draft — Needs Confirmation until body/status enum and audit/schema questions are resolved.

## CURRENT GROUP REVIEW UPDATE — 2026-10-24

- AC-32 macro-review #73–#77 đã hoàn tất sau khi API #77 có DD. Đã cập nhật open questions, plan và verification report của #76.
- Giữ ranh giới #75 metadata-only, #76 status + audit intent theo diagram, #77 soft-delete theo policy; không suy audit hoặc hard-delete/cascade cho #77. Status casing/visibility, physical audit, deletion policy, Admin guard, live schema và error middleware còn mở.
- Review tĩnh tài liệu-only; không chạy application tests. Next API DD: #78.
