---
task_id: "2026-11-06-design-study-screen-gs03"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["GS-03 uses Study API #08 for public course detail and lazy-loads #09 curriculum/#10 reviews; the course ID and linked tabs must agree across GS-01/GS-02/GS-04/GS-05/GS-06/ST-04"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study GS-03

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: node scripts/select-worklogs.mjs --type docs --limit 3
- selector_result: READY; selected 3 exact-type docs worklogs of 162; no shortage.
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-11-06/design-study-screen-gs01.md
    - carry_forward: Keep expected screen behavior separate from current assets/API; source UI/runtime absent; detail navigation uses proposed route only; preserve unsupported card claims.
  - path: .agents/worklog/2026-11-06/design-study-screen-gs02.md
    - carry_forward: Trace backend contracts and current source independently; Study Web stays UNWIRED; keep route, page-size and displayed-field discrepancies explicit; preserve original screen/HTML hashes.
  - path: .agents/worklog/2026-11-06/design-study-screen-sh01.md
    - carry_forward: Do not infer marketing data, price/rating claims, or browser route behavior; record expected/current disagreements; one Screen ID per session.
- shortage: none

## EXPECTED_BEHAVIOR

- Goal objective file was read before this continuation: /home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md. This session covers GS-03 only; plan before DD/annotation; preserve source assets; produce ordered marker mapping, DD, tracker update and worklog.
- Inventory requirement: GS-03 proposes /courses/:courseId, actor Guest, AC-05, APIs #08/#09/#10, and links GS-04/GS-05/GS-06/ST-04. Expected data includes course details, mentor, price, curriculum/reviews tabs, and enrollment CTA. Initial #08 is expected to determine PUBLISHED state; #09 and #10 are expected to load lazily by tab. Expected states: loading, course-404, partial-tab-error.
- Skill routing: context manifest registers createDD-markdown only for Web/API DD and excludes web-ui-only-dd. This screen-level UI DD has no registered canonical skill; do not apply the API DD template as if it were the UI contract.

## CURRENT_BEHAVIOR

- Source/config: At start, GS-03 folder had only `screen.png` and `code.html`; plan/DD/marker/annotated image did not exist. Preserved-source hashes rechecked: screen `94360a8b1b1a9bbe0cdc110f6c243ce5aaabd8b6923331c5667421cb1c37d34d`; HTML `d4f4bfdb56324b7c96589af75362903a491a3f565c97152b63634573c9d69619`. PNG is 1280×1024, entropy 0.35757, 20 colors and visually unusable. HTML is a static empty Guest fallback: links, breadcrumb, title, three tabs (curriculum/reviews disabled), unavailable message, return link and footer; no course hydration, route binding, API request or tab handler.
- Study Web app source/package/router/entrypoint remains absent per `.agents/web-study` `UNWIRED` status; current worktree source inventory has no Study Web runtime. No browser runtime claim is supported.
- API #08: route in `apps/study-server/app/api/v1.py` calls `api_08_courses_detail.view.get_course_detail`; shared `parse_integer` accepts int or digit strings only. Query finds a course by ID with status `PUBLISHED`, LEFT JOINs mentor. Success returns `ApiEnvelope` with `CoursePage` singleton in `data.items` and pagination all 1. Course projection has id/title/optional description/thumbnail_url/price/status/mentor{id/full_name/optional avatar_url}. Invalid/missing/unpublished returns 404 `DESIGN_RESOURCE_NOT_FOUND`; SQL or mapping errors return 500 `DESIGN_INTERNAL_ERROR`. Test source exists and was read, not run. API is `SOURCE_BACKED` despite D label in catalog/inventory.
- API #09: route/module/view/query/test source exist. View checks PUBLISHED course, then lists only PUBLISHED lessons ordered by `sort_order ASC, id ASC`; fields are id/course_id/title/content?/video_url?/order/status. Empty curriculum succeeds with `items=[]`, `total=0`, `total_pages=0`; missing/unpublished course is 404; DB/mapping failure is 500. Test source exists and was read, not run. API is `SOURCE_BACKED`; no preview/access policy was found.
- API #10: catalog and API DD declare public GET `/api/v1/courses/{course_id}/reviews` with page/rating query and `Page<Discussion>`, but no corresponding route/module/test exists in current Study server source. Its DD is `Draft — Needs Confirmation`; checked-in discussions DDL has no title or rating, and no rating table. API is `DECLARED_NOT_RUNNABLE`.
- AC-05 diagram calls #08, #09, and #10 sequentially before rendering; list_screen F02 says #09/#10 lazy by tab. Preserve this orchestration discrepancy. AC-05 permits 403 on private course while current #08 returns 404 for invalid/missing/unpublished.
- Enrollment CTA is required by inventory but absent from HTML. Inventory links ST-04; F03/G-01 block #15 status because Public request only has course_id while response has user_id. Do not invent an enrollment event/request or guest→student/login policy.

## SOURCE_TRACE

- #08 route → view → validator → published-course query + mentor join → singleton CoursePage envelope → test source, as recorded above. GET is read-only; current API trace identifies rollback on SQLAlchemy error.
- #09 route → view → validator → published-course check → published lesson list/order → LessonPage envelope → test source, as recorded above. GET is read-only; rollback on SQLAlchemy errors.
- #10 inventory/API DD only; exact route/module/test search found no executable source. DDL and API DD conflict on rating/title source.
- Screen route remains proposed; Study Web current status is UNWIRED.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| GS-03 screenshot/HTML | Original PNG is nearly blank; static HTML is a Guest empty-state prototype, not a loaded detail screen. Hashes recorded above. | VERIFIED | Preserve original files; render HTML as separate documented replacement only if browser output is faithful. |
| Study Web wiring | Registered Study Web subcontext is UNWIRED; current app source must be rechecked. | UNWIRED | Do not claim browser route or runtime integration. |
| API #08 | Route/module/query/view/test source present and traced; catalog/inventory still labels D. | SOURCE_BACKED; DISCREPANCY | Backend source exists; does not prove UI wiring or deployed DB/runtime. |
| API #09 | Route/module/query/view/test source present and traced. | SOURCE_BACKED | Curriculum tab can be described against current source; lesson visibility semantics remain unresolved. |
| API #10 | Declared in catalog and API DD, absent from current route/module/test source; missing title/rating source. | DECLARED_NOT_RUNNABLE | Reviews/rating tab cannot be called or described as operational. |
| AC-05 API order | AC-05 sequences #08→#09→#10 before render; F02 requires #09/#10 lazy by tab. | DISCREPANCY | Needs Product/BE resolution; document both without inferred reconciliation. |

## CHANGES

- Files changed: Worklog; `GS-03_PLAN.md`; `GS-03_markers.json`; `GS-03_markers_overlay.svg`; `screen_rendered.png`; `screen_annotated.png`; `GS-03.md`; `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` (GS-03 row/progress and verified F02 #09/#10 wiring). Original `screen.png` and `code.html` are preserved.
- CONTEXT_UPDATES: none planned; no implementation, API contract, or database schema is being changed.
- Context pages changed: none.
- Assumptions: none.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective and mandatory docs preflight | Objective reread; selector selected 3 exact-type docs worklogs of 162; all selected files read. | VERIFIED |
| GS-03 source/API/artifact audit | Original hashes unchanged; 83 unique IDs/folders; 10/83 complete artifact sets; marker #1–#10 maps once each to DD; event IDs #01–#06 sequential; relative links resolve; image dimensions/SVG embedding checked; tracker row/status/next ID correct. | VERIFIED |
| `git diff --check` | No whitespace errors. | VERIFIED |
| Context validator | No context pages/manifest were changed; validator not applicable. | NOT_REQUIRED |
| Tests/runtime | Do not run unless user asks. | NOT_RUN |

## HANDOFF

- Remaining blockers: loaded course/mentor/price design and CTA absent; AC-05 eager API order differs from F02 lazy tabs; API #10 has no route/module/test and lacks title/rating data source; G-01 enrollment identity/auth handoff unresolved; Study Web remains UNWIRED. GS-03 is not DD READY.
- Next owner/action: GS-04 in a separate session; do not begin it in this session.

