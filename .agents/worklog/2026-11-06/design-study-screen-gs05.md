---
task_id: "2026-11-06-design-study-screen-gs05"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["GS-05 uses GS-03 courseId/API #08 as a public-course prerequisite and API #10 for public reviews/replies; API #10 is declared but not executable in current source"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study GS-05

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; selected 3 exact-type docs worklogs of 164 available; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Study Web is UNWIRED; preserve expected/current separation and don't claim backend tests or checked-in DDL prove runtime/live schema.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Keep mock/screenshot content distinct from API-supported fields; preserve original asset hashes; document route/query/cache behavior only when sourced.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: API #08/#09 are source-backed, but API #10 has no route/module/test; AC-05 eager flow differs from F02 lazy tab; no average rating/title source is established.
- Additional handoff read: `.agents/worklog/2026-11-06/design-study-screen-gs04.md` (not selected because the exact-type limit selected GS-01..GS-03 first); preserve one-screen-per-session scope, #09 remains source-backed but not access-approved, and GS-05 is the next tracker item.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete GS-05 only; write a per-screen plan before render/annotation/DD; preserve source assets; provide numbered image, marker map, source-traced DD, global tracker update and final worklog.
- Canonical inventory: Guest tab at `/courses/:courseId?tab=reviews`, AC-05, APIs #08/#10; show public reviews/replies, paginate #10, differentiate unpublished/missing course 404 from empty reviews, and do not show average stars without a rating contract. Link back to GS-03 with same `courseId`; expected states loading/empty/ready/error.
- Preserve the discrepancy that AC-05 asks for aggregate rating while GS-05 inventory and G-06 do not approve average stars without a rating schema/contract. F02 specifies lazy #10 by selected tab; AC-05 sequence is eager.

## CURRENT_BEHAVIOR

- Before edits, GS-05 directory had only original `screen.png` and `code.html`; hashes are recorded in `GS-05_PLAN.md`. PNG is 1280×1024, 24 colors, entropy 0.350263; visually nearly blank except the footer band. HTML is a static guest empty-review page with header, breadcrumb, icon, H1, empty copy, `href="#"` return link and footer; no review/reply card, pagination, API call, route binding or JS handler. All anchors use `#`.
- Current Study Web checkout contains docs/assets and a built `dist/` output but no application source/package manifest/entrypoint; the built bundle includes generic router symbols but string inspection found no `/courses` route or `/api/v1` endpoint. Subcontext remains `UNWIRED`.
- API #08 route/view/validator/query and test source exist. Current GET checks PUBLISHED course and returns a 404 for malformed, missing or unpublished IDs; its source response is singleton `Page<Course>`. Tests were read as source only; not run.
- API #10 exists in `docs/lists/list_api.md` and `apps/study-server/docs/dd/10_courses_reviews/`; no matching route/module/test file or route string was found under current Study Server `app/` or `tests/`. API #10 DD status is `Draft — Needs Confirmation` (`DECLARED_NOT_RUNNABLE`).
- Draft #10 proposes public GET `/api/v1/courses/{course_id}/reviews`, optional `page:int32` and literal “rating filter” with unresolved query key/semantics, `ApiEnvelope<Page<Discussion>>`, empty 200, 404 for invalid/missing/unpublished course, 500 system error. Nested replies and page size/order/status filters are design assumptions, not runtime facts.
- Draft item shape requires `title`, but `discussions.title` is absent from the checked-in legacy DDL; no rating column/table or aggregate response exists. `status='ACTIVE'`, root/reply relation and public visibility remain Draft assumptions. Live schema is unverified.

## SOURCE_TRACE

Source audit and final screen trace:

- Inventory GS-05/F02/G-06/API index and AC-05 diagram were inspected; AC-05 requests review plus aggregate rating, while GS-05 row explicitly forbids average stars absent a rating contract.
- API #08 current chain was re-read: route `/courses/{course_id}` → raw-string path → shared integer validator → PUBLISHED-course query/mentor projection → singleton `CoursePage` envelope; test file exists.
- API #10 was searched under current route/module/test source; no executable path/module/test found. Catalog and Draft API DD were read for declaration only.
- Current legacy DDL `discussions` has id/course_id/user_id/parent_id/content/status/created_at/updated_at; no title/rating. Static screen HTML has no handler and all links are `#`.
- Web UI-only DD has no canonical skill in manifest; `createDD-markdown` excludes this boundary. No API-DD skill is applied to this screen-only document.
- Per-screen plan was written before rendering/annotation/DD. Chrome headless render of `code.html` produced a separate 1440×1200 `screen_rendered.png`; original `screen.png` stayed unchanged. Nine markers were visually reviewed in a 2× gutter layout.
- Final DD describes 9 current elements and 8 sequential events, API #08 current source vs API #10 declaration/Draft DD, pagination/empty/error states, and expected/current navigation without claiming #10 runtime behavior.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| PNG vs HTML | PNG nearly blank; HTML shows static empty state only. | DISCREPANCY | Preserve both; render HTML separately for inspectable annotation only. |
| Study Web route/runtime | Current subcontext is `UNWIRED`; app source/router absent. | UNWIRED | Do not assert route, cache, handlers or deployed UI. |
| API #10 | Catalog/Draft DD only; no executable route/module/test found. | DECLARED_NOT_RUNNABLE | Do not write as a current backend call or verified response. |
| Review title/rating | Draft requires title but no DDL source; no rating/aggregate field or table. | DISCREPANCY / BLOCKER | No synthetic title, stars, rating filter or average. |
| Review visibility/replies | Draft assumes ACTIVE roots/replies and parent_id tree; no approved public/moderation policy. | ASSUMPTION / BLOCKER | Do not claim current public content policy. |
| Orchestration | AC-05 eager #08/#09/#10 vs F02 lazy tab; #08 cache semantics absent. | DISCREPANCY / OPEN | Preserve both; do not invent cache or request timing. |
| Source assets | hashes and content recorded in plan; no source files changed. | VERIFIED | Keep original unchanged. |

## CHANGES

- Files changed: GS-05 `GS-05_PLAN.md`, `GS-05.md`, `GS-05_markers.json`, `GS-05_markers_overlay.svg`, `screen_rendered.png`, `screen_annotated.png`; global `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; this worklog. Original `screen.png` and `code.html` preserved.
- CONTEXT_UPDATES: none planned; no current source/context ownership fact changed.
- Context pages changed: none.
- Assumptions: none; Draft-only API behavior and open policies are labeled as such.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/context/worklog preflight | Objective read; context map loaded; selector READY with three exact-type docs worklogs, all read; GS-04 handoff also reviewed; no shortage. | VERIFIED |
| GS-05 source trace | Inventory/AC-05, HTML/PNG, API #08 route source, API #10 Draft DD/catalog, source absence search, discussion DDL and Study Web wiring rechecked. | VERIFIED |
| GS-05 artifact/static audit | Passed: 9 ordered unique JSON markers match 9 DD element rows; 8 sequential event IDs; 8 relative links resolve; original PNG/HTML hashes unchanged; image dimensions 1280×1024 / 1440×1200 / 3040×2400; SVG has 9 circles/leaders/labels and embeds exact render; marker source/canvas bounds and side gutters pass; all 14 current HTML anchors remain `#`; inventory has 83 IDs and 83 matching folders; 12 complete sets; tracker says next GS-06. | VERIFIED |
| Visual review | Annotated preview visually inspected; all nine callouts align with visible elements and do not cover content. | VERIFIED |
| `git diff --check` | Passed after DD, plan and tracker edits; repeat after this worklog update. | VERIFIED |
| Tests/runtime | Not run. | NOT_RUN |

## HANDOFF

- Remaining blockers: API #10 runtime route/module/test; review title/rating schema and public visibility approval; loaded-state/error/pagination design; cache/orchestration; Study Web wiring.
- Next owner/action: GS-05 artifacts are complete with `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED`; continue at GS-06 in a separate session.
