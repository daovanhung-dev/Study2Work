---
task_id: "2026-10-24-create-study-api57-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #57 — Lưu feedback bài nộp Mentor

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Preserve catalog fields/codes; mark candidates `DERIVED`; do not invent persistence, fields or relationships; keep Study DD Markdown-only.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Keep expected contract separate from current runtime; retain `UNWIRED`, `NOT_FOUND`, `SOURCE_REQUIRED`; review related API flows without silently changing schemas.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: API contract and diagram order are authoritative for design; require per-field request/response and query/mutation matrices; unknown Content/attachment storage stays open.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Create only API #57's Vietnamese Markdown DD in this session. Write the plan before authoring sheets, read AC-23 closely, reference #54–#56, and perform a group macro-review of #54–#57 after authoring.
- Canonical contract/approved DD: `docs/lists/list_api.md` row #57 and reusable `Submission`/`UploadAsset`; AC-23 in `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md` and page `AC23` in `AC_03_MENTOR_TEACHING.drawio`; `createDD-markdown` is wired for `server-study`; Study workflow requires Markdown output and forbids a new ZIP.

## CURRENT_BEHAVIOR

- Source/config: API #57 is `POST /api/v1/mentor/submissions/{submission_id}/feedback`, Bearer JWT/Mentor, `submission_id:int64!`, required body descriptors `feedback text:string!` and `attachments:string!`, response `ApiEnvelope<Submission>`, HTTP 200 `DESIGN_RESOURCE_UPDATED`, errors exactly 401/403/404/422/500 as cataloged. AC-23 places #57 after #56's grade/status update. No API #57 route, module or test exists in current Study source.
- Data artifacts: Legacy `assignment_submissions` has nullable `feedback TEXT` and only one nullable `file_url`; no approved feedback-attachment relation was found. Pilot `assessment_reviews.feedback_markdown` belongs to a separate UUID assessment model and has no approved relation to legacy BIGINT submissions. Live schema is unverified.
- Runtime/error: Shared auth is Student-only. Current `error_response(data=None)` serializes `{}` while API Guidelines requires `null`; exact-path `DESIGN_CONTRACT_PATHS` omits dynamic Mentor feedback routes, so future generic validation/system handlers can use fallback codes unless wiring explicitly handles the path.
- Runnable tests: No API #57 test source; no application tests will run for this docs-only task.
- Runtime wiring: `UNWIRED / NOT_FOUND`; this DD is design-only.

## SOURCE_TRACE

```text
Mentor feedback entry after API #56 -> POST #57 -> authenticate/authorize Mentor for submission scope (identity/policy unresolved) -> validate required catalog string descriptors -> candidate UPDATE assignment_submissions.feedback; attachment persistence SOURCE_REQUIRED -> map ApiEnvelope<Submission> (files resolver still SOURCE_REQUIRED) -> success UI / Student visibility timing unresolved
```

## TEMPLATE_AND_ARCHIVE_PREFLIGHT

- Skill: `.agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md`, registered as `createDD-markdown` for `server-study` by `.agents/context-manifest.json`.
- Template: `.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/`; all eight `.md` templates were opened. SHA-256 values match the template fingerprints recorded in API #54/#56 reports; source template appendices will be copied byte-for-byte.
- Archive scan: No `.zip`, `.7z`, `.rar`, `.xlsx`, or `.xlsm` found under `apps/study-server/docs` or the registered `create_dd_api` skill resource. Template includes the source workbook appendix. Study workflow forbids creating a new ZIP.

## PLAN BEFORE DD AUTHORING

