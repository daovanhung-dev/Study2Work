# ME-16 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ME-16-EV-001` | `Source heading` / EV-01 — Khởi tạo màn hình / lấy roster progress | See source event detail below |
| `ME-16-EV-002` | `Source heading` / EV-02 — Đổi course | See source event detail below |
| `ME-16-EV-003` | `Source heading` / EV-03 — Chọn completion filter | See source event detail below |
| `ME-16-EV-004` | `Source heading` / EV-04 — Search student | See source event detail below |
| `ME-16-EV-005` | `Source heading` / EV-05 — Refresh progress | See source event detail below |
| `ME-16-EV-006` | `Source heading` / EV-06 — Mở chi tiết student / ME-17 | See source event detail below |
| `ME-16-EV-007` | `Source heading` / EV-07 — Mở analytics ME-18 | See source event detail below |
| `ME-16-EV-008` | `Source heading` / EV-08 — Header, breadcrumb, help and footer navigation | See source event detail below |
| `ME-16-EV-009` | `Source heading` / EV-09 — Tự động refresh theo cadence copy | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện

### EV-01 — Khởi tạo màn hình / lấy roster progress

- **Element / loại:** screen route load; route dự kiến `/mentor/courses/:courseId/progress`; Load/API read.
- **Precondition:** Mentor session phải hợp lệ; `courseId` phải có numeric signed-int64 mapping và course authorization phải được kiểm tra. Study Web chưa có route/auth/client. Prototype selector slug không thỏa input API.
- **Input:** route `courseId`; `Authorization: Bearer <token>`; không request query/body. Local source nhận path raw rồi parse signed int64 `[-2^63, 2^63-1]` theo validator.
- **Trình tự:**
  1. Parse route input; từ chối gọi API nếu thiếu/không có mapping hợp lệ. Behavior hiển thị lỗi route chưa được app contract hóa.
  2. Xác thực session ở frontend theo auth framework khi được triển khai; local API #65 tự yêu cầu role `MENTOR` trước DB.
  3. Đặt UI vào `loading` theo inventory nếu trạng thái đó được duyệt.
  4. Gửi `GET /api/v1/mentor/courses/{course_id}/progress` với Authorization header.
  5. Server kiểm path, tồn tại course, direct owner rồi aggregate roster. Server hiện trả 401/403/404/500 theo lỗi; 200 envelope có `DESIGN_RESOURCE_RETRIEVED`.
  6. Kiểm tra `success`, business code và shape. Khi dùng local shape, đọc `data.items[]`, pagination; không đọc như catalog `Page<Course>`. Trước mapping UI, owner phải xác nhận response discrepancy.
  7. Khi có items, render các field được duyệt. Không tạo course title, email, last activity, status category, reminder, submission, attendance hoặc update time từ dữ liệu thiếu.
  8. Khi items rỗng, local message là “No students found.”; hiển thị empty state đã được duyệt. Không khẳng định “đang tổng hợp” chỉ từ empty response.
- **API:** #65, `GET /api/v1/mentor/courses/{course_id}/progress`; auth Bearer, role MENTOR; path `course_id:int64`; no query/body; response local `ApiEnvelope<MentorStudentProgressPage>` nhưng catalog `ApiEnvelope<Page<Course>>` (DISCREPANCY). Errors: 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`; no declared 422.
- **Success output:** local fields only: student `{id,full_name,avatar_url?}`, `completed_lessons`, `total_lessons`, `progress_percent`; pagination is page 1 with entire roster. Local empty response: `items=[]`, pagination `{page:1,size:0,total:0,total_pages:0}`.
- **Error/edge output:** invalid path/absent course→404; wrong owner→403; auth invalid→401; DB/projection/invalid stored progress→safe 500. Network timeout, session redirect, retry and response contract resolution are not specified by Study Web.
- **Status:** Source behavior traced locally; frontend implementation blocked by response/path/schema/permission questions. No retry/cache/idempotency needed for the read is specified.

### EV-02 — Đổi course

- **Element / loại:** #19 select; Change.
- **Current input/default:** selected slug `cs-frontend-2025`; alternatives `fs-backend-nodejs`, `ai-ml-pipeline`; labels are static. No handler.
- **Current result:** browser changes selection only; no route update/API call/state persistence is implemented.
- **Target processing when contract exists:** resolve selected option to approved numeric course ID; validate ownership/eligibility; update course context; call EV-01/#65; clear or retain search/filter only under an approved rule.
- **API/source:** #46 may return numeric course IDs for owned courses, but no slug→ID mapping, selector data source, status eligibility or route handoff is defined. Do not call #65 with a slug.
- **Success/error/edge:** selected course currently only changes control value. Unknown slug or missing mapping must not trigger a guessed request. Course switch loading/error/reset policy remains blocked.

### EV-03 — Chọn completion filter

- **Element / loại:** #21–#23 buttons; Click.
- **Current input/result:** labels `Tất cả`, `Đúng tiến độ`, `Cần nhắc nhở`; All is visually selected, but buttons have no IDs, `aria-pressed`, handlers or state.
- **Validation/business rule:** no definition for on-time threshold, reminder classification, due-date source or whether filtering is client/server side. #65 does not return those categories and accepts no query.
- **Target processing:** do not change roster/filter UI until owner supplies category semantics and source. Once available, validate selected enum, filter the approved dataset or call an approved API, then update selected state and empty-filter state.
- **API:** none in current prototype. #65 cannot implement these filters as defined.
- **Output/edge:** current page has no effect; rapid clicks, reset behavior, filtered-empty state and preservation across course change are undefined.

