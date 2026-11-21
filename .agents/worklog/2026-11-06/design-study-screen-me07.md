---
task_id: "2026-11-06-design-study-screen-me07"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: ["test"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ME-07 loads Content from API #49 and creates/updates through #50/#51; course/content IDs, request body, order, payload, version history and direct-owner policy cross the Study Web/Study Server boundary"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ME-07

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: READY; 192 exact-type docs worklogs available; 3 selected; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Keep expected/current separate; source assets and mock behaviors are not API evidence; no Study Web route/runtime exists.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Preserve source hashes; no Study Web router; reject unsupported API/UI fields; fake DB tests do not prove live schema.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: Verify every cross-screen/API handoff from source; preserve catalog/AC/source disagreements; one Screen ID per session.
- shortage: none

## EXPECTED_BEHAVIOR

- Goal objective `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md` read this session. This session covers ME-07 only; write its plan before marker map/annotation/DD; preserve original assets; trace source; update tracker and worklog; distinguish `DD READY`, `IMPLEMENTATION BLOCKED`, and `RUNTIME VERIFIED`.
- Inventory `apps/study-client/docs/list_screen.md` ME-07 row: proposed route `/mentor/courses/:courseId/content/:contentId?`, AC-22, APIs #49/#50/#51; editor by `content_type/payload`; dirty-state validation; read #49, then POST #50 or PUT #51, then refresh #49; linked ME-06/ME-08; expected `draft/dirty/validating/saving/conflict`.
- AC-22 diagram says Mentor has permission to manage the course, reads the content tree and chooses create/update/publish/delete; #51 input is only path-level in the diagram/catalog, but the diagram says “UPDATE Content + version”.
- `createDD-markdown` is registered for Web/API DD and excludes `web-ui-only-dd`; this UI-only DD has no canonical skill.

## CURRENT_BEHAVIOR

- Before this session ME-07 folder contained only `screen.png` and `code.html`. Initial hashes: PNG `e952ed4554505d34c087a4f0812cb06f71839ea193ddb3c84f998118e4349af3` (1600×1400), HTML `98c9eba51f9b827452d5f46f5e440945decc85c3a0b6d80017c34eccbbbe7ead`.
- Screenshot is a create/edit content mockup: title field, type selector (`theory/reading/practice`), order input (`min=1`), disconnected editor placeholder, locked media note, cancel and disabled save-draft button, standards/security text, session/reconciliation status/progress, promotional image and footer links.
- HTML has 14 anchors (all `href="#"`), 2 inputs, 1 select, 1 disabled button, 1 image and no form. It has no custom event logic, fetch/XHR or API binding. Title/type/order fields have no complete validation wiring; “Lưu bản nháp” is disabled in markup.
- Study Web remains `UNWIRED`; current checkout has no editable app source/router/package manifest. No client runtime state can be verified.
- API #49 is a local source-backed read of all active Content rows, returning flat `Content[]` with `id/course_id/content_type/title/payload/status/parent_id/order`; it has no version field. #50 is strict create `{course_id, content_type, title, payload}`; it inserts a root (`parent_id=NULL`) with server-generated root order and `PENDING_REVIEW`. #51 current local body is `{content_type,title,payload}` (DERIVED; absent from catalog request); it archives current data to `content_versions`, updates those fields, sets current status `PENDING_REVIEW`, and preserves `parent_id/order`. Both mutations use direct `courses.mentor_id` ownership; #51 includes a transaction/commit. API DD #50/#51 remain Draft — Needs Confirmation; live DB/deployment unknown.

## SOURCE_TRACE

- Mandatory reads: root/scope instructions, context map, project boundary index, Study Web and Study Server context pages, skill registry, worklog README/template, goal objective and all three selector-selected logs.
- Screen and expected source: `apps/study-client/docs/list_screen.md` ME-07/F08; ME-07 `screen.png`/`code.html`; AC-22 section in `apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio`; API catalog #49–#51; API DD #50/#51 Overview and Open Questions; Study Web design guide.
- Current source: route declarations #50/#51 in `apps/study-server/app/api/v1.py`; #50 models/query/view; #51 models/query/view/validate; #49 models/query/view; focused #50/#51 test source; checked-in `infra/postgres/study-server/DB.sql` and migrations 006/007.
- Intended flow: create route → POST #50 → root Content/PENDING_REVIEW/201; edit route → GET #49 collection to find Content ID → PUT #51 full replacement body (current source) → archive snapshot + update/PENDING_REVIEW/200 → expected GET #49 refresh. Client workflow/runtime is not wired. Fake-session tests were inspected, not run.

## DISCREPANCIES_AND_STATUSES

| Finding | Status | Evidence/impact |
|---|---|---|
| API #51 catalog body is path-only while current code has body | DISCREPANCY; DERIVED | Current strict body is `{content_type,title,payload}`; API DD #51 says it is derived and unapproved. |
| Mockup offers `theory/reading/practice` and positive `sort_order` | DISCREPANCY | Server has open content type; #50 does not accept order/parent; #51 preserves order/parent. |
| Rich editor/payload submission | NOT_FOUND / BLOCKED | UI shows placeholder only; `payload` object subtype/schema is unapproved; no form or submit handler. |
| Version requirement | DISCREPANCY | #51 snapshots previous state in `content_versions`, but #49/#50/#51 response has no version token/selector. |
| Mentor ownership | DISCREPANCY | AC-22 says management permission; #49–#51 use direct course owner, not assignment. |
| Web integration | UNWIRED | No editable Study Web app/router/runtime in current checkout. |
| Local DB artifacts vs live | NOT_VERIFIED | DDL/migrations present; no live schema/deployment probe. |

## CHANGES

- Files created/updated for this Screen ID:
  - `apps/study-client/docs/screen_stitch/04_mentor/ME-07_tao-chinh-sua-noi-dung/ME-07_PLAN.md`
  - `apps/study-client/docs/screen_stitch/04_mentor/ME-07_tao-chinh-sua-noi-dung/ME-07.md`
  - `apps/study-client/docs/screen_stitch/04_mentor/ME-07_tao-chinh-sua-noi-dung/ME-07_markers.json`
  - `apps/study-client/docs/screen_stitch/04_mentor/ME-07_tao-chinh-sua-noi-dung/ME-07_markers_overlay.svg`
  - `apps/study-client/docs/screen_stitch/04_mentor/ME-07_tao-chinh-sua-noi-dung/screen_annotated.png`
  - `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` (ME-07 row and 40/83 checkpoint)
  - `.agents/worklog/2026-11-06/design-study-screen-me07.md`
- Original `screen.png` and `code.html` unchanged; no implementation, API contract, database or context page changed.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Mandatory docs preflight | `node scripts/select-worklogs.mjs --type docs --limit 3`; selector READY, 192 exact-type docs worklogs available, three selected/read, no shortage. | VERIFIED |
| Source/API/DD/AC/asset review | Inspected screen inventory, AC-22, API catalog/DD, route/model/query/view/validation and focused test source for #49–#51, local DDL/migrations and web-study design context; tests not executed. | VERIFIED (source review only) |
| Static artifact audit | 83 source folders; 40/83 have all four core artifacts, 43 incomplete. ME-07: 31 sequential unique in-bounds markers; minimum center separation 31 source px; JSON↔SVG IDs/coordinates and DD 1:1 mapping; 11 sequential events; relative Markdown links resolve. | VERIFIED |
| Annotated image | Rendered from unchanged 1600×1400 source at 2× to 3200×2800. Visually inspected; moved marker 8 above the badge after noticing its initial placement touched text; final image has no marker covering its labels or controls. | VERIFIED |
| Original asset hashes | `screen.png` = `e952ed4554505d34c087a4f0812cb06f71839ea193ddb3c84f998118e4349af3`; `code.html` = `98c9eba51f9b827452d5f46f5e440945decc85c3a0b6d80017c34eccbbbe7ead`. | VERIFIED |
| `git diff --check` | Run on ME-07 DD/plan/map/overlay, global tracker and worklog; no whitespace errors. | VERIFIED |
| Tests / client runtime / live DB | Not run or probed. Focused tests were read only; this work does not claim integration/runtime verification. | NOT_RUN / NOT_VERIFIED |
| Context validator | No `.agents/` context page, contract or registry changed. | NOT_REQUIRED |

## HANDOFF

- ME-07 documentation/artifact audit is complete; screen status remains `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`.
- Remaining blockers: approve #51 full-replacement body; define content-type enum and `payload` subtype/editor; reconcile visible sort order/parent placement with #50/#51; decide draft vs `PENDING_REVIEW`; define version/current revision and stale-write behavior; reconcile AC-22 course-management assignment with direct-owner checks; wire Study Web route/session/form/cache and verify deployed API/live schema.
- Next Screen ID in scope `04_mentor`: ME-08, in a separate session. Student pointer remains ST-25.
