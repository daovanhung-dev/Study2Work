---
task_id: "2026-11-21-load-full-project-web-coding-context-T042"
date: "2026-11-21"
primary_task_type: "coding"
secondary_task_types: ["docs"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies:
  - "Study Web AD06 -> Study Server API #73 GET /api/v1/admin/courses (context boundary only)"
status: "COMPLETE"
---

# Worklog: Load full project and web coding context — T042

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `READY`; 153 available; 3 selected; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-19/implement-all-study-screens-T004.md`
    - carry_forward: Read all 1,709 lines. Recent Study Web work spans Guest, Student, Mentor, Shared and Admin surfaces; prior claims are historical context and current source must be rechecked. Preserve the pre-existing dirty tree. Do not infer feature acceptance from route presence or old screen percentages. Several API, schema, permission, design and runtime gaps remain explicitly gated.
  - path: `.agents/worklog/2026-11-19/implement-study-web-screens-T041.md`
    - carry_forward: Approved decisions were recorded for resources, VNPay, Markdown lecture content, in-app notifications, operations, moderation, reporting and export, but each source claim must be checked against the current checkout. No test/runtime status from this log is current evidence for this task.
  - path: `.agents/worklog/2026-11-18/implement-remaining-study-screens-T040.md`
    - carry_forward: Preserve existing user changes; Study Web has Angular-specific boundaries while Work Web is React; unsupported behavior stays gated; historical no-test limits applied to that task only.
- shortage: `none`
- baseline: `git status --short --branch` reports branch `develop...origin/develop` and extensive pre-existing modified/untracked files, including `.agents/`, `apps/study-client/`, `apps/study-server/`, and migration paths. Command output was truncated (778 lines total), so no exact dirty-file count is asserted. Preserve all existing changes.

## EXPECTED_BEHAVIOR

- Requirement: load full project context and the registry-wired web coding workflow/skill so the next web coding task can follow current project boundaries.
- Canonical contract/approved DD: user-provided root `AGENTS.md`; `.agents/AGENTS.md`; `.agents/context-map.md`; `.agents/context-manifest.json`; global project and web-work context pages. Current source remains authoritative where context snapshots conflict.
- Registry finding: no dedicated web-coding skill is registered. The verified coding workflows are `.agents/project/workflows.md` (`coding`) and `.agents/web-work/study/workflows/screen-implementation.md` (`study-web-screen-coding`). The latter is the applicable Study Web workflow for the open AD06 tabs. `code-review` is review-only and was not activated.
- No specific feature, screen or source edit was requested in this task.

## MILESTONES

Progress starts at 0%; the weights are task-specific and total 100%.

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 40% | 40% | Complete coding worklog preflight: read router/context map, run selector, read all 3 selected worklogs, record carry-forward facts and current dirty baseline in this worklog. | `DONE` |
| 60% | 100% | Load registered global project context and both web-work branches; resolve the web-coding skill/workflow through the registry; load the Study Web/AD06 source and its API #73 dependency; record paths/status and run context validation. | `DONE` |

Current verified task progress: `100%` (M1 and M2 complete).

## CURRENT_BEHAVIOR

- Source/config: current branch is `develop`; the worktree is already extensively dirty. `web-work` contains distinct Study Angular and Work React branches. Study Web source is Angular 22 standalone; Work Web uses React/Express conventions. Do not mix their patterns. The open tabs point to Study Admin screen AD06 and its API #73 boundary.
- Study Web design/rules: use the Study-only light-first ocean palette and accessibility rules; the design guide is intended design, not runtime evidence. Screen boundaries are `pages/`, `ui/`, `data-access/`, `models/`; source and verified API contracts decide behavior.
- AD06 current source: `/admin/courses` is registered by `features/admin/admin.routes.ts`. `AD06Page` calls `AD06ApiService`, which uses Admin API #73. `AdminApiService` obtains a memory-held Admin token, adds Bearer auth and delegates to `StudyApiService`; the API descriptor resolves to `GET /admin/courses` under `/api/v1`.
- AD06 current behavior: page requests include `page` only; unsupported search/status/mentor/category/create/export controls remain disabled. It checks the success business code and response projection/pagination, handles loading/error/empty/out-of-range and COUNT/LIST mismatch separately, preserves returned rows on mismatch while suppressing stale totals/page controls, and offers retry/recovery. Course IDs display precision-safely; detail navigation is provided only for positive JavaScript-safe IDs. Current source does not verify authenticated browser, live API/DB or deployment.
- API #73 current source: shared `ADMIN` JWT guard precedes query parsing/DB access; exact `status` and signed-int64 `mentor` filters; valid `category` is rejected with 422 before DB; page defaults to 1, fixed size 20 and `courses.id ASC` are source choices; count/list share predicates; Course mapping uses the shared mapper; the read path does not commit. Focused source tests exist but were not run in this task.
- Runnable tests: not run; no feature implementation or verification was requested.
- Runtime wiring: source route and API caller were inspected; authenticated browser/live API/DB/deployment runtime remains unverified.

## SOURCE_TRACE

```text
user request -> project registry/context graph -> global + web scope pages -> Study Web screen-coding workflow -> AD06 caller -> API #73 client boundary -> Study Server #73 route/module/test/DD
```

## CONTEXT_LOADED

- Global/project router and graph: `.agents/AGENTS.md`, `.agents/context-map.md`, `.agents/context-manifest.json`, `.agents/project/INDEX.md`, `agent-control.md`, `architecture.md`, `business-code.md`, `conventions.md`, `database.md`, `dependencies.md`, `design.md`, `source-status.md`, `contracts.md`, `workflows.md`, `.agents/skills/INDEX.md`, `.agents/worklog/README.md`, `.agents/worklog/TEMPLATE.md`.
- Prior coding worklogs: T004, T041 and T040 listed above; all three were read in full after the mandatory selector.
- Web scope graph: `.agents/web-work/AGENTS.md`, `INDEX.md`, `architecture.md`, `conventions.md`, `dependencies.md`, `modules/README.md`, `workflows/README.md`; Study subcontext `.agents/web-work/study/AGENTS.md`, `INDEX.md`; Study-specific rules/design `.agents/web-study/frontend-rules.md`, `.agents/web-study/design.md`.
- Registered coding workflow: `.agents/web-work/study/workflows/screen-implementation.md` read in full. Registry status is `VERIFIED` for `study-web-screen-coding`; generic `coding` is also `VERIFIED` in `.agents/project/workflows.md`. The registry contains no dedicated general web-coding skill. `createDD-markdown` is for Web/API DD; `code-review` is review-only.
- Study app architecture and open-tab source: `apps/study-client/gui/architech.md`; `core/constant/api.constants.ts`; AD06 `data-access/ad06-api.service.ts`, `data-access/ad06-api-boundary.ts`, `models/ad06-screen.model.ts`, `ui/ad06-screen.ui.ts`, `pages/ad06-page.ts`, `pages/ad06-page.html`, `pages/ad06-page.spec.ts`; Admin shared `admin-api.models.ts`, `admin-api-guards.ts`, `admin-screen-renderers.ts`, `admin-screen-state.ts`, `admin-query-params.ts`; `core/http/admin-api.service.ts`, `study-api.service.ts`; `core/auth/admin-session.service.ts` token/refresh references; `features/admin/admin.routes.ts`.
- AD06 requirement context: package `apps/study-client/docs/dd_screens/AD-06-DanhSachKhoaHocQuanTri/00-overview.md`, `04-api-integration.md`, and `07-test-cases.md`; current AD06 unit spec was read but not run. Full screen-package image/HTML/event-by-event implementation workflow is deferred until an actual AD06 coding task.
- Cross-scope API boundary: `.agents/server-study/AGENTS.md`, `INDEX.md`, `modules/README.md` API #73 section, `tests.md` relevant #73 status, and API #73 `00_Cover.md`, `02_Overview.md`, `03_Request.md`, relevant `04_Response.md` sections, and `OPEN_QUESTIONS.md`; exact source at `apps/study-server/app/api/v1.py`, `app/modules/admin/api_73_admin_courses_list/{models,validate,query,view}.py`, and focused test `tests/modules/admin/api_73_admin_courses_list/test_admin_courses_list.py`.

## EVENT_LOG

| Events | Sources / operation | Result |
|---|---|---|
| E1–E84 | Mandatory worklog preflight, global project context, web-work scope/context graph and registry inspection (receipts already delivered in task chat). | M1 completed; prior logs and dirty baseline recorded. |
| E85a–E85b | Initial read of Study design/frontend-rules pages. | Output truncated; explicitly not counted as read. |
| E86–E87 | Corrected the assumed path, then located actual `.agents/web-study/` pages and registered workflow. | Paths resolved from checkout. |
| E88–E90 | Read Study Web design, frontend-rules and screen-coding workflow in small chunks. | All three read; design target, Angular boundaries, accessibility and workflow requirements recorded. |
| E91–E94 | Surveyed Study Angular architecture and AD06/API #73 client source, route, types and spec. | Open-tab source path and current AD06 caller verified. |
| E95–E97 | Loaded server-study scope/indexed #73 module, route, validator, query, view/model and test-context evidence. | Cross-scope dependency confirmed; source choices separated from Draft/DERIVED contract. |
| E98–E99 | Read AD06 overview, API integration, test plan and reread DD in smaller chunks after truncation. | Expected behavior, current-source addendum and open gates recorded; no test execution. |
| E100–E104 | Verified route, helper/template state handling, ID rendering, HTTP transport, query serialization and session token references. | Client-to-server source trace completed; browser/live runtime remains unverified. |
| E105 | Updated this worklog; ran `node scripts/validate-agent-context.mjs`. | Validator returned `AGENT_CONTEXT_INVALID` with repository-wide missing DB Admin context/source, orphan skill resource and stale/broken context references; no unrelated repair was made. |
| E106 | Read API #73 `03_Request.md` separately after the combined DD output was truncated. | Bearer/ADMIN, no body/size/sort, and category/page derived choices confirmed. |
| E107–E108 | Finalized milestone/worklog status; inspected exact worklog lines after one patch failed without changes. | No source changes from the failed patch; final validator rerun returned exit code 1 and `AGENT_CONTEXT_INVALID` with the same repository-wide findings. |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Dedicated web-coding skill | `.agents/skills/INDEX.md` and `.agents/context-manifest.json` register Study screen coding as a workflow; no general web-coding skill is registered. | `NOT_FOUND` (dedicated skill); `VERIFIED` (`study-web-screen-coding` workflow) | Use the registered workflow for future Study screen coding; do not call the review-only skill for coding. |
| Study Web route filename convention | `.agents/web-study/frontend-rules.md` says `<group>.route.ts`; `apps/study-client/gui/architech.md` and current source use `admin.routes.ts`. | `DISCREPANCY` | For current behavior, source confirms `admin.routes.ts`; do not silently reconcile the docs. |
| API #73 design vs runtime choices | API catalog/DD declare category and do not finalize page size/order/permission mapping; current source rejects category and uses fixed size 20, ID ASC and shared role `ADMIN`. | `DISCREPANCY`; API DD `Draft — Needs Confirmation`; several runtime choices `DERIVED` | Keep category/permission/pagination/status/schema decisions gated; use source only to describe current behavior. |
| API #73 test-count snapshots | `.agents/server-study/modules/README.md` and parts of `tests.md` retain 830/845 historical suite counts; `.agents/server-study/AGENTS.md` reports a later 1,492-test full suite on 2026-11-16. | `DISCREPANCY` (dated snapshots) | No tests were run in this context-load task; report no current pass result. |
| Authenticated runtime / persistence | AD06 and server context explicitly leave browser, live API/DB and deployment unverified; tests use isolated/fake DB evidence. | `NOT_VERIFIED` | Source wiring does not establish production behavior. |
| Exact next feature task | User asked to load context; no implementation target was specified. IDE tabs point to Study Client AD06 files. | `NOT_SPECIFIED` | Context is prepared around AD06; the full screen package/images/HTML must be read if a concrete screen implementation is requested. |

## CHANGES

- Files changed: this task worklog only; no application source or tests changed.
- CONTEXT_UPDATES: none planned; this task loads existing context only.
- Context pages changed: none.
- Assumptions: “full project context” follows the repository's progressive loading graph, not a full-repository read. Study Server was loaded only for the actual API #73 boundary. “Web coding skill” resolves to the registered Study Web screen-coding workflow because no dedicated web-coding skill exists in the registry.

## VERIFICATION

| Command / evidence | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | `READY`; T004, T041, T040 selected and read in full. | `VERIFIED_PREFLIGHT` |
| `git status --short --branch` | Branch `develop...origin/develop`; extensive dirty worktree; exact file count not asserted because output was truncated. | `VERIFIED_BASELINE` |
| Source/context inspection | Pages and source paths listed under `CONTEXT_LOADED`; no source mutation. | `VERIFIED_CONTEXT_LOAD` |
| `node scripts/validate-agent-context.mjs` | `AGENT_CONTEXT_INVALID`; output includes missing `.agents/db-admin/` pages and source roots, orphan `.agents/skills/create_dd_screen/` resources, broken db-admin links and stale context entries. These are repository-wide issues outside the requested web-context load; no unrelated scope repair was made. | `REPOSITORY_CONTEXT_INVALID` |
| Tests/build/lint/browser/API runtime | Not run; no implementation requested. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: none for context loading; the repository-wide context validator remains invalid for unrelated DB Admin and stale/orphan context entries. Exact feature target is not specified.
- Next owner/action: for a concrete Study Web screen task, complete `study-web-screen-coding` preflight, read the screen's full DD/images/HTML and verify source/contracts before planning implementation. For Work Web, use its separate React/Express patterns.
