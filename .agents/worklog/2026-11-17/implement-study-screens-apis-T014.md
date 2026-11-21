---
task_id: "2026-11-17-implement-study-screens-apis-T014"
date: "2026-11-17"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["web-work (Study Web)", "server-study"]
cross_scope_dependencies: ["GS-04 curriculum presentation -> Study Server API #09 source contract and fake-session tests"]
status: "VERIFIED"
---

# Worklog: Begin coding Study Web screens — GS-04 curriculum page (T014)

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `READY`; T011, T012 and T013 were selected and read in full; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T011.md`
    - carry_forward: AD-22/#97 is a source-backed read-only slice; report projection, permission and live schema remain unresolved.
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T012.md`
    - carry_forward: GS-01–GS-03 are source-wired; keep catalog/design expectation separate from current client runtime and preserve all dirty worktree changes.
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T013.md`
    - carry_forward: GS-04 DTO/service already exists; #09 source returns published lesson `content`/`video_url`; API DD, loaded list/access design, cache and eager/lazy behavior remain unresolved; overall objective is 20% ACTIVE.
- shortage: `none`
- Study FE scope: `screens=GS-04 curriculum page; APIs=#09`
- Additional context/workflow read: `.agents/web-work/study/workflows/screen-implementation.md`, `.agents/web-study/frontend-rules.md`, `.agents/worklog/README.md`, `.agents/worklog/TEMPLATE.md`, `.agents/context-map.md` registry entry for `study-web-screen-coding`.
- Worktree is shared and broadly dirty. Do not clean, reset or stage unrelated changes. In particular, preserve all existing changes under GS03, guest routes, `apps/study-server/app/api/v1.py`, and API #09 validator.

## EXPECTED_BEHAVIOR

- Latest user requirement: begin coding the Study Web screens as part of the active objective to implement all 83 screens and source-backed backend/API interactions.
- GS-04 expected purpose from `list_screen.md`/DD: show public lesson titles in server order; distinguish a truly empty API response from an error; do not open private lessons or create Guest lesson/media access.
- Canonical API #09 current source: `GET /api/v1/courses/{course_id}/curriculum`; response envelope has `data.items` and pagination. The server model includes `id`, `course_id`, `title`, `content`, `video_url`, `order`, `status`; source currently filters PUBLISHED courses and lessons, orders by `sort_order,id`, and returns 404/500 as documented in `SOURCE_TRACE`.
- GS-04 DD is explicitly `DD BLOCKED / IMPLEMENTATION BLOCKED / RUNTIME NOT VERIFIED`. Static HTML provides the empty-card copy only; loaded list visual/access policy is absent. F02 says lazy-on-tab while AC-05 says eager; cache and direct-entry orchestration are unresolved.
- Plan resolves only independently implementable UI/data presentation: a standalone GS04 page receives `courseId`, calls the already-existing #09 service, projects only `title` and `order`, distinguishes loading/empty/ready/404/error, and has no lesson-open/media action. Ready rows and generic loading/error/not-found copy are `DERIVED_IMPLEMENTATION`, not approved DD. Keep the page unregistered and GS03's curriculum tab disabled because current Angular structure has no approved query-tab page composition and frontend rules prohibit direct screen-to-screen imports. Do not add an alternate URL or change #09 behavior.

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 15% | 15% | Complete exact-type worklog preflight, recheck GS-04/API #09 source and workflow, record the supported implementation boundary and plan before code. | `DONE` |
| 65% | 80% | Implement the GS04 standalone page and presentational lesson-list UI using existing four-folder structure and source-backed #09 service, with focused tests for loading, success, empty and errors; keep route composition gated. | `DONE` |
| 20% | 100% | Run focused Angular/API tests and Study Web build, inspect diff/context, update current-source docs and `docs/tasks/process.md`, and record the route/runtime limitation. | `DONE` |

**Current T014 progress: 100%. Overall objective: 20% ACTIVE.**

## CURRENT_BEHAVIOR

- Source/config: `app.routes.ts` loads `guestRoutes` under `/courses`; `guest.route.ts` declares GS01, GS02 and GS03 only. GS03 calls #08, renders an overview and keeps curriculum/reviews tabs disabled. GS04 now has `GS04Page`, which calls #09 through `GS04CurriculumService`, plus a title/order-only child list; no query-tab route host exists.
- API #09: `apps/study-server/app/api/v1.py` registers the public GET route. Validator accepts signed-int64 IDs and maps malformed/out-of-range IDs to 404. View checks a PUBLISHED course, reads PUBLISHED lesson rows, maps `LessonPage`, and returns a safe 500 for database/mapping failures. It has no write or external side effect.
- Runnable tests: `apps/study-server/tests/modules/guest/api_09_courses_curriculum/test_courses_curriculum.py` contains 11 fake-session/TestClient tests. These do not prove live schema or deployed runtime.
- Runtime wiring: the page-to-service caller exists and is covered by Angular tests, but no GS04 route/tab host exists. Browser and live API/database evidence is unavailable in this slice.

## SOURCE_TRACE

