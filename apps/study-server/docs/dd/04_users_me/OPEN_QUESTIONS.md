# OPEN_QUESTIONS — Study API #04

**Trạng thái:** `Draft — Needs Confirmation`
**Endpoint:** `GET /api/v1/users/me`

## Q-04-01 — Claim names dùng chung giữa login và current-user là gì?

**Bằng chứng:** AC-02 diagram ghi token claims `user_id`, `role`; current API #03 tạo access JWT với `sub` và `roles`, còn API #04 helper parse `sub` thành numeric user ID và yêu cầu list `roles`.

**Ảnh hưởng:** API #03 và #04 chưa có claim contract chung được catalog khóa; client/token issuer có thể không khớp diagram.

**Cần xác nhận:** Chốt subject, role claim shape/casing và phiên bản token contract cho #03/#04. Không đổi source hoặc diagram trong DD task.

## Q-04-02 — Quyền `permissions` trong AC-02 lấy từ đâu?

**Bằng chứng:** AC-02 nói API #04 đọc profile, role và permissions. Catalog response là `UserProfile`, không khai báo permissions; current #04 query/model không đọc permissions table/service và response không có field này.

**Ảnh hưởng:** Client không thể dựa vào API #04 hiện tại để nhận permissions theo flow AC-02.

**Cần xác nhận:** Xác định source/schema/API cho permissions hoặc xác nhận bỏ yêu cầu này khỏi flow; không tự thêm response field hay bảng.

## Q-04-03 — Profile có cần lưu/trả `bio` xuyên suốt AC-11 không?

**Bằng chứng:** Catalog `UserProfile` đánh dấu `bio` optional. AC-11 và request API #14 ghi `bio:string!`; current #04 SELECT/model không có `bio`. Current #14 `ProfileUpdateRequest` không khai báo `bio`, dùng `extra="ignore"`, và query/update không ghi cột này; response #14 dùng cùng `UserProfile` model nên cũng omit `bio`.

**Ảnh hưởng:** UI có thể gửi bio nhưng source bỏ qua; sau reload API #04 không thể trả giá trị vừa gửi.

**Cần xác nhận:** Chọn nguồn lưu và required/null/omit semantics cho `bio`, rồi đồng bộ schema, API #14 request/update/response, API #04 query/model và catalog/diagram. Không tạo column hoặc giá trị giả trong DD.

## Q-04-04 — Role và trạng thái tài khoản có cần được đọc lại từ DB trước khi cho phép xem hồ sơ?

**Bằng chứng:** Current guard yêu cầu `STUDENT` trong JWT `roles`; SQL chỉ lọc theo `users.id`, không lọc `users.status` và không so sánh `users.role` với token role. Response role/status lấy từ DB.

**Ảnh hưởng:** Token Student còn hạn có thể qua guard sau khi role/status DB thay đổi; response có thể trả role khác role đã cấp quyền.

**Cần xác nhận:** Chốt freshness/revocation policy và quyền truy cập với tài khoản đã khóa/đổi role. Không suy thêm predicate vào DD.

## Q-04-05 — JWT hợp lệ nhưng không còn user row nên trả mã nào?

**Bằng chứng:** Catalog khai báo 401/403/500, không có 404. Current view map query result `None` thành `401 DESIGN_AUTHENTICATION_REQUIRED` và không rollback.

**Ảnh hưởng:** Chưa rõ đây là token không còn hợp lệ, account đã xóa hay lỗi nhất quán dữ liệu; consumer không có semantics cụ thể.

**Cần xác nhận:** Duyệt mapping 401 hiện tại hay một semantics khác trong error contract; không tự thêm 404.

## Q-04-06 — Sau login có chủ ý gọi lại API #04 để nạp profile không?

**Bằng chứng:** AC-02 yêu cầu #03 login rồi #04 đọc profile/role/permissions. Current #03 success đã trả profile cơ bản cùng token; #04 đọc lại profile từ `users`.

**Ảnh hưởng:** Chưa rõ lần fetch thứ hai nhằm lấy dữ liệu mới nhất, permissions, hay là bước dư; hiện response #04 không có permissions.

**Cần xác nhận:** Chốt handoff/session flow, nguồn dữ liệu sau login và trách nhiệm role routing; đồng bộ hai DD sau khi được duyệt.

## Q-04-07 — Upload avatar và lưu URL cần bảo đảm nhất quán thế nào?

**Bằng chứng:** API #13 upload object rồi trả URL, không ghi DB; API #14 ghi profile URL trong request riêng. Hai thao tác không chung transaction/compensation trong source.

**Ảnh hưởng:** Nếu cập nhật #14 lỗi sau khi #13 upload thành công, object storage và URL trong DB có thể không phản ánh cùng một lần thay đổi; hành vi này được suy ra từ hai side effect độc lập, chưa có flow bù trừ trong diagram/source đã đọc.

**Cần xác nhận:** Chốt retry/cleanup/overwrite và cách xử lý khi #14 thất bại; không thêm side effect hoặc compensation vào DD như hành vi đã có.

## Q-04-08 — Notation request API #04/#14 cần chuẩn hóa thế nào?

**Bằng chứng:** Catalog/AC-02/AC-11 lặp `auth{bearer_jwt!}`. Catalog API #14 dùng literal `avatar_url...:uri!`, chưa thể hiện rõ tên field hay required/null behavior.

**Ảnh hưởng:** API #04 có thể biểu diễn một Authorization header duy nhất theo route hiện tại; contract API #14 vẫn còn mơ hồ cho client và persistence.

**Cần xác nhận:** Dọn notation tại nguồn chuẩn; giữ yêu cầu #04 thành một header và không đoán ý nghĩa `avatar_url...`.

## Q-04-09 — `users.status` có bắt buộc NOT NULL trong schema được triển khai không?

**Bằng chứng:** Current API #04 model khai báo `status: str` bắt buộc. Checked-in `DB.sql` candidate định nghĩa `status VARCHAR(20) DEFAULT 'ACTIVE'` nhưng không có `NOT NULL`; live schema chưa kiểm tra.

**Ảnh hưởng:** Nếu row có `status = NULL`, `UserProfile.model_validate` lỗi và current view trả `500 DESIGN_INTERNAL_ERROR` dù cột được SELECT thành công.

**Cần xác nhận:** Kiểm tra deployed schema và chốt status requiredness/constraint hoặc response policy. Không xem DDL candidate là bằng chứng live và không tự thêm constraint trong DD.
