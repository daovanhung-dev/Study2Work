---
task_id: "2026-11-12-ad01-screen-coding"
date: "2026-11-12"
primary_task_type: "coding"
secondary_types: ["test"]
project_scopes: ["web-work (Study Web)"]
cross_scope_dependencies: []
status: "PARTIAL"
---

# Worklog: Coding Study Web AD-01

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-11/study-client-context-load.md`
    - carry_forward: Study Web remains an Angular 22 scaffold; preserve unrelated worktree state and verify source before edits.
  - path: `.agents/worklog/2026-11-10/study-web-api-service.md`
    - carry_forward: Only generic HTTP transport is available; do not infer feature API behavior without a verified contract.
  - path: `.agents/worklog/2026-11-09/init-study-angular.md`
    - carry_forward: Angular project setup is present; feature routes and runnable unit-test target must be verified from current config.
- shortage: `none` (95 matching logs available; 3 requested and reviewed)

## EXPECTED_BEHAVIOR

- Requirement: Build AD-01 as a Study Ocean screen, retaining the layout with truthful unavailable states; disable unsupported controls and destinations; do not invent API/data/auth behavior. Keep `/admin` unregistered. Temporarily render at `/` for desktop/mobile browser preview and restore the root scaffold.
- Canonical contract/approved DD: `apps/study-client/docs/dd_screens/AD-01-DashboardQuanTri/00-overview.md` through `07-test-cases.md`; design target `.agents/web-study/design.md`; implementation boundaries `.agents/web-study/frontend-rules.md`.

## MILESTONES

Progress started at 0%. Context/source milestone reached 30%; implementation and runnable test setup reached 75%. Tests, production build, browser preview, root restoration, and diff review completed. Repository context validation was run but is blocked by repository-wide manifest/context inconsistencies, so progress remains 75%.

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 30% | 30% | Recheck AD-01 DD, Study Web source/config, worktree and scope rules; identify unsupported behavior and test setup | DONE |
| 45% | 75% | Implement the component-only Ocean UI and focused tests/test target; keep unsupported data/actions honest and do not add `/admin` or backend behavior | DONE |
| 25% | 100% | Run focused tests and production build; inspect desktop/mobile browser preview; restore root scaffold; review diff and required context validation | BLOCKED |

## CURRENT_BEHAVIOR

- Source/config: `apps/study-client/src/app/app.ts` renders the root shell, `app.routes.ts` is empty, and Angular 22 build/serve targets exist. Global Ocean tokens and Inter/system stack exist in `src/styles.css`. `@angular/build@22.2.6` provides `unit-test`; its installed schema defaults to Vitest.
- Runnable tests: A test target now uses `@angular/build:unit-test`/Vitest with `tsconfig.spec.json`; `npm ls` resolves Vitest 4.1.12 and jsdom 26.1.0. Focused AD-01 tests pass 3/3 on rerun.
- Runtime wiring: AD-01 and `/admin` are not wired. No #101 report-summary API source was found; no feature API call is justified.

## SOURCE_TRACE

```text
App -> RouterOutlet -> empty routes -> no feature call / no external side effect -> no response -> no existing tests
AD-01 page -> presentation-only unavailable states -> no data-access/API dependency
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| AD-01 route and report data | Current router is empty; API #101 DD is draft and server has no #101 source | `UNWIRED` / `DESIGN_ONLY` | Keep route and HTTP integration out of scope |
| Identity, audit, service health, RBAC/compliance claims | DD identifies no verified source for these displayed claims | `SOURCE_REQUIRED` | Render no fabricated values or assertions |
| Test setup | `angular.json` has no test target; no feature specs exist | `DECLARED_NOT_RUNNABLE` | Add Angular/Vitest target and focused specs |
| Visual source | Screenshot uses cobalt/remote font; Study Web guide specifies Ocean and Inter/system | `DISCREPANCY` | Follow canonical Study Web tokens |

## CHANGES

