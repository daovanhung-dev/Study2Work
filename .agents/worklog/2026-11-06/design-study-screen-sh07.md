---
task_id: "2026-11-06-design-study-screen-sh07"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["SH-07 operation status consumes API #18 for ST-07, ME-15, AD-21, and AD-25; operation ID/lifecycle/owner and producer mapping require source trace"]
status: "VERIFIED"
---

# Worklog: Rà soát Detailed Design màn hình Study SH-07

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; selected 3 of 159 exact-type docs worklogs; all selected logs read.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-sh01.md`
    - carry_forward: Preserve source assets; use stable ordered marker IDs; distinguish design artifacts/API source/runtime; do not infer a missing destination or content source.
  - path: `.agents/worklog/2026-11-06/design-study-screen-sh02.md`
    - carry_forward: Study Web source/router is absent; API contracts and source can disagree; UI-only DD has no canonical skill; record unresolved session/route behavior as blockers.
  - path: `.agents/worklog/2026-11-06/design-study-screen-sh03.md`
    - carry_forward: Trace source caller-to-callee, DB side effects and response; checked-in tests/DDL do not prove runtime/live schema; preserve expected/current separation.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete SH-07 only in this session; review/update its plan before DD or annotation edits; preserve source `screen.png`/`code.html`; check or create an ordered marker map and annotated image; trace event/API #18 and cross-screen flows; update global tracker and worklog.
- Canonical expected behavior: `apps/study-client/docs/list_screen.md` SH-07 says to use only a backend-issued operation ID, read API #18, and stop on a terminal status; links ST-07, ME-15, AD-21 and AD-25. AC-12/25/36/38 use UUID and owner-only language, while the API #18 catalog row uses `int64` and its tracking summary allows owner/Admin. API #18 DD is Draft/Needs Confirmation; Q-18-01..05 remain open. `.agents/web-study/design.md` is intended UI guidance, not runtime evidence.

## CURRENT_BEHAVIOR

- Source/config: SH-07 is a static gated prototype; it has no fetch, polling or SSE. Its script reads a route segment and inserts a UUID fallback if absent; modal and copy are inline DOM/clipboard actions, and anchors use `#`. Study Web `src/`, package manifest and study subcontext are absent. Study Server has no #17/#18/#103 route/module/test in the inspected tree. Migration 009 adds `notifications.operation_id UUID` and notification delivery outbox storage, not a generic operations table. `contracts/openapi/study/README.md` is a placeholder.
- Runnable tests: Test files exist for #63/#64/#93/#96 and were inspected as source; tests were not run. #17/#18/#103 tests were not found in the scoped tree search.
- Runtime wiring: Study Web route and generic API #18 remain `UNWIRED`; no live deployment or database verification was performed.

## SOURCE_TRACE

Current trace (2026-11-06):

- `apps/study-server/app/api/v1.py` registers Mentor #63 POST (202), Mentor #64 GET (200), Admin #93 POST (202), and Admin #96 GET (200). Scoped route/module searches found no #17/#18/#103 or generic `/operations` route.
- #63 `OperationResponse.id` is UUID; source creates an operation UUID, writes notification/outbox rows, builds `data:OperationResponse` with `NOTIFICATION_DISPATCH`/`QUEUED` and `meta.notification_ids`, commits, then returns 202. #64 takes numeric `notification_id`, checks Mentor sender ownership, aggregates delivery rows and returns UUID Operation-like data with notification-specific `QUEUED`/`FAILED`/`SENT` statuses.
- #93 creates an operation UUID but returns the first `Notification` in `data`, plus `operation_id` and `notification_ids` in `meta`, after committing before 202. #96 takes numeric `notification_id` and returns `Notification`, not generic Operation.
- `docs/lists/list_api.md` API #18 row uses `path operation_id:int64` while reusable Operation schema and AC diagrams use UUID. Authorization differs between owner-only and owner/Admin. `apps/study-server/docs/dd/18_operations/OPEN_QUESTIONS.md` preserves these plus lifecycle/storage, result-by-kind and 403/404 questions. No canonical enum/terminal-state, result mapping, polling/SSE, retention or safe-return decision was found.
- `infra/postgres/study-server/DB.sql` and migration 009 show a UUID on notification rows only. No generic Study operation table was found; Work Server storage is not evidence for Study.
- SH-07 `code.html` and screenshot are mock design artifacts. The current visual contains 35 visible components; the hidden Contract Spec modal has four unnumbered modal-only elements in the DD. The DD already records 10 events and the unresolved contracts without promoting mock values to runtime behavior.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| SH-07 plan/assets/DD | Plan updated after source trace; source image/HTML hashes unchanged; 35-marker map matches 35 visible DD elements; 10 events and local references checked. Marker #23 was moved into the left gutter to avoid covering code. | VERIFIED | DD remains blocked; marker set is readable and traceable. |
| Study Web route/runtime | `src/`, package manifest and study subcontext are absent in checkout; no runtime confirmation. | UNWIRED / NOT VERIFIED | Do not infer runtime from prototype files. |
| API #18 operation contract | Catalog int64 vs UUID schema/AC; owner vs owner/Admin; no route/module/query/test/storage; API #18 DD Draft with open questions. | DISCREPANCY / UNWIRED | ID, auth, lifecycle, result and caller integration cannot be implemented safely. |
| Producer/status shapes | #63 Operation/UUID; #64 notification-ID path and notification-specific Operation-like states; #93 Notification data plus UUID metadata; #96 Notification. #93 catalog row and tracking summary differ. | DISCREPANCY | Do not treat producer IDs or endpoint responses as one generic contract. |

## CHANGES

- Files changed: `.agents/worklog/2026-11-06/design-study-screen-sh07.md`; SH-07 plan, marker JSON/SVG and `screen_annotated.png`; `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`. DD text and source `screen.png`/`code.html` were left unchanged after source review found no misstatement requiring a content correction.
- CONTEXT_UPDATES: None; no shared canonical context page changed.
- Context pages changed: None.
- Skill routing: UI-only DD has no applicable canonical skill; `createDD-markdown` excludes it. Registry was reviewed; no skill invoked.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` + selected-file review | Selected and read 3 exact-type docs worklogs of 159; no shortage. | VERIFIED |
| Source/contract review | Re-read inventory, API #18 DD/open questions, API #63/#64/#93/#96 source/models/routes/queries, Study DDL/migration, OpenAPI placeholder and relevant test source; no tests run. | VERIFIED |
| Marker/DD static audit | JSON parses; 35 ordered unique markers match 35 visible Element IDs; SVG labels #1–#35; 10 unique events; local DD links resolve; marker #23 no longer covers the code block. | VERIFIED |
| Asset/tracker checks | Original PNG/HTML SHA-256 unchanged; source and annotated images are 1503×1600; 83 inventory IDs equal 83 tracker rows; SH-07 remains blocked and handoff is GS-01; `git diff --check` clean. | VERIFIED |
| Tests/runtime | Not run. | NOT_RUN |

## HANDOFF

- Remaining blockers: API #18 is unwired; ID type, role/owner semantics, lifecycle/status, result-by-kind, producer response alignment, polling/retention and safe-return navigation remain unresolved. Study Web and live runtime/schema are not verified.
- Next owner/action: Next session may start GS-01, the first unstarted W0 screen. This session handled SH-07 only.
