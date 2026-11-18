---
task_id: "2026-11-18-fix-st02-profile-dd"
date: "2026-11-18"
primary_task_type: "fix"
secondary_task_types: ["coding", "test"]
project_scopes: ["web-work"]
cross_scope_dependencies: ["Study Server API #04 GET /api/v1/users/me"]
status: "VERIFIED"
---

# Worklog: Align ST-02 profile with DD

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `fix`
- selector_command: `node scripts/select-worklogs.mjs --type fix --limit 3`
- prior_worklogs_reviewed:
  - `.agents/worklog/2026-11-15/fix-st12-st26-visual-match.md` — keep visual changes screen scoped.
  - `.agents/worklog/2026-11-15/fix-st13-playwright-visual-audit.md` — verify a rendered screen after editing.
  - `.agents/worklog/2026-11-01/fix-study-api-null-bind-parameters.md` — preserve API contract and existing dirty files.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Study FE scope: `screens=ST-02; APIs=#04`.
- DD inventory: `GET /api/v1/users/me` with Bearer; display safe avatar/email/role/status; cache profile; edit remains disabled.
- DD source has no authenticated ready-state visual, cache TTL or approved local 401/403 navigation. Existing application routes access failures to SH-05.

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 35% | 35% | Trace DD, #04, auth/session, page and live state | DONE |
| 45% | 80% | Connect avatar with fallback, cache per token, semantic disabled button and focused tests | DONE |
| 20% | 100% | Run focused tests/build and inspect live page | DONE |

## CURRENT_BEHAVIOR

- `/student/profile` is guarded for Student. API #04 is already wired through `StudentAccountProfileService` and Bearer interceptor.
- Live QA student profile displays server name, email, role and status. Its avatar URL is absent, so the fallback icon appears.
- Previously, every visit fetched #04, avatar URL was ignored and edit was a disabled-looking span.

## SOURCE_TRACE

`/student/profile` route → ST-02 page → ST-02 profile service → shared student profile service → API #04 `/users/me` → current user SELECT → safe UserProfile envelope → ST-02 view/tests.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Ready-state design | DD clean PNG lacks body; HTML render is sign-in fallback | DD BLOCKED | Exact signed-in visual cannot be certified. |
| Cache policy | Inventory asks for cache, DD has no TTL/invalidation policy | RESOLVED LOCALLY | Memory cache is scoped to current access token; token change or request error drops cache. |
| 401/403 | DD leaves SH-05 relationship to client policy | EXISTING POLICY | Shared interceptor keeps routing access failures to SH-05. |

## CHANGES

- ST-02 data access: cache successful #04 response per access token; retry after failed request.
- ST-02 UI: show `avatar_url`, icon fallback for null/broken image, native disabled edit button and 44px action targets.
- Added focused service/UI tests. Header/footer and API contract were unchanged.
- CONTEXT_UPDATES: no architecture, endpoint or shared convention changed; this worklog records the implementation.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| `ng test --watch=false --include='src/app/features/student/ST02/**/*.spec.ts'` | 3 files, 6 tests passed | VERIFIED |
| `ng build` | Completed; existing SH-01 CSS budget warning | VERIFIED |
|
g test --watch=false --include='src/app/core/auth/*.spec.ts' | 3 files, 8 tests passed | VERIFIED |
| In-app browser `/student/profile` | QA profile rendered; disabled button exposed as disabled | VERIFIED |
|
ode scripts/validate-agent-context.mjs | Fails on pre-existing missing db-admin/context entries outside ST-02 | BASELINE FAILURE |

## HANDOFF

- Remaining blocker: Product/Design must approve the authenticated ready-state visual and any cache TTL/refresh policy beyond token scope.
- Live QA account has no avatar URL; image URL and error fallback paths are covered by the focused UI test.
