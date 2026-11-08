# ST-20 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-20-EV-001` | `ST20-EV-01` / ST20-EV-01 — Truy cập trang và kiểm tra session | See source event detail below |
| `ST-20-EV-002` | `ST20-EV-02` / ST20-EV-02 — Tải dữ liệu tiến độ qua API #21 | See source event detail below |
| `ST-20-EV-003` | `ST20-EV-03` / ST20-EV-03 — Tải achievement qua API #38 | See source event detail below |
| `ST-20-EV-004` | `ST20-EV-04` / ST20-EV-04 — Tổng hợp và map progress widget | See source event detail below |
| `ST-20-EV-005` | `ST20-EV-05` / ST20-EV-05 — Map danh sách achievement | See source event detail below |
| `ST-20-EV-006` | `ST20-EV-06` / ST20-EV-06 — Render empty/partial/error state của widget | See source event detail below |
| `ST-20-EV-007` | `ST20-EV-07` / ST20-EV-07 — Chọn course để mở ST-21 | See source event detail below |
| `ST-20-EV-008` | `ST20-EV-08` / ST20-EV-08 — Mở ST-22 Thành tích và chứng nhận | See source event detail below |
| `ST-20-EV-009` | `ST20-EV-09` / ST20-EV-09 — Empty-state CTA tới ST-08 | See source event detail below |
| `ST-20-EV-010` | `ST20-EV-10` / ST20-EV-10 — Header, breadcrumb và footer navigation | See source event detail below |
| `ST-20-EV-011` | `ST20-EV-11` / ST20-EV-11 — Xử lý lỗi request và session | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết sự kiện

### ST20-EV-01 — Truy cập trang và kiểm tra session

- **Trigger / điều kiện:** điều hướng tới route đề xuất `/student/progress`; chỉ Student đã xác thực theo inventory/API design.
- **Element kích hoạt / loại:** page lifecycle route `/student/progress` (không có marker UI riêng) / `Page Load`.
- **Input:** route không có path param; session/token là input của ứng dụng nhưng Study Web source hiện không có route/auth guard cho màn hình này.
- **Xử lý:** (1) nhận route; (2) kiểm tra session/role theo cơ chế auth của ứng dụng sau khi được wire; (3) server vẫn phải kiểm tra quyền với mỗi `/me` request; (4) không suy ra auth thành công từ việc prototype render được.
- **Output:** route/UI đầu vào chỉ được xem là thiết kế; chưa có current runtime result. Redirect khi 401, copy khi 403 và return URL policy chưa xác định.
- **Ngoại lệ:** API catalog có 401/403; không có route-level behavior hoặc code ngoài catalog được thêm vào.

### ST20-EV-02 — Tải dữ liệu tiến độ qua API #21

- **Trigger / điều kiện:** page entry sau khi có session Student; inventory yêu cầu request độc lập cho progress widget.
- **Element kích hoạt / loại:** page lifecycle ST-20 / `API Request (GET)`; precondition là Student session theo design contract.
- **Input:** `GET /api/v1/users/me/progress`; Bearer token; query catalog ghi `course_id list hoặc aggregate?:string`; không có body.
- **Xử lý:** (1) chuẩn hóa query chỉ sau khi query grammar được chốt; (2) hiện chưa thể xác định cách encode list/aggregate; (3) gửi request có auth theo API design; (4) chỉ coi 200 + `DESIGN_RESOURCE_RETRIEVED` là success; (5) response type catalog `ApiEnvelope<UserProfile>` không chứa progress schema; không map bằng suy đoán; (6) không thêm retry/dedup/cache behavior chưa được xác nhận.
- **Output:** status/result của progress widget chưa thể triển khai; API #21 hiện `DECLARED_NOT_RUNNABLE`.
- **Lỗi:** catalog chỉ khai báo 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 500 `DESIGN_INTERNAL_ERROR`. Query parse, timeout và network failures chưa có response/business-code contract. Catalog không khai báo 404/422.

### ST20-EV-03 — Tải achievement qua API #38

- **Trigger / điều kiện:** page entry; inventory yêu cầu độc lập với #21.
- **Element kích hoạt / loại:** page lifecycle ST-20 / `API Request (GET)`; precondition là Student session theo design contract.
- **Input:** `GET /api/v1/users/me/achievements`; Bearer token; optional `course_id:int64`; không có body. Overview không truyền `course_id` trừ khi product xác nhận scope/nguồn lựa chọn.
- **Xử lý:** (1) kiểm tra có course filter hợp lệ hay không; (2) không suy ra filter/default; (3) gửi GET; (4) đọc response chỉ với HTTP 200 + `DESIGN_RESOURCE_RETRIEVED`; (5) response là `ApiEnvelope<Page<Achievement>>`; page metadata/request parameters chưa rõ; (6) không tự sinh locked/earned badges.
- **Output:** danh sách server xác nhận chỉ được map sau khi award projection và page shape được chốt. API #38 hiện `DECLARED_NOT_RUNNABLE`.
- **Lỗi:** catalog chỉ khai báo 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 500 `DESIGN_INTERNAL_ERROR`; không khai báo 404/422, parse failure hoặc transport policy.

