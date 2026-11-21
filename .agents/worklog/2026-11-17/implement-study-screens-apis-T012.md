---
task_id: "2026-11-17-implement-study-screens-apis-T012"
date: "2026-11-17"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["web-work (Study Web)", "server-study"]
cross_scope_dependencies: ["Study Web candidate screen -> source-backed Study Server APIs and their contract/tests"]
status: "DONE"
---

# Worklog: Continue Study Web screen implementation — T012

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `READY`; 121 available; 3 selected; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T011.md`
    - carry_forward: T011 completed the bounded AD-22 presentation/source-status slice; #97 report metadata/writer/schema, fine permission, AD-23/#98 handoff and browser runtime remain unresolved. Keep overall goal at 20% ACTIVE and do not start AD-23 by assuming report detail support.
  - path: `.agents/worklog/2026-11-16/implement-study-screens-apis-T004.md`
    - carry_forward: broad goal is role-aligned APIs plus all 83 screens; previous GS-02 work was bounded and did not close all DD blockers. Keep runtime/live DB evidence accurate and preserve unrelated dirty state.
  - path: `.agents/worklog/2026-11-16/implement-study-screens-apis-T005.md`
    - carry_forward: API/body/permission discrepancies must remain explicit; only implement behavior supported by current source/approved DD, with focused verification.
- shortage: `none`
- Additional context read: `.agents/AGENTS.md`, `.agents/context-map.md`, `.agents/project/agent-control.md`, `.agents/worklog/README.md`, `.agents/worklog/TEMPLATE.md`, `.agents/project/INDEX.md`, `.agents/project/{architecture,dependencies,contracts,workflows}.md`, `.agents/web-work/{AGENTS,INDEX}.md`, `.agents/web-work/study/{AGENTS,INDEX}.md`, `.agents/web-study/{design,frontend-rules}.md`, `.agents/web-work/study/workflows/screen-implementation.md`, `.agents/server-study/{AGENTS,INDEX}.md`, and relevant `context-manifest.json` registry entries.
- Current checkout baseline: `develop`; `git status --short | wc -l` reported 606 entries. `apps/study-client/docs/list_screen.md` and `dd_screens/screen-index.md` were already dirty. Preserve all existing changes.

## EXPECTED_BEHAVIOR

- Full active requirement: (1) organize Study Server APIs by `admin`, `student`, `mentor`, `guest`, `shared`; (2) implement all 83 Study Web screen surfaces described by `dd_screens/`, `screen_stitch/`, `list_endpoint.md`, and `list_screen.md`; (3) run backend/API verification while coding, fixing or adding APIs only where DD/BD/source support them; trace conflicts to DD/BD; (4) read relevant Study screen/API/server DD/diagrams; (5) deliver screen logic/UI/UX connected to supported backend behavior; and (6) plan before each operation. This continuation advances the full objective and does not replace it with a one-screen success criterion.
- Overall objective remains **20% ACTIVE** per `docs/tasks/process.md`; no broad percentage increase is claimed at task start.
- Confirmed first coding slice after M0: `GS-01 Danh sách khóa học` at `/courses` plus its navigable read-only `GS-03 Chi tiết khóa học` at `/courses/:courseId`; APIs `#05/#06/#08`. GS-01 is P0. GS-03 is included so course cards do not point to a missing route.
- Confirmed `Study FE scope: screens=GS-01,GS-03; APIs=#05,#06,#08`. This is one bounded start toward the full 83-screen objective, not a replacement for it.
- Canonical contract: Study OpenAPI remains a placeholder. Candidate API #05/#06 behavior must be proven from their DDs and current backend source/tests; catalog alone is not runtime evidence.

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 15% | 15% | Complete current preflight; reconcile all 83 screen and 103 API inventory entries; verify a source-supported next screen/API candidate, worktree baseline and exact DD/source/test paths. | `DONE` |
| 65% | 80% | Read the selected screen's complete DD, image/HTML/plan/marker package and the relevant API DD/source/tests; write a pre-edit plan; implement a behavior-complete, contract-supported screen slice in Study Web layers without inventing unsupported behavior. | `DONE` |
| 20% | 100% | Run applicable focused frontend/backend checks and build; attempt local browser route demo and fixture cleanup when safe; inspect diff/links; update this worklog, `docs/tasks/process.md`, and context pages made stale by changed source; record runtime limits. | `DONE` |

