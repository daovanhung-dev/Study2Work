---
task_id: "T021"
date: "2026-11-17"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["Study Web GS-05 consumes Study Server API #10 after existing published-course lookup API #08"]
status: "DONE_WITH_LIMITATION"
---

# Worklog: T021 — coding GS-05 public reviews tab

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T011.md`
    - carry_forward: API #97 Draft/live DB and AD-23 handoff gates remain open; preserve broad objective at 20% and keep work bounded to verified behavior.
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T012.md`
    - carry_forward: Study Web fake-session/API tests and production builds do not verify a live DB/API; existing Guest source and its contract limitations must be rechecked.
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T013.md`
    - carry_forward: Earlier GS-04 wiring status is historical; re-read current route/source before coding, and do not infer readiness from DD status or file presence.
- shortage: `none`
- `Study FE scope: screens=GS-05; APIs=#08,#10`

## EXPECTED_BEHAVIOR

- Requirement: Begin coding Study Web screens. This continuation implements the bounded, source-supported GS-05 public reviews tab within the overall 83-screen objective.
- Screen locator: `apps/study-client/docs/list_screen.md`, GS-05, route `/courses/:courseId?tab=reviews`, AC-05, APIs #08/#10.
- Canonical screen contract: `apps/study-client/docs/dd_screens/GS-05-DanhGiaVaThaoLuanCongKhai/00-overview.md` through `07-test-cases.md`; source Stitch is under `apps/study-client/docs/screen_stitch/02_guest_discovery/GS-05-danh-gia-va-thao-luan-cong-khai/`.
- Canonical API contract: `apps/study-server/docs/dd/10_courses_reviews/`; API #10 remains `Draft — Needs Confirmation`. Its unresolved title, rating filter/aggregate, public visibility and query-validation rules must not be invented or treated as approved.
- Current API #10 route/module/tests exist in source. Where DD and executable source disagree, record `DISCREPANCY` and implement only fields and behavior supported by current source and necessary for this screen.

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 20% | 20% | M0: Recheck selector worklogs, screen/API catalogs, GS-05 DD/Stitch, API #10 DD/source/tests, current GS03 route/tab caller and workflow. Record source trace, discrepancies, scope and implementation plan in this worklog and `docs/tasks/process.md`. | `DONE` |
| 60% | 80% | M1: Implement GS-05 child UI/API client/model and route-tab wiring using only response-backed supported data. Add focused tests for the caller and its states without breaking GS03/curriculum behavior. | `DONE` |
| 20% | 100% | M2: Run focused frontend tests, production build, backend API #10 suite when source remains unchanged, `git diff --check`, browser/runtime check where available, and context validation after context edits. Update screen DD/catalog, `.agents` context, worklog and tracker with verified outcomes and remaining gates. | `DONE` |

## IMPLEMENTATION_PLAN

- Screen folders (exactly four direct children):
  - `apps/study-client/src/app/features/guest/GS05/data-access/gs05-reviews.service.ts`
  - `apps/study-client/src/app/features/guest/GS05/models/gs05-reviews.models.ts`
  - `apps/study-client/src/app/features/guest/GS05/pages/gs05-page.ts`, `.html`, `.css`, `.spec.ts`
  - `apps/study-client/src/app/features/guest/GS05/ui/gs05-reviews-panel.ts`, `.html`, `.css`
- Layout and route: preserve existing guest route/layout; GS03 remains route/query-tab owner. Mount `GS05Page` only in selected reviews tab after #08 yields a published course. No new URL or group route.
- Shared UI search: no existing shared review panel/list; reuse `GuestSiteLayout` from GS03, `StudyIcon`, Ocean design tokens and existing state-card patterns. Keep GS05-only cards/pagination under `GS05/ui/`.
- Data/events: `GS05Page` accepts the existing string `courseId`; on first mount/course change request #10 with `page=1`; previous/next events request only an in-range page. `GS05ReviewsPanel` receives state and emits page change. Map only author name/content/replies and API page metadata. Preserve returned reply order.
- API boundary: mark client descriptor #10 `WIRED` because the exact server route/module/tests are source-backed; GET `/courses/{course_id}/reviews`, public, path ID stays text, page query only. Do not send rating/size, add mutations, or alter Study Server behavior.
- UI states: loading, empty, ready with root/reply cards and bounded pagination, 404 not-found, and safe service-error. No retry/filter/rating/title/aggregate/CTA is added.
- Tests: add GS05 component/API tests for page query, no Authorization, direct selected-tab entry (through GS03 spec), nested author/content rendering, empty, 404, 500, page bounds and next/previous requests. Keep all existing GS03 overview/curriculum tests green.
- Demo/fixtures: build and open the existing GS03 route at desktop/mobile if local browser is available; exercise `?tab=reviews`, pagination, empty and error via HTTP test fixtures. No DB rows are seeded, so there is no database cleanup step. Live API/DB remains unverified.

