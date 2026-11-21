# ME-18 — Kế hoạch đặc tả màn hình Phân tích khóa học

## 1. Phạm vi và trạng thái preflight

- **Screen ID:** ME-18 — Phân tích khóa học.
- **Task type/scopes:** docs; web-work, server-study.
- **Phiên:** ME-18 only; do not start another Screen ID.
- **Expected route:** /mentor/courses/:courseId/analytics (inventory proposal, not wired).
- **Expected API:** #66 GET /api/v1/mentor/courses/{course_id}/analytics.
- **Cross-screen dependency:** ME-16 course context and API #66; preserve ME-16 inventory navigation versus AC-26 ordering (#65 → #66 → select Student → #67). Keep #65, #66 and #67 separate.
- **Skill selection:** manifest targets createDD-markdown to API DD and explicitly excludes web-ui-only-dd. This deliverable is screen UI DD; no canonical skill applies.
- **Source assets:** screen.png 1600×1380 RGB, SHA-256 8141f4a9670d5a41a82016613928a6abbbfd82ad50bc84049645cbe2a565bb8f; code.html 17,676 bytes, SHA-256 45bc8a7c267a2de2c73a1bedc9b170620334f29b4fe1f89a2e3cd7bd7d367564. Preserve both.

## 2. Expected behavior

- list_screen.md row 58 names ME-18 “Analytics khóa học”, route /mentor/courses/:courseId/analytics, AC-26 and API #66. It expects course performance/completion charts from backend KPIs; metric definitions, period and aggregation remain TBD. Expected states are loading/no-data/ready/error; ME-16 is the linked predecessor.
- API catalog and AC-26 directly declare a Mentor Bearer GET with required course_id:int64, no request body, success 200 DESIGN_RESOURCE_RETRIEVED, errors 401/403/404/500, response ApiEnvelope<Page<Course>>.
- The AC-26 diagram sequences #65 course progress → #66 aggregate learning events → select Student → #67 student progress → render dashboard/drill-down. Inventory instead links ME-16 to both ME-17/#67 and ME-18/#66. Record DISCREPANCY without reconciling.
- ME-16 DD includes an analytics placeholder link but explicitly says not to fetch #66 from ME-16 without an approved ordering and numeric course_id carrier.

## 3. Current behavior and source trace

### 3.1 Screen assets and Study Web

- screen.png presents a Mentor shell, course breadcrumb/title/code, semester and “Chờ đồng bộ dữ liệu” labels, analytics title/description, disabled time-window selector and CSV export, three empty KPI cards, inactive analytics panel, back-to-ME-16 and check-sync controls, two compliance/readiness claims, and footer.
- code.html contains 13 href="#" anchors, a disabled select with 7-day/30-day/all-course choices, and a disabled export button. The check-sync button has inline JS only: “Đang gửi lệnh...” for 1.2 seconds, then “Đã ghi nhận yêu cầu” for 3 seconds, then restores the button. No fetch/Axios/XHR, chart data, route, or export request exists.
- Study Web has no editable src/package manifest/feature route; compiled dist is not evidence of a working screen. Status remains UNWIRED.
- Course name/code, term, ETL/telemetry readiness, completion rate, average duration, discussion interactions, CSV export, WCAG 2.1 AA compliance and “Schema v2.4 Analytical Ready” are static claims without a mapping from API #66.

### 3.2 API #66 current local source

- Route: GET /api/v1/mentor/courses/{course_id}/analytics. Required signed-int64 path and Authorization header; no query/body/page-size.
- Shared Bearer/JWT guard requires role MENTOR before DB. The raw path is parsed as signed int64; malformed/out-of-range → 404 DESIGN_RESOURCE_NOT_FOUND. Course absence → 404; direct-owner mismatch → 403 before aggregate.
- Aggregate SQL repeats the owner predicate and counts distinct (user_id, lesson_id) pairs with non-null lesson_progress.last_accessed_at, for PUBLISHED lessons and users.role=STUDENT. It does not check ACTIVE enrollment.
- Local response is a DERIVED ApiEnvelope<MentorCourseActivityAnalytics>: tracked_lesson_accesses, students_with_activity, last_activity_at. Empty proxy is 0, 0, null. It is a current-state all-time proxy, not event count/history; repeated accesses may have been overwritten. Read-only; no call to #65/#67.
- Direct catalog/AC response remains ApiEnvelope<Page<Course>>, which has no analytics fields. API #66 DD is Draft — Needs Confirmation. The focused tests use fake DB data and do not prove live schema/deployment.
- Current response fields do not represent the mockup KPIs or a time-window filter. The local API does not provide CSV export or ETL activation state.

