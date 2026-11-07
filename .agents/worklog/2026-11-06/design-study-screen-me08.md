---
task_id: "2026-11-06-design-study-screen-me08"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: ["test"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ME-08 consumes a selected Content from ME-06/#49, mutates via #52/#53, then reloads #49; courseId must survive navigation and deletion response omits it"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ME-08

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: READY; 193 exact-type docs worklogs available; 3 selected and read; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Expected/current must remain separate; mockup/static counts are not runtime; preserve the source; fake-session tests do not verify live schema or deployment.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Trace route → handler → query/effect → response; keep catalog/source mismatch explicit; preserve unsupported UI claims and route wiring as blockers.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: One Screen ID per session; current Study Web remains UNWIRED; a declared API or existing test source does not establish deployed/runtime behavior.
- shortage: none

## EXPECTED_BEHAVIOR

- Goal objective `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md`: this session covers ME-08 only; create its plan before marker map/annotation/DD; trace source; update global tracker/worklog; distinguish DD, implementation and runtime status.
- Inventory `apps/study-client/docs/list_screen.md` ME-08/F08: proposed route `/mentor/content/:contentId/actions`; AC-22; APIs #52/#53/#49; review warnings, confirm publish/unpublish or delete, refresh #49; linked ME-06; states `confirm/processing/success/blocked`.
- AC-22 precondition is Mentor permission to manage the course; flow reads #49, branches to PATCH publish, DELETE, then reloads the content tree.
- `createDD-markdown` is registered for Web/API DD and explicitly excludes `web-ui-only-dd`; no canonical UI-only DD skill applies.

## CURRENT_BEHAVIOR

- Before authoring, the ME-08 folder contained only `screen.png` and `code.html`. Source PNG is 1600×1530 with SHA-256 `71b2db17d21899584fa4e70da2ee4955e83d7e701cda21a00d6117dc7e89dc78`; HTML SHA-256 `18e7ee943af98918cd70eb141289015b2fc550088a4c726d57cef8d39ebb6a8b`.
- Screenshot/HTML show a static action page with no selected target (placeholder), sample `DRAFT` label/low-impact rating, unsupported student-impact/audit/environment claims, disabled Publish/Delete buttons, and a return-to-ME-06 link. HTML has 15 anchors (all `href="#"`), two disabled buttons, no inputs, no form, and no API/event binding. It imports remote fonts/Tailwind. No unpublish control is visible.
- Study Web remains `UNWIRED`; editable app source/router/package manifest are absent. This page has no verified client runtime.
- API #49 current source returns an active flat `Content[]` for a course after MENTOR auth/direct-owner check; it excludes `deleted_at IS NOT NULL`, includes statuses and `course_id`, and has no single-Content detail route.
- API #52 current local route requires strict body `{published: boolean}` although catalog/AC declare path only. Source locks Content/Course, requires direct owner, allows `APPROVED → PUBLISHED` or `PUBLISHED → APPROVED`, treats a repeated target as a no-op, updates only status, commits, and returns Content with HTTP 200 `DESIGN_RESOURCE_UPDATED`. Body/transition/readiness rules are DERIVED and the API DD remains Draft.
- API #53 is bodyless DELETE; source locks Content/Course and requires direct owner, blocks PUBLISHED, blocks an active direct child, sets `deleted_at=CURRENT_TIMESTAMP`, commits, returns `{id,status:"deleted",deleted_at}` with HTTP 200 `DESIGN_RESOURCE_DELETED`; active/missing/deleted ID returns 404. Child/PUBLISHED guards and status eligibility are DERIVED; the response omits `course_id`.
- Focused #52/#53 test source and `.agents/server-study/tests.md` were inspected; tests were not run. Test doubles do not prove live schema/deployment. Checked-in migration 006 defines `contents.deleted_at` and parent relation; migration 007 defines `content_versions`; no live DB probe occurred.

## SOURCE_TRACE

- Expected: ME-06 selects a Content → ME-08 review → #52 publish/unpublish or #53 delete → refresh/reload #49 → return to ME-06.
- Current #49: route in `apps/study-server/app/api/v1.py` → `get_course_contents` → shared MENTOR Bearer guard → parse `course_id` → read course and compare `courses.mentor_id` → list active `contents` ordered parent/order/id → map/validate flat tree → 200 Content[]; 401/403/404/500 safe envelopes.
- Current #52: route → `publish_content` → shared MENTOR guard → signed-int64 Content path parse → `LOCK_MENTOR_CONTENT` (Content + Course `FOR UPDATE`) → direct-owner check → request target/current-state check → conditional status-only UPDATE for the two local transitions, or same-target no-op → validate Content projection → commit → 200 `DESIGN_RESOURCE_UPDATED`; malformed body 422; invalid/missing/deleted ID 404; owner mismatch 403; DB/mapping/commit 500; unsupported state 422.
- Current #53: route → `delete_content` → shared MENTOR guard → signed-int64 path parse → lock active Content + Course → direct-owner check → PUBLISHED guard → query active direct Content children → soft-delete with `CURRENT_TIMESTAMP` → validate DeleteResult → commit → 200 `DESIGN_RESOURCE_DELETED`; child/PUBLISHED guards 422, invalid/missing/already deleted ID 404, owner mismatch 403, DB/mapping/commit 500.
- Expected navigation requires #49 reload after either mutation. #52 response includes `course_id`; #53 `DeleteResult` does not, while the proposed ME-08 route carries only `contentId`. The course ID therefore needs to be preserved from ME-06/navigation context; that transport is not specified or wired.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| #52 request/transition | Catalog/AC path-only vs current strict `{published:boolean}` and APPROVED↔PUBLISHED fallback | DISCREPANCY; DERIVED | Publish direction and body require owner approval; DRAFT/PENDING_REVIEW cannot publish through current source. |
| #53 eligibility/dependencies | Current code blocks PUBLISHED and active direct children only; accepts other non-PUBLISHED statuses | DERIVED / OPEN | Does not prove protection for student progress, assessments, assets, audit or review queues shown/claimed in mockup. |
| Target hydration | Inventory route has only contentId; #49 is course collection and requires courseId | OPEN | Need selected Content + course context from ME-06; no detail endpoint or client navigation state is wired. |
| Delete refresh | #53 DeleteResult lacks course_id; #49 refresh requires course_id | OPEN | Preserve the course ID before mutation or the required post-delete refresh cannot be addressed. |
| Mockup claims | Certificate recalculation, attendance/submission retention, latest audit record, production/region/Safe Mode are static and absent from #49/#52/#53 | NOT_FOUND / DISCREPANCY | Must not present as verified server effects/status. |
| Unpublish affordance | Inventory includes publish/unpublish; screenshot only shows disabled publish button and delete button | DISCREPANCY | State-specific action design and confirmation behavior remain incomplete. |
| Study Web/runtime/live DB | No editable client route; local DDL/migrations only | UNWIRED / NOT_VERIFIED | No client, deployment or live schema claim. |

## CHANGES

- Files created/updated for ME-08:
  - `apps/study-client/docs/screen_stitch/04_mentor/ME-08_xuat-ban-xoa-noi-dung/ME-08_PLAN.md`
  - `apps/study-client/docs/screen_stitch/04_mentor/ME-08_xuat-ban-xoa-noi-dung/ME-08.md`
  - `apps/study-client/docs/screen_stitch/04_mentor/ME-08_xuat-ban-xoa-noi-dung/ME-08_markers.json`
  - `apps/study-client/docs/screen_stitch/04_mentor/ME-08_xuat-ban-xoa-noi-dung/ME-08_markers_overlay.svg`
  - `apps/study-client/docs/screen_stitch/04_mentor/ME-08_xuat-ban-xoa-noi-dung/screen_annotated.png`
  - `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` (ME-08 row and artifact-presence checkpoint)
  - `.agents/worklog/2026-11-06/design-study-screen-me08.md`
- Source `screen.png` and `code.html` are unchanged. No server code, API contract, database schema, or context page changed. No other Screen ID artifact was edited.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Mandatory docs preflight | `node scripts/select-worklogs.mjs --type docs --limit 3`; READY with 193 exact-type worklogs; three selected paths individually read; no shortage. | VERIFIED |
| Asset/source/API review | Screen inventory/F08, AC-22, API catalog, #49/#52/#53 route/module/query/view/model/validation, API DD/open questions, focused test source, checked-in migrations and Study Web context read. Tests not executed. | VERIFIED (source review only) |
| Static artifact audit | 83 source screen folders; 42/83 have the four core files, 41 incomplete. Count includes ST-25 file presence observed in checkout; ST-25 content was not audited or changed in this ME-08 session. ME-08 has 46 sequential unique in-bounds markers; min center separation 35 source px; JSON↔SVG IDs/coordinates and DD element mapping are 1:1; 8 sequential events; relative Markdown paths and line anchors resolve. | VERIFIED |
| Annotated image | Rendered from 1600×1530 source at 2× to 3200×3060; visually inspected. Moved marker 17 above the target icon after initial visual review showed it close to the adjacent label; final image leaves text/buttons unobscured. | VERIFIED |
| Original asset hashes | `screen.png` = `71b2db17d21899584fa4e70da2ee4955e83d7e701cda21a00d6117dc7e89dc78`; `code.html` = `18e7ee943af98918cd70eb141289015b2fc550088a4c726d57cef8d39ebb6a8b`. | VERIFIED |
| `git diff --check` | Completed after ME-08 DD, plan, tracker and worklog updates; no whitespace errors. | VERIFIED |
| Tests / Study Web runtime / live DB | Not run or probed. Fake-session focused tests were read only; no deployed API/schema claim. | NOT_RUN / NOT_VERIFIED |
| Context validator | No context page, contract, code or registry changed. | NOT_REQUIRED |

## HANDOFF

- ME-08 documentation/artifact audit is complete; status remains `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`.
- Remaining blockers: approve #52 target body and lifecycle/readiness/publication effect; confirm #53 status/dependency/descendant/history/queue policy; define target/course context handoff from ME-06 and post-delete #49 refresh; remove or source student-impact/audit/environment claims; reconcile direct-owner with AC-22 course-management permission; wire Study Web and verify deployed APIs/live schema.
- Next Mentor Screen ID: ME-09, in a separate session. ST-25 has core files present but was not reviewed in this session; it remains a separate audit task.
