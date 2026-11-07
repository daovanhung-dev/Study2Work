---
task_id: "2026-11-06-design-study-screen-me16"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ME-16 course progress → API #65 and student/course handoff to ME-17; distinguish from ME-18 analytics API #66"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ME-16

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 203; shortage: none.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Preserve original assets; distinguish contract from current source; Study Web is unwired; API test files/fake sessions are not runtime/live-schema proof.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Trace exact response fields and caller/callee; retain API and UI discrepancies; do not infer route, cache, navigation or sorting from mockup.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: Check current API route/source/test wiring; distinguish expected AC orchestration from current backend; do not overstate local tests or source as live runtime.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ME-16 only this session; write its plan before marker map/annotation/DD; keep `screen.png` and `code.html` unchanged; create sequential 1:1 marker map, annotated image and A–F DD; update the screen inventory, `dd_screens/PLAN.md` and worklog; keep DD/implementation/runtime statuses separate.
- Inventory row: ME-16 “Tiến độ toàn khóa học”, proposed route `/mentor/courses/:courseId/progress`, AC-26, API #65, linked ME-17/ME-18. Intended surface is a table of students and lesson completion, with a student action to ME-17; expected states `loading/empty/ready/denied`. Inventory marks #65 `D` and blocks on its `Page<Course>` response shape.
- Cross-screen contract: ME-17 consumes a selected `student_id` plus `course_id` using #67. ME-18 is separate course analytics via #66; do not blend #65 student progress rows with #66 aggregate metrics without evidence.
- Initial asset inventory: `apps/study-client/docs/screen_stitch/04_mentor/ME-16_tien-do-toan-khoa-hoc/` contained only `screen.png` (294,250 bytes; SHA-256 `f94e642b19786f6a111f151986be61366cf96cd1571e222344dc6f804eea4d89`; 1600×1440) and `code.html` (21,826 bytes; SHA-256 `08529aff6c992afdb5f59f1a7dd04bbf2c3b92333c13a8744ed38e0d4f9b7eb9`). Screenshot and HTML were inspected; HTML is a static prototype with 14 placeholder anchors, one select, one search input and four buttons. No source asset edits have been made.

## CURRENT_BEHAVIOR

- The prototype has a mentor header, course breadcrumb/class-code label, title/copy, static enrollment count and timestamp, a static course selector, three progress filter buttons, search field, table shell with empty state, refresh button, ME-18 analytics link, help link, diagnostic copy, standards/refresh claims, and footer. There are no learner rows or table column headers.
- HTML evidence: `#course-select` has three static slug values; `#student-search-input` has no handler; three filter buttons have no IDs/handlers; `#btn-refresh-progress` runs only a local 1-second spinner/disabled state and restores itself. No fetch/XHR/WebSocket/SSE/timer polling is implemented. All 14 anchors use `href="#"`; the ME-18 link has only a `data-path` placeholder. The page has no form submit handler.
- Study Web remains registered `UNWIRED`; current editable app/router/API client is absent. The prototype does not establish a production route, auth guard, real data, navigation, loading/error states or refresh policy.
- Local API #65 source exists at `GET /api/v1/mentor/courses/{course_id}/progress`: shared Bearer guard requires `MENTOR`; raw path parses as signed int64; errors are 401/403/404/500; no request query/body/page-size. It checks direct `courses.mentor_id` ownership before aggregate query, returns one unbounded locally derived page for ACTIVE enrollments and `STUDENT` users, counts PUBLISHED lessons, selects duplicate progress rows by `last_accessed_at DESC NULLS LAST, id DESC`, computes `floor(sum(COALESCE(progress_percent,0))/published_lessons)` with zero for denominator 0, and returns `student{id,full_name,avatar_url?}`, `completed_lessons`, `total_lessons`, `progress_percent`, plus pagination. No email, last activity, course title/code, submissions, attendance, due dates, or support status is returned. The query is read-only; the full roster is not paginated/bounded.
- API #65's local source contract is explicitly a derived `MentorStudentProgressPage`; catalog/AC-26 declare `ApiEnvelope<Page<Course>>`. The local API DD remains Draft/Needs Confirmation, its access/formula/schema assumptions are DERIVED, and checked-in legacy BIGINT DDL differs from V1-PILOT UUID progress schema. Fake-session tests exist, but no tests/runtime/live schema were run or verified in this task.
- API #46 can return a paginated `CoursePage` with numeric `id` values for directly owned courses; ME-16's prototype selector instead uses three slugs and has no mapping or event to #46. No slug→int64 mapping is evidenced.
- API #67 is a separate selected-student detail endpoint requiring both `course_id` and `student_id`; its local response includes student summary, course-level progress summary and published lesson detail. It is the intended candidate ME-17 handoff only after a real student row/action exists.
- API #66 is separately assigned to ME-18. Current local code returns an activity-proxy summary (`tracked_lesson_accesses`, `students_with_activity`, `last_activity_at`) from `lesson_progress.last_accessed_at`, not an event ledger; its DD/catalog response also conflicts (`Page<Course>` vs summary object). It must not be merged into #65 roster data.

## SOURCE_TRACE