**Current T012 progress: 100%. Overall objective: 20% ACTIVE.**

## IMPLEMENTATION_PLAN

Execution Plan V1 — approved for the bounded source-supported coding slice:

1. Add GS-01 `/courses` as a public catalog. Call #05 for category metadata and #06 for page data; keep category names informational because #06 returns 422 for `category` and the checked-in `courses` DDL has no category relation. Do not add cache policy because its TTL/invalidation is unapproved.
2. Render only #06/#08 response-backed course fields. Omit price until currency/display rules are sourced. Use the existing GS02 `/courses/search?q=` route for search handoff; keep paging and sorting within #06's supported parameters.
3. Add GS-03 `/courses/:courseId` so catalog cards have a real target. Retain the source header/breadcrumb/tab/footer frame and disabled curriculum/review tabs; display #08's singleton `data.items[0]` fields in the active overview as `DERIVED_IMPLEMENTATION`, handle 404/error, and do not call reviews/enrollment or imply curriculum/checkout behavior whose UI/API orchestration is not approved.
4. Keep screens in the four Study Web layers, reuse `StudyApiService`, `StudyIcon`, and existing semantic design tokens, and add focused Angular coverage for requests, state transitions, sorting/paging, navigation, and detail failures.
5. Do not change Study Server APIs: #05/#06/#08 routes and query behavior already exist and have tests. Run focused FE/API checks and the production build in M2; report browser/live DB as unverified unless actually observed.

## CURRENT_BEHAVIOR

- Worktree: branch `develop`, 606 short-status entries at baseline; screen catalog and screen index are pre-existing dirty files. No reset/clean/stage operation is authorized.
- Inventory evidence: screen catalog contains 83 unique screen rows; endpoint catalog contains 103 unique API rows. GS-01 is catalog P0 with `#05/#06`; its catalog gate says category metadata only and category filtering unsupported. This is expected/catalog evidence, not current behavior.
- Baseline Guest frontend had only the GS02 `search` child route. Current T012 adds `/courses` (GS01) and `:courseId` (GS03); the app root `/` remains the separate system route. GS01's header/hero search sends users to existing GS02 `/courses/search?q=`.
- Public #05/#06 routes are registered in `apps/study-server/app/api/v1.py`; #05 returns one `CategoryPage`, and #06 returns paged PUBLISHED courses. #06 validates page/size/sort and rejects `category` before database queries. #08 returns one PUBLISHED course inside `CoursePage.items[0]`, 404 for invalid/missing/unpublished IDs, and safe 500 on query/mapping errors.
- `infra/postgres/study-server/DB.sql` defines `categories` and `courses` separately; `courses` has no category key/relation. Existing API tests cover #05 locale/default/empty/error cases, #06 sort/paging/empty/out-of-range/category rejection/errors, and #08 ID/detail success/not-found/errors.
- Reusable frontend evidence: GS02 uses the same `StudyApiService`/`ApiEnvelope`, `StudyIcon`, response-backed cards, and an existing `/courses/search?q=` handoff.
- Runtime/demo and live DB state are not yet verified.

## SOURCE_TRACE

```text
GS-01 `/courses` -> category data-access #05 -> catalog data-access #06
  -> public guest routes/query/service -> categories and PUBLISHED course projection
  -> response-backed list/sort/paging; card -> GS-03 `:courseId` -> #08 singleton detail
```

