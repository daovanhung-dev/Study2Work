---
task_id: "2026-11-12-ad02-ui-only"
date: "2026-11-12"
primary_task_type: "coding"
secondary_task_types: ["test"]
project_scopes: ["web-work (Study Web)"]
cross_scope_dependencies: []
status: "IN_PROGRESS"
---

# Worklog: Implement AD-02 UI-only

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `READY`; 98 exact-type logs available; 3 selected and read.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-12/ad01-screen-coding.md`
    - carry_forward: AD-01 is a presentation-only Study Web page; keep unverified Admin identity, health, audit and API behavior out of UI claims.
  - path: `.agents/worklog/2026-11-12/admin-system-route-wiring.md`
    - carry_forward: `/` readiness and `/admin` AD-01 are routed; Admin currently has no auth guard or feature API; route is navigation only.
  - path: `.agents/worklog/2026-11-12/web-coding-context-prep.md`
    - carry_forward: Current app source must be rechecked per task; Study Web Angular and Work Web React are separate branches; repository context validator has baseline issues.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Implement the user-approved AD-02 UI-only plan at `/admin/users`. Share the existing Admin header/footer through `AdminLayout`, preserve AD-01's visible appearance, render an honest not-connected empty state, keep search/role/status/pagination controls disabled, hide unsupported Add/Export/help controls and health/RBAC/security/sync/audit claims, and add no API/auth/data behavior.
- Study FE scope: `screens=AD-02; APIs=none` — API #68 is referenced by the design/catalog but explicitly excluded from this UI-only implementation.
- Canonical contract/approved DD: User-approved implementation plan; AD-02 package `00-overview.md`–`07-test-cases.md`; `.agents/web-study/design.md`; `.agents/web-study/frontend-rules.md`; registered `study-web-screen-coding` workflow.

## MILESTONES

Progress started at 0%. Worklog preflight and source/context review are complete (25%). Shared shell, AD-02 route/page, registry and architecture changes are complete (55%, cumulative 80%); verification remains.

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 25% | 25% | Read three exact-type prior worklogs; recheck current Study Web source, catalogs, AD-02 gates and context registry | DONE |
| 55% | 80% | Extract the shared Admin shell, retain AD-01 presentation, add the AD-02 route/page with disabled controls and truthful empty state, update architecture/context | DONE |
| 20% | 100% | Run focused route/page tests and build; review browser preview at narrow/mobile/desktop sizes; inspect diff and run context validator | PARTIAL — tests/build pass; browser navigation unavailable; validator reports source drift |

## CURRENT_BEHAVIOR

- Source/config after implementation: Branch `develop` tracks `origin/develop`; preserve pre-existing untracked `web-coding-context-prep.md`. Study Web is Angular 22 with Vitest configured. `app.routes.ts` still loads `/admin` and `/`; `admin.routes.ts` maps `/admin` to AD01Page and `/admin/users` to AD02Page. `AdminLayout` owns the shared header, route-aware navigation, breadcrumb, footer and outlet. AD-02 has four direct folders and no API/model; data-access/models/ui contain only `.gitkeep` placeholders.
- Runnable tests: `npm test` is configured as `ng test --watch=false`; route tests use `RouterTestingHarness`; AD-01 and AD-02 have component tests. Test suite (10 tests) and build passed; browser viewport/focus/reduced-motion review remains blocked by the browser navigation tool.
- Runtime wiring: `/admin` → AdminLayout → AD01Page; `/admin/users` → AdminLayout → AD02Page. The generic `StudyApiService` has no AD-02 caller. Neither Admin route has an auth guard; they provide UI navigation only.

## SOURCE_TRACE

```text
Before: app.routes.ts -> admin.routes.ts -> AdminLayout.RouterOutlet -> AD01Page (header/footer inside page) -> no API
Current: app.routes.ts -> admin.routes.ts -> AdminLayout (shared shell + RouterOutlet) -> AD01Page at /admin or AD02Page at /admin/users -> no API/DB/external side effect
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| AD-02 DD/API gate | Catalog and AD-02 DD mark implementation blocked; #68 contract/policy/schema questions remain open | `EXPECTED_BEHAVIOR` remains blocked for functional list; this task is UI-only | Do not call #68, invent enum options, render user records, or claim the functional DD is complete. |
| Current route/runtime | Before change source had `/admin` only; after change the admin route group has `/admin` and `/admin/users` | `UNWIRED before; presentation-only route wired after` | No API/auth/data or access-control claim; API #68 and functional DD remain blocked. |
| Existing user changes | Worktree has untracked `.agents/worklog/2026-11-12/web-coding-context-prep.md` | `PRE_EXISTING` | Preserve it unchanged. |

