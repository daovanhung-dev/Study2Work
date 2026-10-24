# Câu hỏi còn mở — API #91 Xem thống kê quiz

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** `GET /api/v1/admin/quizzes/{quiz_id}/statistics`
**Nhóm:** AC-35 #87–#91; dependency AC-16 #29–#32.

Các metric và lifecycle proposal là `DERIVED`, chưa được owner phê duyệt.

## Q-91-01 — Schema response

**Evidence:** AC-35 yêu cầu aggregate statistics; catalog/reusable schema chỉ có `ApiEnvelope<Quiz>` và Quiz không có metrics.

**Đề xuất:** DTO riêng `QuizStatistics` gồm quiz_id, attempt/submitted/graded counts, average_score, passed_attempt_count và pass_rate_percent. Giữ direct catalog contract cho tới khi được cập nhật.

**Cần xác nhận:** Chọn response schema nào? Có cần kèm title/course metadata? Catalog có cần sửa trước implementation không?

## Q-91-02 — Bộ metric và attempt được tính

**Evidence:** Diagram không định nghĩa metrics. AC-16 có IN_PROGRESS, PENDING_GRADE và GRADED; DDL có submitted_at/score nullable.

**Đề xuất DERIVED:** attempt_count = mọi row gắn quiz; submitted count = submitted_at khác NULL; graded count = score khác NULL; average trên score khác NULL; không filter enum status.

**Cần xác nhận:** Có status nào bị loại? Có cần phân biệt attempt đang làm/chờ chấm/đã chấm trong response?

## Q-91-03 — Passing score, NULL và rounding

**Evidence:** Quiz logical schema yêu cầu passing_score; legacy DDL không đặt NOT NULL. Score/threshold là numeric.

**Đề xuất DERIVED:** Pass nếu score >= threshold. Threshold NULL làm passed count/rate NULL. Không có scored attempts làm average/rate NULL. Tỷ lệ là passed/graded × 100.

**Cần xác nhận:** Threshold NULL hợp lệ không? Có dùng auto_score hay final score? Decimal scale/rounding là gì?

## Q-91-04 — Soft delete và lịch sử

**Evidence:** AC-35 yêu cầu soft delete khi có attempts; #90 đề xuất giữ quiz/history. AC-16 APIs #29–#32 tạo, lưu, submit và đọc attempt.

**Đề xuất macro DERIVED:** #87 ẩn DELETED mặc định; #89 từ chối update tombstone; #29 từ chối attempt mới; #30–#32 giữ flow attempt đã có; #91 đọc aggregate lịch sử còn row; hard-delete/no-row trả 404.

**Cần xác nhận:** Duyệt status DELETED và toàn bộ hành vi trên không? Attempt đang làm có được hoàn tất sau soft delete? Tombstone/audit timestamp lưu ở đâu?

## Q-91-05 — Schema vật lý và NULL/orphan data

**Evidence:** Legacy guide/ERD mô tả BIGINT 1:N, DDL cho phép quiz_id/passing_score NULL; V1-PILOT là UUID model khác.

**Đề xuất:** Dùng legacy schema làm candidate duy nhất cho query minh họa; không khẳng định live schema.

**Cần xác nhận:** Schema baseline, FK/nullability, score precision và cách xử lý orphan rows?

## Q-91-06 — Admin authorization/error wiring

**Evidence:** AC-35 yêu cầu Admin + quiz-management permission; Study source hiện không có Admin guard và path trong DESIGN_CONTRACT_PATHS.

**Cần xác nhận:** Claim/policy Admin nào được dùng? Middleware nào giữ đúng 401/403/404/500 catalog codes khi route được wire?

## Q-91-07 — Direct Quiz nested projection

**Evidence:** Direct Quiz có questions[].type và choices[]; legacy question table thiếu type, QuizChoice schema chưa có.

**Đề xuất:** Không bịa nested fields, không chèn statistics vào Quiz. Chốt response schema trước implementation.

**Cần xác nhận:** Nếu giữ ApiEnvelope<Quiz>, API có cần trả question tree không? Schema và persistence nào là nguồn?

## Trạng thái
Response schema, metric, threshold, tombstone, Admin policy và active schema vẫn chặn Approved/Final. Không sửa catalog/diagram/runtime/DDL trong task DD.