### EV-04 — Search student

- **Element / loại:** #25 text input; Input/change (no submit form).
- **Current input:** arbitrary text; placeholder requests name, student number or email; no default, max length or debounce rule in HTML; no handler.
- **Target processing:** owner must decide searchable identifier fields, normalization, matching, privacy and client/server query design. #65 supports neither query parameters nor email; `student.id`/`full_name` are present only in local derived response. Do not implement email search or invent query parameters.
- **API:** none currently. If local filtering is later approved, it would only have the fields received in the accepted response and may be unsafe for an unbounded roster; bound and performance must be settled first.
- **Output/edge:** typing currently changes only the text field. No empty-result message, clear action, debounce, case/diacritic behavior, validation or request cancellation exists.

### EV-05 — Refresh progress

- **Element / loại:** #32 button; Click.
- **Current input/result:** no request input; local JS adds `animate-spin` and `disabled`, waits 1000 ms, then removes both. It does not change data, message, freshness indicator or cache.
- **Intended action in copy:** manually retrieve current course progress. This is design intent, not implemented behavior.
- **Target processing if approved:** require resolved numeric course ID and Mentor session; prevent duplicate click while request is pending; call same #65 GET as EV-01; validate response/error/business code; replace/refetch roster and show approved result/error state. Retry, timeout, stale-data handling and button re-enable behavior need API/client policy.
- **API:** no API is called by current HTML. Candidate API #65 is the same GET as EV-01; catalog/source response discrepancy remains.
- **Output/edge:** current only shows a 1-second cosmetic busy state. No freshness timestamp is returned by #65; rapid/repeated clicks are not network-protected.

### EV-06 — Mở chi tiết student / ME-17

- **Element / loại:** intended student row/action; Click. No such row/action is visible in prototype; inventory states the handoff.
- **Input:** accepted roster row with `course_id:int64` and `student_id:int64`. Local #65 returns student ID in each item; current empty screen has no item.
- **Target processing:** select a real row; preserve both IDs; authorize with Mentor session; navigate to ME-17 and call #67 with both path values. Do not derive student ID from name/email or use profile endpoint.
- **API:** #67 `GET /api/v1/mentor/courses/{course_id}/students/{student_id}/progress`; local contract requires direct owner and eligible active Student. Local response includes course/student summary and lesson items (`lesson_id`, title, order, status, percent, access/completion timestamps); catalog response currently differs. See ME-17 DD in its own session.
- **Output/edge:** expected navigation only after a valid row is selected. Not found, wrong course/student, 401/403/404/500 behavior is handled by #67 locally; selection UX, back navigation and route carrier are not wired. AC-26 sequence with #66 preceding this action remains unresolved.

### EV-07 — Mở analytics ME-18

- **Element / loại:** #33 anchor/button; Click.
- **Current input/result:** no parameter; `data-path="phan-tich-khoa-hoc-me18"`, `href="#"`; clicking does not establish a route.
- **Target processing:** require approved course ID; navigate to ME-18 route `/mentor/courses/:courseId/analytics` from inventory. The owner must decide how the screen flow relates to AC-26 where #66 appears before student selection.
- **API boundary:** this is navigation to ME-18, not a reason to merge #66 data into ME-16. Local #66 is `GET /api/v1/mentor/courses/{course_id}/analytics`, requires Mentor/direct owner, and returns a derived activity proxy (`tracked_lesson_accesses`, `students_with_activity`, `last_activity_at`), not the event ledger or catalog `Page<Course>`.
- **Output/edge:** current placeholder anchor only. Course identity, destination route, analytics metric definition and response acceptance are unresolved. Do not fetch #66 in this screen absent an approved orchestration change.

### EV-08 — Header, breadcrumb, help and footer navigation

- **Element / loại:** #1–#7, #9–#10, #35, #40–#42; Click.
- **Current input/result:** all are anchors with `href="#"`; several have decorative `data-path`, but no router consumes it in the prototype. #8 profile is not an anchor.
- **Target processing:** no destination can be assigned from current evidence. Preserve current screen/context only if browser default does so; do not invent routes, back behavior or sign-out.
- **API:** none established.
- **Output/edge:** clicks may only jump to page top/current fragment. Active nav and current breadcrumb are visual only. Route/auth behavior is UNWIRED.

### EV-09 — Tự động refresh theo cadence copy

- **Element / loại:** #37 static text; timer claim.
- **Current behavior:** no `setInterval`, polling loop, websocket/SSE or scheduled fetch exists. The “Mỗi 15 phút” string is not a timer.
- **Target processing:** none until product/API owner defines polling interval, visibility/background policy, stale response ordering, cancellation, retries, rate limits and whether #65 can handle expected roster size.
- **API:** none called by the timer claim.
- **Output/edge:** no automatic refresh occurs in current prototype; do not report it as active functionality.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
