# OPEN_QUESTIONS

Các câu hỏi này chặn việc chuyển DD sang Final hoặc triển khai API #18. Bản Draft giữ các khai báo hiện có và không tự chọn câu trả lời.

## Q-18-01 — Kiểu operation_id

**Bằng chứng**

- Quy ước trong list_api.md khai báo operation_id và traceId là UUID.
- Reusable Operation schema khai báo id:uuid.
- API #18 row khai báo path operation_id:int64!.
- AC-12, AC-25, AC-36 và AC-38 diagrams khai báo operation_id:uuid.

**Vấn đề**

- API row không đồng nhất với quy ước, schema dùng chung và diagrams.

**Ảnh hưởng**

- Client không thể đảm bảo ID trả về từ Operation dùng được để gọi API #18.

**Cần quyết định**

- Contract owner chọn một kiểu chuẩn và cập nhật mọi nguồn canonical liên quan trước khi DD/API được chốt.

## Q-18-02 — Authorization: owner-only hay owner/Admin

**Bằng chứng**

- API #18 row mô tả Bearer JWT; operation owner.
- Diagrams ghi RBAC Student|Mentor|Admin; owner only.
- Phần Operation tracking của catalog nói chỉ owner hoặc Admin được xem.
- Catalog chưa định nghĩa claim hoặc predicate liên kết caller với owner_id.

**Vấn đề**

- Chưa rõ Admin được bypass ownership hay chỉ owner được xem.

**Ảnh hưởng**

- Không thể chốt role matrix, authorization query hoặc cách xử lý operation của người khác.

**Cần quyết định**

- Xác nhận owner/Admin policy, role eligibility và nguồn caller identity/owner mapping trong contract chuẩn.

## Q-18-03 — Study Operation storage, enums và lifecycle

**Bằng chứng**

- Study reusable Operation schema khai báo id, kind, status, owner_id, submitted_at, updated_at, optional completed_at và optional result.
- Study DB.sql, DB_UNICA_TABLES.md và DB_UNICA_ERD.drawio không định nghĩa Study Operation table.
- Current Study route/module/query/test scan không tìm thấy API #18.
- Có một bảng operations trong Work Server schema, nhưng FK tham chiếu work_users; không có contract xác nhận dùng chung với Study.
- API #17 DD cũng ghi persistence, enum values, initial state, lifecycle và owner source là SOURCE_REQUIRED.

**Vấn đề**

- Chưa có nguồn xác nhận Study physical storage, OperationKind/OperationStatus values, state transitions, producer/worker lifecycle, retention hoặc owner source.

**Ảnh hưởng**

- Không thể xác định cách truy vấn, dữ liệu response thực tế, terminal state hoặc bảo đảm operation có thể poll được.

**Cần quyết định**

- Cung cấp approved Study persistence/query source, enum registry, lifecycle/state machine, owner source và retention policy; xác nhận rõ nếu Work Server table có quan hệ cross-service.

## Q-18-04 — Operation result theo từng loại job và producer response contract

**Bằng chứng**

- Reusable Operation schema khai báo optional result:Payment.
- Operation tracking section nói payments, mentor notifications, admin notifications và report export trả Operation.
- Catalog rows cho API #93 admin notification và API #103 report export lần lượt khai báo ApiEnvelope<Notification> và ApiEnvelope<Report>; điều này không khớp với Operation tracking summary.
- Catalog reusable schemas cũng có NotificationDelivery, Report, ExportAsset và OperationError, nhưng không chỉ rõ trường hợp nào nằm trong Operation.result.

**Vấn đề**

- Không rõ result của operation notification/export có dùng Payment, NotificationDelivery, Report, ExportAsset hay shape khác; producer rows chưa nhất quán.

**Ảnh hưởng**

- Client không thể giải mã kết quả polling theo kind; response schema có thể lệch với API trả operation_id ban đầu.

**Cần quyết định**

- Xác định result schema theo từng OperationKind và thống nhất success response của các producer với Operation tracking contract.

## Q-18-05 — Semantics của 403 và 404

**Bằng chứng**

- API #18 khai báo cả 403 DESIGN_ACCESS_DENIED và 404 DESIGN_RESOURCE_NOT_FOUND.
- Business-code definition nói 403 bao gồm sai role, ownership hoặc access; 404 dùng khi resource/operation không tồn tại.

**Vấn đề**

- Chưa rõ operation tồn tại nhưng thuộc user khác trả 403 hay được ẩn như 404; chưa xác nhận thứ tự authorization và existence check.

**Ảnh hưởng**

- Không thể chốt nhánh lỗi, leakage policy hoặc test cases tương ứng.

**Cần quyết định**

- Phê duyệt behavior cho missing operation, wrong owner, disallowed role và Admin access; cập nhật catalog/diagrams nếu code mapping thay đổi.
