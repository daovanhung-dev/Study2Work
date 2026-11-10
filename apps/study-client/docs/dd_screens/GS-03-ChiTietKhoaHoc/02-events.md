# GS-03 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `GS-03-EV-001` | `GS03-EV-01` / `GS03-EV-01` — Mở màn hình / tải course detail | See source event detail below |
| `GS-03-EV-002` | `GS03-EV-02` / `GS03-EV-02` — Chọn tab Đề cương | See source event detail below |
| `GS-03-EV-003` | `GS03-EV-03` / `GS03-EV-03` — Chọn tab Đánh giá | See source event detail below |
| `GS-03-EV-004` | `GS03-EV-04` / `GS03-EV-04` — Quay lại danh sách khóa học | See source event detail below |
| `GS-03-EV-005` | `GS03-EV-05` / `GS03-EV-05` — Điều hướng qua brand/nav/breadcrumb/footer | See source event detail below |
| `GS-03-EV-006` | `GS03-EV-06` / `GS03-EV-06` — CTA ghi danh expected nhưng chưa có source | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện

### `GS03-EV-01` — Mở màn hình / tải course detail

| Thuộc tính | Đặc tả |
|---|---|
| Element / loại | Entry event của route đề xuất; `Load`. Không có handler trong `code.html`. |
| Điều kiện tiên quyết | URL có path segment `courseId`; Study Web route/runtime phải được nối. Course visibility được backend kiểm tra ở #08. |
| Input | `courseId` từ URL path, catalog type `course_id:int64`; không có query/body theo API #08. Current route nhận `str` và shared parser không kiểm tra signed int64/positive range. Không dùng cache/session field nào được source xác nhận. |
| Thành công | Gọi `GET /api/v1/courses/{course_id}` public, không Bearer; nhận envelope HTTP 200, `businessCode=DESIGN_RESOURCE_RETRIEVED`; đọc `data.items[0]` và các field Course/Mentor từ API table bên dưới. Current backend trả `CoursePage` singleton. |
| UI output expected | Rời loading sang loaded detail khi có course published. Không có visual loaded-state trong tài sản. Không được dùng empty-state prototype như thể API trả empty list cho detail. |
| Current source result | HTML không khởi tạo request hoặc binding; browser hiện thẳng empty/unavailable state. Event hiện là expected design, chưa được triển khai. |

**Trình tự expected nếu UI được nối:**

1. Đọc raw `courseId` từ path.
2. Chuyển raw value cho API theo dạng path; current backend parse ID bằng `parse_integer`. Invalid integer syntax trả 404 `DESIGN_RESOURCE_NOT_FOUND`. Parser không enforce catalog `int64` range/positive-only rule; oversized path và cách DB error được xử lý cần được xác nhận, không tự thêm client validation.
3. Bật trạng thái loading cho vùng detail. Visual loading chưa có trong source; cần thiết kế trước khi implement.
4. Gửi GET #08. Không có query, body hoặc Bearer header theo public contract.
5. Với HTTP 200, kiểm tra envelope và business code; lấy phần tử `data.items[0]`. API source đặt pagination page=1, size=1, total=1, total_pages=1.
6. Map `Course` cùng nested `mentor`; giữ nguyên `price` dạng string cho tới khi có quy tắc currency/format đã duyệt. Không tính rating từ response này.
7. Chuyển sang loaded state chỉ sau khi `status=PUBLISHED` được trả bởi current query. Current source query đã lọc PUBLISHED.
8. Chọn thời điểm gọi #09/#10 theo quyết định orchestration còn mở: inventory F02 nói lazy theo tab; AC-05 nói tuần tự ngay trong page load. Không gửi cả hai request theo một lựa chọn tự suy đoán.

**Lỗi/ngoại lệ theo current #08:**

