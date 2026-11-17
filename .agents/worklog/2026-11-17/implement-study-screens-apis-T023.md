---
task_id: "2026-11-17-implement-study-screens-apis-T023"
date: "2026-11-17"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["Study Web GS-07 /resources/:resourceId -> Study Server API #12 GET /api/v1/resources/{resource_id}"]
status: "DONE_WITH_LIMITATION"
---

# Worklog: T023 — continue coding Study Web screens, GS-07 resource detail

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `READY`; T011, T012 and T013 selected; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T011.md`
    - carry_forward: AD-22/#97 is source-wired but report projection, permissions, live schema and AD-23 handoff remain unresolved; avoid inferring missing API fields or policy.
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T012.md`
    - carry_forward: the broad goal remains role-aligned APIs plus all 83 screens; keep fake-DB tests separate from live runtime evidence and preserve unrelated dirty files.
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T013.md`
    - carry_forward: GS-04/#09 source/contract and presentation gates remain open; recheck current source instead of treating historical screen status as runtime evidence.
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T022.md`
    - carry_forward: GS-06 intentionally makes no #11/#12 call; API #12 currently lacks the AC-06 access/signing behavior per T022 audit; preserve the blocker and verify current source before deciding the GS-07 boundary.
- shortage: `none`
- Additional preflight context read: `.agents/AGENTS.md`, relevant Guest section of `.agents/context-map.md`, `.agents/project/INDEX.md`, `.agents/project/agent-control.md`, registered workflow entry in `.agents/context-manifest.json`, `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`, `.agents/web-work/study/workflows/screen-implementation.md`, `.agents/web-study/frontend-rules.md`, `.agents/web-study/design.md`, `.agents/server-study/AGENTS.md`, `.agents/server-study/INDEX.md`, `.agents/worklog/README.md`, `.agents/worklog/TEMPLATE.md`, and current `docs/tasks/process.md`.

## EXPECTED_BEHAVIOR

- Requirement: continue the active broad objective to organize Study Server APIs by role and implement all 83 Study Web screens; this continuation evaluates and implements the largest independently supported GS-07 slice, while updating `docs/tasks/process.md` at every verified milestone. The overall objective remains 20% ACTIVE until aggregate evidence supports a change.
- Candidate from current catalog: GS-07, “Xem/tải tài nguyên”, `/resources/:resourceId`, API #12. The screen/API package is under M0 review; DD status and exact implementation boundary will be recorded after that review.
- Current contract registry: Study OpenAPI is `NOT_FOUND`; endpoint catalog describes API #12 as public `GET /api/v1/resources/{resource_id}` returning `Resource`. Catalog/DD do not prove source wiring or authorize behavior beyond current source.

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 20% | 20% | M0: complete preflight; inspect both catalogs, full GS-07 DD/Stitch/image package, API #12 DD/source/tests/schema, route/transport/tests and dirty-state baseline; record discrepancies and implementation boundary. | `DONE` |
| 60% | 80% | M1: implement a useful GS-07 page/route slice that is independently specified and source-supported, within the registered four-folder structure, without inventing access policy, fields, URL handling or API behavior; add focused tests. | `DONE` |
| 20% | 100% | M2: run focused applicable FE/API checks and build; demo route and clean up fixtures when safe; synchronize DD/catalog/context, worklog and process tracker; record runtime limits and compare context validator to baseline if context changes. | `DONE` |

**Current T023 progress: 100% (`DONE_WITH_LIMITATION`). Overall objective: 20% ACTIVE.**

## PLAN_V0

1. Revalidate GS-07 route/API inventory against the current source and read the complete screen and API packages before selecting implementation behavior.
2. Keep API #12 source unchanged unless an independently supported requirement and current-source discrepancy justify a minimal fix.
3. Write an execution Plan V1 after M0 and before application source edits. If access or URL policy remains unresolved, implement only a truthful, independently specified gate/presentation state and do not call/open/download the resource.
4. Preserve the existing dirty worktree. Test only the targeted Study Web and API suites relevant to the resulting slice; do not seed an unverified database.

