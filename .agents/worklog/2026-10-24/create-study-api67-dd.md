---
task_id: "2026-10-24-create-study-api67-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #67

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Preserve contract and distinguish candidate rules from source; Mentor identity/assignment and legacy-vs-pilot schema remain unverified.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Keep Mentor Content separate from Course progress; do not infer content or progress schema from unrelated state tables.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Keep exact catalog codes; label deductions DERIVED; physical table and column names require source evidence.
- shortage: `none`

## TASK_CLASSIFICATION

```text
primary_task_type: docs
secondary_task_types: []
project_scopes: [server-study]
cross_scope_dependencies: []
```

## EXPECTED_BEHAVIOR

- Requirement: Create API #67 as one Vietnamese Markdown DD, write the plan and matrices before authoring, inspect the AC-26 diagrams and related DDs, validate immediately, then macro-review the linked AC-26 group #65–#67.
- Catalog #67: `GET /api/v1/mentor/courses/{course_id}/students/{student_id}/progress`; Bearer JWT, role Mentor; `course_id:int64!` and `student_id:int64!`; no body/query; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; direct response `ApiEnvelope<Page<Course>>`; exact errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`.
- AC-26: Mentor opens course dashboard; #65 aggregates enrollment/progress; #66 aggregates learning events; UI selects a Student; #67 reads that Student progress; UI renders dashboard/drill-down.

## CURRENT_BEHAVIOR

- Source/config: No API #67 route declaration, module or focused test exists in the current Study tree. The shared auth helper validates Student role only; Mentor guard/identity mapping is absent. Middleware design-code path allowlist does not contain the #67 path. Current `error_response` defaults omitted error data to `{}`, while API guidelines expect `null`; no API #67 runtime behavior is observed.
- Data source: `DB_UNICA_TABLES.md` marks #65/#67 SELECT as DESIGN_ONLY and table-specific runtime query as NOT_FOUND. Legacy checked-in `DB.sql` has candidate `courses`, `enrollments`, `users`, `lessons`, and `lesson_progress`; progress stores user_id, lesson_id, status (default NOT_STARTED), progress_percent (default 0), last_accessed_at and completed_at. Its user/lesson references are nullable and it does not declare unique `(user_id, lesson_id)`. This is not live-schema evidence.
- Alternate schema: V1-PILOT uses UUID course/enrollment/lesson-progress facts; `lesson_progress_facts` has status and timestamps but no percent; `progress_snapshots` has course-version aggregate metrics. It is not equivalent to legacy BIGINT or the catalog int64 path. Live schema/migrations remain unverified.
- Related behavior: current API #9 source reads a PUBLISHED course and PUBLISHED lessons, ordered by `sort_order, id`; this is a source-backed candidate lesson set, not a rule stated in AC-26. AC-14 says start marks progress IN_PROGRESS and completion marks COMPLETED; API #25 DD and DDL mappings remain DESIGN_ONLY/candidate.
- Related DDs: #65 candidate uses the same published lesson denominator and `floor(sum(progress_percent with missing as zero) / total_lessons)`, with zero for an empty denominator; the formula remains DERIVED. #66 is separate course-level learning-event analytics and its event source is not approved. #37 AC-18 describes broader Student-side lesson/quiz/assignment progress, but it is a separate flow and does not prove #67 scope.
- Runnable tests: no application tests will be run; this is docs-only. API #67 has no test source.
- Runtime wiring: API #67 is UNWIRED / NOT_FOUND. Current source search does not prove live behavior for the legacy or pilot schema.

## SOURCE_TRACE

```text
Mentor opens AC-26 dashboard -> #65 class enrollment/lesson-progress summary -> #66 course-wide learning-event aggregate -> UI selects a Student -> #67 checks Mentor course scope and Student course membership -> reads that student's per-lesson current progress -> renders drill-down. #67 does not call #65/#66 server-to-server and does not recount learning events.
```

## PLAN BEFORE DD AUTHORING

