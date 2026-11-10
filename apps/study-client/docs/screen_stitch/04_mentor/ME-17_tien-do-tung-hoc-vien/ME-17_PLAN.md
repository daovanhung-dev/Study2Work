# ME-17 — Kế hoạch đặc tả màn hình Tiến độ từng học viên

## 1. Phạm vi

- **Screen ID:** ME-17 — Tiến độ từng học viên.
- **Task type/scopes:** `docs`; `web-work`, `server-study`.
- **Phiên này:** ME-17 only. ME-18 is not started.
- **Route đề xuất:** `/mentor/courses/:courseId/students/:studentId/progress` (inventory).
- **API chính:** #67 `GET /api/v1/mentor/courses/{course_id}/students/{student_id}/progress`.
- **Cross-screen dependency:** selected Student + course from ME-16. API #65 is the roster/course summary; #66 is a separate ME-18 activity analytics API. Do not combine the three responses.
- **Expected/current split:** inventory + AC/catalog are expected design evidence; current API source/test and prototype are current evidence. API #67 DD remains Draft/Needs Confirmation; source-backed does not mean contract approved, deployed, or live-schema verified.
- **Skill routing:** registry excludes `web-ui-only-dd` from `createDD-markdown`; this is UI-only DD and has no canonical skill, so no skill applies.
- **Source assets:** `screen.png` 1280×1266 RGBA, SHA-256 `ce7edffabc9e197410021ae40b43a8726104baa0e21578cf0cceedbb00624417`; `code.html` 20,218 bytes, SHA-256 `a299cd075c5fcee09285bf9755e7768cd1b7a970f318f20cf24b09a773719d1c`. Preserve both.

## 2. Expected behavior

- `list_screen.md` row 57: Mentor detail of one learner; AC-26; #67; next/previous relation to ME-16; expected states `loading/ready/denied/not-found`; timeline and missing learning items.
- `list_api.md` and AC-26 diagram declare both required path params `course_id:int64`, `student_id:int64`; Bearer JWT / Mentor; GET with no request body; success `200 DESIGN_RESOURCE_RETRIEVED`; errors 401/403/404/500; response `ApiEnvelope<Page<Course>>`.
- AC-26 sequence is dashboard → #65 course progress → aggregate enrollment/progress → #66 analytics → aggregate learning events → choose Student → #67 Student progress → read progress → render dashboard + drill-down. The screen inventory instead places #67 on ME-17 linked from ME-16 and #66 on separate ME-18. This is a `DISCREPANCY`; keep both statements and ask the flow owner to resolve.
- Expected handoff requires both numeric IDs. ME-16's local #65 row can contain `student.id`, but its direct catalog response differs from local response and its prototype has no rows/action. No approved route carrier or selection behavior is known.

## 3. Current behavior and source trace

### 3.1 Study Web and assets

- Rechecked `apps/study-client/`: docs/assets, ignored `dist`, and `node_modules` exist; editable `src/` and `package.json` are absent. Registered Study Web subcontext is `UNWIRED`; the compiled bundle is not evidence of a feature route/runtime.
- Screenshot is a static empty-timeline view. It contains Mentor header/profile, breadcrumb, green “giám sát trực tiếp” label, detail title, cosmetic refresh, “Đang đồng bộ hồ sơ…”, “Mã học viên: Chưa nạp”, enrollment-confirmed badge, course name, 0% progress, last-send status, assignment/quiz/self-study metrics, empty timeline and three explanatory tiles.
- HTML has placeholder anchors, one refresh control and one back-to-course-progress link. It has no data/API call, route binding, student ID source, loaded lesson timeline rows, table/form or empty/error/loading state machine. The only handler rotates the refresh icon and disables it for 600 ms.
- Static screen claims such as course title, enrollment confirmation, assignment and quiz counts, self-study hours, last send time, historical event sync, comments, milestone completion, real-time monitoring, and WCAG copy lack #67 data/source.

### 3.2 API #67 current local source

