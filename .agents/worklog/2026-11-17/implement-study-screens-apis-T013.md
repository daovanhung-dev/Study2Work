---
task_id: "2026-11-17-implement-study-screens-apis-T013"
date: "2026-11-17"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["web-work (Study Web)", "server-study"]
cross_scope_dependencies: ["Candidate GS-04 curriculum tab -> Study Server API #09 route/contract/tests/schema"]
status: "IN_PROGRESS"
---

# Worklog: Continue Study Web screen implementation — T013

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `READY`; 122 available; T011, T012 and T004 selected and read in full; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T011.md`
    - carry_forward: AD-22/#97 is source-wired but report projection/permission/live schema are unresolved; keep its metadata gates and do not infer #98 report detail behavior.
  - path: `.agents/worklog/2026-11-17/implement-study-screens-apis-T012.md`
    - carry_forward: GS-01 #05/#06 and GS-03 #08 are implemented; GS-03 curriculum/reviews/enrollment remain gated. Focused tests/build passed, but local #09 API/browser data runtime is unverified. Keep all user dirty worktree paths.
  - path: `.agents/worklog/2026-11-16/implement-study-screens-apis-T004.md`
    - carry_forward: GS-02 is a bounded #07 slice; category/cache/order behaviors remain gated. Overall objective remains role-aligned APIs plus all 83 Study Web screens.
- shortage: `none`
- Additional context read: `.agents/AGENTS.md`, partial `.agents/context-map.md` (Guest source description is stale and needs exact source check), `.agents/project/agent-control.md` (required flow/receipt sections), `.agents/worklog/{README,TEMPLATE}.md`, `.agents/project/INDEX.md`, `.agents/web-work/study/{AGENTS,INDEX}.md`, `.agents/web-study/{frontend-rules,design}.md`.
- Current worktree baseline: branch `develop`; `git status --short | wc -l` reported 609 entries. T012 final check reported no staged changes. Preserve all existing dirty files; do not reset, clean or stage.

## EXPECTED_BEHAVIOR

- Full active objective: organize Study Server API packages by `admin`, `student`, `mentor`, `guest`, `shared`; implement all 83 Study Web screens from `dd_screens/`, `screen_stitch/`, `list_endpoint.md` and `list_screen.md`; run backend/API checks while coding and add/fix APIs only when DD/BD/source support them; read relevant design and server documents; deliver supported UI behavior integrated with backend; plan before every operation.
- Overall objective remains **20% ACTIVE** at T013 start; this continuation must make progress without redefining the 83-screen/API objective around one screen.
- Candidate from current screen catalog: `GS-04 Đề cương khóa học`, `/courses/:courseId?tab=curriculum`, API #09. This is a candidate only until current route, DD, API source/tests/schema and blockers are verified.
- Study FE scope candidate: `screens=GS-04; APIs=#09`. Any final narrowing or expanded scope will be recorded after M0.

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 15% | 15% | Complete worklog/context preflight, inspect current screen/API catalogs and worktree, verify the next source-supported screen/API candidate and exact DD/source/test paths. | `DONE` |
| 65% | 80% | Read the full selected screen package and relevant API DD/BD/source/tests/schema, record caller-to-response evidence and discrepancies, then implement the largest behavior-complete subset supported by evidence without inventing contract or policy. | `PENDING` |
| 20% | 100% | Run applicable focused frontend/backend checks and build; attempt browser route demo and fixture cleanup when safe; inspect diff/links/context; update this worklog, current-source context and `docs/tasks/process.md`; state runtime gaps. | `PENDING` |

**Current T013 progress: 15%. Overall objective: 20% ACTIVE.**

## CURRENT_BEHAVIOR

