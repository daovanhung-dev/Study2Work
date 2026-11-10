---
task_id: "2026-11-07-design-study-screen-ad14"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-34; AD-13 → AD-14; API #83–#86; AD-12 reload/#82"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-14

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 219; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Separate expected/current behavior; preserve assets; trace permission/query/response/test source; keep Study Web `UNWIRED`; do not claim runtime or tests.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Preserve Admin permission and data/privacy blockers; do not infer field/filter/action semantics; fake DB and API catalog are distinct evidence.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Keep identity handoff explicit; distinguish local source from catalog/AC; fake DB tests do not prove live schema or deployment.
- additional handoff reviewed: `.agents/worklog/2026-11-07/design-study-screen-ad13.md`.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-14 only in this session. Inspect current assets, contracts, AC-34, API #83–#86, and backend/source/test evidence. Write `AD-14_PLAN.md` before marker map, annotation, or screen DD; preserve source assets; map every marker to a DD element; author sections A–F with traceable event/API/error/state/navigation details; update inventory, API reverse index/global plan and this worklog; stop before AD-15.
- Inventory row 72 describes `/admin/lessons/:lessonId/edit`, AC-34, APIs #83–#86, lesson editing, status change and delete with dependency confirmation; AD-12 and AD-13 are related screens. This is an expected flow to verify against current contracts/source, not implementation evidence.
- AC-34 expected branch from AD-13/#83 to AD-14 update #84, status #85, or delete #86, then refresh #82/#83. Preserve each operation and route boundary; do not infer client semantics from the mockup.

## CURRENT_BEHAVIOR