## CHANGES

- Files changed: `src/app/shared/ui/study-icon.*`, `src/app/layouts/admin/admin-layout.*`, `src/app/features/admin/admin.routes.ts`, AD-01 page/template/style, removed AD01Header files and `shared/.gitkeep`, AD-02 four-folder feature (page/spec plus `.gitkeep`s), architecture, screen inventory, Study Web AGENTS/INDEX, context manifest, and this worklog.
- CONTEXT_UPDATES: Architecture, Study Web registry and screen inventory now record `/admin/users` as presentation-only and retain API/auth/DD blockers.
- Context pages changed: `apps/study-client/gui/architech.md`; `.agents/web-work/study/AGENTS.md`; `.agents/web-work/study/INDEX.md`; `.agents/context-manifest.json`; `apps/study-client/docs/list_screen.md`.
- Assumptions: Keep AD-01 content and visible shell appearance; make Overview and Users the only active Admin destinations; retain neutral disabled shell placeholders; AD-02 has no rows or record count, only the response-field table headings and a clear not-connected state; no DB fixtures are needed.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | `READY`; all three selected worklogs were read | VERIFIED_PREFLIGHT |
| Study Web scope, catalogs, AD-02 DD, source and registry | AD-02/#68 gates recorded; current Admin route/layout and test patterns rechecked | VERIFIED_STATIC |
| `npm test` | 3 test files passed; 10 tests passed, including `/`, `/admin`, `/admin/users`, and active navigation | VERIFIED |
| `npm run build` | Angular build passed with no component-style budget warning | VERIFIED |
| `curl -sSI http://127.0.0.1:4200/admin/users` | Development server returned `HTTP/1.1 200 OK` | VERIFIED_HTTP |
| Browser preview / viewport / keyboard / reduced motion | Chrome tab creation succeeds, but documented `goto()` fails before navigation; in-app browser unavailable. No visual viewport/focus/reduced-motion verification completed. | BLOCKED_BY_BROWSER_TOOL |
| Static UI audit / whitespace | AD-02 has no HTTP/API caller, user records or unsupported action/claim strings; `git diff --check` clean. CSS provides 44px controls, responsive breakpoints, visible focus and reduced-motion handling. | VERIFIED_STATIC |
| `node scripts/validate-agent-context.mjs` | Exit 1: `AGENT_CONTEXT_INVALID`; reports `CONTEXT_STALE web-work/study-web` for Git source drift and pre-existing db-admin missing paths. All 42 Study Web `requiredSourcePaths` exist; no missing AD-02 registry paths. | BASELINE_DRIFT |

## HANDOFF

- Remaining blockers: Browser preview/visual viewport, keyboard-focus and reduced-motion checks could not run because the selected Chrome `goto()` API failed before navigation and in-app browser was unavailable. API/auth/schema/PII decisions remain blockers for any later live-data integration. Context validator reports existing source drift and unrelated db-admin paths.
- Next owner/action: Re-run the browser preview checks when a working browser navigation backend is available; keep API #68/DD functional behavior blocked until its decisions are resolved.
