---
task_id: "2026-11-06-design-study-screen-me01"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: ["test"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["Study Web ME-01 dashboard uses current Study Server APIs #46/#54/#58; all require MENTOR JWT and the Study Web client/router is UNWIRED"]
status: "VERIFIED"
---

# Worklog: Detailed Design Study ME-01 — Dashboard mentor

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; selected 3 exact-type docs worklogs of 177; all selected worklogs were read.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Keep expected screen design distinct from current API/source; source PNG/HTML are static; Study Web remains UNWIRED; preserve original assets and mark unsupported widget fields/routes as blockers.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Do not promote catalog/diagram claims to runtime behavior; current API filters/pagination may differ from mockup; one Screen ID per session and current source wins for CURRENT_BEHAVIOR.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: Trace route/view/query/mapping and tests separately; preserve AC vs inventory navigation discrepancies; no runtime claim from static HTML or fake-row tests.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ME-01 only in this session; author its plan before marker image/DD, preserve source assets, map every marker to one DD element, trace events/APIs/routes to source, update `dd_screens/PLAN.md` and this worklog; report DD/implementation/runtime states separately.
- Objective: `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md` — detailed screen DD needs plan, annotated image, marker map, source trace, event/state/navigation details and explicit blockers; one Screen ID per session.
- Canonical screen inventory: `apps/study-client/docs/list_screen.md` ME-01 row proposes `/mentor`, AC-21/23/24, APIs #46/#54/#58, linked ME-02/ME-09/ME-11 and independent loading/partial/empty/error widget states. AC-21/23/24 diagrams cover lecture creation, grading and support flows, not all screenshot dashboard widgets.
- Skill routing: `.agents/context-manifest.json` excludes `web-ui-only-dd` from `createDD-markdown`; no registered UI-only skill was used.

## CURRENT_BEHAVIOR

- Source/config: Preserved `screen.png` is a 1086×1600 raster design sample (SHA-256 `f135d0b109a05d276654a6b8b51545d9f2996ab474c47b7829c9983739eea3d2`). `code.html` is 52,234 bytes (SHA-256 `f10dfa929e89288165bf0264b1b1f863f2380006d064f8e470118a7cfe626334`). Main layout and content correspond, but values are sample data. HTML has 24 `href="#"` anchors, static input/buttons, no app handler/API/router. Current `apps/study-client/` has docs/dist/tsbuildinfo only, no `src/` or `package.json`; dist bundle route search found only `/`.
- Study Server: route/module source exists for #46/#54/#58. #46 pages direct `courses.mentor_id` ownership and returns Course summary/page. #54 returns a fixed 20/page Submission projection with exact `status` string but no pending/due-date/student display contract. #58 returns every owned SupportRequest with full messages/attachments and no pagination; model/schema choices are derived and live schema is unverified.
- Tests: test source for all 3 APIs was inspected for success/empty/auth/validation/error branches; no tests were run. API #54/#58 tests use fake DB projections; no live database check was done.
- Runtime wiring: Study Web remains `UNWIRED`; no client route/session/API caller or deployed UI was verified. API source and test files do not imply live deployment/database availability.

## SOURCE_TRACE

```text
GET /api/v1/mentor/courses
  -> app/api/v1.py:mentor_courses
  -> api_46_mentor_courses.view.get_mentor_courses
  -> validate_current_user_request(role=MENTOR) + query status/page/size
  -> count/list courses where courses.mentor_id = JWT sub, LEFT JOIN users
  -> map Course + Pagination -> 200 DESIGN_RESOURCE_RETRIEVED; safe 401/403/422/500

GET /api/v1/mentor/submissions
  -> app/api/v1.py:get_mentor_submissions_list
  -> api_54_mentor_submissions_list.view.get_mentor_submissions
  -> MENTOR guard; optional course/status exact filters; page default 1, size fixed 20
  -> count/list assignment_submissions -> assignments -> courses -> users; optional UploadAsset exact-URL mapping
  -> SubmissionPage + Pagination -> 200 DESIGN_RESOURCE_RETRIEVED; safe 401/403/422/500

GET /api/v1/mentor/support/requests
  -> app/api/v1.py:get_mentor_support_requests_list
  -> api_58_mentor_support_requests.view.get_mentor_support_requests
  -> MENTOR guard; optional course/status exact filters
  -> list owner-scoped support_requests, then all message/upload rows if requests exist
  -> SupportRequest[] full-thread envelope -> 200 DESIGN_RESOURCE_RETRIEVED; safe 401/403/422/500
```

Source trace was checked in `app/api/v1.py`, `app/utils/auth.py`, each API module's models/query/view, shared Course mapper/models, relevant migration/database context and test source. #54 assignment/upload projection and #58 support tables/thread response are `DERIVED` implementation fallbacks; checked-in DDL/migration and fake tests do not prove production schema.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Study Web runtime | Current checkout has no editable source/package/router; compiled dist has only root route. | UNWIRED | Do not claim `/mentor` or any UI interaction works. |
| API inventory status | Inventory/API DD snapshots label #46/#54/#58 D/Draft; current routes/modules exist. | DISCREPANCY | Current source status is separate from contract approval/live runtime. |
| Course ownership | #46/#54 filter by direct `courses.mentor_id`; no assigned-mentor mapping is used. | DISCREPANCY | “Owned/assigned” requires a scope decision before course coverage claims. |
| Dashboard mockup | Rating, active learners, overdue/SLA, schedule, notices, unread count, user profile/title and card metadata lack the referenced API fields. | NOT_FOUND / DESIGN GAP | Do not display sample values as dynamic data; DD remains blocked. |
| #54 dashboard preview | Page size fixed at 20; status is an unvalidated exact string; no “pending”, due date, assignment title or student summary. | SOURCE_BACKED_WITH_DERIVED_PROJECTIONS | The screenshot list/KPI cannot be mapped fully. |
| #58 support preview | Returns all full threads without pagination or summary; no subject, unread count, SLA or last-activity field. | SOURCE_BACKED_WITH_DERIVED_PROJECTIONS | Need an approved projection/volume decision before implementing as a compact dashboard list. |
| CTA flow | Image labels direct actions ME-10/ME-12; AC/inventory flow lists ME-09/ME-11 first. | DISCREPANCY | Product must choose direct detail vs list-first. |
| Design system | Prototype uses `#004ac6`, remote Plus Jakarta Sans, CDN Tailwind, large hero gradient and 40px controls; guide specifies different tokens/font/accessibility baseline. | DESIGN DISCREPANCY | Reconcile when implementation design is approved; no source asset was modified. |

## CHANGES

- Files changed: `apps/study-client/docs/screen_stitch/04_mentor/ME-01_dashboard-mentor/ME-01_PLAN.md`, `ME-01.md`, `ME-01_markers.json`, `ME-01_markers_overlay.svg`, `screen_annotated.png`; `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; this worklog.
- Original `screen.png` and `code.html` were preserved; their hashes were rechecked after annotation.
- CONTEXT_UPDATES: None. No API/runtime/DB context page or implementation source changed.
- Context pages changed: None. Worklog only under `.agents/worklog/`.
- Assumptions: None. Unsupported visual values and destinations were kept as sample/blocked content.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` + selected-file review | Selected/read GS-01/GS-02/GS-03 worklogs; 177 exact-type docs available; no shortage. | VERIFIED |
| API/source/AC trace | #46/#54/#58 route, auth guard, query, mapping, response/error and test source were read; current code distinguished from API DD/design snapshots. Tests not executed. | VERIFIED_SOURCE_REVIEW |
| Source asset audit | `file` reports PNG 1086×1600; original screenshot/HTML hashes unchanged; static HTML has 24 placeholder anchors. | VERIFIED |
| Annotation/marker audit | 23 sequential unique markers; 23/23 `ME01-EL-01..23` DD rows; 12 sequential Event IDs; 23 SVG groups/circles/texts; coordinate bounds valid; annotated PNG 2172×3200 at 2× same aspect ratio. | VERIFIED |
| Visual review | `screen_annotated.png` opened and inspected; numbers are legible, grouped near targets and do not cover primary text/controls. | VERIFIED |
| Link/whitespace audit | Every relative link in ME-01 DD/plan resolves; new DD/plan/JSON/SVG have no trailing whitespace. `git diff --check -- apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` passed. | VERIFIED |
| Global artifact count | Static presence count is 26/83 core packs; current list includes ME-01. This is file presence, not DD READY count. | VERIFIED |
| `node scripts/validate-agent-context.mjs` | Exit 1; reported 49 global findings, including missing db-admin context/source and stale source inventories for server-study/db-admin. No context pages/manifest were changed in this task. | BLOCKED_BY_EXISTING_CONTEXT_BASELINE |
| Runtime/tests | No tests or runtime flows were run. | NOT_RUN |

## HANDOFF

- Screen status: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
- Remaining blockers: ME01-B01–ME01-B12 in `ME-01.md`; especially Mentor session/bootstrap, data projections for the mockup, pending/deadline policy, unpaged full support threads, unsupported rating/calendar/notices/profile data, and direct-vs-list CTA routes.
- Next owner/action: ME-02 — process in a separate session within `screen_stitch/04_mentor`; do not begin ME-02 in this session.
