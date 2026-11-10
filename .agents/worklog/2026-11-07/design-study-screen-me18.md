---
task_id: "2026-11-07-design-study-screen-me18"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ME-16/ME-17/ME-18 orchestration through APIs #65/#66/#67 and AC-26 ordering discrepancy"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ME-18

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 205; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-me17.md`
    - carry_forward: Keep ME-16/#65, ME-17/#67 and ME-18/#66 separate; preserve the AC-26 ordering discrepancy; do not infer a selected-student/course ID carrier or merge #66 into student progress; DD/implementation/runtime statuses remain distinct.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Preserve source assets and expected/current separation; Study Web remains UNWIRED; API/source and design discrepancies must remain explicit; tests/fake rows do not prove runtime or live schema.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Do not infer routes, cache, response mapping or filter behavior from a prototype; inspect server caller/callee/effects/errors; keep screen DD blockers distinct from current source behavior.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ME-18 only in this session; write its plan before markers, annotation or DD; preserve original assets; make ordered one-to-one markers; author A–F DD with traceable events/API/states/navigation; update inventory/global plan/worklog; distinguish `DD READY`, `IMPLEMENTATION BLOCKED`, and `RUNTIME VERIFIED`.
- Inventory row 58: ME-18 “Analytics khóa học”, proposed route `/mentor/courses/:courseId/analytics`, AC-26, API #66; course performance/completion charts based on backend KPIs; metric definitions, period and aggregation remain TBD; expected states loading/no-data/ready/error; linked from ME-16; status currently D.
- Cross-screen dependency: Inventory separates ME-16/#65 → ME-17/#67 and ME-18/#66. AC-26 diagram sequences #65 → #66 → select Student → #67. Keep this as a discrepancy and do not reconcile by assumption.

## CURRENT_BEHAVIOR

- Assets: original screen.png is 1600×1380 RGB, SHA-256 `8141f4a9670d5a41a82016613928a6abbbfd82ad50bc84049645cbe2a565bb8f`; code.html is 17,676 bytes, SHA-256 `45bc8a7c267a2de2c73a1bedc9b170620334f29b4fe1f89a2e3cd7bd7d367564`. Source assets remain unchanged. Screenshot depicts disabled 7/30-day/all-course timeframe and CSV export, three empty KPIs, an inactive-analysis empty state, back-to-ME-16 anchor and “check sync” control.
- HTML: 13 placeholder anchors (`href="#"`); timeframe select is disabled and exposes 7 days/30 days/all-course options; CSV button is disabled; no forms, tables, chart data rows, fetch/Axios/XHR or route wiring. “Kiểm tra đồng bộ lại” has inline JS only: changes button copy to “Đang gửi lệnh...” for 1.2 s, then “Đã ghi nhận yêu cầu” for 3 s, then restores original HTML. It sends no request or state to server.
- Study Web: context and rechecked tree show no editable src/package manifest/feature route; compiled dist is not runtime evidence; status UNWIRED.
- API #66 route: GET `/api/v1/mentor/courses/{course_id}/analytics`, raw path + Authorization, required signed-int64 course_id; no query/body/page-size. Shared Bearer/JWT guard requires role MENTOR before DB. It parses path to int64; malformed/out-of-range → 404. Course lookup missing → 404; direct-owner mismatch → 403 before aggregate. Local SQL repeats owner predicate and aggregates distinct pairs of (user_id, lesson_id) where lesson is PUBLISHED, user role is STUDENT and last_accessed_at is non-null. It does not require ACTIVE enrollment.
- API #66 local response is ApiEnvelope<MentorCourseActivityAnalytics>: tracked_lesson_accesses (distinct Student/lesson progress pairs, not event count), students_with_activity (distinct Student IDs in those pairs, not enrollment count), last_activity_at (MAX stored last_accessed_at or null). This is an all-time current-state proxy; overwritten accesses cannot be reconstructed. Empty aggregate returns 0/0/null. No event ledger, time window, metrics for completion/average duration/discussion, export or write is present.
- Catalog and AC-26 still declare ApiEnvelope<Page<Course>>. API #66 DD is Draft — Needs Confirmation; local object/owner scope/aggregation are DERIVED. Errors locally: 401 auth required, 403 role/owner, 404 bad/missing course, 500 safe internal error with data null. Focused test source has 18 parameter-expanded cases using fake DB and is read but not run; it covers auth, owner, malformed int64, empty aggregate, invalid projection, safe query failure, read-only and OpenAPI. No live DB/deployment verified.

## SOURCE_TRACE

- Expected screen path: inventory ME-16 → ME-18/#66 with numeric course_id, while AC-26 diagram is #65 → #66 → choose Student → #67. ME-16 DD has a “View course analytics” placeholder event that says not to fetch #66 from ME-16 until flow ordering is approved. Preserve the inventory/diagram conflict.
- Current server chain: `app/api/v1.py` GET route → shared MENTOR auth → signed-int64 parse → course lookup/direct `courses.mentor_id` check → aggregate SQL over `lesson_progress`, `lessons`, `users`, `courses` → validated local response summary or safe 401/403/404/500. The query is read-only; no server-to-server #65/#67 calls.
- API #66 model/validator/query/view, Draft DD sheets/open questions, direct catalog row, AC-26 diagram, DB context and focused test source were reviewed. Legacy DDL has current progress/access state but no learner event ledger; V1-PILOT facts/snapshots are not read. No live schema claim.
- Current UI source is a static mockup; empty state and “waiting sync” claims are not returned by #66. None of the three named KPIs map to the three local proxy fields. Disabled timeframe/export controls have no active event; sync click is local cosmetic text/timer only.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #66 success response | Catalog/AC say `ApiEnvelope<Page<Course>>`; local source returns singular summary object. | DISCREPANCY / DRAFT | Do not implement a client mapping until API owner resolves. |
| KPI/schema and time range | Inventory says definitions/period/aggregation TBD; screen names completion, avg duration and discussion interaction; #66 returns current-state pair count, distinct student count and last timestamp, with no query window. | OPEN / BLOCKER | No chart/KPI mapping, timeframe behavior or export can be inferred. |
| Analytics event semantics | AC says aggregate learning events; current DDL/API only expose latest progress access markers. | DISCREPANCY / DERIVED | Do not label proxy counts as event count, repeat access or discussion interaction. |
| Empty/inactive state | Screenshot says “Chưa kích hoạt”/ETL waiting; #66 returns zero/null for empty proxy but has no pipeline activation flag. | STATIC_ONLY / UNMAPPED | Cannot distinguish inactive pipeline from no tracked progress rows. |
| Course identity/access | Inventory route needs courseId; #66 needs int64 and direct owner; ME-16 link is placeholder, selection carrier unresolved. | DERIVED / BLOCKER | Need numeric ID and owner/assignment policy before load. |
| Prototype interactions | Timeframe and export are disabled; sync handler only mutates button markup/timers; navigation hrefs are placeholders. | UNWIRED | No route, refresh, filter or export is implemented. |
| Runtime/schema | Study Web is UNWIRED; tests use fake DB; API #66 DD is Draft. | UNVERIFIED | No runtime/live schema/deployment claim. |
| AC-26 orchestration | Diagram puts #66 before Student selection/#67; inventory places #66 on ME-18 separate from #67 on ME-17. | DISCREPANCY | Flow owner must resolve without changing either source silently. |

## CHANGES

- Wrote `ME-18_PLAN.md` after source/context trace and before marker map, annotation or screen DD.
- Created `ME-18_markers.json`, `ME-18_markers.svg`, `screen_annotated.png` (35 elements) and `ME-18.md` sections A–F with EV-01…EV-06, API/status/error mappings, states/navigation, and open decisions.
- Updated ME-18 inventory and API #66 source classification D→R in `list_screen.md`; updated ME-18 row and projected core-artifact count in `dd_screens/PLAN.md`.
- Original `screen.png` and `code.html` preserved. No context page changed; no API/server source changed.
- Skill routing: registry says `createDD-markdown` targets API DD and excludes `web-ui-only-dd`; this artifact is a screen UI DD, so no canonical skill applies and none was invoked.
- Assumptions: none. DD remains blocked on API/KPI/period/loaded-state decisions.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Goal/router/context/worklog preflight | Objective reread; docs selector READY 3/205; ME-17, GS-01, GS-02 selected worklogs fully read. | VERIFIED |
| ME-18 source trace | Inventory, AC-26, #66 source/model/query/view, Draft DD/open questions, DB context, focused fake-DB test source and screen HTML/image reviewed. | VERIFIED |
| Source asset hashes | screen.png `8141f4a9670d5a41a82016613928a6abbbfd82ad50bc84049645cbe2a565bb8f`; code.html `45bc8a7c267a2de2c73a1bedc9b170620334f29b4fe1f89a2e3cd7bd7d367564`; unchanged. | VERIFIED |
| Marker/DD static audit | 35 ordered unique in-bounds markers; 35 rows exact 1:1; JSON/XML parse; annotated PNG 1600×1380; all DD local links resolve; final image visually reviewed. | VERIFIED |
| Artifact inventory | 83 screen folders; 53/83 have all four core artifacts after ME-18. | VERIFIED |
| `git diff --check` | Passed. | VERIFIED |
| Application tests/runtime | Not run; no live-schema/runtime claim. | NOT_RUN |

## HANDOFF

- Remaining blockers: catalog Page<Course> vs local analytics-summary shape; KPI/data source/formulas; period/window; event history vs current-state proxy; empty/ETL meaning; export and sync command; numeric course_id carrier and owner policy; AC-26 order; Study Web UNWIRED; live schema/deployment.
- Session outcome: artifacts and trackers complete; `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`.
- Next candidate screen is AD-01 per current global screen plan; process only in a separate session.
