---
task_id: "2026-10-24-create-study-api77-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #77

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3` (`node` không có trong PATH)
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ contract trực tiếp; tách expected/current; không suy diễn từ DDL legacy thành runtime; giữ source gaps rõ.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Đọc AC liên quan để giữ ranh giới flow; không invent table/field/error code; Study DD chỉ là Markdown.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Phân loại status/persistence proposal là `DERIVED`; giữ exact catalog error set và không tuyên bố source/runtime khi route vắng mặt.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD tiếng Việt cho API catalog #77 sau khi lập plan, đọc toàn bộ diagram AC-32 và DD liên quan; kiểm tra DD ngay sau authoring; sau #77 thực hiện macro-review nhóm AC-32 #73–#77.
- Canonical contract: `DELETE /api/v1/admin/courses/{course_id}`, Bearer JWT, role Admin, `path{course_id:int64!}`, không body/query, `ApiEnvelope<DeleteResult>`, HTTP 200 `DESIGN_RESOURCE_DELETED`; lỗi đúng 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`.
- Reusable `DeleteResult`: `id:int64`, `status:"deleted"`, `deleted_at:date-time`.
- AC-32: Admin cần quyền course management; nhánh #77 soft delete theo policy rồi reload management. Catalog title nói conditional và kiểm tra enrollment/content; diagram không nêu dependency predicates, block rule hoặc response của nhánh bị chặn.

## CURRENT_BEHAVIOR

- Source/config: `app/api/v1.py` không có route Admin course; không tìm thấy module/test `api_77`. `app/utils/auth.py` chỉ có Student current-user guard. `DESIGN_CONTRACT_PATHS` không có Admin course paths và middleware so sánh `request.url.path` bằng exact membership. Current `error_response()` đổi data vắng mặt thành `{}`, trong khi API guideline yêu cầu `null` cho error data.
- Database artifacts: Legacy `courses` dùng BIGSERIAL và không có deletion timestamp/marker; `enrollments.course_id` và `lessons.course_id` là FK candidates, cùng một số bảng course-linked khác. Legacy generic Content relation không có. V1-PILOT dùng UUID `courses`, `archived_at`, versioned `course_versions` và FK `ON DELETE RESTRICT`; không map `archived_at` sang `DeleteResult.deleted_at` hoặc ghép với API int64. Live schema chưa xác minh.
- Runnable tests: Không có test API #77; không chạy tests vì task chỉ tạo tài liệu.
- Runtime wiring: `UNWIRED / NOT_FOUND`; không tuyên bố Admin auth, dependency policy, soft-delete persistence hoặc response chạy được.

## SOURCE_TRACE

