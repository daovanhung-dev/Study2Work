---
task_id: "2026-11-07-design-study-screen-me17"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ME-17 student/course drill-down handoff from ME-16 through API #67; distinguish roster API #65 and analytics #66; compare AC-26 ordering and inventory links"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ME-17

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 204; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Preserve original assets and distinguish expected contract from current source; Study Web remains UNWIRED; tests/fake rows and checked-in schema do not prove live runtime/schema.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Do not infer routes, filters, cache or data mapping from prototype; inspect current server fields/errors; keep catalog/source discrepancies explicit and don't claim tests were run.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: One Screen ID per session; API source can exist while catalog/DD differs; preserve AC-26 vs inventory orchestration discrepancies; don't invent enrollment/auth/navigation policy.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ME-17 only this session; inspect and write its plan before any marker map/annotation/DD; preserve existing source assets; create sequential one-to-one markers, annotated image and A–F DD; update tracker and worklog; separate `DD READY`, `IMPLEMENTATION BLOCKED` and `RUNTIME VERIFIED`.
- Inventory row 57: ME-17 “Tiến độ từng học viên”, proposed route `/mentor/courses/:courseId/students/:studentId/progress`, AC-26, API #67; timeline of learning and missing assignments; both `course_id` and `student_id` are path IDs, server checks ownership; linked ME-16; expected states `loading/ready/denied/not-found`; current row remains `D`.
- Cross-screen contract: ME-17 follows ME-16 student selection and uses API #67 with both `course_id` and `student_id`; API #65 is course roster progress; API #66 is separate ME-18 analytics. AC-26 ordering must be compared without inferred reconciliation.

## CURRENT_BEHAVIOR

- Target folder contains only `screen.png` (1280×1266 RGBA; SHA-256 `ce7edffabc9e197410021ae40b43a8726104baa0e21578cf0cceedbb00624417`) and `code.html` (20,218 bytes; SHA-256 `a299cd075c5fcee09285bf9755e7768cd1b7a970f318f20cf24b09a773719d1c`). No plan/DD/markers/annotation existed. Both sources are unchanged.
- Study Web tree has docs/assets, ignored `dist` and `node_modules`, but no editable `src/` or `package.json`; registered subcontext remains `UNWIRED`.
- Screenshot is a static Mentor Student-detail mockup with profile sync copy, student ID “Chưa nạp”, enrollment-confirmed badge, course title, `0%`, last-send copy, project/quiz/self-study metrics, an empty Learning Timeline and three explanatory tiles. Most values/claims are not returned by #67.
- HTML is also a static empty-state prototype. It has 12 placeholder anchors (`href="#"`), a refresh button and a back button; no form, table, lesson rows, request or client route. Refresh only rotates `#syncIcon`, disables the button, waits 600 ms, then restores it. No API/fetch/polling exists.
- Local #67 route is `GET /api/v1/mentor/courses/{course_id}/students/{student_id}/progress`, both required signed-int64 paths, Authorization Bearer, shared `MENTOR` guard, no query/body. It checks direct course owner first, then requires the requested user in ACTIVE enrollment with role STUDENT, then returns PUBLISHED lessons ordered by `sort_order,id`. Duplicate progress chooses `last_accessed_at DESC NULLS LAST, id DESC`; missing row becomes `NOT_STARTED`/0/null timestamps. Summary is completed count and floor-average percent; denominator zero gives zero. It is read-only.
- Local #67 success is `ApiEnvelope<StudentCourseProgress>` with `course_id`, `student{id,full_name,avatar_url}`, `summary{completed_lessons,total_lessons,progress_percent}`, and `lessons[]` containing lesson ID/title/order/status/percent/access/completion timestamps. Errors are 401/403/404/500. Source maps bad IDs to 404, wrong course owner to 403, and missing/out-of-roster Student to 404.
- #67 catalog/AC direct response remains `ApiEnvelope<Page<Course>>`, conflicting with singular local progress response; API DD is Draft/Needs Confirmation and documents owner/ACTIVE-roster/PUBLISHED/formula/schema decisions as DERIVED. Checked-in legacy BIGINT schema and V1-PILOT UUID progress schema differ; live schema/deployment is not verified.
- API #67 test source has 25 focused HTTP cases for valid/empty progress, auth, path IDs, owner/roster, safe errors, invalid/duplicate projections, OpenAPI and trace; fake-DB tests were read, not run.

## SOURCE_TRACE

