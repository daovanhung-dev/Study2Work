# ME-02 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: 2. Luồng tổng thể

1. Người dùng đi tới route đề xuất `/mentor/courses`. Route, token/session hydration và role-aware shell chưa tồn tại trong Study Web source hiện tại.
2. Khi client được triển khai, chỉ gửi Bearer access token theo auth boundary của app; không nhận `mentor_id` từ query hoặc form. Current #46 guard đọc và xác thực JWT claims, yêu cầu role `MENTOR`, rồi lấy numeric `sub` làm principal.
3. Gọi `GET /api/v1/mentor/courses` với query đã được quyết định. Không gửi search/level/sort/semester/status label của mockup khi chưa có mapping. Query defaults current: `page=1`, `size=20`, không có status filter.
4. #46 validate `status` thuộc `DRAFT|PUBLISHED`, page `>=1`, size `1..100` trước DB query. Nếu hợp lệ, count và page query cùng áp dụng owner/status predicate; SQL order cố định `courses.created_at DESC, courses.id ASC`; query chỉ đọc.
5. View kiểm tra count/projection, map từng row thành `Course`, tính `total_pages`, rồi trả success envelope `DESIGN_RESOURCE_RETRIEVED`. `items=[]` là 200 thành công; out-of-range page cũng có thể trả `items=[]` nhưng vẫn giữ `total`/`total_pages`.
6. Chỉ các field có trong Course response được coi là current source data. Không suy ra KPI, status label, course code, rating, module/lab count hay capability/assignment từ nội dung mẫu.
7. Chọn một card có thể điều hướng sang ME-03 với `Course.id` nếu route/ownership handoff được duyệt. Các action khác hiện là target đề xuất hoặc blocker trong §5 và §7.

### Source trace — API #46

```text
GET /api/v1/mentor/courses
  -> apps/study-server/app/api/v1.py:mentor_courses
  -> MentorCourseQuery(status, page, size)
  -> app.modules.mentor.api_46_mentor_courses.view.get_mentor_courses
  -> validate_current_user_request(role="MENTOR")
  -> validate status DRAFT|PUBLISHED, page>=1, size 1..100
  -> count_owned_courses / find_owned_courses
       -> COUNT + LIST SQL; courses.mentor_id = JWT sub; optional exact status
       -> LEFT JOIN users; ORDER BY created_at DESC, id ASC; LIMIT/OFFSET
  -> map_course -> CoursePage(items, pagination)
  -> ApiEnvelope success DESIGN_RESOURCE_RETRIEVED or safe error response
  -> test source covers auth/query/page/empty/error branches (read, not run)
```

`find_owned_courses` và `count_owned_courses` dùng cùng direct-owner predicate và status nếu có. GET không ghi dữ liệu, không commit và không có external side effect. Query/status validation diễn ra sau auth guard; sai role trả 403 trước query. Test source dùng fake DB session/rows, vì vậy không xác minh live schema, deployment hay PostgreSQL query execution. DB context ghi live schema là `NOT_VERIFIED`.

### API liên quan tới các chỉ số trong mockup

- **#62 `GET /api/v1/mentor/courses/{course_id}/students`:** current source kiểm tra trực tiếp `courses.mentor_id`, rồi trả danh sách `StudentSummary` distinct từ enrollment `ACTIVE`; response không có aggregate total, không pagination. Không chứng minh KPI tổng học viên toàn bộ course hoặc dedup giữa các course.
- **#65 `GET /api/v1/mentor/courses/{course_id}/progress`:** current source trả một row cho mỗi active Student gồm `completed_lessons`, `total_lessons`, `progress_percent` theo lesson `PUBLISHED`. `progress_percent` là per-Student; contract source không trả average course completion. Tự average/dedup thêm ở ME-02 chưa được duyệt.
- **#66 `GET /api/v1/mentor/courses/{course_id}/analytics`:** current source trả `tracked_lesson_accesses`, `students_with_activity`, `last_activity_at`; đây là activity proxy, không phải rating, Capstone pass rate hay completion KPI. API catalog/DD snapshot còn mô tả #65/#66 response là `Page<Course>`, khác model runtime source.
- Các API trên cần `course_id`; chúng không nằm trong API list của ME-02 row ngoại trừ CTA/ME-16 handoff. Không gọi chúng để tạo KPI mới nếu màn hình/API orchestration chưa được phê duyệt.

