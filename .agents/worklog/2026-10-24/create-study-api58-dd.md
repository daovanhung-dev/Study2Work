---
task_id: "2026-10-24-create-study-api58-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #58 — Lấy support requests

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: /home/daovanhung/.local/bin/deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-10-24/create-study-api48-dd.md
    - carry_forward: Giữ đúng catalog, ghi DERIVED/SOURCE_REQUIRED tách biệt, không ép schema pilot vào Legacy DD.
  - path: .agents/worklog/2026-10-24/create-study-api49-dd.md
    - carry_forward: Mô tả các field response chưa có persistence như SOURCE_REQUIRED; giữ đúng shape catalog và ghi discrepancy thay vì tự đổi response.
  - path: .agents/worklog/2026-10-24/create-study-api50-dd.md
    - carry_forward: Mọi candidate status/placement phải ghi DERIVED; không bịa INSERT/schema; giữ AC-24 group macro-review đến khi đủ #58–#61.
- shortage: none

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD Markdown tiếng Việt riêng cho API #58 trong một phiên; lập plan trước khi authoring; đọc diagram AC-24; tham khảo DD đã tạo; sau authoring kiểm tra ngay; macro-review toàn nhóm AC-24 sau khi #61 được tạo.
- Canonical contract: docs/lists/list_api.md row #58 và reusable schemas SupportRequest, SupportMessage, UploadAsset, UserSummary.
- Contract trực tiếp: GET /api/v1/mentor/support/requests; Bearer JWT, role Mentor; query course_id?:int64, status?:string; response ApiEnvelope<SupportRequest>; HTTP 200 DESIGN_RESOURCE_RETRIEVED; errors 401 DESIGN_AUTHENTICATION_REQUIRED, 403 DESIGN_ACCESS_DENIED, 500 DESIGN_INTERNAL_ERROR.
- Workflow/skill: createDD-markdown được registry wire cho server-study; Study giao Markdown, không tạo ZIP.

## CURRENT_BEHAVIOR

- Source/config: Router hiện không khai báo API #58; không có module api_58, view hoặc test. Middleware DESIGN_CONTRACT_PATHS chưa có endpoint này. Shared current-user guard yêu cầu role STUDENT; chưa có Mentor guard/principal-to-subject mapping.
- Database: Legacy DB.sql và DB_UNICA_TABLES/ERD không có support request/message tables. V1-PILOT có support_tickets và support_messages nhưng dùng UUID, không có course_id trong support_tickets, và không khớp int64/API response; live schema chưa xác minh.
- Runnable tests: Không chạy; docs-only; không có test API #58.
- Runtime wiring: UNWIRED / NOT_FOUND. DDL pilot không chứng minh bảng có mặt trong runtime.

## SOURCE_TRACE

Catalog/API AC-24 → Mentor mở danh sách → GET API #58 → backend đọc yêu cầu thuộc scope Mentor → trả SupportRequest theo catalog → Mentor có thể chọn request để đọc thread qua API #59.
API #58 là read-only; API #60 riêng ghi support message và API #61 riêng resolve request.

## SOURCES REVIEWED

- AGENTS.md, .agents/AGENTS.md, .agents/context-map.md, .agents/context-manifest.json.
- .agents/server-study/AGENTS.md, INDEX.md, workflows/README.md, apis/declared-routes.md, database.md.
- .agents/worklog/README.md, TEMPLATE.md và ba worklog docs do selector chọn.
- Registry và entry createDD-markdown; bộ template Markdown đã kiểm kê.
- docs/lists/list_api.md row #58 và reusable SupportRequest/SupportMessage/UploadAsset/UserSummary.
- AC/API index AC-24 và toàn bộ node/edge của page AC24 trong AC_03_MENTOR_TEACHING.drawio.
- DB_UNICA_TABLES.md, DB_UNICA_ERD.drawio, infra/postgres/study-server/DB.sql và phần support_tickets/support_messages/file_objects/learner_profiles của infra/postgres/02_study_db.sql.
- contracts/api-guidelines/README.md; current router, middleware, auth helper và source/test inventory.
- DD #54 overview/request/response/open questions/verification report; các quyết định liền kề #55–#57.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| List cardinality | Path/name are plural; catalog and AC-24 diagram return singular SupportRequest with no Page/items | DISCREPANCY | Keep exact singular contract and leave list shape unresolved; do not change to Page. |
| Support persistence | Legacy ERD/DDL has no support tables; pilot support_tickets/messages use UUID; API contract uses int64 | DISCREPANCY / SOURCE_REQUIRED | Candidate tables are not direct implementation mapping. |
| Course filter | API accepts course_id; pilot support_tickets has no course_id or course-version link | SOURCE_REQUIRED | Cannot define a supported course filter against pilot schema. |
| Mentor scope | AC-24 says requests are within Mentor scope; pilot assigned_to_subject_id is nullable UUID, but Mentor identity binding and assignment semantics are absent | DERIVED / SOURCE_REQUIRED | Keep assigned-to as a candidate only; do not claim permission mapping. |
| Nested response | SupportRequest includes numeric course/student/message IDs and UploadAsset arrays; pilot relations use UUID and no approved asset URL projection | SOURCE_REQUIRED | Full response mapping is not implementation-ready. |
| Status filter | Query status is generic string; SupportStatus values are not defined in catalog | SOURCE_REQUIRED | Apply exact supplied value only as a candidate; do not invent validation/default. |
| Runtime error mapping | API path is absent from design-code allowlist; shared helper defaults missing error data to {} while guideline says null | DISCREPANCY / CONDITIONAL_FUTURE_WIRING | Preserve catalog code set and report current helper mismatch. |

