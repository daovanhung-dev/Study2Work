---
task_id: "2026-11-06-design-study-screen-me06"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: ["test"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ME-06 reads API #49 Content[] and hands off to ME-07/#50/#51 and ME-08/#52/#53; Content.id/version, tree relationships and direct-owner policy cross the UI/server boundary"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ME-06

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: READY; 189 docs worklogs available; 3 selected by exact task type; shortage none.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Tách expected/current; Study Web source/runtime vắng; giữ sample claims khỏi data contract.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Preserve source hashes; route/API declaration không chứng minh deployment; giữ field/pagination discrepancies rõ.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: Respect UNWIRED; verify exact API source independently; do not infer routes, content, or cross-role access.
- shortage: none

## EXPECTED_BEHAVIOR

- Goal objective `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md` was read. This session covers ME-06 only; write its plan before markers/annotation/DD, keep original assets, trace current source, update global tracker and worklog, and report `DD READY`, `IMPLEMENTATION BLOCKED`, and `RUNTIME VERIFIED` independently.
- Inventory `apps/study-client/docs/list_screen.md` row ME-06: route `/mentor/courses/:courseId/content`, AC-22, API #49, links ME-07/ME-08; GET the content tree; preserve IDs/version; do not render draft as published; states `loading/empty/ready/error`.
- F08 links ME-06 with ME-04, ME-05, ME-07 and ME-08; each related Screen ID remains out of scope for this session.
- No canonical skill is registered for web UI-only DD; `createDD-markdown` is routed to Web/API DD, not this UI DD.

## CURRENT_BEHAVIOR

- At start ME-06 folder had only `screen.png` and `code.html`. Rechecked SHA-256: PNG `3efb10d47fb04b743f64c224d6feb1f8faa3b284b2dbfc9676b73cdb0682e0b8`; HTML `83a77f82e4e8a89122be88e6f78d2538329d6e0800bd4c789a1aadd207d60543`. PNG dimensions 1367×1600; both sources remain unchanged.
- Screenshot is a populated desktop mockup with summary/KPI, filters, tree rows, distribution, LMS rules, audit log and footer. Static HTML has local accordion/filter/search/toast logic only; no API, route or persistence. The reorder toast names a nonexistent `PUT #52 reorder`; current #52 is PATCH publish. The draft publish handler only alters DOM text/data.
- Study Web context is `UNWIRED`; no editable app source/router/package manifest is available for runtime verification.
- API #49 route/module/query/model/test source exists locally. It checks MENTOR role and direct course owner; queries active `contents`; returns a flat Content[] ordered by parent/order/id with raw status and no version. Empty is 200 `data:[]`; invalid path/missing course 404; owner mismatch 403; SQL/mapping/tree errors safe 500.
- Current checked-in `DB.sql` includes `contents`/`content_versions`; migrations 006/007 exist. Their live application is unknown. API DD #49 remains Draft — Needs Confirmation.
- #50 creates only root Content with PENDING_REVIEW; #51 archives the current version and updates title/type/payload, setting PENDING_REVIEW while keeping parent/order; #52 is publish/unpublish (`APPROVED↔PUBLISHED` only; other source status → 422); #53 soft-deletes and rejects PUBLISHED or parents with active children. Local source/test files exist; tests were read/inspected, not run.

## SOURCE_TRACE

- Read root `AGENTS.md`, `.agents/AGENTS.md`, `.agents/context-map.md`, web-work and Study Web scope context, server-study scope/index, worklog README/template, context manifest/registry, the goal objective and all three selector-selected docs worklogs.
- Screen sources: `apps/study-client/docs/list_screen.md` ME-06/F08; `.../ME-06_cay-noi-dung-khoa-hoc/{screen.png,code.html}`; existing sibling ME-05 DD/plan/marker conventions; renderer `apps/study-client/docs/screen_stitch/dd_screens/tools/render_annotation.py`.
- Server route: `apps/study-server/app/api/v1.py` #49 at route section around line 862 and #50–#53 around lines 898–1028.
- Read #49 models/query/view/validate; #50 models/query/view; #51 models/query/view; #52 models/query/view; #53 models/query/view. Read API #49 Overview and Open Questions; read `infra/postgres/study-server/DB.sql`, migrations `006_contents.sql`/`007_content_versions.sql`; inspected corresponding focused test source/signatures. No database calls or test execution.
- Trace: UI route proposed → #49 route → `get_course_contents` → MENTOR guard/path parse → course/direct owner query → active Content query → projection/tree validation → success/error envelope. Read-only. Related mutations and their DB effects are summarized in `ME-06.md`.

## DISCREPANCIES_AND_STATUSES

| Finding | Status | Evidence/impact |
|---|---|---|
| Old inventory blocker says Content absent from 18-table DDL | DISCREPANCY | Current checked-in legacy DB.sql and migrations 006/007 contain `contents`/`content_versions`; live DB still unknown. |
| API #49 response says `Content[]`; API DD is Draft | SOURCE_BACKED; DISCREPANCY | Local route/model/query/view/test source exists; owner approval and live deployment not established. |
| Expected tree/version vs flat response/no version | DISCREPANCY | `parent_id` supports client tree; #49 has no version field/selector. |
| Mockup CRUD/order/status vs current APIs | DISCREPANCY | #50 root-only, #51 no move/reorder, #52 publish PATCH not reorder, #53 guarded soft-delete; draft CTA conflicts with allowed publish source state. |
| Direct-owner source vs assigned-course wording | DISCREPANCY | #49–#53 check `courses.mentor_id == principal`; assignment not supported in these handlers. |
| KPI/quality/audit panels | NOT_FOUND in ME-06/#49 response | No source mapping in the screen’s referenced contract; screenshot values are fixture data. |
| Study Web route/runtime | UNWIRED | Context and checkout do not provide an editable client/router; no runtime claim. |
| Live DB/deployment | NOT_VERIFIED | DDL/migrations/test source are local artifacts only. |

## CHANGES

- Files changed: `apps/study-client/docs/screen_stitch/04_mentor/ME-06_cay-noi-dung-khoa-hoc/ME-06_PLAN.md`, `ME-06_markers.json`, `ME-06_markers_overlay.svg`, `screen_annotated.png`, `ME-06.md`; `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; this worklog.
- Original `screen.png`/`code.html` and other Screen IDs were not modified.
- Context pages changed: none; no server/web/API/database contract was edited.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Mandatory preflight selector and three selected logs | Selector READY (189 available); three exact-type docs logs read; no shortage. | VERIFIED |
| API/schema and UI source trace | Route, validators, query/view/model, focused test source, DDL/migrations and static HTML handlers read; no test executed. | VERIFIED (static source review) |
| `render_annotation.py` | Produced annotated PNG 2734×3200 with 44 markers after adapting canonical object JSON into a temporary renderer list; final image viewed visually. | VERIFIED (artifact render) |
| Marker/JSON/SVG/DD/link/hash/tracker audit | Python static audit passed: source hashes unchanged; 44 markers sequential, unique, in-bounds and >21 px apart; JSON/SVG/DD match; 17 event IDs sequential; local Markdown links resolve; annotated PNG is 2734×3200; 83 source folders and 38 complete core artifact sets; no trailing whitespace. | VERIFIED |
| `git diff --check` | Exit code 0; no whitespace errors. | VERIFIED |
| Tests/browser/runtime/live DB | Not run or verified by user request/scope. | NOT_RUN / NOT_VERIFIED |
| Context validator | No context pages/manifest changed. | NOT_REQUIRED |

## HANDOFF

- Remaining blockers: Study Web remains UNWIRED; #49 response/tree approval and live migrations; content type/status/payload/version; direct-owner vs assigned course; child creation/reorder; publish readiness; metrics/quality/audit read models. Screen status: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Overall inventory: 38/83 core artifact sets complete, 45 incomplete.
- Next screen in Mentor sequence: ME-07 in a separate session.
