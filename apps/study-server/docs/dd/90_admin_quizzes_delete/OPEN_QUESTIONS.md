# Open Questions — API #90 Xóa quiz

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** `DELETE /api/v1/admin/quizzes/{quiz_id}`

Các đề xuất bên dưới giữ nguyên catalog và AC-35; chúng chưa được phê duyệt thành runtime/schema behavior.

## Q-90-01 — Tombstone và `deleted_at`

**Evidence:** AC-35 node n10 yêu cầu soft delete khi có attempts. Legacy `quizzes` có `status VARCHAR(20)` và `updated_at`, nhưng không có `deleted_at` hoặc status enum canonical. DeleteResult yêu cầu `deleted_at:date-time`.

**Đề xuất:** Dùng `status='DELETED'` làm tombstone và `updated_at` làm thời điểm xóa, rồi map timestamp đó vào `DeleteResult.deleted_at`. DELETE lặp lại là no-op 200, giữ nguyên timestamp. Đây là cách dùng lại cột hiện có, `DERIVED`.

**Cần xác nhận:** Giá trị `DELETED` có được chấp nhận không; có thể dùng `updated_at` làm thời điểm xóa không; timestamp phải UTC/offset nào; quiz đã tombstone có bất biến không; DELETE lặp lại có trả 200 không?

## Q-90-02 — Quiz không có attempt

**Evidence:** AC-35 ghi soft-delete khi quiz đã có attempts nhưng không mô tả nhánh không có attempt. Legacy DDL có FK chain choices → questions → quiz, không ghi cascade.

**Đề xuất:** Nếu không có bất kỳ attempt nào, hard delete choices → questions → quiz trong một transaction. Đây là `DERIVED` và chỉ dùng legacy relation làm candidate.

**Cần xác nhận:** Nhánh hard delete có được duyệt không; có thể còn dependency khác ngoài attempts/answers không; live FK có khớp legacy DDL không?

## Q-90-03 — Attempt được tạo đồng thời

**Evidence:** API #29 tạo `quiz_attempts` với trạng thái `IN_PROGRESS`; API #29 DD chưa chốt quiz-open state, concurrency hoặc locking.

**Đề xuất:** #90 và #29 phải đồng bộ kiểm tra/trạng thái trong transaction để một attempt không được tạo sau tombstone. Không thêm HTTP 409 vì catalog #90 không khai báo.

**Cần xác nhận:** Lock/isolation/recheck cụ thể và điều kiện API #29 từ chối quiz đã xóa.

## Q-90-04 — Visibility sau xóa trong AC-35

**Evidence:** #87 list, #89 update, #91 statistics là các nhánh của cùng AC-35; DD #91 hiện đã được tạo. AC-16 #29–#32 tạo, lưu, nộp và đọc attempt history.

**Đề xuất:** Không cho tạo/sửa quiz đã tombstone; giữ #30–#32 và #91 đọc history/statistics; mặc định ẩn tombstone khỏi #87, trừ khi filter Admin chọn rõ.

**Cần xác nhận:** List filter/default, update behavior, statistics visibility, repeated DELETE response và policy cho quiz đã xuất bản.

## Q-90-05 — Admin authorization và error wiring

**Evidence:** Catalog/AC-35 yêu cầu Admin và quiz-management permission; current Study auth helper chỉ có Student guard; API #90 path không nằm trong `DESIGN_CONTRACT_PATHS`.

**Đề xuất:** Tích hợp Admin + quiz-management authorization trước lookup; map exact catalog 401/403/404/422/500 codes.

**Cần xác nhận:** Admin claim/permission source và cách thêm dynamic path vào error-code selection.

## Kết quả macro-review AC-35

- Review #87–#91 hoàn tất ở mức tài liệu với trạng thái VERIFIED_WITH_OPEN_QUESTIONS.
- Đề xuất dùng chung: soft-delete khi có attempt và giữ attempt/answer history; hide tombstone khỏi #87 mặc định; #89 không thay đổi quiz có history hoặc tombstone; #29 không tạo attempt mới; #30–#32 giữ attempt đã tạo; #91 tổng hợp history còn lưu.
- Nhánh hard-delete khi không có attempt, tombstone value/timestamp, xử lý attempt đang làm và race/transaction vẫn cần xác nhận.
- Xem [Verification Report nhóm AC-35](../91_admin_quizzes_statistics/VERIFICATION_REPORT.md).