1. Keep API #57's method/path, Bearer JWT and Mentor role, required `submission_id:int64!`, two required `string!` descriptors, `ApiEnvelope<Submission>`, HTTP 200 `DESIGN_RESOURCE_UPDATED`, and exact errors 401/403/404/422/500. Add no query, success field or business code.
2. Follow AC-23 sequence: #54 list → #55 detail and files/rubric → Mentor enters grade/comment → #56 updates score/status `GRADED` → #57 stores feedback → success. Do not move feedback into #56 or make #57 alter score/status.
3. Preserve catalog descriptor `feedback text` verbatim and flag JSON wire-key spelling as unresolved; do not silently rename it to `feedback`. Keep `attachments` as a required string descriptor; do not assume JSON array/stringified JSON, upload ID format, URL scheme or association.
4. Propose only the simplest schema-backed feedback candidate: update the existing nullable `assignment_submissions.feedback` text column for the selected submission. Diagram says INSERT/UPDATE, but do not invent a history table or choose append/overwrite semantics as confirmed; label update as `DERIVED` and ask whether repeated feedback replaces or versions it.
5. Treat feedback attachments separately from student-submitted `Submission.files`. Do not reuse `assignment_submissions.file_url`, map feedback attachments into `Submission.files`, or join UUID assessment review tables. Mark attachment persistence and full `UploadAsset[]` response lookup `SOURCE_REQUIRED`.
6. Reuse #54–#56's candidate direct-owner scope via `courses.mentor_id` only as `DERIVED`; Mentor claim→Study ID, assigned-Mentor policy, null/orphan relations, and 403/404 masking remain open. AC-23's UI order does not establish a direct-call `status=GRADED` precondition for #57.
7. Map every envelope and `Submission`/nested `UploadAsset` field. Candidate `feedback` response value comes from `assignment_submissions.feedback`; `score`/`status` are preserved from #56. Missing rubric response field in reusable `Submission` and Student result visibility timing remain explicit group-level questions.
8. Create `PLAN_RESULT.md` first, then exactly eight registered template sheets, one candidate table mapping `07_assignment_submissions_feedback_update.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md`. No runtime, schema, catalog, diagram or client edits; no ZIP.
9. Static-verify the exact 11-file manifest, exact catalog contract/error set, all request/response fields, candidate mutation boundary, all eight front matters and byte-identical template appendix tails, valid JSON examples, links/anchors, table widths, code fences and whitespace. Do not run application tests.
10. Macro-review #54–#57 for AC-23 sequence, singular-vs-list response, rubric availability, score/status/feedback mutation ownership, attachment vs submitted-file semantics, common candidate schema/access and error mapping. Update #54–#56 review notes/worklogs and refresh DD inventory after #57 exists.

## API REQUIREMENT MATRIX

