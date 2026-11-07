---
task_id: "2026-11-06-design-study-screen-me03"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: ["test"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ME-03 consumes Study Server APIs #49/#65 using courseId from the ME-02/#46 flow; course ownership and module permissions must remain source-backed"]
status: "VERIFIED"
---

# Worklog: Detailed Design Study ME-03 — Workspace khóa học của mentor

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; selected 3 exact-type docs worklogs of 182; all selected files were read.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Keep expected behavior separate from source/runtime; preserve screenshot and HTML; Study Web remains UNWIRED; trace APIs and do not treat static/prototype content as live.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Recheck each source/API and keep unsupported fields, routes, filters and page behavior explicit; tests read are not runtime evidence; one Screen ID per session.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: Preserve image/HTML hashes; distinguish source-backed backend from absent UI wiring and runtime; record AC/inventory orchestration discrepancies without reconciliation by assumption.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ME-03 only in this session; inspect current screen/source and inventory; write its plan before DD/annotation; preserve original assets; create/check annotated image and marker map; trace all screen events, APIs and navigation to source; update global `dd_screens/PLAN.md` and this worklog; report `DD READY`, `IMPLEMENTATION BLOCKED` and `RUNTIME VERIFIED` separately.
- Inventory: `apps/study-client/docs/list_screen.md` row ME-03 proposes `/mentor/courses/:courseId`, actor Mentor, AC-22/AC-26, API #49/#65 after the course is identified through #46, render modules by permissions, and links ME-04/ME-06/ME-16. Expected states: loading/no-content/partial/error.
- Objective attachment: `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md`; one Screen ID per session, plan-first and required DD/artifact/status deliverables.

## CURRENT_BEHAVIOR

- Source assets: `screen.png` is 1234×1600, SHA-256 `4874aa947cdbb6526c4dda6fb29603cfa6e9ed88f644ac335966e9aa4fefbcb7`; `code.html` is 43,129 bytes, SHA-256 `268bb2385f79d049f3d2d77ce6ebc95333b33694f835dfcd5f1a11953cffdde5`. The screenshot is a static full workspace. HTML has 12 anchors (all `href="#"`), 15 buttons, one text input, no form/select/article, two script tags, no fetch/XHR, event listeners or page handlers. It labels #49/#65 “Synchronized/Live Feed”, but those are prototype copy. Existing directory had only the two original source files before this session.
- The design shows a course hero with code/cohort/date/owner/standard/enrollment/average-progress data; curriculum counts and four module cards; a weekly activity graph; recent activities; at-risk Student rows and reminder/scheduling actions; satisfaction/drop-off measures; three repository links; an AI Mentor callout; and page-level actions. The #49/#65 responses below do not support most of these sample values or panel grains.
- Study Web current tree was rechecked: no editable `src/`, `package.json` or router exists; ignored `dist/` exists. Runtime/route `/mentor/courses/:courseId` remains `UNWIRED` and serving is unverified.
- API #49: `app/api/v1.py` registers GET `/api/v1/mentor/courses/{course_id}/content` and delegates to `get_course_contents`. Shared Bearer/JWT guard requires `MENTOR` and runs before DB. Raw path is signed-int64 parsed; malformed/out-of-range and missing course map to 404. The view first reads `courses`, permits only direct `courses.mentor_id = JWT sub` (another owner → 403), then reads all same-course `contents` with `deleted_at IS NULL`, no status filter or pagination, ordered `parent_id NULLS FIRST, content_order ASC, id ASC`. Response is a flat `Content[]` with id/course_id/content_type/title/payload/status/optional parent_id/order. `payload` must be a JSON object; duplicate IDs, wrong-course rows, missing parents, cycles or invalid projections fail the entire response with safe 500. Empty tree is 200 `DESIGN_RESOURCE_RETRIEVED` with `data: []`. Read-only; no commit.
- API #65: `app/api/v1.py` registers GET `/api/v1/mentor/courses/{course_id}/progress` and delegates to `get_mentor_course_progress`. Same Bearer/JWT `MENTOR` guard, signed-int64 path and direct-owner check; another owner → 403, missing/malformed course → 404. The aggregate reads distinct ACTIVE enrollments for STUDENT users, uses PUBLISHED lessons, selects the latest `lesson_progress` per user/lesson by `last_accessed_at DESC NULLS LAST, id DESC`, counts COMPLETED lessons and computes floor-average percent, with 0 when no lessons. It returns an unbounded one-page `MentorStudentProgress` roster with Student id/name/optional avatar, completed/total lessons and percent; no page/size, module rows, at-risk status, events, assignments, review scores or timestamps. Empty roster is 200 with `items: []`, `size/total=0`, `total_pages=0`. Invalid aggregate mapping and DB errors return safe 500. Read-only.
- Contract boundaries: #49 catalog and AC-22 both declare `ApiEnvelope<Content[]>`; its local API DD remains Draft — Needs Confirmation for Content type/status/payload, revision and owner/assignment policy. #65 catalog remains `ApiEnvelope<Page<Course>>`, while current local source returns `Page<MentorStudentProgress>`; its local response, formula, active-enrollment and pagination choices are DERIVED and awaiting owner confirmation. Both use checked-in legacy BIGINT DDL/migrations; live schema/deployment were not checked.
- API #46 current query, rechecked for the ME-03 handoff, lists only directly owned courses and its Course model exposes id/title/description/thumbnail_url/price/status/Mentor summary. It has no course code, cohort/term, last-content-updated, enrollment count, standard, average progress or rating. ME-02 documented the same assigned-course discrepancy; AC-21 assignment semantics remain open.
- Test source exists for #49/#65 and was inspected for flat tree/empty/auth/role/path/owner/mapping/error and roster/formula/empty behaviors. Tests were not run. Fake-session test coverage and prior verification reports do not prove live schema/deployment.

## SOURCE_TRACE

```text
GET /api/v1/mentor/courses/{course_id}/content
  -> apps/study-server/app/api/v1.py:get_mentor_course_contents
  -> api_49_mentor_content_list.view.get_course_contents
  -> shared JWT/MENTOR guard -> signed-int64 path parse
  -> SELECT course -> direct owner predicate
  -> SELECT active Content rows -> validate projection/tree
  -> 200 Content[] / safe 401, 403, 404, 500; read-only
  -> focused API #49 test source reviewed, not run

GET /api/v1/mentor/courses/{course_id}/progress
  -> apps/study-server/app/api/v1.py:get_mentor_course_progress_endpoint
  -> api_65_mentor_course_progress.view.get_mentor_course_progress
  -> shared JWT/MENTOR guard -> signed-int64 path parse
  -> SELECT course -> direct owner predicate
  -> aggregate ACTIVE Student roster × PUBLISHED lessons/latest progress
  -> map one full-roster MentorStudentProgress page (DERIVED)
  -> 200 page / safe 401, 403, 404, 500; read-only
  -> focused API #65 test source reviewed, not run
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Study Web route/runtime | No editable app source/package/router; ignored `dist/` only. | UNWIRED | Route, client calls, caching and browser states are not current runtime behavior. |
| Course route context / access | Inventory/AC allow management or analytics permission and AC-21 includes assigned courses; #46/#49/#65 currently require direct `courses.mentor_id = JWT sub`, with role-only guard. | DISCREPANCY / BLOCKER | Assigned Mentors and fine-grained manage/view permissions are not supported by current API predicates. |
| Course summary | #49/#65 omit title/code/cohort/owner metadata; #46 provides a limited Course projection and has list pagination. | SOURCE_GAP | Direct entry/refresh cannot reliably hydrate the hero or resolve a course outside the current #46 page. |
| Curriculum and module progress | #49 returns flat Content nodes; #65 returns course-wide per-Student summaries over PUBLISHED lessons, with no per-module aggregation. | SOURCE_GAP / DISCREPANCY | Do not map arbitrary Content nodes or course averages to the screenshot's sections/modules. |
| Risk, activity, quality, resources, AI and export panels | Mockup fields/actions are not returned by #49/#65 and are outside ME-03 API inventory. | NOT_FOUND / BLOCKER | Remove/disable or obtain approved APIs and calculation/permission rules before implementation. |
| API #65 contract | `list_api.md` declares `Page<Course>`; current source emits a derived `Page<MentorStudentProgress>`; no paging request. | DISCREPANCY | UI must follow neither shape as canonical until API owner approves the local response and bounds. |
| Prototype behavior and visual target | Static labels claim API sync; anchors are `#`, controls have no handlers/API calls; remote Plus Jakarta Sans/Tailwind and compact controls differ from Study guide. | UNWIRED / DESIGN DISCREPANCY | Treat PNG/HTML as sample design only; apply Study design guide and resolve interaction data before frontend work. |

## CHANGES

- Files changed: `apps/study-client/docs/screen_stitch/04_mentor/ME-03_workspace-khoa-hoc-cua-mentor/ME-03_PLAN.md`, `ME-03_markers.json`, `ME-03_markers_overlay.svg`, `screen_annotated.png`, `ME-03.md`; `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; this worklog.
- Original `screen.png` and `code.html` were preserved; their SHA-256 hashes are recorded above.
- CONTEXT_UPDATES: None; no source/contract convention changed. UI-only DD has no registered canonical authoring skill in `context-manifest.json`; `createDD-markdown` is scoped to Web/API DD.
- Context pages changed: None.
- Assumptions: None.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Selector + selected worklog review | Three exact-type docs logs selected and read; no shortage. | VERIFIED |
| Inventory/context/source preflight | Objective attachment, ME-03 inventory/tracker, Web/Study context graph, manifest skill boundary, AC-22/AC-26, #46/#49/#65 source/catalog/DD/tests and candidate DDL reviewed. | VERIFIED_SOURCE_REVIEW |
- Plan-first order | Plan timestamp precedes marker JSON, annotated image and DD. | VERIFIED |
- Marker/artifact audit | 53 sequential unique markers match plan, JSON, SVG and DD; coordinates are in source-image bounds; 18 event rows/sections; source dimensions 1234×1600 and annotated dimensions 2468×3200; original asset hashes unchanged. Minimum marker-center distance is 34 px. | VERIFIED_STATIC |
- Links/format/tracker audit | Local Markdown links resolve; no trailing whitespace; `git diff --check` clean; global tracker is 31/83 with ME-03 statuses recorded. | VERIFIED_STATIC |
- Context validation | No `.agents/` context pages were changed. | NOT_REQUIRED |
- Tests/runtime | Tests not run; route and runtime not verified. | NOT_RUN |

## HANDOFF

- Screen statuses: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. The worklog `VERIFIED` status means source trace and static artifact audit are complete; it does not mean DD READY or runtime verification.
- Remaining blockers: ME-03 plan B01–B07 and DD B01–B09, including course assignment and fine-grained permissions, unresolved #65 response contract, missing course summary and unsupported risk/activity/quality/resource/AI/export data, and the Study Web route being UNWIRED.
- Next Screen ID: ME-04 in a separate session. Global tracker progress is 31/83 complete artifact packs; ST-20 remains a separate flow.
