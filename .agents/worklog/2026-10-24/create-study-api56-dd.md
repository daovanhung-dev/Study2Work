---
task_id: "2026-10-24-create-study-api56-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #56 — Lưu điểm

## CLASSIFICATION

```text
primary_task_type: docs
secondary_task_types: []
project_scopes: [server-study]
cross_scope_dependencies: []
```

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- selected_paths:
  - `.agents/worklog/2026-10-24/create-study-api48-dd.md`
  - `.agents/worklog/2026-10-24/create-study-api49-dd.md`
  - `.agents/worklog/2026-10-24/create-study-api50-dd.md`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Keep the API catalog contract, label inferred behavior `DERIVED`, do not create physical schema, and keep the Study delivery Markdown-only.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Keep Content separate from Lecture; schema/enum/payload, Mentor identity binding and generic tree rules remain source gaps.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: API #50's initial `PENDING_REVIEW` is an explicit inference from AC-22/AC-33; do not invent the physical Content table.
- Additional directly relevant records read: `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md`, API #55 DD and its report/open questions, API #54 DD, API #35 and #36 DDs.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Create a source-aware Vietnamese Markdown DD for API #56 after recording the plan. Preserve the catalog request/response/status/error contract and AC-23 order. Keep unresolved rubric, score, schema and Mentor-access rules explicit.
- Canonical contract: `docs/lists/list_api.md` row #56 and reusable `Submission` row; AC-23 index and diagram `apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio`.
- API #56 direct contract: `POST /api/v1/mentor/submissions/{submission_id}/grade`; Bearer JWT, role Mentor; `submission_id:int64!`; body `score:int32!` and catalog descriptor `rubric items:string!`; success `200 DESIGN_RESOURCE_UPDATED`, `ApiEnvelope<Submission>`; exact errors 401/403/404/422/500 as listed in the catalog.
- AC-23 says grade input precedes API #56; #56 updates grade and status `GRADED`; API #57 is a separate feedback write afterward.

## CURRENT_BEHAVIOR

- Source/config: Router `apps/study-server/app/api/v1.py` has no API #56 route; no API #56 `view.py` module exists. Current shared Bearer guard only defines Student access. No Mentor principal-to-Study numeric ID mapping or approved assignment/ownership relation is source-backed. Current `error_response(data=None)` emits `data: {}`, while API Guidelines says error data is null. `DESIGN_CONTRACT_PATHS` uses exact path equality and omits the dynamic API #56 route, so generic validation/system handlers can emit fallback `VALIDATION_ERROR`/`INTERNAL_SERVER_ERROR` if future wiring does not map it explicitly.
- Database: Legacy `infra/postgres/study-server/DB.sql` and `DB_UNICA_TABLES.md` describe `assignment_submissions.score` and `.status`; the legacy `assignments` row has decimal `max_score`. The DDL permits nullable relation FKs. No grade rubric-item relation exists there. V1-PILOT rubric tables use UUID and link to `assessments`, not legacy BIGINT assignment submissions. Live schema/migrations are not verified.
- Runnable tests: No API #56 module/test exists; application tests are not run for this docs-only task.
- Runtime wiring: `UNWIRED / NOT_FOUND`; DD is design-only.

## SOURCE_TRACE

```text
AC-23 Mentor enters score/rubric items -> POST API #56 -> intended Mentor/auth and submission-scope check -> candidate assignment_submissions score/status update -> ApiEnvelope<Submission> -> API #57 separately writes feedback -> success UI
```

## TEMPLATE_AND_ARCHIVE_PREFLIGHT

- Skill: `.agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md`, registered as `createDD-markdown` for `server-study` by `.agents/context-manifest.json`.
- Template folder: `.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/`; eight files opened. SHA-256: `00_Cover.md fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63`; `01_Lich_su.md d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e`; `02_Overview.md c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6`; `03_Request.md 37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa`; `04_Response.md 5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8`; `05_Data_Mapping.md 11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b`; `06_Error.md e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b`; `07_table.md 4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356`.
- Archive scan: no `.zip`, `.7z`, `.rar`, `.xlsx`, or `.xlsm` in `apps/study-server/docs` or `.agents/skills/create_dd_api`; the canonical Markdown template is present and source workbook appendices are embedded in it.
- Scope workflow `.agents/server-study/workflows/README.md` requires Markdown and forbids creating a new ZIP for Study API DD output.
- Error contract source: `contracts/api-guidelines/README.md`; runtime: `apps/study-server/app/core/responses.py` and `apps/study-server/app/core/middleware.py`.

