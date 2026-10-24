---
task_id: "2026-10-24-create-study-api59-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #59

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ nguyên contract catalog; ghi candidate schema là DERIVED/SOURCE_REQUIRED và tách code source khỏi runtime verification.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Tạo matrices theo field; không invent physical mapping, enum, behavior hoặc error code.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Giữ expected/current và source/schema gap tách biệt; Study API DD chỉ giao Markdown.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD Markdown tiếng Việt cho API #59, lập và lưu plan trước authoring; liên kết với AC-24 và API #58; xác minh tĩnh gói DD ngay sau khi tạo.
- Canonical contract/approved DD: `docs/lists/list_api.md` row #59; reusable `SupportRequest`, `SupportMessage`, `UserSummary`, `UploadAsset`; AC-24 API index và page trong `AC_03_MENTOR_TEACHING.drawio`; registered `createDD-markdown` skill và Study `docs-dd` workflow.

## CURRENT_BEHAVIOR

- Source/config: Catalog #59 là `GET /api/v1/mentor/support/{request_id}`, Bearer JWT / Mentor, `request_id:int64!`, không body/query, `ApiEnvelope<SupportRequest>`, HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; lỗi đúng 401/403/404/500. AC-24 node #59 đọc request + conversation sau #58. Không tìm thấy route/module/test cho #59 trong Study source; `DESIGN_CONTRACT_PATHS` chưa có path này. Shared current-user guard chỉ phục vụ Student.
- Schema: Legacy DB.sql/ERD không có support tables. V1-PILOT `support_tickets`/`support_messages` có UUID IDs, ticket không có `course_id`, author/file projections không khớp trực tiếp contract int64; đây chỉ là candidate schema, không chứng minh runtime/live mapping.
- Runnable tests: Không chạy; docs-only và API #59 chưa wired.
- Runtime wiring: `UNWIRED / NOT_FOUND`; chưa có Mentor guard, identity/assignment predicate hoặc approved physical resolver cho SupportRequest/messages/attachments.

## SOURCE_TRACE

```text
Mentor Bearer principal -> GET detail bằng request_id -> kiểm tra request tồn tại và thuộc phạm vi Mentor -> đọc SupportRequest cùng conversation/messages và các projection -> map ApiEnvelope<SupportRequest> -> trả 200 hoặc đúng catalog 401/403/404/500 -> UI tiếp tục reply/resolve qua #60/#61
```

## PLAN BEFORE DD AUTHORING

1. Tạo API requirement matrix từ đúng catalog row #59: `GET /api/v1/mentor/support/{request_id}`; Mentor Bearer JWT; `request_id:int64!`; không body/query; `ApiEnvelope<SupportRequest>`; 200 `DESIGN_RESOURCE_RETRIEVED`; errors đúng 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`.
2. Theo AC-24: #58 mở danh sách; #59 đọc một request và conversation; #60 gửi reply; #61 resolve conditional. Không đưa mutation vào #59; không tự thêm query pagination, sort, 422, 409 hoặc 503.
3. Giữ response shape singleton theo contract. Khác #58, đây là endpoint detail nên không có list-vs-object cardinality conflict; vẫn ghi rõ SupportRequest.messages[] bắt buộc nhưng thứ tự/giới hạn và internal-message visibility chưa được catalog/diagram chốt.
4. Query matrix: mô tả Q1 logical lookup theo request_id nhưng không viết SQL vật lý; pilot `support_tickets.id` là UUID, không tương thích `int64`. Ghi Q2 conversation/message lookup là SOURCE_REQUIRED; pilot `support_messages.ticket_id/id` là UUID và author/file projection không khớp. Không tự ép cast hoặc map UUID sang int64.
5. Giữ Mentor scope theo AC-24 precondition. Không lấy `request_id` hay client input làm quyền; không chọn `assigned_to_subject_id` hoặc course ownership làm predicate được duyệt khi principal mapping/assignment chưa có nguồn.
6. Lập response source matrix đủ mọi field của SupportRequest → UserSummary → SupportMessage → UploadAsset. Ghi ID, course relation, author/user projection, signed URL, content type, upload status và null/omit rules là SOURCE_REQUIRED khi không có mapping được duyệt.
7. Giữ 404 cho resource không tìm thấy theo contract và 403 cho access denied; không tự chốt thứ tự existence-vs-scope check nếu contract/security policy chưa nói rõ. Ghi malformed/overflow path behavior vì catalog không có 422. Nêu discrepancy middleware allowlist chỉ là future-wiring risk, không phải hành vi route #59 hiện tại.
8. Trước mọi DD sheet, tạo `59_mentor_support_request_detail/PLAN_RESULT.md` làm artifact đầu tiên; sau đó tạo 8 template sheets + `OPEN_QUESTIONS.md` + `VERIFICATION_REPORT.md`, tổng 11 Markdown files. Dùng appendix/template registry từ `createDD-markdown`; `07_table.md` ghi `N/A — READ-ONLY API`; không tạo ZIP theo Study workflow.
9. Static verify exact endpoint/auth/status/error set, all response field coverage, JSON examples, 8 front matter/appendix tails, exact 11-file manifest, links/anchors, tables/fences/whitespace và `git diff --check`. Runtime tests `NOT_RUN`. Giữ AC-24 macro-review pending tới khi #60–#61 có DD.

