---
task_id: "2026-11-17-implement-study-screens-apis-T032"
date: "2026-11-17"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AD-07 Study Web detail -> Study Server API #74 GET /api/v1/admin/courses/{course_id}"]
status: "DONE_WITH_LIMITATION"
---

# Worklog: Continue Study Web screen implementation — T032 AD-07

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `READY`; T011, T012, T013 selected and read; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T011.md`
    - carry_forward: Keep current route/source wiring distinct from report/API permission, schema and browser-runtime gates; do not infer downstream AD-23 behavior.
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T012.md`
    - carry_forward: Preserve the complete 83-screen objective and dirty worktree; source-backed fake-session tests do not establish live DB/runtime; keep only supported fields/actions.
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T013.md`
    - carry_forward: Do not invent screen behavior to bridge DD/UI gates; preserve int64 IDs as strings at client route boundaries; distinguish source from runtime.
- shortage: `none`
- Additional context: T031 completed AD-06 at 100%; overall objective remains 20% ACTIVE. T032 reuses the already loaded Study Web/Study Server workflows but will recheck current source and the mandatory context map before deep implementation work.

## EXPECTED_BEHAVIOR

- Full active objective remains: organize Study Server API modules by role; implement all 83 Study Web screen surfaces; run relevant API checks and add/fix APIs only when DD/BD/source supports them; read relevant DD/BD/UC/diagram sources; deliver supported UI/UX integrated with the backend; plan before each operation.
- Overall objective remains **20% ACTIVE**.
- Provisional screen: `AD-07 Chi tiết khóa học quản trị`, `/admin/courses/:courseId`, P1, API #74. M0 may retain or replace this candidate after the source/contract audit.
- Do not assume fields, status actions, curriculum behavior, permission mapping, cache, or navigation persistence from the Stitch prototype. Preserve course IDs as strings at the route boundary and verify current source/API #74 first.

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 10% | 10% | Complete preflight, full AD-07 DD/Stitch/catalog/API/source/test and dirty-state audit; write a source-backed plan. | `DONE` |
| 70% | 80% | Restyle AD-07 in its component CSS to match Study tokens, responsive width, keyboard focus and target-size rules; preserve the current API/data behavior. | `DONE` |
| 20% | 100% | Run focused FE/API checks and build, inspect diff/links/context, synchronize only supported DD/inventory status if needed, and update worklog/process progress. | `DONE_WITH_LIMITATION` |

**Current T032 progress: 100%. Overall objective: 20% ACTIVE.**

## CURRENT_BEHAVIOR

- Current source confirms `/admin/courses/:courseId` -> `AD07Page` -> `AD07ApiService` -> `AdminApiService` -> Study API #74; the detail route is read-only and displays the route ID as text.
- API #74 authenticates ADMIN before path parsing/query, parses positive int64 IDs, selects only course metadata and mentor, maps a singleton `CoursePage`, and has 401/403/404/500 responses. It does not return curriculum, counters or course code.
- `angular.json` globally registers `admin-detail-page.css`; its legacy gradient and hardcoded colors affect AD-07 and AD-13. AD-07 has a component stylesheet, so local overrides can scope the visual update without touching AD-13/shared styles.
- AD-07 currently presents the source limitations honestly; retain all existing loading/error/content/actions behavior. The only independent supported improvement is page-local visual/accessibility styling against `.agents/web-study/design.md`.
- Runtime, live API/DB and authenticated browser rendering remain unverified. API test source uses `FakeSession`, so its evidence is not live DB behavior.

## SOURCE_TRACE

```text
admin.routes.ts (`courses/:courseId`) -> AD07Page/adminRouteState ->
AD07ApiService -> AdminApiService/Admin session -> StudyApiService API_074 ->
Study Server #74 route -> ADMIN guard + int64 validator -> parameterized detail
query -> shared Course mapper + singleton CoursePage -> AD-07 metadata UI
```

## DISCREPANCIES_AND_STATUSES

`DISCREPANCY`: global detail stylesheet still uses legacy gradient/hardcoded colors while the Study Web design target requires semantic tokens and restrained surfaces. Resolve locally in AD-07 CSS; do not change shared rules also used by AD-13. API #74 Draft/permission/schema gates remain separate from source-wired read-only display. Keep expected design, current source and runnable test evidence separate.

## IMPLEMENTATION_PLAN

1. Override AD-07 visual rules in `ad07-page.css` only: semantic tokens, 1120px content width, calm surfaces, readable labels/body copy, visible `:focus-visible`, and 44px links/actions; preserve responsive reflow and reduced motion.
2. Do not change HTML/TS, routes, API callers, shared AD-13 CSS, or unsupported data/actions.
3. After the CSS edit, run the existing focused AD-07 Angular spec, API #74 FakeSession suite, and Study Web production build; inspect only T032's diff plus relevant DD/inventory status and link/whitespace state. Report runtime limits accurately.

## CHANGES

- Files changed in this slice: `apps/study-client/src/app/features/admin/AD07/pages/ad07-page.css`; T032 worklog; `docs/tasks/process.md` progress row. Pre-existing dirty AD07 TS/shared spec remain untouched.
- Context pages changed: None.
- Assumptions: Styling-only AD-07 refinement is independently implementable; API #74's documented gates do not block the existing read-only fields.

## VERIFICATION

| Command / evidence | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | READY; T011, T012, T013 selected and read. | `VERIFIED_PREFLIGHT` |
| AD-07 source/API audit | Caller and current UI inspected; API #74 view/query/tests read; global stylesheet registration confirmed in `angular.json`; Study design rules read. | `VERIFIED_SOURCE_AUDIT` |
| `npm run test -- --include=src/app/features/admin/admin-detail-pages.spec.ts` | 1 file, 2 tests passed. | `PASS` |
| `.venv/bin/pytest tests/modules/admin/api_74_admin_course_detail/test_admin_course_detail.py -q` | 15 passed; one Starlette/httpx deprecation warning; `FakeSession` only. | `PASS_FAKE_SESSION` |
| `npm run build` | Pass. Final build has only the three existing Student CSS budget warnings; AD-07 warning from the first build was removed by reducing the component stylesheet below 4 KiB. | `PASS_WITH_BASELINE_WARNINGS` |
| AD-07 local visual implementation | Component stylesheet now uses Study semantic colors, responsive gutters/layout, visible keyboard focus and 44px+ controls; reduced-motion handling is unnecessary because no animation is added. No template/API/shared stylesheet changes. | `IMPLEMENTED` |
| Final scoped diff and whitespace | Only the AD-07 component CSS was added in this slice; `git diff --check` passed. Pre-existing dirty `ad07-page.ts` and shared `admin-detail-pages.spec.ts` were not touched. | `PASS` |
| Relative links and CSS token scan | 22 relative links in process/worklog resolve; AD-07 CSS is 4,078 bytes and contains no literal hex colors. | `PASS` |

## HANDOFF

- Remaining blockers: authenticated browser/runtime and live API/DB are unverified; API permission/schema/write-flow gates for downstream actions remain outside this styling slice.
- Next action: Select the next Study Web screen from current route/API/DD evidence under a new preflight/worklog.
