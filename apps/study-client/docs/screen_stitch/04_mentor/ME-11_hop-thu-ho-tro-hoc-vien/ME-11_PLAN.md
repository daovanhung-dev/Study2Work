# Kế hoạch Detailed Design — ME-11

> **Plan status:** COMPLETE — được viết trước marker map, ảnh chú thích và DD; artifacts đã tạo và static-audit.
> **Screen status dự kiến sau audit:** `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
> **Phạm vi phiên:** chỉ Screen ID **ME-11**.

## 1. Phân loại, phạm vi và nguồn

```text
primary_task_type: docs
secondary_task_types: []
project_scopes:
  - web-work
  - server-study
cross_scope_dependencies:
  - ME-01 → ME-11 GET #58 → ME-12 requestId handoff / GET #59; #60 reply and #61 resolve belong to ME-12
```

- Goal objective: `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md`; task classification, worklog selector and selected worklogs: [ME-11 worklog](../../../../../../.agents/worklog/2026-11-06/design-study-screen-me11.md).
- Screen requirement: [ME-11 row and F09](../../../list_screen.md); [UC24 “Hỗ trợ học viên”](../../../../../../docs/diagrams/UC_UNICA.drawio); [AC-24 activity/API flow](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio); [AC/API index](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md).
- API contract evidence: `docs/lists/list_api.md` #58; Study API #58 DD files under `apps/study-server/docs/dd/58_mentor_support_requests/`, including `OPEN_QUESTIONS.md` and `VERIFICATION_REPORT.md`. API DD remains `Draft — Needs Confirmation`; derived local fallback decisions are not approved contract.
- Visual inputs: `screen.png` 1600×1425, SHA-256 `2cbdc3691a241ee755ce6f422768472c943ddb352554f9ed9159df1cd5105272`; `code.html` SHA-256 `54536f7794787f3c93772c54805c42712f2339434a4c7f58fd3611925b64b2d5`. Preserve both source files.
- Current implementation evidence: Study Web has documentation/assets and an ignored `dist` bundle only; editable app source/package/router are absent (`UNWIRED`). #58 route/view/query/models and focused test source exist in Study Server. `.agents/server-study/tests.md` records a historical focused result of 12 passes using fake sessions; tests are not run in this docs session.
- Schema evidence: checked-in `infra/postgres/study-server/DB.sql` and `migrations/008_support_requests.sql` contain the legacy BIGINT support tables. This corrects the stale inventory claim that `support_requests` is absent. These artifacts and temporary-branch test history do not verify production schema or migration deployment.
- Skill routing: `.agents/context-manifest.json` marks `createDD-markdown` as Web/API DD and excludes `web-ui-only-dd`; no canonical screen-level UI DD skill applies.
- Design target: `.agents/web-study/design.md` is intended guidance only. The source mockup uses a different bright-blue palette and external Tailwind/Google Fonts references; no UI runtime or responsive behavior is established.

## 2. Mục tiêu và điều kiện nghiệm thu

Tạo một DD truy vết đầy đủ cho ME-11’s visible empty state: sequential one-to-one markers, A–F screen specification, API #58 request/response/error mapping, event/state/navigation matrix, privacy/accessibility notes, open decisions and source links. Keep current source behavior separate from AC/inventory expectations.

Do not invent a loaded-row layout, course option values, “Open” status grouping, counts, SLA clock, real-time notifications, canned replies or external meeting flow. The screenshot contains no request rows. Because the primary ready state is not designed and several contract mappings remain unresolved, this plan expects the screen to remain `DD BLOCKED` after static audit even if its empty-state artifacts are complete.

## 3. Expected behavior

1. Mentor enters proposed `/mentor/support` from ME-01 or an approved direct route.
2. AC-24 starts with GET #58, restricted to requests belonging to courses in the Mentor’s responsibility scope.
3. Optional course/status filters may be sent only with confirmed option-to-query mapping. Inventory expects All/Open/Resolved tabs and a course selector.
4. An empty collection renders the empty state. A selected request passes its `data[].id` as `requestId` to ME-12; #59/#60/#61 are not called by ME-11 itself.
5. AC-24’s precondition says the Mentor already has an in-scope request, while the screenshot/inventory require an empty state. Keep the discrepancy open until product confirms whether that precondition applies only to the detail/reply flow.

## 4. Current behavior and source trace to preserve

- Screenshot: empty inbox; all/open/resolved counters are sample zeroes; course options are sample titles with slug values; visible claims include `<4 giờ`, “Vừa cập nhật tức thì”, automatic real-time notifications, standard response guidance, and Google Meet support.
- HTML: no request rows and no API call. Tab clicks only update selected styling/ARIA; course select has no change handler; refresh runs a local 650ms spinner and updates the browser clock; header/footer anchors use `#`. The prototype references Tailwind CDN and Google Fonts. These actions do not establish Study Web runtime behavior.
- #58 route: `GET /api/v1/mentor/support/requests`; optional positive-int64 `course_id` and optional unvalidated string `status`; Bearer MENTOR. FastAPI query validation can produce 422 before view-level auth for malformed/out-of-range `course_id`; catalog precedence is unspecified.
- #58 view: shared MENTOR guard before view queries; optional course lookup returns 403 only when an existing course belongs to another Mentor; unknown course continues to a successful empty collection. Collection and all matching messages are read in bulk; success is 200 `DESIGN_RESOURCE_RETRIEVED`; GET does not commit. SQL/projection/attachment mismatch produces safe 500 with rollback. Invalid `course_id` uses the registered validation handler (422 `DESIGN_VALIDATION_ERROR`).
- #58 query: direct `courses.mentor_id` filter; exact AND of `course_id`/`status`; requests ordered `created_at DESC, id DESC`; all messages ordered `created_at ASC, id ASC`; no pagination/limit. Unknown status strings match nothing and return `[]`.
- Response projection: `SupportRequest[]` with `id`, `course_id`, `student{id,full_name,avatar_url?}`, `status`, complete `messages[]`, `created_at`, `resolved_at?`; each message has `id`, author summary, content, attachments[] and created_at. Upload metadata is returned only for exact linked upload, same owner/course, role-specific purpose and `UPLOADED` status. No course title, count facets, unread flag, SLA/due time, last-updated field or contact details are returned; null optional fields are omitted. `meta={}`.
- API #46 is an existing source-backed Mentor course list that returns paged courses, but it is not declared as an ME-11 dependency. Evaluate only as a candidate course-option source; do not silently add a request or pagination behavior.
- Candidate DB tables exist in `DB.sql`/migration 008, but live schema and deployment are unverified. Current API DD calls the BIGINT support model, owner scope, status values, full-thread response and attachment mapping derived fallbacks.