### ST20-EV-04 — Tổng hợp và map progress widget

- **Trigger / điều kiện:** API #21 success với schema tiến độ đã được phê duyệt; điều kiện hiện chưa thể đạt theo contract đang có.
- **Element kích hoạt / loại:** API #21 success response / `Response Mapping` nội bộ; precondition là HTTP 200, `DESIGN_RESOURCE_RETRIEVED` và progress DTO được chốt.
- **Input:** cần tổng lesson, tiến độ theo course, course identifier và/hoặc aggregate theo inventory; catalog hiện trả `UserProfile` và query grammar mơ hồ.
- **Xử lý:** (1) kiểm tra response schema/required fields; (2) xác nhận owner/user scope từ server response/context; (3) chỉ thực hiện merge theo course key và công thức khi được định nghĩa; (4) không tính tỷ lệ, denominator, rounding, trạng thái completed hoặc thời điểm từ candidate `lesson_progress`; (5) không coi profile thiếu field là zero progress.
- **Output:** không có phép tính hay mapping được xác nhận ở thời điểm này; progress widget giữ trạng thái chưa khả dụng theo implementation blocker, không hiển thị số liệu bịa.
- **Ngoại lệ:** no-enrollment, empty-progress, partially populated course và malformed response chưa phân biệt được.

### ST20-EV-05 — Map danh sách achievement

- **Trigger / điều kiện:** API #38 success với Page/Achievement schema và award policy được duyệt.
- **Element kích hoạt / loại:** API #38 success response / `Response Mapping` nội bộ; precondition là schema `Page<Achievement>` và award projection được duyệt.
- **Input:** `Page<Achievement>`; logical candidate fields `id`, `code`, `title`, `awarded_at`, `course_id?` chưa được xác nhận làm runtime DTO.
- **Xử lý:** (1) xác nhận response item là award đã cấp; (2) không tự tính điều kiện từ lessons/quizzes/assignments; (3) hiển thị chỉ các field được phép; (4) không tạo locked state, chứng nhận, link tải hoặc badge action nếu không có contract; (5) không suy ra thứ tự/paging khi chưa có Page request semantics.
- **Output:** chỉ hiển thị award do backend xác nhận sau khi schema/rule được chốt; nếu không thì không dựng nội dung từ mockup.
- **Ngoại lệ:** empty Page, unknown achievement code, duplicate award và course filter behavior chưa có policy.

### ST20-EV-06 — Render empty/partial/error state của widget

- **Trigger / điều kiện:** có kết quả riêng từ #21 và/hoặc #38; inventory yêu cầu widget state độc lập, AC-18 lại mô tả chuỗi tuần tự.
- **Element kích hoạt / loại:** kết quả success/empty/error của từng request / `Widget State Transition` nội bộ; precondition là request tương ứng đã có outcome.
- **Input:** mỗi request có loading/success/empty/error outcome; response contracts và timing chưa được wire.
- **Xử lý:** (1) giữ status riêng cho từng widget theo inventory; (2) nếu một API success và API kia lỗi, chỉ render widget có data đã xác nhận khi contract UI được bổ sung; (3) không coi error/no-enrollment/no-progress đồng nghĩa; (4) không dùng HTML empty card làm chuẩn empty condition; (5) không tự chọn chạy song song hay tuần tự vì conflict inventory/AC-18 chưa được giải quyết.
- **Output:** expected state names gồm `loading`, `partial`, `empty`, `error`; các nhánh con của empty và thông điệp lỗi chưa đủ contract. Current runtime không có state nào được xác minh.
- **Ngoại lệ:** late response, race, refresh, stale cache và cancellation behavior chưa có nguồn.

### ST20-EV-07 — Chọn course để mở ST-21