```text
Admin Bearer principal -> Admin/course-management authorization -> validate course_id -> Q1 existence -> Q2 enrollment/content eligibility -> approved logical soft-delete (physical marker SOURCE_REQUIRED) -> DeleteResult -> AC-32 reload
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #77 runtime | Router/module/focused test không có trong current Study source. | `UNWIRED / NOT_FOUND` | DD chỉ là design; không có runtime claim. |
| Delete policy | AC-32 diagram nói soft delete theo policy; catalog title nói conditional và check enrollment/content, nhưng không định nghĩa rule. | `DIRECT INTENT / SOURCE_REQUIRED` | Không hard-delete/cascade; đề xuất block khi có dependency là `DERIVED`, cần owner duyệt. |
| Physical marker/timestamp | `DeleteResult.deleted_at` là field direct; legacy courses không có delete marker; V1-PILOT có UUID `archived_at` với nghĩa archive. | `DISCREPANCY / SOURCE_REQUIRED` | Không invent `deleted_at`/status column hoặc map archive sang delete; success mapping implementation chưa đủ nguồn. |
| Enrollment/content dependencies | Legacy enrollments/lessons có course FK; generic Content relation không có; pilot version model khác. | `SOURCE_REQUIRED` | Không chọn đầy đủ relations/predicates/active statuses; candidate dependency check không phải SQL được duyệt. |
| Admin authorization | AC-32 yêu cầu Admin/course-management permission; current shared helper chỉ cho Student. | `SOURCE_REQUIRED` | Không dùng Student guard hoặc tự tạo claim/permission mapping. |
| Error integration | Catalog có 422; dependency-block meaning chưa xác định. Middleware path allowlist và error data shape chưa đồng bộ. | `DISCREPANCY / DERIVED` | Giữ đúng codes; malformed path, dependency message và future dynamic path mapping cần xác nhận. |
| AC-32 consistency | #73 list, #74 detail, #75 metadata, #76 status/audit, #77 soft delete có các wrappers/side effects khác nhau. | `MACRO_REVIEW_REQUIRED` | Sau khi tạo #77 cần rà visibility, mutation boundaries, status/audit, deletion result và shared security/schema/error gaps. |

## PLAN BEFORE DD AUTHORING

1. Giữ chính xác DELETE path, Bearer/Admin, `course_id:int64!`, không body/query, `ApiEnvelope<DeleteResult>`, HTTP 200 và exact 401/403/404/422/500 codes; không thêm status/business code.
2. Dùng AC-32 sequence #73 list → #74 detail/owner/counters → decision → #75 metadata hoặc #76 status+audit hoặc #77 soft-delete policy → reload. #77 không cập nhật metadata/status và không chép audit side effect của #76.
3. Giữ soft-delete là intent trực tiếp, không chọn hard-delete, cascade, anonymization hoặc physical field. Dùng `DeleteResult.status="deleted"` trực tiếp; map `id` từ target khi mutation thành công; `deleted_at` cần physical marker/timestamp được duyệt.
4. Request chỉ có path ID. Q1 candidate kiểm tra course existence theo legacy `courses.id`; query chỉ là schema candidate. Q2 tách enrollment check khỏi content check; `enrollments.course_id` và `lessons.course_id` chỉ là legacy candidates, không chứng minh full policy hoặc live FK.
5. Đề xuất đơn giản `DERIVED`: nếu dependency được policy xác nhận là blocker, trả 422; nếu policy cho phép và physical soft-delete mapping đã được chọn, đánh dấu xóa logic. Condition, dependency set và blocked behavior vẫn là open questions; không sinh `reason`/business code mới.
6. Đề xuất dependency read + soft-delete mutation nằm trong một transaction để tránh race, nhưng không chỉ định lock/isolation/SQL khi relation, field và transaction owner chưa có source. Không thay đổi child rows hoặc lịch sử.
7. Đọc API #72 DELETE làm precedent cho `DeleteResult`/policy gaps, nhưng không copy user-specific identity, PII, anonymization hoặc dependency behavior. Rà #73–#76 để giữ `#75` metadata-only, `#76` status+audit, `#77` delete-only.
8. Tạo 8 template sheets và 3 reports tại `apps/study-server/docs/dd/77_admin_course_delete/`; giữ appendix baseline byte-match; không tạo ZIP, runtime/schema/catalog/diagram edits.
9. Các Requirement, Request Usage, Query, Mutation và Response Source matrices dưới đây được ghi trước khi tạo DD folder. Sau authoring kiểm tra exact package, contract/error codes, JSON, matrices, Markdown tables/fences, relative links/anchors, whitespace và fingerprint; sau đó macro-review #73–#77 và cập nhật reports/worklogs liên quan.

### API Requirement Matrix

| API ID | Contract item | Giá trị | Basis/status |
|---|---|---|---|
| #77 | Method/path | `DELETE /api/v1/admin/courses/{course_id}` | Catalog + AC-32; DIRECT |
| #77 | Actor/auth | Bearer JWT; Admin/course-management permission | Catalog/AC-32; DIRECT requirement, guard SOURCE_REQUIRED |
| #77 | Path | `course_id:int64!` | Catalog; DIRECT |
| #77 | Body/query | Không khai báo | Catalog; DIRECT |
| #77 | Delete intent | Conditional; kiểm tra enrollment/content; soft delete theo policy | Catalog title + AC-32; direct intent, exact rule SOURCE_REQUIRED |
| #77 | Success | HTTP 200 `DESIGN_RESOURCE_DELETED`; `ApiEnvelope<DeleteResult>` | Catalog; DIRECT |
| #77 | Success data | `id:int64`, `status:"deleted"`, `deleted_at:date-time` | Reusable schema; DIRECT fields, physical timestamp SOURCE_REQUIRED |
| #77 | Errors | 401/403/404/422/500 với đúng catalog codes | Catalog; DIRECT |

### Request Usage Matrix

| Request item | Source/use | Query/mutation/response use | Rule/status |
|---|---|---|---|
| Authorization | Bearer JWT; Admin/course-management authorization | Principal authorized before Q1; actor only if audit is separately approved | DIRECT requirement; claims/guard/audit SOURCE_REQUIRED |
| `course_id` | Required path int64 | Q1 existence; Q2 dependency scope; soft-delete target; `data.id` | DIRECT type; physical relation is legacy candidate only |
| Request body | None | None | DIRECT absence from catalog |
| Query parameters | None | None | DIRECT absence from catalog |
| `Idempotency-Key` | Not declared | No runtime use until endpoint retryability is approved | Guideline applies to retryable mutations; endpoint semantics SOURCE_REQUIRED |

### Query Matrix

| Query | Type | Candidate source | Columns/condition | Purpose/status |
|---|---|---|---|---|
| Q1 | SELECT | Legacy `courses AS c` | `c.id`; `c.id = :course_id` | Candidate existence; legacy DDL only, live schema unknown. |
| Q2a | EXISTS/SELECT | Legacy `enrollments AS e` | Candidate `e.course_id = :course_id`; status predicate unspecified | Enrollment dependency gate; exact blocking statuses/source need confirmation. |
| Q2b | SELECT | No approved generic Content relation | Physical relation/columns/conditions not established; legacy `lessons.course_id` is only a possible content candidate | `SOURCE_REQUIRED`; do not present as complete content check or executable query. |

