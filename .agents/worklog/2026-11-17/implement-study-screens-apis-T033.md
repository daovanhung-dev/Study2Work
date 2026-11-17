---
task_id: "2026-11-17-implement-study-screens-apis-T033"
date: "2026-11-17"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AD-08 current GET #74 caller -> Study Server API #74; PUT #75 exists locally but has no Study Web caller and remains contract/policy gated"]
status: "DONE_WITH_LIMITATION"
---

# Worklog: Continue Study Web screen implementation — T033

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `READY`; T011, T012, T013 selected and read; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T011.md`
    - carry_forward: Keep source wiring separate from Draft contracts and runtime; do not infer downstream AD-23 report details or API fields.
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T012.md`
    - carry_forward: Preserve the all-83-screen objective and dirty worktree; fake-session tests do not prove live API/DB; implement only supported fields/actions.
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T013.md`
    - carry_forward: Do not invent behavior to bridge DD/UI gates; preserve int64 IDs as strings at client boundaries; distinguish source from runtime.
- shortage: `none`
- Immediate predecessor evidence: T031 completed AD-06 and T032 completed AD-07 styling; the overall 83-screen/API objective remains 20% ACTIVE.

## EXPECTED_BEHAVIOR

- Active broad objective remains role-aligned Study Server API organization and all 83 Study Web screens, with source-supported API integration/checks and relevant DD/BD/UC/diagram review.
- Continue with one independently supported Study Web slice while preserving every unrelated dirty path. Do not raise the overall objective percentage based on a single screen slice.
- Confirmed next screen: `AD-08 Chỉnh sửa khóa học`, current GET #74 caller; PUT #75 is a candidate write API only and must remain disabled because its body/authorization/schema/revalidation are unapproved.

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 10% | 10% | Complete coding worklog preflight, inspect current inventory/routes/DD/API/source/tests and dirty state, choose the next viable screen, and write a source-backed plan. | `DONE` |
| 70% | 80% | Restyle only AD-08's host-scoped stylesheet to the Study design system; improve legibility, focus, targets and reflow while preserving all current screen and API behavior. | `DONE` |
| 20% | 100% | Run relevant focused checks/build, inspect scoped diff/links/context, synchronize supported status notes, and update this worklog plus `docs/tasks/process.md` with limitations. | `DONE_WITH_LIMITATION` |

**Current T033 progress: 100%. Overall objective: 20% ACTIVE.**

## CURRENT_BEHAVIOR

- `admin.routes.ts` declares `/admin/courses/:courseId/edit` -> `AD08Page`. The page preserves route ID as string and calls `AD08ApiService.getCourse` -> `AdminApiService` GET #74; loading/loaded/error states exist. Page-local title/description/price edits change only a component-memory draft; mentor/status/ID are read-only; no PUT #75 caller exists.
- `angular.json` registers `AD08/pages/ad08-page.css` as a global stylesheet, but selectors are prefixed with `study-ad08-page`. Current stylesheet has 11,817 bytes, numerous hardcoded colors, several 9–12px text styles, 42px links/buttons and a low-contrast literal focus color.
- API #74 is a read-only source path returning Course detail; API #75 local source parses a candidate body, runs UPDATE on four metadata fields + `updated_at`, then SELECTs/maps a Course projection and commits. API #75 side effects are not used by this Angular page.
- API #75 catalog/AC omit body; its DD remains Draft. Body/full-replacement/null semantics, course-management permission, legacy-vs-pilot schema, thumbnail upload, response cardinality and client response/revalidation remain open. Keep Save/upload disabled and do not add a PUT caller.
- Worktree before T033 source edits: five pre-existing dirty files in AD-08 HTML/spec/TS and API #75 models/view. The dirty changes correct route-ID precision and shared mapper imports; preserve them.
- Authenticated browser/runtime and live API/DB remain unverified; FakeSession API tests are not live schema evidence.

## SOURCE_TRACE

`admin.routes.ts` -> `AD08Page` -> `AD08ApiService.getCourse(string)` -> `AdminApiService`/Admin session -> Study API_074 -> #74 route/ADMIN guard/int64 parser/view/query/shared Course mapper -> singleton `Page<Course>` -> AD-08 local draft + read-only context. API #75 route -> strict candidate body/ADMIN validation -> metadata UPDATE + #74 projection SELECT + commit exists on the server, but no Angular caller; do not call it while its contract gates remain open. Existing Angular AD08 spec asserts exact large route-ID string, only GET #74, draft-only edits, disabled write/upload controls, errors and return link.

## DISCREPANCIES_AND_STATUSES

`DISCREPANCY`: AC-32 says an Admin needs course-management permission, while local #75 only checks shared role `ADMIN`; catalog/AC omit #75 request body but local source requires four candidate fields. Both remain gates; no write flow will be added. Prototype static course-code/mentor selector/counters/readiness/diagnostics are not current source behavior. Browser/live schema remain `NOT_VERIFIED`.

## IMPLEMENTATION_PLAN

1. Edit only `apps/study-client/src/app/features/admin/AD08/pages/ad08-page.css`; keep all selectors host-scoped. Use semantic Study tokens, a centered ~1120px layout, desktop/tablet/mobile reflow at existing design breakpoints, readable body/help text, visible `:focus-visible`, and >=44px interactive targets.
2. Replace the legacy gradient-like pale blue hero, dense small typography and hardcoded hues with restrained surface/background/accent tokens; avoid heavy shadows and added animation. Preserve the page structure, local draft, API #74 loading/error, direct route ID text, back links, and disabled Save/upload controls.
3. Do not modify the five pre-existing dirty HTML/spec/TS/API files, global/shared design sheets, route, or API #75 caller. DD/API status is already current; synchronize no other docs unless this slice reveals factual drift.
4. Run the existing focused Angular AD08 spec, source-backed #74 and #75 FakeSession suites, and Study Web production build. Inspect final scoped diff, links and whitespace; report authenticated browser/live DB limitations.

## CHANGES

- Files changed so far: `apps/study-client/src/app/features/admin/AD08/pages/ad08-page.css`; T033 worklog; T033 row in `docs/tasks/process.md`. The five pre-existing dirty AD-08/#75 HTML/spec/TS/model/view files remain untouched.
- Context pages changed: None.
- Assumptions: AD-08/#75 is only a provisional candidate; an unresolved mutation/policy gate may require selecting another screen.

## VERIFICATION

| Command / evidence | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | READY; T011, T012, T013 selected and reviewed; no shortage. | `VERIFIED_PREFLIGHT` |
| Candidate source/DD/API audit | Read 8 AD-08 DD pages; Stitch source/plan/HTML/image and 61 markers; current Angular route/page/service/spec; API #74/#75 source/route/tests; API #75 Open Questions/DD; AC-32 diagram; Study design/frontend rules; scope context and manifest. | `VERIFIED_M0` |
| AD-08 presentation styling | Replaced the host-scoped legacy palette with Study semantic tokens; content width ~1120px; improved type scale, focus contrast, breadcrumb/footer/back/button target heights and tablet/mobile reflow. No markup, route, API or shared layout change. | `IMPLEMENTED` |
| `npm run test -- --include=src/app/features/admin/AD08/pages/ad08-page.spec.ts` | 1 file, 4 tests passed. | `PASS` |
| `.venv/bin/pytest tests/modules/admin/api_74_admin_course_detail/test_admin_course_detail.py -q` | 15 passed; one upstream Starlette/httpx deprecation warning; FakeSession only. | `PASS_FAKE_SESSION` |
| `.venv/bin/pytest tests/modules/admin/api_75_admin_course_update/test_admin_course_update.py -q` | 27 passed; one upstream Starlette/httpx deprecation warning; FakeSession only. | `PASS_FAKE_SESSION` |
| `npm run build` | Pass; 3 pre-existing Student CSS budget warnings; no AD-08 warning. | `PASS_WITH_BASELINE_WARNINGS` |
| Local route/browser attempt | `ng serve` on 127.0.0.1:4201; `/admin/courses/11/edit` returned HTTP 200. Firefox headless screenshot showed the Admin login gate because no session was available; AD-08 loaded state/API was not verified. Shared Chrome and IAB providers were unavailable. Dev server stopped; temporary profile/screenshot removed; no backend/DB started. | `ROUTE_SPA_ONLY; AUTH_RUNTIME_NOT_VERIFIED` |
| Final CSS format/whitespace/token/link scan | Prettier check passed; scoped `git diff --check` passed; 23 local links resolve; 0 literal hex colors in AD-08 CSS. Worktree confirms only AD-08 CSS was added by T033; five pre-existing dirty AD-08/#75 files remain untouched. Current DD status already matched source, so no screen/API DD edits were needed. | `PASS` |

## HANDOFF

- Remaining blockers: API #75 body, permission, schema, upload and response/revalidation gates; authenticated AD-08 loaded state, live API/DB and deployment remain unverified.
- Next action: Continue the 83-screen objective by selecting the next source-supported Study Web screen with a fresh worklog preflight.