- Route: `GET /api/v1/mentor/courses/{course_id}/students/{student_id}/progress`. Both raw path values parse as signed int64; the route declares both required in OpenAPI. No query/body/page-size.
- Shared Bearer/JWT guard requires role `MENTOR` before DB. Course existence/ID is checked first; direct owner mismatch returns 403. Then the requested user must be in an `ACTIVE` enrollment and have `users.role='STUDENT'`; otherwise 404.
- Query returns only `PUBLISHED` lessons for the course, ordered `sort_order ASC, id ASC`. Duplicate `(user_id,lesson_id)` progress rows choose `last_accessed_at DESC NULLS LAST`, then `id DESC`. An absent row becomes `NOT_STARTED`, percent `0`, null timestamps.
- Local response is singular `ApiEnvelope<StudentCourseProgress>`: `course_id`; `student{id,full_name,avatar_url}`; `summary{completed_lessons,total_lessons,progress_percent}`; `lessons[]{lesson_id,title,order,progress_status,progress_percent,last_accessed_at,completed_at}`. Summary is `completed` count and `floor(sum(percent)/published_lesson_count)`; empty lesson set yields 0. It is read-only and does not call #65 or #66 server-to-server.
- Local errors are 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`; malformed/out-of-range paths follow local source and become 404. Ineligible Student and absent course are 404; wrong course owner is 403.
- Catalog/diagram still declare `ApiEnvelope<Page<Course>>`; API #67 DD is Draft/Needs Confirmation. Singular response, direct-owner rule, active roster, PUBLISHED scope, formula, default status and latest-row policy remain DERIVED/open questions. Fake DB tests exist; they do not prove live schema/deployment.
- Local #67 fields cannot directly supply the static course name, enrollment confirmation, assignment/quiz metrics, self-study hours, event history, mentor comments, project milestones or “last sent” freshness shown in the screenshot.

## 4. Candidate marker coverage

Plan **39 sequential markers** for every distinct visible control/content block. Decorative icon pieces are grouped with the component they label; independent links/buttons receive their own IDs.

1. Header brand; 2–6. five Mentor navigation links; 7. notification bell; 8. Mentor identity.
9–10. breadcrumb link and current breadcrumb.
11. live-monitoring eyebrow; 12. page title; 13. refresh button.
14. student profile icon/heading; 15. student-code label/value; 16. enrollment-confirmed badge.
17. course title; 18. course progress percent/bar; 19. last-data-send metric.
20. monitoring panel heading/decorative tune glyph; 21–23. assignment, quiz, self-study metric rows; 24. monitoring note.
25. timeline heading; 26. phase label; 27. empty-state illustration; 28. lock badge; 29. empty-state heading; 30. description; 31. back-to-course-progress action.
32–34. lesson/video, Mentor-comment and project-milestone tiles.
35. footer mark; 36. footer copyright/standards copy; 37–39. three footer links.

Use centers from the 1280×1266 original PNG, keep circles inside image bounds and place them beside text/control edges. Visually inspect after rendering and move any marker that covers important copy or controls. Preserve original `screen.png`; create annotation as a separate output.

## 5. Events to specify

1. **EV-01 Load detail:** two required route IDs and Mentor auth; candidate #67 GET; map source fields only after direct-vs-local response approval. Handle 401/403/404/500 and empty published lessons separately; no cache/retry/freshness policy is declared.
2. **EV-02 Refresh connection:** current click is only a 600 ms cosmetic rotation. If a real refresh is approved, repeat #67 for the same IDs; request/response contract still conflicts and no network call currently occurs.
3. **EV-03 Back to course progress:** anchor `href="#"`; inventory points to ME-16, but destination, history/route carrier and safe course ID mapping are not wired.
4. **EV-04 Header/breadcrumb/footer navigation:** all anchors use `href="#"`; record placeholders without inventing destinations.
5. **No lesson-row click event:** screenshot and HTML have no loaded lesson rows/actions. Do not invent a further Student, assignment, quiz, discussion or mentor-note route.

## 6. Blockers and status criteria

- `Page<Course>` direct contract conflicts with the singular local #67 response; the API DD asks for approval.
- No approved ME-16→ME-17 selected-row carrier; ME-16 #65 local response also differs from its direct contract.
- Timeline loaded state is absent. Current #67 is a per-lesson state snapshot ordered by curriculum, not chronological event history; it does not supply assignment, quiz, study-hour, comment or project-milestone data.
- Screenshot claims/fields have no source mapping; no additional API may be invented or merged from #65/#66.
- Direct-owner vs assigned Mentor, active-roster eligibility, 403/404 privacy, formula/default statuses, latest duplicate selection, pagination bound, and legacy BIGINT vs V1-PILOT UUID live schema are unresolved.
- Study Web feature route/client/runtime is absent. Do not claim `RUNTIME VERIFIED`.
- Final DD status should remain **DD BLOCKED** if the owner must still define the loaded timeline or approve response/mapping decisions; mark **IMPLEMENTATION BLOCKED** independently. Use `DD READY` only if every unresolved choice is explicitly outside implementation scope and the spec can be implemented without guessing.

## 7. Order of work and verification

1. [x] Write this plan before marker/DD creation.
2. [x] Create `ME-17_markers.json`, SVG overlay and `screen_annotated.png` from the unchanged PNG; review marker placement visually.
3. [x] Write `ME-17.md` sections A–F with 39 elements, recognized events, input/process/output/API/errors, state/navigation, trace links and named blockers.
4. [x] Update ME-17 inventory and global plan rows, the 83-screen artifact count and this worklog.
5. [x] Static audit JSON sequence/bounds, one-to-one marker/element mapping, source hashes, dimensions, links, visual annotation and `git diff --check`. Application tests/runtime were not run.
6. [x] Stop after ME-17; do not start ME-18.

**Outcome:** `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.

## 8. Sources

- `apps/study-client/docs/list_screen.md` — ME-17 row/F10 flow.
- `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` — global ME-17 row and progress.
- `apps/study-client/docs/screen_stitch/04_mentor/ME-16_tien-do-toan-khoa-hoc/ME-16.md` — preceding screen's candidate #67 handoff and unresolved #65 response.
- `apps/study-client/docs/screen_stitch/04_mentor/ME-17_tien-do-tung-hoc-vien/{screen.png,code.html}` — original design/prototype.
- `apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio` and `docs/lists/list_api.md` — AC-26 sequence/API contract.
- `apps/study-server/app/api/v1.py`, `app/modules/mentor/api_67_mentor_student_progress/`, `apps/study-server/docs/dd/67_mentor_student_progress/`, `apps/study-server/tests/modules/mentor/api_67_mentor_student_progress/test_mentor_student_progress.py` — current route, local fallback, unresolved contract and test source.
- `.agents/web-work/study/`, `.agents/web-study/design.md`, `.agents/server-study/{AGENTS.md,INDEX.md,database.md,tests.md}` — scoped runtime/design/test boundaries.