```text
future GS04 host -> GS04Page(courseId input) -> GS04CurriculumService
  -> StudyApiService -> API_009 GET /api/v1/courses/{course_id}/curriculum
  -> validate signed-int64 -> query PUBLISHED course -> query PUBLISHED lessons
  -> LessonPage {items,pagination} -> projection {title,order} -> static list UI
  -> #09 fake-session/TestClient tests (11 cases; live DB/deployment unverified)
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Loaded curriculum visual/access design | DD element map says no lesson rows/order labels and marks loaded list/access design missing; API response includes `content` and `video_url`. | `DD BLOCKED / DERIVED_IMPLEMENTATION` | Minimal title/order list is for progress only; hide content/media and provide no lesson action; require DD/product approval for final UI. |
| Eager/lazy orchestration | F02 says lazy on tab; AC-05 says eager; inventory mentions #08 cache then #09. | `DISCREPANCY` | This standalone slice does not choose or implement tab orchestration. |
| Screen composition | GS-04 proposed route is a query tab on GS-03; route table currently only registers GS03, and frontend rule prohibits direct screen-to-screen imports. | `UNWIRED / DESIGN_GAP` | Do not register an invented path or import GS04 into GS03; keep GS03 tab disabled pending approved composition boundary. |
| Public visibility policy and live schema | API #09 DD is Draft and marks PUBLISHED visibility as assumption; live DB schema is unverified. | `SOURCE_BACKED_LOCALLY / NOT_VERIFIED` | Display only the metadata response supplied by current API source; do not claim deployment or policy approval. |

## IMPLEMENTATION_PLAN

1. Keep screen layout at `features/guest/GS04/` with exactly `data-access/`, `models/`, `pages/`, `ui/` direct folders; reuse T013 service/model, `StudyApiService`, `StudyIcon`, and semantic design tokens.
2. Add `GS04Page` in `pages/`; accept host-provided `courseId` as a string input. The page owns request state and calls only the GS04 data-access service.
3. Add a presentational `GS04LessonList` in `ui/`; it receives title/order projections only and has no router, API, or click behavior. Preserve server-returned order.
4. Add focused Angular tests for #09 GET path/no Authorization, initial loading, empty response, ready title/order projection (assert content/video are absent), 404 and safe 500/business-code error handling.
5. Do not change `guest.route.ts`, GS03 page, or server source in this slice because route composition and orchestration are unresolved. Keep runtime entry explicitly `UNWIRED`.
6. Run focused Angular spec, existing API #09 fake-session suite (user previously required API tests), and Study Web build; update `gui/architech.md`, relevant Study Web context, GS04 status page and `docs/tasks/process.md`; run context validation and `git diff --check`.

## CHANGES

- Files changed: `GS04/models/gs04-curriculum.models.ts`; `GS04/pages/gs04-page.{ts,html,css,spec.ts}`; `GS04/ui/gs04-lesson-list.{ts,html,css}`; `apps/study-client/docs/list_screen.md`; GS04 DD `00-overview.md`, `03-data-flow.md`, `04-api-integration.md`, `05-business-rules.md`, `06-navigation.md`; `apps/study-client/gui/architech.md`; `.agents/context-manifest.json`, `.agents/context-map.md`, `.agents/project/dependencies.md`, `.agents/web-study/design.md`, `.agents/web-work/study/{AGENTS,INDEX}.md`; `docs/tasks/process.md`; this worklog. Guest route/GS03 and Study Server runtime files were not changed.
- CONTEXT_UPDATES: recorded GS04 page-to-#09 caller and title/order-only projection; query-tab remains unregistered and GS03 tab remains disabled; manifest source list includes new page/UI/spec files.
- Context pages changed: `.agents/context-map.md`, `.agents/project/dependencies.md`, `.agents/web-study/design.md`, `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`, `apps/study-client/gui/architech.md`; GS04 DD/catalog status updated while preserving all open gates.
- Assumptions: title/order-only rendering is derived from the screen purpose and API schema; no preview/access capability is implied.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `uv run pytest tests/modules/guest/api_09_courses_curriculum/test_courses_curriculum.py -q` | 11 passed; 1 upstream Starlette/httpx deprecation warning; fake-session tests only. | `VERIFIED` |
| `npm run test -- --include src/app/features/guest/GS04/pages/gs04-page.spec.ts` | 1 file, 4 tests passed. | `VERIFIED` |
| `npm run build` | Passed; 3 existing Student CSS budget warnings, no Guest/GS04 warning. | `VERIFIED` |
| Browser demo `/courses/:courseId?tab=curriculum` | Not run: query-tab route host remains `UNWIRED`; no live fixture/DB was used. | `BLOCKED_BY_DESIGN_GATE` |
| `node scripts/validate-agent-context.mjs` | Exit 1, 1,431 output lines matching T012/T013 baseline; 0 GS04/T014 findings. | `BASELINE_INVALID` |
| `git diff --check` | Passed after code/context updates. | `VERIFIED` |

## HANDOFF

- Remaining blockers: approved GS-04 loaded-list visual/access policy; eager/lazy and #08 cache/direct-entry behavior; query-tab composition consistent with the no-cross-screen-import rule; live schema and browser end-to-end runtime.
- Next action: continue the active 83-screen/API goal with another source-supported screen; revisit GS04 route composition when the query-tab design boundary is available.