- Expected chain: inventory ME-16 → ME-17 with `course_id` + `student_id` → API #67. The AC-26 diagram instead sequences #65 → #66 → choose Student → #67; inventory assigns #66 separately to ME-18. Keep this as `DISCREPANCY`.
- Current chain: route in `app/api/v1.py` → shared MENTOR auth → signed-int64 parsing → course owner lookup → ACTIVE Student roster lookup → PUBLISHED lesson query/latest-progress projection → summary/model mapping → 200 envelope or safe 401/403/404/500. No DB mutation; no #65/#66 server-to-server call.
- Traced local query/model/view/validator, API #67 Draft DD/open questions, catalog row, AC-26 diagram, checked-in legacy DDL, context route/test/database pages and focused HTTP test names. #65 is a course roster summary; #66 is a course-wide current-state activity proxy, not an event ledger. Neither is merged into #67.
- Traced source screenshot and HTML. The visible empty timeline is not evidence of an event-history endpoint; local #67 returns current per-lesson state sorted by curriculum order. The mockup has no populated timeline row design.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| ME-17 assets and loaded timeline | Screenshot presents empty history; HTML has no lesson rows or loaded design. | DESIGN GAP | Don't invent populated timeline appearance/interaction from current-state API fields. |
| API #67 response | Catalog/AC says `Page<Course>`; local source returns derived singular `StudentCourseProgress`. | DISCREPANCY / DRAFT | Keep direct contract and local source separate; no approved screen mapping yet. |
| Student/course identity and privacy | Route requires two int64 IDs; API source requires direct owner and ACTIVE STUDENT roster; inventory hands off from ME-16. | DERIVED / BLOCKER | Handoff carrier, role policy, eligibility and 403/404 privacy require approval. |
| Mockup metrics and course context | Course title, enrollment badge, assignment/quiz/self-study metrics, last-send freshness and comment/milestone claims are absent from #67. | STATIC_ONLY / UNMAPPED | Do not invent fields or silently add #65/#66/other API calls. |
| AC-26 orchestration | Diagram places #66 before Student selection/#67; inventory puts #67 on ME-17 and #66 on ME-18. | DISCREPANCY | Preserve both; require flow-owner decision. |
| Schema/runtime | Legacy BIGINT source differs from V1-PILOT UUID schema; tests use fake DB; Study Web source absent. | UNVERIFIED / UNWIRED | No live DB/deployment/UI runtime claim. |

## CHANGES

- Tạo `ME-17_PLAN.md` trước marker map/DD; ghi expected/current behavior, #67 source trace, AC-26 discrepancy và blocker.
- Tạo `ME-17_markers.json`, `ME-17_markers.svg`, `screen_annotated.png` từ ảnh gốc; 39 marker bám từng visual element, đã dời khỏi text/control và xem ảnh kết quả.
- Tạo `ME-17.md` sections A–F, 39 element rows, EV-01…EV-04, source/API mapping, lỗi, states/navigation và unresolved decisions.
- Cập nhật row ME-17 và API #67 source classification D→R trong `list_screen.md`; cập nhật row ME-17, count 52/83 và phiên sử dụng trong `dd_screens/PLAN.md`.
- Giữ nguyên screen.png và code.html. Không thay đổi `.agents` context pages; context registry/architecture không đổi.
- Assumptions: không có. DD vẫn BLOCKED vì response shape và loaded timeline cần quyết định owner.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Objective reread; exact docs selector READY 3/204; GS-01, GS-02, GS-03 reviewed. | VERIFIED |
| Source asset hashes | screen.png `ce7edffabc9e197410021ae40b43a8726104baa0e21578cf0cceedbb00624417`; code.html `a299cd075c5fcee09285bf9755e7768cd1b7a970f318f20cf24b09a773719d1c`; unchanged. | VERIFIED |
| Marker/DD static audit | 39 sequential unique in-bounds markers; 39 element rows exact 1:1; JSON/XML parse; annotation 1280×1266; local Markdown links resolve; image visually reviewed. | VERIFIED |
| Artifact inventory | 83 screen folders, 52/83 with all four core artifacts after ME-17. | VERIFIED |
| `git diff --check` | Passed. | VERIFIED |
| Application tests/runtime | Not run; not requested. No runtime/live schema claim. | NOT_RUN |

## HANDOFF

- Remaining blockers: catalog Page<Course> vs local singular StudentCourseProgress; AC-26 ordering; ME-16 numeric-ID carrier; loaded timeline and empty semantics; unsupported mockup metrics; owner/eligibility/privacy and live-schema approval; Study Web UNWIRED.
- Session outcome: artifacts and trackers complete; `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`.
- Next screen for a separate session: ME-18. Do not start it in the ME-17 session.
