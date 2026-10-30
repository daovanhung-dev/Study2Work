# OPEN_QUESTIONS — Study API #44

**Status:** Draft — Needs Confirmation
**Endpoint:** `PATCH` `/api/v1/notifications/{notification_id}/read`
**Related group:** AC-20 APIs #43–#45; macro review sau khi tạo DD #45.

## Q-44-01 — Recipient và read timestamp

**Evidence:** AC-20 yêu cầu `UPDATE` `read_at` trên `NotificationRecipient`; DB guide/ERD/DDL chỉ có `notifications`.`user_id` nullable và `is_read` `BOOLEAN`. Không có physical `NotificationRecipient` hoặc `read_at`.

**Ảnh hưởng:** `is_read`=`TRUE` lưu boolean nhưng không lưu thời điểm đọc; broadcast/segment `user_id` NULL không có per-user state.

**Đề xuất `DERIVED`:** chỉ cập nhật direct-user row theo notification ID và principal; không update broadcast row toàn cục; không tạo schema trong DD này.

**Cần xác nhận:** dùng physical recipient table hay chuẩn hóa diagram/schema sang boolean `is_read`? Read state của broadcast được lưu ở đâu?

## Q-44-02 — `Notification` fields và read-state trả cho client

Catalog yêu cầu `channels`/`status`; `read_at` optional. DDL chỉ có type/`is_read`, không có enum hoặc timestamp. API #43 filter dùng `is_read` nhưng response không có `is_read`.

**Cần xác nhận:** field nào biểu diễn read/unread cho client? Source/enum values của `channels`/`status` là gì? Có chốt chung `Notification` contract cho #43–#45 không?

Xem [API #43 open questions](../43_users_me_notifications/OPEN_QUESTIONS.md).

## Q-44-03 — Response `Page`

Catalog và diagram khai báo `Page<Notification>`; API #44 không nhận `page`. Đề xuất `DERIVED`: một item đã cập nhật với `page`/`size`/`total`/`total_pages` bằng 1, dựa trên API #42 singleton `Page` precedent.

**Cần xác nhận:** #44 trả singleton, trang `Notification` Center hiện tại hay shape khác? API #45 có cùng semantics không?

## Q-44-04 — 404 và broadcast

Đề xuất `DERIVED`: update theo `notification_id` và authenticated `user_id`; trả cùng 404 cho row không tồn tại, thuộc user khác hoặc `user_id` NULL để tránh lộ existence.

**Cần xác nhận:** chốt concealment 404 và cách `Student` address/read broadcast notification.

## Q-44-05 — `Idempotency-Key`

API guideline nhắc `Idempotency-Key` cho retryable mutation; API #44 chỉ khai báo `notification_id`. Candidate assignment `is_read`=`TRUE` idempotent theo state.

**Cần xác nhận:** guideline có bắt buộc header cho state update vốn idempotent không? Không thêm header khi catalog chưa khai báo.

## Q-44-06 — Error envelope

Guideline yêu cầu error `data`:null; current error_response() trả `data`:{} khi `data`=None. API #44 chưa wired.

**Cần xác nhận:** xử lý shared helper/guideline discrepancy trong task riêng đúng scope.

## Q-44-07 — Timestamp/timezone và omission dùng chung

`created_at` là `TIMESTAMP` không timezone; `read_at`/`scheduled_at` optional nhưng thiếu source.

**Cần xác nhận:** dùng chung quyết định timezone và null/omission của API #43 cho cả nhóm #43–#45.
