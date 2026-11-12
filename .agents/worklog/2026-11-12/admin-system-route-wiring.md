---
task_id: "2026-11-12-admin-system-route-wiring"
date: "2026-11-12"
primary_task_type: "coding"
secondary_task_types: ["test"]
project_scopes: ["web-work (Study Web)"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Nối route AD-01 và system route

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `READY`; 96 matching logs; selected and read all three.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-12/ad01-screen-coding.md`
    - carry_forward: AD-01 presentation page exists and tests/build passed; keep it placeholder-only; `/admin` had not been wired; repository context validator has unrelated structural errors and drift.
  - path: `.agents/worklog/2026-11-11/study-client-context-load.md`
    - carry_forward: Study Web Angular scaffold has no routes/auth; preserve the root readiness view until a routed replacement is approved.
  - path: `.agents/worklog/2026-11-10/study-web-api-service.md`
    - carry_forward: Generic `/api/v1` transport exists, but no feature endpoint contract should be inferred; keep route task independent of API/server behavior.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Add `features/admin/admin.routes.ts` for AD-01 at `/admin`; route the existing readiness scaffold at `/`; compose both route groups in `app.routes.ts`; keep `/admin` presentation-only and unguarded; do not add API, wildcard, `/forbidden`, or `/not-found` routes.
- Study FE scope: `screens=AD-01 plus root readiness scaffold; APIs=none` (API #101 is outside route-only scope).
- Canonical contract/approved DD: User-approved plan; AD-01 `06-navigation.md` lists `/admin` as candidate/design route and `05-business-rules.md` records API #101/auth blockers. The readiness scaffold is not SH-01.

## MILESTONES

Progress started at 0%. Source/config/DD review reached 30%; route groups/layouts, root shell move, tests/build, browser review, context updates, and required validator run are complete. The validator returned repository-wide baseline errors, recorded separately below. Verified task progress: 100%.

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 30% | 30% | Recheck Study Web worktree, root router, AD-01 route/DD and route/layout/test conventions; preserve pre-existing AD-01 changes | DONE |
| 50% | 80% | Add system/admin layouts and routes; move existing scaffold into the system root page; compose routes; test `/` and `/admin` isolation | DONE |
| 20% | 100% | Run tests/build, preview both routes, review diff, update architecture/worklog, and run context validator | DONE |

## CURRENT_BEHAVIOR

- Source/config: Angular 22 standalone app; `app.config.ts` provides `provideRouter(routes)`. `app.routes.ts` lazy-loads the system route at `/` and Admin routes under `/admin`. App root now contains only `RouterOutlet`; the readiness view and its styles live in a system page. Admin and system route groups have outlet-only layouts.
- Runnable tests: Vitest target exists. Route integration tests and existing AD-01 tests pass 6/6 across two spec files.
- Runtime wiring: `/` renders the readiness page and `/admin` renders AD01Page. No Study Web auth guard or Admin feature API is present. `/admin` is presentation-only and unguarded by user choice.

## SOURCE_TRACE

```text
browser `/` -> App RouterOutlet -> lazy system.routes -> SystemLayout -> SystemReadinessPage -> no external side effect
browser `/admin` -> App RouterOutlet -> lazy admin.routes -> AdminLayout -> AD01Page -> existing presentation-only UI / no API side effect
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| AD-01 route | Catalog/DD candidate `/admin`; source router empty | `UNWIRED` | Register only existing AD-01 page |
| API/auth | API #101 is `DESIGN_ONLY`; client has no guard/token/auth flow; user approved presentation-only routing | `SOURCE_REQUIRED` / `UNWIRED` | Add no API or client guard; route is not access control |
| System route grouping/name | User requested a root system route and exact plural `admin.routes.ts`; canonical guide groups SH screens in `shared` and uses singular `.route.ts` | `DISCREPANCY` | Treat root readiness route as a one-task `features/system` exception; do not move SH-* screens or change global convention |
| Root scaffold | Currently static in root App template; user chose to preserve it at `/` | `VERIFIED` current / route target approved | Move existing content/style into routed readiness page to avoid showing it at `/admin` |

## CHANGES

- Files changed: `apps/study-client/src/app/app.routes.ts`, `app.routes.spec.ts`, `app.html`, `app.css`; `features/admin/admin.routes.ts`; `features/system/system.routes.ts` and readiness page; Admin/System outlet layouts; removed replaced group `.gitkeep` files; `apps/study-client/gui/architech.md`; `.agents/web-work/study/AGENTS.md`, `INDEX.md`, `.agents/context-manifest.json`; this worklog.
- CONTEXT_UPDATES: Updated architecture/source status, Study Web context router/index/manifest and verified source list for the root readiness route and unguarded AD-01 route.
- Context pages changed: `apps/study-client/gui/architech.md`, `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`, `.agents/context-manifest.json`.
- Assumptions: Keep AD-01 UI unchanged; preserve exact readiness copy/style; use minimal layouts containing only `RouterOutlet`; no wildcard/system state routes; do not add auth/API behavior.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Worklog preflight | `READY`; 3/96 exact-type coding worklogs selected and read | VERIFIED |
| Study Web scope/catalog/DD/source read | Screen AD-01 route `/admin`; APIs `none` for this task; router empty; AD01 page exists; root scaffold is static; no client auth guard | VERIFIED_STATIC |
| `npm test` (final after context update) | 2 spec files passed; 6/6 tests passed, including `/` and `/admin` route assertions | VERIFIED |
| `npm run build` (final after context update) | exit 0; production bundle generated separate `admin-routes` and `system-routes` lazy chunks | VERIFIED |
| `git diff --check` | exit 0; no whitespace errors | VERIFIED |
| Chrome headless preview `/` and `/admin` | Reviewed 1440px desktop and 390px mobile screenshots; root shows readiness only; `/admin` shows AD-01 without the root scaffold; content stacks responsively and nav scrolls horizontally | VERIFIED_LOCAL_BROWSER |
| Preview cleanup | `curl` to `127.0.0.1:4211` fails after trapped server shutdown | VERIFIED_STOPPED |
| Context manifest parse and `git diff --check` | Manifest is valid JSON; no whitespace errors | VERIFIED |
| `node scripts/validate-agent-context.mjs` | exit 1; missing db-admin context/source entries, orphan `create_dd_screen` resources, and source drift across multiple scopes including Study Web; no new missing Study Web source paths reported | BASELINE_INVALID |

## HANDOFF

- Remaining blockers: None for route-only presentation wiring; route has no authentication/access control and contains no live data by approved scope. The repository-wide context validator remains invalid due missing db-admin context/source, orphan skill resources, and deep-scope source drift.
- Next owner/action: Follow up on Admin auth/API only after their contracts are verified; resolve repository context baseline separately.
