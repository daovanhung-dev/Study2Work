---
task_id: "2026-11-17-implement-study-screens-apis-T020"
date: "2026-11-17"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["web-work (Study Web)", "server-study"]
cross_scope_dependencies: ["SH-07 operation tracking screen ↔ Study API #18 shared operation lookup and unresolved ID/owner/lifecycle contract"]
status: "IN_PROGRESS"
---

# Worklog: Continue Study Web screen coding — T020 (SH-07)

## PRIOR_WORKLOG_REVIEW

- `primary_task_type`: `coding`
- `selector_command`: `node scripts/select-worklogs.mjs --type coding --limit 3`
- `selector_result`: `READY`; 129 available; T011, T012 and T013 selected; no shortage.
- `prior_worklogs_reviewed`:
  - `.agents/worklog/2026-11-17/implement-study-screens-apis-T011.md` — preserve source/DD/runtime separation; do not fabricate fields or permissions; use focused frontend/API/build checks when coding a supported slice.
  - `.agents/worklog/2026-11-17/implement-study-screens-apis-T012.md` — broad objective remains API role organization plus all 83 Study Web screens; retain backend fake-DB/runtime limitations and preserve dirty state.
  - `.agents/worklog/2026-11-17/implement-study-screens-apis-T013.md` — keep int64/string and contract discrepancies explicit; implement only behavior supported by current source/approved DD; overall objective remains 20% active.
- `shortage`: `none`.
- Additional context read: `.agents/AGENTS.md`, `.agents/context-map.md`, `.agents/project/workflows.md`, `.agents/project/agent-control.md`, `.agents/worklog/README.md`, `.agents/worklog/TEMPLATE.md`, `.agents/web-work/study/{AGENTS,INDEX}.md`, `.agents/web-work/study/workflows/screen-implementation.md`, `.agents/server-study/{AGENTS,INDEX}.md`, `.agents/server-study/modules/README.md`, `.agents/server-study/apis/declared-routes.md`, and relevant `context-manifest.json` entries.
- Validator baseline: `node scripts/validate-agent-context.mjs` → `AGENT_CONTEXT_INVALID`, exit 1, 1,431 lines, captured at `/tmp/study-agent-context-T020-baseline.log`; includes repo-wide missing DB Admin pages, orphan skill resources and stale-context findings. Compare findings by identity after any context edits.

## EXPECTED_BEHAVIOR

- Full active objective remains: (1) organize Study Server APIs by `admin`, `student`, `mentor`, `guest`, `shared`; (2) implement all 83 Study Web screens from DD/Stitch/catalogs; (3) run backend/API checks while coding and fix/add API only when DD/BD/source evidence supports it; (4) read relevant screen/API/server DD and diagrams; (5) deliver correct, usable UI connected to supported backend behavior; and (6) plan before operations. This task advances that objective without redefining it around one screen.
- Overall objective remains **20% ACTIVE** at T020 start.
- Candidate from current tracker/catalog: SH-07 “Theo dõi tác vụ bất đồng bộ”, `/operations/:operationId`, P2, API #18. This is provisional until its full DD, API #18 DD/source/tests, diagrams, owner and ID contracts are reviewed.
- Study FE scope: `screens=SH-07; APIs=#18`. API #18 is classified in Shared by the Study Server registry; the client route is Shared and remains gate-only.

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 20% | 20% | Complete preflight: read SH-07 inventory/DD/Stitch plan/images/HTML/markers, API #18 DD/open questions/AC diagrams/catalog/source/tests, Study Web/Server rules, route graph, worktree and test/runtime configuration; record current source and unresolved conflicts. | `DONE` |
| 60% | 80% | Implement the largest source-supported slice: add a Shared SH-07 route and accessible unavailable gate only. Do not call API #18 or render an operation ID/status/result; omit polling, retries, unsafe return CTA and prototype diagnostics. Keep the API descriptor UNWIRED and update DD/context to distinguish gate UI from operation tracking, which remains blocked. | `DONE` |
| 20% | 100% | Run focused SH-07 route test, focused API #18 HTTP tests, Study Web production build and browser demo if a browser surface is available; otherwise use the route test plus local HTTP deep-link check and record that visual browser behavior is unverified. Run diff/context checks and record remaining gates. No fixtures or data cleanup are planned. | `DONE_WITH_BROWSER_LIMITATION` |

**Current T020 progress: 100%. Overall objective: 20% ACTIVE.**

## M0_CANDIDATE