## PLAN BEFORE DD AUTHORING

1. Preserve the exact catalog method/path, Mentor Bearer requirement, optional course_id/status filters, singular ApiEnvelope<SupportRequest>, success status/code and the three catalog error cases.
2. Use AC-24 sequence: API #58 reads list; #59 reads one request/thread; #60 inserts a message; #61 resolves. Do not add mutation to #58.
3. Treat list cardinality as a contract discrepancy. Keep singular SupportRequest in request/response examples; do not add Page, items, pagination, sort or default because none is approved.
4. Candidate logical Q1 reads support requests in current Mentor scope. Apply course_id/status filters only when supplied. Do not define physical SQL until an approved model resolves the Legacy/Pilot mismatch.
5. Record pilot support_tickets.assigned_to_subject_id as a DERIVED assignment candidate only. Do not equate nullable UUID assignment with the Mentor principal or course ownership.
6. Do not map course_id through course_enrollments or another guessed relation. Pilot support_tickets has no course relation.
7. Cover every SupportRequest, nested UserSummary, SupportMessage and UploadAsset field in Response Source Matrix. Mark ID, course, student, message author and attachment projections SOURCE_REQUIRED where no compatible source exists.
8. Keep 07_table.md as N/A — READ-ONLY API; no mutation mapping.
9. Create eight sheets plus PLAN_RESULT.md, OPEN_QUESTIONS.md and VERIFICATION_REPORT.md. Preserve each registered template appendix byte-for-byte. Do not create ZIP, runtime code, tests, schema or catalog edits.
10. Verify exact contract/error set, source and diagram trace, every nested response field, JSON validity, template fingerprint/tails, links/anchors, Markdown tables/fences/whitespace and exact 11-file manifest. Leave AC-24 macro-review pending until #59–#61 exist.

## CHANGES

- Files changed: apps/study-server/docs/dd/58_mentor_support_requests/ (8 sheets + 3 reports); this worklog.
- CONTEXT_UPDATES: None; no runtime/source/schema/catalog/context page changes.
- Context pages changed: None.
- Assumptions: Use only labeled DERIVED candidates; keep unresolved list shape, course relation, Mentor identity, status values, nested field projection and signed asset URL policy open.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog preflight | Deno selector returned #48, #49, #50; all three read. | VERIFIED |
| Skill/registry/template | createDD-markdown is wired to server-study; exact registered 8-file Markdown template pack is readable. | VERIFIED_STATIC_ONLY |
| AC-24 diagram | Parsed page AC24; confirms list → single request/thread → reply/INSERT SupportMessage → optional resolve/UPDATE status. | VERIFIED_STATIC_ONLY |
| Catalog/schema | Exact #58 contract and reusable response schemas inspected. | VERIFIED_STATIC_ONLY |
| Runtime/schema inventory | No API #58 route/module/test; Legacy support model absent; pilot UUID support model differs. | VERIFIED_STATIC_ONLY |
| Post-authoring DD validation | Exact 11-file manifest; 8 appendix tails/fingerprints; front matter; JSON; response field coverage; exact catalog error set; tables/fences/whitespace; local links/anchors. | VERIFIED_STATIC_ONLY |
| Catalog/DD inventory | 103 API IDs; 58 folders with all 8 core sheets; 46 full 11-file packs; missing DD IDs #59–#103 (45). | VERIFIED_STATIC_ONLY |
| Source implementation inventory | #58 absent; current source inventory remains 12 route+view API IDs and 91 without the pair. | VERIFIED_STATIC_ONLY |
| git diff --check | No diagnostics. | VERIFIED |
| Tests | Not run; documentation-only. | NOT_RUN |
| Context validator | Ran; returned AGENT_CONTEXT_INVALID for missing DB Admin context/source roots and CONTEXT_STALE server-study from existing source drift. No worklog-specific error; API #58 changed no source/context page. | FAILED_UNRELATED_REPOSITORY_DRIFT |

## HANDOFF

- Remaining blockers: Physical support model compatible with catalog, course association, Mentor identity/scope, list response cardinality, SupportStatus members, messages projection and attachment mapping; see OPEN_QUESTIONS.md.
- Next action: Continue one-API-per-session at #59. Macro-review #58–#61 is now complete with open questions; current inventory is recorded below.

## MACRO_REVIEW UPDATE — 2026-10-24

- AC-24 group #58–#61 reviewed after #61 authoring. Result: `VERIFIED_WITH_OPEN_QUESTIONS`; sequence and mutation boundaries match the diagram.
- Preserved the #58 plural/list versus singular `ApiEnvelope<SupportRequest>` catalog discrepancy. Shared schema/UUID-int64/course, Mentor scope, nested response and error-wiring blockers remain unresolved.
- Updated this DD's verification report; consolidated findings are in `apps/study-server/docs/dd/61_mentor_support_resolve/PLAN_RESULT.md`.
- Refreshed inventory: 61 DD folders, 42 without DD, 49 full 11-file packs, 12 source-programmed APIs and 91 without the route+view pair.