## 4. Candidate marker coverage

Plan 35 sequential markers; combine decorative icon/text inside the component they identify and give independent anchors/buttons their own IDs.

1 brand; 2–6 five header navigation links; 7 notification bell/unread dot; 8 Mentor identity/profile.
9 breadcrumb course-list link; 10 course-title/code link; 11 current breadcrumb.
12 semester badge; 13 course sync-state label; 14 page title; 15 subtitle.
16 timeframe label; 17 disabled timeframe select/options/lock; 18 report-task label; 19 disabled CSV export.
20 completion-rate KPI card; 21 average-duration KPI card; 22 discussion-interaction KPI card.
23 empty analytics illustration; 24 inactive-analysis status badge; 25 empty-state heading; 26 explanatory copy; 27 back-to-ME-16 link; 28 check-sync button; 29 WCAG badge; 30 schema-readiness badge.
31 footer mark; 32 footer copyright/standards copy; 33–35 footer links.

Use centers on the original 1600×1380 PNG. Keep markers beside controls/text, especially the three KPI card contents, disabled control labels, empty-state heading, and bottom compliance row. Visually review before accepting the overlay.

## 5. Events to specify

1. **EV-01 Load analytics:** route courseId + Mentor auth; candidate #66 call only after numeric ID carrier, response contract and metric mapping are approved. Specify exact request/error shape. Map only approved fields; do not treat proxy counts as events or any mockup KPI.
2. **EV-02 Time-window selection:** current selector is disabled and has no handler; options are 7 days, 30 days, all course. No API query or local filtering can be specified. Record no event until product/API contract defines period semantics.
3. **EV-03 Export CSV:** button is disabled. No API/file generation/download exists; record non-action rather than invent an export flow.
4. **EV-04 Check sync:** current inline timer changes button markup for 1.2 s then shows “request recorded” for 3 s and restores original copy. No API/network/state update. Any future refresh/ETL trigger needs a separate approved contract.
5. **EV-05 Back to ME-16:** href="#" placeholder; expected predecessor is ME-16, but route and int64 course ID carrier are not wired.
6. **EV-06 Header/breadcrumb/footer navigation:** all anchors use href="#"; data-path is prototype metadata only. No destination/API may be invented.

No chart hover/drill-down, KPI-card click, download, timeline, data timer or automatic polling exists in the source asset.

## 6. Blockers and status criteria

- Catalog/diagram Page<Course> conflicts with local summary response.
- Inventory does not define KPI names/formulas, time window, aggregation, no-data meaning or export contract; #66 cannot populate completion/average-duration/discussion KPIs.
- AC requests learning-event aggregation while current-state lesson_progress cannot recover event history.
- Course ID carrier and ownership policy (direct owner versus assigned Mentor) are not resolved; Study Web route/auth/client remains UNWIRED.
- “Inactive ETL” and “ready schema” claims have no API/source fields; zero/null summary cannot identify a pipeline status.
- Do not claim DD READY while response/KPI/period/loaded visual choices require product/API decisions. Expected result is DD BLOCKED and IMPLEMENTATION BLOCKED, independently of RUNTIME NOT VERIFIED.
- Verification is static only: preserve source hashes, check 35 marker IDs/order/bounds and one-to-one DD rows, parse JSON/SVG/PNG, resolve local links, inspect annotated image, update trackers/worklog and run git diff --check. Do not run application tests/runtime.

## 7. Plan order

1. [x] Complete docs worklog preflight and read three selected docs logs before deep inspection.
2. [x] Load required context and trace ME-18 expected/current sources before authoring.
3. [x] Write this plan before marker map, annotation or DD.
4. [x] Create 35-marker JSON/SVG and screen_annotated.png from unchanged screen.png; inspect visually.
5. [x] Write ME-18.md sections A–F, including element/event/API/error/state/navigation trace and unresolved decisions.
6. [x] Update ME-18/list_screen/global PLAN rows, recompute 83-screen artifact count, complete worklog and static audit.
7. [x] Stop after ME-18; no next Screen ID in this session.


**Outcome:** DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED.