- Inventory and tracker rows: `apps/study-client/docs/list_screen.md` and `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` describe ME-16 as `/mentor/courses/:courseId/progress`, AC-26, #65, linked to ME-17/ME-18; both retain a #65 `Page<Course>` blocker.
- AC source: `apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio` sequence is dashboard → #65 → aggregate enrollment/progress → #66 → aggregate learning events → choose Student → #67 → read student progress → render. This conflicts with inventory's ME-16 → ME-17/#67 and separate ME-18/#66 presentation. Preserve both statements as `DISCREPANCY` pending flow-owner decision.
- Traced #65 caller/route, validator, view, query, response model, error mapping, API DD, DB candidate and focused test names. Tests cover success aggregate, empty denominator/roster, auth/role, path parsing, owner scope, safe query/projection errors, OpenAPI shape and trace ID; tests were not run. Source-backed local behavior does not establish deployed runtime or live schema.
- Traced #46 response model and mapper: numeric course ID is available, but prototype slug values are unrelated to its response and no route/state handoff contract is present.
- Traced #67 endpoint/model for the student-detail handoff and #66 model/view/query/DD for the separate proxy analytics boundary.
- Traced prototype controls and static copy from `code.html`, and preserved original PNG/HTML hashes above.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #65 response | Catalog and AC-26 specify `ApiEnvelope<Page<Course>>`; local source returns derived `ApiEnvelope<MentorStudentProgressPage>`. API DD remains Draft/Needs Confirmation. | DISCREPANCY | Table mapping cannot be treated as approved contract; preserve exact local fields and block unprovided columns/filters. |
| AC-26 orchestration | Diagram places #66 before Student selection/#67; screen inventory assigns #66 to ME-18 and links ME-16 to ME-17. | DISCREPANCY | Do not silently decide whether analytics is embedded or opened separately. |
| Selector key | Prototype uses course slugs; #65/#46 use numeric int64 course IDs; no mapping/handoff exists. | BLOCKER | Course selection cannot safely construct #65 path from prototype data. |
| Prototype behavior | Search, filter and course selector have no handlers; refresh is a 1-second local animation; anchors are placeholders. | STATIC_ONLY | Document intended interactions as proposed and blocked, not current runtime behavior. |
| Unsupported UI claims | Email search, submissions, reminders, LMS sync, SCORM/xAPI, WCAG, 15-minute refresh, cohort diagnosis and enrollment timestamp lack #65 fields/implementation. | UNVERIFIED | Do not specify them as live behavior or derive values. |
| Study Web runtime | Registered Study Web subcontext and editable app/router/client remain `UNWIRED`/absent. | UNWIRED | No runtime verification, actual auth guard, navigation or client states can be claimed. |
| Schema and paging | Local SQL targets legacy BIGINT tables; V1-PILOT schema uses UUID/versioned facts; #65 emits all roster rows as one unbounded page. | UNVERIFIED / DERIVED | Deployment compatibility and safe roster bound require resolution. |

## CHANGES

- Completed source and asset trace, then created `ME-16_PLAN.md` before marker map, annotation or DD.
- Work started/preflighted on 2026-11-06 and completed on 2026-11-07 (Asia/Bangkok); the worklog remains under the original start-date folder.
- Created `ME-16_markers.json` (42 IDs), `ME-16_markers_overlay.svg`, `screen_annotated.png` (1600×1440) and `ME-16.md` with sections A–F.
- Updated ME-16 tracker rows in `apps/study-client/docs/list_screen.md` and `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; changed API #65 reverse source status D→R because local route/module/query/model and focused test source exist. API DD remains Draft/DERIVED; no live runtime claim.
- Added 51/83 progress checkpoint to the global plan; ME-17 remains the next Mentor Screen ID in a separate session.
- CONTEXT_UPDATES: none; no `.agents/` context page was changed.
- Assumptions: none; unresolved API/UI mappings will be recorded as blockers.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | 3 exact-type docs worklogs selected of 203; no shortage. | VERIFIED |
| Selected worklog review | GS-01, GS-02, GS-03 read fully. | VERIFIED |
| Source and asset trace | Inventory, prototype, #46/#65/#66/#67, API DD, AC-26, route/view/query/model and focused #65 test coverage inspected. | VERIFIED_STATIC |
| Marker/DD/static audit | JSON parses; 42 sequential/unique/in-bounds marker centers; SVG XML parses with 42 circles/texts; DD has 42 matching element rows; relative DD links resolve. | VERIFIED_STATIC |
| Source preservation | `screen.png` SHA-256 `f94e642b19786f6a111f151986be61366cf96cd1571e222344dc6f804eea4d89`; `code.html` SHA-256 `08529aff6c992afdb5f59f1a7dd04bbf2c3b92333c13a8744ed38e0d4f9b7eb9`; both unchanged. | VERIFIED |
| Annotated image review | `screen_annotated.png` opens as 1600×1440; reviewed after moving markers from copy/control areas into adjacent whitespace. | VERIFIED_VISUALLY |
| `git diff --check` | Passed. | VERIFIED |
| Tests/runtime | Not run; no Study Web runtime or live schema verification claimed. | NOT_RUN |

## HANDOFF

- Remaining blockers: response/catalog discrepancy, AC-26 ordering vs inventory cross-screen flow, slug→int64 course input, no pagination bound, unresolved business mapping for filter/search/submission/reminder fields, API #65 DD confirmation, live schema/deployment, Study Web UNWIRED.
- Completed this session: ME-16 plan, 42 markers/annotated image, A–F DD, tracker and worklog updates; static audit passed. Status `DD READY`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
- Next screen in the Mentor sequence: ME-17, only in a separate session. Stop after ME-16.