### API Requirement Matrix

| API ID | Contract item | Giá trị | Basis/status |
|---|---|---|---|
| #59 | Method/path | `GET /api/v1/mentor/support/{request_id}` | Catalog + AC-24; DIRECT |
| #59 | Actor/auth | Bearer JWT; Mentor | Catalog + AC-24; DIRECT |
| #59 | Path | `request_id:int64!` | Catalog; DIRECT |
| #59 | Body/query | Không khai báo | Catalog; DIRECT |
| #59 | Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<SupportRequest>` | Catalog/diagram; DIRECT |
| #59 | Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR` | Catalog/diagram; DIRECT |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #59 runtime | Current router/module/test scan has no endpoint source | `UNWIRED / NOT_FOUND` | DD is design-only. |
| Physical model and IDs | Legacy Study schema lacks support tables; V1-PILOT uses UUID IDs while API contract uses int64 | `DISCREPANCY / SOURCE_REQUIRED` | No physical SQL or cast can be finalized. |
| Mentor access | AC-24 requires in-scope Mentor request; current guard is Student-only and identity/assignment link is absent | `SOURCE_REQUIRED` | No executable scope predicate. |
| Nested response | Contract requires messages, authors and attachments; physical projection/resolver not approved | `SOURCE_REQUIRED` | Full response mapping blocked. |
| Error dispatch | Middleware design-code allowlist excludes #59 path | `DISCREPANCY / CONDITIONAL_FUTURE_WIRING` | Revisit when endpoint is implemented; not current #59 runtime behavior. |

## CHANGES

- Files changed: `apps/study-server/docs/dd/59_mentor_support_request_detail/` (8 sheets + 3 reports), this worklog, and refreshed inventory worklog `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md`.
- CONTEXT_UPDATES: None; no runtime/schema/catalog/diagram/context source changes.
- Context pages changed: None.
- Assumptions: No physical support model, access predicate, message order, enum, or URL resolver is selected; unresolved behavior remains open.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector/review | Deno selector selected #48/#49/#50; all three were read. | `VERIFIED` |
| Catalog and AC-24 | #59 row/schema fields and AC-24 #58→#59→#60→#61 flow read. | `VERIFIED_STATIC_ONLY` |
| Current source | Router, modules, tests and middleware scanned; #59 absent and path absent from contract allowlist. | `VERIFIED_STATIC_ONLY` |
| Schema artifacts | Legacy schema lacks support tables; V1-PILOT candidate definitions read; runtime schema not established. | `VERIFIED_STATIC_ONLY` |
| DD verification | Exact 11-file manifest; 8 front matters/appendix tails; exact catalog contract/error set; 24 response fields; JSON, 34 relative links/anchors, table widths, whitespace and `git diff --check` passed. | `VERIFIED_STATIC_ONLY` |
| Runtime tests | Not run; docs-only, #59 unwired. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: Approved support schema/ID contract, Mentor principal and assignment scope, nested message/author/asset projection, message visibility/order/limits, malformed path behavior, and conditional error middleware integration.
- Next owner/action: AC-24 macro-review completed with open questions; see current group result below and consolidated findings in API #61 PLAN_RESULT.

## MACRO_REVIEW UPDATE — 2026-10-24

- AC-24 group #58–#61 reviewed after #61 authoring. Result: `VERIFIED_WITH_OPEN_QUESTIONS`; #59 remains read-only between list and reply.
- Physical ID/model, Mentor principal/scope, message ordering/visibility and author/attachment projection remain open; no response contract or source mapping was invented.
- Updated this DD's verification report; consolidated findings are in `apps/study-server/docs/dd/61_mentor_support_resolve/PLAN_RESULT.md`.
