# OPEN_QUESTIONS — Study API #45

**Status:** Draft — Needs Confirmation  
**Endpoint:** `PATCH /api/v1/notifications/read-all`  
**Related group:** AC-20 APIs #43–#45; see macro review in [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).

## Q-45-01 — Chọn schema Notification áp dụng cho Study API

**Evidence**

- API catalog/AC-20/DB guide/ERD và `infra/postgres/study-server/DB.sql` dùng notification ID `int64`, `user_id` và boolean `is_read`.
- `infra/postgres/02_study_db.sql` là V1-PILOT DDL riêng: notification ID UUID, `learner_id` UUID, `read_at`, `expires_at`, `payload`, và `notification_deliveries`.
- Current Study JWT helper trả numeric `users.id`; V1-PILOT DDL không có bảng `users` để join trực tiếp.
- Live schema chưa được xác minh.

**Ảnh hưởng**

Không thể vừa giữ int64 API ID/numeric principal vừa dùng pilot `read_at`/delivery fields nếu chưa có migration hoặc identity mapping được duyệt.

**Cần xác nhận**

Schema nào là target của Study API AC-20? Nếu V1-PILOT là target, xác định mapping giữa JWT subject, `identity_subject_id`, `learner_profiles.id` và API notification ID.

## Q-45-02 — Recipient, broadcast và read timestamp

**Evidence**

- AC-20 gọi logical `NotificationRecipient` và API #44/#45 cập nhật read state.
- Legacy schema không có recipient table; `notifications.user_id` nullable và `is_read` nằm trên notification row.
- V1-PILOT có `notifications.learner_id` và `read_at`, nhưng không khớp numeric identity của API hiện tại.

**Ảnh hưởng**

Candidate legacy chỉ cập nhật direct-recipient rows; không thể ghi read state riêng cho broadcast rows có `user_id IS NULL`. Candidate không lưu thời điểm đọc.

**Đề xuất DERIVED**

Trong legacy-schema proposal, chỉ cập nhật notification có `user_id` bằng Student principal và `is_read=FALSE`; không update broadcast row.

**Cần xác nhận**

Có chuyển sang per-recipient table/timestamp hoặc dùng V1-PILOT model không? Broadcast/segment notification được đánh dấu đọc theo từng Student ở đâu?

## Q-45-03 — Nguồn `channels`, `status` và `scheduled_at`

**Evidence**

- `Notification` response bắt buộc `channels` và `status`; `scheduled_at` là optional.
- Legacy table có `type`/`is_read`, không có `channels`/`status`/`scheduled_at`.
- V1-PILOT có per-delivery `channel`/`status`; `notification_status` mô tả trạng thái delivery, chưa được xác nhận đồng nghĩa `NotificationStatus`.

**Cần xác nhận**

Chọn physical field/table và enum semantics; xác định omission/null behavior cho các timestamp optional. Không map hai schema thay thế cho nhau khi chưa có quyết định.

## Q-45-04 — Semantics `Page<Notification>` cho mark-all

**Evidence**

- API #45 không nhận `page`/`size` nhưng catalog response là `Page<Notification>`.
- AC-20 chỉ yêu cầu bulk update unread state, không quy định response projection.

**Đề xuất DERIVED**

Trả mọi row vừa chuyển unread→read trong một page: `page=1`, `size=updated_count`, `total=updated_count`, `total_pages=0` khi rỗng hoặc `1` khi có row.

**Ảnh hưởng**

Response có thể lớn theo số unread notification; `PageMeta.size`=0 khi empty và size có thể vượt int32 cần được xem xét.

**Cần xác nhận**

API #45 nên trả toàn bộ item, page giới hạn, empty Page, hay một summary/count contract? API #44 singleton Page và #43 list Page cần được khóa cùng nhau.

## Q-45-05 — `body{}` và HTTP 422

**Evidence**

- Catalog ghi `body{}` nhưng không ghi requiredness hoặc `additionalProperties`.
- Catalog có 422 `DESIGN_VALIDATION_ERROR`, không nêu trigger.

**Đề xuất DERIVED**

Nhận JSON object rỗng `{}`; reject malformed/non-object/non-empty body bằng 422.

**Cần xác nhận**

Body có thể bị bỏ qua/omitted không? Có reject property không khai báo không?

## Q-45-06 — Trạng thái `is_read` NULL trong legacy DDL

**Evidence**

- `infra/postgres/study-server/DB.sql` khai báo `is_read BOOLEAN DEFAULT FALSE` nhưng không khai báo `NOT NULL`.
- Candidate M1 dùng `is_read=FALSE`, không match row có `is_read IS NULL`.

**Cần xác nhận**

Null legacy rows có được xem là unread hay phải sửa dữ liệu/schema trước khi triển khai?

## Q-45-07 — Timezone và retention

**Evidence**

- Legacy `created_at` là `TIMESTAMP` không timezone; pilot DDL dùng `timestamptz` và `expires_at`/retention policy.

**Cần xác nhận**

Chốt timezone/ISO-8601 cho toàn nhóm và chọn expiry/retention behavior theo schema được duyệt.

## Q-45-08 — Error envelope và Idempotency-Key

**Evidence**

- API guidelines yêu cầu error `data:null`; current `error_response()` fallback trả `data:{}`.
- Guidelines nhắc `Idempotency-Key` cho retryable mutations; API #45 không khai báo header và state assignment là idempotent.

**Đề xuất**

Không thêm header vào API #45 DD; dùng catalog và giữ helper discrepancy ở mức shared issue.

**Cần xác nhận**

Có quy ước header bắt buộc cho mọi PATCH bất kể operation idempotent không? Xử lý shared error-envelope mismatch ở task phù hợp.
