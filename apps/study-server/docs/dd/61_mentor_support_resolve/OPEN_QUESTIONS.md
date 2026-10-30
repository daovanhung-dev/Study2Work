# OPEN_QUESTIONS — Study API #61

Status: `Draft — Needs Confirmation`. Catalog và AC-24 trực tiếp được giữ nguyên; local schema/identity/lifecycle lựa chọn là `DERIVED` theo chỉ đạo người dùng và phải được xác nhận trước khi coi là business contract hoặc live deployment.

| ID | Câu hỏi còn mở | Bằng chứng và ảnh hưởng | Trạng thái triển khai |
|---|---|---|---|
| Q-61-01 | Business owner có phê duyệt fallback BIGINT `support_requests`, FK `course_id` và direct owner `courses.mentor_id = JWT sub` làm contract chính thức không? | Đây là local migration/API #58–#60 pattern; V1-PILOT UUID `support_tickets` khác model. | Đã dùng `DERIVED` cho local code theo chỉ đạo; live schema chưa xác minh. |
| Q-61-02 | Có xác nhận mọi trạng thái active (`OPEN`, `IN_PROGRESS`, `WAITING_LEARNER`) đều resolve được, retry `RESOLVED` idempotent, `CANCELLED` trả 422 không? | AC-24 chỉ ghi YES→RESOLVED và NO giữ OPEN; pre-state/retry chưa nêu. | Đã chọn ma trận rõ ràng, đơn giản để triển khai; cần business approval. |
| Q-61-03 | Live database đã áp dụng đúng migration 008 và các ràng buộc/enum chưa? | Repo chỉ chứng minh checked-in migration/DDL và fake-DB test. | Chưa xác minh live metadata hoặc deployment. |
| Q-61-04 | Có privacy policy khác cho request ngoài owner scope (403 so với 404) không? | API #59/#60 hiện dùng 403 cho request tồn tại của Mentor khác. | Local code giữ đúng pattern hiện có; policy rộng hơn chưa xác nhận. |

## Ranh giới đã giữ

- API #61 chỉ resolve SupportRequest; #60 sở hữu INSERT SupportMessage.
- Không ghi `resolution_code`, `cancelled_at`, `updated_at` hoặc `row_version` nếu local migration không có các cột đó.
- Không dùng V1-PILOT UUID table cho numeric API contract.
- Không thêm business code ngoài exact set 401/403/404/422/500.
- Tests dùng fake DB; không chứng minh schema/deployment hoặc concurrency live.
