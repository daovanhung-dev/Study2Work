# OPEN_QUESTIONS — Study API #58

Status: `Draft — Needs Confirmation`. Các câu hỏi dưới đây chặn chốt query/response để code; DD giữ nguyên contract trực tiếp và không tự sửa catalog.

| ID | Câu hỏi cần xác nhận | Bằng chứng và ảnh hưởng | Khuyến nghị đơn giản | Mức độ |
|---|---|---|---|---|
| Q-58-01 | Endpoint danh sách cần trả `SupportRequest` đơn, `SupportRequest[]` hay `Page<SupportRequest>`? | URI/name và AC-24 node n1 là danh sách; catalog/diagram node n2 trả `ApiEnvelope<SupportRequest>`. 0 hoặc nhiều record không thể biểu diễn bằng object đơn. | Xác nhận collection response; phương án đơn giản là `ApiEnvelope<SupportRequest[]>` với hai filter hiện có. Chỉ thêm pagination khi có requirement. | BLOCKING — contract |
| Q-58-02 | Physical support model nào là nguồn được duyệt cho AC-24, và API ID dùng int64 hay UUID? | Legacy DB.sql/ERD không có support tables. Pilot có support_tickets/support_messages với UUID, khác ID int64 của SupportRequest/Message. | Chọn model/schema và ID contract trước khi chốt Q1/Q2; không map UUID sang int64 giả. | BLOCKING — data model |
| Q-58-03 | Support request liên kết với course bằng quan hệ nào để hỗ trợ `course_id` filter và `data.course_id`? | Catalog khai báo cả query và response course_id; pilot support_tickets không có course_id/course_version_id. | Bổ sung/duyệt quan hệ domain hoặc bỏ course filter/field qua contract change; không nối suy đoán bằng enrollment. | BLOCKING — query/response |
| Q-58-04 | Quyền Mentor dựa trên ticket được assigned trực tiếp, ownership của course, hay cả hai? JWT principal map sang khóa nào? | AC-24 yêu cầu request thuộc phạm vi Mentor; pilot assigned_to_subject_id nullable UUID; runtime guard hiện chỉ xác nhận STUDENT. | Dùng một predicate được duyệt và thống nhất với #59–#61; assignment candidate chỉ dùng sau khi identity binding được xác nhận. | BLOCKING — authorization |
| Q-58-05 | Các giá trị hợp lệ của SupportStatus là gì và query status có exact match/case-insensitive behavior nào? | Catalog chỉ khai báo SupportStatus và query string. Pilot có OPEN, IN_PROGRESS, WAITING_LEARNER, RESOLVED, CANCELLED nhưng là schema khác. | Duyệt enum và filter rule; giữ pilot values là candidate, không áp dụng ngầm. | BLOCKING — validation |
| Q-58-06 | List #58 phải tải toàn bộ `messages[]` cho mỗi request hay trả tóm tắt và để #59 tải thread? Quy tắc thứ tự và giới hạn? | SupportRequest bắt buộc messages[]; AC-24 có API #59 đọc nội dung/thread riêng; catalog không có pagination hoặc message limit. | Chốt projection list/detail; nếu giữ messages[], định nghĩa thứ tự và giới hạn trước khi triển khai. | BLOCKING — response/performance |
| Q-58-07 | Làm sao map student/message author sang UserSummary và attachments sang UploadAsset, gồm URL ký và trạng thái quét? | Pilot dùng UUID subject/file IDs; file_objects lưu storage_key, không lưu public URL; author có LEARNER/STAFF; contract cần numeric IDs và đủ metadata. | Chọn identity projection và file resolver/provider; không trả storage_key hoặc bịa field. | BLOCKING — response/security |
| Q-58-08 | Query sai kiểu/format xử lý bằng status/code nào, khi catalog không khai báo 422 cho #58? Error envelope data sẽ theo guideline null hay helper hiện hành {}? | FastAPI query parsing có thể phát validation error; #58 chưa được thêm DESIGN_CONTRACT_PATHS. API Guidelines và current helper khác nhau về data lỗi. | Chốt error contract và cập nhật allowlist/helper cùng task wiring; không thêm error row vào DD hiện tại. | BLOCKING — error contract |
| Q-58-09 | Empty result, thứ tự request, page size và giới hạn response được xử lý thế nào? | Đây là endpoint list nhưng không có collection shape, pagination, sort hoặc empty-result contract. | Chốt cùng Q-58-01; tối thiểu collection rỗng trả thành công với mảng rỗng nếu chủ API phê duyệt. | BLOCKING — list behavior |

## Quy tắc giữ nguyên trong DD hiện tại

- Không tự đổi catalog hay diagram để chọn một phương án.
- Không chọn record đầu tiên, cắt kết quả, thêm status enum hoặc nối bảng ngoài nguồn.
- Không xem V1-PILOT là schema runtime hoặc là model đã được chủ API duyệt.
- Sau khi #59–#61 được tạo, macro-review toàn bộ AC-24 để kiểm tra scope Mentor, trạng thái, thread/messages, attachment và response envelope nhất quán.
