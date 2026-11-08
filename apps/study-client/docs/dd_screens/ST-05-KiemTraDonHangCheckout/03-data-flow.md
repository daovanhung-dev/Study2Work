# ST-05 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

### Luồng dự kiến

1. Nhận `courseId` từ route dự kiến. Xác thực role Student theo AC-12 và #16 trước khi hiển thị hoặc tạo Order. Route, session guard và cách map route parameter hiện chưa được triển khai.
2. Gọi API #08 để revalidate course theo yêu cầu inventory. Catalog: Public `GET /api/v1/courses/{course_id}`, `course_id:int64`, không query/body. Current handler nhận path string rồi parse integer; chỉ query course `PUBLISHED`.
3. Với #08 success, current API trả `ApiEnvelope<Page<Course>>` dạng singleton `data.items[0]` và pagination `{page:1,size:1,total:1,total_pages:1}`. Fields đã được source-backed gồm `id`, `title`, nullable `description`, nullable `thumbnail_url`, decimal-string `price`, `status`, và `mentor{id,full_name,avatar_url?}`. Không có category/currency. Không suy ra tiền phải thu từ `price` nếu chưa có quy tắc amount/currency.
4. Chỉ trình bày thông tin checkout/amount/provider/điều khoản sau khi owner phê duyệt nguồn và cách ánh xạ. Hiện prototype không có các phần tử đó.
5. Student xác nhận tường minh. Không tự submit khi trang load, khi #08 thành công, hoặc chỉ vì Student mở nhánh paid. Hình thức control, wording, consent và validation của confirmation còn cần quyết định sản phẩm.
6. Sau một thao tác xác nhận, gửi một POST #16 với body đúng contract `{course_id:int64!, payment_provider:PaymentProvider!}` và Bearer JWT. Không tự thêm field; không gửi nếu provider/amount terms chưa được chốt.
7. Khi response thành công, API contract khai báo HTTP 201, `businessCode=DESIGN_RESOURCE_CREATED`, data là logical Order `{id,course_id,user_id,amount,currency,status,created_at}`. AC-12 quy định initial `status=PENDING`. Vật lý, amount/currency, user mapping, key generation và `data.id` ↔ #17 `order_id` chưa được xác nhận; không coi flow này là runtime.
8. Chỉ khi API/ID mapping được phê duyệt mới handoff ST-06 với order identifier. ST-06/#17 là POST riêng sau #16; không khởi tạo payment hoặc ghi danh từ client callback.
9. Lỗi #08 xử lý theo API #08 (404 hoặc 500 hiện hành); lỗi #16 chỉ dùng status/business codes trong catalog 401/403/422/500. UI copy, retry behavior, idempotency và trạng thái lưu sau lỗi chưa có contract; không tự thêm.

### Current behavior

- Mở HTML trực tiếp luôn hiển thị trạng thái unavailable. Không có route state, gọi #08, #16, xác nhận, loading, validation, cache hoặc mutation.
- CTA #11 điều hướng theo HTML tới `/courses`; label nói quay lại kiểm tra ghi danh nhưng không truyền `courseId`.
- Study Web không có editable app source/router/package manifest; `/student/checkout/:courseId` chưa được wire.
- API #08 có route/module/query/mapper và test source hiện hành. Test source không được chạy trong phiên này và không chứng minh database/deployment live.
- Không tìm thấy API #16 route/module/query/model/test trong Study Server. API #16 là contract design-only; không có order side effect hiện hành được xác minh.

### API boundary

| API | Request / quyền | Success | Error/current boundary | Tác động |
|---|---|---|---|---|
| #08 | `GET /api/v1/courses/{course_id}`; Public; `course_id:int64` | 200 `DESIGN_RESOURCE_RETRIEVED`; current envelope `Page<Course>` singleton | Catalog/current source: 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`; current code maps invalid ID or missing/unpublished course to 404; query/mapping error to 500 | Read-only; không sửa enrollment/order. Current SQL dùng `LEFT JOIN users`; Draft API #08 mô tả `INNER JOIN`, cần giữ discrepancy. |
| #16 | `POST /api/v1/orders`; Bearer JWT; role Student; body `{course_id:int64!, payment_provider:PaymentProvider!}` | Contract: 201 `DESIGN_RESOURCE_CREATED`, `ApiEnvelope<Order>` | Catalog: 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`; #16 chưa có runtime response | AC-12 chỉ yêu cầu tạo logical Order `PENDING` ở paid branch; physical write/transaction/idempotency chưa có nguồn. |

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

