---
task_id: "2026-10-24-create-study-api100-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #100 và macro-review AC-37

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ catalog làm contract; phân biệt `DIRECT`, `DERIVED`, `SOURCE_REQUIRED`; không suy ra schema, enum hoặc identity mapping.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Tách expected/current behavior; route và matching `view.py` mới được tính source-wired; không suy runtime từ DD.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Study DD gồm 8 sheet và 3 report, Markdown-only; candidate ngoài sơ đồ phải ghi là đề xuất và giữ open question.
  - path: `.agents/worklog/2026-10-24/create-study-api99-dd.md`
    - carry_forward: #99 cập nhật moderation state + audit; nhánh delete tách riêng sang #100; macro-review #97–#100 đang chờ #100.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tiếp tục chuỗi một API DD mỗi phiên, tạo DD #100 theo nguồn và rà nhất quán AC-37 với #97–#99. Cập nhật số DD có/chưa có và API có/chưa có cặp route+view source.
- Canonical sources: `docs/lists/list_api.md` row #100 và reusable `DeleteResult`; AC-37 index/activity diagram; `server-study` workflow; registered skill `createDD-markdown` và 8 template sheets.
- Direct contract: `DELETE /api/v1/admin/discussions/{discussion_id}`; Bearer JWT, role Admin; `discussion_id:int64!`; không body/query; `ApiEnvelope<DeleteResult>`; HTTP 200 `DESIGN_RESOURCE_DELETED`; đúng lỗi 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`.
- Direct response schema: `DeleteResult{id:int64, status:"deleted", deleted_at:date-time}`.
- AC-37: sau #99 và quyết định cần xóa, #100 thực hiện soft delete và giữ audit trail.

## CURRENT_BEHAVIOR

- Baseline trước authoring: 103 API ID duy nhất; 99 DD folder (#01–#99), #100–#103 chưa có folder; 12 API có route marker và matching `view.py`, còn 91 API chưa có cặp này.
- Runtime: API #100 không có route/module/test trong `apps/study-server`; trạng thái `UNWIRED / NOT_FOUND`.
- Auth: catalog yêu cầu Admin; current shared auth helper chỉ xác minh Student; không có Admin guard/claim policy đã được source xác nhận.
- Legacy schema: `discussions` có `id BIGSERIAL`, `status VARCHAR(20) DEFAULT 'ACTIVE'`, `updated_at TIMESTAMP`; không có `deleted_at` hoặc audit relation. Pilot `admin_adjustments`/`audit_events` có UUID/versioned identifiers, chưa có mapping tương thích được duyệt với Discussion BIGINT.
- Runnable tests: không có test #100; đây là task tài liệu, không chạy application tests.

## SOURCE_TRACE

```text
Admin Bearer principal -> DELETE discussion_id -> authorize Admin and locate target -> soft-delete logical discussion while preserving audit trail -> ApiEnvelope<DeleteResult> -> AC-37 reloads moderation queue
```

## PLAN BEFORE DD AUTHORING

1. Giữ nguyên contract catalog #100: method/path, Admin Bearer, path int64, không body/query, `ApiEnvelope<DeleteResult>`, status 200 và đúng 5 lỗi catalogued.
2. Dùng AC-37 trực tiếp: #97 queue → #98 detail → quyết định vi phạm → #99 moderation state + audit → quyết định xóa → #100 soft delete + preserve audit trail → reload queue. Không nhập DELETE vào #99.
3. Ghi `DeleteResult` đủ ba field. `id` map theo path là candidate/direct shape; giá trị `status:"deleted"` là literal contract. Nguồn lưu hoặc tạo `deleted_at` chưa được chọn.
4. Legacy `discussions.status` và `updated_at` chỉ là candidate. Có thể nêu `status='DELETED'` cùng `updated_at` làm thời điểm phản hồi như một phương án `DERIVED`, không phải enum/schema được phê duyệt; không thêm cột. Giữ câu hỏi về thời điểm soft-delete và audit persistence.
5. Không hard-delete, cascade replies/reports, hoặc giả định idempotency. Giữ `SOURCE_REQUIRED` cho trạng thái đã xóa, reply/child visibility, report retention, trước đó phải moderate hay không, và tiêu chí 404.
6. Diagram yêu cầu preserve audit trail. Phân biệt giữ lịch sử có sẵn với việc append một delete event mới; actor/resource key, schema, transaction atomicity và audit event cụ thể chưa có mapping được duyệt. Pilot audit UUID schema không tự động map vào legacy Discussion BIGINT.
7. Ghi đủ response/error/request matrices với từng field/condition riêng. Giữ 422 trong contract; trigger và parse behavior chưa được nêu. Không thêm body reason hoặc business code.
8. Tạo Markdown-only folder `apps/study-server/docs/dd/100_admin_discussions_delete/`: đúng 8 sheet template và 3 report (`PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`); không sửa runtime, DDL, catalog, diagram hay client.
9. Static-verify manifest/front matter, template suffix fingerprints, exact endpoint/errors, `DeleteResult` fields, JSON, links/anchors, tables, code fences, whitespace, output fingerprints và `git diff --check`.
10. Sau khi #100 được tạo, macro-review #97–#100: flow/order, reason semantics, response/report gaps, queue visibility sau delete, moderation/delete/audit persistence, authorization và error integration. Cập nhật các report/worklog liên quan nếu có điểm nối cần ghi; không xóa status/open questions hoặc tự reconcile discrepancy.
11. Tính lại inventory từ catalog, DD folder/core sheets, và router + matching view source; báo current source coverage, không gọi là runtime verification.

### API Requirement Matrix

| API ID | Contract item | Giá trị | Basis/status |
|---|---|---|---|
| #100 | Method/path | `DELETE /api/v1/admin/discussions/{discussion_id}` | Catalog; DIRECT |
| #100 | Actor/auth | Admin; Bearer JWT | Catalog; DIRECT; guard/claims chưa có source |
| #100 | Path | `discussion_id:int64!` | Catalog; DIRECT |
| #100 | Body/query | Không khai báo | Catalog; DIRECT |
| #100 | Success | HTTP 200 `DESIGN_RESOURCE_DELETED`; `ApiEnvelope<DeleteResult>` | Catalog; DIRECT |
| #100 | Response data | `id:int64`, `status:"deleted"`, `deleted_at:date-time` | Reusable schema; DIRECT |
| #100 | Errors | 401, 403, 404, 422, 500 với đúng code catalog | Catalog; DIRECT |
| #100 | Mutation | Soft delete + preserve audit trail | AC-37; logical effect DIRECT; physical persistence SOURCE_REQUIRED |

### Request Usage Matrix

| Request item | Source/use | Rule/status |
|---|---|---|
| `Authorization` | Bearer JWT; authenticate Admin principal | DIRECT; Admin claims/guard/policy SOURCE_REQUIRED |
| `discussion_id` | Required int64 path; identify target Discussion | DIRECT; parse/overflow mapping not specified |
| Request body | None declared | DIRECT |
| Query parameters | None declared | DIRECT |
| `reason` | Not part of #100 contract | Do not copy #99 body reason or #97 filter query |

### Query and Mutation Matrix

| Step | Operation | Target/source | Candidate mapping/effect | Evidence status |
|---|---|---|---|---|
| Q1 | SELECT target | Legacy `discussions` | Candidate `id = :discussion_id` | Legacy DDL only; live schema unverified |
| M1 | UPDATE soft-delete marker | Logical Discussion | Candidate existing `status`; token `DELETED` is DERIVED only | AC-37 soft delete DIRECT; physical state/token SOURCE_REQUIRED |
| M1 | UPDATE timestamp | Candidate `discussions.updated_at` | Could supply operation timestamp for response | DERIVED proposal; no dedicated delete timestamp; requires approval |
| M2 | Preserve/append audit | Logical audit trail | Keep existing history; new event behavior and target unresolved | Diagram DIRECT on preservation; append semantics/persistence SOURCE_REQUIRED |
| M3 | DELETE row | Legacy `discussions` | No physical row deletion in soft-delete flow | DIRECT diagram meaning |
| M4 | Cascade child/reports | Child discussion/report sources | No cascade rule inferred | SOURCE_REQUIRED |
| Q2 | Build response | `DeleteResult` | `id`, literal `"deleted"`, deletion time | Shape DIRECT; timestamp source/semantics SOURCE_REQUIRED |

### Response Source Matrix

| Response field | Contract type | Candidate source/transform | Evidence status |
|---|---|---|---|
| `success` | boolean | Envelope | Direct shared convention |
| `businessCode` | string | Catalog literal | DIRECT `DESIGN_RESOURCE_DELETED` |
| `message` | string | Application message | Exact text unspecified |
| `data.id` | int64 | Path `discussion_id` / target row id | Shape DIRECT; source consistency candidate |
| `data.status` | string literal | Constant `deleted` | DIRECT |
| `data.deleted_at` | date-time | Soft-delete operation timestamp | Field/type DIRECT; persistence/source and clock policy SOURCE_REQUIRED; `updated_at` mapping DERIVED only |
| `meta` | object | Envelope | Endpoint-specific metadata not defined |
| `traceId` | uuid | Request trace | Shared envelope convention |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| #100 runtime | No route/module/test | `UNWIRED / NOT_FOUND` | Design-only; no runtime claim |
| Soft-delete marker/time | Legacy status/update fields exist; no approved delete token or dedicated timestamp | `DERIVED / SOURCE_REQUIRED` | Persistence cannot be finalized |
| Audit trail | Diagram requires preserve; legacy schema has no audit relation; pilot audit uses UUID identifiers | `DISCREPANCY / SOURCE_REQUIRED` | Physical audit mapping and append semantics unresolved |
| Admin auth | Catalog says Admin; Study helper enforces Student | `DISCREPANCY / SOURCE_REQUIRED` | No approved authorization implementation |
| Child/report behavior | Diagram does not define cascades or queue visibility | `SOURCE_REQUIRED` | Avoid collateral deletes; result visibility unresolved |
| Error 422 | Catalog includes 422 but no validation rules | `DIRECT / SOURCE_REQUIRED` | Preserve code; trigger/response mapping unresolved |

## CHANGES

- Files changed: this plan-first worklog; then the API #100 DD folder and, if macro-review finds a needed cross-reference, only connected AC-37 DD/report/worklog files.
- CONTEXT_UPDATES: None planned; no context page/registry changes expected.
- Context pages changed: None planned.
- Assumptions: `status='DELETED'` plus `updated_at` is only a DERIVED option; no migration/runtime/schema behavior is approved by this DD.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector/review | Selected #48/#49/#50 docs worklogs read; #99 handoff reviewed | VERIFIED |
| Catalog inventory | 103 unique endpoint IDs; #100 exact contract extracted | VERIFIED_STATIC_ONLY |
| Pre-authoring DD/source inventory | 99 DD folders; #100 absent; 12 route+view pairs | VERIFIED_STATIC_ONLY |
| AC-37 activity diagram | Parsed AC-37 page; #100 soft delete + preserve audit trail confirmed | VERIFIED_STATIC_ONLY |
| Schema/auth/source review | Legacy discussion columns, pilot audit identifiers, router/auth/middleware/test search reviewed | VERIFIED_STATIC_ONLY |
| DD manifest/template/contract checks | 11 Markdown files; 8 template suffixes exact; exact contract/errors and JSON/links/tables/fences/whitespace verified; `git diff --check` clean. | VERIFIED |
| Post-authoring inventory | 100 folders/100 with 8 core sheets; 88 with 3 reports; 3 IDs #101–#103 missing; 12 source route+view pairs, 91 without. | VERIFIED_STATIC_ONLY |
| Macro-review #97–#100 | Flow order consistent; report/projection/auth/audit/delete-visibility gaps recorded across connected DDs. | VERIFIED_STATIC_ONLY |
| Runtime tests | Not run; docs-only | NOT_RUN |

## HANDOFF

- Remaining blockers: Confirm delete status token/time persistence, audit append/retention and actor mapping, Admin auth, already-deleted behavior, child/report handling, and 422 trigger; AC-37 report/projection gaps remain open.
- Next owner/action: Continue with API #101 in the next one-DD session; current inventory is 100 DDs created and 12 source-programmed API IDs.
