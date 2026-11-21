# ME-01 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ME-01-EV-001` | `ME01-EV-01` / `ME01-EV-01` — Vào dashboard và tải các widget | See source event detail below |
| `ME-01-EV-002` | `ME01-EV-02` / `ME01-EV-02` — Mở khóa học phụ trách | See source event detail below |
| `ME-01-EV-003` | `ME01-EV-03` / `ME01-EV-03` — Mở workspace của course | See source event detail below |
| `ME-01-EV-004` | `ME01-EV-04` / `ME01-EV-04` — Mở cây nội dung course | See source event detail below |
| `ME-01-EV-005` | `ME01-EV-05` / `ME01-EV-05` — Mở danh sách bài cần chấm | See source event detail below |
| `ME-01-EV-006` | `ME01-EV-06` / `ME01-EV-06` — Chọn submission từ preview | See source event detail below |
| `ME-01-EV-007` | `ME01-EV-07` / `ME01-EV-07` — Mở support inbox | See source event detail below |
| `ME-01-EV-008` | `ME01-EV-08` / `ME01-EV-08` — Mở một support request | See source event detail below |
| `ME-01-EV-009` | `ME01-EV-09` / `ME01-EV-09` — Nhập global search | See source event detail below |
| `ME-01-EV-010` | `ME01-EV-10` / `ME01-EV-10` — Mở notification hoặc Mentor profile | See source event detail below |
| `ME-01-EV-011` | `ME01-EV-11` / `ME01-EV-11` — Đổi ca, xem lịch hoặc vào meeting | See source event detail below |
| `ME-01-EV-012` | `ME01-EV-12` / `ME01-EV-12` — Academic notices và footer destinations | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: 5. Event specification

### `ME01-EV-01` — Vào dashboard và tải các widget

- **Trigger / loại:** Route entry `/mentor`; `Load` (route chỉ là expected design).
- **Element:** #2 nav current route; dữ liệu gắn với #8–#11, #12–#17.
- **Precondition:** Client auth/bootstrap chưa có source. Mỗi API yêu cầu valid Bearer access JWT có role `MENTOR`. Server guard không thay thế client login/session policy.
- **Input:** Access token từ session (nguồn/lưu trữ chưa xác minh); không có path ID. API #46 query `status?`, `page=1`, `size=20` (size 1–100); #54 `course_id?`, `status?`, `page=1`, page size cố định 20; #58 `course_id?`, `status?`, không có pagination. Không thêm `rating`, `deadline`, `unread`, `calendar` hoặc `size` cho #54/#58.
- **Xử lý tuần tự:**
  1. Chặn truy cập nếu application shell không xác định được session/role; cách redirect/login chưa có contract.
  2. Sau khi có điều kiện gọi API, request #46/#54/#58 độc lập. Backend không quy định thứ tự hoặc concurrency; client chưa tồn tại nên không được ghi “parallel” như current behavior.
  3. Với mỗi response, kiểm tra HTTP status, `success`, `businessCode`, `traceId`; chỉ map keys có trong response model. Không ánh xạ số liệu trong mockup sang API.
  4. #46: lấy `data.items` và `data.pagination`; có thể đọc `pagination.total` đúng phạm vi direct-owner và filter, chưa thể gọi là assigned count.
  5. #54: lấy `data.items`/`data.pagination`; page size cố định 20. `status` lọc exact string và không có enum validation. Chưa có căn cứ phân nhóm pending/late hoặc chọn preview size 4.
  6. #58: `data` là array không phân trang, gồm full `messages[]`/attachments. Không có summary projection; quyết định có gọi/render thread trên dashboard và giới hạn dữ liệu cần API/product agreement.
  7. Giữ `loading/empty/error` riêng từng widget; success của một API không phụ thuộc success của API khác. Cache, retry, timeout và stale-data behavior chưa được xác định.
