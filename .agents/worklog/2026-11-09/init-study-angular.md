---
task_id: "2026-11-09-init-study-angular"
date: "2026-11-09"
primary_task_type: "coding"
secondary_task_types: ["docs"]
project_scopes: ["web-work"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Khởi tạo Angular Study Web

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `READY`; 92 exact-type worklogs available; three selected and read.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: Preserve existing worktree changes; do not infer behavior beyond verified source/contracts.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: Keep scope narrow, retain source/design/runtime status distinctions, and do not invent API contract behavior.
  - path: `.agents/worklog/2026-10-26/implement-api76-admin-course-status.md`
    - carry_forward: Update the context registry when architecture changes and report verification limits explicitly.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Create a runnable Angular Study Web SPA and a detailed Vietnamese architecture guide at `apps/study-client/gui/architech.md`; preserve existing docs/assets; no business screens, API integration, auth, or test suite in this bootstrap.
- Canonical contract/approved DD: User-approved plan; Study Web visual and accessibility target at `.agents/web-study/design.md`; 83-screen inventory/DDs remain design evidence, not runtime contracts.

## CURRENT_BEHAVIOR

- Source/config: `apps/study-client/` contains `docs/` only; there is no Angular workspace, source, package manifest, or compiled `dist`. Existing Study Web context says `UNWIRED`. Node/npm versions were inspected in the planning pass as Node 22.23.3 and npm 10.9.9.
- Runnable tests: None exist or are requested for this bootstrap; no test suite will be added or run.
- Runtime wiring: No Study Web runtime exists. Study OpenAPI/API integration and deployment are outside this scope.

## SOURCE_TRACE

```text
user request -> Angular CLI workspace -> main.ts/bootstrap -> app config/router -> temporary root placeholder; no feature/API path is wired
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Study Web runtime | Current source tree has only docs/assets, while the approved plan requires an Angular scaffold. | `EXPECTED_BEHAVIOR / CURRENT_BEHAVIOR GAP` | Add only the runnable base SPA and keep feature/API behavior unwired. |
| Context status | Registry and Study Web pages currently say `UNWIRED` because no app source exists. | `CONTEXT_UPDATE_REQUIRED` | Move to `SKELETON_ONLY` after the scaffold is created and verified. |

## CHANGES

- Files changed: Angular CLI workspace/config/dependency files under `apps/study-client/`; root component/template/styles; architecture placeholders under `src/app/{core,layouts,shared,features}`; `README.md`; `gui/architech.md`; Study Web context pages and manifest; this worklog.
- CONTEXT_UPDATES: Registered the Angular scaffold as `SKELETON_ONLY`, added the Angular source/config inventory, and kept business routes/API/auth/deployment explicitly unwired or unverified.
- Context pages changed: `.agents/context-map.md`, `.agents/project/architecture.md`, `.agents/project/dependencies.md`, `.agents/web-work/AGENTS.md`, `.agents/web-work/INDEX.md`, `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`, `.agents/web-study/design.md`.
- Assumptions: Angular 22, npm, standalone feature-first, CSS design tokens, SPA without SSR, no generated or executed tests; preserve all existing `docs/` and context edits.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Angular CLI workspace generation | `npx @angular/cli@^22 new ... --standalone --routing --style css --ssr=false --strict --skip-git --skip-tests`; generated Angular CLI 22.2.6 / Angular core 22.2.5 and npm lockfile. No test specs or test target were retained. | VERIFIED_STATIC |
| `npm run build` | Production build succeeds; initial bundle 192.24 kB raw (52.35 kB estimated transfer). | VERIFIED_BUILD |
| `npm start -- --host 127.0.0.1 --port 4201` + headless Chrome DOM | Server returned the compiled SPA; rendered heading `Khung ứng dụng đã sẵn sàng` at `/`. Server stopped after smoke check. | VERIFIED_SMOKE |
| Tests | No `*.spec.ts` / `*.test.ts` files or `test` script/target; suite not run as requested. | NOT_REQUESTED |
| Context manifest JSON and required sources | JSON parses; all 23 Study Web required source paths exist; manifest status is `SKELETON_ONLY`. | VERIFIED_STATIC |
| `git diff --check` / docs status | No whitespace errors; `apps/study-client/docs/` has no changes. | VERIFIED_STATIC |
| `node scripts/validate-agent-context.mjs` | Exit 1, `AGENT_CONTEXT_INVALID`: repository baseline has missing DB Admin context/source, 33 orphan `create_dd_screen` resources and broken DB Admin links. Drift mode also reports historical Study Vue paths at the old manifest snapshot and stale source in other scopes. | BASELINE_CONTEXT_INVALID |
| `node scripts/validate-agent-context.mjs --skip-drift` | Exit 1 only for the unrelated DB Admin context/source/links and orphan skill resources; no Study Web registry, required-path, or link errors. | BASELINE_FAIL_OUT_OF_SCOPE |

## HANDOFF

- Remaining blockers: None expected; Study API and deployment contracts remain outside this task.
- Next owner/action: Complete the Angular base scaffold, architecture guide, context updates, then run only the approved build and root-page smoke checks.
