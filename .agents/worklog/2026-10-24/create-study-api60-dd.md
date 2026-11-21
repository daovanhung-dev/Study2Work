---
task_id: "2026-10-24-create-study-api60-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #60

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ đúng catalog error set; không biến candidate schema/authorization thành runtime fact; read-only DD tách khỏi implementation.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Bảo toàn response contract, giữ `SOURCE_REQUIRED` cho phần schema chưa có; ghi conditional middleware discrepancy thay vì coi là runtime behavior.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Chỉ dùng flow/schema evidence được diagram và DDL hỗ trợ; ghi rõ mọi trạng thái/placement/order suy diễn; không tạo physical Content model.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD tiếng Việt cho API #60, lập và lưu plan trước authoring; bám AC-24; giữ mạch #58 list → #59 detail → #60 reply → #61 resolve; static verify ngay sau authoring.
- Canonical contract/approved DD: `docs/lists/list_api.md` row #60; reusable `SupportRequest`, `SupportMessage`, `UserSummary`, `UploadAsset`; AC-24 index/diagram; API #34 upload DD, API #35 `file refs`, API #47 `asset refs`; prior AC-24 DD #58/#59; registered `createDD-markdown`; Study workflow Markdown-only.

## CURRENT_BEHAVIOR

- Source/config: Catalog #60 là `POST /api/v1/mentor/support/{request_id}/reply`, Bearer JWT / Mentor, `request_id:int64!`, body `message:string!` và `attachment refs:string!`, success HTTP 200 `DESIGN_RESOURCE_UPDATED`, response `ApiEnvelope<SupportRequest>`, errors đúng 401/403/404/422/500. AC-24 node #60 dẫn tới `INSERT SupportMessage`; sau đó decision “Vấn đề đã được xử lý?” đi riêng tới #61 resolve hoặc giữ OPEN. Không có route/module/test #58–#60 trong Study runtime; #60 path chưa có trong `DESIGN_CONTRACT_PATHS`.
- Upload reference: AC-17/AC-21 gọi API #34 upload trước API downstream. API #34 DD chưa xác định ID, metadata persistence, URL/purpose/ownership; #35 giữ `file refs` key/encoding unresolved; #47 dùng `asset_refs` chỉ như DERIVED wire-key candidate và giữ chuỗi opaque.
- Schema: Legacy DB.sql/ERD không có support message table. V1-PILOT `support_messages` có UUID id/ticket_id/author_subject_id, body, UUID[] attachment_file_ids, `is_internal` default false và `sent_at`; candidate này không khớp request/API int64 trực tiếp, không chứng minh live schema.
- Runnable tests: Không chạy; docs-only, API #60 chưa wired.
- Runtime wiring: `UNWIRED / NOT_FOUND`; Mentor guard/principal mapping, attachment resolver và support schema chưa được xác nhận. Current DB helper không commit; transaction thuộc caller.

## SOURCE_TRACE

```text
Mentor Bearer principal -> POST reply theo request_id + message/attachment refs -> kiểm tra request thuộc phạm vi và refs hợp lệ -> INSERT SupportMessage -> reload SupportRequest/thread gồm message mới -> commit theo candidate transaction -> trả 200 DESIGN_RESOURCE_UPDATED -> AC-24 decision riêng: #61 resolve hoặc giữ OPEN
```

## PLAN BEFORE DD AUTHORING

