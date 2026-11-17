---
task_id: "T022"
date: "2026-11-17"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["Study Web GS-06 tab shell -> GS03 query-tab state; API #11/#12 were audited but remain deliberately unwired because cardinality/access contracts conflict with current source"]
status: "DONE_WITH_LIMITATION"
---

# Worklog: T022 — continue coding Study Web screens

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `READY`; 131 available; T011, T012, T013 selected.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T011.md`
    - carry_forward: AD-22/#97 is source-wired but report fields, fine-grained permission, live schema and AD-23/#98 handoff are unresolved; continue only with source-backed behavior.
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T012.md`
    - carry_forward: broad objective is role-aligned APIs plus all 83 screens; API tests use fake DB and browser/API runtime limits must remain explicit; preserve unrelated dirty worktree state.
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T013.md`
    - carry_forward: GS-04/#09 contract/visibility/layout/orchestration gates remain open; verify current source before relying on historical screen status.
- Additional immediate predecessor reviewed: `.agents/worklog/2026-11-17/implement-study-screens-apis-T021.md`; GS-05/#10 is source-wired with response-backed fields while API DD and live runtime remain gated.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Continue implementing the active Study Server API organization and all 83 Study Web screens; plan before operations, read applicable DDs/diagrams, and use only behavior supported by approved contracts or current source.
- Overall objective remains `20% ACTIVE` at T022 start.
- Candidate selected: GS-06 (`/courses/:courseId?tab=resources`), hosted by the existing GS03 course-detail route. The supported implementation boundary is a contract-blocked presentation state only; resource listing/opening is not approved by current API/DD evidence.
- `Study FE scope: screens=GS-06; APIs=#11,#12;` (both API references audited; neither will be called by this slice).

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 20% | 20% | M0: Complete worklog/context preflight; verify GS-06 inventory, full screen/API DD and Stitch package, route/caller/API source/tests/schema, workflow and dirty-state baseline; record exact implementation boundary. | `DONE` |
| 60% | 80% | M1: Implement the largest useful GS-06 screen behavior supported by evidence, with focused UI/API caller tests and no invented API or policy. | `DONE` |
| 20% | 100% | M2: Run applicable frontend/backend verification, build and local route demo where available; synchronize DD/catalog/context/worklog and `docs/tasks/process.md`; compare context validator to baseline when context changes. | `DONE` |

**Current T022 progress: 100%. Overall objective: 20% ACTIVE.**

## IMPLEMENTATION_PLAN

- Plan V0: confirm or replace the GS-06 candidate during M0 before editing application source. Keep the slice within one screen and its directly consumed APIs. Preserve all pre-existing user changes.
- Plan V1 (written after M0, before application-source edits):
  - Screen/group folders: create `apps/study-client/src/app/features/guest/GS06/{data-access,models,pages,ui}/`, exactly the four direct folders required by the registered workflow. `data-access/README.md` will record why no service is wired in this slice; no placeholder API service will be created.
  - Layout/routes: keep GS06 inside the existing GS03 course-detail route and guest layout; add `resources` to the existing `?tab=` state. Do not add a top-level route, guard, fallback, or route policy.
  - Page/UI: add a standalone `GS06Page` child component and a screen-local unavailable panel. Render neutral Vietnamese copy (“Tài nguyên hiện chưa khả dụng” / “Hiện chưa thể hiển thị hoặc mở tài nguyên của khóa học này.”) as an accessible status. Do not present it as an empty collection or a backend error.
  - Events/data flow: selecting the tab changes query state; existing arrow/Home/End keyboard handling includes the fourth tab. No resource request, metadata, links, open/download action, or resource-ID navigation is added.
  - APIs/models: keep API #11 `UNWIRED` in the FE registry; do not change server API #11/#12 or their contracts. Add only a local `contract-blocked` presentation-state type. The current #11 singleton/first-row response is incompatible with a reliable collection UI; #12 direct URL/no-authorization behavior and the missing visibility policy do not satisfy AC-06.
  - Tests: update GS03 focused tests for direct `?tab=resources`, selection, keyboard End, and the absence of #11/#12 requests; add GS06 panel accessibility/copy test. Run focused/full Study Web tests and build, plus existing API #11/#12 fake-DB test suites.
  - Demo/cleanup: run the local Study Web route with a temporary loopback #08 fixture only; demonstrate desktop and mobile layout and verify no #11/#12 request. No database seeding. Stop the app and fixture processes and verify their listeners are gone.
  - Documentation: update GS06's eight DD pages, screen/API inventory and current-source context to distinguish the implemented gated tab from the still-blocked resource list/open flow; register API #11 current-source/test evidence without promoting its Draft contract. Preserve runtime/live DB limitations.

