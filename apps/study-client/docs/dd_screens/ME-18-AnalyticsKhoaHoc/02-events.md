# ME-18 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ME-18-EV-001` | `Source heading` / EV-01 — Load course analytics | See source event detail below |
| `ME-18-EV-002` | `Source heading` / EV-02 — Chọn khoảng thời gian phân tích (chưa phát sinh) | See source event detail below |
| `ME-18-EV-003` | `Source heading` / EV-03 — Xuất CSV (chưa phát sinh) | See source event detail below |
| `ME-18-EV-004` | `Source heading` / EV-04 — Kiểm tra đồng bộ lại | See source event detail below |
| `ME-18-EV-005` | `Source heading` / EV-05 — Quay lại ME-16 | See source event detail below |
| `ME-18-EV-006` | `Source heading` / EV-06 — Header, breadcrumb và footer navigation | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết sự kiện

### EV-01 — Load course analytics

- **Trigger / loại:** Mount route /mentor/courses/:courseId/analytics (candidate Load event; route chưa wire).
- **Điều kiện tiên quyết:** Mentor session hợp lệ; numeric course_id:int64 từ course context được duyệt. Direct-owner versus assigned-course policy và ID mapping chưa chốt.
- **Input:** Candidate courseId path → API course_id signed int64; Authorization Bearer JWT. Không có query/body. Client path parsing/role guard chưa có source.
- **Xử lý:**
  1. Sau khi route/carrier được duyệt, lấy numeric course_id; không suy từ title/code/term.
  2. Kiểm tra Mentor auth theo app contract; current server #66 yêu cầu MENTOR trước DB.
  3. Gọi GET /api/v1/mentor/courses/{course_id}/analytics. Không gửi period/from/to, page, size, sort hoặc body.
  4. Parse HTTP/businessCode. Catalog success là ApiEnvelope<Page<Course>>, còn local model là ApiEnvelope<MentorCourseActivityAnalytics>; giữ dữ liệu chờ duyệt và không map nếu discrepancy chưa được giải quyết.
  5. Nếu summary shape được duyệt, tracked_lesson_accesses chỉ là unique Student/lesson pair count; students_with_activity là distinct Student proxy count; last_activity_at là latest stored progress timestamp. Không map sang completion/duration/discussion charts.
  6. Empty 0/0/null chỉ chứng minh không có proxy rows theo query; không chứng minh ETL inactive, course không có học viên, không có enrollment hoặc event pipeline chưa chạy.
  7. API GET không ghi dữ liệu. Không cache, retry, poll hoặc gọi #65/#67 nếu chưa có contract.
- **API request:** #66 GET; path course_id:int64 required; Authorization Bearer JWT, role Mentor; query/body không khai báo. Direct catalog 200 DESIGN_RESOURCE_RETRIEVED ApiEnvelope<Page<Course>>; local source 200 ApiEnvelope<MentorCourseActivityAnalytics>. Exact errors 401/403/404/500; không có 422 do route đưa raw path vào view.
- **Response / data:** Local envelope success=true, businessCode=DESIGN_RESOURCE_RETRIEVED, message “Course analytics retrieved.”, data gồm tracked_lesson_accesses:int64≥0, students_with_activity:int64≥0, last_activity_at:datetime|null, meta rỗng và traceId. Các field đều DERIVED so với catalog. Empty aggregate 0/0/null.
- **Errors / side effects:** 401 DESIGN_AUTHENTICATION_REQUIRED trước DB; 403 DESIGN_ACCESS_DENIED khi thiếu MENTOR role hoặc direct owner mismatch; 404 DESIGN_RESOURCE_NOT_FOUND khi malformed/out-of-range ID hoặc course không tồn tại; 500 DESIGN_INTERNAL_ERROR khi query/projection lỗi với data null/safe message. Query error rollback; course owner mismatch không chạy aggregate; không mutation. Client UX/error copy/re-auth/network retry chưa được định nghĩa.

### EV-02 — Chọn khoảng thời gian phân tích (chưa phát sinh)

- **Element / loại:** #17 select, Change event chỉ có thể tồn tại nếu control được enable.
- **Current precondition:** Select có disabled attribute; user không thể đổi option. Không có event handler.
- **Options:** “7 ngày gần đây (Chưa có dữ liệu)”, “30 ngày gần đây (Chưa có dữ liệu)”, “Toàn khóa học (Chưa có dữ liệu)”. Period boundary, timezone, end-exclusive/inclusive và current course timeline chưa được khai báo.
- **Current processing/output:** Không nhận Change, không gọi API, không cập nhật state.
- **Future dependency:** #66 không có period query. Chỉ thiết kế event sau khi product/API owner chốt field/semantics; không tự lọc client-side từ all-time maximum timestamp.

### EV-03 — Xuất CSV (chưa phát sinh)

- **Element / loại:** #19 disabled button; không có click event hiện hành.
- **Precondition/input:** Luôn disabled trong HTML; không nhận payload/user selection.
- **Current processing/output:** Không có handler, request, file, job ID, URL hoặc download.
- **Future dependency/errors:** Cần định nghĩa export scope, period, schema, authorization, generation/status, file delivery và error/retry policy trước khi enable. Không dựng API từ nhãn CSV.

### EV-04 — Kiểm tra đồng bộ lại

- **Trigger / loại:** Click #28, inline onclick.
- **Precondition:** Button hiển thị enabled; HTML handler không tắt button và không chặn concurrent clicks.
- **Input:** Không có form data, course ID hoặc API token được dùng trong handler; chỉ DOM button reference và HTML gốc tại thời điểm click.
- **Current processing theo thứ tự:**
  1. Lưu innerHTML hiện tại vào orig.
  2. Đổi markup thành spinner + “Đang gửi lệnh...”.
  3. Sau 1,200 ms đổi thành check icon + “Đã ghi nhận yêu cầu”.
  4. Sau thêm 3,000 ms khôi phục orig đã lưu.
  5. Không có fetch/XHR/provider request, server-side state update, toast ngoài button hoặc ETL trigger. Nhiều click tạo timer chain chồng lấn; restore order phụ thuộc thời điểm click.
- **Output/error:** Chỉ DOM copy/icon change tổng cộng khoảng 4.2 giây. Không có API success/error semantics. Đây không phải xác nhận server đã nhận lệnh đồng bộ.
- **Future behavior:** Nếu action phải trigger synchronization, cần API/permission/idempotency/operation-status contract riêng. Không tự gọi #66 vì #66 chỉ đọc.

### EV-05 — Quay lại ME-16

- **Trigger / loại:** Click anchor #27.
- **Input:** Candidate course_id giữ từ ME-18 route; không thay bằng course code/title.
- **Current processing:** href="#" và data-path mẫu; không có route transition/API.
- **Expected candidate output:** Về ME-16 với course identity sau khi router/carrier được chốt. AC-26 ordering conflict và app auth/history behavior cần quyết định.
- **Error:** Thiếu numeric ID thì destination/fallback chưa được xác định; không tự chuyển tới /mentor/courses.

### EV-06 — Header, breadcrumb và footer navigation

- **Trigger / loại:** Click anchors #1–#7, #9–#10, #33–#35.
- **Input:** Không có form input; nav data-path là prototype metadata, còn breadcrumb/footer chỉ có href="#".
- **Current processing/output:** Placeholder fragment navigation; không có router/API.
- **Error/destination:** Không xác định. Không tự nối sang ME-01/ME-02/ME-13, notifications, external docs hoặc course detail.
- **Non-events:** Profile, metric cards, illustration, badges, status text và empty copy không có click handler. Không thêm chart drill-down/hover behavior.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