Fill exact caller/callee and response evidence after the M0 audit.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| GS-01 loaded-state design | Supplied PNG/HTML shows only an empty catalog; loaded cards, count, sort and pagination are not approved in the DD. | `DERIVED_IMPLEMENTATION` | Implement response-backed controls needed by inventory; record this visual/product decision and avoid adding unsupported fields or API behavior. |
| Frontend route wiring | Baseline route had only `search`; current route adds catalog and detail children. | `SOURCE_WIRED_T012` | Verify route navigation in focused tests; root `/` remains separate. |
| Category filter | #06 runtime validator returns 422 for `category`, and checked-in DDL has no course-category relation. | `VERIFIED_UNSUPPORTED` | Fetch/display #05 category metadata only; do not send category to #06 or imply filtering. |
| Price presentation | #06/#08 expose decimal-string `price` without currency; DD does not establish currency or display rules. | `CẦN_XÁC_NHẬN` | Omit price from these screens. |
| Search/detail/enrollment/reviews | GS02 search and GS03 detail routes now exist; #10 reviews and #15 enrollment status remain unwired/gated. | `MIXED_SOURCE_STATUS` | Search and detail navigation are wired; do not imply enrollment or review actions. |
| Cache policy | GS-01 package suggests cache-first, but TTL/invalidation is not approved and current GS01 caller is absent. | `CẦN_XÁC_NHẬN` | Do not invent a client cache. |
| Study OpenAPI | Project contract registry says Study OpenAPI is placeholder/`NOT_FOUND`. | `NOT_FOUND` | Use the exact API DD and current source/tests; do not invent a broader contract. |

## CHANGES

- Files changed: T012 worklog, T012 row in `docs/tasks/process.md`, Guest route, shared Guest layout/model, GS01/GS03 API services/models/pages/UI, GS03 required empty `models/` and `ui/` placeholders, and focused page specs, plus targeted current-source context/inventory updates.
- CONTEXT_UPDATES: `.agents/web-work/INDEX.md`, `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`, `.agents/context-manifest.json`, and the route-status paragraph in `apps/study-client/docs/list_screen.md` now describe Guest GS-01–GS-03 source wiring and retain design/runtime gates.
- Context pages changed: Guest route and caller paths are now required in the `study-web` context manifest; Guest partial status is explicit, and Mentor/remaining screen gaps remain.
- Assumptions: GS01 loaded states and GS03 loaded overview are `DERIVED_IMPLEMENTATION` from the user-authorized screen objective and source-backed API fields; DD visual/design status remains blocked and runtime remains unverified.

## VERIFICATION

