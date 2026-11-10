---
task_id: "2026-11-06-design-study-screen-gs04"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["GS-04 uses Study API #09 for curriculum data and preserves courseId from GS-03; lesson click/access behavior may connect to ST-10 and must follow an approved contract"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study GS-04

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 163; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Keep the Study Web runtime `UNWIRED`; trace API and current UI independently; don't infer lesson/card flows from a static screen.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Preserve expected/current separation, route proposals, image/HTML mismatches and explicit UI blockers; don't infer routing/cache/runtime.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: API #09 is source-backed but its current query exposes only PUBLISHED lessons ordered by sort_order then id; no preview/access policy was found; GS-03→GS-04 courseId flow is proposed, not runtime verified.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Finish GS-04 only in this session; review assets and dependencies; write the screen plan before annotation/DD; preserve original assets; produce a numbered annotation, marker map and implementation-ready DD; update the GS-04 row and progress in `dd_screens/PLAN.md` and this worklog.
- Inventory baseline: GS-04 is the course curriculum tab at proposed `/courses/:courseId?tab=curriculum`, AC-05, API #09; related screens GS-03 and ST-10. It expects public lessons by `sort_order`, a separate empty state, reuse of #08 from cache before #09, and no Guest opening of private lessons. Exact field rules, item interactions, cache semantics, and access boundaries are verified below against `list_screen.md`, AC-05, #09 current source/tests, and current assets.
- Preserve separate labels for `DD READY`, `IMPLEMENTATION BLOCKED`, and `RUNTIME VERIFIED`; do not infer lesson preview or access behavior.

## CURRENT_BEHAVIOR

- Source/config: GS-04 original `screen.png` SHA-256 `4892375ec0fe6316e126b1eefe85ce05b0852079c6d666290e43c4a6f13b85c2`, 1280×1024, entropy 0.134765, 1930 colors; visually it is nearly blank except the footer. `code.html` SHA-256 `cb500b6794bc3336167dfce639506b99f438e789d64055717cedc1849b5be22c`; static HTML contains header/nav, breadcrumb, H1, empty curriculum card/icon/copy, a back-to-detail anchor with `href="#"`, and footer. No lesson rows, route hydration, API requests or event handlers are present. Tailwind and Material Symbols are loaded via CDN.
- Study Web app source/package/router/entrypoint remains absent; `.agents/web-work/study` is `UNWIRED`. The inventory route is proposed only.
- API #09 current source: `/api/v1/courses/{course_id}/curriculum` is registered in `app/api/v1.py`, public GET with DB dependency. Validator uses shared `parse_integer`; malformed IDs map to 404 `DESIGN_RESOURCE_NOT_FOUND`. View checks course `PUBLISHED` (Q1), then lists only PUBLISHED lessons (Q2), ordered `sort_order ASC, id ASC`. Current `Lesson` returns `id`, `course_id`, `title`, nullable `content`, nullable `video_url`, `order`, `status`. Success uses `DESIGN_RESOURCE_RETRIEVED`; empty is 200 with `items=[]`, total/size/total_pages 0 and message “No published lessons.” Missing/unpublished course is 404; SQL/mapping failure is safe 500 `DESIGN_INTERNAL_ERROR` with rollback on SQLAlchemy errors.
- API #09 test source has fake-session checks for invalid IDs, missing course, Q1/Q2 DB errors, successful mapping, empty success and TestClient route composition. Read only; not run. It does not validate real DB/schema/access rules.
- Design discrepancy: API #09 DD remains `Draft — Needs Confirmation` and explicitly labels `status='PUBLISHED'` as a design-only visibility assumption. It maps both `content` and `video_url` into the public response. `list_screen.md` says private lessons must not be opened by Guest and F04 says public curriculum is not the Student permission tree; no `preview/access` field exists in API #09 model/query. Do not render/play `content` or `video_url` or create a lesson-open destination in this Guest tab.
- DDL discrepancy: `infra/postgres/study-server/DB.sql` is a legacy BIGINT `lessons` candidate with `name/content/video_url/sort_order/status` and no preview field; current query matches these names. `infra/postgres/02_study_db.sql` is a separate V1-PILOT UUID/versioned model with `title/summary/position/estimated_minutes/is_preview` and different course relations. Context says neither establishes live schema; current API does not query V1-PILOT `is_preview`.
- AC-05 describes #09 immediately after #08 then #10 before render; F02 says #09/#10 lazy by tab. GS-04 row specifically says reuse #08 from cache then GET #09; cache key/freshness/missing-cache behavior is unspecified. Preserve these expected-contract points without inventing cache policy.
- Tests/runtime: no tests or Study Web runtime requested; no test has been run and no runtime behavior is verified.

## SOURCE_TRACE

- `apps/study-client/docs/list_screen.md` GS-04/F02/F04/AC-05/G-06 → Guest curriculum proposal, route and API #09 expectation; AC-05 eager order vs F02 lazy tab and inventory cache reuse are retained as unresolved expectations.
- Original `screen.png` and `code.html` hashes were checked; HTML source contains only static header, breadcrumb, H1, empty card, `href="#"` back anchors and footer. Firefox render was created separately and visually inspected.
- API #09 trace: `app/api/v1.py` → `api_09_courses_curriculum` validator/view/query/models. Current query gates PUBLISHED course and returns PUBLISHED lessons ordered by `sort_order,id`; response contains `content`/`video_url` but no preview/access flag.
- API #09 fake-session test source was read, not run. It does not establish live schema or deployment behavior.
- API #09 Draft DD and both checked-in lesson DDL candidates were reconciled; visibility is a documented assumption and legacy vs V1-PILOT schema remains unresolved.
- `.agents/web-work/study` marks Study Web `UNWIRED`; proposed route and anchor destinations are not runtime verified.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| GS-04 screenshot/HTML | Screenshot is nearly blank; HTML shows only a static no-content state and `#` detail return links. Hashes recorded above. | DISCREPANCY | Preserve sources; render HTML separately if browser output is faithful. No lesson-list design exists in the asset. |
| API #09 public projection / lesson visibility | Current source filters PUBLISHED but returns `content` and `video_url`; API DD says PUBLISHED visibility is design-only; no preview/access field. | DISCREPANCY / BLOCKER | Do not claim the status filter proves public preview eligibility; no Guest lesson-open/media behavior. BE/Product must settle safe public projection and access policy. |
| Current API vs checked-in DDL | Legacy BIGINT DDL matches names used by query; V1-PILOT UUID/versioned DDL has different lesson/course fields and `is_preview`; live schema unverified. | DISCREPANCY | Do not map V1-PILOT preview into API #09 or claim runtime schema compatibility. |
| API #09 execution/tests | Route/module/query/model and fake-DB test source exist; no real DB verification. | SOURCE_BACKED; NOT RUNTIME VERIFIED | Document current source response; do not claim deployed API/schema. |
| Orchestration/cache | GS-04 inventory says #08 cache → #09; AC-05 describes #09 in eager sequence after #08; F02 says lazy per tab. Cache freshness/miss behavior missing. | DISCREPANCY / OPEN | Keep GS-04 route direct-entry and stale cache policy unresolved; avoid inventing retries or cache TTL. |
| Study Web route/runtime | Registered Study Web subcontext is `UNWIRED`. | UNWIRED | `/courses/:courseId?tab=curriculum` remains proposed absent current router. |

## CHANGES

- Added `apps/study-client/docs/screen_stitch/02_guest_discovery/GS-04_de-cuong-khoa-hoc/GS-04_PLAN.md` before rendering/annotation/DD; completed its review checklist.
- Added `GS-04.md`, `GS-04_markers.json`, `GS-04_markers_overlay.svg`, `screen_rendered.png`, and `screen_annotated.png`; preserved original `screen.png` and `code.html`.
- Updated `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`: GS-04 blockers/status, progress to 11/83 complete sets, and next screen GS-05.
- CONTEXT_UPDATES: none. No `.agents` context page or registry changed in this screen session.
- Assumptions: none. Unresolved cache/access/schema/orchestration topics are recorded as blockers.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Docs preflight | Selector `READY`; three selected worklogs read individually; shortage none. | VERIFIED |
| GS-04 source/API/artifact audit | Python static audit passed: 10 markers, 10 element rows, 7 relative links resolved; source hashes and 1280×1024 / 1440×1200 / 3040×2400 dimensions match; SVG has 10 circles/leaders/labels and embeds the exact render; marker bounds/gutters pass; inventory 83 IDs/83 folders; complete sets 11/83; tracker says next GS-05. Annotated preview was visually inspected. | VERIFIED |
| `git diff --check` | Passed after DD, plan, tracker and worklog updates. | VERIFIED |
| Tests/runtime | Not run unless requested. | NOT_RUN |

## HANDOFF

- Remaining blockers: Loaded lesson-list and preview/access design; safe public API projection; approval of PUBLISHED visibility policy; current DDL/live schema reconciliation; #08 cache miss/freshness and AC-05/F02 orchestration; Study Web route/client wiring.
- Next owner/action: GS-04 documentation/artifact set is complete with `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED`. Continue at GS-05 in a separate session.
