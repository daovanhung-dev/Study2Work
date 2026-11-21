---
task_id: "2026-11-17-implement-study-screens-apis-T016"
date: "2026-11-17"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["web-work (Study Web)", "server-study (API contract/source read-only)"]
cross_scope_dependencies: ["SH-01 Study Web public landing -> Study Server API #05 categories and #06 published courses; search forwards q to GS-02/#07"]
status: "VERIFIED"
---

# Worklog: Continue coding Study Web screens — T016 (SH-01)

## PRIOR_WORKLOG_REVIEW

- `primary_task_type`: `coding`
- `selector_command`: `node scripts/select-worklogs.mjs --type coding --limit 3`
- `selector_result`: `READY`; T011, T012 and T013 were selected and read in full; no shortage.
- `prior_worklogs_reviewed`:
  - `.agents/worklog/2026-11-17/implement-study-screens-apis-T011.md`
    - carry-forward: AD-22/#97 is a bounded read-only slice; API DD/report projection, fine-grained permission and live schema remain unresolved.
  - `.agents/worklog/2026-11-17/implement-study-screens-apis-T012.md`
    - carry-forward: broad goal remains all 83 screens and role-aligned APIs at 20%; Guest GS01–GS03 are source-wired; loaded behavior and live/browser evidence must stay qualified.
  - `.agents/worklog/2026-11-17/implement-study-screens-apis-T013.md`
    - carry-forward: GS04/#09 has current source but API approval, visibility, loading design, eager/lazy, cache and direct-entry gates remain open.
- Additional handoff read: `.agents/worklog/2026-11-17/implement-study-screens-apis-T015.md`; GS04 is now mounted as a GS03-owned curriculum tab. The broad 83-screen objective remains 20% ACTIVE.
- `shortage`: `none`.

## EXPECTED_BEHAVIOR

- Latest user request: start coding the Study Web screens; retain the active all-83-screen/API objective and report continuation progress in `docs/tasks/process.md`.
- Overall objective remains **20% ACTIVE**. T016 is one bounded implementation slice and cannot raise the coarse overall estimate by itself.
- Candidate: **SH-01 public Study landing**, P0, route `/`, APIs #05 and #06. Source-backed independent behavior: public GET categories and published courses in separate regions; trim non-empty search and navigate to `/courses/search?q=...`; links only to inventory routes already declared.
- Preserve known blockers: DD remains `DD BLOCKED`; API #05/#06 DDs are `Draft — Needs Confirmation`; #06 category query currently returns 422; category chips stay informational; course cards do not navigate because SH-01/F02 and inventory destinations disagree; no currency is added to the price; unsupported KPI, ratings, popularity, duration, testimonials, company logos, email collection, accreditation, legal/footer copy and prototype placeholders are excluded.
- Visual target is `.agents/web-study/design.md`; PNG and HTML are discrepant references, not a selected runtime source.

## CURRENT_BEHAVIOR

- Current Angular source before T016: `/` loads `SystemReadinessPage` through `systemRoutes`; `sharedRoutes` registers only `/login` (SH-02) and `/register` (SH-03); there is no SH-01 component or #05/#06 caller.
- `SharedLayout` renders only `RouterOutlet`, so SH-01 can own `/` inside the Shared route group without inheriting duplicate page chrome.
- `StudyApiService` returns `ApiEnvelope<T>` and `STUDY_SERVER_APIS.API_005` / `API_006` are marked `WIRED`.
- Current API source: #05 returns ACTIVE categories with id/name/slug/optional description; #06 returns PUBLISHED courses, supports page/size, rejects any category filter with 422, and maps title/description/thumbnail/decimal-string price/status/mentor. API DDs remain Draft and live DB/deployment are not verified.
- Existing GS01 caller uses page size 20 and shared Guest models. SH-01 will use local screen DTOs and page size 6; it will not import another feature screen or its data-access layer.
- Worktree already contains many dirty files from prior/user work. Preserve all unrelated state; do not stage, reset, clean, or overwrite it.