- **API/error:** #46/#54/#58 trả 200 `DESIGN_RESOURCE_RETRIEVED` cho kết quả hợp lệ, kể cả rỗng. 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED` cho role không hợp lệ hoặc course ngoài direct-owner scope khi có course filter; 422 `DESIGN_VALIDATION_ERROR` khi input typed/validator lỗi; 500 `DESIGN_INTERNAL_ERROR` khi query/mapping lỗi. Không có API 404 flow cho dashboard collection.
- **Kết quả:** Mỗi widget có kết quả độc lập. 401/403 phải được chuyển tới auth/access behavior đã phê duyệt; không tự xóa token hoặc redirect sang route chưa xác minh. 422/500/network cần message và retry policy được chốt; không retry tự động theo giả định.
- **Blocker:** Mapping sample values; unresolved dashboard preview/page rules; #58 full unbounded threads; role bootstrap; không có current client.

### `ME01-EV-02` — Mở khóa học phụ trách

- **Trigger / loại:** Click nav “Khóa học phụ trách” hoặc link “Tất cả lớp học”; `Click`.
- **Element:** #2 hoặc #14.
- **Input:** Destination route đề xuất ME-02 `/mentor/courses`; không cần truyền query/path data theo inventory.
- **Xử lý:** 1) Kiểm tra link/router sau khi app route được implement; 2) chuyển tới ME-02; 3) ME-02 tự tải #46 theo contract của screen đó, không yêu cầu ME-01 mutation.
- **Output / ngoại lệ:** Route hiện là design-only; HTML href `#`; route 401/403 behavior do application shell quyết định. `UNWIRED`.

### `ME01-EV-03` — Mở workspace của course

- **Trigger / loại:** Click “Workspace (ME-03)” trên một course card; `Click`.
- **Element:** #15.
- **Input:** `courseId` cần lấy từ `Course.id` của #46; không dùng tên course hay ID sample.
- **Xử lý:** 1) Không kích hoạt nếu thiếu ID; 2) điều hướng mục tiêu thiết kế ME-03 `/mentor/courses/:courseId`; 3) destination kiểm tra quyền server-side bằng API liên quan. Không phát sinh call/mutation trên ME-01.
- **Output / ngoại lệ:** ID không hợp lệ/route không tồn tại cần not-found behavior đã phê duyệt; no client router hiện hữu. `UNWIRED`.

### `ME01-EV-04` — Mở cây nội dung course

- **Trigger / loại:** Click icon có title “Xem cây nội dung bài giảng”; `Click`.
- **Element:** #15.
- **Input:** `Course.id` từ #46.
- **Xử lý:** Target dự kiến ME-06 `/mentor/courses/:courseId/content` theo screen inventory và label. Gọi API #49 thuộc màn hình ME-06, không phải dashboard event.
- **Output / ngoại lệ:** `code.html` để `href="#"`; không có route client. Target trực tiếp ME-06 cần được xác nhận với flow ME-03. `UNWIRED`.

### `ME01-EV-05` — Mở danh sách bài cần chấm

- **Trigger / loại:** Click nav “Chấm bài & Đồ án” hoặc “Xem tất cả”; `Click`.
- **Element:** #2 hoặc #12.
- **Input:** Route mục tiêu ME-09 `/mentor/submissions`, không có submission ID.
- **Xử lý:** Điều hướng tới ME-09; ME-09 gọi #54 theo kế hoạch riêng. ME-01 không chấm, không POST #56/#57.
- **Output / ngoại lệ:** Route design-only; link HTML `#`. `UNWIRED`.

### `ME01-EV-06` — Chọn submission từ preview

- **Trigger / loại:** Click card/“Chấm bài (ME-10)”; `Click`.
- **Element:** #13.
- **Input:** `Submission.id` từ #54 nếu row thật được load; ID trong screenshot không có.
- **Xử lý:** Mockup chỉ dẫn ME-10 `/mentor/submissions/:submissionId`. AC-23 và inventory mô tả mở ME-09 rồi chọn submission trước khi gọi #55 ở ME-10. Hai luồng không đồng nhất; cần Product quyết định direct detail hay list-first. Không gọi API #55/#56/#57 từ dashboard khi chưa chốt.
- **Output / ngoại lệ:** Khi target được phê duyệt, ME-10 nhận ID qua route param; API #55 kiểm role/owner. API #54 không trả Rubric, tên học viên hoặc assignment title.