| Item | Contract | Basis/status |
|---|---|---|
| Method/path | `POST /api/v1/mentor/submissions/{submission_id}/feedback` | Catalog + AC-23; DIRECT |
| Actor/auth | Bearer JWT; role Mentor | Catalog + AC-23; DIRECT |
| Path | `submission_id:int64!` | Catalog; DIRECT |
| Body | `feedback text:string!`; `attachments:string!` | Catalog descriptors; DIRECT; wire key/encoding unresolved |
| Success | HTTP 200 `DESIGN_RESOURCE_UPDATED`; `ApiEnvelope<Submission>` | Catalog + AC-23; DIRECT |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR` | Catalog + diagram; DIRECT |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Runtime API #57 | No router route, module view or API test | `UNWIRED / NOT_FOUND` | Design-only; no runtime claim. |
| Feedback descriptor | Catalog spells `feedback text`; JSON property spelling is not otherwise specified | `DIRECT_DESCRIPTOR / SOURCE_REQUIRED_WIRE_KEY` | Preserve exact descriptor and leave key confirmation open. |
| Attachments | Required string request field; no approved attachment table/association/encoding; response has no feedback-attachments property | `SOURCE_REQUIRED` | Cannot complete attachment persistence or response projection. |
| Candidate feedback update | Legacy row has `feedback TEXT`; AC-23 node says INSERT/UPDATE | `DERIVED` | Simple existing-column update proposal; history/overwrite semantics remain open. |
| Mentor access | AC-23 requires permission; current guard is Student-only; direct owner is only a candidate | `DERIVED / SOURCE_REQUIRED` | Reuse group candidate without claiming assigned-Mentor coverage. |
| Error serialization/dispatch | Helper emits `{}` for omitted error data; guidelines specify `null`; exact path allowlist omits dynamic route | `DISCREPANCY / CONDITIONAL_FUTURE_WIRING` | Record future integration gap, not current API behavior. |

## CHANGES

- Files changed: API #57 DD folder (8 template sheets + 3 reports); API #54–#56 reports and worklogs updated with group review; inventory worklogs refreshed; this worklog.
- CONTEXT_UPDATES: None planned.
- Context pages changed: None planned.
- Assumptions: Only the existing `feedback` column and direct-owner candidate are proposed; both remain explicitly `DERIVED`. Unknown wire/persistence rules stay open.

## VERIFICATION

| Check | Result | Status |
|---|---|---|
| Worklog preflight | Selected/read `create-study-api48-dd.md`, `create-study-api49-dd.md`, `create-study-api50-dd.md`; no shortage. | `VERIFIED` |
| AC-23 source | Parsed page nodes/edges and index: #54 → #55 → #56 grade/status → #57 feedback → success. | `VERIFIED_STATIC_ONLY` |
| API contract/source/schema | Catalog rows #54–#57, Submission fields, legacy DDL/table guide, pilot assessment review and current route/error source inspected. | `VERIFIED_STATIC_ONLY` |
| Template/archive | Registry verified; 8 templates opened and hashed; scoped archive scan empty; Study output Markdown-only. | `VERIFIED_STATIC_ONLY` |
| DD authoring | Exact 11-file package created; template appendix, contract/error set, field coverage, JSON, links/anchors, tables, fences and whitespace checks passed. | VERIFIED_STATIC_ONLY |
| AC-23 macro-review #54–#57 | Compared list/detail/rubric/grade/feedback order, response schema, mutation ownership, assets, Mentor scope and error mapping; connected reports/worklogs updated. | VERIFIED_WITH_OPEN_QUESTIONS |
| Application tests and runtime | Not run; API #57 is unwired and task is docs-only. | NOT_RUN |

## HANDOFF

- Remaining blockers: Feedback wire key, attachment encoding/storage, update/history behavior, Mentor principal/assignment, response asset/rubric mapping, Student disclosure timing, live schema and error-helper/middleware alignment.
- Next owner/action: API #57 DD and AC-23 #54–#57 macro-review are statically verified with open questions. Continue one-API-per-session at API #58; current inventory is 57 DDs created / 46 not created and 12 source-programmed / 91 without route plus view.

## GROUP_MACRO_REVIEW

- Trạng thái: VERIFIED_WITH_OPEN_QUESTIONS sau khi tạo DD API #57.
- Flow chung: #54 list → #55 detail/files/rubric → #56 score/status GRADED → #57 feedback → success; mỗi API giữ đúng phần read/write của mình.
- API #54 vẫn có mismatch giữa mục đích danh sách và response Submission đơn; 409 chưa có nhánh trong AC-23. Giữ contract catalog hiện tại tới khi owner quyết định.
- API #55 có gap rubric trong response; #56 nhận rubric items nhưng chưa có key, schema hoặc persistence legacy được xác nhận.
- API #56 giữ mutation score/status; #57 tách riêng feedback.
- Submission.files vẫn thiếu UploadAsset resolver. attachments của #57 không phải files học viên nộp, không dùng lại file_url; chưa có bảng hoặc field response được suy diễn.
- Mentor JWT identity, assigned-course, direct-owner candidate và quan hệ nullable/orphan còn mở.
- Error data null/object và middleware dynamic path mapping là gap wiring tương lai.
- Không chạy runtime tests hay AC-23 end-to-end; đây chỉ là macro-review tài liệu.
