# ST-17_PLAN — Chi tiết bài tập

> **Trạng thái:** PLAN COMPLETE; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED

## 1. Phạm vi và phân loại

- Phiên này chỉ xử lý **ST-17 — Chi tiết bài tập**; không bắt đầu ST-18.
- `primary_task_type: docs`; `secondary_task_types: []`; `project_scopes: [web-work, server-study]`.
- Cross-scope dependencies: Study Web route → Study API #33; AC-17 assignment/deadline decision; ST-17 → ST-18 submission handoff; ST-09 course context.
- Inventory: proposed route `/student/assignments/:assignmentId`, actor Student, AC-17, API #33, related ST-18/ST-09, expected states `loading/open/closed/not-found`. GET #33; server must determine deadline/permission, not a client clock.
- API #33 contract: `GET /api/v1/assignments/{assignment_id}`, Student Bearer, `assignment_id:int64` path only, no query/body; `ApiEnvelope<Assignment>`; success 200 `DESIGN_RESOURCE_RETRIEVED`; errors 401/403/404/500. API #33 DD is `Draft — Needs Confirmation`; current Student route/module/test is absent.
- The machine-readable skill registry excludes `web-ui-only-dd` from `createDD-markdown`; no canonical UI-only screen DD skill applies.

## 2. Asset baseline and source state

- `screen.png`: 667×1600 RGB; SHA-256 `7ac187345ca89ef08462767a6269e91af888944d4a8b76494896596e1f6c7c86`.
- `code.html`: 9,745 bytes; SHA-256 `82de50d864c0be013a198358a1f41de72acf032d18add1107114eb07c76580f6`.
- PNG shows a loaded Student assignment mockup with status/title/progress/deadline/mentor/SLA, video preview, brief, four objectives, four rubric rows, three attached resources, submission instructions/checklist, mentor contacts, submission history and a submit CTA. Visible IDs, course/assignment content, date/countdown, points, progress, resource names/files, mentor and contact values are sample design content.
- HTML is a different static Guest unavailable state with login/register header, generic “not ready” message and link `/student/courses`; it has no assignment route binding, API call, form or submission behavior. Preserve both source assets; do not treat either as runtime evidence.
- Current Study Web has no editable app source/package manifest or Student route. Current Study Server has no Student API #33 route/module/test. Current Mentor APIs #54–#57 are separate submission operations and do not implement #33.

## 3. Contract expectations, source limits and blockers

- AC-17 sequence: open assignment → GET #33 → read Assignment + “submission rule” → deadline/permission decision → if allowed, input/file → #34 upload → object storage → #35 submission create → #36 submission read/confirmation. The error branch is 403/409 for overdue/no permission; #33 catalog does not include 409.
- Reusable `Assignment` has only `id`, `course_id`, `title`, optional `description`, optional `due_at`, and `max_score`. It has no submission status/history, course title, course weight/progress, rubric, resource files, preview video, mentor/SLA, checklist state or policy fields.
- API #33 DD Q-33-01…05 leave access/403-vs-404; deadline read/rejection/boundary and 403-vs-409; submission-rule schema; nullability/timezone/decimal serialization; and path parsing/error mapping unresolved.
- Checked-in DDL candidate `assignments` has nullable `course_id`, nullable `max_score` (default 10), `name` instead of logical `title`, nullable `due_at TIMESTAMP` without timezone. Logical API contract requires `course_id` and `max_score`. DDL is not live schema evidence.
- Do not add #34/#35/#36 calls to ST-17. The submit CTA may hand off `assignmentId` to the proposed ST-18 route only after the server allows it and route handoff is approved. No route, download, checklist persistence, contact action or submission history behavior is inferred from the screenshot.

## 4. Element and marker plan

Create sequential markers `#1–#49`, each mapped exactly once to `ST17-EL-01`…`ST17-EL-49` in the DD element table. Keep badges in white gutters, align each badge to its target row, avoid badge overlap, and preserve all screenshot content. In `ST-17_markers.json`, `x/y` are source-image coordinates and `badge_x/badge_y` are annotation-canvas coordinates.