### `ME01-EV-07` — Mở support inbox

- **Trigger / loại:** Click nav “Hỗ trợ học viên” hoặc link “Mở Workspace Hỗ Trợ…”; `Click`.
- **Element:** #2 hoặc #18.
- **Input:** Route mục tiêu ME-11 `/mentor/support`; không có request ID.
- **Xử lý:** Điều hướng tới ME-11; screen đó tải #58 theo DD riêng. ME-01 không gọi reply/resolve #60/#61.
- **Output / ngoại lệ:** Route chưa có client implementation; link HTML `#`. `UNWIRED`.

### `ME01-EV-08` — Mở một support request

- **Trigger / loại:** Click “Trả lời ngay (ME-12)” hoặc request row; `Click`.
- **Element:** #17.
- **Input:** `SupportRequest.id` từ #58 nếu row thật được load.
- **Xử lý:** Asset hướng tới ME-12 `/mentor/support/:requestId`; AC-24/inventory mô tả mở ME-11 trước rồi chọn request. Chốt direct/list-first trước khi gắn link. Không tự gọi #59/#60/#61 từ dashboard.
- **Output / ngoại lệ:** ME-12 mới có thể tải #59 và thực hiện reply/resolve; server phải kiểm tra direct course owner. API #58 trả full thread, nên không cần gửi nội dung thread qua URL/navigation state.

### `ME01-EV-09` — Nhập global search

- **Trigger / loại:** Input/Enter/change vào text field; `Input/Submit`.
- **Element:** #3.
- **Input:** Chuỗi học viên/bài tập theo placeholder; max length/normalization chưa có.
- **Xử lý:** HTML không có `id/name/form`, submit handler, API, search route hoặc filter behavior. Không gửi query đến #54/#58 vì chúng không khai báo global free-text filter.
- **Kết quả:** Không có current behavior. Cần định nghĩa search scope, data fields, permissions và destination trước khi triển khai.

### `ME01-EV-10` — Mở notification hoặc Mentor profile

- **Trigger / loại:** Click bell/badge, “Thông báo” nav, hoặc profile; `Click`.
- **Element:** #2, #4, #5.
- **Input:** Badge `3` và profile trong ảnh là sample; không có `notification_id` hoặc current Mentor profile response để truyền.
- **Xử lý:** #64 chỉ đọc status theo notification ID; #63 tạo notifications. Chúng không xác định unread inbox/badge. #04 `/users/me` yêu cầu Student, không phải Mentor. Không gọi các API đó để dựng bell/profile.
- **Kết quả:** Destination, count source, read/unread update, profile query/logout menu đều chưa có contract. `NOT_FOUND/UNWIRED`.

### `ME01-EV-11` — Đổi ca, xem lịch hoặc vào meeting

- **Trigger / loại:** Click “Đổi ca trực”, appointment details hoặc “Vào Google Meet”; `Click`.
- **Element:** #7 hoặc #20.
- **Input:** Duty/appointment time, attendee, meeting URL trong asset chỉ là sample; không có API provider, calendar ID, authorization hoặc external URL được contract hóa.
- **Xử lý:** Không tạo schedule endpoint, cập nhật lịch, deep link Meet hay booking rule. Chỉ sau khi có nguồn dữ liệu, quyền và route/URL policy mới có thể xác định tab/window behavior.
- **Kết quả:** Các actions chưa triển khai; không đặt link ngoài từ static text.

### `ME01-EV-12` — Academic notices và footer destinations

- **Trigger / loại:** Click announcement/card, logo, policy/footer link; `Click`.
- **Element:** #21–#23.
- **Input:** Nội dung, ngày/kỳ học, URL, hotline/email/logo sample nằm tĩnh trong HTML.
- **Xử lý:** Không có notification listing hoặc academic bulletin API trong ME-01. API #63 là send; #64 là status theo ID. Tất cả links trong HTML là `#`; không mở URL hoặc mark read.
- **Kết quả:** Chỉ hiển thị khi nội dung và destinations được cung cấp/duyệt; current prototype không có handler.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