## PLAN BEFORE DD AUTHORING

1. Preserve API #56 path, auth label, exact body descriptor, `ApiEnvelope<Submission>`, success and five catalog error cases. Add no status/code absent from the catalog.
2. Follow AC-23 `#54 list -> #55 detail -> Mentor inputs grade -> #56 grade/status GRADED -> #57 feedback -> success`. Keep feedback writes in #57; #56 may return the currently stored optional feedback but does not take a feedback request field.
3. Make request usage explicit: `score` is a required int32. `rubric items` is a required catalog descriptor whose literal wire-key spelling/serialization is unresolved; do not silently rename it or invent an item schema.
4. Build query/mutation matrices from candidate legacy `assignment_submissions`, `assignments`, and `courses` only. Direct course-owner check through `courses.mentor_id` is `DERIVED`; authenticated Mentor ID mapping and assigned-Mentor policy remain `SOURCE_REQUIRED`.
5. Candidate mutation updates only `assignment_submissions.score` and `.status='GRADED'`. Do not add rubric columns, audit/history rows, timestamps, feedback writes, score bounds, rounding, retry or concurrency behavior without a source.
6. Mark `rubric items` persistence as `SOURCE_REQUIRED`: no relation to legacy assignment submissions is present; pilot rubric criteria belong to UUID-based assessments. Do not join or copy that model implicitly.
7. Map every `Submission` and `ApiEnvelope` field in the response matrix. Mark `score:int32` input to `score:decimal-string` output conversion `SOURCE_REQUIRED`; carry `status=GRADED` from AC-23; keep files resolver gap from #55; preserve existing feedback candidate value without defining Student release policy.
8. Author exactly eight template sheets, one candidate `07_assignment_submissions_update.md`, plus `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md`. Keep all template Excel appendices byte-identical. No runtime source, schema, catalog, diagram, or client edits.
9. Run docs-only static validation: exact 11 files; contract/error set; all request/response fields; JSON; template tails; front matter; links; table widths; code fences; whitespace; and `git diff --check`. Do not run application tests.
10. Record current error-helper discrepancy (`data={}` vs API Guidelines `data=null`) and dynamic-route middleware allowlist gap as conditional future wiring issues.
11. Refresh inventory after authoring: 56 DD folders/47 missing; source implementation stays 12 wired/91 without route+view; keep AC-23 group macro-review #54–#57 pending until #57 DD exists.

### API Requirement Matrix

| API ID | Method/path | Actor/auth | Input | Response/success | Errors | Basis/status |
|---|---|---|---|---|---|---|
| #56 | `POST /api/v1/mentor/submissions/{submission_id}/grade` | Bearer JWT; Mentor | Path `submission_id:int64!`; body `score:int32!`, `rubric items:string!` | `ApiEnvelope<Submission>`; 200 `DESIGN_RESOURCE_UPDATED` | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR` | Catalog/diagram DIRECT; persistence/access/value policy partially SOURCE_REQUIRED |

### Request Usage Matrix

| Request item | Source/use | Query/mutation/response use | Rule/status |
|---|---|---|---|
| Authorization | Bearer JWT | Role Mentor; candidate `sub` for course scope | Catalog DIRECT; Mentor guard and ID mapping SOURCE_REQUIRED |
| `submission_id` | Required path int64 | Candidate submission lookup/update key | Type DIRECT; malformed-path branch SOURCE_REQUIRED within exact catalog error set |
| `score` | Required body int32 | Candidate update of `assignment_submissions.score`; response `Submission.score` decimal-string | Type DIRECT; min/max, max-score relation, scale/format SOURCE_REQUIRED |
| `rubric items` | Required body string descriptor | Persistence/serialization use unresolved | Required string DIRECT; exact property spelling/payload meaning/table SOURCE_REQUIRED |
| Query/body extras | None beyond catalog body fields | None | Do not add fields |