1. Preserve the exact direct catalog contract: GET `/api/v1/mentor/courses/{course_id}/students/{student_id}/progress`; Bearer JWT/Mentor; both required int64 path values; no query/body; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Page<Course>>`; only 401/403/404/500 with their catalog codes.
2. Parse AC-26 index and the full draw.io AC-26 page. Keep responsibilities separate: #65 class-level enrollment/progress, #66 course-wide learning events, #67 selected Student progress. The UI sequence does not establish a server-to-server call.
3. Review DD #65 and #66, related progress DD #21/#25/#37, Mentor roster DD #62 and current API #9 source. Keep expected contract distinct from the current source and candidate logic.
4. Verify current Study route/module/test/auth/response/middleware source for #67; inspect DB guide, legacy and V1-PILOT DDL. Do not select a live schema or treat progress rows/snapshots as event history.
5. Keep the direct response `ApiEnvelope<Page<Course>>` and enumerate envelope, Course and PageMeta fields. Record that it cannot express student progress and PageMeta has no page/size request.
6. Propose a simple DERIVED response only for review: one `StudentCourseProgress` object with course/student identity, summary (`completed_lessons`, `total_lessons`, `progress_percent`) and a list of published lesson progress (`lesson_id`, `title`, `order`, `progress_status`, `progress_percent`, `last_accessed_at`, `completed_at`). This candidate is intentionally separate from the direct wire contract.
7. Reuse #65 candidate denominator and formula so the dashboard summary and student detail agree: current API #9 PUBLISHED lesson set, sort by `sort_order, id`; missing progress is zero; completed status is COMPLETED; percentage is floor of summed per-lesson progress divided by denominator; zero when denominator is zero. Mark every rule DERIVED and request confirmation; do not present these as approved runtime rules.
8. Require the selected student to be in the same approved course enrollment/roster scope as #65 before returning their progress. Keep enrollment status, direct-owner vs assignment authorization, identity binding and privacy-aware 403/404 order SOURCE_REQUIRED. Do not disclose arbitrary Student data.
9. Keep quiz/assignment progress outside the #67 candidate because AC-26 does not name those units and #65 is lesson-based; record a question because the separate AC-18/#37 flow is broader.
10. Complete API Requirement, Request Usage, Query, Mutation and Response Source matrices before authoring. Do not write physical SQL that chooses between legacy BIGINT and V1-PILOT UUID schema; show candidate columns and unresolved schema boundary only.
11. Create 8 template sheets + `OPEN_QUESTIONS.md`, `PLAN_RESULT.md`, `VERIFICATION_REPORT.md` under `apps/study-server/docs/dd/67_mentor_student_progress/`; `07_table.md` says N/A — READ-ONLY API. No ZIP, runtime, catalog, diagram or context edits.
12. Static-check exact 11-file set, contract/errors, full direct and candidate field mapping, JSON, links, table widths, fences, template suffixes, front matter, whitespace and `git diff --check`; no application tests.
13. After #67 verification, macro-review #65–#67 for responsibilities, formulas, source boundaries, authorization, pagination/response shape and error conventions. Update #65/#66 reports and question lists, #67 report and inventory worklog; keep unresolved questions visible.

### API Requirement Matrix

| API ID | Method/path | Actor/auth | Input | Success/response | Errors | Basis/status |
|---|---|---|---|---|---|---|
| #67 | `GET /api/v1/mentor/courses/{course_id}/students/{student_id}/progress` | Mentor / Bearer JWT | `course_id:int64!`, `student_id:int64!`; no query/body | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Page<Course>>` | 401 authentication required; 403 access denied; 404 resource not found; 500 internal error | Catalog DIRECT; selected-Student progress DIRECT at purpose level from AC-26; output fields and formulas DERIVED/SOURCE_REQUIRED |

