---
task_id: "2026-11-17-implement-study-screens-apis-T019"
date: "2026-11-17"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["web-work (Study Web)", "server-study"]
cross_scope_dependencies: ["SH-06 route/state view vs Study Server API #08 resource-not-found response; verify whether #08 is a caller or reference only"]
status: "IN_PROGRESS"
---

# Worklog: Continue coding Study Web screens — T019 (SH-06)

## PRIOR_WORKLOG_REVIEW

- `primary_task_type`: `coding`
- `selector_command`: `node scripts/select-worklogs.mjs --type coding --limit 3`
- `selector_result`: `READY`; T011, T012 and T013 selected; no shortage.
- `prior_worklogs_reviewed`:
  - `.agents/worklog/2026-11-17/implement-study-screens-apis-T011.md` — preserve source/DD/runtime distinction, avoid inventing downstream screen behavior, and use focused API tests as source evidence only.
  - `.agents/worklog/2026-11-17/implement-study-screens-apis-T012.md` — broad objective remains all 83 screens and role-aligned APIs; preserve user dirty state and distinguish fake-session tests from live DB/runtime.
  - `.agents/worklog/2026-11-17/implement-study-screens-apis-T013.md` — do not wire UI behavior blocked by API/DD policy; retain ID type and handoff constraints.
  - `.agents/worklog/2026-11-16/implement-study-screens-apis-T004.md` — GS-02 has a bounded #07 implementation, but its full DD remains blocked; avoid repeating its completed slice.
- `shortage`: `none`.

## EXPECTED_BEHAVIOR

- The active broad objective remains Study Server role organization plus implementation of all 83 Study Web screens with verified backend behavior and `docs/tasks/process.md` progress updates. Overall progress remains **20% ACTIVE**.
- T019 implements a bounded SH-06 404 page at the catalog route `/not-found`. A direct route page is in scope; an application-wide wildcard is not established by the DD/source and will remain absent.
- SH-06 expected behavior is a generic 404 view for route/resource-not-found, with no raw URL, course ID, private status, or error-body disclosure. API #08 500/network errors and 403 remain separate.
- The expected UI links target GS-01 `/courses` and SH-01 `/`; both destinations are present in current route source.

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 15% | 15% | Complete coding preflight; read SH-06 DD/Stitch assets, catalog and current frontend/#08 source; record worktree evidence and a bounded pre-edit plan. | `DONE` |
| 65% | 80% | Implement only the explicit SH-06 404 page and route supported by current destinations; keep wildcard, #08 handoff and blocked prototype surfaces unchanged; update DD and wired context pages. | `DONE` |
| 20% | 100% | Complete applicable non-test validation, update final process/worklog evidence, and report remaining verification/gates. Automated tests/build/browser demo are not assumed complete unless actually run. | `DONE` |

**Current T019 progress: 100%. Overall objective: 20% ACTIVE.**

## M0_CANDIDATE

- Selector returned T011/T012/T013 and all were read individually in full. T004 was additionally read because T011/T013 cite it as direct GS-02 predecessor evidence.
- Current catalog row 06: SH-06 `/not-found`, AC-05, API #08, P0. It distinguishes route-level 404 and resource 404 and says not to map 500 to 404.
- DD package is `apps/study-client/docs/dd_screens/SH-06-TrangKhongTonTaiTaiNguyenKhongCon/`; Stitch package is `apps/study-client/docs/screen_stitch/01_shared_auth_system/SH-06_trang-khong-ton-tai-tai-nguyen-khong-con/`. All eight DD sections, source DD, plan, marker JSON, HTML and clean/numbered PNGs were read/reviewed.
- Current source has Shared SH-01 at `/`, SH-02 at `/login`, SH-03 at `/register`; Guest GS-01/02/03 routes at `/courses`, `/courses/search`, `/courses/:courseId`. SH-06 page/route and wildcard are absent before this task. Legacy readiness files remain in source but are unmounted.
- Current GS-03 calls API #08 and keeps a local course not-found state for HTTP 404; its service-error state remains distinct. API #09 curriculum 404 has a separate panel state.
- Existing DD package locator: `apps/study-client/docs/dd_screens/SH-06-TrangKhongTonTaiTaiNguyenKhongCon/`; Stitch source locator: `apps/study-client/docs/screen_stitch/01_shared_auth_system/SH-06_trang-khong-ton-tai-tai-nguyen-khong-con/`.