- Catalogs: `list_screen.md` has 83 screen rows; `list_endpoint.md` defines 103 APIs. GS-04 is `/courses/:courseId?tab=curriculum`, P1, API #09, as a tab within GS-03.
- Current client: `app.routes.ts` loads `guestRoutes` under `/courses`; `guest.route.ts` contains GS02 `/search`, GS03 `/:courseId`, GS01 `''`. `GS03Page` reads the route string and calls #08 via `GS03CourseDetailService`; curriculum/review tabs are disabled, with no #09 client caller.
- Current API #09: `app/api/v1.py` registers public `GET /courses/{course_id}/curriculum` and passes the path string to `get_course_curriculum`. The validator parses signed-int64; the view checks a PUBLISHED course, reads only PUBLISHED lessons ordered by `sort_order, id`, maps `LessonPage` with one page and returns `DESIGN_RESOURCE_RETRIEVED`; invalid/out-of-range/missing/unpublished course maps 404 and DB/mapping failure maps safe 500. No write or external side effect.
- Current API #08 and #09 validators both enforce signed-int64; the inventory's prior “raw string has no range” gate is stale for current backend source. The client route parameter remains text; UI behavior waits for DD review.
- `.agents/server-study/tests.md` records API #09 focused suite 11/11 after the signed-int64 fix; tests use fake DB sessions. No T013 API test has been run.
- Checked-in `DB.sql` defines `courses.id BIGSERIAL`, `lessons.course_id BIGINT`, and lesson `name`, `content`, `video_url`, `sort_order`, `status`; this DDL artifact does not prove live schema/deployment.
- Study OpenAPI remains `NOT_FOUND`. `.agents/context-map.md`, `.agents/project/dependencies.md`, `.agents/web-study/design.md`, and `apps/study-client/gui/architech.md` still have stale Guest route summaries and need reconciliation after package review.

## SOURCE_TRACE

