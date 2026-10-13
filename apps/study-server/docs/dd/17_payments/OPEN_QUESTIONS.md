# OPEN_QUESTIONS

Các câu hỏi dưới đây chặn việc chuyển DD sang trạng thái final hoặc triển khai API #17. Draft giữ contract đã có và không tự chọn câu trả lời.

## Q-17-01 — Liên kết Order với Payment

**Bằng chứng**

- API #17 nhận order_id:int64; reusable Payment schema cũng có order_id:int64.
- DB.sql và ERD V1 có bảng payments nhưng không có cột payments.order_id hoặc bảng orders.
- API #16 DD giữ physical Order persistence ở SOURCE_REQUIRED.

**Vấn đề**

- Chưa có nguồn schema/relationship xác định cách resolve Order và gắn Payment vào Order.

**Ảnh hưởng**

- Không thể chốt query Order, insert/link Payment, response Payment.order_id hoặc transaction boundary.

**Cần quyết định**

- Cung cấp schema/relationship được phê duyệt cho Order–Payment và xác định migration/physical mapping.

## Q-17-02 — Quyền sở hữu và eligibility của Order

**Bằng chứng**

- Contract yêu cầu Student Bearer JWT và nhận order_id.
- API #16 DD ghi direct-call eligibility của Order chưa được xác định.
- API #17 contract chỉ khai báo 401, 403, 422, 503, 500; không khai báo 404/409.

**Vấn đề**

- Chưa rõ API #17 phải kiểm tra Order thuộc caller, trạng thái nào được thanh toán, hoặc xử lý Order không tồn tại/đã xử lý ra sao.

**Ảnh hưởng**

- Không thể đặc tả authorization/query branch hoặc thêm response code ngoài contract.

**Cần quyết định**

- Xác nhận ownership/status predicates và giữ/chỉnh contract error codes trong nguồn chuẩn trước implementation.

## Q-17-03 — Nguồn amount, currency, user và course

**Bằng chứng**

- Order schema có amount và currency; Payment schema có amount nhưng không có currency.
- payments có user_id, course_id và amount; bảng Order physical chưa có nguồn.

**Vấn đề**

- Chưa xác nhận Payment amount lấy từ Order snapshot hay nguồn khác; currency được cố định/đọc/lưu ở đâu; user/course lấy từ JWT hay Order.

**Ảnh hưởng**

- Không thể chốt insert values, response mapping, currency behavior hoặc đảm bảo giá trị thanh toán nhất quán.

**Cần quyết định**

- Cung cấp authoritative mapping cho amount/currency/user/course và quy tắc snapshot/định dạng tiền.

## Q-17-04 — Provider values và continuity với API #16

**Bằng chứng**

- API #16 nhận payment_provider:PaymentProvider; API #17 nhận provider:string.
- Payment schema dùng PaymentProvider; DB column là provider VARCHAR(50).
- API #16 DD chưa có enum member values hoặc semantics.

**Vấn đề**

- Allowed values, chuẩn hóa/case, adapter mapping và quan hệ giữa hai request fields chưa được xác định.

**Ảnh hưởng**

- Không thể chốt provider validation, giá trị lưu DB hoặc provider được gọi.

**Cần quyết định**

- Phê duyệt provider registry/enum và quy tắc truyền provider từ tạo Order sang khởi tạo Payment.

## Q-17-05 — Payment Gateway protocol và kết quả

**Bằng chứng**

- AC-12 nói Payment Gateway xử lý giao dịch; success đi tiếp, failure/cancel dừng flow.
- Contract có 202 Operation và 503 dependency-unavailable.
- Không có protocol, callback, credential, retry hoặc idempotency source trong catalog/diagram đã đọc.

**Vấn đề**

- Chưa rõ gateway request/confirmation, callback/webhook, retry, duplicate submission, timeout, hoặc cách phân biệt dependency failure với payment decline/cancel.

**Ảnh hưởng**

- Không thể chốt side effect trước/after 202, recovery, rollback hoặc error mapping.

**Cần quyết định**

- Cung cấp gateway integration contract cùng retry/idempotency, callback verification và outcome mapping.

## Q-17-06 — Payment status và transaction boundary

**Bằng chứng**

- payments.status có default PENDING trong DB.sql; PaymentStatus không có enum members trong API catalog.
- AC-12 chỉ mô tả success/failure/cancel ở mức flow.
- payments.transaction_code có UNIQUE constraint; created_at là NOT NULL không default trong DB.sql.

**Vấn đề**

- Chưa có status transitions, lúc ghi paid_at/transaction_code, xử lý duplicate transaction, transaction owner hoặc rollback behavior.

**Ảnh hưởng**

- Không thể chốt INSERT/UPDATE lifecycle, concurrency/idempotency hoặc consistency giữa gateway và DB.

**Cần quyết định**

- Xác nhận state machine, transaction/outbox boundary, duplicate policy và cách áp dụng các constraints hiện hữu.

## Q-17-07 — Operation persistence và lifecycle

**Bằng chứng**

- Reusable Operation có id:uuid, kind:OperationKind, status:OperationStatus, owner_id:int64, submitted_at, updated_at, optional completed_at và optional result:Payment.
- API #17 trả Operation với HTTP 202; không có Operation table/service trong current Study runtime hoặc DB.sql.

**Vấn đề**

- Chưa có enum values, initial state, persistence, worker/lifecycle, owner source hoặc quy tắc populate result.

**Ảnh hưởng**

- Không thể chốt response values, API #18 lookup hoặc theo dõi tác vụ trong runtime.

**Cần quyết định**

- Cung cấp Operation schema/storage/lifecycle và cách liên kết Payment result với operation.

## Q-17-08 — Kiểu operation_id của API #18

**Bằng chứng**

- Quy ước catalog ghi operation_id là uuid; Operation.id là uuid; AC diagrams khai báo API #18 path operation_id:uuid.
- Dòng API #18 trong list_api.md khai báo path operation_id:int64!.

**Vấn đề**

- Các nguồn trong cùng API catalog/diagram không thống nhất kiểu path.

**Ảnh hưởng**

- API #17 trả Operation.id nhưng client không thể poll API #18 theo một kiểu thống nhất nếu discrepancy còn nguyên.

**Cần quyết định**

- Chủ contract cập nhật/duyệt một kiểu thống nhất trong catalog và diagrams. DD API #17 không tự chọn hoặc sửa API #18.

## Q-17-09 — Nullability của user_id và course_id trong bảng payments

**Bằng chứng**

- DB.sql khai báo hai FK không có NOT NULL.
- DB_UNICA_TABLES gọi user_id/course_id là bắt buộc.

**Vấn đề**

- Tài liệu thiết kế bảng và SQL schema không thống nhất nullability.

**Ảnh hưởng**

- Không thể khẳng định constraint vật lý hoặc yêu cầu mapping của insert.

**Cần quyết định**

- Xác nhận schema artifact nào là baseline được duyệt và cập nhật source thiết kế tương ứng.

## Q-17-10 — Payment failure/cancel và error/Operation mapping

**Bằng chứng**

- AC-12 nói failure/cancel dừng flow.
- API #17 không có business code riêng cho payment decline/cancel ngoài các lỗi chung đã liệt kê.

**Vấn đề**

- Chưa rõ decline/cancel trả Operation hoàn tất với status/result nào hay xử lý theo một contract khác.

**Ảnh hưởng**

- Không thể đặc tả response/poll result hoặc client message mà không thêm behavior/code mới.

**Cần quyết định**

- Xác định state/result của Operation cho decline/cancel và cập nhật contract/diagram nếu có HTTP/business code mới.
