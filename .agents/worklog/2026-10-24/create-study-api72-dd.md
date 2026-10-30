---
task_id: "2026-10-24-create-study-api72-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #72

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` (Node không có trong PATH)
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ chính xác contract catalog, đánh dấu candidate `DERIVED`, không bịa nguồn `assets`/schema và rà nhất quán nhóm sau khi đủ DD.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Giữ khác biệt `DIRECT`/`DERIVED`/`SOURCE_REQUIRED`, không trộn schema legacy BIGINT với pilot UUID; Study DD chỉ xuất Markdown.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Giữ body/schema chưa có làm gap; proposal không biến thành implementation contract; số route+view chỉ là source evidence.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD tiếng Việt cho API #72; lập plan và các ma trận trước khi tạo folder DD; đọc kỹ toàn flow AC-31; kiểm tra ngay sau authoring; sau khi #72 tồn tại, macro-review toàn nhóm #68–#72.
- Canonical contract/approved DD: `docs/lists/list_api.md` API #72: `DELETE /api/v1/admin/users/{user_id}`, Bearer JWT role Admin, `path{user_id:int64!}`, `ApiEnvelope<DeleteResult>`, HTTP 200 `DESIGN_RESOURCE_DELETED`, lỗi 401/403/404/422/500 đúng mã catalog. `DeleteResult` gồm `id:int64`, `status:"deleted"`, `deleted_at:date-time`. AC-31 yêu cầu Admin có quyền user management, kiểm tra ràng buộc, soft delete/anonymize theo policy, rồi reload list/detail.

## CURRENT_BEHAVIOR

- Source/config: Không có route API #72 trong `apps/study-server/app/api/v1.py`, không có module `api_72_*`/`view.py` hoặc test API #72. Shared auth guard hiện chỉ cấp Student; middleware `DESIGN_CONTRACT_PATHS` chưa có `/api/v1/admin/users/{user_id}`. `error_response` hiện biến error `data` vắng mặt thành `{}`; guideline của scope yêu cầu `null`.
- Schema artifacts: `infra/postgres/study-server/DB.sql` có legacy BIGINT `users` với `status`, `created_at`, `updated_at` nhưng không có `deleted_at`, `anonymized_at` hoặc cột/record xóa; có nhiều quan hệ user như courses, enrollments, progress, quiz attempts, submissions, discussions, notifications, payments và refresh tokens. Chỉ refresh_tokens khai báo `ON DELETE CASCADE`; đây là DDL artifact, không phải live constraint evidence. `infra/postgres/02_study_db.sql` là mô hình V1-PILOT UUID khác, gồm `identity_projections.account_status` lifecycle và `learner_profiles.deleted_at`; không được ghép ngầm với `users` BIGINT. Live schema chưa xác minh.
- Runnable tests: Không có test API #72; không chạy application tests cho task docs-only.
- Runtime wiring: API #72 `UNWIRED / NOT_FOUND`; không được coi DD là bằng chứng triển khai.

## SOURCE_TRACE

```text
Admin Bearer principal -> xác thực/ủy quyền user-management -> nhận user_id -> kiểm tra tồn tại và các ràng buộc theo policy đã duyệt -> áp dụng soft-delete/anonymization đã duyệt (không hard-delete) -> map DeleteResult {id, status:"deleted", deleted_at} -> 200 DESIGN_RESOURCE_DELETED hoặc exact catalog error -> reload list/detail
```

Đây là flow kỳ vọng theo catalog/diagram. Runtime API hiện chưa tồn tại; bảng/cột, dependency query, retention policy, transaction và nguồn `deleted_at` chưa được chỉ định.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #72 runtime | Router/module/test/Admin guard không có trong current source. | `UNWIRED / NOT_FOUND` | DD không khẳng định runtime. |
| Delete policy | Diagram nói soft delete/anonymize theo policy nhưng không chọn một policy. | `DIRECT INTENT / SOURCE_REQUIRED DETAIL` | Không tạo physical DELETE hoặc tự chọn cột/trạng thái. |
| Legacy persistence | Legacy `users` không có deletion timestamp/state; nhiều bảng liên quan tham chiếu `users`. | `SCHEMA GAP / LIVE NOT_VERIFIED` | Không thể viết mutation SQL hoặc khẳng định constraint/cascade runtime. |
| Pilot model | UUID `identity_projections`/`learner_profiles` có deletion lifecycle khác legacy `users` int64. | `DISCREPANCY` | Không map ngầm pilot columns sang API #72. |
| DeleteResult.deleted_at | Catalog yêu cầu datetime, nhưng legacy users không có nguồn timestamp xóa. | `SOURCE_REQUIRED` | Success projection chưa implementation-ready. |
| Dependency-to-error mapping | Catalog có 422, diagram bảo kiểm tra ràng buộc nhưng không chỉ định điều kiện/mapping. | `SOURCE_REQUIRED` | Giữ code 422 trong catalog; không gán policy constraint cụ thể. |
| Admin/error integration | Chưa có Admin guard hoặc middleware allowlist path; error helper và guideline khác nhau về `data`. | `CONDITIONAL FUTURE DISCREPANCY` | Chỉ mô tả gap hạ tầng, không gán runtime behavior cho #72. |

## PLAN BEFORE DD AUTHORING

1. Giữ nguyên method/path, Bearer JWT role Admin, `user_id:int64!`, không body/query, response `ApiEnvelope<DeleteResult>`, HTTP 200 và đúng tập lỗi catalog 401/403/404/422/500.
2. Theo toàn flow AC-31: #68 list → chọn user → #69 detail → quyết định Update/Status/Delete → #72 DELETE → soft delete/anonymize theo policy → reload list/detail. Không thay đổi semantics của #68–#71.
3. Luồng candidate bắt đầu bằng xác thực/ủy quyền Admin trước database. Có thể tra user theo `id` như candidate legacy read để phân biệt no-row; đánh dấu nguồn legacy là design artifact, không phải SQL đã duyệt.
4. Mô tả dependency review ở mức logic theo AC-31. Dẫn các FK user-linked trong legacy DDL như danh sách ứng viên cần policy owner xem xét; không tự đặt điều kiện “có quan hệ thì chặn”, cascade, anonymization field map hoặc transaction.
5. Không hard-delete `users` hay bảng con. Ghi soft-delete/anonymization là intent trực tiếp nhưng physical target/policy chưa có nguồn. `07_table.md` sẽ nêu `SOURCE_REQUIRED` cho physical mapping, không bịa table/column. DDL `refresh_tokens ... ON DELETE CASCADE` không được diễn giải thành yêu cầu xóa vật lý.
6. Map mọi field `DeleteResult`: `id` từ user được yêu cầu nếu xác nhận mutation thành công; `status` literal `"deleted"` theo schema; `deleted_at` cần nguồn timestamp từ policy/schema đã duyệt và phải để `SOURCE_REQUIRED`. Không trả PII trong response.
7. Giữ code/error set chính xác. 404 cho target không tồn tại là candidate mapping; 422 invalid request/policy validation chỉ dùng trong giới hạn code catalog và không định nghĩa constraint cụ thể; 401/403 auth; 500 internal. Không thêm 409.
8. Tạo đúng 8 sheet template và 3 report trong `72_admin_user_delete/`. Mỗi file tiếng Việt; appendix template giữ nguyên. Không tạo ZIP, code, schema, catalog hoặc diagram.
9. Static-check manifest 11 file, exact catalog/errors/response fields, JSON, relative links/anchors, tables/fences/whitespace, policy/schema gaps và source absence; không chạy application tests.
10. Sau khi #72 tạo xong, macro-review #68–#72 về list/detail projection, update/status boundaries, delete lifecycle/visibility, Admin auth, PII/audit, dependencies, `DeleteResult` và error envelope. Cập nhật các open questions, plan results, verification reports và inventory; giữ các quyết định thiếu nguồn ở trạng thái mở.

### API Requirement Matrix

| API ID | Contract item | Giá trị | Basis/status |
|---|---|---|---|
| #72 | Method/path | `DELETE /api/v1/admin/users/{user_id}` | Catalog + AC-31; DIRECT |
| #72 | Actor/auth | Bearer JWT; role Admin, quyền user-management theo AC-31 precondition | Catalog/diagram; DIRECT |
| #72 | Path | `user_id:int64!` | Catalog + diagram; DIRECT |
| #72 | Body/query | Không khai báo | Catalog; DIRECT |
| #72 | Logical action | Soft delete/anonymize theo policy; kiểm tra ràng buộc | AC-31 diagram; DIRECT intent, policy detail SOURCE_REQUIRED |
| #72 | Success | HTTP 200 `DESIGN_RESOURCE_DELETED`; `ApiEnvelope<DeleteResult>` | Catalog + diagram; DIRECT |
| #72 | `DeleteResult` | `id:int64`, `status:"deleted"`, `deleted_at:date-time` | Reusable catalog schema; DIRECT |
| #72 | Error | 401 `DESIGN_AUTHENTICATION_REQUIRED` | Catalog; DIRECT |
| #72 | Error | 403 `DESIGN_ACCESS_DENIED` | Catalog; DIRECT |
| #72 | Error | 404 `DESIGN_RESOURCE_NOT_FOUND` | Catalog; DIRECT code/status; no-row branch DERIVED |
| #72 | Error | 422 `DESIGN_VALIDATION_ERROR` | Catalog; DIRECT code/status; exact policy/input conditions SOURCE_REQUIRED |
| #72 | Error | 500 `DESIGN_INTERNAL_ERROR` | Catalog; DIRECT |

### Request Usage Matrix

| Request item | Source/use | Mapping/query use | Rule/status |
|---|---|---|---|
| Authorization | Header Bearer JWT; verify Admin and user-management permission before lookup | Principal for authorized deletion scope | Role/permission DIRECT; guard/claim/scope implementation SOURCE_REQUIRED |
| `user_id` | Required path int64 | Q1 candidate lookup; response `data.id` after approved successful action | Type DIRECT; malformed/int64 parser behavior to follow 422 catalog, exact mapping not implemented |
| Request body | None declared | None | DIRECT |
| Query parameters | None declared | None | DIRECT |

### Query Matrix

| Query ID | Type | Candidate source | Columns/condition | Purpose/status |
|---|---|---|---|---|
| Q1 | SELECT | Legacy `users` artifact | `id` and only minimum fields needed by approved policy; `id=:user_id` | Existence candidate; no password/PII needed; live schema unverified |
| Q2 | Dependency/policy evaluation | No approved runtime relation set | No SQL/table list authorized by current contract | Diagram requires check, but exact dependencies, branches and result mapping are `SOURCE_REQUIRED`; legacy FK list is contextual only |
| Q3 | N/A until policy selected | No approved mutation target | No DELETE/UPDATE SQL specified | Physical soft-delete/anonymization schema absent; no invented query |

### Mutation Matrix

| Mutation ID | Operation | Target | Condition | Fields | Transaction/failure | Status |
|---|---|---|---|---|---|---|
| M1 | Logical soft-delete or anonymize; never hard-delete by candidate | Physical target `SOURCE_REQUIRED` | Approved policy and dependency rules only | No column/value specified | Transaction and rollback ownership `SOURCE_REQUIRED` | Intent DIRECT; implementation DERIVED only at logical level |

### Response Source Matrix

| Response field | Type | Candidate source/transform | Null/empty rule | Evidence status |
|---|---|---|---|---|
| `success` | boolean | Envelope outcome | Required | DIRECT envelope |
| `businessCode` | string | Catalog code | Exact branch code | DIRECT |
| `message` | string | Safe localized message | Exact text unspecified | DERIVED |
| `data.id` | int64 | Existing target ID; path is candidate echo only after success | Required | Type DIRECT; target/source mapping needs approved policy |
| `data.status` | literal `"deleted"` | Catalog constant | Exact lowercase literal | DIRECT |
| `data.deleted_at` | date-time | Approved persisted deletion/anonymization timestamp | Required | Contract DIRECT; source `SOURCE_REQUIRED` |
| `meta` | object | Envelope convention | `{}` candidate; error guideline expects null data | Convention candidate / discrepancy |
| `traceId` | uuid | Request trace | Required | Current middleware convention; endpoint unwired |

## CHANGES

- Files changed: `apps/study-server/docs/dd/72_admin_user_delete/` (11 Markdown files); AC-31 macro-review notes in DD #68–#71; `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md`; this worklog.
- CONTEXT_UPDATES: None; this is documentation only.
- Context pages changed: None.
- Assumptions: Preserve all existing user modifications; no hard delete, cascade, constraint policy, anonymization map, DB field or business code is invented.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector/read | Deno selector chose #48/#49/#50; all three were read fully before deep inspection. | `VERIFIED` |
| Catalog/AC-31 | API #72 exact row, `DeleteResult`, AC-31 index and every AC31 node/edge inspected. | `VERIFIED_STATIC_ONLY` |
| Prior DDs | #68–#71 overview, request/response/mapping/error/open questions/plan/report reviewed for group boundaries. | `VERIFIED_STATIC_ONLY` |
| Current source/schema | API #72 route/module/test absent; Student-only guard; middleware path absent; legacy/pilot DDL and user dependencies inspected; live schema not verified. | `VERIFIED_STATIC_ONLY` |
| Template/skill | Registry wires `createDD-markdown` to `server-study`; 8 template sheets present; Study workflow prohibits new ZIP. | `VERIFIED_STATIC_ONLY` |
| Plan-before-authoring | Requirement, Request Usage, Query, Mutation and Response Source matrices are recorded above before DD folder creation. | `VERIFIED` |
| DD package/static checks | Exact 11-file manifest; all 8 Excel appendix suffixes byte-match templates; contract fields/codes, JSON, relative links/anchors, fences, whitespace and required status markers checked with no errors. | `VERIFIED_STATIC_ONLY` |
| AC-31 macro-review | APIs #68–#72 reviewed document-level; reports updated in all five DDs; unresolved policy/schema/security gaps are retained. | `VERIFIED_WITH_OPEN_QUESTIONS` |
| Inventory | 103 catalog APIs; 72 core DD folders (60 full 11-file packs); 31 without DD; 12 route-plus-view source pairs and 91 without. | `VERIFIED_STATIC_ONLY` |
| Git whitespace | `git diff --check` completed cleanly. | `VERIFIED` |
| Runtime tests | Not run; docs-only task. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: Physical soft-delete/anonymization policy/schema, dependency conditions and error mapping, timestamp source, Admin guard, live schema and error envelope convention.
- Next owner/action: Continue the one-API-per-session DD goal with API #73. AC-31 #68–#72 document-level review is complete; implementation/schema policy questions remain for owners to resolve before coding.
