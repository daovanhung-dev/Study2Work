---
task_id: "2026-11-06-design-study-screen-st11"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-10 to ST-11 lessonId handoff; API #24 lesson content; APIs #25 progress, #26 resources and #27 next lesson; ST-12 resource panel; Study Web route/auth boundary"]
status: "PARTIAL"
---

# Worklog: Detailed Design màn hình Study ST-11

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected from 172; all selected files read; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Keep expected/current separate; preserve source assets; Study Web runtime is UNWIRED; trace API behavior from current backend rather than catalog alone.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Do not infer URL sync, debounce or navigation; API catalog can disagree with validators/response projections; fake tests and checked-in DDL do not prove runtime/live schema.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: One Screen ID per session; API #08/#09 source-backed but separate from Study Web; API #10 design-only; retain API orchestration discrepancies and avoid invented guest/student handoff.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ST-11 only; read its source and contracts; create a detailed plan before DD/annotation; preserve original `screen.png` and `code.html`; map every visible group to a sequential marker and DD element; trace events/APIs/state/navigation; update global tracker and worklog.
- Inventory: route `/student/lessons/:lessonId`, actor Student, AC-14/AC-15, APIs #24/#25/#26/#27; links ST-12/ST-09/ST-13/ST-17. Expected sequence: GET #24; GET #26 lazily; PATCH #25 on valid progress events; GET #27 after completion. States listed: loading/playing/paused/progress-saving/finished. Inventory blocker: throttle and autosave policy undecided.
- Canonical source/UI skill routing is being confirmed in the context registry; UI-only DD has no assumed API-DD template semantics.

## CURRENT_BEHAVIOR

- Initial folder inventory: only `screen.png` and `code.html`; screenshot is 1280×1024 and depicts a static “Bài học / Nội dung bài học hiện chưa sẵn sàng” fallback, not a lesson player. Source hashes: PNG `a7548e9f2523f9b6f4b8b71f986a1a199eb36e0654ed5bafdd454ccc8d37de33`; HTML `237ab57e4700a87b98e387f8a99554f4524ff7b6467d79a58b7f8d4e2c1d80e4`.
- Current HTML exactly reflects the fallback: 7 anchors: `/student/courses` (5), `/student` (1), `/student/progress` (1); no video/audio/iframe/source/form/input/canvas/button or inline handlers. Tailwind CDN/config scripts are the only scripts. The header/back CTA/footer are static links; route handling is not established.
- Study Server `app/api/v1.py` has 69 route decorators and no `/lessons` Student paths. Its five `/admin/lessons*` routes are Admin APIs #82–#86, not substitutes. `app/modules/student/` contains only API #34; exact route/test search found no #24–#27 Student route/module/query/focused tests. Current Study API implementation set excludes #22–#27.
- API catalog declares #24 GET Lesson; #25 PATCH body `{position:int32!, percent:int32!, completed:boolean!}`; #26 GET resources; #27 GET next. All require Student Bearer JWT and declare `ApiEnvelope<Lesson>`; all four API DD folders are Draft — Needs Confirmation. #25/#26/#27 are not in current source. Relevant Student test inventory has no API #24–#27 tests; existing Admin lesson routes/tests are role/path-distinct.
- API DD open questions: #24 entitlement/JWT, publish scope, 403/404, projection/null/path; #25 `position` meaning/storage, percent range, progress state/timestamps, upsert identity/idempotency, direct-call authorization, aggregate/transaction and response; #26 Lesson-vs-Resource payload/cardinality/order/empty, entitlement/publish/visibility, stored-vs-signed URL and path; #27 authorization/publish, curriculum ordering/ties, no-next vs not-found, Lesson payload/schema/path.
- Checked-in DDL is candidate only: `lessons` has nullable `course_id`, content/video_url and sort_order/status; `resources` has nullable lesson_id, name/type/url but no visibility; `lesson_progress` has nullable user_id/lesson_id, status/progress_percent/timestamps, no position or unique `(user_id,lesson_id)`. Live schema is not verified.
- Current Study Web remains UNWIRED. Editable source/package/router is absent; the student route is not present. Do not infer authentication, playback, navigation, cache, request ownership or media signing from mockup/API declarations.

## SOURCE_TRACE

