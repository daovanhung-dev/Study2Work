---
task_id: "2026-11-17-implement-study-screens-apis-T015"
date: "2026-11-17"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["web-work (Study Web)", "server-study"]
cross_scope_dependencies: ["GS-03/GS-04 Study Web query-tab -> Study Server API #09 current route, validator, view and fake-session tests"]
status: "VERIFIED"
---

# Worklog: Continue coding Study Web screens — T015

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `READY`; 125 available; T011, T012 and T013 selected and read in full; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T011.md`
    - carry_forward: AD-22/#97 is a bounded read-only slice; API DD/report projection/fine permission/live schema remain unresolved; avoid using #98 as an AD-22 caller.
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T012.md`
    - carry_forward: broad goal remains all 83 screens plus role-aligned APIs at 20%; GS01–03 are source-wired, but some loaded states are derived and fake-DB/browser gaps remain.
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T013.md`
    - carry_forward: GS04 service #09 exists; API DD, visibility, loaded visual, cache, eager/lazy and query-tab composition remain gates; T014 added a standalone page but no route host.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Latest user requirement: continue coding Study Web screens within the active all-83-screen/API objective.
- Overall objective remains 20% ACTIVE; T015 is a bounded continuation and must not redefine the broad objective.
- Latest user requirement: continue coding screens within the active all-83-screen/API objective.
- T015 candidate selected: GS-04 curriculum tab embedded on GS-03 `/courses/:courseId`, API #09. The GS04 standalone page from T014 is not mounted; `list_screen.md` allows Tab screens to be components/modals/sub-routes, while frontend rules prohibit direct screen-to-screen imports.
- Expected behavior: select the curriculum tab with `?tab=curriculum`, wait for GS-03 #08 to confirm a PUBLISHED course, then lazy-load #09; distinguish empty from not-found/service error; show only lesson title/order and no Guest lesson/media action. F02 and the inventory row support lazy tab loading, but AC-05 says eager and remains a `DISCREPANCY`.
- Overall objective remains 20% ACTIVE; this is an integration continuation for GS-04, not completion of the 83-screen objective.

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 15% | 15% | Complete exact-type worklog/context preflight; reject blocked SH-05 after DD/source audit; select the source-supported GS-04 query-tab integration; record current/expected evidence and plan before code. | `DONE` |
| 65% | 80% | Implement the GS-04 curriculum panel as a GS03-owned query tab, gated by successful #08 and using #09 without exposing lesson content/media/actions. | `DONE` |
| 20% | 100% | Run focused UI/API verification and build, update current-source context and `docs/tasks/process.md`, and record remaining blockers. | `DONE` |

**Current T015 progress: 100%. Overall objective: 20% ACTIVE.**

## CURRENT_BEHAVIOR

- Current client after T015 implementation: GS03Page owns `/courses/:courseId`, reads `tab=curriculum`, gates #09 until #08 confirms a published course, preserves course IDs as strings, and renders a GS03-local panel with loading/empty/ready/404/error states. Only lesson title/order are projected; there is no lesson/media action or client cache. The duplicate unmounted GS04 page implementation was removed.
- Current API #09: existing public GET source validates signed-int64 while client must preserve ID text, checks PUBLISHED course/lessons, returns `LessonPage` with title/order/content/video, and has 11 fake-session tests; live schema/runtime are not verified.
- Rejected alternative: SH-05 remains blocked by B01–B07 (no error-context/auth manager, unresolved 401 recovery/copy/safe fallback and prototype UI approval); no code is changed there.

## CHANGES

- Added GS03-local #09 model/service and `GS03CurriculumPanel`; removed the duplicate unmounted GS04 page/caller.
- GS03 tabs now synchronize through query params with accessible tab semantics and keyboard navigation. #09 is lazy and cancelled when leaving the tab or changing course.
- Updated GS03/GS04 inventories, current-source DD notes, context pages and manifest. DD/access blockers remain explicitly open.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | `READY`; T011, T012 and T013 selected and read in full. | `VERIFIED_PREFLIGHT` |
| Candidate and composition audit | SH-05 rejected: its DD explicitly blocks frontend implementation pending auth/error-context and UX decisions. GS-04 selected: inventory says it is a tab under GS-03; current route is already `:courseId`; #09 source and tests exist; moving the #09 data-access/model into GS03 avoids importing another screen. | `VERIFIED_CANDIDATE` |
| `npm test -- --include=src/app/features/guest/GS03/pages/gs03-page.spec.ts` | GS03 focused spec: 6/6 passed after adding an assertion that #09 is not requested before #08 succeeds. | `PASS` |
| `npm run build` | Production build passed after removing duplicate GS04 source. GS03 is within CSS budget; three Student CSS budget warnings remain. | `PASS` |
| Study Server API #09 tests | T014 verification: 11 fake-session tests passed; no server code changed in T015. | `PASS_PRIOR_SLICE` |
| Headless browser direct-entry | Angular route returned HTTP 200. Firefox screenshot showed the loading state; Chrome after 5s showed the safe #08 service error. `127.0.0.1:3003` refused connections, so curriculum API/data state was not browser-verified. Shared Chrome and in-app browser were unavailable. | `ROUTE_VERIFIED_API_BLOCKED` |

## HANDOFF

- Remaining blockers: API #09 `PUBLISHED` visibility remains an unapproved assumption; raw content/video fields have no preview/access projection; no #08 cache exists; AC-05 eager and F02 lazy differ; loaded-state design, live DB schema and browser/API deployment remain unverified. GS-05/#10 remains blocked by contract gaps.
- T015 is complete at 100% for this bounded GS04 integration slice. The broader 83-screen/API objective remains 20% ACTIVE; select the next source-supported screen slice when continuing.
