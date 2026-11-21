---
task_id: "2026-11-06-design-study-screen-st08"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-08 API #20/#21 contract", "Student session handoff from SH-02", "navigation to ST-09/ST-20"]
status: "BLOCKED"
---

# Worklog: Complete ST-08 screen DD

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: READY; 3/169 exact-type docs worklogs selected.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Keep Study Web UNWIRED; distinguish inventory/mockup expectations from current source; no tests unless requested; handle one Screen ID per session.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Preserve original asset hashes; don't infer runtime from static HTML/PNG; report API source status from route/module/query/test evidence.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: Separate expected/current behavior; keep unconfirmed API fields and UI states blocked; update only the relevant screen and tracker.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: ST-08 is the Student's enrolled-course page. Inventory expects course listing, status filter and progress; route `/student/courses`; AC-13; APIs #20/#21; links to ST-09 and ST-20.
- Canonical contract/approved DD: `apps/study-client/docs/list_screen.md`; AC-13 in Study Server API index/diagram; API catalog rows #20/#21. API #20/#21 DDs are Draft — Needs Confirmation, so unresolved response/query details remain blockers.

## CURRENT_BEHAVIOR

- Source/config: Study Web has no app source/router/entrypoint in this checkout. ST-08 HTML is static empty state with header/nav/footer anchors; source PNG omits the header and has a black band below the footer. Static Firefox render was used as the clean annotation base. Study Server search for the #20/#21 routes/module names in `app` and `tests` returned no matches.
- Runnable tests: No #20/#21 endpoint tests found by source search; tests were not run per the goal instructions.
- Runtime wiring: API #20/#21 are catalog/DD declarations only (`ApiEnvelope<UserProfile>`); endpoint runtime is NOT_FOUND in current source. ST-08 UI route/API calls are UNWIRED. Runtime NOT VERIFIED.

## SOURCE_TRACE

```text
list_screen ST-08 / AC-13 / API catalog
  -> expected GET #20 enrolled courses
  -> expected GET #21 progress (conditional in inventory, required in AC-13)
  -> expected merge by course_id
  -> API #20/#21 route/module/query/test lookup: no source found
  -> DB.sql candidate DDL only; live schema/query not verified
  -> static ST-08 code.html: empty-state markup and anchors; no app/router/API behavior
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #20/#21 response types | Catalog/DD Draft say `ApiEnvelope<UserProfile>`; AC-13 expects course and progress data. | DISCREPANCY; NOT_FOUND in current endpoint source | Cannot define list/progress mapping or DD READY. |
| API #20 query | `status?:string`, `page?:int32`; enrollment-vs-course status, enum/default, paging/order unresolved. | DECLARED_ONLY; Draft | Filter and page behavior blocked. |
| API #21 query/aggregation | Catalog phrase `course_id list hoặc aggregate?:string`; response and formula unresolved. | DECLARED_ONLY; Draft | Cannot request/merge or calculate progress safely. |
| UI loaded/filter states | Inventory expects list/filter/progress; HTML/PNG show static empty state only. | DESIGN GAP; Study Web UNWIRED | Missing card, filter, loading, partial and error designs. |
| Navigation | HTML anchors point to `/student`, `/student/courses`, `/student/progress`; no router source. ST-09 card absent. | EXPECTED DESIGN; runtime unverified | Route resolution and courseId handoff are blocked. |
| Original PNG | Header absent and large black band below footer; static HTML render includes full page. | SOURCE ASSET INCOMPLETE | Preserve original; use documented `screen_rendered.png` for annotation. |

## CHANGES

- Files changed: ST-08 plan (added expected ST-09 card event); ST-08 DD; global `dd_screens/PLAN.md`; this worklog. Existing marker JSON/SVG, `screen_rendered.png` and `screen_annotated.png` were created earlier in this ST-08 session from the plan. Original `screen.png` and `code.html` preserved.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none added. Course-card navigation and status-filter event are documented as expected but unavailable in current assets.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Python static audit of `ST-08.md`, `ST-08_markers.json`, `ST-08_markers_overlay.svg`, and image files | All relative links resolve; marker order is 1–9 with 9 matching DD rows and 9 SVG circles; original PNG/HTML and rendered-image hashes match marker metadata; dimensions are source/render 1280×1024 and annotated 2720×2048; SVG embeds the rendered source hash; no trailing whitespace. An initial pass found one bad global-plan link, corrected to `../../dd_screens/PLAN.md`, then rerun successfully. | PASS |
| `git diff --check` | No whitespace errors in tracked diffs. | PASS |
| Visual review of `screen_annotated.png` | All nine markers remain in side gutters and point to the intended visible elements without obscuring the page content. | PASS |
| Tests/runtime | Not run; no tests were requested and static assets do not establish runtime behavior. | NOT RUN |

## HANDOFF

- Remaining blockers: Confirm #20 course payload/filter/paging/empty response; #21 query/progress schema/formula/empty response; AC-13 vs inventory request order; loaded-state/filter design; Student identity binding; Study Web router/API wiring.
- Next owner/action: Resolve API/business contracts and loaded-state design; next screen in W1 order is ST-09, to be handled in a separate session.