## IMPLEMENTATION_PLAN

Plan V1 — M0 completed; recorded before application-source changes:

1. Create `apps/study-client/src/app/features/guest/GS07/{data-access,models,pages,ui}/`, exactly four direct folders. `data-access/README.md` will state why API #12 is intentionally not called. `models/` will contain only a local `contract-blocked` presentation-state type; no API DTO or guessed resource fields.
2. Add a standalone `GS07Page` using the existing shared `GuestSiteLayout` and `StudyIcon`; add a screen-local availability notice in `ui/`. Render one accessible `role="status"` state with neutral Vietnamese copy. Do not display `resourceId`, metadata, URL, access status, API code, preview, download, zoom/fullscreen, retry, or a return link.
3. Preserve `/courses` guest routing. Export a Guest group route branch from `guest.route.ts` for the inventory's root `/resources/:resourceId` path, using `GuestLayout` and `GS07Page`; compose that group route branch from `app.routes.ts`. The route parameter is not consumed. This is navigation to a local gate only and creates no resource access policy.
4. Keep the existing API #12 descriptor and Study Server source unchanged. GS07 must make no API #12 request because current source returns a direct URL without authorization/visibility/signer and the AC-06 private-resource behavior is unresolved.
5. Extend `app.routes.spec.ts` for direct `/resources/:resourceId` entry and assert the gate renders, root readiness scaffold is absent, the ID is not exposed, and no API #12 request is made. Add a focused GS07 component spec for accessible copy and absence of links/buttons.
6. Synchronize GS-07 package/source notes, `list_screen.md`, Study Web architecture/context/index/manifest, and this tracker to say `SOURCE_WIRED_GATE_ONLY`, with full access/preview/download `DD BLOCKED` and runtime `NOT VERIFIED`. Keep source `screen.png`/HTML and markers unchanged.
7. Verify focused and full Study Web tests, API #12 fake-session suite, production build, local desktop/mobile route demo, fixture/process cleanup, scoped links and diff. Run the context validator and compare it to the M0 baseline; no DB fixture or live API call is permitted for this gate-only route.

### M0 source findings

- Screen catalog row 14: GS-07 is `/resources/:resourceId`, #12, AC-06; inventory expects preview/download when allowed. API catalog row #12 is public `GET /api/v1/resources/{resource_id}`, no Bearer, with `Resource` envelope.
- GS-07 DD 00–07 and original DD/Stitch package distinguish expected AC-06 behavior from the static prototype. Gated presentation is independently specified; ready/403/404/410 simulator tabs and status samples are design-only and conflict with current contract/source. Route, ID hydration, entry/return context, renderer, URL/MIME policy, access policy and runtime are unresolved.
- Clean/numbered DD images were visually reviewed. Image README, PNG copies, full HTML, plan and marker JSON were inspected. Parser confirms 26 sequential unique markers map one-to-one to 26 DD IDs; no duplicate centers/out-of-bounds markers. SVG parser confirms 26 labels/circles/leader lines and embedded source image equality.
- API #12 current route is composed in `apps/study-server/app/api/v1.py` with no Authorization dependency. Its validator parses signed-int64; its query reads `id/lesson_id/name/type/url` and conditionally checks non-DELETED lesson + PUBLISHED course only when `lesson_id` is non-null. `ResourceDetail` omits visibility; `url` may be null/direct. There is no access check, signer or expiry behavior. Current errors are 404/500. Descriptor `API_012` is client-registry `WIRED`, but no client caller exists.
- AC-06 diagram specifies public-or-authorized access, 403 denial and Object Storage signed URL for private resources, which differs from catalog/current API. API DD #12 is Draft; its `DECLARED_NOT_RUNNABLE` label conflicts with local composed route/test source, not production verification. Study OpenAPI is `NOT_FOUND`.
- Legacy `DB.sql` has BIGINT `resources` with nullable `lesson_id`, `url NOT NULL`, and no `visibility`; checked-in V1-PILOT DDL has no `resources` table. Live schema/deployment are unknown. API #12 tests are fake-session tests; current test context records 17 focused tests.
- Current Study Web has no GS07 page/route; `app.routes.spec.ts` already tests `/` and root-only scaffold. `/resources/:resourceId` must be a root path, not a child of `/courses`. Reuse `GuestSiteLayout` and `StudyIcon`; no GS06 child widget can be imported across screen boundaries.
- Current branch: `develop`; before application changes the checkout reports 641 short-status entries and 0 staged paths. Preserve all unrelated pre-existing work.