### Query Matrix

| Query | Type | Candidate source | Columns/predicate | Purpose/status |
|---|---|---|---|---|
| Q1 | SELECT | `assignment_submissions s LEFT JOIN assignments a LEFT JOIN courses c` | `s.id`, assignment/course keys and `c.mentor_id`; `s.id=:submission_id` | Candidate lookup + course owner authorization; physical nullability and Mentor identity unresolved; direct-owner predicate DERIVED |
| Q2 | UPDATE ... RETURNING or transactional reread | `assignment_submissions` | candidate `score`, `status`; key `id=:submission_id` | Candidate grade persistence, only after access check; exact transaction/locking/re-read policy SOURCE_REQUIRED |
| Q3 | SELECT or returned row mapping | `assignment_submissions` candidate fields | Full logical Submission fields | Response reload mapping; files/asset resolver SOURCE_REQUIRED |
| Rubric query/write | None approved | No assignment-rubric relation in legacy DDL; pilot assessment schema is different | N/A | SOURCE_REQUIRED; do not invent relation |

### Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| UPDATE candidate | `assignment_submissions` | `id=:submission_id` after auth/access check | `score=:score`; `status='GRADED'` | AC-23 logical action DIRECT; legacy columns candidate DESIGN_ONLY; persistence design candidate |
| Rubric items write | No approved target | N/A | No physical field/table established | SOURCE_REQUIRED; blocks implementation-ready rubric persistence |
| Feedback write | None in API #56 | API #57 is separate endpoint after #56 | No feedback mutation in this request | AC-23 sequence DIRECT; keep separate |

### Response Source Matrix

| Field | Contract type | Candidate source/transform | Gap/status |
|---|---|---|---|
| `success` | boolean | Shared envelope | Envelope convention; exact future route runtime absent |
| `businessCode` | string | Catalog success literal | DIRECT `DESIGN_RESOURCE_UPDATED` |
| `message` | string | Safe application message | Exact text/localization unspecified; DERIVED |
| `data.id` | int64 | `assignment_submissions.id` | Candidate legacy mapping; live schema unverified |
| `data.assignment_id` | int64 | `.assignment_id` | Candidate; legacy FK nullable despite logical required field |
| `data.user_id` | int64 | `.user_id` | Candidate; identity/data disclosure policy unresolved |
| `data.content` | string? | `.content` | Candidate direct nullable mapping |
| `data.files[]` | UploadAsset[] | No approved relation; legacy has one `file_url` | SOURCE_REQUIRED; carries API #55 gap |
| `data.files[].id/name/url/content_type/size_bytes/status` | per UploadAsset schema | No source-backed asset resolver | SOURCE_REQUIRED |
| `data.status` | SubmissionStatus | Candidate `.status`; AC-23 target `GRADED` | Target value DIRECT; full enum and storage availability unverified |
| `data.submitted_at` | date-time | Candidate `.submitted_at` | Timezone/serialization policy unspecified |
| `data.score` | decimal-string? | Candidate `.score`; request `int32` | Numeric conversion/scale and limits SOURCE_REQUIRED |
| `data.feedback` | string? | Candidate `.feedback`; no update from #56 | Null/omit and release policy unresolved; keep separate from #57 write |
| `meta` | object | Shared envelope | No pagination shape; empty object example only |
| `traceId` | uuid | Request trace | Shared envelope convention; API #56 runtime absent |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #56 runtime | No route, module `view.py`, or test | `UNWIRED / NOT_FOUND` | Design-only; no runtime claims. |
| Rubric input | Catalog uses `rubric items:string!`; no wire-key or item schema; legacy assignment tables have no rubric storage relation | `SOURCE_REQUIRED` | Cannot finalize validation or persistence until owner resolves contract/schema. |
| Score shape | Request `int32`, response `decimal-string?`, assignment max score `NUMERIC(6,2)` | `DISCREPANCY / SOURCE_REQUIRED` | Range, decimal scale, conversion and max-score validation are undefined. |
| Mentor access | AC-23 says Mentor must have permission; current guard is Student-specific; legacy `courses.mentor_id` is only a direct-owner candidate | `DERIVED / SOURCE_REQUIRED` | Principal mapping, assigned Mentor and 403/404 masking policy are unresolved. |
| Submission schema | Legacy DDL and table guide are design artifacts; relation FKs are nullable in DDL; live schema not verified | `DESIGN_ONLY / NOT_VERIFIED` | Candidate query/update cannot be called runtime verified. |
| Rubric pilots | V1-PILOT `rubrics`/`rubric_criteria` use UUID and assessment relations; no legacy assignment submission link | `DISCREPANCY` | Do not join these tables to BIGINT assignment submissions. |
| Error contract/runtime | API Guidelines specifies error data null; current `error_response(None)` emits `{}`. Exact-path middleware allowlist excludes dynamic API #56 path. | `DISCREPANCY / CONDITIONAL_FUTURE_WIRING` | Resolve response shape and route-specific DESIGN_* dispatch when implementing the endpoint. |
| Group order | AC-23 places #57 feedback after #56 grade; #54 response cardinality discrepancy remains in #54 | `GROUP_MACRO_REVIEW_PENDING` | Review #54–#57 after #57 DD exists. |

