---
task_id: "2026-11-17-implement-study-screens-apis-T030"
date: "2026-11-17"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AD-02 consumes Study Server API #68 GET /api/v1/admin/users"]
status: "DONE_WITH_LIMITATION"
---

# Worklog: T030 — AD-02 honest loading, error, and page recovery

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T011.md`
    - carry_forward: Preserve the broad objective at 20%; keep expected and current behavior separate; choose only a source-backed screen slice.
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T012.md`
    - carry_forward: Do not treat an API catalog or screen artifact as runtime evidence; keep API and browser state explicit.
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T013.md`
    - carry_forward: Do not infer unsupported screen behavior; record source discrepancies and preserve unrelated worktree changes.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Begin coding Study screens. This continuation implements the source-supported AD-02 loading/error recovery slice and keeps progress synchronized to `docs/tasks/process.md`.
- Canonical contract/approved DD: AD-02 DD states distinguish `loading`, `ready`, `empty`, `filter-error` (API #68 422 for `page`), `unauthenticated`, `forbidden`, and service `error`. A 422 should be associated with page state and allow correction/reset; a service error should show safe copy and retry. Empty HTTP 200 must not be presented as sync status. API #68 is read-only and accepts exact-string role/status, keyword, and page; size is fixed at 20.
- Open decisions retained: ADMIN claim as user-management permission; role/status enumerations and labels; PII/lifecycle visibility; live schema/deployment; 401/403 shared auth UX; empty-page representation. No new API behavior or enum mapping is introduced.

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 15% | 15% | Read AD-02 package, both screen images, Stitch plan/markers/HTML, current web route/page/API adapter/spec, API #68 DD/source/tests and relevant scope context; record current discrepancies and execution plan. | DONE |
| 60% | 75% | Implement distinct accessible loading, empty, filter-error (422), and service-error states in AD-02; preserve query filters on page recovery; add focused Angular assertions and pass the focused spec. | DONE |
| 25% | 100% | Pass focused API #68 tests and Study Web build; synchronize AD-02 DD/inventory and process tracker to verified current source; run diff/context checks and attempt local browser verification when safe. Browser attempt is complete; record any authentication/runtime limitation explicitly. | DONE_WITH_LIMITATION |

## CURRENT_BEHAVIOR

- Source/config: `admin.routes.ts` maps `users` to `AD02Page`; `AD02Page` hydrates/updates URL filters and page, calls `AD02ApiService` via `AdminApiService` and API_068, renders safe UserProfile fields, refreshes an empty list, and links row IDs to AD-03. Loading, loaded-empty, retryable service-error, and page-422 recovery now render as separate accessible states; the 422 recovery preserves filters and unrelated query parameters.
- Runnable tests: AD-02 component spec covers unauthenticated access, #68 success/pagination, filters/query restoration, empty, refresh, absence of unsupported claims, loading/error distinction, retry, and 422 recovery. API #68 HTTP tests cover auth-before-query, validation, exact filters, empty response, safe projection, rollback and OpenAPI. Both suites passed in T030.
- Runtime wiring: Local source route and client call are present. Dev server returned HTTP 200 for `/admin/users`; Firefox headless showed the Admin login gate because no authenticated session was available. Authenticated AD-02, live API/database, schema and deployment remain `NOT VERIFIED`.

## SOURCE_TRACE

```text
admin.routes.ts users child → AD02Page → AD02ApiService.getUsers → AdminApiService
→ API_068 descriptor / StudyApiService → GET /api/v1/admin/users
→ get_admin_users_endpoint → shared ADMIN JWT guard → page validation/keyword normalization
→ matching COUNT_ADMIN_USERS + LIST_ADMIN_USERS (read-only legacy users candidate)
→ allowlisted UserProfile + Page envelope → AD02 rows/pagination
→ Angular spec + Study Server API #68 fake-session HTTP tests
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| AD-02 docs say Study Web has no route/client and implementation is blocked as UNWIRED | Current `admin.routes.ts`, `AD02Page`, `AD02ApiService`, `API_068` descriptor and `ad02-page.spec.ts` contain the route/caller/tests; DD, inventory and tracker current-source status were updated. | `RESOLVED` — stale source-status documentation corrected | DD/business blockers and authenticated runtime `NOT VERIFIED` remain. |
| Loading and service errors share no-results row | The original `ad02-page.html` used one no-result branch; current source now has separate loading status, loaded empty, and error alert/retry presentation. | `RESOLVED` — current UI defect fixed | Focused Angular spec verifies state separation and retry. |
| API 422 is mapped only to a generic filter message | API #68 contract/test identifies `fieldErrors[0].field == 'page'`; `adminDataError` now retains HTTP status/retryability and page exposes recovery. | `RESOLVED` — source-backed recovery implemented | Focused Angular spec verifies page=1 recovery preserves filters and unrelated query. |
| Backend policy/schema decisions remain open | API #68 DD is Draft; local query uses legacy users candidate and fallback ADMIN claim. | `BLOCKED` decisions; no live evidence | No backend changes, enum assumptions, or runtime claims. |