1. Giữ đúng catalog: `POST /api/v1/mentor/support/{request_id}/reply`; Bearer JWT/Mentor; `request_id:int64!`; required `message:string!` và `attachment refs:string!`; no query; HTTP 200 `DESIGN_RESOURCE_UPDATED`; `ApiEnvelope<SupportRequest>`; exact errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`.
2. Bám diagram AC-24: #58 mở list, #59 đọc detail/thread, #60 chỉ INSERT SupportMessage, rồi quyết định riêng #61 resolve hoặc NO giữ OPEN. Không tự UPDATE ticket status tại #60; không gửi notification hoặc ghi Object Storage nếu diagram không nêu.
3. Tạo request matrix, giữ “attachment refs” đúng catalog label. Đề xuất `attachment_refs` làm wire key và chuỗi comma-separated các `UploadAsset.id` int64 từ #34; `""` biểu thị không có file. Đây là giải pháp đơn giản `DERIVED`, cần chốt chung với #35 `file refs` và #47 `asset refs`; không coi là approved. API #34 chưa có ID/metadata registry và pilot UUID `file_objects` không map trực tiếp, nên lookup/ownership vẫn `SOURCE_REQUIRED`.
4. Candidate Q1 kiểm tra SupportRequest tồn tại và scope Mentor nhưng không viết SQL vật lý: int64 request ID không khớp pilot UUID ticket ID; principal/assignment binding chưa có. Candidate Q2 kiểm tra refs của upload thuộc đúng caller/purpose/request scope, nhưng không có asset registry được duyệt để query.
5. Candidate M1 là logical `INSERT SupportMessage`; pilot columns id, ticket_id, author_subject_id, author_type, body, attachment_file_ids, is_internal, sent_at chỉ liệt kê như candidate. Không cast IDs. `author_type=STAFF` cho Mentor và `is_internal=false` cho learner-visible reply là simple `DERIVED` proposals, không được trình bày là approved mapping.
6. Ghi validation proposal đơn giản `message` không rỗng sau trim → 422, nhưng không đặt min/max/length; đánh dấu `DERIVED / needs confirmation`. `attachment refs` bắt buộc là string theo catalog; empty/no-attachment semantics và duplicate refs còn open.
7. Candidate transaction: sau scope/input/ref checks, insert rồi reload SupportRequest để response có message mới; chỉ commit sau khi mapping response hoàn tất, lỗi thì rollback. Đây là proposal theo caller-owned transaction convention hiện tại, chưa phải runtime/API guarantee. Request status giữ nguyên; #61 là API duy nhất resolve.
8. Tạo `60_mentor_support_reply/PLAN_RESULT.md` làm DD artifact đầu tiên sau plan này; sau đó 8 registered sheets + `OPEN_QUESTIONS.md` + `VERIFICATION_REPORT.md`, tổng 11 Markdown. Dùng exact template appendix tails. Vì diagram yêu cầu INSERT và V1-PILOT có table candidate, `07_table.md` sẽ ghi candidate `support_messages` columns với trạng thái từng field, ID/type/schema mismatch và approval/live status rõ ràng; không trình bày candidate như runtime mapping. Không tạo ZIP.
9. Static verify exact contract/error set, response field coverage cho SupportRequest và nested UploadAsset, matrix tách expected/candidate, JSON, exact manifest/frontmatter/appendices, links/anchors/table/fences/whitespace và `git diff --check`. Runtime tests `NOT_RUN`. Để macro-review AC-24 #58–#61 pending cho tới khi #61 có DD.

### API Requirement Matrix

| API ID | Contract item | Giá trị | Basis/status |
|---|---|---|---|
| #60 | Method/path | `POST /api/v1/mentor/support/{request_id}/reply` | Catalog + AC-24; DIRECT |
| #60 | Actor/auth | Bearer JWT; role Mentor | Catalog + AC-24; DIRECT |
| #60 | Path | `request_id:int64!` | Catalog; DIRECT |
| #60 | Body | `message:string!`; `attachment refs:string!` | Catalog + diagram; labels/types DIRECT, exact JSON key/encoding unresolved |
| #60 | Success | HTTP 200 `DESIGN_RESOURCE_UPDATED`; `ApiEnvelope<SupportRequest>` | Catalog + diagram; DIRECT |
| #60 | Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR` | Catalog + diagram; DIRECT |
| #60 | Mutation | INSERT SupportMessage | AC-24 diagram; logical effect DIRECT, physical mapping unresolved |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #60 runtime | No route/module/test; path absent from design-code allowlist | `UNWIRED / NOT_FOUND` | DD is design-only; middleware mapping must be revisited during wiring. |
| Support model/IDs | Legacy schema has no support tables; pilot IDs UUID vs catalog int64 | `DISCREPANCY / SOURCE_REQUIRED` | No production INSERT or conversion can be finalized. |
| Attachment refs | #34 cannot supply a confirmed ID/metadata registry; #35/#47 leave encoding unresolved | `DERIVED / SOURCE_REQUIRED` | Recommend shared comma-separated #34 UploadAsset int64 refs, `""` for none; parser and ownership lookup await approval/model. |
| Mentor identity/author type | AC-24 role Mentor; pilot author type allows LEARNER/STAFF; current guard is Student-only | `SOURCE_REQUIRED / DERIVED` | STAFF and identity binding are proposals only. |
| Request state | Diagram assigns resolve to #61 and NO branch keeps OPEN | `DIRECT` for split actions; post-resolve reply policy `SOURCE_REQUIRED` | Do not change request status in #60. |
| Message validation/visibility | Catalog allows 422; no blank/length or internal-note policy | `DERIVED / NEEDS_CONFIRMATION` | Propose nonblank only, no length; visibility open. |

## CHANGES

- Files changed: `apps/study-server/docs/dd/60_mentor_support_reply/` (8 sheets + 3 reports) and this worklog.
- CONTEXT_UPDATES: None; no runtime/schema/catalog/diagram/context source changes.
- Context pages changed: None.
- Assumptions: Candidate `attachment_refs` comma-separated asset IDs (`""` means none), nonblank message validation, `STAFF`, `is_internal=false` and insert/reload transaction are labeled DERIVED, not confirmed behavior.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector/review | Deno selector selected #48/#49/#50; all three logs were read. | `VERIFIED` |
| Catalog and diagrams | #60 contract, AC-24 sequence, #34 upload call chains in AC-17/AC-21 read. | `VERIFIED_STATIC_ONLY` |
| Related DDs | #34, #35, #47, #58 and #59 reviewed for reference semantics, support blockers and sequence. | `VERIFIED_STATIC_ONLY` |
| Current source/schema | Router/modules/tests scan, middleware allowlist, DB helper and V1-PILOT support table definitions read. | `VERIFIED_STATIC_ONLY` |
| DD verification | Exact 11-file manifest, 8 front matters/appendix tails, catalog contract/error set, 24 nested fields, JSON, 42 links/anchors, table widths, whitespace and `git diff --check` passed. | `VERIFIED_STATIC_ONLY` |
| Runtime tests | Not run; docs-only and API #60 unwired. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: Approved support model/IDs, Mentor identity and assignment scope, attachment wire key/encoding and #34 asset registry, status after resolution, message length/visibility, and exact response rehydration rules.
- Next owner/action: AC-24 macro-review completed with open questions; see current group result below and consolidated findings in API #61 PLAN_RESULT.

## MACRO_REVIEW UPDATE — 2026-10-24

- AC-24 group #58–#61 reviewed after #61 authoring. Result: `VERIFIED_WITH_OPEN_QUESTIONS`; #60 only inserts SupportMessage and #61 owns resolution.
- Attachment ref coordination with #34/#35/#47, post-resolve reply policy and shared schema/access/response blockers remain open.
- Updated this DD's verification report; consolidated findings are in `apps/study-server/docs/dd/61_mentor_support_resolve/PLAN_RESULT.md`.
