---
task_id: "2026-10-24-create-study-api66-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #66

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-10-24/create-study-api48-dd.md
    - carry_forward: Preserve catalog response; mark inferred behavior DERIVED; keep absent event/storage source SOURCE_REQUIRED.
  - path: .agents/worklog/2026-10-24/create-study-api49-dd.md
    - carry_forward: Parse the AC diagram sequence; do not merge neighboring APIs; keep exact error set and schema gaps explicit.
  - path: .agents/worklog/2026-10-24/create-study-api50-dd.md
    - carry_forward: Preserve current source versus design-only boundaries; use 8 sheets plus reports; Study output is Markdown-only.
- shortage: none

## EXPECTED_BEHAVIOR

- Requirement: Create Vietnamese DD #66 as one API unit in this turn; plan first, read AC-26 carefully, consult earlier DDs, validate immediately, and leave group macro-review #65–#67 pending until #67 exists.
- Canonical contract: docs/lists/list_api.md row #66: GET /api/v1/mentor/courses/{course_id}/analytics; Bearer JWT, Mentor; course_id:int64!; no body/query; HTTP 200 DESIGN_RESOURCE_RETRIEVED; ApiEnvelope<Page<Course>>; errors exactly 401/403/404/500.
- AC-26: Mentor opens the course progress dashboard; #65 aggregates enrollment/progress; #66 aggregates learning events; learner is selected; #67 reads that learner progress; UI renders dashboard and drill-down.

## CURRENT_BEHAVIOR

- Source/config: No API #66 route marker in app/api/v1.py, no api_66 view module and no focused test file. Current auth helper supports Student authorization only. DESIGN_CONTRACT_PATHS does not include the #66 path.
- Database evidence: Legacy Study DDL contains courses, enrollments, lessons and lesson_progress state rows, but no learning event history relation. V1-PILOT has progress facts/snapshots and last_event_id references, plus generic audit/outbox records; none is an approved learner learning-event source. These are checked-in design artifacts, not live-schema evidence.
- Response discrepancy: Page<Course> has no analytics metrics. PageMeta exists but #66 declares no page/size input. API guideline expects error data:null while error_response currently defaults absent data to {}.
- Runtime status: UNWIRED / NOT_FOUND. No application tests will be run for this docs-only API.

## SOURCE_TRACE

~~~text
Mentor UI opens dashboard -> #65 reads class enrollment/progress -> #66 reads course learning-event aggregate -> UI selects a Student -> #67 reads that Student progress -> dashboard/drill-down renders.
~~~

## PLAN BEFORE DD AUTHORING

1. Preserve the exact direct catalog contract: GET /api/v1/mentor/courses/{course_id}/analytics; Mentor Bearer JWT; course_id:int64!; no query/body; HTTP 200 DESIGN_RESOURCE_RETRIEVED; ApiEnvelope<Page<Course>>; exact 401/403/404/500 errors. Do not add direct contract fields or codes.
2. Parse the full AC-26 index and drawio nodes/edges. Keep API responsibilities separate: #65 enrollment/progress; #66 learning events; #67 selected-Student progress. The UI sequence does not imply an API-to-API server call.
3. Read and compare DD #65, #62, #21, #25 and the catalog reusable schemas. Reuse the explicit DERIVED/SOURCE_REQUIRED style and keep #66 connected to #65/#67 without copying their payloads.
4. Recheck current router/module/test source, auth helper, response helper, middleware allowlist, DB table guide, legacy DDL and V1-PILOT DDL. Do not use audit_events as learning analytics and do not invent a learning_events table or physical columns.
5. Keep ApiEnvelope<Page<Course>> as the direct response; enumerate its envelope, Course and PageMeta fields and mark the lack of event metrics as a DISCREPANCY.
6. For the diagram's unspecified analytics, propose a small review-only CourseLearningAnalytics summary: total_learning_events, students_with_learning_events, last_activity_at. Define the candidate conceptually as all-time-to-date course activity; zero events gives zero counts and null last_activity_at. Mark fields, event taxonomy, deduplication, time window, event source and retention as DERIVED/SOURCE_REQUIRED; this is not the wire contract.
7. Recommend a single aggregate object response (ApiEnvelope<CourseLearningAnalytics>) only as a DERIVED alternative to Page<Course>; do not change the catalog row. Keep pagination out of this summary proposal.
8. Candidate access follows the #65 question only at the logical level: ensure the Mentor may view the course; direct owner via courses.mentor_id is DERIVED, assignment/identity and privacy-aware 403/404 order remain SOURCE_REQUIRED. No ownership SQL against an assumed live schema.
9. Complete API Requirement, Request Usage, Query, Mutation and Response Source matrices before authoring. For event query, state physical relation and columns SOURCE_REQUIRED; give no SQL against guessed storage.
10. Create the 8 template sheets and 3 reports in apps/study-server/docs/dd/66_mentor_course_analytics/. 07_table.md must say N/A — READ-ONLY API. No ZIP, runtime, schema, catalog, diagram or context edits.
11. Static-validate the exact 11-file set, front matter, registered template appendix/hash, contract/error set, direct-versus-derived fields, JSON, links, tables, fences, whitespace and git diff --check. Do not run application tests. Update the inventory worklog after #66; macro-review #65–#67 remains pending #67.

### API Requirement Matrix

| API ID | Method/path | Actor/auth | Input | Success/response | Errors | Basis/status |
|---|---|---|---|---|---|---|
| #66 | GET /api/v1/mentor/courses/{course_id}/analytics | Mentor / Bearer JWT | course_id:int64!; no body/query | HTTP 200 DESIGN_RESOURCE_RETRIEVED; ApiEnvelope<Page<Course>> | 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 404 DESIGN_RESOURCE_NOT_FOUND; 500 DESIGN_INTERNAL_ERROR | Catalog DIRECT; AC-26 aggregate learning events DIRECT at purpose level; details DISCREPANCY/DERIVED |