1. Header Study2Work logo/brand.
2. Header primary navigation group.
3. Notification control.
4. Student avatar/name/profile control.
5. Breadcrumb trail.
6. Assignment state/code/project-category chips.
7. Assignment title.
8. Assignment summary/description.
9. Progress and total/max-score panel.
10. Due-date summary.
11. Time-remaining summary.
12. Assigned mentor stat.
13. Review SLA stat.
14. Video preview card/title.
15. Section 1 heading and core-requirement introduction.
16–19. Four individual core objective cards: Virtualization & Rendering; server-side filtering/debounce; RBAC; dynamic UI.
20. Rubric heading, total score and “4 skill axes” summary.
21–24. Four individual rubric criteria A–D with their displayed score/value.
25. Attached-resources heading and introduction.
26. Starter Kit download row/action.
27. Figma specification row/action.
28. API mock-data row/action.
29. Submission requirements heading and introduction.
30. GitHub repository delivery requirement.
31. Vercel live preview requirement.
32. Technical PDF report requirement.
33. Late-submission penalty note.
34. Submission status card (“Chưa nộp bài”).
35. Deadline countdown block and displayed deadline.
36. “Soạn và Nộp bài tập ngay” CTA.
37. Pre-submit checklist heading and completion count.
38–41. Four individual pre-submit checklist lines.
42. Academic-integrity/commitment note.
43. Mentor profile image/name/role.
44. Mentor biography.
45. Discord support action.
46. Mentor office-hours action.
47. Submission history row/count.
48. Footer brand/description/certification badges.
49. Footer navigation/legal links.

## 5. Events and data flow to specify

1. **ST17-EV-01 — Open assignment detail:** route-load, Student context, `assignmentId`, single GET #33; include Bearer/path-only request, envelope mapping, 401/403/404/500 and no current route/runtime.
2. **ST17-EV-02 — Map Assignment response:** bind only approved `id`, `course_id`, `title`, `description?`, `due_at?`, `max_score`; keep course title, project progress/weight, submission status, rubric, resources, video, mentor/SLA/history as unsourced.
3. **ST17-EV-03 — Display deadline/status:** distinguish visual countdown from server-side eligibility; timezone, deadline boundary and whether #33 rejects after due time are open. Do not enable/deny submission based only on local time.
4. **ST17-EV-04 — Pre-submit checklist:** screenshot shows four checkbox-like lines; semantics, ownership, state persistence and effect are undefined. Do not treat local toggles as submission validation or persist them without approval.
5. **ST17-EV-05 — Open resource/video/support links:** screenshot actions lack URL/file/entitlement/destination contracts. Do not invent download endpoints or external contact routes.
6. **ST17-EV-06 — Continue to submission (ST-18):** when approved server state permits, pass `assignmentId` to proposed ST-18; do not upload, submit, or call #34/#35/#36 from this detail event.
7. **ST17-EV-07 — Global navigation and failure states:** keep prototype anchors separate from current routes; handle catalog errors and network/malformed response without treating screenshot samples as success. AC-17 409 remains a contract discrepancy.

## 6. State, navigation, acceptance and verification plan

- Target state flow from inventory: `loading → open | closed | not-found`; add access-denied/error states for catalog/runtime failures. Exact mapping of due/permission to #33 response remains blocked.
- Navigation: preceding assignment list/course context is not identified as an ST-17 route in the inventory; related ST-09 is not automatically a breadcrumb/CTA destination. The CTA relates to ST-18 and should hand off `assignmentId` only under approved route policy.
- Accessibility target follows `.agents/web-study/design.md`: semantic links/buttons, keyboard/focus, accessible names for icon actions, non-color status cues, responsive reflow/reduced motion. This is intended design, not current runtime.
- Static verification after authoring: preserve original hashes/dimensions; verify all 49 markers are ordered, in-bounds, non-overlapping and map one-to-one to DD; parse SVG; verify annotated image dimensions/visual legibility; check local links, inventory/folder count, tracker totals/next pointer and `git diff --check`. Do not run tests or claim runtime.
- Blockers: API #33 route/module/test absent; access/deadline/submission-rule/error mapping unresolved; response cannot support most loaded-screen content; image/HTML state/actor mismatch; Study Web UNWIRED.

## 7. Sources