## 5. Element and marker plan

Use `ME11-EL-01`…`ME11-EL-33`, with source coordinates in the 1600×1425 screenshot. Marker centers are chosen in nearby whitespace or on non-text container margins; review the rendered annotation and move any badge that covers meaningful content.

| # | Planned element | Marker center (x,y) |
|---:|---|---:|
| 1 | Study2Work Mentor brand/logo link | (246,16) |
| 2 | Header navigation: Tổng quan | (330,16) |
| 3 | Header navigation: Khóa học phụ trách | (465,16) |
| 4 | Header navigation: Chấm bài | (650,16) |
| 5 | Active navigation: Hộp thư hỗ trợ | (805,16) |
| 6 | Header navigation: Thông báo | (955,16) |
| 7 | Notification bell and unread dot | (1276,16) |
| 8 | Mentor sample name, role and avatar | (1524,16) |
| 9 | Support eyebrow/icon | (20,111) |
| 10 | Page title | (20,173) |
| 11 | Page description | (20,218) |
| 12 | SLA `<4 giờ` badge | (1118,198) |
| 13 | “Vừa cập nhật tức thì” badge | (1530,198) |
| 14 | Filter panel/surface | (48,397) |
| 15 | “Tất cả” tab and sample count | (60,307) |
| 16 | “Đang mở” tab and sample count | (229,307) |
| 17 | “Đã giải quyết” tab and sample count | (402,307) |
| 18 | Course filter label | (1040,318) |
| 19 | Course filter select | (1530,307) |
| 20 | Empty-state panel | (50,455) |
| 21 | Empty-state mail illustration | (712,540) |
| 22 | Empty-state heading | (518,695) |
| 23 | Empty-state explanatory copy | (430,750) |
| 24 | “Làm mới hộp thư” button | (652,887) |
| 25 | Automatic notification/realtime claim | (509,957) |
| 26 | SLA information card | (51,1116) |
| 27 | Standard-answer information card | (567,1116) |
| 28 | Direct meeting information card | (1084,1116) |
| 29 | Footer logo | (20,1365) |
| 30 | Copyright/WCAG/footer claim | (88,1345) |
| 31 | Footer link: Quy chế Giảng viên | (1078,1345) |
| 32 | Footer link: Tiêu chuẩn đánh giá | (1265,1345) |
| 33 | Footer link: Hỗ trợ kỹ thuật | (1450,1345) |

