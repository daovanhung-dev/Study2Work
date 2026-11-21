---
task_id: "2026-11-21-prepare-study-web-screen-coding-T043"
date: "2026-11-21"
primary_task_type: "coding"
secondary_task_types: ["docs"]
project_scopes: ["web-work"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Prepare Study Web screen coding context — T043

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `READY`; 154 available; 3 selected; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-21/load-full-project-web-coding-context-T042.md`
    - carry_forward: The global project and Study Web context was previously loaded; Study Web uses Angular and Work Web uses React. The registered Study screen implementation workflow is verified. T042 prepared around AD-06/API #73 from then-open tabs, but the current screen and source must be confirmed for this request.
  - path: `.agents/worklog/2026-11-19/implement-all-study-screens-T004.md`
    - carry_forward: All 83 screen IDs are an inventory, not acceptance coverage. Recent changes and screen percentages are historical and must be checked against current source. Preserve the extensively dirty workspace; no tests were run in that task. Known API, design, permission, schema and runtime gaps remain gated.
  - path: `.agents/worklog/2026-11-19/implement-study-web-screens-T041.md`
    - carry_forward: Approved policy notes cover resources, VNPay, Markdown lecture content, in-app notifications, operations, moderation, reports and exports. Recheck current source before relying on any prior status; its implementation/verification boundary is historical.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Load project context and prepare for coding a Study Web screen.
- Canonical contract/approved DD: user-provided root `AGENTS.md`, `.agents/AGENTS.md`, `.agents/context-map.md`, current `.agents/context-manifest.json`, global project context, Web Work context, and Study Web screen implementation workflow.
- Screen-specific scope: no exact screen or feature was named in the request; use the most recent AD-06 context only as a candidate until confirmed by current workspace evidence.

## TARGET_UPDATES

| Target | From → to | Evidence / reason |
|---|---:|---|
| `Nạp context và chuẩn bị coding màn Study Web` | `0% → 0%` | Initial target created; acceptance requires current registry/context/workflow and Study Web source entry points to be loaded. |
| `Nạp context và chuẩn bị coding màn Study Web` | `0% → completed; row removed` | Loaded the registered global/Web/Study context, verified current Study Web routes and AD-06 candidate source, recorded validator baseline, and closed the context-preparation task. Exact screen remains to be named before implementation starts. |

## CURRENT_BEHAVIOR

- Source/config: `apps/study-client/src/app/app.routes.ts` lazy-loads `./features/admin/admin.routes`; `admin.routes.ts` maps `/admin/courses` to AD06. AD06 uses `AD06ApiService` and API #73 (`GET /admin/courses`); the route and feature files exist in current source. `apps/study-client/package.json` identifies Angular 22.2 and the `ng serve`, `ng build`, and `ng test --watch=false` scripts.
- Runnable tests: not run; this task prepares context and does not request implementation or tests. AD06 has `ad06-page.spec.ts`, inspected but not run.
- Runtime wiring: route/API source wiring is present; no authenticated browser, server, or database runtime was requested or exercised.
- Workspace state: branch `develop`, 788 pre-existing `git status --porcelain=v1` entries observed. Existing modifications in `admin-api.service.ts` and AD06 page CSS/HTML/TS were preserved; no application source was edited.

## CONTEXT_LOADED

- Router and workflow: `.agents/AGENTS.md`, `.agents/context-map.md`, `.agents/worklog/README.md`, `.agents/worklog/TEMPLATE.md`, `.agents/project/agent-control.md`, `.agents/project/INDEX.md`, and the project context pages for architecture, conventions, design, dependencies, contracts, business codes, database, and workflows.
- Registry: `.agents/context-manifest.json` and `.agents/skills/INDEX.md`; confirmed `study-web-screen-coding` is registered and verified at `.agents/web-work/study/workflows/screen-implementation.md`.
- Web scope: `.agents/web-work/AGENTS.md`, `.agents/web-work/INDEX.md`, architecture, conventions, dependencies, module/workflow indexes, and `.agents/web-work/study/{AGENTS.md,INDEX.md}`.
- Study Web details: `.agents/web-study/frontend-rules.md`, `.agents/web-study/design.md`, `.agents/web-work/study/workflows/screen-implementation.md`, and `apps/study-client/gui/architech.md`.
- Current source evidence: Study Client app/admin routes, AD06 page/data-access/models/UI sources, API constants and service chain, screen/endpoint catalogs, AD06 spec, and package scripts.
- The registered screen workflow's screen-specific DD, image, API, caller/callee, and test trace is deferred until a screen ID or behavior is supplied.

## SOURCE_TRACE

```text
user request -> project registry/context map -> coding worklog preflight -> global and Study Web context -> registered screen workflow -> current Study Client source
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Exact Study screen/feature | The request says to prepare coding for a Study Web screen but gives no screen ID or behavior. T042's AD-06 context is historical candidate evidence only. | `NOT_SPECIFIED` | Load general Study Web implementation context now; finish screen-specific DD/source/API trace once the target is known. |
| Scope architecture summary vs current Study Web routes | `.agents/web-work/architecture.md` describes Study Web business routes/auth/features as unwired; current `app.routes.ts`, `admin.routes.ts`, and AD06 sources show wired route and feature code. | `DISCREPANCY` | Follow current source for current behavior; do not revise unrelated context during this preparation task. |
| Route naming convention vs source | `.agents/web-study/frontend-rules.md` names singular `<group>.route.ts`; current source uses `admin.routes.ts`, also reflected by `gui/architech.md`. | `DISCREPANCY` | Recheck relevant module convention when a concrete screen is selected; no context correction made now. |
| Validator baseline | Baseline run before this task's worklog/target changes reported `AGENT_CONTEXT_INVALID`, missing `db-admin` context/source roots and links, orphan `create_dd_screen` resources, and `CONTEXT_STALE` findings across existing scopes including `web-work` and `web-work/study-web`. | `DECLARED_NOT_RUNNABLE` | These are pre-existing repository context issues; compare final validation against the saved baseline and report any additional findings without fixing unrelated pages. |

## CHANGES

- Files changed: this task worklog and `.agents/target.md` only; the target row is removed on completion, leaving the required table header.
- CONTEXT_UPDATES: none; this task loads existing context.
- Context pages changed: none.
- Application source changed: none.
- Assumptions: “full project context” means the registered progressive context graph and relevant Study Web pages, not an indiscriminate read of every repository file.

## VERIFICATION

| Command / evidence | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | `READY`; T042, T004 and T041 were selected and read in full. | `VERIFIED_PREFLIGHT` |
| Current source inspection | Confirmed Study Web admin route to AD06 and AD06 API #73 call in current source; inspected catalog entries and existing spec. | `VERIFIED_READ_ONLY`; tests not run |
| `git status --porcelain=v1` and targeted diffs | 788 dirty entries pre-existed; the relevant admin API/AD06 files were already modified. No source changes were made by this task. | `VERIFIED_PRESERVED` |
| `node scripts/validate-agent-context.mjs` baseline | Captured in `/tmp/t043-validator-baseline.log` before this task's worklog/target edits; exited non-zero with existing missing db-admin paths, orphan skill resources, broken links, and stale-context findings. | `BASELINE_INVALID` |
| Final `node scripts/validate-agent-context.mjs` | Exited 1 with `AGENT_CONTEXT_INVALID`; final output is byte-for-byte identical to the captured pre-edit baseline (`/tmp/t043-validator-baseline.log`, 1,784 lines). Existing missing db-admin paths, orphan skill resources, broken links, and stale-context findings remain; no new validator finding was introduced. | `BASELINE_INVALID_UNCHANGED` |

## HANDOFF

- Remaining input: exact screen ID or feature behavior is not specified; AD06 is only a current-source candidate and is not assumed to be the target.
- Next action: when the screen is named, follow `.agents/web-work/study/workflows/screen-implementation.md`, load its screen-specific DD/API/evidence, and trace current caller/callee/side effects/tests before editing.