## CURRENT_BEHAVIOR

- Source/config:
  - Guest route mounts GS03 at `/courses/:courseId`; GS03 now owns overview, curriculum and reviews tabs through `?tab=`. It loads GS05 only when reviews is selected and #08 has returned a published course. String `courseId` is preserved.
  - GS03 calls #09 only for the selected curriculum tab and lazily calls #10 through GS05 for the selected reviews tab. The Study Web descriptor for #10 is now `WIRED`; API #10 server behavior was not changed.
  - GS05 sends only `page` to public `GET /courses/{course_id}/reviews` and maps response-backed root/reply author names and content plus page metadata. The page shows loading, empty, ready, not-found and safe error states with bounded previous/next paging. It does not show title, rating/aggregate, IDs, status or timestamps, and adds no rating filter, mutation, retry or URL page state.
- Runnable tests:
  - Focused GS03+GS05 Angular specs passed 12/12; full Study Web suite passed 153/153 across 35 files.
  - API #10 suite passed 22/22 with fake/overridden DB sessions; this does not verify a live database or deployment.
- Runtime wiring:
  - Production build passed. Desktop and 390×844 mobile routes were rendered and visually checked in local Chrome against a temporary loopback in-memory #08/#10 fixture. This proves local rendering and proxy wiring only, not live API/DB behavior.
  - API #10 DD remains Draft. Title, rating/filter/aggregate, public visibility/query error policy, loaded-state design approval and AC-05 eager-versus-tab-lazy orchestration remain unresolved. Live API/DB and deployment are unverified.

## SOURCE_TRACE

```text
GS03 route/query tab -> #08 published course lookup -> (reviews selected and #08 ready) GS05 page -> StudyApiService #10 -> GET /courses/{course_id}/reviews -> public-course/root/reply queries -> envelope with discussion content/authors and page metadata -> API #10 tests (22 passing, fake DB)
```

GS05 will render only author names, content, nested reply author/content, and current page metadata. It will not render title, rating, aggregate, status, internal IDs, or root timestamps that lack a screen-approved use. It will not add a rating filter or mutation controls. Reply ordering has no source guarantee; client must preserve returned order.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| GS-05 catalog/DD say API #10 has no route/module/test; current server route, module and 22-test suite exist | `apps/study-server/app/api/v1.py`, `app/modules/guest/api_10_courses_reviews/`, focused test; `.agents/server-study/modules/README.md` and `tests.md` | `DISCREPANCY` | Update current-source status after implementation; retain API DD Draft status and approval gates. |
| API #10 DD requires `Discussion.title`, while current source returns `title: null`; DD also describes a rating filter/aggregate ambiguously while source implements neither | API #10 DD request/response/data mapping vs current models/query/view | `DISCREPANCY` | Do not fabricate title, rating, aggregate or filter behavior. |
| AC-05 sequence mentions #08 → #09 → #10 and aggregate rating, while screen inventory/F02 describe lazy review-tab loading and source has no rating aggregate | AC-05 diagram, screen DD/inventory, GS03 current caller and API #10 source | `DISCREPANCY` | Preserve current tab-lazy caller and state that eager orchestration/aggregate remains unresolved. |
| DD public root/reply visibility and malformed optional query semantics remain unapproved; current source filters published course and ACTIVE discussion rows, and maps request exceptions through current 500 path | API #10 DD vs validate/query/view source | `Draft` / `SOURCE_BACKED` | Surface only source-backed not-found/error states; do not alter server behavior without contract support. |
| Loaded reviews/replies/loading/error design is absent from Stitch and numbered prototype; prototype is static and uses remote/CDN assets | GS-05 Stitch, plan, images and `code.html` | `NOT_SPECIFIED` | Use Study Web tokens and common state-card patterns; keep page functional and responsive without claiming visual approval. |
| Repo context validator has a known repo-wide invalid baseline | baseline run: exit 1, `AGENT_CONTEXT_INVALID`, 1,431 output lines, matching T020 tracker note | `BASELINE_INVALID` | Compare after context edits; do not attribute unrelated baseline findings to T021 without evidence. |