### Request Usage Matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Header | Authenticate Mentor and scope course before reading Student data | Bearer/role DIRECT; guard and identity binding SOURCE_REQUIRED |
| `course_id` | Required int64 path | Candidate course lookup and progress scope | DIRECT type; legacy/pilot schema and live binding unresolved |
| `student_id` | Required int64 path | Candidate membership check and per-Student progress scope | DIRECT type; must not be trusted as authorization by itself |
| Query/body | None | No page/size, filter, sort, window or mutation data | DIRECT |

### Query Matrix

| Query ID | Purpose/type | Source/columns | Predicate/group | Evidence/status |
|---|---|---|---|---|
| Q1 | Course scope/access candidate | Legacy `courses.id`, `courses.mentor_id` | Match `course_id`; compare authenticated Mentor only if identity model is approved | Legacy candidate only; Mentor identity/assignment/live schema unresolved |
| Q2 | Student membership candidate | Legacy `enrollments.course_id`, `user_id`, `status`; Student identity in `users` | Require same eligible learner set used by #65; no status chosen | Candidate; active/completed/withdrawn policy and live schema SOURCE_REQUIRED |
| Q3 | Published lesson set | API #9 source `lessons.id`, `course_id`, `name`, `sort_order`, `status` | Course match and status PUBLISHED; order by `sort_order`, `id` | Current source behavior for API #9; DERIVED denominator for #65/#67 |
| Q4 | Per-lesson progress read | Legacy candidate `lesson_progress.user_id`, `lesson_id`, `status`, `progress_percent`, `last_accessed_at`, `completed_at` | Match selected learner and lesson; missing row behaves as zero only in candidate formula | DDL candidate; uniqueness, nullability, schema and join strategy unresolved |
| Q5 | Summary calculation | Candidate published lessons + selected learner progress | Count completed; total published lessons; floor average; zero denominator => zero | Reuse #65 DERIVED proposal; no approved SQL or live query |

### Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | GET is read-only | No INSERT/UPDATE/DELETE | N/A — READ-ONLY API |

### Response Source Matrix

| Response field/group | Direct/candidate type | Candidate source | Mapping/null rule | Evidence/status |
|---|---|---|---|---|
| Direct `data.items[]` | `Course[]` | Catalog reusable Course | Preserve direct contract | DIRECT; no student-progress fields |
| Direct `data.pagination` | PageMeta | Catalog `page,size,total,total_pages` | Preserve direct schema | DIRECT; request has no page/size |
| `StudentCourseProgress.student` | UserSummary | Candidate enrolled Student | Minimal display identity | DERIVED; privacy and identity projection SOURCE_REQUIRED |
| `summary.completed_lessons` | int32 | Selected learner lesson progress | Count COMPLETED in denominator | DERIVED; enum/schema unresolved |
| `summary.total_lessons` | int32 | PUBLISHED curriculum items | Count items returned by API #9 lesson set | DERIVED from #9, requires group approval |
| `summary.progress_percent` | int32 | Per-lesson progress_percent | Same floor average as #65; zero if denominator empty | DERIVED; range/rounding/live schema unresolved |
| `lessons[].lesson_id` | int64 | Candidate lessons.id | One row per published lesson | Legacy candidate; pilot ID incompatible |
| `lessons[].title` | string | Candidate lessons.name/API #9 title mapping | `name → title` | Candidate from current API #9 source |
| `lessons[].order` | int32 | Candidate lessons.sort_order/API #9 order mapping | `sort_order → order` | Candidate from current API #9 source |
| `lessons[].progress_status` | string | Candidate lesson_progress.status | Missing row proposed as NOT_STARTED | DERIVED; exhaustive enum and missing-row rule unresolved |
| `lessons[].progress_percent` | int32 | Candidate lesson_progress.progress_percent | Missing row proposed as zero | DERIVED; DDL SMALLINT, range not constrained |
| `lessons[].last_accessed_at` | date-time? | Candidate lesson_progress.last_accessed_at | Null if no timestamp | DDL candidate; serialization unresolved |
| `lessons[].completed_at` | date-time? | Candidate lesson_progress.completed_at | Null until completed | DDL candidate; transition/serialization unresolved |
| Envelope fields | success, businessCode, message, data, meta, traceId | Reusable ApiEnvelope<T> | Direct contract fields | DIRECT schema; route absent |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #67 runtime | No route/module/focused test; path absent from allowlist | UNWIRED / NOT_FOUND | DD is design-only |
| Response shape | Catalog Page<Course> vs AC-26 Student progress | DISCREPANCY | Preserve catalog; candidate summary needs contract approval |
| Pagination | PageMeta exists, request has no page/size | DISCREPANCY | No pagination behavior can be inferred from contract |
| Progress schema | Legacy BIGINT `lesson_progress` vs V1-PILOT UUID facts/snapshots | DISCREPANCY / SOURCE_REQUIRED | Cannot produce one approved executable query |
| Authorization | Mentor course permission plus selected Student membership; current guard Student-only | DIRECT requirement / SOURCE_REQUIRED mechanism | Identity, assignment and privacy policy unresolved |
| Progress semantics | AC-14 and API #9 source give partial evidence; exact formula/status/missing row rules not approved | DERIVED / SOURCE_REQUIRED | Candidate must remain separate from wire behavior |
| AC-26 group | #65 class summary, #66 learning-event analytics, #67 Student detail; catalog responses all Page<Course> | DISCREPANCY | Macro-review required and recorded after authoring |
| Error envelope | Guideline `data:null` vs helper `{}`; route not allowlisted | DISCREPANCY / conditional future wiring | Reconcile before implementation |


