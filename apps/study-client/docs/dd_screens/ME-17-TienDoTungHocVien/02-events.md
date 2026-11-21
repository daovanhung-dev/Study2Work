# ME-17 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ME-17-EV-001` | `Source heading` / EV-01 — Khởi tạo/tải tiến độ học viên | See source event detail below |
| `ME-17-EV-002` | `Source heading` / EV-02 — Làm mới kết nối | See source event detail below |
| `ME-17-EV-003` | `Source heading` / EV-03 — Quay lại tiến độ toàn khóa | See source event detail below |
| `ME-17-EV-004` | `Source heading` / EV-04 — Header, breadcrumb và footer navigation | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết sự kiện

### EV-01 — Khởi tạo/tải tiến độ học viên

- **Trigger / loại:** Mount route ME-17 (candidate Load event); route hiện chưa được wire.
- **Điều kiện tiên quyết:** Session Mentor hợp lệ; có course_id và student_id numeric int64 từ handoff được duyệt. Hiện chưa có carrier/map giữa ME-16 prototype và API #67.
- **Input:** Candidate route params courseId/studentId, chuyển thành path course_id/student_id; Authorization Bearer JWT. Không có query/body. Cách parse phía client, session source và lỗi thiếu ID chưa được định nghĩa.
- **Xử lý:**
  1. Khi route và carrier được triển khai, lấy đúng hai IDs từ route state đã duyệt; không suy ra ID từ slug/title.
  2. Kiểm tra session/role theo auth design được duyệt. Server #67 hiện yêu cầu role MENTOR.
  3. Gọi GET /api/v1/mentor/courses/{course_id}/students/{student_id}/progress một lần. Không gửi query/body; không có #65/#66 prefetch do contract này.
  4. Parse success envelope và businessCode. **Dừng mapping nếu catalog ApiEnvelope<Page<Course>> vẫn là contract bắt buộc trong khi server local trả ApiEnvelope<StudentCourseProgress>.**
  5. Nếu singular local shape được duyệt, candidate data mapping là student name/avatar, summary progress và lesson snapshot. Chưa có approved loaded-row template/status-to-copy mapping; không tạo timeline giao diện từ suy đoán.
  6. Chỉ cập nhật visible fields có source mapping được duyệt. Không map course title, enrollment badge, assignments/quizzes/hours, last-send, mentor comments hoặc milestones từ response không có các field đó.
  7. Không lưu/mutate server state. Cache, refresh policy và auto-retry chưa được quy định.
- **API request:** API #67, GET, path course_id:int64 + student_id:int64, Authorization Bearer JWT, request body/query không có. Direct catalog success được khai báo ApiEnvelope<Page<Course>>; local current source trả singular ApiEnvelope<StudentCourseProgress>. Không gọi API khác cho đến khi có contract.
- **Candidate outcomes / errors:**
  - 200 DESIGN_RESOURCE_RETRIEVED: data hiển thị chỉ theo contract được phê duyệt.
  - 401 DESIGN_AUTHENTICATION_REQUIRED: local source; client re-auth/session-expiry action chưa có thiết kế.
  - 403 DESIGN_ACCESS_DENIED: local direct-owner mismatch; không lộ chi tiết nếu privacy policy chưa chốt.
  - 404 DESIGN_RESOURCE_NOT_FOUND: local malformed/out-of-range ID, missing course hoặc Student không thuộc ACTIVE roster; không có phân biệt UI-approved.
  - 500 DESIGN_INTERNAL_ERROR hoặc transport/network failure: local/API client UX, retry, timeout và copy chưa được quy định.
  - lessons=[]: local snapshot có thể là course không có PUBLISHED lessons; không tự hiển thị thông điệp “chưa sync lịch sử”.
- **Output:** Candidate ready/error UI state only after response contract, identity mapping and loaded presentation are approved. Current prototype has no actual output/data update.

### EV-02 — Làm mới kết nối

- **Trigger / loại:** Click nút #13, Click.
- **Điều kiện tiên quyết:** Nút enabled; HTML handler disables trong hiệu ứng 600 ms. Không có request in-flight.
- **Input:** Không có user-entered data; candidate IDs/auth giống EV-01 nếu future refresh behavior is approved.
- **Current processing:** Handler thêm rotate-180 vào sync icon, disable button, đợi 600 ms, bỏ class và enable lại. Không gọi API, không thay đổi nội dung/state dữ liệu.
- **Candidate future processing:** Chỉ khi yêu cầu “làm mới kết nối” được định nghĩa là fetch mới và API contract được giải quyết, gọi lại #67 cho cùng hai IDs; thực hiện auth/error/data mapping theo EV-01. Không tự thêm timer/poll, retries, cache invalidation hoặc gọi #65/#66.
- **Output/error:** Hiện chỉ hiệu ứng quay 600 ms; không có success toast, error state hay freshness update. Future API response/error theo EV-01, nhưng tương tác này chưa thể được xem là refresh dữ liệu đã implement.

### EV-03 — Quay lại tiến độ toàn khóa

- **Trigger / loại:** Click #31, anchor navigation.
- **Điều kiện tiên quyết:** Cần course_id numeric hợp lệ và đích ME-16 được wire.
- **Input:** Candidate course_id giữ nguyên từ ME-17 route; không lấy course title/slug thay ID.
- **Current processing:** href="#" nên không điều hướng tới ME-16. Không gọi API.
- **Expected candidate processing:** Sau khi route/carrier được phê duyệt, trở về ME-16 với cùng course identity; auth session được giữ theo app auth policy. History/back behavior, route URL và fallback nếu thiếu ID chưa có contract.
- **Output/error:** Hiện không có cross-screen output. Không tự fallback sang /mentor/courses hoặc route tự tạo.

### EV-04 — Header, breadcrumb và footer navigation

- **Trigger / loại:** Click anchor #1–#7, #9, #37–#39.
- **Điều kiện tiên quyết:** Không có validation/input; các anchor hiện có href="#". Header nav có data-path nhưng không có router listener.
- **Input:** Không có form data. Các data-path là tong-quan, khoa-hoc-phu-trach, cham-bai, hop-thu-ho-tro hoặc thong-bao; đây là metadata prototype, không phải route contract.
- **Current processing:** Native placeholder anchor; không có Study Web route mapping hoặc API.
- **Output/error:** Không có destination được xác nhận. Không tự nối sang ME-01/ME-02/ME-09/ME-11/ME-13/ME-16/ME-18, notifications hoặc external docs.
- **Ngoài phạm vi event:** Profile, heading, metric cards, illustration và three explanatory tiles không có event handler trong HTML. Không tạo click behavior cho các lesson/assignment/quiz/comments.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