- Expected source chain: ST-10 → lessonId → ST-11; player inventory calls #24, loads #26 lazily, patches #25 on valid progress events, and calls #27 after completion; AC-14/15 describe lesson access/content/resources/next. ST-10 itself also calls #24 before handoff, creating an unresolved single-vs-duplicate read ownership question.
- Current client chain: no editable Study Web source/router → static `code.html` fallback only → its anchors point to `/student/courses`, `/student`, `/student/progress`; no API calls/events/media controls. Screenshot and HTML hashes are recorded above and will be rechecked after annotation.
- Current API chain: catalog + AC/API DD declarations #24–#27 → exact current Study router/module/test scan → NOT_FOUND for all Student endpoints; Admin #82–#86 are separate. No API query or side effect can be traced for this screen.
- Candidate data: AC-14 says update lesson progress and course aggregate; checked-in `lesson_progress` lacks `position` and unique user/lesson key. AC-15 says check access/publish; no API #24/#26/#27 authorization query exists. DB artifacts are not live-schema proof.
- #26 response remains `ApiEnvelope<Lesson>` in catalog although use-case names attached resources; candidate Resource model has separate fields and no visibility column. #27 has no ordering/tie-break or terminal-item contract. No runtime policy is inferred.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Player screen state | Screenshot and HTML show unavailable-content fallback; no player/media/controls/resource list/progress UI is visible. | DISCREPANCY / DESIGN GAP | Do not invent a playing state or controls as current UI. |
| Study Web runtime | Editable Study Web source/package/router absent; `apps/study-client` current editable tree has documentation/assets only. | UNWIRED | Route, authentication, API calls and runtime behavior are not verified. |
| APIs #24–#27 | Catalog and four API DD drafts exist; exact Study router/module/test scan found no Student endpoints or focused tests. | DECLARED_NOT_RUNNABLE / NOT_FOUND | Do not describe API behavior as implemented or runtime verified. |
| #24 ownership | ST-10 inventory/DD calls #24 before handoff; ST-11 inventory also calls #24 on open. | DISCREPANCY / OPEN | Product/FE must specify whether transition or player owns the read and whether state is handed off. |
| #25 progress protocol | Required body includes position/percent/completed; candidate DDL has no position/unique key; throttle/autosave, aggregate, retry and state rules open. | DESIGN_ONLY / BLOCKER | Cannot specify event frequency, validation, persistence, dedup or completion trigger. |
| #26 resources | `ApiEnvelope<Lesson>` catalog conflicts with resource use-case and separate Resource schema; no current endpoint/visibility source. | DISCREPANCY / SECURITY BLOCKER | No resource list mapping, empty state, signed URL or safe open behavior can be finalized. |
| #27 next lesson | No route/module; ordering/tie-break, access, end-of-curriculum and payload semantics remain open in DD. | DECLARED_NOT_RUNNABLE / OPEN | No automatic next navigation or 404-to-finished mapping may be assumed. |
| Fallback versus player | The 1280×1024 screenshot and static HTML contain unavailable-copy only, no media/player/progress/resources/Next controls. | DISCREPANCY / DESIGN GAP | Current asset cannot prove the loaded/playing/paused/finished states promised by screen name/inventory. |

## CHANGES

- Files changed: `.agents/worklog/2026-11-06/design-study-screen-st11.md`; `apps/study-client/docs/screen_stitch/03_student/ST-11_trinh-hoc-bai-lesson-player/ST-11_PLAN.md`, `ST-11.md`, `ST-11_markers.json`, `ST-11_markers_overlay.svg`, `screen_annotated.png`; `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`. Original `screen.png` and `code.html` are preserved.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none; unresolved screen/API/player policy remains explicit.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective + mandatory docs preflight | Objective requirement carried forward; selector and all 3 selected exact-type worklogs read. | VERIFIED |
| Source/API trace | Inventory/AC/catalog/API DD/current router/modules/tests/candidate DDL and linked ST-10 were checked; #24–#27 are declarations only and no Student runtime source/test exists. | VERIFIED |
| Inventory coverage + static artifact audit | `list_screen.md` has 83 unique IDs; all 83 have a folder with original PNG/HTML; 20/83 now have the full plan/DD/marker/annotated bundle. 14 ordered unique markers ↔ 14 DD element rows; 8 sequential events; 14 SVG circles; original PNG bytes embedded; local links resolve; PNG/HTML hashes match baseline; dimensions 1280×1024 / 2820×2048; badges in bounds and non-overlapping. | VERIFIED |
| Visual review | Annotated screenshot opened; all labels readable, marker #3 moved above breadcrumb, no marker covers important text/control. | VERIFIED |
| `git diff --check` + whitespace audit | `git diff --check` exited 0; custom whitespace audit of changed Markdown/JSON/SVG/tracker/worklog passed. | VERIFIED |
| Context validator | No context pages/manifest changed. | NOT_REQUIRED |
| Tests/runtime | Not requested; no suites or runtime calls run. | NOT_RUN |

## HANDOFF

- Remaining blockers: fallback vs player design; #24 request ownership between ST-10/ST-11; missing lessonId handoff/Study Web route/auth; #24–#27 absent from Student runtime; #24 access/publish/error/content URL; #25 position/range/completion/upsert/aggregate/autosave/throttle/retry; #26 Resource response/cardinality/visibility/signed URL; #27 curriculum ordering/tie-break/no-next; no player controls or loading/error/recovery/accessibility states. ST-11 remains DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED.
- Next owner/action: ST-11 artifact bundle is complete with static checks; next independent session may start ST-12. Do not add another Screen ID in this session.
