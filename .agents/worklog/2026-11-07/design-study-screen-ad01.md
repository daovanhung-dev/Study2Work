---
task_id: "2026-11-07-design-study-screen-ad01"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AD-01 Study LMS admin route /admin and API #101 / AC-38; dashboard data and navigation to AD-02, AD-06, AD-24"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-01

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 206; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-me17.md`
    - carry_forward: Preserve expected/current separation; don't infer routes or data mapping from mockups; trace caller through backend, tests and response; keep Study Web UNWIRED and AC/API discrepancies explicit.
  - path: `.agents/worklog/2026-11-07/design-study-screen-me18.md`
    - carry_forward: UI-only DD has no canonical skill; preserve original assets; do not map screenshot KPIs to backend fields without evidence; test source/fake DB does not prove runtime or live schema.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Treat Study Web route/runtime as UNWIRED unless current editable source proves otherwise; distinguish API catalog from current server behavior; don't claim tests were run.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-01 only in this session; write its plan before marker map, annotation or DD; preserve original assets; create ordered one-to-one markers and annotated image; author the A–F screen DD with traceable events, APIs, states and navigation; update `list_screen.md`, `dd_screens/PLAN.md` and this worklog; distinguish `DD READY`, `IMPLEMENTATION BLOCKED` and `RUNTIME VERIFIED`.
- Inventory row 59: AD-01 “Dashboard quản trị”, proposed route `/admin`, AC-38, API #101 `GET /api/v1/admin/reports/summary` with `from`/`to`; system overview by date range with student/course/impact KPIs; expected `loading/partial/no-data/error`; links AD-02, AD-06 and AD-24; P1; inventory blocker says admin role-profile endpoint is missing.
- AC-38: actor Admin; precondition is permission to view report/analytics; postcondition is an aggregate report displayed or exported. Diagram order is open dashboard → #101 KPI summary → #102 community impact → optional #103 export.
- API #101 catalog/DD: `GET /api/v1/admin/reports/summary`, Bearer JWT / role Admin, optional `from?:date`, `to?:date`, no body, direct `ApiEnvelope<Report>`, 200 `DESIGN_RESOURCE_RETRIEVED`, and 401/403/500. `Report` has `period`, `metrics[]`, `generated_at`; keys/formulas/default date range/empty behavior remain open. Four timestamp counts in the API DD are `DERIVED`, not approved.

## CURRENT_BEHAVIOR

- Assets: original `screen.png` is 1600×1594, SHA-256 `93304b0a9846047a5e21a90bdb44fb197d4449e9dc725ec13b4239f416a0c25f`; `code.html` is 26,680 bytes, SHA-256 `e9c678cee115f8ac83b9d73779420005d411ad7918846696ff4c6fe8484df979`. Screenshot has four placeholder KPI cards, activity/audit panel, server-status panel, Admin identity and quick links.
- HTML: five primary nav anchors and three footer anchors use `href="#"`; three date-range buttons and audit-log button are disabled; refresh click only rotates its icon for 700 ms with a local timer; notification has no listener. Three quick links use `/admin/users`, `/admin/courses`, `/admin/content/pending`, but no Study Web router exists. No API request or data mapping exists in the HTML. Status, identity, audit, ISO and infrastructure claims are static copy.
- Study Web: current root contains `docs/`, ignored `dist/`, and `node_modules/`; editable source/package manifest is absent. `dist/index.html` is the only built file and no `/admin` or report-summary route string is present. Runtime/serving is unverified; UI is `UNWIRED`.
- Study API: current `app/api/v1.py` and admin module tree compose APIs #68–#98; #101, `/admin/reports/summary`, and a corresponding test/module are absent. API #101 catalog and DD remain declared/Draft only. No local aggregation query, response mapping, or side effect exists to trace.
- Existing Admin APIs #68–#98 use shared Bearer/JWT role validation with `ADMIN`; shared helper accepts an explicit role or role list. This current source contradicts the older #101 DD statement that the shared helper only supports Student. It does not establish #101 authorization or a report-specific permission policy.
- Profile gap remains: current `GET /api/v1/users/me` explicitly requires role `STUDENT`; no `/admin/me` or Admin profile route is declared. Do not map the static Admin name/avatar to #69 without an approved current-user ID carrier.
- API #101 DD is `Draft — Needs Confirmation`; generic response shape is direct, while four candidate count metrics/date defaults/authorization policy/empty semantics are `DERIVED` or open. No API #101 test was found by scoped search; no tests were run.

## SOURCE_TRACE

```text
Expected: `/admin` → GET #101 with optional `from`/`to` → Admin/report authorization → date-window resolution and approved aggregate source → `ApiEnvelope<Report>` → render selected metrics; AC-38 continues to #102 or optional #103.
Current: no Study Web route/client caller → no #101 route/module/query/model/test → no current aggregate side effect or response; existing unrelated Admin APIs #68–#98 use the shared ADMIN guard. Current `/users/me` is Student-only.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #101 runtime | Catalog row and Draft DD exist; router/module/test search and source inventory stop at API #98. | `UNWIRED / NOT_FOUND` | No client can call #101 today; runtime success/error mapping is not verified. |
| Admin authorization vs profile | Current #68–#98 guards support `ADMIN`; API #101 report permission is still open; `/users/me` is Student-only and no `/admin/me` route exists. #101 DD's “Student-only helper” statement is stale. | `DISCREPANCY / BLOCKER` | Do not claim #101 is protected or render Admin identity from an inferred endpoint. |
| KPI mapping and period | Catalog `Report` is generic; API DD's four created-row counts/default 30-day range are `DERIVED`; screenshot's users/active-course/moderation/system-load values have no approved mapping. | `OPEN / BLOCKER` | No KPI formula, label, unit, date default, partial or empty rule can be finalized. |
| Static operational/audit claims | Prototype states system normal, readiness, database/auth/queue status, audit empty, ISO compliance; no relevant #101 fields or current screen API. | `STATIC_ONLY / UNMAPPED` | Do not present these as live system checks or audited behavior. |
| UI wiring and design source | Study Web route/source absent; placeholder nav/footer links, disabled filters/audit button and timer-only refresh; screenshot uses different palette/font than Study Web guide. | `UNWIRED / DESIGN DISCREPANCY` | No implemented route/event; reconcile mockup with canonical design guide before frontend implementation. |