- AD-14 source folder initially contains only `screen.png` (1510×1600; SHA-256 `6566d258887283bbba59361f613441cfdefe8f0a2a3416204016e1ec0e2baca9`) and `code.html` (23,359 bytes; SHA-256 `77e632dad66ca86d823e575c8339d7af0efd073976519602fdc06181d05118f9`). The prototype has a static lesson edit form, a status-action panel, a dependency-lock delete panel, and static Admin shell/footer. All five form controls are disabled; save/status/delete buttons are disabled. Links use `href="#"`; there is no route binding, request, listener, timer, SSE/WebSocket, or client data binding. Study Web currently has docs/assets and ignored `dist`, but no editable source, package manifest, router or API client; status `UNWIRED`, runtime not verified.
- Inventory row 72 and AC-34 expect the path `/admin/lessons/:lessonId/edit`, Admin with lesson-management permission, a selected lesson, three separate mutation branches (#84 update, #85 status, #86 delete), then a reload of AD-12 through #82. AC-34 node n5 says “lesson + dependencies”; its diagram does not define the dependency output shape.
- API #84 is composed as `PUT /api/v1/admin/lessons/{lesson_id}` and returns direct `ApiEnvelope<Lesson>` / `DESIGN_RESOURCE_UPDATED`. Catalog and AC declare only path `lesson_id:int64!`, no body; current typed Pydantic body is a DERIVED strict full replacement `{title, content, video_url, order}`. All four keys are required; `content` and `video_url` may be null, title is max 200 chars (empty/untrimmed accepted), order strict int32, extras forbidden. FastAPI validates the typed body before the endpoint checks auth. View then checks shared `ADMIN`, parses signed int64 path (invalid/out-of-range -> local 422), updates legacy candidate `lessons.name/content/video_url/sort_order/updated_at`, excludes `DELETED`, maps the returned row to reusable Lesson, then commits; query/no-row/mapping/commit failures rollback and map to safe 500/404. It preserves course/status and performs no dependency/audit mutation.
- API #85 is composed as `PATCH /api/v1/admin/lessons/{lesson_id}/status`, with typed required `{status}` and local DERIVED values `DRAFT|PUBLISHED|SUSPENDED` (strict, extra fields forbidden); direct response is Lesson. It locks the active non-DELETED legacy Lesson, returns a no-op Lesson and commits without duplicate audit when status is unchanged, otherwise updates status/updated_at, inserts actor + previous/new values into `lesson_status_audit_logs`, validates the returned Lesson, then commits atomically. No transition matrix, readiness/progress gate, moderation rule, or fine-grained permission is present in current code. Body validation precedes handler/auth.
- API #86 is composed as path-only `DELETE /api/v1/admin/lessons/{lesson_id}` and direct `ApiEnvelope<DeleteResult>`; local response data is `{id, status:"deleted", deleted_at}`. Shared ADMIN auth precedes raw signed-int64 validation/query; invalid path -> 422. It locks a non-DELETED Lesson, checks for any `lesson_progress`, `resources`, or `lesson_uploads` reference, returns catalog 422 without mutation if any exist, otherwise writes status `DELETED` and `updated_at=CURRENT_TIMESTAMP`, maps returned `updated_at` to `deleted_at`, and commits. Missing/already-deleted -> 404; query/projection/commit failures -> safe 500 and rollback. No dependency counts or detail list are returned, and the set/completeness policy is DERIVED.
- API #84/#85/#86 focused HTTP test source is present and was reviewed. Tests cover auth/query order, input/path/body cases, response/mapping, mutation/audit or dependency branches, rollback, safe errors and OpenAPI. They use fake sessions/DB projections; tests were not run in this session and do not prove PostgreSQL/live schema/deployment.
- API #84/#85/#86 DD folders all say `Draft — Needs Confirmation`. Current checked-in legacy `lessons` is BIGINT with nullable `course_id`, `sort_order`, and `status`; API #85 migration 012 is a checked-in legacy BIGINT audit candidate only. V1-PILOT uses UUID lessons with chapter/course-version fields and no matching Lesson status; neither proves live schema. Reusable Lesson requires numeric `course_id`, int order and string status.
- Screenshot shows course/type selectors not present in #83/#84 mapping, no video_url control despite #84 requiring it, and an “Archived/Lưu trữ” state label while #85 accepts `SUSPENDED` rather than `ARCHIVED`. Its “two-layer validation”/progress-preservation claims and disabled controls are not runtime evidence. Study Web visual target is ocean-blue, Inter/system, centered/responsive; prototype uses full-width Plus Jakarta Sans and cobalt styling.

## SOURCE_TRACE

```text
Expected: AD-13 numeric Lesson.id → proposed AD-14 route → GET #83 Lesson → choose one action branch → #84 UPDATE, #85 status + audit, or #86 conditional soft-delete → AC-34 reload AD-12/#82.
Current: no Study Web caller/wiring → route handlers in apps/study-server/app/api/v1.py pass path/body/header/Session/trace to separate #84/#85/#86 modules → shared ADMIN guard (typed #84/#85 bodies are parsed before handler) → module-specific validation and query → transaction-owned effect/response. #84 updates metadata only; #85 changes status and records audit; #86 locks then checks progress/resources/uploads and soft-deletes only if no references. API DDs and local tests remain Draft/fake-DB evidence; production schema/runtime is unverified.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| #84 request vs edit form | Catalog/AC omit a body; current implementation uses a DERIVED required full-replacement body with `title/content/video_url/order`. The screenshot has course/type controls and no video_url control. | `DISCREPANCY / BLOCKER` | Do not invent mappings or silently clear/preserve hidden values; contract and editor field behavior need confirmation. |
| #85 status vocabulary/policy | Mockup says Draft/Published/Archived; local body allows `DRAFT/PUBLISHED/SUSPENDED`; no transition/readiness/progress rule; status audit uses migration 012 candidate. | `DISCREPANCY / BLOCKER` | Do not equate Archived with SUSPENDED or claim a publish gate; status enum/transition/audit schema need approval. |
| #86 dependency gate | AC-34 says lesson + dependencies and catalog title requires progress/reference checks; current local #86 checks any progress/resources/lesson_uploads at mutation time only and returns generic 422. #83 exposes no dependency output. | `DERIVED / BLOCKER` | UI cannot know deletion eligibility/counts before action; approve dependency set and retain server-side recheck. |
| Authorization | AC-34 requires lesson-management permission; all current mutation routes use shared role `ADMIN` only. | `DISCREPANCY / BLOCKER` | Fine-grained authorization policy/claim is unresolved. |
| Schema/audit/runtime | Legacy BIGINT lessons vs V1-PILOT UUID model; legacy required-response columns nullable; migration 012 and API test doubles do not prove live schema. | `OPEN / BLOCKER` | No live DB, migration, FK/lock or production behavior claim. |
| Study Web and design | Prototype is static with disabled form/actions; no editable app source/router/client; mockup differs from Study design guide. | `UNWIRED / DESIGN DISCREPANCY` | No frontend implementation or runtime verification; proposed route remains design-only. |

## CHANGES

- Created `AD-14_PLAN.md` before marker map, annotation and screen DD; plan defines 72 markers and EV-01…EV-07.
- Preserved original `screen.png` and `code.html`; created `AD-14_markers.json`, `AD-14_markers.svg`, `screen_annotated.png` 3020×3200, and `AD-14.md` A–F with 72 rows and explicit source/API blockers. Final visual review moved #35, #38, and #42 clear of adjacent markers and labels; DD coordinates match the final JSON/SVG.
- Updated AD-14 inventory row 72 and API reverse index #084–#086 from D→R based on local route/module/query/model/test source. Updated global AD-14 plan row and appended 67/83 checkpoint; AD-15 unchanged and API DD folders remain Draft.
- Files changed: `apps/study-client/docs/screen_stitch/05_admin/AD-14_sua-doi-trang-thai-xoa-bai-hoc/AD-14_PLAN.md`, `AD-14_markers.json`, `AD-14_markers.svg`, `screen_annotated.png`, `AD-14.md`; `apps/study-client/docs/list_screen.md`; `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; this worklog.
- CONTEXT_UPDATES: none. Context pages changed: none. Assumptions: none.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Objective reread; docs selector READY 3/219; AD-01, AD-02, AD-03 and AD-13 worklogs reviewed. | VERIFIED |
| AD-14 source and API trace | Screen assets, inventory, AC-34, API catalog and #84–#86 Draft DD, route/module/query/model/test source, legacy/V1-PILOT DDL and design guide reviewed. Test sources were read, not run. | VERIFIED_SOURCE_REVIEW |
| AD-14 static artifact audit | 17/17 checks passed: source hashes; 1510×1600 → 3020×3200 dimensions; 72 ordered JSON/SVG/DD markers with exact label/coordinate mapping, in-bounds and no marker overlaps; A–F/EV-01…EV-07; 24/24 local links; 83/83 inventory IDs/folders; 67/83 core artifact sets; all 8 plan items; no new trailing whitespace; updated tracker rows/checkpoint with AD-15 still D; explicit blocker states; and `git diff --check`. Final annotated PNG was visually inspected after the marker adjustments. | VERIFIED |
| Application tests/runtime | Not run. | NOT_RUN |

## FINAL_STATUS

- AD-14 screen: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Unresolved body/form mapping, status vocabulary/policy, dependency output/completeness, lesson-management authorization, live schema/migration and Study Web wiring remain explicit blockers.
- AD-14 artifact and source review work is complete. No application tests or runtime were run.

## HANDOFF

- Remaining AD-14 work: none.
- Next screen in a separate session: AD-15. Do not start it in this session.
