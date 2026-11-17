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
| Điều kiện tiên quyết | Guest router maps `/courses/:courseId` to GS03Page; browser/live runtime remains unverified. Course visibility is checked by #08. |
| Input | `courseId` từ URL path, catalog type `course_id:int64`; không có query/body theo API #08. Backend route receives text and validator enforces signed-int64 bounds; client preserves the route value as a string. No cache/session field is used. |
| Thành công | Gọi `GET /api/v1/courses/{course_id}` public, không Bearer; nhận envelope HTTP 200, `businessCode=DESIGN_RESOURCE_RETRIEVED`; đọc `data.items[0]` và các field Course/Mentor từ API table bên dưới. Current backend trả `CoursePage` singleton. |
| UI output expected | Rời loading sang loaded detail khi có course published. Không có visual loaded-state trong tài sản. Không được dùng empty-state prototype như thể API trả empty list cho detail. |
| Current source result | Angular GS03Page requests #08 and maps ready/not-found/error; `code.html` remains a static prototype and browser/live API runtime is unverified. |

**Current partial implementation trace:**

1. Đọc raw `courseId` từ path.
2. Pass route text to #08 without converting through JavaScript `Number`; backend enforces signed-int64 bounds.
3. Show the current loading state and send public GET #08 without query/body/Bearer.
4. On a successful envelope, read `data.items[0]`; the API source returns singleton pagination.
5. Map Course/Mentor, retain `price` as text and do not infer a rating.
6. Enter ready only for a returned `PUBLISHED` course. Current detail UI is derived because its loaded visual is not approved.
7. If query param is `tab=curriculum`, call #09 only after #08 is ready. This follows F02; AC-05 eager sequencing remains a discrepancy. No #10 caller is present.

**Lỗi/ngoại lệ theo current #08:**

| Kết quả | Current behavior | UI mapping còn thiếu |
|---|---|---|
| 404 `DESIGN_RESOURCE_NOT_FOUND` | Invalid ID hoặc không có course PUBLISHED; message source “Published course not found.” | Inventory gọi `course-404`; AC-05 còn nêu 403. Cần xác nhận trang/lỗi hiển thị; không biến 404 thành 403. |
| 500 `DESIGN_INTERNAL_ERROR` | SQL/mapping error được log nội bộ và trả safe error; SQLAlchemy error rollback. | Current UI shows a safe error message; retry/timeout policy is not implemented. Internal detail is not displayed. |
| Network/timeout | Không có behavior/UI source để xác nhận. | Trạng thái và retry chưa được định nghĩa; không tự thêm số lần retry. |

### `GS03-EV-02` — Chọn tab Đề cương

| Thuộc tính | Đặc tả |
|---|---|
| Element / loại | #5 `GS03-EL-05`; click or keyboard activation on the enabled curriculum tab. |
| Điều kiện tiên quyết | GS03 #08 must return a PUBLISHED course; the current page renders tabs only in ready state. |
| Input | `courseId` giống route và confirmed course. Không có page/query/body trong current #09 route. |
| API | `GET /api/v1/courses/{course_id}/curriculum`, Public, không Bearer, không request body. Current route/module/view/query/test source tồn tại. |

**Current partial flow follows F02 lazy-load:**

1. Khi user vào tab từ overview hoặc direct-entry, dùng đúng course ID của GS-03; không gọi nếu course detail chưa được xác nhận public.
2. Select `?tab=curriculum`; the GS03 panel shows loading while #09 is pending.
3. Gọi #09. Current backend kiểm tra course `PUBLISHED`, sau đó lấy lesson `PUBLISHED`, order `sort_order ASC, id ASC`.
4. Với 200 `DESIGN_RESOURCE_RETRIEVED`, đọc `data.items` và pagination. Mỗi item có `id`, `course_id`, `title`, optional `content`, `video_url`, `order`, `status`.
5. Nếu `items=[]`, current source vẫn trả 200 với message “No published lessons.”, total=0, total_pages=0; biểu diễn empty curriculum riêng với API error.
6. Nếu có items, hiển thị theo `order` đã nhận; chưa có contract cho preview, mở bài học, quyền học hoặc access denied. Không thêm affordance mở video/lesson từ các field có mặt.
7. 404 `DESIGN_RESOURCE_NOT_FOUND` biểu thị course không tồn tại/không PUBLISHED ở lúc gọi; 500 `DESIGN_INTERNAL_ERROR` biểu thị query/mapping failure. SQLAlchemy error hiện rollback.
8. No client cache or retry is implemented. `switchMap` cancels the active #09 request when tab/course changes; direct-entry and large text IDs are covered by the GS03 spec.