- `apps/study-client/docs/list_screen.md` identifies SH-07 at `/operations/:operationId`, API #18, P2, and caller links from ST-07/ME-15/AD-21/AD-25.
- SH-07 DD and Stitch source mark generic tracking `BLOCKED`: UUID vs int64, owner-only vs owner/Admin, lifecycle/result, producer mapping, polling and safe return remain unresolved. The prototype's sample ID, status cards, diagnostic panel and architecture claims are explicitly non-runtime content.
- AC-12/25/36/38 and the reusable Operation schema specify UUID and owner-only; the API catalog row says int64 while its tracking summary says owner-or-Admin. No approved change resolves these discrepancies.
- Study Web has a runnable Angular 22 app; `shared.route.ts` has SH-01/02/03/06 but no SH-07 route. `API_018` is `UNWIRED`; `StudyApiService` throws for UNWIRED descriptors.
- Study Server API #18 is in Shared and is source-wired. It validates UUID, allows AC-listed roles, filters a read-only notification/outbox query by authenticated owner, and projects notification-only `NOTIFICATION_DISPATCH` with local `QUEUED`/`FAILED`/`SENT` statuses. Its DD remains Draft and no generic Study Operation table/lifecycle/result exists.
- Focused frontend command: `npm test -- --include=src/app/app.routes.spec.ts` from `apps/study-client`; production build: `npm run build`. Focused API command: `.venv/bin/python -m pytest tests/modules/shared/api_18_operations/test_operations.py -q` from `apps/study-server`. Browser demo uses the local app and a non-sensitive preview path; no backend fixture is needed.

## EXECUTION_PLAN — V1 (recorded before source changes)

### Scope and screen structure

- Screen: SH-07 under `apps/study-client/src/app/features/shared/SH07/`, with exactly four direct folders: `data-access/`, `models/`, `pages/`, `ui/`.
- Add one route `operations/:operationId` to the existing Shared group in `features/shared/shared.route.ts`; do not change top-level `app.routes.ts`, add guards, or add wildcard/fallback routes.
- Use the established Shared layout, which is a child `RouterOutlet`; build only route-backed header navigation to `/`, `/courses`, `/courses/search`, `/login`, and `/register` if needed.
- The page must not read or display the raw route ID. Render a static, accessible message that no verified task status is available in this client. No status, progress, operation kind, result, ownership, timestamps or error details are shown.
- Keep the API #18 descriptor `UNWIRED`; do not inject `StudyApiService` or issue a request. Add no API DTO/model, polling/SSE, retry/cache, clipboard, contract modal, lifecycle reference cards, developer diagnostics, architecture diagram, download affordance, caller-specific return link or fake operation data.
- Keep all four screen folders. Put the route page in `pages/`, the small unavailable notice in `ui/`, and short README boundary notes in `data-access/` and `models/` explaining why no service or Operation model exists until the contract is approved.

### Route, navigation and failure behavior

- Direct `/operations/<segment>` navigation renders the same unavailable notice for any segment; it does not validate/normalize/echo it and does not send an API request.
- `/` remains the existing SH-01 route. Use only route targets confirmed in current Shared/Guest route definitions. Do not add product recovery behavior or claim browser history is caller-safe.
- The unavailable notice describes client capability only, not backend health, job status or a retry policy. No modal/clipboard actions are carried from the prototype.

### Documentation and context

- Update SH-07 DD current-source notes and relevant route/API/test sections to say the gate route is implemented while operation tracking remains `IMPLEMENTATION BLOCKED`; keep API #18 DD Draft and its contract questions open.
- Update Study Web context/index and the screen tracker only where their current SH-07/SH-screen statements become inaccurate. Preserve earlier dirty edits; compare diffs before patching.
- Update `docs/tasks/process.md` at each milestone; overall objective stays 20% ACTIVE.

### Verification and cleanup

- Add a direct-route test for `/operations/<preview-only-segment>` that asserts the SH-07 notice appears and the route ID is neither rendered nor sent to the server. Existing root route coverage must continue to assert SH-01 at `/`.
- Run the focused Angular route spec, `npm run build`, and the focused API #18 pytest suite. Backend source is not in this slice; its tests establish current API evidence only.
- Start the Angular app and inspect `/` and `/operations/preview-only` in a local browser if one is connected. If no browser exists, record that limitation and use the route rendering test plus local HTTP GETs for both paths; do not claim visual verification. Do not submit forms or use real operation IDs. No DB, API fixture or persistent browser data is created, so no cleanup command is needed.
- Finish with `git diff --check` and `node scripts/validate-agent-context.mjs`; compare validator findings against `/tmp/study-agent-context-T020-baseline.log` and report pre-existing repository findings separately.

## CURRENT_BEHAVIOR

