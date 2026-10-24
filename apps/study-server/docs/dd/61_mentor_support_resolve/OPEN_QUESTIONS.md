# OPEN_QUESTIONS — Study API #61

Status: `Draft — Needs Confirmation`. Contract trực tiếp và behavior trong AC-24 được giữ nguyên; proposal DERIVED chưa được coi là implementation fact.

| ID | Câu hỏi cần xác nhận | Bằng chứng và ảnh hưởng | Khuyến nghị đơn giản | Mức độ |
|---|---|---|---|---|
| Q-61-01 | SupportRequest dùng physical table và ID type nào: API int64 hay pilot UUID? | Legacy DB thiếu support model; V1-PILOT `support_tickets.id` là UUID. Chặn mọi UPDATE predicate. | Chọn một schema canonical; không cast hoặc giả lập ID. | BLOCKING — data model |
| Q-61-02 | Mentor principal map sang identity key nào và “request thuộc scope” nghĩa là assignment trực tiếp hay scope theo course? | AC-24 yêu cầu request thuộc phạm vi Mentor; pilot có `assigned_to_subject_id` nullable UUID; current Study guard chỉ Student. | Dùng direct assignment làm candidate đơn giản; phê duyệt claim/key và dùng chung ở #58–#61. | BLOCKING — authorization |
| Q-61-03 | SupportStatus gồm những giá trị nào và status nào được chuyển sang RESOLVED? | Diagram nêu YES → RESOLVED và NO giữ OPEN; pilot enum là OPEN, IN_PROGRESS, WAITING_LEARNER, RESOLVED, CANCELLED nhưng chưa được duyệt cho API. | Cho phép OPEN → RESOLVED; RESOLVED lặp lại idempotent; xác nhận hành vi cho state còn lại. | BLOCKING — lifecycle |
| Q-61-04 | Gọi lại API sau khi request đã RESOLVED trả success và giữ nguyên `resolved_at` không? | Catalog có PATCH cập nhật; diagram không nói retry semantics. | Trả 200 với resource hiện tại, không ghi đè thời điểm resolve ban đầu. | NEEDS CONFIRMATION — idempotency |
| Q-61-05 | `resolved_at` có phải ghi khi chuyển sang RESOLVED và lấy thời gian từ server/DB nào? | Catalog có `resolved_at?`; pilot có timestamptz nhưng diagram chỉ nêu status. | Gán một timestamp server lần đầu; giữ nguyên khi retry. | NEEDS CONFIRMATION — timestamp |
| Q-61-06 | Request không tồn tại và request ngoài Mentor scope được phân biệt 404/403 theo thứ tự nào? | Catalog khai báo cả hai; #59 để check-order/privacy open. | Trả 404 cho missing, 403 cho existing-but-out-of-scope nếu không có yêu cầu chống enumeration; xác nhận policy. | BLOCKING — security |
| Q-61-07 | `SupportRequest` response được rehydrate thế nào sau update, gồm `course_id`, student, thread và attachments? | #59/#60 response matrices còn `SOURCE_REQUIRED`; pilot ticket thiếu course_id và ID type không khớp. | Tái sử dụng một projection chung sau khi model/identity/asset resolver được duyệt; không trả object giả. | BLOCKING — response/data |
| Q-61-08 | Error envelope lỗi dùng `data:null` hay `{}` khi route được wiring? | API Guidelines muốn null; current `error_response` mặc định `{}`; support route chưa thuộc middleware allowlist. | Chốt/cập nhật helper hoặc route wiring đồng bộ theo API contract. | BLOCKING — error contract |
| Q-61-09 | State ngoài OPEN/RESOLVED có trả 422 như proposal không, và có field `reason` nào được hỗ trợ không? | Catalog khai báo 422 nhưng không nêu state rule hoặc error payload shape. | Dùng code 422 đã có, không thêm field response; chốt allowed-state list. | NEEDS CONFIRMATION — validation |
| Q-61-10 | Update và reload có nằm trong một transaction; đồng thời hai request resolve được serialize ra sao? | Study helper không commit; AC-24 không định nghĩa concurrency. | Caller-owned transaction; conditional update/row lock theo schema được duyệt; lần resolve sau cùng trả current resource idempotently. | NEEDS CONFIRMATION — transaction/concurrency |

## Ranh giới đã giữ

- API #61 chỉ resolve SupportRequest; #60 sở hữu INSERT SupportMessage.
- Không ghi `resolution_code`, không đổi `cancelled_at`, không xóa hoặc cập nhật messages.
- Không biến API #58 thành list response mới; cardinality conflict của #58 còn blocking.
- V1-PILOT là candidate, không chứng minh live schema.
- Không thêm business code ngoài exact set 401/403/404/422/500.
