# Câu hỏi còn mở — API #88 Tạo quiz mới

**Trạng thái DD:** Draft — Needs Confirmation

**Endpoint:** POST /api/v1/admin/quizzes

**Nhóm:** AC-35, API #87–#91

Các lựa chọn cục bộ đã dùng để hoàn tất implementation đều là `DERIVED`, không phải owner approval. Live schema/deployment vẫn chưa xác minh.

| ID | Vấn đề | Quyết định local | Trạng thái còn lại |
|---|---|---|---|
| Q-88-01 | JSON schema trong hai string | `config={course_id,title,duration_minutes?,passing_score}`; `questions=[{text,type,choices:[{text,is_correct?}]}]`. | `DERIVED`; owner có thể thay embedded contract. |
| Q-88-02 | QuestionType values/storage | Dùng `SINGLE_CHOICE`, `MULTIPLE_CHOICE`, `TRUE_FALSE`; migration 013 thêm nullable legacy `question_type` có CHECK; API #88 ghi non-null. | `DERIVED`; vocabulary mượn từ pilot, không dùng pilot rows/IDs. |
| Q-88-03 | QuizChoice shape/answer key | Input `{text,is_correct?}`; absent `is_correct` mặc định false; Admin response `{id,text,is_correct}`. | `DERIVED`; reusable QuizChoice schema chưa có trong catalog. |
| Q-88-04 | Số đáp án đúng/validation nghiệp vụ | Không áp rule theo question type; lưu đúng boolean client gửi. | `SOURCE_REQUIRED`; cần owner chốt nếu publish/grade flow yêu cầu. |
| Q-88-05 | Physical schema/live database | Dùng legacy BIGINT; migration 013 thêm `question_type` và `sort_order`. | Source/migration local; live schema/deployment `NOT_VERIFIED_HERE`. |
| Q-88-06 | Course reference/Admin permission | Check `courses.id`, course không tồn tại → 422; runtime chỉ enforce shared ADMIN role. | Course mapping `DERIVED`; fine-grained quiz-management permission `SOURCE_REQUIRED`. |
| Q-88-07 | Quiz status lifecycle | Dùng DB default `DRAFT`; API #88 không nhận status. | `SOURCE_REQUIRED`; cách chuyển sang trạng thái làm bài chưa rõ. |
| Q-88-08 | Thứ tự choices | Migration 013 thêm `quiz_choices.sort_order`, gán index zero-based. | `DERIVED`; không đổi outer request contract. |
| Q-88-09 | Error envelope | Dùng shared error helper hiện trả `data:null` và `meta.fieldErrors`; path đã được đăng ký bởi #87. | `CURRENT_RUNTIME_CONVENTION`; chưa có contract mismatch ở helper hiện hành. |
| Q-88-10 | Liên kết #87–#91 | Giữ direct contract của từng API; #87 list metadata-only, #89 body/replacement, #90 attempt history, #91 statistics không sửa trong task này. | Macro-review `VERIFIED_WITH_OPEN_QUESTIONS`; không phải approval. |

## Ranh giới proposal

- `DIRECT`: POST/path, Admin Bearer role, outer body field names/types, `ApiEnvelope<Quiz>`, HTTP 201, `DESIGN_RESOURCE_CREATED`, errors 401/403/422/500.
- `DERIVED`: embedded JSON shape, QuestionType vocabulary, local QuizChoice shape, migration columns, course check→422, order preservation và atomic transaction.
- `SOURCE_REQUIRED`: fine-grained permission, answer-count rules, publication lifecycle, owner approval, live schema và migration deployment.
- `DISCREPANCY`: DB diagram/legacy schema ban đầu thiếu question type và choice order so với logical nested response.

API #28 Student read phải tiếp tục loại `is_correct`. Việc thêm cột nullable để tương thích rows hiện hữu không tự lấp QuestionType cho dữ liệu cũ.