## M1_SOURCE_TRACE

```text
GS03Page paramMap
  -> GS03CourseDetailService.getCourse(courseId)
  -> StudyApiService API_008 GET /api/v1/courses/{course_id}
  -> Study Server app/api/v1.py route
  -> api_08_courses_detail.validate.validate_course_id
  -> view.find_published_course_detail + FIND_PUBLISHED_COURSE_DETAIL
  -> shared CoursePage/map_course
  -> success DESIGN_RESOURCE_RETRIEVED; invalid/missing/unpublished 404 DESIGN_RESOURCE_NOT_FOUND; query/mapping failure 500 DESIGN_INTERNAL_ERROR
  -> GS03 currently renders inline not-found for 404, service-error for other failures
```

- Source read: `apps/study-client/src/app/app.routes.ts`, `features/shared/shared.route.ts`, `features/guest/guest.route.ts`, GS03 page/template/service/model/spec, `StudyApiService`, API descriptor #08.
- Backend source read: `apps/study-server/app/api/v1.py`, API #08 `view.py`, `validate.py`, `query.py`, `models.py`, and focused test source. Tests were read, not run. The API selects only PUBLISHED and has no 403 response branch.
- SharedLayout is a RouterOutlet only; `StudyIcon` is reusable and already includes brand/arrow icons. Global Study ocean tokens are defined in `src/styles.css`.
- Current Shared/Guest route sources contradict stale SH-06 DD re-audit dated 2026-11-16, which says root is readiness, `/courses` is absent, and GS-03/#08 caller is absent.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| SH-06 explicit page route | No SH-06 feature or `/not-found` route existed before this task; the page and explicit child route are now present in source. | `WIRED; RUNTIME NOT VERIFIED` | Keep route-level UI distinct from a wildcard/static-host fallback. |
| Global route fallback | No wildcard route or source-backed host fallback exists. | `UNWIRED` | Leave unmatched-route dispatch unchanged. |
| Resource #08 handoff | GS-03 caller exists and handles #08 404 inline; SH-06 DD expects a generic state but does not give a current transport. | `DISCREPANCY / NOT WIRED` | Do not change GS-03 in this bounded page-only slice; preserve its current 404 and 500 states. |
| API #08 contract/source | Root API contract is approved design; API DD #08 is Draft; local source/tests are present; deployment/live DB unverified. | `SOURCE_BACKED; RUNTIME NOT VERIFIED` | Keep labels distinct; no backend edit. |
| AC-05 403 branch | AC diagram mentions 404/403; API #08 source/contract has 404/500 and no 403. | `DISCREPANCY` | Do not map a 500 or source 403 to SH-06. |
| SH-06 production surfaces | Recommendation cards, support/contact, footer links/legal/copyright lack approved source/data/routes. | `BLOCKED` | Leave these prototype regions out of this partial implementation; do not use mock data or href placeholders. |
| Stale DD audit | SH-06 2026-11-16 audit incorrectly described the root, Guest routes and GS03/#08 caller as absent. | `RESOLVED IN DD/CONTEXT` | The 2026-11-16 record is labeled historical; 2026-11-17 current-source state is recorded. |
| Overall objective | Tracker and predecessor worklogs keep all-screens/API objective at 20%. | `ACTIVE` | T019 is one bounded slice only. |

## PRE_EDIT_PLAN