## 6. Event plan

| Event | Trigger / kind | Planned source and outcome |
|---|---|---|
| ME11-E01 | Proposed route load | Resolve approved auth state; call #58 without invented defaults; validate envelope and map only returned fields; loading/empty/ready/error. |
| ME11-E02 | Status tab click/change | Current HTML changes visual selection only. Future query/local filter behavior, status grouping and counts require approval; exact status strings cannot be inferred from the tab labels. |
| ME11-E03 | Course selector change | Current options are static slugs with no handler. Future value must map to positive-int64 `course_id`; course-option source (possibly #46) requires approval. |
| ME11-E04 | Refresh button click | Current action is local animation/clock only. Future refresh may repeat #58 with the approved filters; errors must preserve prior data and show stale/error state. |
| ME11-E05 | Request row click (expected loaded state only) | No row is present in the asset. When a confirmed row design exists, pass `data[].id` to ME-12; do not call #59 from this screen unless the route contract assigns that load to ME-12. |
| ME11-E06 | Header/footer link click | Current anchors are `href="#"`; destinations are unverified, no API/data handoff is defined. |

The SLA/realtime/help cards are static source content, not separate events. The prototype’s timer and style changes are recorded as current HTML behavior, never as current Study Web behavior.

## 7. States, blockers and status

- States to document: route/auth gate; loading; empty; ready (expected but visually unspecified); status-filtered; course-filtered; refreshing; stale-after-refresh-error; 401 auth-required; 403 access-denied; 422 invalid course query; 500 detail/list error; no-match; returning/opening ME-12.
- Open decisions: AC-24 precondition vs empty state; loaded request-row presentation and visible fields; “Open” grouping and treatment of `WAITING_LEARNER`/`CANCELLED`; counts/facets; course option source and ID mapping; behavior/order for large unpaginated full-thread payload; query-validation/auth precedence; SLA/realtime/notification/standard-answer/Meet claims; Student request producer; palette/font/CDN approval; live schema/migration state.
- Status gate: `DD BLOCKED` because the loaded inbox view and core filter mappings are not specified; `IMPLEMENTATION BLOCKED` by the listed decisions and absent Study Web source; `RUNTIME NOT VERIFIED` because there is no ME-11 application route/runtime.

## 8. Steps and results

1. **Completed:** corrected the ME-11 inventory row and API #58 source classification; retained API DD Draft and live-schema uncertainty.
2. **Completed:** created 33-entry `ME-11_markers.json`, `ME-11_markers_overlay.svg`, and 2× `screen_annotated.png`; reviewed the rendered image and moved the course-label marker above the label to preserve legibility.
3. **Completed:** wrote [ME-11.md](ME-11.md), sections A–F, six event specifications and the #58 source trace.
4. **Completed:** static-audited marker/data/event correspondence, image dimensions, relative links, source hashes, 83-screen count and artifact checkpoint; no tests/runtime were run.
5. **Completed:** updated [global tracker](../../dd_screens/PLAN.md) and [screen inventory](../../../list_screen.md). Continue with ME-12 only in a separate session.

## 9. Results

- Artifacts: source `screen.png` and `code.html` retained; added `screen_annotated.png` (3200×2850), `ME-11_markers.json` (33), `ME-11_markers_overlay.svg`, and `ME-11.md` (A–F).
- Source hashes at final audit: PNG `2cbdc3691a241ee755ce6f422768472c943ddb352554f9ed9159df1cd5105272`; HTML `54536f7794787f3c93772c54805c42712f2339434a4c7f58fd3611925b64b2d5`.
- Result: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Loaded state/filter contracts remain open.