### Execution boundary

The screen will be wired only as a local contract-gate presentation. It will not invoke #12, show the ID or metadata, open a URL, simulate backend errors, or add a return destination. This advances the screen surface while preserving `DD BLOCKED`, `IMPLEMENTATION PARTIAL`, and `RUNTIME NOT VERIFIED` for the full resource-view/download flow.

## CURRENT_BEHAVIOR

- Current route: `app.routes.ts` mounts a direct `/resources/:resourceId` branch through `guest.route.ts` to GS07. The page renders only the contract-blocked gate; it does not consume or display the route ID, call API #12, or show resource actions. The direct-route and page specs cover the gate.
- API client: `API_012` descriptor is marked `WIRED`; no Study Web source calls it. `StudyApiService` would send the descriptor through `/api/v1` but GS07 will not consume it while access behavior is unresolved.
- Study Server: route #12 is locally composed and calls the source-backed validator/view/query/model. It returns direct URL fields without visibility/access authorization/signer, with 404/500 error branches. Tests use fake DB/session overrides; latest focused context reports 17 tests.
- Runtime/live API/DB/deployment: not verified. Checked-in DDL artifacts disagree and do not establish live schema.

## SOURCE_TRACE

Before T023: no GS-07 route/page/caller and no frontend transport call. After M1: direct route -> GS07 contract-blocked gate -> no API caller. If API #12 is called directly, its route -> `validate_resource_id` -> `get_resource_detail` -> Q1 resource lookup -> optional Q2 published-parent lookup only for non-null lesson ID -> `ResourceDetail{id,name,type,url,lesson_id}` -> 200, 404 `DESIGN_RESOURCE_NOT_FOUND`, or 500 `DESIGN_INTERNAL_ERROR` -> fake-session suite. AC-06 expects an access decision and private-resource signer, which current source does not provide.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Study OpenAPI | `.agents/context-manifest.json` contract entry says `NOT_FOUND`. | `NOT_FOUND` | Use the exact screen/API DD and current source/tests; do not invent a broader contract. |
| API #12 access/URL behavior | AC-06 diagram expects an access decision, 403 and private signer; current route is public/no-auth and returns direct `resources.url`, without visibility/access/signer. | `DISCREPANCY` | Do not wire API #12 or expose/open/download its URL in GS07. |
| API #12 contract/source status | API DD is Draft and includes visibility/signed-URL design; current local source route is composed/tested and has no visibility/signer. API DD says `DECLARED_NOT_RUNNABLE`. | `DISCREPANCY` | Source-backed locally does not prove production runtime; do not promote Draft fields/policy. |
| GS-07 route/runtime | Catalog/DD specify `/resources/:resourceId`; current Study Web mounts the direct route to a contract-blocked gate, with no ID consumption or API #12 call. | `SOURCE-WIRED GATE ONLY / RUNTIME NOT VERIFIED` | The full resource-detail behavior remains blocked; local route/demo verifies only presentation. |
| Resource storage schema | Legacy `DB.sql` has BIGINT `resources`, nullable lesson ID and non-null URL; V1-PILOT has no `resources` table. | `ARTIFACT_DISCREPANCY / LIVE_NOT_VERIFIED` | No live-schema or database-backed demo claim. |
| Prototype behavior | Stitch HTML/API card and simulator claim Bearer/signed URL, 403/410 and preview/download; source is local text-only and conflicts with current API/catalog. | `DESIGN_ONLY / DISCREPANCY` | Do not copy simulator controls, codes or URL behavior into the application. |
| Browser/runtime | No deployed route, authenticated/private resource or live DB has been observed. | `NOT_VERIFIED` | Local route demo verifies only the gate presentation. |

