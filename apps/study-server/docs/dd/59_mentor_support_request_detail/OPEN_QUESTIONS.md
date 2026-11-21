# OPEN_QUESTIONS — Study API #59

Status: `Draft — Needs Confirmation`. Các câu hỏi dưới đây được phân biệt giữa fallback đã chọn để triển khai local và điều kiện còn cần xác minh ngoài source. Các fallback là `DERIVED`, không phải phê duyệt live schema hoặc business owner.

| ID | Vấn đề | Quyết định cho local implementation | Basis/status |
|---|---|---|---|
| Q-59-01 | Physical support model và ID int64/UUID | Kế thừa `support_requests`, `support_messages`, `support_message_uploads` BIGINT từ API #58 migration 008; không dùng V1-PILOT UUID. | `RESOLVED_FOR_LOCAL_IMPLEMENTATION — DERIVED`; live schema chưa xác minh. |
| Q-59-02 | Mentor principal/scope | Shared `MENTOR` guard; `courses.mentor_id = JWT sub` cho request và message reads. | `RESOLVED_FOR_LOCAL_IMPLEMENTATION — DERIVED_FROM_API58`. |
| Q-59-03 | Request missing hay ngoài scope | Không có row → 404; row tồn tại nhưng direct owner khác → 403, theo API #48/#55 và catalog. | `RESOLVED_FOR_LOCAL_IMPLEMENTATION — DERIVED`; resource enumeration policy vẫn cần business owner review. |
| Q-59-04 | Course relation | Dùng `support_requests.course_id` FK → `courses.id` từ migration 008. | `RESOLVED_FOR_LOCAL_IMPLEMENTATION — DERIVED_FROM_API58`. |
| Q-59-05 | Thread visibility/order/bound/empty | Tất cả rows trong selected legacy model, `created_at ASC, id ASC`, full thread, no limit; empty là `[]`. Schema không có `is_internal`. | `RESOLVED_FOR_LOCAL_IMPLEMENTATION — DERIVED_FROM_API58`; private-message policy không được biểu diễn bởi fallback schema. |
| Q-59-06 | Student/author projection | Dùng numeric `users.id`, non-null `full_name`, optional `avatar_url`. | `RESOLVED_FOR_LOCAL_IMPLEMENTATION — DERIVED_FROM_API58/LEGACY DDL`. |
| Q-59-07 | Attachment resolver | Dùng ordered link table và API #34 `uploads`; constrain owner/course/role-purpose/`UPLOADED`; invalid link làm response safe 500. | `RESOLVED_FOR_LOCAL_IMPLEMENTATION — DERIVED_FROM_API58`; không chứng minh URL còn truy cập được. |
| Q-59-08 | SupportStatus/UploadStatus | Trả status string theo row; local request status CHECK candidates là `OPEN`, `IN_PROGRESS`, `WAITING_LEARNER`, `RESOLVED`, `CANCELLED`; UploadAsset phải `UPLOADED`. | `DERIVED_FROM_API58`; enum/business approval và live constraint chưa xác minh. |
| Q-59-09 | Optional values | Omit `avatar_url`/`resolved_at` khi NULL theo API #58 serialization. | `RESOLVED_FOR_LOCAL_IMPLEMENTATION — CURRENT_RUNTIME_CONVENTION`. |
| Q-59-10 | Malformed path khi catalog không có 422 | Map sai format/overflow sang 404 `DESIGN_RESOURCE_NOT_FOUND`, như API #48; không thay catalog. | `RESOLVED_FOR_LOCAL_IMPLEMENTATION — DERIVED_FROM_API48`. |
| Q-59-11 | Empty thread hoặc linked upload không đủ điều kiện | Trả `messages: []` nếu chưa có message; linked upload không resolve đủ metadata/scope làm lỗi 500, không trả partial. | `RESOLVED_FOR_LOCAL_IMPLEMENTATION — DERIVED_FROM_API58`. |
| Q-59-12 | Live schema/migration/deployment | Chưa có live metadata hoặc migration probe; migration 008 chỉ là checked-in source. | `NOT_VERIFIED_HERE`; runtime deployment vẫn cần xác nhận riêng. |

## Macro-review AC-24 #58–#61

- #58 list và #59 detail dùng cùng BIGINT request/message model, direct course-owner predicate, full ordered thread và UploadAsset scope đã chọn tại #58.
- #60 vẫn sở hữu SupportMessage insert; #61 vẫn sở hữu status `RESOLVED` update. Hai API không được triển khai trong phiên #59.
- Retry/status transition của #61 và request attachment-ref format của #60 không bị suy ra từ #59.