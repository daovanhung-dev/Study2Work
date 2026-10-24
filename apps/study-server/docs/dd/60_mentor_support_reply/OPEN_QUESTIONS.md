# OPEN_QUESTIONS — Study API #60

Status: `Draft — Needs Confirmation`. Proposal hỗ trợ triển khai được đánh dấu `DERIVED`; contract và nguồn vật lý chưa được sửa/khẳng định.

| ID | Câu hỏi cần xác nhận | Bằng chứng và ảnh hưởng | Khuyến nghị đơn giản | Mức độ |
|---|---|---|---|---|
| Q-60-01 | `attachment refs` có wire key `attachment_refs` và encoding comma-separated `UploadAsset.id` int64 không? | #60/#35/#47 dùng string ref labels; #47 đề xuất wire key `asset_refs` nhưng encoding opaque; #34 chưa có confirmed ID registry. | Dùng một convention chung: snake_case `*_refs`, comma-separated UploadAsset IDs, empty string nghĩa none; chốt đồng thời #35/#47/#60. | BLOCKING — shared contract |
| Q-60-02 | API #34 lưu asset metadata/identity ở đâu và xác thực ownership/purpose/status bằng cách nào? | #34 DD không chỉ định DB write; V1-PILOT `file_objects` dùng UUID; UploadAsset cần int64 id/url/status. | Chọn registry/resolver và ID mapping trước khi reply chấp nhận refs; không dùng raw URL/storage key. | BLOCKING — security/data |
| Q-60-03 | Support model nào được duyệt và API ID dùng int64 hay UUID? | Legacy DB thiếu support tables; pilot support_tickets/support_messages dùng UUID; API #60/SupportRequest dùng int64. | Chọn một canonical schema/ID contract cho #58–#61 trước implementation. | BLOCKING — data model |
| Q-60-04 | Mentor principal map sang `author_subject_id` nào và có được assigned request không? | AC-24 scope Mentor; current Study guard Student-only; pilot assigned_to_subject_id nullable UUID. | Duyệt identity mapping/predicate chung cho #58–#61; không chỉ dựa trên request_id. | BLOCKING — authorization |
| Q-60-05 | Mentor reply có dùng `author_type=STAFF` và luôn learner-visible (`is_internal=false`) không? | Pilot enum LEARNER/STAFF và default is_internal=false; diagram chỉ nói Mentor nhập phản hồi, không có internal note mode. | Coi Mentor là STAFF và reply learner-visible; xác nhận với owner. | BLOCKING — message policy |
| Q-60-06 | `message` có bắt buộc nonblank không; có giới hạn độ dài/format nào? | Catalog chỉ khai string required và 422; không có limits. | Reject whitespace-only, giữ nguyên text, chưa đặt min/max; confirm proposal. | NEEDS CONFIRMATION — validation |
| Q-60-07 | Empty `attachment_refs` có hợp lệ khi không đính kèm không; duplicate/malformed token xử lý ra sao? | Field required string nhưng no encoding/empty/duplicate rules. | Cho phép `""` là no attachments; 422 nếu token không phải UploadAsset ID hợp lệ; chốt duplicate policy. | BLOCKING — request contract |
| Q-60-08 | Reply được gửi khi request đã RESOLVED/CANCELLED không? Nếu được, có reopen hay giữ nguyên trạng thái? | AC-24 đưa resolve qua #61; không nêu post-resolve behavior; catalog #60 không có 409. | Không tự reopen hoặc update status; chốt nếu reply cần bị từ chối bằng 422 đã khai báo. | BLOCKING — lifecycle |
| Q-60-09 | Response rehydrate có trả toàn bộ thread, thứ tự và giới hạn nào? | Success trả SupportRequest; #59 đọc conversation; catalog không định nghĩa order/limit. | Trả thread theo một stable order được duyệt, có bound; bảo đảm message vừa gửi xuất hiện. | BLOCKING — response/performance |
| Q-60-10 | Nếu insert thành công nhưng response mapping/asset resolver lỗi, transaction có rollback không? | Current DB helper giao transaction caller; AC-24 không nêu rollback. | Giữ insert và reload trong một transaction, commit khi full response sẵn sàng; confirm với implementation owner. | NEEDS CONFIRMATION — transaction |
| Q-60-11 | Catalog body wire media type là JSON? | Body là string fields nhưng catalog không khai Content-Type. | Dùng application/json làm DERIVED candidate; xác nhận nếu gateway/API standard yêu cầu. | NEEDS CONFIRMATION — transport |

## Quy tắc giữ nguyên trong DD hiện tại

- Không sửa catalog fields/status/error codes; không thêm 409, 503, notification hoặc status mutation.
- Candidate V1-PILOT `support_messages` không phải runtime/live schema; không cast UUID sang int64.
- `attachment_refs` CSV, blank-message validation, STAFF, `is_internal=false` và transaction boundary vẫn là proposal DERIVED.
- Sau DD #61, macro-review AC-24 #58–#61 và đối chiếu ref convention với #34/#35/#47 trước khi gọi nhóm này implementation-ready.