## CHANGES

- Files changed: `apps/study-client/docs/screen_stitch/05_admin/AD-01_dashboard-quan-tri/AD-01_PLAN.md`, `AD-01_markers.json`, `AD-01_markers.svg`, `screen_annotated.png`, `AD-01.md`; `apps/study-client/docs/list_screen.md`; `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; this worklog.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none; unresolved product/API decisions remain blockers, not assumptions.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | `READY`; reviewed ME-17, ME-18 and GS-01 worklogs. | VERIFIED |
| Objective/router/context/worklog preflight | Objective read; root router/context-map/worklog contract loaded; exact docs selector `READY` 3/206; ME-17, ME-18, GS-01 fully reviewed; manifest confirms no canonical skill for UI-only DD. | VERIFIED |
| AD-01 source/asset/API/AC trace | Inventory, AC-38, API catalog/#101 Draft DD, source HTML/PNG, Study Web tree/dist, Study router/admin modules/test inventory, Admin role guard, Student profile guard and `/health/ready` source reviewed. #101 has no current route/module/query/model/test. | VERIFIED |
| Marker/DD static audit | Source hashes preserved; PNG 1600×1594; annotated PNG 3200×3188; 35 ordered/in-bounds marker IDs align across JSON/SVG/DD rows; A–F, EV-01…EV-08 and all relative DD links checked; final image viewed directly. | VERIFIED |
| Artifact inventory | 83 screen folders; 54/83 have all four core artifacts after AD-01. | VERIFIED |
| Authored text / `git diff --check` | Authored files have no trailing whitespace; `git diff --check` exited 0. | VERIFIED |
| Application tests/runtime | Not run. | NOT_RUN |

## HANDOFF

- Remaining blockers: API #101 is D/UNWIRED; KPI and range semantics; Admin report permission and self-profile mapping; audit/service status sources; Study Web route; screenshot/design-system discrepancy. See `AD-01.md` §F.
- Session outcome: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. No application tests/runtime claim.
- Next screen candidate: AD-02, in a separate session; this session stops after AD-01.
