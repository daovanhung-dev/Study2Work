# OPEN_QUESTIONS

## Q-16-01 — Order persistence schema

**Bằng chứng**

- API catalog định nghĩa logical response Order gồm id, course_id, user_id, amount, currency, status, created_at.
- AC-12 yêu cầu tạo Order = PENDING.
- DB_UNICA ERD V1 ghi không tách orders; DB_UNICA_TABLES nêu API #16 có liên quan Order nhưng ERD không có bảng này.
- Checked-in DB.sql khai báo payments, không khai báo orders.

**Vấn đề**

- Chưa có physical table, column, key, constraints, transaction boundary hoặc idempotency policy cho Order.

**Ảnh hưởng**

- Không thể chốt INSERT mapping, rollback, response source hoặc duplicate handling.
- Không thể thay Order bằng payments; đó là logical resource/API riêng.

**Quyết định authoring**

- Ghi Order là logical resource và giữ physical persistence ở SOURCE_REQUIRED.
- Cần nguồn schema được phê duyệt trước runtime implementation.

## Q-16-02 — PaymentProvider enum và ý nghĩa request field

**Bằng chứng**

- API #16 body yêu cầu payment_provider:PaymentProvider!.
- API #16 response schema Order không có field provider.
- API #17 body nhận provider:string! riêng khi khởi tạo/xác nhận payment.
- Catalog/schema được đọc không liệt kê member values của PaymentProvider.

**Vấn đề**

- Allowed values chưa được định nghĩa.
- Chưa rõ API #16 dùng provider để validation, lưu/forward, hay giữ lại ở bước gọi API #17.

**Ảnh hưởng**

- Không thể chốt enum validation, mapping hoặc continuity giữa tạo Order và payment.

**Quyết định authoring**

- Giữ field/type như contract; member values và semantics là SOURCE_REQUIRED.
- Không đưa provider vào Order response hoặc payment persistence mapping khi chưa có nguồn.

## Q-16-03 — Amount và currency

**Bằng chứng**

- Order schema có amount:decimal-string và currency:string.
- Contract/AC-12 được đọc không chỉ rõ amount source, discount/tax rule hoặc currency value.

**Vấn đề**

- Chưa xác nhận amount có lấy trực tiếp từ courses.price hay áp dụng quy tắc khác.
- Chưa xác nhận currency source/default.

**Ảnh hưởng**

- Response và Order INSERT chưa thể có value mapping an toàn.

**Quyết định authoring**

- Giữ hai field trong expected response; physical/value source là SOURCE_REQUIRED.

## Q-16-04 — OrderStatus enum

**Bằng chứng**

- Schema dùng type OrderStatus.
- AC-12 chỉ xác nhận trạng thái lúc tạo là PENDING.

**Vấn đề**

- Các trạng thái hợp lệ sau bước tạo và transition rules chưa được nguồn xác nhận.

**Ảnh hưởng**

- Không thể định nghĩa enum đầy đủ hoặc status transitions trong API #16 DD.

**Quyết định authoring**

- Chỉ ghi trạng thái khởi tạo PENDING; không suy diễn các trạng thái khác.

## Q-16-05 — Eligibility khi gọi trực tiếp API #16

**Bằng chứng**

- API catalog đánh dấu API #16 Conditional, cho paid course.
- AC-12 sequence kiểm tra course, enrollment hiện có và nhánh free/paid trước khi gọi API #16.
- API #16 contract chỉ khai báo 401, 403, 422 và 500.

**Vấn đề**

- Chưa rõ API #16 có tự kiểm tra course tồn tại/paid status/already-enrolled khi được gọi trực tiếp.
- Không có 404 hoặc 409 trong error contract của API #16.

**Ảnh hưởng**

- Không thể thêm response/error branch hoặc xác định endpoint precondition ngoài flow context.

**Quyết định authoring**

- Ghi rõ AC-12 context, giữ nguyên danh sách error contract, và chờ owner xác nhận direct-call behavior trước implementation.