| Kết quả | Current behavior | UI mapping còn thiếu |
|---|---|---|
| 404 `DESIGN_RESOURCE_NOT_FOUND` | Invalid ID hoặc không có course PUBLISHED; message source “Published course not found.” | Inventory gọi `course-404`; AC-05 còn nêu 403. Cần xác nhận trang/lỗi hiển thị; không biến 404 thành 403. |
| 500 `DESIGN_INTERNAL_ERROR` | SQL/mapping error được log nội bộ và trả safe error; SQLAlchemy error rollback. | Chưa có error UI, retry rule hoặc timeout policy trong asset. Không hiển thị internal detail. |
| Network/timeout | Không có behavior/UI source để xác nhận. | Trạng thái và retry chưa được định nghĩa; không tự thêm số lần retry. |

### `GS03-EV-02` — Chọn tab Đề cương

| Thuộc tính | Đặc tả |
|---|---|
| Element / loại | #5 `GS03-EL-05`; `Click` trên tab Đề cương. Hiện button disabled nên sự kiện không thể thực hiện. |
| Điều kiện tiên quyết | Tab phải được bật trong loaded screen sau khi #08 xác nhận PUBLISHED. Current HTML không có tiêu chí bật tab. |
| Input | `courseId` giống route và confirmed course. Không có page/query/body trong current #09 route. |
| API | `GET /api/v1/courses/{course_id}/curriculum`, Public, không Bearer, không request body. Current route/module/view/query/test source tồn tại. |

**Trình tự expected theo F02 lazy-load:**

1. Khi user chọn tab lần đầu, dùng đúng course ID của GS-03; không gọi nếu course detail chưa được xác nhận public.
2. Hiển thị loading state riêng cho tab; chưa có visual/loading contract.
3. Gọi #09. Current backend kiểm tra course `PUBLISHED`, sau đó lấy lesson `PUBLISHED`, order `sort_order ASC, id ASC`.
4. Với 200 `DESIGN_RESOURCE_RETRIEVED`, đọc `data.items` và pagination. Mỗi item có `id`, `course_id`, `title`, optional `content`, `video_url`, `order`, `status`.
5. Nếu `items=[]`, current source vẫn trả 200 với message “No published lessons.”, total=0, total_pages=0; biểu diễn empty curriculum riêng với API error.
6. Nếu có items, hiển thị theo `order` đã nhận; chưa có contract cho preview, mở bài học, quyền học hoặc access denied. Không thêm affordance mở video/lesson từ các field có mặt.
7. 404 `DESIGN_RESOURCE_NOT_FOUND` biểu thị course không tồn tại/không PUBLISHED ở lúc gọi; 500 `DESIGN_INTERNAL_ERROR` biểu thị query/mapping failure. SQLAlchemy error hiện rollback.
8. Client cache/lưu tab state, retry, abort request khi chuyển tab, duplicate-click behavior đều chưa có nguồn xác nhận.

| Kết quả/ngoại lệ | Expected mapping theo source hiện có | UI còn thiếu |
|---|---|---|
| #09 thành công có lessons | Map `data.items` theo `order`; giữ response status/field từ source. | Loaded lesson-list state chưa có visual contract. |
| #09 thành công rỗng | `items=[]`, total=0 là successful empty curriculum, không phải API error. | Empty-state copy/action chưa được duyệt. |
| #09 404/500 hoặc network error | 404 course không còn public; 500 query/mapping failure; network không có current behavior source. | Error state, retry và thông báo chưa được thiết kế. |
| Current source | Tab đang disabled nên không thể kích hoạt; HTML không gửi request hoặc đổi state. | Đây là expected event, chưa chạy trong UI. |

AC-05 mô tả #09 được gọi ngay sau #08 mà không chờ user chọn tab. Đây là discrepancy với F02, không được tự giải quyết bằng implementation giả định.

### `GS03-EV-03` — Chọn tab Đánh giá

| Thuộc tính | Đặc tả |
|---|---|
| Element / loại | #5 `GS03-EL-05`; `Click` trên tab Đánh giá. Hiện button disabled. |
| Điều kiện tiên quyết | Chỉ có thể bật sau khi course được xác nhận public và API #10 đã có executable contract/source. Hai điều kiện chưa thỏa trong checkout hiện tại. |
| Input khai báo | `courseId` từ route; catalog/API DD khai báo optional `page:int32` và literal `rating filter?:string`. API DD chuẩn hóa query key thành `rating` nhưng cũng ghi physical key/semantics chưa xác nhận. |
| API status | API #10 hiện `DECLARED_NOT_RUNNABLE`: không có route/module/test source. Không gửi request runtime. Catalog design khai báo public GET `/api/v1/courses/{course_id}/reviews`, response `ApiEnvelope<Page<Discussion>>`, 200/404/500. |

