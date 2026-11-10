---
task_id: "2026-11-06-design-study-screen-me02"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: ["test"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["Study Web ME-02 consumes Study Server #46; course ownership/assignment and downstream course routes must agree"]
status: "VERIFIED"
---

# Worklog: Detailed Design Study ME-02 — Các khóa học phụ trách

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; selected 3 exact-type docs worklogs of 180; all selected files were read.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Keep design separate from current source; preserve source PNG/HTML; Study Web is UNWIRED; inventory/data/filter fields need exact trace; don't treat fake UI or API docs as runtime evidence.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Recheck source and API current state each screen; retain query/filter/page-size discrepancies; prototypes and fake-session tests do not prove runtime/live schema; one Screen ID per session.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: UI-only DD has no canonical skill; use manifest boundary; source-backed API does not establish frontend route/runtime; preserve approval and source/current discrepancies explicitly.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ME-02 only in this session; write its plan before DD/annotation; preserve source assets; create/check annotated screenshot and marker map; trace source/API/events/states/navigation; update `dd_screens/PLAN.md` and this worklog; distinguish DD readiness, implementation blockers and runtime verification.
- Inventory: `apps/study-client/docs/list_screen.md` ME-02 row, route proposal `/mentor/courses`, AC-21, API #46, course ownership/assignment, status/page/size and manage actions. Expected states loading/empty/ready/denied; linked screens ME-03/ME-04/ME-16.
- Activity flow: AC-21 in `apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio` says Mentor must own or be assigned the course before creating a lecture; #46 selects courses then #34/#47 create the lecture.
- Skill routing: `.agents/context-manifest.json` lists `createDD-markdown` with exclusion `web-ui-only-dd`; no canonical UI-only DD skill applies. No API DD skill/template was used for this UI DD.

## CURRENT_BEHAVIOR

- Assets: `screen.png` is 1100×1600, SHA-256 `fc133a37e6b5783d1d220145d07fb995be4d7bd0962c218e65d3d876c49a9bc4`; `code.html` is 47,810 bytes, SHA-256 `1f0287c63b92f85c98a34f2a8862ac14c7a93a6a080adc679c3d13e250559354`. The page is a static sample with 3 course cards, KPI/filter/footer content, 19 `href="#"` anchors, 11 buttons, 2 text inputs, 4 selects and 3 articles. It has no app/API/router binding; its `querySelectorAll` selector includes non-standard `:contains()`.
- Study Web: current checkout has docs, ignored `dist`, node_modules and tsbuildinfo, but no editable `src/`, `package.json` or router. Registered Study Web subcontext marks it `UNWIRED`; bundle has only root route `/`; serving/deployment unverified.
- API #46: `app/api/v1.py` registers `GET /api/v1/mentor/courses`; route calls `get_mentor_courses`. Shared guard validates JWT numeric subject and `MENTOR` role before query. Inputs are optional `status` exact `DRAFT|PUBLISHED`, `page=1`, `size=20` with page>=1 and size 1..100. Count and list scope direct `courses.mentor_id = JWT sub`; optional status predicates match; fixed order `created_at DESC, id ASC`; GET is read-only. Course output is id/title/optional description/thumbnail_url/decimal-string price/status/Mentor summary plus pagination. It has no search, code, level, sort, student/course completion/rating/capstone metrics.
- Related source: #62 returns active Student roster per directly owned course; #65 returns per-Student progress rows for active students over published lessons; #66 returns activity proxy counts/timestamp for one directly owned course. These do not directly supply the mockup’s global/student, average completion, rating or Capstone KPIs.
- Tests: API #46 test source was inspected for happy path, defaults, empty/out-of-range, auth, validation, DB/mapping errors and trace; tests were not run. Test doubles do not establish production schema or deployment. Database context records live schema `NOT_VERIFIED`.

## SOURCE_TRACE

```text
GET /api/v1/mentor/courses
  -> app/api/v1.py:mentor_courses
  -> MentorCourseQuery(status,page,size)
  -> api_46_mentor_courses.view.get_mentor_courses
  -> validate_current_user_request(role=MENTOR)
  -> validate status/page/size
  -> count_owned_courses + find_owned_courses
       -> same optional-status and direct courses.mentor_id predicates
       -> LEFT JOIN users; created_at DESC/id ASC; LIMIT/OFFSET
  -> map_course + CoursePage/Pagination
  -> success envelope 200 or safe 401/403/422/500
  -> focused API #46 test source inspected, not executed
```

GET has no write/commit/external side effect. API DD #46 is Draft and still says route/module/test are absent and Mentor guard is Student-specific; current route/module/guard/test source contradict that snapshot. AC-21’s assigned-course branch is not represented in the current direct-owner predicate. Related #62/#65/#66 APIs were source-traced only to evaluate mockup KPI/CTA fit; none was added to ME-02 expected orchestration.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Study Web route/session | No editable app source/package/router; only root `/` in ignored bundle. | UNWIRED | `/mentor/courses` is not runtime verified. |
| Course ownership | AC-21 says owned/assigned; #46 query only direct `courses.mentor_id`. | DISCREPANCY | Assigned courses may be omitted; don't infer assignment. |
| API #46 documentation | Current route/module/test source exists; API DD snapshot says `UNWIRED / NOT_FOUND`. | DISCREPANCY | Current source takes precedence; production deploy remains unverified. |
| Filters/search/sort | Mockup has course name/code search, active/upcoming/archived, level, term and student/progress/updated sort. #46 has only DRAFT/PUBLISHED status, page and size. | NOT_FOUND / DISCREPANCY | Do not send unsupported query values or fake client filters. |
| Mockup KPIs/card fields | Rating, capstone, course code/level, pending counts, students, lesson/lab counts, average progress absent from #46. #62/#65/#66 have different grain/definitions. | NOT_FOUND / DESIGN GAP | Sample values must not be represented as live data. |
| CTA handoff | Top create-lecture lacks courseId; ME-06/ME-09 actions differ from inventory links; report destination absent. | DISCREPANCY / BLOCKER | Need approved navigation/data handoff. |
| Status labels | UI labels cannot be mapped to current enum DRAFT/PUBLISHED. | SOURCE_REQUIRED | Do not serialize labels as API status. |
| Design/accessibility | Prototype uses remote Plus Jakarta Sans/Tailwind, #004ac6, 32–40px controls, 1440px max; Study guide targets Ocean #0B5F8A, Inter/system, >=44px controls and ~1120px content. | DESIGN DISCREPANCY | Resolve before frontend implementation. |

## CHANGES

- Files changed: `apps/study-client/docs/screen_stitch/04_mentor/ME-02_cac-khoa-hoc-phu-trach/ME-02_PLAN.md`, `ME-02_markers.json`, `ME-02_markers_overlay.svg`, `screen_annotated.png`, `ME-02.md`; `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; this worklog.
- Original `screen.png` and `code.html` were preserved; initial hashes are recorded above.
- CONTEXT_UPDATES: None. No source, API contract, database, skill/workflow or context page was changed.
- Context pages changed: None.
- Assumptions: None. Unsourced sample fields/routes remain documented as blockers.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Selector + selected-file review | Selected/read GS-01/GS-02/GS-03; 180 exact-type docs worklogs available, no shortage. | VERIFIED |
| ME-02 source/API trace | Plan written first; #46 route/guard/validation/query/map/response/errors and test source read; related #62/#65/#66 source read. Tests not run. | VERIFIED_SOURCE_REVIEW |
| Marker/artifact audit | Static audit: source hashes unchanged; source PNG 1100×1600 and annotated PNG 2200×3200; 47 sequential unique markers in JSON/overlay/DD, exact coordinate match with plan, no marker centers under 22 source px, 16 unique sequential event sections. Viewed final annotated PNG; markers remain legible and point to corresponding UI regions. | VERIFIED_STATIC |
| Link/whitespace/global progress audit | Python link audit found no broken relative links in ME-02 plan/DD, global plan or worklog; no trailing whitespace in those files; `git diff --check -- apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` clean; tracker row retains the three separate statuses and progress is 28/83. | VERIFIED |
| Context validator | No context pages/manifest changed; not required by router. | NOT_REQUIRED |
| Runtime/tests | No app/runtime verification and no tests run. | NOT_RUN |

## HANDOFF

- Screen status: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Worklog `VERIFIED` means the document/artifact/static audits completed; it does not mean DD READY or RUNTIME VERIFIED.
- Remaining blockers: ME02-B01–ME02-B10 in `ME-02.md`, especially assignment semantics, unsupported filters/KPIs and course-context route decisions.
- Next owner/action: ME-03, in a separate session; this session processes ME-02 only.
