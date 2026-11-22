---
task_id: "2026-11-22-study-context-bugfix-prep"
date: "2026-11-22"
primary_task_type: "fix"
secondary_task_types: ["docs"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["Study Web to Study Server API boundary; contract status to be verified"]
status: "VERIFIED"
---

# Worklog: Prepare Study project context for bug fixing

Read-only context handoff. The user has not supplied a specific bug report or target path.

## READ_PLAN

| Path | Needed section/range | Task-specific reason | Status |
|---|---|---|---|
| `AGENTS.md` | Supplied task context; router/task rules | Classify and route this request without reopening the supplied file | `READ_FROM_CONTEXT` |
| `.agents/AGENTS.md` | Scope registry, read-set, target, and worklog rules | Required repository bootstrap | `READ` |
| `.agents/context-map.md` | Bootstrap sequence; Study tree, scope, and contract graph | Route Study Web and Study Server pages and dependencies | `READ` |
| `.agents/context-manifest.json` | Registry entries for worklog, Study scopes/subcontext, workflows, and Study OpenAPI | Verify machine-readable wiring before loading pages | `READ` |
| `.agents/project/agent-control.md` | Target, read-set, worklog, and evidence rules | Required all-scope task control | `READ` |
| `.agents/target.md` | Active target table | Preserve/update the only live progress tracker | `READ` |
| `.agents/worklog/README.md` | Creation, read-set, preflight, and ordering requirements | Follow canonical worklog workflow | `READ` |
| `.agents/worklog/TEMPLATE.md` | Required fields and sections | Keep this task log canonical | `READ` |
| `scripts/select-worklogs.mjs` | CLI and selection behavior | Run the required exact-type preflight | `READ` |
| `.agents/worklog/2026-11-22/study-context-bugfix-prep.md` | Current task log metadata only | Selector returned this current log as a newest `fix` match; it is not prior work | `SKIPPED` |
| `.agents/worklog/2026-11-21/fix-study-admin-login-refresh-tokens.md` | Relevant prior task summary, source trace, verification, and handoff | Carry forward recent Study Admin bug-fix context | `READ` |
| `.agents/worklog/2026-11-15/fix-st12-st26-visual-match.md` | Relevant prior task summary, source trace, verification, and handoff | Carry forward recent Study Web UI bug-fix context | `READ` |
| `.agents/project/INDEX.md` | Cross-scope project context routing | Study Web and Study Server cross-scope boundary | `READ` |
| `.agents/project/workflows.md` | `fix` workflow and verification order | Required by the registered fix workflow | `READ` |
| `.agents/project/architecture.md` | Ownership/deployable boundaries for Study only | Understand current client/server ownership | `READ` |
| `.agents/project/dependencies.md` | Study dependency edges only | Confirm whether any other scope is actually required | `READ` |
| `.agents/project/contracts.md` | Study contract status and boundary notes | Confirm the Study Web/Server API evidence boundary | `READ` |
| `.agents/project/database.md` | Study-related database status only | Check known Study DB boundary; file is already dirty and must be preserved | `READ` |
| `.agents/web-work/AGENTS.md` | Study-specific routing only | Required parent Web scope instructions | `READ` |
| `.agents/web-work/INDEX.md` | Study subcontext routing only | Find the canonical Study Web page graph | `READ` |
| `.agents/web-work/study/AGENTS.md` | Study Web source, DD, screen, and test rules | Load the Study Web-specific context; file is already dirty and must be preserved | `READ` |
| `.agents/web-work/study/INDEX.md` | Study Web page graph | Choose exact current client context and source paths; file is already dirty and must be preserved | `READ` |
| `.agents/web-work/study/workflows/screen-implementation.md` | Relevant bug-fix workflow requirements | Prepare for a future Study Web screen bug report if applicable | `READ` |
| `.agents/web-study/AGENTS.md` | Scope instructions | Check whether a separate Study Web scope entry exists; manifest currently routes through `web-work/study` | `SKIPPED` |
| `.agents/web-study/INDEX.md` | Scope page graph | Check whether a separate Study Web index exists; manifest currently routes through `web-work/study` | `SKIPPED` |
| `.agents/web-study/design.md` | Relevant visual/interaction guidance | Support future UI bug triage if applicable | `READ` |
| `.agents/web-study/frontend-rules.md` | Relevant layer and dependency rules | Support future client bug trace if applicable | `READ` |
| `.agents/server-study/AGENTS.md` | Scope instructions | Required Study Server instructions | `READ` |
| `.agents/server-study/INDEX.md` | Page graph and source routing | Find exact server context for future bug triage | `READ` |
| `.agents/server-study/architecture.md` | Relevant module and layer ownership | Prepare server-side bug trace | `READ` |
| `.agents/server-study/apis/declared-routes.md` | Route status and declared API map | Identify source-backed Study endpoint entry points | `READ` |
| `.agents/server-study/core/runtime.md` | Application/router/runtime wiring | Trace route callers when a bug is supplied | `READ` |
| `.agents/server-study/core/database-security.md` | Relevant Study DB/RLS boundary | Prepare side-effect/security trace | `READ` |
| `.agents/server-study/database.md` | Study migration/schema status | Check current DB context; file is already dirty and must be preserved | `READ` |
| `.agents/server-study/modules/README.md` | Module ownership/index only | Route a future bug to the exact API module | `READ` |
| `.agents/server-study/tests.md` | Test layout and runnable commands | Prepare regression verification entry point | `READ` |
| `.agents/server-study/workflows/README.md` | Fix workflow only | Load registered Study Server workflow | `READ` |
| `contracts/openapi/study` | Existence/status check only; do not open unless a contract file is present | Verify manifest `NOT_FOUND` status and avoid inventing an API contract | `CHECKED_BY_TOOL` |
| `contracts/openapi/study/README.md` | Placeholder/status statement | Verify the exact Study OpenAPI contract gap | `READ` |
| `apps/study-client/gui/architech.md` | Angular app composition and feature structure | Follow the canonical Study client architecture pointer | `READ` |
| `apps/study-client/src/app/app.routes.ts` | Current route composition only | Establish source-backed Study Web entry routing | `READ` |
| `apps/study-client/src/app/core/constant/api.constants.ts` | API descriptor registry structure and status semantics | Establish how Study client API IDs are represented | `READ` |
| `apps/study-client/src/app/core/http/study-api.service.ts` | Generic transport and error mapping | Establish the client API boundary for future trace | `READ` |
| `apps/study-client/package.json` | Scripts and test/build tool versions only | Record client verification entry points without running them | `READ` |
| `apps/study-server/app/main.py` | App composition only | Confirm current server startup entry | `READ` |
| `apps/study-server/app/api/v1.py` | Router inclusion only | Confirm current Study API route composition | `READ` |
| `apps/study-client/src/app/features/guest/guest.route.ts` | Guest routes including GS-07 | Verify current route-to-screen wiring behind the detected context discrepancy | `READ` |
| `apps/study-client/src/app/features/guest/GS07/` | Filename inventory only | Identify the exact current GS-07 page/data-access/test files before reading them | `CHECKED_BY_TOOL` |
| `apps/study-server/app/modules/guest/api_12_resources_detail/` | Filename inventory only | Identify current API #12 source layers for the detected context discrepancy | `CHECKED_BY_TOOL` |
| `apps/study-server/tests/modules/guest/api_12_resources_detail/` | Filename inventory only | Identify current API #12 regression test entry point | `CHECKED_BY_TOOL` |
| `apps/study-client/src/app/features/guest/GS07/pages/gs07-page.ts` | Page routing/event/API behavior only | Verify whether current source consumes the resource ID and invokes data access | `READ` |
| `apps/study-client/src/app/features/guest/GS07/data-access/gs07-resource.service.ts` | API #12 descriptor call and response mapping | Verify the current client-to-API call behind the context discrepancy | `READ` |
| `apps/study-client/src/app/features/guest/GS07/models/gs07-resource-screen-state.model.ts` | State mapping only | Identify the current resource loading/error states | `READ` |
| `apps/study-client/src/app/features/guest/GS07/pages/gs07-page.spec.ts` | API #12 caller behavior tests | Check source-backed focused verification entry point without running tests | `READ` |
| `apps/study-server/app/modules/guest/api_12_resources_detail/view.py` | API #12 read/authorization/response flow | Verify current server side effects and response behavior | `READ` |
| `apps/study-server/app/modules/guest/api_12_resources_detail/query.py` | API #12 SQL constants | Verify current persistence read shape | `READ` |
| `apps/study-server/app/modules/guest/api_12_resources_detail/validate.py` | API #12 request/auth/access validation | Verify access control path | `READ` |
| `apps/study-server/app/modules/guest/api_12_resources_detail/models.py` | API #12 response fields only | Confirm current response projection without inventing contract fields | `READ` |
| `apps/study-server/tests/modules/guest/api_12_resources_detail/test_resources_detail.py` | API #12 HTTP tests only | Identify existing regression coverage without running tests | `READ` |
| `scripts/validate-agent-context.mjs` | Validation command only; do not inspect script source | Required final validation after updating worklog/target context artifacts | `CHECKED_BY_TOOL` |

## LEAF_TARGET_PLAN

| Target | Single operation | Acceptance evidence |
|---|---|---|
| Ghi nhận trạng thái Git để bảo toàn thay đổi hiện có | Record active branch and existing dirty paths | Captured `git status --short --branch`; no pre-existing files changed |
| Đọc worklog fix liên quan Study để tiếp nhận carry-forward | Read only the selected `fix` worklogs | Selector output and concise carry-forward facts recorded below |
| Nạp hướng dẫn và index của Study Web và Study Server | Read registered Study context pages | Scope/subcontext routes and boundaries recorded below |
| Xác nhận trạng thái contract Study Web ↔ Study Server | Check registered API contract and current route/source references | Contract status and limitations recorded with evidence paths |
| Lập bản bàn giao context để bắt đầu trace bug Study | Record current source/test routing and missing bug-specific inputs | Worklog handoff provides exact next step without claiming a bug was traced |

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `fix`
- selector_command: `node scripts/select-worklogs.mjs --type fix --limit 3` failed (`node: command not found`); fallback `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type fix --limit 3` succeeded.
- selector result: `available: 11`, `selected: 3`, `status: READY`.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-21/fix-study-admin-login-refresh-tokens.md`
    - carry_forward: API #03 login source had been traced through `AdminLayout.signIn` → `AdminSessionService.login` → `/api/v1/auth/login` → token issuance and refresh-token persistence. A prior live migration check established `refresh_tokens` in `neondb/dao_van_hung`; focused tests were fake-DB based and did not prove positive login with real credentials. Recheck current source/runtime before relying on this historical database result.
  - path: `.agents/worklog/2026-11-15/fix-st12-st26-visual-match.md`
    - carry_forward: Requested ST-12–ST-26 screenshot comparison was blocked by unavailable browser capture; HTTP 200 showed only the SPA shell, not visual correctness. That task changed no application source. Recheck current UI source and available browser tooling for any future visual bug.
- selector self-match: `.agents/worklog/2026-11-22/study-context-bugfix-prep.md` was selected as the newest `fix` match and skipped as not prior work.
- shortage: none reported by selector; one selected path was the current task log, so two prior worklogs were reviewed.

## EXPECTED_BEHAVIOR

- Requirement: Load Study project context read-only and prepare for a subsequent bug-fix trace.
- Canonical contract/approved DD: `.agents/project/workflows.md` requires reproduce → trace → root cause → smallest fix → regression test. `contracts/openapi/study/README.md` is a placeholder and defines no endpoint contract. No bug-specific requirement was supplied.

## TARGET_UPDATES

| Target | From → to | Evidence / reason |
|---|---:|---|
| Ghi nhận trạng thái Git để bảo toàn thay đổi hiện có | `0% → 0%` | Initial leaf target; acceptance is an observed branch/status snapshot and preservation of existing dirty files. |
| Ghi nhận trạng thái Git để bảo toàn thay đổi hiện có | `0% → 100%` | Initial and final `git status --short --branch` match for all pre-existing paths; temporary target rows were cleared after completion, leaving only this new worklog as the task change. |
| Lập bản bàn giao context để bắt đầu trace bug Study | `0% → 0%` | Initial leaf target; acceptance is an actionable handoff with bug-specific work explicitly pending. |
| Lập bản bàn giao context để bắt đầu trace bug Study | `0% → 100%` | Recorded current scope, API boundary, source trace, test entry points, validation result and the exact bug-specific information needed to begin a fix. |
| Đọc worklog fix liên quan Study để tiếp nhận carry-forward | `0% → 100%` | Read the two selector-matched prior logs; recorded the 2026-11-21 API #03 DB-verification boundary and 2026-11-15 browser-visual blocker. |
| Xác nhận trạng thái contract Study Web ↔ Study Server | `0% → 100%` | Manifest says `NOT_FOUND`; `contracts/openapi/study/README.md` is a placeholder, with no API schema to rely on. |
| Nạp hướng dẫn và index của Study Web và Study Server | `0% → 100%` | Read the registered Web/Study and Server context graphs and their visual, layer, database and test guidance; checked current route/API #12 source where architecture notes disagree. |

## CURRENT_BEHAVIOR

- Source/config: `apps/study-client/src/app/app.routes.ts` lazy-loads Shared, Guest, Student, Mentor and Admin groups; `/resources/:resourceId` loads `guestResourceRoutes`. `GS07Page` reads the resource ID and calls `GS07ResourceService`, which selects `StudentApiService` when authenticated and generic `StudyApiService` otherwise. API #12 is `GET /resources/{resource_id}` with descriptor status `WIRED`; generic transport prefixes `/api/v1` and rejects `UNWIRED` descriptors. Study Server `main.py` composes FastAPI and includes `app.api.v1.router`; API #12 validates signed-int64 IDs, reads resource/parent metadata, requires Student bearer plus ACTIVE enrollment for PRIVATE resources and requests a 300-second signed URL; PUBLIC URLs are constrained to HTTP(S). It returns `DESIGN_RESOURCE_RETRIEVED` with `id`, `name`, `type`, `url`, `visibility`, and nullable `lesson_id`.
- Runnable tests: Client package declares `npm test` (`ng test --watch=false`) using Angular 22/Vitest. Server guidance uses `uv run pytest`; focused client and server API #12 test files exist. Prior context records #11/#12 fake-source tests passing on 2026-11-21, but tests were not run in this task and do not establish live DB, storage or deployment behavior.
- Runtime wiring: Local architecture context reports the Angular dev proxy forwards `/api/v1` to Study Server loopback at `127.0.0.1:3003`; current production routing and authenticated browser/API/DB runtime remain unverified. DB context only has live `refresh_tokens` verification for the specific `neondb/dao_van_hung` target from 2026-11-21; other Study schema state is unverified.

## SOURCE_TRACE

```text
apps/study-client/src/app/app.routes.ts
  -> guestResourceRoutes (`guest.route.ts`, `/resources/:resourceId`)
  -> GS07Page (reads route ID, maps response/error state)
  -> GS07ResourceService (StudentApiService or StudyApiService)
  -> `GET /api/v1/resources/{resource_id}` (API #12 in `app/api/v1.py`)
  -> get_resource_detail -> validate_resource_id -> query resource and published parent
  -> PRIVATE: Student auth -> ACTIVE enrollment -> signed storage URL (300 sec)
     PUBLIC: validated direct HTTP(S) URL
  -> `DESIGN_RESOURCE_RETRIEVED` ResourceDetail envelope
  -> existing GS07 client spec and API #12 server test module
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Study Web to Study Server OpenAPI contract | Manifest says `NOT_FOUND`; `contracts/openapi/study/README.md` says artifacts will follow after the API grows beyond the health foundation | `NOT_FOUND` | Do not infer request/response fields from Work or DD files |
| GS-07 current implementation versus architecture snapshots | `context-map.md` and `apps/study-client/gui/architech.md` say gate-only; current dirty Study Web scope pages and `app.routes.ts`, `guest.route.ts`, GS07 page/service, API #12 route/module say source-wired | `DISCREPANCY` | Current source takes precedence; architecture/map remain stale and were not edited in this read-only handoff |

## CHANGES

- Files changed: this new worklog. `.agents/target.md` was used for live tracking and returned to its original empty table; all pre-existing modified/untracked files remain untouched.
- CONTEXT_UPDATES: none expected for this read-only context handoff.
- Context pages changed: none.
- Assumptions: `fix` is the primary type because this request prepares the next bug-fix task; no bug-specific trace can be completed without a reported symptom/path.
- Target progress updates and completion evidence: see `TARGET_UPDATES`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Initial `git status --short --branch` | `develop...origin/develop`; pre-existing modifications in project/server-study/Web Study pages and Admin layout; two untracked prior fix worklogs | `VERIFIED` |
| Final `git status --short --branch` | Same pre-existing modified/untracked paths; only this new worklog remains as the task change, and `.agents/target.md` matches its initial empty table | `VERIFIED` |
| `node scripts/select-worklogs.mjs --type fix --limit 3` | Could not start: `node: command not found` | `TOOL_UNAVAILABLE` |
| `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type fix --limit 3` | `available: 11`, `selected: 3`, `READY`; self-match plus two prior paths | `VERIFIED` |
| First `PATH=.../node scripts/validate-agent-context.mjs` run | `AGENT_CONTEXT_INVALID`; reported a temporary non-sequential target STT caused by target completion updates, which was corrected | `FIXED_AFTER_VALIDATION` |
| Final `scripts/validate-agent-context.mjs` via Node 22 wrapper after log/target completion | Exit 1 `AGENT_CONTEXT_INVALID`; zero target tracker or worklog findings. Repository findings: missing DB Admin context/source and contract, one missing registered Study Web source file, orphan skill resources, broken context links, and stale context snapshots. The selected 2026-11-21 worklog recorded the overlapping DB Admin, orphan-skill, and stale-context categories as baseline findings. | `BASELINE_INVALID` |

## HANDOFF

- Remaining blockers: No specific bug report, symptom, reproduction, or affected screen/API was supplied. The Study OpenAPI contract is a placeholder, and GS-07 architecture summaries are stale relative to current source.
- Next owner/action: Provide the affected screen/API, observed versus expected result, exact repro steps and any HTTP status/trace ID. Then reproduce against current source, trace caller → callee → DB/external side effect → response → tests, and implement the smallest supported fix.
