# ST-05 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-05-EV-001` | `Source heading` / EV-01 — Route entry và Student context | See source event detail below |
| `ST-05-EV-002` | `Source heading` / EV-02 — Revalidate course bằng API #08 | See source event detail below |
| `ST-05-EV-003` | `Source heading` / EV-03 — Student xác nhận order terms | See source event detail below |
| `ST-05-EV-004` | `Source heading` / EV-04 — Tạo Order bằng API #16 (DESIGN_ONLY) | See source event detail below |
| `ST-05-EV-005` | `Source heading` / EV-05 — Quay lại kiểm tra ghi danh | See source event detail below |
| `ST-05-EV-006` | `Source heading` / EV-06 — Điều hướng header, breadcrumb và footer | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết từng sự kiện

### EV-01 — Route entry và Student context

- **Trigger / loại:** Mở route candidate `/student/checkout/:courseId`; page load/navigation.
- **Điều kiện:** AC-12 yêu cầu Student đã đăng nhập và đã được chuyển từ nhánh paid của ST-04. Study Web chưa có route hoặc auth guard; route chưa thể khởi tạo ở runtime.
- **Input:** Candidate `courseId` từ URL/ST-04. API #08/#16 cần `course_id:int64`. Chưa có client rule chuyển đổi/canonicalize hoặc return-state policy.
- **Xử lý:** (1) Target client phải resolve session/role theo contract được duyệt. (2) Nếu Student context hợp lệ, chuẩn hóa route ID theo int64 contract. (3) Nếu thiếu/sai role, destination, 401/403 UI và safe return URL cần được xác nhận; không suy ra chỉ từ public shell. (4) Sau khi route/guard được triển khai, EV-02 mới có thể chạy.
- **API / side effect:** Không có API riêng cho route/auth trong ST-05. #08 public; #16 yêu cầu Bearer Student. Không tạo Order ở bước load.
- **Output / lỗi:** Current: mở file HTML thấy static state. Expected: Student checkout route. Route/auth errors và UI chưa được định nghĩa.
- **Current status:** Study Web `UNWIRED`; runtime `NOT VERIFIED`.

### EV-02 — Revalidate course bằng API #08

- **Trigger / loại:** ST-05 có `courseId` sau khi vào route; GET read. Đây là revalidation thứ hai theo inventory; thời điểm so với #15 AC-12 chưa thống nhất.
- **Input:** `course_id:int64` từ candidate route. Không có query/body. API #08 là Public, không yêu cầu Bearer theo catalog.
- **API:** `GET /api/v1/courses/{course_id}`; status 200 `DESIGN_RESOURCE_RETRIEVED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`.
- **Xử lý hiện hành:** (1) Route nhận raw path string. (2) `validate_course_id` parse integer; parse failure trả 404. (3) Query lọc `courses.id` và `status='PUBLISHED'`, hiện `LEFT JOIN users`. (4) Missing/unpublished trả 404; SQLAlchemy failure rollback rồi trả 500. (5) `map_course` ánh xạ course/mentor; lỗi mapper trả 500. (6) Success trả `data.items` singleton và pagination page/size/total/total_pages đều 1, cùng envelope metadata/trace ID.
- **Mapping:** Có `id,title,description?,thumbnail_url?,price` decimal string, `status`, `mentor{id,full_name,avatar_url?}` theo current mapper. Không có currency, amount due, payment eligibility hoặc provider. #08 không có side effect.
- **UI/output:** Khi success, UI chỉ được coi course published/đọc được. Amount display/payment terms vẫn bị chặn cho đến khi source rule được duyệt. 404/500 presentation cần quyết định; không đổi 500 thành “không tìm thấy”.
- **Discrepancy/retry:** API #08 Draft DD mô tả `INNER JOIN`; source hiện tại là `LEFT JOIN` và mapper xử lý thiếu mentor như internal error. Không có retry/cache/freshness policy được xác nhận. Không diễn giải lần đọc này thành giá quote có hiệu lực nếu quote policy chưa có.
- **Current status:** API route/module/query/test source tồn tại; test không chạy trong phiên này. Không có UI caller hiện hành.

### EV-03 — Student xác nhận order terms