- Files changed: `apps/study-client/src/app/features/admin/AD01/` (page, local header/metric/overview/shortcut/icon UI, specs and required four-folder structure); `apps/study-client/angular.json`, `apps/study-client/tsconfig.spec.json`, `apps/study-client/package.json`, `apps/study-client/package-lock.json`, `apps/study-client/gui/architech.md`, `apps/study-client/README.md`.
- CONTEXT_UPDATES: Updated the architecture page to describe the four-folder screen structure and the AD-01 component-only/unwired state.
- Context pages changed: `apps/study-client/gui/architech.md`; this worklog.
- Assumptions: Use a presentation-only component; preserve four direct feature folders; do not create fake API/data-access behavior. Use the existing root temporarily only for local browser preview and restore it afterward.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `git status --short`; coding worklog selector | Worktree has one pre-existing unrelated untracked worklog; selector returned 3/95 logs | VERIFIED |
| Study Web source/config/DD read | Scaffold, empty router, no test target, AD-01 blocked DD, Ocean tokens | VERIFIED |
| Angular builder / generator dry-run | `@angular/build@22.2.6` includes `unit-test`; Vitest generator needs test target; dry-run wrote no files | VERIFIED |
| `npm install --save-dev vitest@4.1.12 jsdom@26.1.0 --legacy-peer-deps --no-audit --no-fund` | exit 0; 71 packages added, 3 removed | VERIFIED |
| `npm ls @angular/build vitest jsdom --depth=0`; `git diff --check` | Dependencies resolve; no whitespace errors | VERIFIED |
| `npm test` | Bundle compiled; 2/3 tests passed. One negative regex also matched the legitimate section heading “Hoạt động hệ thống gần đây” | PARTIAL; assertion needs narrower target |
| `npm test` (rerun) | Bundle compiled; 1 test file and 3/3 tests passed | VERIFIED |
| `npm test` (after panel split) | Bundle compiled; 1 test file and 3/3 tests passed | VERIFIED |
| `npm test` (after header split) | Bundle compiled; 1 test file and 3/3 tests passed | VERIFIED |
| `npm test` (after Prettier) | Bundle compiled; 1 test file and 3/3 tests passed | VERIFIED |
| `npm test` (after final visual adjustments) | Bundle compiled; 1 test file and 3/3 tests passed | VERIFIED |
| `npm run build` (final, after visual fixes/root restore) | exit 0; production bundle generated without component style warnings/errors | VERIFIED |
| Chrome headless screenshots | 1440×1600 desktop, 390×3000 mobile, 320×1800 narrow view reviewed; corrected top-nav overlap and removed false selected period; CUA browser providers unavailable | VERIFIED via local Chrome |
| Root restore / scope check | `app.ts`, `app.html`, `app.routes.ts` have no diff; localhost server stopped; AD01 has no href/API/route/report endpoint wiring | VERIFIED |
| `git diff --check` | exit 0 | VERIFIED |
| `npm run build` | Application code compiled, but component CSS measured 11.54 kB and exceeded the 8 kB error budget | PARTIAL; reduce component stylesheet before retry |
| `npm run build` (retry) | Component CSS reduced to 10.25 kB but still exceeded the 8 kB error budget | PARTIAL; split screen-local UI component styles |
| `npm run build` (after panel split) | exit 0; page CSS 5.69 kB remains above 4 kB warning budget, below 8 kB error budget | PARTIAL; split header styles to remove warning |
| `npm run build` (after header split) | exit 0; production bundle generated without component style warnings/errors | VERIFIED |
| `node scripts/validate-agent-context.mjs` | exit 1; reports missing db-admin context/source entries, unregistered DD skill resources, broken db-admin links, and source drift across multiple scopes including Study Web | BLOCKED by repository-wide context manifest mismatch |
| `node scripts/validate-agent-context.mjs --skip-drift` | exit 1; structural context/registry errors remain without drift checks | BLOCKED by repository-wide context manifest mismatch |

## HANDOFF

- Remaining blockers: The component is implemented and verified. Backend/API contract, Admin identity and live audit/health sources remain outside this component-only task. The repository-wide context validator cannot pass while its manifest references missing db-admin files and unregistered resources; it also reports source drift across scopes.
- Next owner/action: Resolve the repository context manifest/source drift separately; later wire AD-01 only after data/API/auth contracts are verified.