```text
/courses -> guestRoutes -> GS03Page -> current #08 detail GET
  -> GS-04 curriculum tab has no caller yet
  -> candidate GS04 data-access -> StudyApiService API_009
  -> FastAPI #09 -> signed-int64 validator -> PUBLISHED course lookup
  -> PUBLISHED lesson query ordered by sort_order,id
  -> LessonPage {items,pagination} -> candidate tab UI
  -> #09 fake-DB HTTP tests (11 prior passes; not live DB)
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| GS-04 client wiring | Current `guest.route.ts` registers GS01–GS03 only; GS03 curriculum tab is disabled and there is no #09 client caller. | `UNWIRED` | Candidate is an embedded tab; do not invent a separate URL or bypass GS03 course state before DD review. |
| GS-04/API #09 expected behavior | Inventory row 11 maps #09 to public `Page<Lesson>` and flags visibility, cache, eager/lazy and direct-entry behavior. Full screen/API DD review is pending. | `DISCREPANCY / PENDING_DD` | Do not determine activation, cache, returned fields or lesson navigation before full package review. |
| Course ID validation | APIs #08 and #09 current validators both enforce signed-int64; older inventory text says #08 has no range validation. | `SOURCE_SUPERSEDES_STALE_INVENTORY` | Reconcile inventory/DD against current code after API DD review; do not use JS Number for int64 IDs. |
| Database evidence | `DB.sql` has BIGSERIAL/BIGINT course/lesson columns and fields consumed by #09; deployed schema was not observed. | `DDL_ARTIFACT_ONLY / LIVE_NOT_VERIFIED` | No DB fixtures or production/live schema assumptions. |
| Current Guest context | `context-map.md`, project dependencies, Study design guide and app architecture still summarize Guest as GS02-only. | `CONTEXT_STALE` | Update those summaries from verified current routes/source as part of T013. |

## IMPLEMENTATION_PLAN

M0 selected GS-04/#09 for M1. The full GS-04 DD/HTML/image/marker package, API #09 DD/source/tests, the AC-05/ERD diagrams, current Guest route graph, API transport and GS03 caller/spec are now reviewed.

### EXECUTION_PLAN_V1 — recorded before implementation

1. `DONE`: add only the source-backed GS04 client data-access contract: typed response models and a `GS04CurriculumService` that calls registered API #09 with the route `courseId` preserved as a string. Do not convert path IDs through JavaScript `Number`.
2. Do not wire the service into a route or render returned lessons yet. API #09 DD is Draft; its `PUBLISHED` visibility filter is an assumption, the response includes public `content`/`video_url` without a preview/access field, the loaded-list/error designs are absent, and AC-05 eager versus F02 lazy plus cache/direct-entry behavior conflict. A clarification has been sent for the permitted Guest fields and lazy/eager call timing.
3. Keep Study Server source unchanged unless a mismatch with the DD/BD/source justifies a fix. Run the focused API #09 fake-session suite after the client slice as requested; label it as non-live evidence.
4. `DONE`: reconcile the current-source summaries in `.agents/context-map.md`, `.agents/project/dependencies.md`, `.agents/web-study/design.md`, and `apps/study-client/gui/architech.md`; correct GS04 package/inventory claims about #09 ID parsing and Guest wiring. Preserve unresolved behavior as `CẦN_XÁC_NHẬN`/`DD BLOCKED`.
5. After the clarification arrives, implement only the approved GS04 UI behavior; otherwise stop UI wiring at the recorded contract gate and report the exact missing decision. Then run the applicable frontend checks/build, inspect the diff, update this worklog and `docs/tasks/process.md`, and run the context validator if context files changed.

## CHANGES

- Files changed: T013 worklog, T013 row in `docs/tasks/process.md`, GS04 client DTO/service, `.agents/context-map.md`, `.agents/project/dependencies.md`, `.agents/web-study/design.md`, `apps/study-client/gui/architech.md`, `apps/study-client/docs/list_screen.md`, GS04 DD 00–07 current-source notes, and GS04 Stitch source/plan follow-up.
- CONTEXT_UPDATES: Guest route/caller summaries now reflect GS01–GS03 and the uncalled GS04 service. GS04 docs/catalog reflect signed-int64 server validation, the 11-test run, and the still-open visibility/layout/orchestration gates.
- Context pages changed: `.agents/context-map.md`, `.agents/project/dependencies.md`, `.agents/web-study/design.md`, `apps/study-client/gui/architech.md`.
- Assumptions: candidate GS-04 may be narrowed or rejected if source/DD evidence shows no independently implementable behavior.

## VERIFICATION

| Command / evidence | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | `READY`; T011, T012, T004 selected and read in full. | `VERIFIED_PREFLIGHT` |
| Catalog rows | `list_screen.md` contains 83 screen rows; GS-04 row 11 maps to API #09. API catalog full endpoint count/source trace pending. | `PARTIAL_M0` |
| API #09/current client source audit | `guest.route.ts` has GS01–GS03 only; GS03 calls #08 and leaves curriculum disabled. Server #09 is a public read route with signed-int64 parsing and a published-course/published-lesson projection; route/module/focused-test paths verified. DDL inspected as artifact only. | `VERIFIED_M0_CANDIDATE` |
| GS04/API #09 package and design evidence | Read GS04 DD 00–07, Stitch source/plan/markers/HTML and rendered/annotated images; read API #09 DD 00–07, current module/tests, AC-05 and DB ERD. Confirmed no loaded-list/error design, unapproved visibility assumption, public content/video fields, eager/lazy/cache/direct-entry discrepancies, and stale DD parser notes. | `VERIFIED_M1_AUDIT; UI_GATE_REMAINS` |
| GS04 client API contract | Added response DTOs and `GS04CurriculumService` using API #09 and the unmodified string route ID. No page calls the service yet. | `CODE_ADDED_NOT_WIRED` |
| API #09 focused suite | `uv run pytest tests/modules/guest/api_09_courses_curriculum/test_courses_curriculum.py -q` | `11 passed`; 1 Starlette/httpx deprecation warning; fake-session only; no live DB verification. | `VERIFIED_TESTS` |
| Study Web production build | `npm run build` in `apps/study-client` | Pass; 3 existing Student CSS budget warnings; no Guest CSS budget warning. | `VERIFIED_BUILD` |
| Context validator | `node scripts/validate-agent-context.mjs` after context-manifest update | `AGENT_CONTEXT_INVALID`, 1,431 output lines, same count as T012 baseline; filtered findings for GS04/T013/process: 0. Repo-wide DB Admin/orphan-skill/context-stale findings remain. | `BASELINE_LIMITATION` |
| Whitespace/stale scan | Scoped `git diff --check` and current-source `rg` scan | Whitespace clean. Only old parser note is in historical 2026-11-16 plan snapshot and is superseded by its 2026-11-17 follow-up. | `VERIFIED_DOC_SYNC` |

## HANDOFF

- Remaining blockers: API #09 DD approval, lesson field/access/display policy, loaded/error/loading visual design, AC-05 eager vs F02 lazy, cache/direct-entry, and live DB remain unresolved.
- Next owner/action: continue GS04 page/tab UI only after the pending product/API clarification. Current code is limited to the typed #09 client data-access slice; do not infer that the UI or runtime is complete.