## CHANGES

- Files changed:
  - `apps/study-client/src/app/core/constant/api.constants.ts`
  - `apps/study-client/src/app/features/guest/GS03/pages/gs03-page.ts`
  - `apps/study-client/src/app/features/guest/GS03/pages/gs03-page.html`
  - `apps/study-client/src/app/features/guest/GS03/pages/gs03-page.spec.ts`
  - `apps/study-client/src/app/features/guest/GS05/data-access/gs05-reviews.service.ts`
  - `apps/study-client/src/app/features/guest/GS05/models/gs05-reviews.models.ts`
  - `apps/study-client/src/app/features/guest/GS05/pages/gs05-page.ts`, `.html`, `.css`, `.spec.ts`
  - `apps/study-client/src/app/features/guest/GS05/ui/gs05-reviews-panel.ts`, `.html`, `.css`
- Documentation/context updated: `apps/study-client/docs/list_screen.md`; GS-03 and GS-05 DD packages; GS-03/GS-05 Stitch plan status snapshots; `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`; `docs/tasks/process.md`.
- CONTEXT_UPDATES: completed after source wiring. The validator's T021-added finding was fixed by linking the Study Web companion `INDEX.md`; final output matches the pre-edit baseline.
- Context pages changed: `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`.
- Assumptions: GS05 consumes public API #10 only after #08 confirms the course is published; it uses the existing `tab=reviews` query convention. These are implementation choices, not approval of unresolved DD/AC-05 orchestration.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | Selected T011, T012, T013; all three read. | `PASS` |
| `uv run pytest -q tests/modules/guest/api_10_courses_reviews/test_courses_reviews.py` (`apps/study-server`) | 22 passed; fake/overridden DB session only. | `PASS — source baseline` |
| `npm test -- --include=src/app/features/guest/GS03/pages/gs03-page.spec.ts --include=src/app/features/guest/GS05/pages/gs05-page.spec.ts` (`apps/study-client`) | 2 files, 12 tests passed; covers existing GS03, direct review entry after #08, keyboard tab navigation, mapping, paging, empty and API error states. | `PASS` |
| `npm test` (`apps/study-client`) | 35 files, 153 tests passed. | `PASS` |
| `npm run build` (`apps/study-client`) | Production build passed; three existing Student CSS budget warnings remain, and GS03 has no CSS budget warning. | `PASS_WITH_EXISTING_WARNINGS` |
| Local browser route check | Desktop and 390×844 mobile screenshots checked using temporary loopback in-memory #08/#10 fixture; #08/#10 proxy requests returned 200. | `PASS — LOCAL STUB ONLY` |
| `git diff --check` | No whitespace errors. | `PASS` |
| `node scripts/validate-agent-context.mjs` | Exit 1; `AGENT_CONTEXT_INVALID`, 1,431 lines, byte-for-byte same output as captured baseline; no T021-specific finding remains. | `BASELINE_UNCHANGED` |

## HANDOFF

- Remaining blockers: API #10 DD approval; `title`, rating filter/aggregate, public visibility/query error semantics; live DB/deployment; loaded-state visual approval; AC-05 eager-versus-tab-lazy orchestration discrepancy.
- Next owner/action: choose the next screen slice from the active 83-screen objective, re-read its current DD/source and coding worklogs, and keep `docs/tasks/process.md` current. The broad objective remains 20% ACTIVE.