1. Add `features/shared/SH06/pages/sh06-page.ts|html|css` and only the required four direct screen folders. Use existing `StudyIcon` and global Study design tokens; no new API/service/model.
2. Add explicit `path: 'not-found'` to `features/shared/shared.route.ts`. Do not add a wildcard or claim static-host fallback.
3. Render a generic 404 heading/description with internal RouterLinks to source-backed `/courses` and `/`. Do not echo route text, course IDs, API body, draft/private status or raw errors.
4. Keep GS03’s current inline #08 404 and separate error state unchanged; keep #09 curriculum 404 unchanged. Resource-to-SH06 handoff remains an open follow-up.
5. Do not implement recommendation cards, support/contact, footer destinations/legal copy, or unverified header actions. Keep the screen explicitly partial while those visible prototype surfaces remain blocked.
6. Update SH-06 current-source DD sections, `apps/study-client/gui/architech.md`, and `.agents/web-work/study/INDEX.md` to state the explicit page route is wired, while wildcard/resource handoff and runtime verification remain outstanding.
7. Do not edit unrelated dirty files. After code/docs, run the required agent-context validator if its page is changed and `git diff --check`; no automated tests/build/browser demo is included in this plan.

## CHANGES

- Added `features/shared/SH06/pages/sh06-page.ts|html|css` and the required four direct screen folders; the page uses the existing Study icon/design tokens, generic 404 copy and source-backed internal links.
- Added explicit `path: 'not-found'` → `SH06Page` to `features/shared/shared.route.ts`; no wildcard or API/service was added.
- Left GS-03's inline #08 404, separate 500/service error and #09 curriculum 404 unchanged; omitted unresolved recommendations, support/contact and footer surfaces.
- Updated SH-06 DD current-source sections, Stitch source/plan audit, `apps/study-client/gui/architech.md`, and `.agents/web-work/study/INDEX.md` to record partial wiring and remaining gates.
- Updated `docs/tasks/process.md` at M0, M1 and M2; this T019 slice is complete at 100%. Broad objective remains 20% ACTIVE.
- `CONTEXT_UPDATES`: Study Web INDEX and architecture summaries now reflect current route/source wiring.

## VERIFICATION

| Command / evidence | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | `READY`; T011–T013 selected; all three read in full. | `VERIFIED_PREFLIGHT` |
| T004 predecessor worklog | Read in full; GS-02/#07 bounded slice and remaining gates reviewed. | `VERIFIED_PRIOR_SLICE` |
| SH-06 DD/Stitch package | All eight DD sections, source DD, plan, marker JSON, HTML, README and both DD images read/reviewed. | `VERIFIED_DESIGN_READ` |
| Current frontend route/caller source | Shared root/SH-01, Guest routes and GS03 #08 caller verified; SH-06 explicit page route and wildcard absent before edit. | `VERIFIED_SOURCE_TRACE` |
| API #08 source/test | Route→validator→query→view→model/response and focused test source read; 404/500 mappings separated; no tests executed. | `VERIFIED_SOURCE_READ` |
| Git/worktree | `develop` branch is 41 commits ahead with extensive pre-existing dirty/untracked work; no T019 source edits existed at baseline. | `VERIFIED_BASELINE` |
| SH-06 implementation/readback | Explicit route/page, internal destinations, no API call, four direct screen folders, and current-source DD/context updates read back. GS-03 and #09 handling remain unchanged. | `VERIFIED_SOURCE_AND_DOC_READBACK` |
| `git diff --check` | Pass after implementation and documentation updates. | `PASS` |
| `node scripts/validate-agent-context.mjs` | `AGENT_CONTEXT_INVALID` (1,078 output lines); repo-wide context findings; no SH-06/SH06/T019-specific finding. | `BASELINE_REPO_WIDE_FAILURE` |
| Tests/build/browser/live service | Not run; this coding slice does not claim compile/runtime verification. | `NOT_RUN` |
| Final tracker/worklog `git diff --check` | Pass after final T019 process/worklog update; output empty. | `PASS` |

## HANDOFF

- Remaining gates: Product/UX surface decisions, AC-05 403 discrepancy, global wildcard/static-host behavior, GS03→SH06 resource handoff, and implementation verification.
- T019 is complete as a source/documentation slice; remaining gates are recommendation/contact/footer decisions, AC-05 403 discrepancy, wildcard/static-host fallback, GS03→SH06 resource handoff, browser/build/test, deployment and live API/DB verification. The broad objective remains 20% ACTIVE.