- **Trigger / loại:** Student click confirm control dự kiến; control không tồn tại trong HTML hiện tại.
- **Điều kiện:** Student hợp lệ; #08 đã revalidate thành công; nhánh paid được server/AC xác nhận; amount, currency, provider, terms, stale-price policy và wording đã được owner phê duyệt.
- **Input:** User action rõ ràng; course ID và các order terms đã được phê duyệt. `payment_provider` là API field bắt buộc, nhưng enum values và nguồn lựa chọn chưa có.
- **Xử lý:** (1) Client thu nhận thao tác một lần. (2) Kiểm tra dữ liệu theo rule đã được duyệt; hiện không có đủ rule để xác định validation. (3) Không auto-confirm theo load hoặc chỉ theo route. (4) Chỉ khi tất cả điều khoản và provider contract được chốt mới chuyển tới EV-04. (5) Trạng thái “một lần theo user action” là yêu cầu inventory; cơ chế chống trùng server/client chưa được xác định.
- **API / side effect:** Chưa gọi API trong bước consent. Không tự tạo checkbox, input hay provider list dựa trên mockup.
- **Output / lỗi:** Expected transition sang `order-creating`; hiện không thể trigger. UI disabled/blocked treatment cần design decision.

### EV-04 — Tạo Order bằng API #16 (DESIGN_ONLY)

- **Trigger / loại:** Một thao tác xác nhận explicit từ EV-03; POST mutation. Hiện không có trigger element.
- **Authentication/authorization:** Header `Authorization: Bearer <JWT>` bắt buộc; role Student. Không lấy `user_id` từ body; claim-to-user mapping thuộc backend contract và còn unresolved.
- **Request:** `POST /api/v1/orders`, `Content-Type: application/json`; body chỉ gồm `{ "course_id": int64, "payment_provider": "PaymentProvider" }` theo catalog. Không có path/query param. Provider member values chưa biết; placeholder không phải giá trị gửi được.
- **Xử lý theo contract:** (1) Chỉ gọi sau explicit confirm, không gọi từ page load. (2) Gửi đúng hai field và Bearer Student. (3) Server dự kiến tạo logical Order `PENDING` trong paid branch theo AC-12. (4) Parse response envelope. (5) Success contract là 201 `DESIGN_RESOURCE_CREATED` với `data: Order`. (6) Không tiếp tục nếu response shape/mapping không được xác nhận. (7) Chỉ handoff tới ST-06 khi `data.id` được xác nhận là cùng định danh mà #17 yêu cầu dưới tên `order_id`.
- **Response fields:** `id:int64`, `course_id:int64`, `user_id:int64`, `amount:decimal-string`, `currency:string`, `status:OrderStatus`, `created_at:date-time`. Order status ban đầu `PENDING` theo AC-12; allowed values khác và physical mapping chưa biết. Logical response contract không chứng minh physical persistence.
- **Errors:** Chỉ catalog: 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`. Không tự thêm 404/409/503. Chi tiết UI, field-level validation, network timeout, retry/duplicate/idempotency/rollback chưa được xác định.
- **Side effect / current status:** AC-12 kỳ vọng tạo Order logical; physical table/schema/transaction chưa có. Không tìm thấy current route/module/query/model/test #16; hiện không thể gọi hoặc claim Order đã tạo.

### EV-05 — Quay lại kiểm tra ghi danh

- **Trigger / loại:** Click CTA #11.
- **Input hiện tại:** Static `href="/courses"`; không có `courseId`, return URL, filter hay ST-04 path.
- **Xử lý hiện tại:** (1) Browser/client xử lý anchor. (2) Điều hướng tới `/courses` nếu route tồn tại. (3) Không gọi API hoặc thực hiện mutation. (4) Không thể khôi phục ST-04 context từ markup.
- **Kết quả / lỗi:** Label nói quay lại enrollment check nhưng đích là danh sách khóa học. Destination đúng và cách giữ course context cần được chốt. Study Web route hiện chưa có.

### EV-06 — Điều hướng header, breadcrumb và footer

- **Trigger / loại:** Click anchor ở #1–#5 hoặc #13; navigation. #12 là static brand group, không phải anchor.
- **Input:** Các `href` literal trong HTML: `/`, `/courses`, `/student/courses`, `/student/progress`, `/login`, `/register`. Breadcrumb có thêm label “Kiểm tra đơn hàng” dạng text không clickable.
- **Xử lý:** (1) Browser nhận static destination. (2) Chỉ điều hướng nếu route target có sẵn. (3) Không có API/mutation, auth-aware menu, course/order ID, query state hoặc redirect state trong markup. (4) Header nav có class `hidden md:flex`; không thấy menu thay thế ở viewport nhỏ.
- **Kết quả / lỗi:** Current page prototype có các link trên; route availability không xác minh được vì Study Web `UNWIRED`. Không xem link Student hoặc Sign In/Sign Up là bằng chứng auth state.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