- [Screen inventory, AC-17 flow and G-09](../../../list_screen.md)
- [Original screenshot](./screen.png), [HTML companion](./code.html)
- [API catalog #33 and Assignment schema](../../../../../../docs/lists/list_api.md)
- [AC/API index](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-17 activity diagram](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio)
- API #33 DD: [overview](../../../../../../apps/study-server/docs/dd/33_assignments_detail/02_Overview.md), [request](../../../../../../apps/study-server/docs/dd/33_assignments_detail/03_Request.md), [response](../../../../../../apps/study-server/docs/dd/33_assignments_detail/04_Response.md), [mapping](../../../../../../apps/study-server/docs/dd/33_assignments_detail/05_Data_Mapping.md), [errors](../../../../../../apps/study-server/docs/dd/33_assignments_detail/06_Error.md), [open questions](../../../../../../apps/study-server/docs/dd/33_assignments_detail/OPEN_QUESTIONS.md)
- [Candidate assignment DB design](../../../../../../apps/study-server/docs/diagrams/DB_UNICA_TABLES.md), [legacy candidate DDL](../../../../../../infra/postgres/study-server/DB.sql), [V1-PILOT schema artifact](../../../../../../infra/postgres/02_study_db.sql)
- [Current Study route inventory](../../../../../../.agents/server-study/apis/declared-routes.md), [Study Web status](../../../../../../.agents/web-work/study/INDEX.md), [Study Web design target](../../../../../../.agents/web-study/design.md)

## 8. Re-audit trước khi cập nhật DD/tracker (2026-11-07)

- Rechecked ST-17/ST-18/ST-19 inventory rows, F06, AC-17 API index and the AC-17 page in `AC_02_STUDENT_LEARNING.drawio`. AC-17 is Student-facing; its expected sequence is GET #33 assignment/rule → deadline/permission decision → optional #34 upload → #35 submission create → #36 receipt. The diagram’s `403/409` overdue/no-permission branch conflicts with #33 catalog’s 401/403/404/500 set.
- Rechecked API catalog #33 and API #33 Draft DD (`02_Overview`, `03_Request`, `04_Response`, `05_Data_Mapping`, `06_Error`, `OPEN_QUESTIONS`, `VERIFICATION_REPORT`). Contract remains GET `/api/v1/assignments/{assignment_id}`, Student Bearer, required int64 path only, `ApiEnvelope<Assignment>`, 200 `DESIGN_RESOURCE_RETRIEVED`, errors 401/403/404/500. Q-33-01…05 remain open for access/403-vs-404, deadline/error mapping, submission-rule schema, nullability/timezone/decimal serialization, and path validation. The logical Assignment schema is still `id`, `course_id`, `title`, optional `description`, optional `due_at`, `max_score`.
- Current source search finds no #33 GET route, Student #33 module or test. The Student module tree contains API #34 uploads; APIs #54–#57 are Mentor submission flows and are not the Student #33/#35/#36 contract. Current API #34 is `POST /api/v1/uploads`, supports purpose `SUBMISSION` and returns an UploadAsset ID; it does not download resources or create a submission. No Student #35/#36 route/module/test was found. Study Web editable source/package manifest is absent, ignored `dist` has no assignment route string, and the subcontext remains `UNWIRED`.
- Database sources disagree: legacy Study Server `DB.sql` and DB table notes contain BIGINT `assignments`/`assignment_submissions` candidates; `assignments.course_id`, `max_score` are nullable, `due_at` is timestamp without timezone, and physical `name` maps to logical `title`. The V1-PILOT `02_study_db.sql` has no business `assignments` or `assignment_submissions` tables (its `service_role_assignments` is a different identity table). No live schema or #33 adapter is verified.
- Asset recheck: `screen.png` remains 667×1600 with SHA-256 `7ac187345ca89ef08462767a6269e91af888944d4a8b76494896596e1f6c7c86`; `code.html` remains 9,745 bytes with SHA-256 `82de50d864c0be013a198358a1f41de72acf032d18add1107114eb07c76580f6`. PNG is a loaded Student assignment-detail mockup; HTML is Guest/unavailable with login/register and a course-list link, with no route state or API. The PNG is dense at its 667px source width; HTML imports remote Plus Jakarta Sans/Material Symbols and Tailwind CDN and uses a 1440px max width. This conflicts with Study Web guidance (system font without remote import, ~1120px max width, mobile reflow below 768px, 44px controls). Keep source assets unchanged and record the visual/system mismatch as a blocker.
- Existing annotation audit before DD edits: source target 667×1600; annotated image 1718×3200 from canvas 859×1600 at 2×; 49 sequential markers, 49 DD element rows and 49 SVG groups; all target/badge coordinates unique and in bounds; SVG badge centers match JSON; 22 DD links and 17 plan links resolve. Raw and annotated images were inspected; gutter markers do not cover content.
- Planned edits: update ST-17 DD with the V1-PILOT/legacy model gap and design-target mismatch; clarify the related #34/#35/#36 status at the screen handoff; update only the ST-17 inventory row and global tracker row, plus F06’s verified assignment API handoff status; complete the ST-17 worklog. No ST-18/ST-19 screen DD/tracker row, API DD, DDL, or other Screen ID will be edited. No application tests/runtime/live DB check.
- Post-edit static audit: A–F sections and seven events remain present; 49 marker IDs match 49 `ST17-EL-01`…`49` rows and 49 SVG groups; every badge center matches JSON, source targets are unique/in bounds, and nearest badge centers are 26px apart versus a 25.5px outer circle diameter. Final local links resolve (DD 25, plan 18); inventory/folders remain 83/83 with 82 complete six-artifact bundles (only ST-01 incomplete; ST-17 complete). `screen.png` and `code.html` fingerprints are unchanged; annotated image remains 1718×3200. Scoped `git diff --check` passed. `node scripts/validate-agent-context.mjs` exits 1 with repository-wide missing db-admin context/source roots and stale manifests for db-admin, mobile-work, server-study, server-work, web-work and web-work/work-web; output does not mention ST-17. Application tests, app runtime and live DB were not run.