- **Trigger / điều kiện:** Student chọn course item/progress link sau khi loaded-state UI và course ID đã có source. Element này chưa tồn tại trong HTML.
- **Element kích hoạt / loại:** course card/link ở loaded-state tương lai (chưa có marker vì không có trong source asset) / `Click`; precondition là course ID đến từ response được duyệt.
- **Input:** course ID từ response #21 hoặc nguồn được duyệt; kiểu/API #37 cần được xác nhận với ST-21.
- **Xử lý:** (1) kiểm tra ID đến từ data được xác nhận, không parse từ copy; (2) không gửi user ID; (3) route dự kiến `/student/progress/:courseId`; (4) ST-21 cần gọi #37 theo course_id và phải áp dụng access policy phía server; (5) giữ link back về ST-20 nếu router được wire.
- **Output:** chuyển ST-21 chỉ là expected flow; route/course handoff chưa hoạt động trong Study Web source.
- **Ngoại lệ:** course không tồn tại/không thuộc user, route parse và lỗi #37 cần theo contract ST-21/#37; không thêm status cho #21.

### ST20-EV-08 — Mở ST-22 Thành tích và chứng nhận

- **Trigger / điều kiện:** Student chọn link xem achievements sau khi loaded-state UI được thiết kế; hiện link này không có trong HTML prototype.
- **Element kích hoạt / loại:** action/link xem tất cả achievements ở loaded-state tương lai (chưa có marker) / `Click`; precondition là đích ST-22 được wire.
- **Input:** course filter chỉ nếu user chọn course và policy #38 xác nhận truyền filter; nếu không, danh sách overview scope chưa được định nghĩa.
- **Xử lý:** (1) không tự thêm query parameter; (2) route đề xuất `/student/achievements`; (3) ST-22 dùng API #38 theo contract chung; (4) không cấp/chứng nhận tại client; (5) truyền selected course chỉ khi route/handoff được chốt.
- **Output:** navigation tới ST-22 là expected inventory link, chưa có route source.
- **Ngoại lệ:** không tạo badge detail/download action vì #38 không khai báo.

### ST20-EV-09 — Empty-state CTA tới ST-08

- **Trigger / điều kiện:** người dùng bấm “Xem khóa học của tôi” trong HTML empty-state prototype.
- **Element kích hoạt / loại:** `ST20-EL-09` / `Click`; precondition là static empty-state anchor hiển thị.
- **Input:** anchor `/student/courses`; không có course ID.
- **Xử lý:** (1) prototype anchor chỉ biểu thị ý định; (2) inventory route của ST-08 là `/student/courses`; (3) hiện Study Web không có router để thực hiện; (4) không mang theo fabricated progress/course payload.
- **Output:** ST-08 là target dự kiến; current route transition chưa xác minh.
- **Ngoại lệ:** nếu ST-08 không khả dụng hoặc session hết hạn, handling thuộc route/auth contract chưa có.

### ST20-EV-10 — Header, breadcrumb và footer navigation

- **Trigger / điều kiện:** kích hoạt brand/nav/breadcrumb/footer link trong HTML prototype.
- **Element kích hoạt / loại:** anchors thuộc `ST20-EL-01`, `-02`, `-03`, `-11`, `-12`, `-15`, `-16` / `Click`; precondition là anchor tương ứng được render.
- **Input:** anchor labels/hrefs tĩnh; một số anchor không có destination runtime.
- **Xử lý:** (1) chỉ xác định element/link label từ prototype; (2) không suy ra search, notification, profile hoặc help API; (3) active nav `Tiến độ` là trạng thái trình bày; (4) back/navigation target phải lấy từ route design được duyệt.
- **Output:** không có destination nào được xác nhận bởi Study Web runtime.
- **Ngoại lệ:** link `#`, destination thiếu, auth hoặc browser back behavior chưa được đặc tả.

### ST20-EV-11 — Xử lý lỗi request và session

- **Trigger / điều kiện:** #21 hoặc #38 trả lỗi đã khai báo, hoặc transport không nhận response.
- **Element kích hoạt / loại:** outcome callback của request #21/#38 / `API Response Error` hoặc `Transport Error`; precondition là request tương ứng đã được bắt đầu.
- **Input:** HTTP/business code theo từng endpoint; catalog #21/#38 có 401/403/500 với code tương ứng; transport error không phải business code catalog.
- **Xử lý:** (1) giữ lỗi gắn với API/widget tương ứng; (2) 401 = `DESIGN_AUTHENTICATION_REQUIRED`, 403 = `DESIGN_ACCESS_DENIED`, 500 = `DESIGN_INTERNAL_ERROR`; (3) không hiển thị nội dung protected/achievement nếu request tương ứng bị từ chối; (4) không quy định retry/redirect/circuit breaker/cache khi chưa có policy; (5) không tự chuyển 404/422 sang error mapping vì catalog không khai báo hai mã này.
- **Output:** expected page có thể partial nếu policy inventory được duyệt; copy, retry control và session recovery cần product/auth contract. Runtime hiện chưa thể xác minh.
- **Ngoại lệ:** malformed query, malformed envelope, timeout, offline và một widget success/một widget fail chưa có policy đầy đủ.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