### Request Usage Matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Required header | Authenticate Mentor and scope course analytics | Bearer/Mentor DIRECT; no Mentor guard or identity binding in current Study source |
| course_id | Required path int64 | Candidate course lookup and logical event scope | DIRECT type; physical schema and live mapping SOURCE_REQUIRED |
| Query/body | None | No window, page, size, or event-type filter | DIRECT; no declared pagination controls |

### Query Matrix

| Query ID | Purpose/type | Source/columns | Predicate/group | Evidence/status |
|---|---|---|---|---|
| Q1 | Course existence/access / SELECT candidate | Legacy candidate courses.id and courses.mentor_id | course_id match; direct-owner predicate only as a DERIVED proposal | Design-only; identity, assignment, live schema and privacy order unresolved |
| Q2 | Learning-event aggregate / conceptual read | No approved event relation or columns found | Conceptual course filter; count events, distinct Student actors, maximum event time | Physical source/query SOURCE_REQUIRED; do not use audit_events, progress facts or snapshots as an event log without approval |

### Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | GET is read-only | No INSERT/UPDATE/DELETE | N/A — READ-ONLY API |

### Response Source Matrix

| Response field | Type | Candidate source | Mapping/null rule | Evidence |
|---|---|---|---|---|
| Envelope fields | success, businessCode, message, data, meta, traceId | ApiEnvelope<T> | Preserve reusable schema | DIRECT; endpoint unwired |
| data.items[] | Course[] | Catalog reusable Course | Preserve direct type | DIRECT; has no learning-event metrics |
| Course fields | id, title, description?, thumbnail_url?, price, status, mentor, category? | Reusable Course schema | Every field listed in DD; physical course mapping is candidate only | DIRECT schema; enum/joins unresolved |
| data.pagination | page, size, total, total_pages | PageMeta | Preserve direct schema | DIRECT; request has no page/size |
| Candidate total_learning_events | int64 | Approved learning-event source not found | Count all qualifying course events to date | DERIVED proposal; table/id/dedup/window SOURCE_REQUIRED |
| Candidate students_with_learning_events | int32 | Approved event actor source not found | Count distinct Student actors with qualifying events | DERIVED proposal; actor role/linkage SOURCE_REQUIRED |
| Candidate last_activity_at | date-time? | Approved event timestamp source not found | Maximum event time; null when there are no qualifying events | DERIVED proposal; physical timestamp SOURCE_REQUIRED |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #66 runtime | No router declaration, module or focused test | UNWIRED / NOT_FOUND | Documentation-only design |
| Analytics source | Diagram says aggregate learning events; reviewed DDL has no approved learning-event history relation | SOURCE_REQUIRED | No executable event query or result mapping |
| Response shape | Catalog Page<Course> does not include event metrics | DISCREPANCY | Preserve direct contract; proposed summary needs approval |
| Pagination | PageMeta exists but no page/size input | DISCREPANCY | Do not infer pagination defaults |
| Mentor permission | Catalog role plus AC-26 course permission; current helper Student-only | DERIVED / SOURCE_REQUIRED | Principal, assigned-course support and 403/404 order unresolved |
| Error handling | API guidelines data:null vs helper absent-data {} and path absent from design allowlist | DISCREPANCY / conditional future wiring | Must reconcile when implementation is authorized |

## CHANGES

- Files changed: this worklog, `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md`, and `apps/study-server/docs/dd/66_mentor_course_analytics/` (8 sheets + 3 reports).
- CONTEXT_UPDATES: None planned; no source, schema, catalog, diagram or context edits.
- Assumptions: the three minimal analytics metrics and all-time scope are explicitly DERIVED proposals; no physical event schema is invented.

## VERIFICATION

| Check | Planned result | Status |
|---|---|---|
| Preflight | Three docs worklogs #48/#49/#50 read in full; no shortage | VERIFIED |
| AC-26/catalog/source/schema | Exact contract and sequence checked; API #66 remains absent; approved event schema not found | VERIFIED_STATIC_ONLY |
| Template gate | Registered createDD-markdown and eight templates inspected; Study workflow is Markdown-only | VERIFIED |
| Static DD validation | Exact 11-file set, front matter, all 8 template appendix suffixes, contract/error set, JSON, links, tables, fences and whitespace passed | VERIFIED |
| Runtime tests | Not run; docs-only | NOT_RUN |

## HANDOFF

- DD #66 is created as Draft — Needs Confirmation; the response-shape conflict and learning-event source remain open questions.
- Group macro-review #65–#67 is complete at document level with open questions recorded.
- Next API DD: #68. No application tests were run.

## GROUP_MACRO_REVIEW — 2026-10-24

- Status: `VERIFIED_WITH_OPEN_QUESTIONS`; see [API #66 report](../../../apps/study-server/docs/dd/66_mentor_course_analytics/VERIFICATION_REPORT.md) and [API #67 report](../../../apps/study-server/docs/dd/67_mentor_student_progress/VERIFICATION_REPORT.md).
- #65 covers class roster progress, #66 course-wide events, and #67 one Student's current lesson state. The diagram orders UI actions and does not require server-to-server calls.
- `students_with_learning_events` remains an event-source metric, not enrollment count; #67 does not use progress state as event history. #65/#67 share the same candidate published-lesson denominator/formula.
- Shared unresolved issues: response `Page<Course>` mismatch and no pagination inputs, Mentor course-scope implementation, live schema, enrollment/progress semantics, error envelope and design-code allowlist. No runtime tests were run.