### Mutation Matrix

| Operation | Target | Condition | Fields/effect | Status |
|---|---|---|---|---|
| M1 | Logical course soft-delete | Q1 target exists; approved dependency policy permits delete | Mark course deleted without deleting children/history; physical target/marker/timestamp unspecified | Soft-delete intent DIRECT; physical mutation SOURCE_REQUIRED |
| Hard delete/cascade | N/A | No source authorizes it | Do not delete course or child relations physically | Excluded; not inferred from HTTP method/FK artifacts |
| Transaction | Caller/use case | Dependency reads and M1 must not race if policy/mapping is approved | Commit marker + success source atomically; rollback on failure | Atomic check/mutation DERIVED; owner/isolation unresolved |

### Response Source Matrix

| Response field | Type | Candidate source/mapping | Null/omit rule and status |
|---|---|---|---|
| `success` | boolean | Envelope branch | true on success, false on error; envelope convention |
| `businessCode` | string | Catalog | `DESIGN_RESOURCE_DELETED` or exact catalog error code; DIRECT |
| `message` | string | Safe application message | Exact text unspecified; DERIVED |
| `data.id` | int64 | `course_id` / successfully marked course ID | Required; physical target binding candidate |
| `data.status` | literal `"deleted"` | Reusable DeleteResult | Constant; DIRECT |
| `data.deleted_at` | date-time | Approved soft-delete timestamp source | Required by schema; physical source absent; SOURCE_REQUIRED |
| `data.reason` | Not in DeleteResult | No mapping | Do not add field or use optional unrelated `reason` schema |
| `meta` | object | Envelope | `{}` candidate; no pagination |
| `traceId` | uuid | Shared trace middleware | Propagate/generate per current convention |
| Error `data` | null per API guideline | Current helper defaults to `{}` | `DISCREPANCY`; endpoint is unwired |

## CHANGES

- Files changed: `apps/study-server/docs/dd/77_admin_course_delete/` (8 template sheets + 3 reports), AC-32 review updates for DD #73–#76, five related worklogs, inventory worklog, and this worklog.
- CONTEXT_UPDATES: None.
- Context pages changed: None.
- Assumptions: Soft-delete is direct intent; dependency block behavior and atomic read/mutation are DERIVED proposals; physical schema remains SOURCE_REQUIRED.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector/review | Deno selector chọn #48/#49/#50; cả ba đã đọc đầy đủ. | `VERIFIED` |
| Catalog/diagram/source/prior DD | API #77 row/schema, AC-32 index và toàn bộ page nodes/edges; current route/auth/middleware/response/schema artifacts; #72 và nhóm #73–#76 đã rà. | `VERIFIED_STATIC_ONLY` |
| Plan-before-authoring | Requirement, Request Usage, Query, Mutation, Response Source matrices được ghi trước khi tạo DD folder. | `VERIFIED` |
| Static DD validation | Exact 11-file package; template suffix 8/8; exact catalog business-code set; DeleteResult fields; 2 JSON; 28 core tables; 7 fences; 36 local links/19 anchors; newline/whitespace checks passed. | `VERIFIED_STATIC_ONLY` |
| Application tests | Không chạy; docs-only. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: Dependency policy, Content relation, physical soft-delete marker/timestamp, Admin guard, live schema, idempotency/repeat-delete semantics và dynamic middleware mapping.
- Next owner/action: Continue with API #78. AC-32 #73–#77 macro-review is complete at document level; owner/schema/runtime questions remain open.

## CURRENT RECHECK AFTER API #77 — 2026-10-24

- DD #77: exact 11-file Markdown package; 8/8 template appendix suffixes byte-match; all core sheets have front matter. Static checks confirmed direct catalog code set (success + five errors), all three DeleteResult fields, 2 valid JSON examples, 28 core-sheet tables, 7 fences, 36 resolvable local links/19 anchors, final newline and no trailing whitespace. Fingerprints are in `VERIFICATION_REPORT.md`.
- AC-32 #73–#77: macro-review complete at document level. Functional boundaries and response wrapper types stay aligned with catalog; category/counters, Admin guard, CourseStatus casing, schema generation, audit persistence, soft-delete/deleted-target visibility, dependency policy, timestamp and error middleware remain unresolved. Reports and worklogs #73–#76 were updated.
- Inventory: 103 catalog IDs; 77 DD folders (all eight core sheets); 65 full 11-file packages; 26 missing DDs (#78–#103). Route + matching view source exists for 12 IDs (#01–#09, #12–#14); 91 do not. This is source wiring, not runtime-pass evidence.
- Application tests: `NOT_RUN`; task scope is documentation and inventory. `git diff --check` produced no diagnostics; custom whitespace checks covered untracked DD files.
- Next API DD: #78.