## STUDY_FE_SCOPE

`Study FE scope: screens=SH-01 Trang giới thiệu Study (/); APIs=#05 GET /api/v1/categories, #06 GET /api/v1/courses?page=1&size=6. Cross-screen routes: GS-01 /courses, GS-02 /courses/search?q=..., SH-02 /login, SH-03 /register. Server scope is read-only API source/contract evidence; no Study Server implementation change is planned.`

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 15% | 15% | Complete selector/context preflight, read all SH-01 DD/Stitch/API evidence and current route/callers, capture discrepancies, and save the pre-edit plan below. | `DONE` |
| 65% | 80% | Implement the independently specified SH-01 public landing slice in the four-folder structure: root route, search navigation, independent #05/#06 loading/ready/empty/error/retry states, and response-backed category/course presentation. Unsupported actions/data remain unavailable. | `DONE` |
| 20% | 100% | Run focused Angular and #05/#06 fake-session tests plus production build; demonstrate root route where available; update current-source DD/context and process tracker, preserving all blockers. | `DONE` |

**Current T016 progress: 100%. Overall objective: 20% ACTIVE.**

## SOURCE_AND_DESIGN_REVIEW

- Mandatory screen/API catalogs read: `apps/study-client/docs/list_screen.md` (SH-01 row 01), `apps/study-client/docs/list_endpoint.md` (#05/#06 rows 5/6), `apps/study-client/docs/dd_screens/screen-index.md` (SH-01 locator).
- Full screen package read: `apps/study-client/docs/dd_screens/SH-01-TrangGioiThieuStudyVariant1/00-overview.md` through `07-test-cases.md`, `images/README.md`, clean and numbered PNGs, source `SH-01.md`, `SH-01_PLAN.md`, `SH-01_markers.json`, and the complete `code.html`.
- Study Server context/source read: `.agents/server-study/AGENTS.md`, API #05 and #06 `02_Overview.md`, `03_Request.md`, `04_Response.md`, route registrations in `app/api/v1.py`, and the current category/course models and views.
- Frontend current source read: `app.routes.ts`, `shared.route.ts`, `SharedLayout`, `system.routes.ts`, `app.routes.spec.ts`, `StudyApiService`, `ApiEnvelope`, API descriptors, GS01 catalog service/models/page, and `package.json`.
- Required visual/architecture guidance read: `.agents/web-work/study/workflows/screen-implementation.md`, `.agents/web-study/frontend-rules.md`, `.agents/web-study/design.md`, `.agents/web-work/study/AGENTS.md` and `INDEX.md`.
- `DISCREPANCY`: DD still describes no Angular source/router, but current source has an Angular SPA, Guest routes GS01–GS03 and Shared SH02/SH03. SH-01 itself is still absent; `/` currently resolves to readiness scaffold.
- `DISCREPANCY`: API #06 catalog/DD permits `category`, but current validator rejects it with 422 because no course-category relation is confirmed. SH-01 must not send `category`.
- `DISCREPANCY`: PNG, HTML and marker/package copy do not establish one approved layout. The HTML has prototype cards, category labels and an empty state at once; it has placeholder fragment links. None of these are copied as runtime data/actions.
- `BLOCKED` decisions retained: full editorial landing design, course-card destination, category filtering, price currency, marketing claims/consent/footer/legal copy and unavailable variant-2.

## PRE_EDIT_PLAN

1. Add `features/shared/SH01/{data-access,models,pages,ui}`. Implement a local `SH01CatalogService` using the existing `StudyApiService` descriptors #05/#06. Define only response fields evidenced by API source; keep each public GET independent and pass `page=1,size=6` only to #06.
2. Implement `SH01Page` with separate category/course state signals and manual per-region retry. Use `Router.navigate` with a trimmed `q` query parameter for non-empty search; keep empty input on `/` without a validation message. Link to existing `/courses`, `/login`, `/register`; use neutral semantic labels and avoid unapproved editorial claims.
3. Add a screen-local course-card UI rendering only server-returned published-course fields. Keep cards non-clickable; keep categories non-interactive. Omit currency-dependent price display and unsupported prototype metadata. Do not collect email or render KPI/testimonial/company/accreditation content.
4. Change `shared.route.ts` so `/` is SH-01 under `SharedLayout`; remove the root readiness route from `app.routes.ts` because `/` is the SH-01 inventory route. Leave the readiness component/source intact and unmounted; do not add an undocumented `/system` route.
5. Update `app.routes.spec.ts` to assert direct `/` entry renders SH-01, no readiness scaffold leaks into `/courses` or `/login`, existing auth routes remain, and search routes with trimmed `q` to GS02.
6. Add `sh01-page.spec.ts` for exact #05/#06 requests, public headers, independent success/empty/error states, isolated retries, category non-interaction, no prototype sample content, and search navigation behavior.
7. Verify with focused Angular specs, Study API #05/#06 fake-session suites, `npm run build`, local route/browser demo if tools are available, and `git diff --check`. No DB fixture is needed; if server is unavailable, record the browser/backend runtime limitation.
8. After implementation, update only SH-01 current-source context/DD/index/inventory, the registered context manifest as needed, this worklog and `docs/tasks/process.md`; run `node scripts/validate-agent-context.mjs` because context pages will change.

## CHANGES

- Added SH01 local API data-access, response models, landing page and course-card UI under the required four-folder structure.
- SH01 loads #05 and #06 independently; #06 sends only `page=1&size=6`; errors and retries stay scoped to their data region.
- Category labels are non-interactive; course cards show only response-backed published course title/optional description/thumbnail/mentor and remain non-clickable. Currency-dependent price display and prototype-only metadata are omitted.
- Search trims `q` and navigates to the existing GS02 route. The GS02 source currently lowercases the query before requesting #07; SH01 does not lowercase it.
- Registered SH01 at `/` in Shared routes and removed the readiness route from the root route list; readiness source remains intact and unmounted.
- Added focused SH01 data/state specs and updated root/search route specs.
- Synchronized the current-source status in Study Web router/index/design context, SH-01 DD overview and source header, screen index, inventory, and context manifest. Registered all nine SH01 source files in the Study Web `requiredSourcePaths` manifest.

## VERIFICATION

- Focused Angular test command: `npm test -- --include=src/app/features/shared/SH01/pages/sh01-page.spec.ts --include=src/app/app.routes.spec.ts` — **13/13 passed**.
- Study Server source-backed fake-session tests from `apps/study-server`: `uv run pytest -q tests/modules/guest/api_05_categories/test_categories.py tests/modules/guest/api_06_courses/test_courses.py` — **29 passed**, with one pre-existing Starlette/httpx deprecation warning.
- Production `npm run build` — **passed**. No SH01 style budget warning; three pre-existing Student CSS budget warnings remain (`student-static-screen.css`, ST22, and Student layout).
- Local browser route: `GET http://127.0.0.1:4200/` returned HTTP 200. Headless Chrome rendered the SH01 route at 1440x1100 and 390x844; both independent data regions showed their designed error/retry state because `GET /api/v1/categories` through the dev proxy returned HTTP 502. This verifies local Angular route/rendering only; live API, DB, populated state and production deployment remain unverified. No database fixtures were created.
- `git diff --check` — passed. `node scripts/validate-agent-context.mjs` remains `AGENT_CONTEXT_INVALID` with 1,431 output lines, matching the known repo-wide baseline; findings concern DB Admin context/source, broken context links, orphan skill resources, and stale context. SH01 manifest paths: 9 registered / 9 present; no new T016/SH01 findings.

## HANDOFF

`VERIFIED for the bounded SH-01 partial source slice. Carry forward DD/API approval, live DB/deployment, category relation/filter, course-detail navigation, price currency, editorial/legal copy and full-screen design gates. The broad all-83-screen/API objective remains 20% ACTIVE.`