## CHANGES

- Files changed: `apps/study-server/docs/dd/67_mentor_student_progress/` (8 sheets + 3 reports); connected AC-26 review updates to #65/#66 `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`; #65/#66 worklogs; this worklog; `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md`.
- CONTEXT_UPDATES: None; no context page or manifest changed.
- Runtime/source/schema/catalog/diagram unchanged. No ZIP or application tests.
- DD remains Draft — Needs Confirmation; exact catalog response is kept and candidate logic is marked DERIVED/SOURCE_REQUIRED.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector and preflight | `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` selected #48/#49/#50; all read in full. | VERIFIED |
| Plan-before-authoring | Plan and API Requirement, Request Usage, Query, Mutation and Response Source matrices recorded before DD folder creation. | VERIFIED |
| Catalog/diagram/source/schema | Exact #67 contract and AC-26 page parsed; #65–#67 route/module/test scan empty; legacy/PILOT schema mismatch recorded; API #9 PUBLISHED source checked. | VERIFIED_STATIC_ONLY |
| DD structure/template | Exact 11-file package; all 8 front matters and template appendix suffixes verified. | VERIFIED |
| Contract/errors | Direct response and exact four errors checked against catalog. | VERIFIED_STATIC_ONLY |
| Markdown/JSON/links | JSON parse, relative files/anchors, tables, fences, and whitespace passed. | VERIFIED |
| AC-26 macro-review | Responsibilities, candidate formula boundary, event/progress separation, Page<Course>/pagination, authorization/schema/error gaps reconciled across #65–#67. | VERIFIED_WITH_OPEN_QUESTIONS |
| Inventory refresh | 67/103 DDs; 36 missing; 55 full 11-file packages; 12 source-wired route+view pairs and 91 without. | VERIFIED_STATIC_ONLY |
| `git diff --check` | Passed after connected reports/worklogs were updated. | VERIFIED |
| Runtime tests | Not run; docs-only, API #67 unwired. | NOT_RUN |
| Context validator | Not applicable; no context pages/manifest changed. | NOT_APPLICABLE |

## HANDOFF

- Remaining blockers: direct response `Page<Course>` does not represent progress; pagination, Mentor identity/course assignment, Student eligibility/privacy, selected schema, duplicate row handling, formula/empty rules and error-envelope policy need approval/source.
- Next API DD: #68. AC-26 macro-review is complete at document level with open questions; no application runtime claim is made.