## CURRENT_BEHAVIOR

- GS03 now accepts `overview|curriculum|reviews|resources`, maps `?tab=` and uses one `ViewChildren` tab order for click and keyboard navigation. GS05 is lazily mounted after API #08 confirms a published course. GS06 is mounted only after the same #08 published-course check and renders the `contract-blocked` status; it makes no #11/#12 request. `API_011` remains `UNWIRED`; `API_012` remains `WIRED` for other consumers.
- Study Server API #11 is mounted at public `GET /api/v1/courses/{course_id}/resources`, validates a positive integer ID, rejects a non-published/missing course, queries all linked resource rows ordered by ID, then returns 404 for none or serializes only `rows[0]` into a singleton `ResourceItem{id,name,type,url,lesson_id}`. It performs no visibility/access filtering. Its current tests cover empty 404, singleton success, missing course, DB rollback and validation; no multi-row case exists.
- API #12 returns a direct `resources.url` without authorization, visibility/enrollment or signer checks; parent-course validation is conditional on `lesson_id != NULL`. Its DD remains Draft and conflicts with AC-06 private-resource/403/signed-URL expectations. API #11 DD remains Draft and its mapping rule disallows choosing the first of multiple resources.
- Legacy `infra/postgres/study-server/DB.sql` contains `resources` without `visibility`; V1-PILOT `infra/postgres/02_study_db.sql` contains no resources table. Live schema/deployment is not verified.
- Existing relevant Angular tests cover API #08 sequencing, direct curriculum/reviews query entry and keyboard End to reviews. No GS06 implementation/test existed at T022 start. No live API/DB state is assumed.

## SOURCE_TRACE