## CHANGES

- Files changed: `app.routes.ts`, Guest group route, GS07 four-folder screen (data-access README, state type, page, unavailable notice and page spec), direct route spec; GS-07 DD current-status notes, screen inventory, Study Web architecture/context/index/page graph/manifest, T023 worklog and tracker.
- CONTEXT_UPDATES: completed after M0/M1/M2 evidence; the registry includes all new GS07 screen files.
- Context pages changed: `apps/study-client/gui/architech.md`, `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`, `.agents/context-map.md`, `.agents/context-manifest.json`.
- Assumptions: none beyond the documented gate boundary; resource access, URL handling and return context remain unresolved rather than inferred.

## VERIFICATION

| Command / evidence | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | Selected T011, T012 and T013; each selected file was read individually in full. | `VERIFIED_PREFLIGHT` |
| `npm test -- --include=src/app/app.routes.spec.ts --include=src/app/features/guest/GS07/pages/gs07-page.spec.ts` (`apps/study-client`) | 2 files passed, 12 tests passed; Angular test build completed. | `VERIFIED_FOCUSED_FE` |
| `npm test` (`apps/study-client`) | 37 test files passed; 157 tests passed. | `VERIFIED_FULL_FE` |
| `npm run build` (`apps/study-client`) | Production build passed. Three existing Student CSS budget warnings (student static screen, student layout, ST22); none from GS07. | `VERIFIED_BUILD_WITH_EXISTING_WARNINGS` |
| `uv run pytest -q tests/modules/guest/api_12_resources_detail/test_resources_detail.py` (`apps/study-server`) | 17 tests passed using fake DB/session overrides; one upstream Starlette/httpx deprecation warning. This is not live DB/API verification. | `VERIFIED_API_12_FAKE_SESSION` |
| Local route/demo | Direct route returned HTTP 200. Firefox headless screenshots at 1440×1000 and 390×844 were visually inspected; gate copy and responsive shell rendered, with no resource ID/action. The route/page specs assert no #12 request. | `VERIFIED_LOCAL_PRESENTATION` |
| Demo cleanup | Angular dev server stopped; port 4200 has no listener; no matching dev-server/Firefox process remains. Temporary Firefox profiles, screenshots and response HTML removed; no DB fixture/rows were created. | `VERIFIED_CLEANUP` |
| `node scripts/validate-agent-context.mjs` | Exit 1 `AGENT_CONTEXT_INVALID`; final output is byte-identical to M0 baseline, 1,431 lines, SHA256 `7496126958d348bb35ec8a7df9ca7228326ba4735b79536b28119e6d26afe9e0`; no new T023 finding. | `BASELINE_IDENTICAL` |
| `git diff --check` | Pass. | `VERIFIED_DIFF_CHECK` |
| M2 acceptance | Full frontend/API checks and build pass; local desktop/mobile gate demo/cleanup complete; DD/catalog/context/process synchronized; API #12 and full resource behavior remain gated. | `DONE_WITH_LIMITATION` |

## HANDOFF

- Remaining blockers: API #12 authorization/visibility/signer contract, GS-07 loaded/error/preview/download behavior, MIME/URL safety and GS-06/ST-12 return context require product/backend/storage decisions. Live schema/API/deployment remain unverified.
- Next owner/action: continue the active 83-screen objective with the next catalog/DD-backed screen and maintain a separate source/runtime evidence record.