## CHANGES

- Files changed: `apps/study-server/docs/dd/56_mentor_submissions_grade/` (eight template sheets, one table mapping, three reports); this worklog; `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md` refreshed after creation. Existing unrelated worktree changes were preserved.
- CONTEXT_UPDATES: None planned; no runtime, schema, catalog, or diagram changes.
- Context pages changed: None planned.
- Assumptions: Direct-owner lookup and score/status persistence are labeled candidate/DERIVED; rubric items are not silently discarded or mapped to invented storage; all unresolved rules stay open.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector/read | Selected three `docs` worklogs; #48–#50 read; also reviewed inventory and directly related DDs. | `VERIFIED` |
| Template and skill | Registry wiring confirmed; eight Markdown template files opened and fingerprinted. | `VERIFIED_STATIC_ONLY` |
| Archive scan | No archive/workbook inputs under scoped Study DD or registered API DD skill resources. | `VERIFIED_STATIC_ONLY` |
| Catalog and AC-23 | API #56 row, Submission schema, AC-23 index, full diagram nodes/edges reviewed. | `VERIFIED_STATIC_ONLY` |
| Database artifacts | Legacy Study DDL, DB table guide, API #35/#36 DDs, V1-PILOT rubric table definitions reviewed. | `VERIFIED_STATIC_ONLY` |
| Current source | Router/module/test inventory contains no API #56 wiring. | `VERIFIED_STATIC_ONLY` |
| Error helper and middleware | `error_response(data=None)` serializes `{}`; generic validation/system handlers use DESIGN_* only for exact allowlisted paths, and API #56 dynamic path is absent. | `VERIFIED_STATIC_ONLY / CONDITIONAL_FUTURE_WIRING` |
| Markdown checks | Exact 11-file set; all eight template appendix tails byte-identical; front matter; request/response field coverage; catalog request/success/error codes; JSON examples; relative links/anchors; table widths; code fences; whitespace; mutation limited to candidate score/status all passed. | `VERIFIED_STATIC_ONLY` |
| `git diff --check` | No diagnostics. | `VERIFIED` |
| Verification report fingerprint | `apps/study-server/docs/dd/56_mentor_submissions_grade/VERIFICATION_REPORT.md` SHA-256 `c5b507fc0810e17f67ec3e3f224a25168467be80c39a99d8577abbcaa993efa0`. | `VERIFIED` |
| Inventory refresh | 103 catalog endpoint IDs; 56 DD core packages, 47 missing; 44 full 11-artifact packages; source route+view intersection 12, 91 without pair. | `VERIFIED_STATIC_ONLY` |
| Application tests | Not run; docs-only task. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: Rubric wire contract and persistence; score range/scale/conversion; Mentor identity/assignment policy; files resolver; current/live database schema; error data null/object discrepancy and middleware dynamic-path error-code mapping.
- Next owner/action: API #56 DD and static checks are complete with open questions. Continue API #57 in the next one-API session; macro-review AC-23 #54–#57 after #57 exists.

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