## CHANGES

- Files changed:
  - `apps/study-client/src/app/shared/ui/admin-screen.model.ts`
  - `apps/study-client/src/app/features/admin/admin-screen-state.ts`
  - `apps/study-client/src/app/features/admin/AD02/pages/ad02-page.ts`
  - `apps/study-client/src/app/features/admin/AD02/pages/ad02-page.html`
  - `apps/study-client/src/app/features/admin/AD02/pages/ad02-page.css`
  - `apps/study-client/src/app/features/admin/AD02/pages/ad02-page.spec.ts`
  - `apps/study-client/src/styles.css` (state styling moved to global styles to stay within component CSS budget)
  - `apps/study-client/docs/dd_screens/AD-02-DanhSachNguoiDung/00-overview.md` through `07-test-cases.md`
  - `apps/study-client/docs/screen_stitch/05_admin/AD-02_danh-sach-nguoi-dung/AD-02.md`
  - `apps/study-client/docs/list_screen.md`
  - `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`
- CONTEXT_UPDATES: Current source status is synchronized in AD-02 DD/inventory/tracker. No project/scope context page or registry was edited in this T030 continuation; unrelated pre-existing context changes are preserved.
- Assumptions: Page 1 is the only contract-backed recovery for an API #68 invalid-page 422; navigate to it while preserving current filter and unrelated query params.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | READY; T011, T012, T013 selected and read | VERIFIED |
| `npm test -- --include=src/app/features/admin/AD02/pages/ad02-page.spec.ts` | 1 file, 8 tests passed | VERIFIED |
| `uv run pytest -q tests/modules/admin/api_68_admin_users_list/test_admin_users_list.py` | 15 passed; 1 upstream Starlette/httpx deprecation warning; fake DB/session | VERIFIED |
| `npm run build` (Study Web, final CSS placement) | Exit 0; three existing Student CSS budget warnings; no AD-02 warning | VERIFIED |
| `curl -i http://127.0.0.1:4200/admin/users`; Firefox headless screenshot | App served HTTP 200; screenshot showed Admin login gate, no authenticated session; no fixture/DB rows created; server stopped | PARTIAL — authenticated screen/runtime NOT VERIFIED |
| `node scripts/validate-agent-context.mjs` | Exit 1, `AGENT_CONTEXT_INVALID`; 1,431 existing repo-wide findings (DB Admin context/source, broken context links, orphan skill resources, `CONTEXT_STALE`). Filtered output contains no AD-02/T030/process finding. | BASELINE LIMITATION |
| `git diff --check` (T030 scoped paths) | Exit 0; no whitespace errors | VERIFIED |

## HANDOFF

- Remaining blockers: ADMIN permission scope, role/status enum mapping, PII/lifecycle policy, live DB schema/deployment and shared auth UX remain unresolved; authenticated browser/live runtime not verified.
- Next owner/action: Continue with the next source-backed Study screen slice under the broad goal. This bounded AD-02 continuation is complete; open permission/enum/PII/schema and authenticated runtime decisions remain explicit blockers.