```text
GS03 `/courses/:courseId?tab=resources` -> GS06 contract-blocked presentation component -> no resource API call
Potential future path (blocked): API #11 -> DB `lessons/resources` -> singleton-first-row response -> incompatible with a trustworthy resource collection; API #12 -> direct URL without access policy
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #11 source status vs DD cardinality rule | Current route/module/query/model/tests exist. The view queries all rows but returns only `rows[0]`; API #11 DD requires that multi-row cardinality not be collapsed. GS06/source catalogs now distinguish local implementation from its Draft contract. | `DISCREPANCY` | Do not wire API #11 or change server behavior without approved collection contract. |
| API #11 cardinality and empty behavior | Current source is a singleton response and maps an empty DB result to HTTP 404; catalog/DD expect a list use case but do not define collection semantics. | `DISCREPANCY` | Cannot render truthful list or empty state. |
| Resource access policy | AC-06 expects public-or-authorized access, 403 and private signed URL; current API #12 is public/no-auth and returns direct URL with no visibility check/signer. | `DISCREPANCY` | No resource link/open/download flow. |
| Resource persistence | Legacy DDL has `resources`; V1-PILOT DDL does not; live deployment unknown. | `NOT VERIFIED` | No database-backed demo/claim. |
| GS06 current screen | GS03 now has a fourth resources query tab and mounts a contract-blocked status after #08 success; it makes no #11/#12 request and has no list/open action. | `IMPLEMENTED PARTIAL` | Resource listing/opening remains blocked by API cardinality and access policy. |

## CHANGES

- Files changed: GS03 tab component/template/spec; new GS06 page, panel, state model, screen spec, and no-service rationale; GS06 DD/Stitch plan/catalog; API #11 source-status documentation; Study Web and Study Server context; this worklog and T022 process row.
- CONTEXT_UPDATES: GS06 source state and API #11 module/test/route evidence updated; API Draft/cardinality/access blockers preserved.
- Context pages changed: `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`, `.agents/web-study/design.md`, `.agents/server-study/AGENTS.md`, `.agents/server-study/apis/declared-routes.md`, `.agents/server-study/modules/README.md`, `.agents/server-study/tests.md`.
- Assumptions: keep the GS06 route as a query tab inside GS03 because that is the inventory route and GS03 is the verified current owner; do not infer resource access policy from the Guest actor label.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | Selected T011, T012, T013; all three read in full, with T021 read as immediate predecessor. | `VERIFIED_PREFLIGHT` |
| GS06 package/image/source audit | Read DD 00–07, image README, clean/numbered PNG visually, source Stitch HTML/plan/marker JSON and image provenance; numbered DD PNG matches Stitch `screen_annotated.png` (`cmp` exit 0). | `VERIFIED_M0` |
| GS03/API source trace | Read current GS03 route owner/component/template/spec, API registry, API #11 route/view/query/model/test and API #12 module/test/source reports; current-source discrepancies recorded above. | `VERIFIED_M0` |
| M0 implementation gate | Presentation-only resources tab is separable from the unresolved listing/access actions; Execution Plan V1 recorded above before app-source editing. | `M0_DONE` |
| Focused GS03/GS06 Angular specs | `npm test -- --include src/app/features/guest/GS03/pages/gs03-page.spec.ts --include src/app/features/guest/GS06/pages/gs06-page.spec.ts` | `10 passed, 0 failed` |
| M1 acceptance | Direct resources query entry, End-key navigation, accessible unavailable state, and no API #11/#12 requests are covered by current Angular specs. | `M1_DONE` |
| Full Study Web suite | `npm test` | `155 passed, 0 failed` |
| Production frontend build | `npm run build` | `PASS`; three existing Student CSS budget warnings, no GS06 warning |
| Study Server API #11/#12 focused suites | `uv run pytest -q tests/modules/guest/api_11_courses_resources/test_courses_resources.py tests/modules/guest/api_12_resources_detail/test_resources_detail.py` | `24 passed, 0 failed`; one upstream Starlette/httpx deprecation warning; fake DB/session only |
| Local GS06 browser demo | Firefox headless/Selenium direct query-tab route at 1440×1000 and 390×844 | `PASS`; selected tab/status visible, zero resource actions; browser loaded only `/api/v1/courses/42` from a local fixture |
| Demo fixture cleanup | Stopped Angular dev server and loopback #08 fixture; verified listeners/processes on ports 4200/9929 | `PASS`; no listener/process remained; no database rows created |
| Context validator | `node scripts/validate-agent-context.mjs` with stderr captured and compared to M0 baseline | `AGENT_CONTEXT_INVALID`, 1,431 lines, byte-identical to baseline; no new T022 finding |
| Diff whitespace check | `git diff --check` | `PASS` |
| M2 acceptance | Frontend/backend checks, desktop/mobile demo and cleanup complete; DD/catalog/context/process synchronized without API contract promotion. | `M2_DONE` |

## HANDOFF

- Remaining blockers: #11 singleton/first-row mapping vs collection need; no visibility policy; #12 direct URL/no authorization/signer; API #11/#12 DDs remain Draft; V1-PILOT resource schema/live deployment not verified. GS-06 remains partial and resource list/open/download remains unavailable.
- Next owner/action: continue the broad 83-screen objective in a new continuation; GS-07 is the adjacent candidate and must retain #12 access-policy gates.