### Trích từ DD nguồn: 6. State matrix

| State | Condition | UI/data expectation | Evidence/status |
|---|---|---|---|
| `loading` | First #46 request pending. | Page/list loading indicator; exact skeleton/layout not present in source. | Expected state from ME-02 inventory; Study Web `UNWIRED`. |
| `ready` | #46 200 with non-empty `items`. | Render allowed Course fields and server pagination only. | API source-backed; sample KPI/card extras remain blocked. |
| `empty` | #46 200 with `items=[]`, including no matching status/owner rows. | Distinguish empty from request error; empty copy/CTA not designed. | Current source returns success. |
| `out-of-range-page` | 200 page request beyond result range. | Current response may contain empty `items` but positive `total`; whether to clamp/reset page is a client/product decision. | Test source inspected; no app policy. |
| `unauthenticated` | Missing/invalid/expired token (as surfaced by current guard). | Login/session refresh/handoff not defined for Mentor Web. | #46 source returns 401. |
| `denied` | Valid JWT without `MENTOR`; or destination enforces course access. | Do not render course data after 403; access-denied UX/return path not defined. | #46 source returns 403 before query for wrong role. |
| `validation-error` | Invalid `status`, `page`, or `size`. | Keep separate from empty state; field-specific UI errors require mapping contract. | #46 returns 422. |
| `request-error` | #46 safe 500 or network failure. | Do not replace with empty or sample metrics. Trace ID/retry/persistence policy not designed. | API 500 source-backed; network UX not found. |
| `unsupported-metrics` | #46 succeeds, but mockup expects rating/progress/capstone/etc. | Hide those values or render an approved static/empty treatment only after design decision; never show sample values as live. | `NOT_FOUND` in #46 projection. |

`partial` appears on ME-01, not ME-02 inventory. Do not introduce independent dashboard-style widgets here unless the screen contract adds independently loaded APIs and error states.

### Trích từ DD nguồn: 7. Navigation/data handoff

| Origin | Proposed destination | Data | Gate |
|---|---|---|---|
| ME-01 “Tất cả lớp học” / header “Khóa học phụ trách” | ME-02 `/mentor/courses` | No route parameter. | Inventory proposal; app route/session absent. |
| Each card Workspace CTA | ME-03 `/mentor/courses/:courseId` | Current #46 `Course.id`. | Inventory link; ensure server verifies exact access; direct-owner/assignment discrepancy remains. |
| Top “Tạo bài giảng mới” | ME-04 `/mentor/courses/:courseId/lectures/new` | Requires a course ID; current button supplies none. | Must choose a course or move action into a course card; product decision required. |
| Card manage content action | Prototype ME-06 `/mentor/courses/:courseId/content` | Course ID. | Inventory ME-02 link row does not include ME-06; resolve direct vs ME-03 first. |
| Card grading action | Prototype ME-09 `/mentor/submissions` | Potential course context, if destination supports it. | Not in ME-02 screen links; handoff query/route contract absent. |
| Card progress action | ME-16 `/mentor/courses/:courseId/progress` | Course ID. | Inventory-linked; #65 destination current source returns per-Student progress. |
| “Phân tích lớp học” / overall report | Candidate ME-18 per-course `/mentor/courses/:courseId/analytics`, or global report target unknown. | Per-course ID required by #66; global report has no identified API. | Do not choose target/aggregation from label alone. |
| Header nav | Dashboard, ME-02, ME-09, support and notifications proposals from inventory. | No query/path data for top-level routes. | HTML links all `#`; runtime route/role guard absent. |

## 4. Luồng đọc (Read)
- Orchestration từ inventory: GET #46; mentor chỉ thao tác course hợp quyền từ server, không tự suy ownership ở client.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [ME-02](../../screen_stitch/04_mentor/ME-02_cac-khoa-hoc-phu-trach/ME-02.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
