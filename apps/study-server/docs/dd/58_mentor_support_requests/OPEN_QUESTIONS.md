# OPEN_QUESTIONS — Study API #58

Status: `Draft — Needs Confirmation`. Theo chỉ dẫn mới nhất của user, các conflict được giải quyết bằng fallback đơn giản để triển khai local. Các lựa chọn dưới đây là `DERIVED`; chúng không chứng minh migration đã được áp dụng vào live database hoặc được contract owner phê duyệt lâu dài.

| ID | Vấn đề | Quyết định triển khai | Basis/status |
|---|---|---|---|
| Q-58-01 | List response khai báo singleton ở catalog/diagram nhưng AC-24 là bước mở danh sách. | `data` là `SupportRequest[]`; không thêm pagination vì request không có page/size; empty result là `[]`. | `RESOLVED_FOR_IMPLEMENTATION — DERIVED` |
| Q-58-02 | Không có support model trong legacy Study DDL; V1-PILOT dùng UUID và khác runtime convention. | Thêm legacy BIGINT `support_requests`, `support_messages`, `support_message_uploads` trong DB.sql và migration 008; giữ V1-PILOT riêng. | `RESOLVED_FOR_IMPLEMENTATION — USER-DIRECTED FALLBACK` |
| Q-58-03 | `course_id` filter/response thiếu relation trong pilot ticket model. | `support_requests.course_id` FK tới legacy `courses.id`; `student_id` FK tới `users.id`. | `RESOLVED_FOR_IMPLEMENTATION — DERIVED` |
| Q-58-04 | Mentor identity/predicate chưa được support schema cung cấp. | Dùng numeric JWT subject và direct `courses.mentor_id` ownership, nhất quán với API #46/#49/#54. Request tới course owner khác trả 403. | `RESOLVED_FOR_IMPLEMENTATION — DERIVED` |
| Q-58-05 | `SupportStatus` chưa có enum trong catalog. | DDL check cho `OPEN`, `IN_PROGRESS`, `WAITING_LEARNER`, `RESOLVED`, `CANCELLED`; filter là exact string match; giá trị lạ trả list rỗng. | `RESOLVED_FOR_IMPLEMENTATION — DERIVED FROM PILOT VALUES` |
| Q-58-06 | #58 có tải thread đầy đủ khi #59 cũng đọc conversation không? | Tải toàn bộ `messages[]` để giữ reusable `SupportRequest` shape; order `created_at ASC, id ASC`; không cắt dữ liệu. | `RESOLVED_FOR_IMPLEMENTATION — DERIVED`; payload size là residual risk. |
| Q-58-07 | Identity/attachments không map được từ UUID pilot sang int64 runtime. | Dùng numeric `users` projection; thêm `support_message_uploads`; resolve legacy UploadAsset nếu owner, course, role-purpose và status `UPLOADED` khớp. | `RESOLVED_FOR_IMPLEMENTATION — DERIVED`; source #34 supplies URL metadata. |
| Q-58-08 | Catalog ban đầu không khai báo 422 cho invalid `course_id`. | Đồng bộ thêm 422 `DESIGN_VALIDATION_ERROR` vào catalog/diagram; dùng shared validation handler. | `RESOLVED_FOR_IMPLEMENTATION — USER-DIRECTED FALLBACK` |
| Q-58-09 | Empty result, ordering và page size chưa được quy định. | HTTP 200 với `data: []`; requests order `created_at DESC, id DESC`; không phân trang. | `RESOLVED_FOR_IMPLEMENTATION — DERIVED` |
| Q-58-10 | Nullability của `resolved_at` và avatar URL. | Omit optional fields khi NULL theo response model `exclude_none=True`. | `RESOLVED_FOR_IMPLEMENTATION — EXISTING RUNTIME CONVENTION` |
| Q-58-11 | Migration/live database availability. | Chưa xác minh live metadata hoặc migration state; chỉ kiểm chứng source và fake-session HTTP behavior. | `NOT_VERIFIED_HERE`; không cản local implementation |

## Macro-review AC-24 #58–#61

- #58 trả collection, #59 trả một SupportRequest/thread, #60 insert một reply message, #61 chỉ cập nhật trạng thái `RESOLVED`.
- Các API #59–#61 chưa được code trong phiên #58; các phiên sau phải reuse BIGINT support tables, `courses.mentor_id` predicate và asset-link rules được chọn ở đây.
- Những quyết định về trạng thái chuyển đổi, retry khi resolve và attachment request body của #60 vẫn thuộc phạm vi DD/API tương ứng; không được suy rộng từ API #58.
