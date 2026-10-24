# OPEN_QUESTIONS — Study API #59

Status: `Draft — Needs Confirmation`. Các câu hỏi dưới đây chặn chốt mapping để code; DD giữ nguyên contract trực tiếp và không tự sửa catalog.

| ID | Câu hỏi cần xác nhận | Bằng chứng và ảnh hưởng | Khuyến nghị đơn giản | Mức độ |
|---|---|---|---|---|
| Q-59-01 | Physical support model nào là nguồn được duyệt cho AC-24, và ID API dùng int64 hay UUID? | Legacy Study schema không có support tables; V1-PILOT dùng UUID trong khi SupportRequest/SupportMessage yêu cầu int64. | Chọn schema/model và chốt ID contract trước khi viết query; không ép cast UUID. | BLOCKING — data model |
| Q-59-02 | Mentor principal map sang khóa nào và quyền dựa trên assignment nào? | AC-24 yêu cầu request thuộc phạm vi Mentor; current guard chỉ hỗ trợ Student; pilot `assigned_to_subject_id` nullable UUID. | Chọn một predicate được duyệt, thống nhất với #58/#60/#61, và xác nhận identity mapping. | BLOCKING — authorization |
| Q-59-03 | Quy tắc phân biệt request không tồn tại (404) với request ngoài scope (403) là gì? | Catalog có cả hai code nhưng chưa quy định check order hoặc privacy policy. | Xác nhận existence-vs-scope ordering để tránh resource enumeration ngoài ý muốn. | BLOCKING — security/error |
| Q-59-04 | Request liên kết course bằng quan hệ nào để trả `course_id`? | Contract bắt buộc course_id; pilot support_tickets không có course_id/course_version_id. | Bổ sung/chọn quan hệ domain hoặc điều chỉnh contract có phê duyệt. | BLOCKING — query/response |
| Q-59-05 | Thread có gồm message nội bộ, thứ tự nào, và có giới hạn số lượng không? | Contract yêu cầu `messages[]`; pilot có `is_internal` và `sent_at`, nhưng catalog/diagram không nêu visibility/order/limit. | Chốt visibility, thứ tự ổn định và giới hạn; không lấy pilot index làm API rule. | BLOCKING — response/security/performance |
| Q-59-06 | Làm sao map learner/mentor authors sang UserSummary đầy đủ? | Contract cần int64 id, non-null full_name và optional avatar_url; pilot subject/profile IDs là UUID và profile full_name nullable. | Chọn identity projection và xác nhận null/fallback policy cho tên/avatar. | BLOCKING — response mapping |
| Q-59-07 | Attachment resolver cung cấp URL, content type, size và UploadStatus thế nào? | Pilot file refs là UUID; file_objects lưu storage key/metadata, chưa có approved signed URL hoặc enum mapping. | Chọn resolver, MIME source, scan eligibility và UploadStatus mapping; không trả storage_key. | BLOCKING — security/data mapping |
| Q-59-08 | `SupportStatus` và `UploadStatus` gồm những giá trị nào? | Catalog chỉ khai báo type; pilot status values thuộc schema khác, chưa được duyệt cho API. | Duyệt enum/API mapping trước khi chốt examples và validation. | BLOCKING — contract |
| Q-59-09 | `resolved_at`, avatar_url và optional fields dùng null hay omit? | Contract đánh dấu optional nhưng không quy định serialization semantics. | Chốt null-vs-omit convention nhất quán với clients. | NEEDS CONFIRMATION — serialization |
| Q-59-10 | Path sai kiểu/overflow xử lý thế nào khi catalog #59 không khai báo 422? | FastAPI có thể xử lý parse error trước view; route chưa wired và middleware allowlist chưa có path #59. | Chốt status/business code trong giới hạn contract trước khi wiring. | BLOCKING — error contract |
| Q-59-11 | Khi thread không có message hoặc chỉ có attachment đã bị quarantine, response/visibility xử lý ra sao? | Catalog yêu cầu arrays/UploadAsset nhưng không nêu empty hoặc blocked-file policy. | Xác nhận empty collection và file eligibility behavior với chủ API. | NEEDS CONFIRMATION — response/security |

## Quy tắc giữ nguyên trong DD hiện tại

- Không đổi contract int64, endpoint, response shape hoặc error set bằng suy đoán.
- Không coi V1-PILOT là live schema hoặc model được chủ API duyệt.
- Không tự đưa message nội bộ, giả mạo ID numeric, suy ra enum, hoặc tạo URL từ storage key.
- Giữ AC-24 macro-review pending đến khi #60 và #61 có DD.