| State | Điều kiện / dữ liệu | Kết quả / chuyển tiếp | Tình trạng |
|---|---|---|---|
| `web-unwired` | Không có app source/router cho Study Web | Không có route UI ST-05 để thực thi | Current source status |
| `prototype-static-unavailable` | Mở `code.html` | Hiển thị #9/#10 và CTA #11; không gọi #08/#16 | Current HTML only |
| `route-auth-pending` | Mở candidate `/student/checkout/:courseId` | Cần Student guard và ID mapping trước data flow | Expected; chưa wire |
| `course-loading` | EV-02 GET #08 đang xử lý | Chờ 200/404/500; không tạo Order trong lúc này | Expected; UI chưa có |
| `course-ready-terms-blocked` | #08 200 với course PUBLISHED | Course read thành công; chờ approved amount/currency/provider/terms trước confirm | Expected; contract chưa đủ |
| `confirming` | Terms và provider được phê duyệt, Student đang chờ explicit action | Confirm đưa sang `order-creating`; không auto-submit | Inventory expected; current confirm control absent |
| `order-creating` | Một thao tác confirm hợp lệ, POST #16 đang chờ | Chờ response; no repeat/retry policy established | Inventory expected; #16 unwired |
| `course-unavailable` | #08 404 | Hiện course unavailable state; không nhầm thành #16 error | API #08 current; UI chưa định nghĩa |
| `course-read-error` | #08 500 | Hiện lỗi đọc/mapper; không chuyển thành 404 | API #08 current; UI chưa định nghĩa |
| `order-validation-error-422` | #16 trả 422 | Giữ lỗi theo response envelope; không tự tạo field messages | Catalog expected only; #16 unwired |
| `order-error` | #16 trả 401/403/500 hoặc request không hoàn tất | Auth/permission/server/network presentation và retry policy chưa được phê duyệt | Inventory state name; API contract/current UI incomplete |
| `order-created-handoff-blocked` | #16 contract success 201 | Candidate Order data được nhận; ST-06 chỉ sau khi `data.id` → `order_id` mapping và #17 flow được chốt | Expected design; #16/#17 unwired |
| `back-to-courses` | Click #11 | Current destination `/courses`; không giữ course context | Current HTML anchor |
| `return-to-ST-04` | Desired return per inventory | Route/data contract chưa có; không phải behavior hiện hành | Expected; blocked |

### Điều hướng và payload

| Từ | Điều kiện | Đến | Dữ liệu chuyển | Tình trạng |
|---|---|---|---|---|
| ST-04 | Backend/AC xác nhận nhánh paid | ST-05 candidate route | `courseId` candidate; quy tắc `course_id:int64` ở client chưa chốt | Expected; route unwired |
| ST-05 | Revalidation + terms/provider được phê duyệt; explicit confirm; #16 success | ST-06 | Inventory gọi `order_id`; API #16 trả `data.id:int64`; equivalence cần confirm | Expected; ID handoff blocked |
| ST-05 | CTA hiện tại | `/courses` | Không có ID hoặc return state | Current HTML only |
| ST-05 | Desired return | ST-04 | Course ID và return-state semantics cần quyết định | Expected; blocked |

Không được đánh dấu payment paid/enrolled hoặc chuyển tới ST-07/ST-08 từ response client, callback gateway hoặc trạng thái HTML. AC-12 đặt kiểm chứng payment/entitlement ở server-side flow; #17/#18/#19/#20 thuộc các DD sau. API #18 có discrepancy ID type (catalog int64; AC diagram UUID) và sequence node không nối.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: Revalidate #8; POST #16 một lần theo action người dùng; lưu order_id từ response.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [ST-05](../../screen_stitch/03_student/ST-05_kiem-tra-don-hang-checkout/ST-05.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
