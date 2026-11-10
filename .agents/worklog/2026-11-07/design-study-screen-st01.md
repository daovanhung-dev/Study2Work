---
task_id: "2026-11-07-design-study-screen-st01"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-01 dashboard widgets → APIs #20/#21/#38/#43 and AC-13/AC-18/AC-20"]
status: "PARTIAL"
---

# Worklog: Detailed Design màn hình Study ST-01

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 249 exact-type docs worklogs available, 3 selected, no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Separate expected behavior from current source; inspect route/API wiring; preserve mockup limitations and implementation/runtime statuses.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Do not infer user fields, route behavior or actions from static prototypes; source-backed API behavior and Draft contract remain distinct.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Keep cross-screen handoffs and unresolved role/data policy explicit; do not claim runtime/live schema from local source or test artifacts.
  - path: `.agents/worklog/2026-11-07/design-study-screen-st08.md` (supplemental)
    - carry_forward: APIs #20/#21 remain Draft and absent from Study Server; catalog returns UserProfile while AC-13 needs course/progress collections; AC-13 empty and merge semantics are unresolved; legacy BIGINT and V1-PILOT UUID progress models differ.
  - path: `.agents/worklog/2026-11-07/design-study-screen-st20.md` (supplemental)
    - carry_forward: Inventory calls #21/#38 independently while AC-18 sequences #21 → #37 → #38; do not infer orchestration order or page-entry timing.
  - path: `.agents/worklog/2026-11-07/design-study-screen-st22.md` (supplemental)
    - carry_forward: API #38 criteria/projection/filter/page semantics remain open; only backend-confirmed awards may be represented; Study Web is UNWIRED.
  - path: `.agents/worklog/2026-11-05/complete-study-screen-docs.md` (supplemental objective history)
    - carry_forward: Recheck all current source; ST-01 was the sole missing core bundle at its earlier checkpoint; legacy SH-01 draft is separate and does not replace ST-01.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ST-01 only; write `ST-01_PLAN.md` before marker map, annotation or DD; preserve usable source assets; create ordered one-to-one element markers; document A–F with source-traced events, data, states, navigation and blockers; update `list_screen.md`, `dd_screens/PLAN.md` and this worklog.
- Inventory row 15: Student overview at proposed `/student`; AC-13, AC-18, AC-20; APIs #20/#21/#38/#43; independent widgets with #20/#21 at entry and achievements/notifications lazy or parallel; links ST-08, ST-20, ST-26 and ST-02; loading/empty/partial-widget/403 states; P1; API design-only.
- Expected API catalog: #20 GET `/api/v1/users/me/courses`; #21 GET `/api/v1/users/me/progress`; #38 GET `/api/v1/users/me/achievements`; #43 GET `/api/v1/users/me/notifications`, each Student Bearer contract and design-only. Preserve each documented contract and its unresolved semantics; do not use the incorrect prototype URLs as API definitions.

## CURRENT_BEHAVIOR

- Source/config: Folder initially contained only `screen.png` (1067×1600; SHA-256 `8ac0708a12c0221ef529b26c3fc601d46405003476225fdc492475df8ed6b9cd`) and `code.html` (24,459 bytes; SHA-256 `f9870e9e6ec797ee96f340d663efaa9904ae1c5b5f3300be140575c50244770f`). The static HTML has Tailwind CDN/config, three Google Fonts imports and 13 `href="#"` anchors; no fetch/XHR/form/input/button/app handler. Its four endpoint paths differ from the API catalog. Current `apps/study-client` still has no editable `src`, package manifest or router; `dist` search found no `/student` or these four API paths.
- Current Study Server exact-path search found no #20/#21/#38/#43 route in `app/api/v1.py`, module source or tests. API DDs #20/#21/#38/#43 are Draft; each endpoint remains design-only and no runtime call was made.
- Runnable tests: Not run; this is a screen-documentation task.
- Runtime wiring: Study Web is `UNWIRED`; APIs #20/#21/#38/#43 are `NOT_FOUND` in current Study Server source. No deployed UI, API or live DB claim is made.

## SOURCE_TRACE