| Command / evidence | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | `READY`; 121 available; T011, T004 and T005 selected and read in full. | `VERIFIED_PREFLIGHT` |
| `git branch --show-current && git status --short \| wc -l` | `develop`; 606 entries. Catalog and screen index already dirty; preserve them. | `VERIFIED_BASELINE` |
| Screen inventory crosswalk | 83/83 unique screen IDs extracted with route/API/priority/gate columns. | `VERIFIED_INVENTORY` |
| Endpoint inventory crosswalk | 103/103 unique API IDs extracted with method/path/auth/response columns. | `VERIFIED_INVENTORY` |
| GS-01 exact catalog row and DD locator | P0 `/courses`, AC-03, #05/#06, category filter unsupported; index points to full GS-01 DD and Stitch source. | `VERIFIED_CANDIDATE_ONLY` |
| GS-01 DD/Stitch package | All 8 DD sections, source markdown, plan, marker JSON/SVG, README, HTML and clean/numbered PNGs reviewed; PNG copies match the source artifacts byte-for-byte. Screenshot contains empty state only; source HTML has no working loaded list and its script references absent DOM IDs. | `VERIFIED_ARTIFACTS_AND_GAP` |
| GS-03 DD/Stitch package | All 8 DD sections, source markdown, plan, markers, HTML, original/rendered/numbered images and README reviewed. Original `screen.png` is near-white; rendered and annotated images show only the static unavailable state. Loaded detail remains undesigned; tabs/review/enrollment orchestration remain gated. | `VERIFIED_ASSETS_AND_GATES` |
| API #05/#06/#08 and DB evidence | Routes, query/view/model/validator code, route descriptors, focused test cases and checked-in DDL inspected. Category relation is absent; no live DB claim made. | `VERIFIED_SOURCE_ONLY` |
| Frontend routes and reusable source | Baseline route had only `search`; T012 adds `/courses` (GS01 #05/#06) and `:courseId` (GS03 #08). GS02 remains `/courses/search` (#07); all use shared API/envelope and Guest chrome patterns. | `VERIFIED_CURRENT_SOURCE` |
| Focused Angular specs | `ng test --watch=false --include=...GS01... --include=...GS03...` built and passed both new spec files, 7/7 tests. | `VERIFIED_FRONTEND_SLICE` |
| Study Server #05/#06/#08 focused suites | `uv run pytest -q tests/modules/guest/api_05_categories/test_categories.py tests/modules/guest/api_06_courses/test_courses.py tests/modules/guest/api_08_courses_detail/test_courses_detail.py` → 38 passed, one upstream Starlette/httpx deprecation warning; fake DB sessions. | `VERIFIED_FAKE_DB_TESTS` |
| Production Angular build | `npm run build` passes; no GS-01/GS-03 CSS budget warnings. Three existing Student CSS budget warnings remain. | `VERIFIED_PRODUCTION_BUILD` |
| Local browser route demo | `ng serve --host 127.0.0.1 --port 4200` built successfully. Firefox headless opened `/courses` at 1440px and 390px and `/courses/12` at 1440px; direct route returned HTTP 200 and the layout rendered. API proxy calls failed with `ECONNREFUSED 127.0.0.1:3003` / HTTP 502, so screenshots remained in loading state; successful data/error state and interactive/keyboard behavior were not verified. CUA had no browser surface. Dev server stopped; no DB fixtures were created. | `DEMO_BLOCKED_API_UNAVAILABLE` |
| Screen folder structure | GS-01/GS-02/GS-03 each have exactly the required `data-access/`, `models/`, `pages/`, and `ui/` direct folders; GS-03 uses placeholders in currently empty `models/` and `ui/`. | `VERIFIED_STRUCTURE` |
| Diff and local source format | Touched source formatted with project Prettier; `git diff --check` passes. Targeted Markdown local-link check found 0 broken links across 6 files. The `study-web` manifest parses and all 258 required source paths exist. A broader scan found 4 pre-existing Markdown hard-break spaces on `list_screen.md:3–6`; they are outside the T012 diff and were preserved. | `VERIFIED_LOCAL_CHECKS` |
| Context validator | `node scripts/validate-agent-context.mjs` still returns `AGENT_CONTEXT_INVALID` with 1,431 output lines and the repository-wide DB Admin, orphan skill and `CONTEXT_STALE` findings recorded by prior worklogs; the new `study-web` required paths are present (0 missing). | `BASELINE_REPO_FINDINGS` |
| Exact source/DD/API/tests/demo | M1 implementation/specs, focused API suites, production build, direct-route browser layout attempt, four-folder structure, diff/link/manifest checks and context update are complete. Loaded API behavior, interactive/keyboard browser behavior and live DB runtime remain unverified because the Study API is not running locally. | `DONE_BOUNDED_SLICE_WITH_RUNTIME_BLOCKER` |

## HANDOFF

- Remaining blockers: DD visual approval for loaded states; live browser/API/database runtime; user identity/enrollment, review contract and category relation remain outside this slice.
- Next owner/action: continue with the next source-supported Study Web screen after coding preflight; the overall 83-screen and role-aligned API objective remains active at 20%.