- Source/config: Angular 22 app with Shared lazy route group and route-backed SH-01/02/03/06; SH-07 absent. API_018 client descriptor is UNWIRED. API #18 backend route/module/query are source-wired under Shared but notification-only.
- Runnable tests: Angular uses `ng test --watch=false` (focused route test via `--include`); Study Server uses pytest and has a focused API #18 suite.
- Runtime wiring: no SH-07 page/caller/API client request existed at M0. The planned coding slice adds only an unavailable UI route; operation tracking remains unverified/blocked.

## SOURCE_TRACE

```text
SH-07 /operations/:operationId
  -> SharedLayout child route
  -> static unavailable notice (no route-param echo, no API call)

API #18 remains a separate, source-wired Shared endpoint:
  route -> UUID/auth validator -> owner-bound notification/outbox query
  -> notification-only envelope; no generic payment/export lifecycle
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Operation ID | AC diagrams/shared schema/current API route use UUID; API catalog row declares int64. | `DISCREPANCY / OPEN` | SH-07 route accepts a path segment but does not parse, echo or submit it. |
| Operation owner and role | AC diagrams/API row say owner-only; tracking summary says owner-or-Admin; current #18 binds authenticated owner for notifications. | `DISCREPANCY / OPEN` | No client-side role or ownership policy is added. |
| Lifecycle/result | Generic contract has no canonical enums/store; current #18 projects notification-only QUEUED/FAILED/SENT. Payment/export producer/result mapping is missing or inconsistent. | `BLOCKED / SOURCE_REQUIRED` | No operation status mapping, result UI, polling or retry. |
| Role API organization | `.agents/server-study/AGENTS.md` and source path classify #18 under Shared. | `VERIFIED_SOURCE` | Preserve Shared classification; this screen slice does not reorganize server modules. |
| Overall objective | `docs/tasks/process.md` and prior worklogs retain 20% active. | `ACTIVE` | T020 is one slice only. |

## CHANGES

- At task start, added this T020 worklog and 0% process row; M0 completed and process/worklog recorded 20% before source changes.
- Implemented the gate-only SH-07 route/page and updated SH-07 DD plus Study Web context. No operation model/API caller or backend change was added.
- M1 and M2 are complete for the gate-only slice. Generic operation tracking remains blocked; visual browser verification was unavailable. Validator baseline and final outputs are recorded.

## VERIFICATION

| Command / evidence | Result | Status |
|---|---|---|
| Coding worklog selector | `READY`; T011/T012/T013 selected and read in full. | `VERIFIED_PREFLIGHT` |
| Context validator baseline/final | `AGENT_CONTEXT_INVALID`, exit 1, 1,431 lines each; `/tmp/study-agent-context-T020-baseline.log` and `...-final.log` are byte-identical, with existing DB Admin/orphan-skill findings and no T020 finding. | `NO_NEW_FINDINGS` |
| SH-07/API #18/source review | Inventory, full screen DD/Stitch source and visuals, API #18 DD/open questions/AC/catalog/source/test/config inspected. | `M0_COMPLETE` |
| Gate route/page and source/context docs | Implemented from PLAN V1; route renders unavailable notice and does not use the route segment or issue API #18. | `M1_COMPLETE` |
| Angular route spec | `npm test -- --include=src/app/app.routes.spec.ts`: 10 passed; includes root SH-01 and direct SH-07 route/no API request. | `PASS` |
| API #18 focused suite | `.venv/bin/python -m pytest tests/modules/shared/api_18_operations/test_operations.py -q`: 8 passed, 1 upstream Starlette/httpx deprecation warning; fake-session tests only. | `PASS` |
| Study Web production build | `npm run build`: pass; three existing Student CSS budget warnings, no SH-07 warning. | `PASS_WITH_EXISTING_WARNINGS` |
| Local route smoke and browser | HTTP GET root and SH-07 preview path both returned 200. CUA had no browser; no Chromium/Chrome/Playwright installed. | `HTTP_PASS; VISUAL_NOT_VERIFIED` |
| Diff/format | `git diff --check` pass. Prettier passes all new SH-07 files and produces no change for the T020 test block; whole dirty `app.routes.spec.ts` already fails Prettier at HEAD due unrelated formatting. | `PASS_WITH_PREEXISTING_FORMAT_DRIFT` |

## HANDOFF

- Remaining gates for full SH-07 tracking: API #18 canonical ID, owner/Admin policy, generic persistence/lifecycle/result, producer handoff, polling/retention and safe-return decisions.
- The gate-only T020 slice is complete. Continue the broader 83-screen objective with the next screen whose DD/contract dependencies are ready; return to SH-07 tracking when its contract blockers are resolved.