**Xử lý bị chặn:**

1. Tab hiện disabled nên không phát request/event handler.
2. Trước implementation, BE/Product phải nối endpoint/model và chốt physical query key/semantics, page validation, review title source, rating source/aggregate, visibility/status và reply mapping.
3. Không biến `discussions.content` thành `title`, không suy ra rating, không tính aggregate và không giả lập dữ liệu review.
4. Chỉ sau khi contract được xác nhận mới định nghĩa loading/empty/ready/error response handling. API DD hiện design-only nói empty reviews là 200 với items rỗng và 404/500; chưa phải current runtime behavior.

| Kết quả/ngoại lệ | Current/expected result |
|---|---|
| Current source | Tab disabled; không có click handler, request, state transition hay review data. Trang giữ static unavailable state. |
| Blocked expected event | Chưa xác định loaded, empty, error, pagination hoặc rating output; không được dựng các state này chỉ từ catalog/API DD. |
| Failure | Không có executable #10 để cung cấp HTTP/business error behavior; contract owner cần xác nhận trước khi lập trình. |

### `GS03-EV-04` — Quay lại danh sách khóa học

| Thuộc tính | Đặc tả |
|---|---|
| Element / loại | #8 `GS03-EL-08`; click anchor `/courses`. |
| Input | Không có form/user data; href là literal `/courses`. |
| Xử lý | Browser xử lý anchor thường; không có API, cache mutation hay course ID handoff. |
| Kết quả expected | Mở danh sách khóa học GS-01. Study Web route chưa tồn tại trong checkout nên đây là destination dự kiến, chưa runtime verified. |
| Lỗi/edge | HTML không có handler cho route-not-found, history, preserve-filter/query hoặc network. Không khẳng định list query được giữ lại. |

### `GS03-EV-05` — Điều hướng qua brand/nav/breadcrumb/footer

| Thuộc tính | Đặc tả |
|---|---|
| Element / loại | #1, #2, #3 và #10; click các anchor static. Footer brand #9 không phải link. |
| Input và đích | Brand/Trang chủ → `/`; Khóa học/breadcrumb/footer → `/courses`; Đăng nhập → `/login`; Đăng ký → `/register`. Current breadcrumb item là text, không click được. |
| Xử lý / API | Không có API hoặc local state mutation trong HTML. Browser theo href thông thường. |
| Kết quả | Chỉ xác nhận href trong source. Đích route/session behavior không thể xác nhận khi Study Web chưa wired. |

### `GS03-EV-06` — CTA ghi danh expected nhưng chưa có source

| Thuộc tính | Đặc tả |
|---|---|
| Element / loại | Expected CTA theo inventory GS-03; không có element/marker/handler trong `code.html`. Event này là blocked requirement, không phải hành vi hiện tại. |
| Input có thể truy vết | Course ID/detail từ #08 nếu request được xác nhận; không có input identity/auth từ GS-03 source. |
| Điều kiện/blocker | Inventory liên kết `/student/enroll/:courseId` (ST-04). F03/G-01 chặn API #15 vì request chỉ có course_id nhưng response Enrollment chứa user_id trong endpoint public. Chưa chốt guest login/handoff hoặc selection identity. |
| Xử lý/API | Không gọi #15, #19 hoặc API khác từ GS-03 theo DD này. Giá #08 tự nó không xác nhận đã ghi danh hoặc eligibility/payment. |
| Kết quả | Chưa thể xác định label/action/đích chính xác. Sau khi Product/Auth/BE chốt, cần bổ sung CTA và luồng điều hướng có bảo toàn `courseId`; cho tới đó không hiển thị trạng thái đăng ký thành công. |

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