```text
Inventory ST-01 → Student entry → #20 courses / #21 aggregate progress → #38 achievements and #43 notifications per inventory's independent-widget note
AC-13: #20 Enrollment/Course then #21; client merge and empty branch
AC-18: #21 → select course → #37 → #38 → render progress/achievement
AC-20: #43 list → unread badge/list → optional #44/#45 read actions (outside ST-01)
Current: static gated HTML only; no Study Web route; #20/#21/#38/#43 Study Server route/module/query/test not found
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #20/#21 response and merge | Catalog/Draft returns UserProfile; AC-13 requires Course and progress data; query/empty/identity rules remain open. | `DISCREPANCY`; Draft; `NOT_FOUND` | No course or progress mapping/formula can be claimed. |
| AC-13 empty branch | Both EMPTY and HAS DATA edges target the same render node. | `DISCREPANCY` | Empty-state transition is not implementable from the diagram as written. |
| API #38 projection | Page<Achievement> is catalog-only; award criteria, fields' source, filter and pagination remain open. | Draft; `NOT_FOUND` | Do not show certificate/proof claims or synthesize earned rows. |
| API #43 latest/list projection | Notification fields and recipient mapping have source gaps; latest sort is unconfirmed; API contract says the `/users/me/notifications` page, not prototype `/notifications/latest`. | Draft; `NOT_FOUND`; `DISCREPANCY` | Cannot promise “latest” ordering, unread mapping or rendering fields. |
| Request orchestration | Inventory says independent #21/#38 widgets; AC-18 sequences #21 → #37 → #38. | `DISCREPANCY` | Keep each widget blocked and do not infer call order. |
| Prototype routes and visual system | All links use `#`; API matrix URLs are wrong; remote fonts/CDN, 1440px container and cobalt colors diverge from Study Web guide. | `DESIGN_ONLY / DISCREPANCY` | No current navigation/runtime; alignment decision needed before implementation. |

## CHANGES

- Files changed: `ST-01_PLAN.md`, `ST-01_markers.json`, `ST-01_markers_overlay.svg`, `screen_annotated.png`, `ST-01.md`, `apps/study-client/docs/list_screen.md`, `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`, this worklog. Original `screen.png` and `code.html` were preserved byte-for-byte.
- Order: `ST-01_PLAN.md` was written before marker JSON, SVG/annotation and DD.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: None; unresolved API and flow decisions stay blockers.

## VERIFICATION

| Check | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Objective and router/map/worklog instructions read; selector READY 3/249; selected AD-01/AD-02/AD-03 and supplemental ST-08/ST-20/ST-22/history logs reviewed. | `PASS` |
| Source/contract review | Inventory, source HTML/PNG, API catalog and Draft DDs #20/#21/#38/#43, AC-13/18/20, Study Web design target and current Study Server route/module/test source checked. No app route or API route/module/query/test for the four endpoints; Study Web route absent. | `PASS_STATIC_REVIEW` |
| Plan before authoring | Plan file authored before marker JSON/SVG, annotated image and DD. | `PASS` |
| Source asset / annotation audit | Original source hashes unchanged; source PNG 1067×1600; annotated PNG 1227×1680; annotation visually reviewed. | `PASS` |
| Marker/DD/event audit | 37 sequential unique marker IDs = 37 element rows = 37 SVG labels; bounds valid; 10 ordered events each have Trigger, Element/precondition, Input, Xử lý, Output and Ngoại lệ; sections A–F present. | `PASS` |
| JSON/SVG/links | JSON parses; SVG XML parses at 1227×1680; DD/plan local links resolve. | `PASS` |
| Inventory audit | 83 inventory IDs = 83 matching folders; all 83 now have four core artifacts (annotated PNG, DD, plan, marker JSON). | `PASS` |
| Whitespace | Scoped `git diff --check` on tracked inventory/global plan; authored DD/plan/worklog trailing-whitespace scan clean. | `PASS` |
| Application tests/runtime/live DB | Not requested/performed. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: #20/#21 response, merge/formula/identity/empty semantics; #38 award projection/filter/page rules; #43 recipient/fields/order; AC-13 empty branch and AC-18 ordering; Study Web route/client and APIs #20/#21/#38/#43 are absent; prototype endpoint paths and visual system diverge from canonical sources.
- Session outcome: ST-01 artifacts and trackers updated; `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. No application tests/runtime/live DB verification.
- Next owner/action: Stop after ST-01. The global plan's next W0 candidate is SH-01, to be handled in a separate session.