| Kết quả/ngoại lệ | Expected mapping theo source hiện có | UI còn thiếu |
|---|---|---|
| #09 thành công có lessons | Map `data.items` theo `order`; current mapper copies title/order only. | Current derived list has no approved visual/access contract. |
| #09 thành công rỗng | `items=[]`, total=0 là successful empty curriculum, không phải API error. | Current empty copy is derived; no copy/layout approval. |
| #09 404/500 hoặc network error | 404 maps to not-found; 500/transport maps to safe service error. | Retry and approved error UX remain undefined. |
| Current source | GS03 query tab is source-wired; #09 loads after #08 succeeds. The static `code.html` prototype remains disabled and does not establish app behavior. |

AC-05 mô tả #09 được gọi ngay sau #08 mà không chờ user chọn tab. Đây là discrepancy với F02, không được tự giải quyết bằng implementation giả định.

### `GS03-EV-03` — Chọn tab Đánh giá

| Thuộc tính | Đặc tả |
|---|---|
| Element / loại | #5 `GS03-EL-05`; enabled click on the “Đánh giá” tab in current Angular. The static Stitch HTML still depicts it disabled. |
| Điều kiện tiên quyết | Current UI enables the tab after #08 confirms a PUBLISHED course. GS05/#10 caller is locally wired; API #10 title/rating/visibility/query contract remains Draft and is not approved. |
| Input khai báo | `courseId` từ route; catalog/API DD khai báo optional `page:int32` và literal `rating filter?:string`. API DD chuẩn hóa query key thành `rating` nhưng cũng ghi physical key/semantics chưa xác nhận. |
| API status | Backend API #10 route/module/tests and frontend `API_010`/GS05 caller are source-wired locally. Source returns `title: null`, has no rating/aggregate and does not apply `rating`; GS05 sends only `page`. API DD/catalog contract remains Draft. |

**Xử lý bị chặn:**

1. Current tab selection updates `tab=reviews`; GS05 requests #10 only after #08 succeeds. The static Stitch asset remains disabled and is not the Angular runtime.
2. Trước implementation, BE/Product phải nối endpoint/model và chốt physical query key/semantics, page validation, review title source, rating source/aggregate, visibility/status và reply mapping.
3. Không biến `discussions.content` thành `title`, không suy ra rating, không tính aggregate và không giả lập dữ liệu review.
4. Current GS05 maps source-backed loading/empty/ready/404/other-error states and page metadata. This bounded projection does not approve the Draft response or loaded-state design.

| Kết quả/ngoại lệ | Current/expected result |
|---|---|
| Current source | Enabled query tab; GS05/#10 lazy request after #08 success, source-backed review/reply projection and pagination. Angular tests cover the flow; local browser render used an in-memory stub. |
| Remaining contract/design gate | Title/rating/aggregate/visibility/query semantics remain unresolved; loaded view is derived and is not DD-approved. |
| Failure | Current #10 404 maps to not-found and other errors to safe error; deployed behavior and unresolved Draft contract remain unverified. |

### `GS03-EV-04` — Quay lại danh sách khóa học

| Thuộc tính | Đặc tả |
|---|---|
| Element / loại | #8 `GS03-EL-08`; click anchor `/courses`. |
| Input | Không có form/user data; href là literal `/courses`. |
| Xử lý | Browser xử lý anchor thường; không có API, cache mutation hay course ID handoff. |
| Kết quả expected | Mở danh sách khóa học GS-01. Angular router exists, but the Guest `/courses` route is not wired; destination remains a proposal and is not runtime verified. |
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
