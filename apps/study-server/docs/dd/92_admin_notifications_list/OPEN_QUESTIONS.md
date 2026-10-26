# Câu hỏi mở — API #92 Lấy notification list

**Trạng thái:** `Draft — Needs Confirmation`; runtime có fallback cụ thể nhưng chưa có owner approval.

## Q-92-01 — Response singleton hay danh sách

**Evidence:** Catalog #92 khai báo `ApiEnvelope<Notification>`; API name, `page` query và AC-36 intent là list. Diagram không mô tả response wrapper.

**Current fallback DERIVED:** Runtime trả `ApiEnvelope<Page<Notification>>` để danh sách có pagination.

**Cần xác nhận:** Catalog có đổi sang Page không? PageMeta thuộc `data` như runtime hay nơi khác?

## Q-92-02 — Page origin, size và ordering

**Evidence:** Request chỉ có `page?:int32`; catalog không định nghĩa origin, default, size, PageMeta hoặc ordering.

**Current fallback DERIVED:** Page bắt đầu 1, default 1, fixed size 20, sort `created_at DESC, id DESC`, count trùng predicate.

**Cần xác nhận:** Các giá trị này có được duyệt không? Có cần con trỏ hoặc scheduled-first ordering?

## Q-92-03 — Campaign hay recipient-level notification

**Evidence:** AC-36 #93 tạo Notification và recipients; legacy/API #63 ghi từng `notifications.id` theo recipient, dùng `operation_id` chung cho một dispatch. Không có campaign aggregate được duyệt.

**Current fallback DERIVED:** Mỗi item là một notification ID có delivery; không group operation/campaign và không trả recipient identity.

**Cần xác nhận:** Admin list nên hiển thị từng recipient notification hay một campaign summary?

## Q-92-04 — Physical Admin notification model

**Evidence:** Legacy `notifications` + migration 009/outbox phục vụ API #63; V1-PILOT notification là UUID/learner-scoped. Không có Admin model được duyệt.

**Current fallback DERIVED:** Dùng legacy BIGINT candidate và delivery outbox; chỉ lấy notification có delivery rows để đủ required channels/status.

**Cần xác nhận:** Admin #93 sẽ ghi cùng legacy/outbox model không? Draft/scheduled rows chưa có delivery được quản lý ra sao?

## Q-92-05 — `NotificationChannel` và `NotificationStatus`

**Evidence:** Catalog không liệt kê enum values. API #63/DDL có `PUSH`/`EMAIL`; API #64 aggregate có `QUEUED`/`FAILED`/`SENT`.

**Current fallback DERIVED:** Channels từ delivery rows; status dùng API #64 precedence (queued trước failed, rồi sent). Filter exact.

**Cần xác nhận:** Các value set/aggregate semantics này có áp dụng cho Admin Notification không?

## Q-92-06 — `read_at` và `scheduled_at`

**Evidence:** Legacy chỉ có `is_read`; không có `scheduled_at`. Pilot `read_at` theo learner UUID model; `expires_at` khác nghĩa scheduled time.

**Current fallback:** Runtime omit cả hai optional fields; không đổi boolean hay expiry timestamp.

**Cần xác nhận:** Admin list có cần các field này và nguồn vật lý nào?

## Q-92-07 — Admin permission và visibility scope

**Evidence:** Catalog yêu cầu Admin; AC-36 yêu cầu notification-management permission. Current Study guard có role ADMIN nhưng chưa có permission key hoặc tenant scope.

**Current fallback DERIVED:** Shared ADMIN guard; query nhìn thấy mọi legacy row có delivery; không trả user IDs.

**Cần xác nhận:** Permission claim và phạm vi global/tenant/sender nào được dùng?

## Q-92-08 — 503 dependency trigger

**Evidence:** Catalog có 503, diagram chỉ ghi “Query notifications”.

**Current fallback DERIVED:** Database operational/connection-invalidated failures trả 503; SQL/data-mapping failures khác trả 500.

**Cần xác nhận:** Owner có chủ ý gắn DB connectivity với dependency code 503 không?

## Q-92-09 — Empty result và validation errors

**Evidence:** Catalog không liệt kê 404/422. Page query nhận int32 nhưng không có range rule.

**Current fallback DERIVED:** Empty/out-of-range page trả 200 Page rỗng; page invalid/non-positive trả 422; filter không match trả 200 rỗng.

**Cần xác nhận:** Có chấp nhận 422 ngoài direct error set và semantics này không?

## Q-92-10 — #93 create response và Operation tracker

**Evidence:** Catalog/diagram #93 trả Notification nhưng operation tracking prose nói Admin notification POST trả Operation; ID types khác nhau.

**Current handling:** API #92 không chọn Operation ID, không group theo operation và không giải quyết bridge.

**Cần xác nhận:** #93 trả Notification hay Operation? Operation UUID và notification int64 nối thế nào?

## Ranh giới giữ nguyên

Không đổi catalog/schema/diagram hoặc đánh dấu DD Approved/Final. Chưa xác minh live schema, migration deployment, Admin permission hoặc Notification campaign model.

## AC-36 macro-review result

- Status: `VERIFIED_WITH_OPEN_QUESTIONS` ở document level; quyết định cho API #92 chưa được owner phê duyệt.
- Group findings: [AC-36 macro-review #92–#96](../96_admin_notifications_status/AC-36_MACRO_REVIEW.md).
- Source wiring/test của #92 được cập nhật trong [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md); trạng thái hiện tại của #93–#96 được tổng hợp trong [AC-36 macro-review](../96_admin_notifications_status/AC-36_MACRO_REVIEW.md).
