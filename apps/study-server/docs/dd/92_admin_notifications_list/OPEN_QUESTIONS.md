# Câu hỏi mở — API #92 Lấy notification list

**Trạng thái:** `Draft — Needs Confirmation`; contract direct được giữ, các proposal bên dưới không được hiểu là owner approval.

## Q-92-01 — Response singleton hay danh sách

**Evidence:** Catalog #92 khai báo `ApiEnvelope<Notification>`; API name, `page` query và AC-36 intent nói tới notification list. Notification schema không có collection wrapper.

**Đề xuất DERIVED:** Đổi response thành `ApiEnvelope<Page<Notification>>` nếu mục tiêu là danh sách có pagination. API #43 là precedent Page, không chuyển Student access predicate sang Admin.

**Cần xác nhận:** Direct singleton có chủ ý không? Nếu list: Page nằm ở `data` hay `meta`, có `total/total_pages` không?

## Q-92-02 — Page origin, size và ordering

**Evidence:** Request có `page?:int32` nhưng không có `size`, default, range, response PageMeta hoặc ordering.

**Đề xuất DERIVED:** Nếu #92 được duyệt thành Page, dùng page bắt đầu 1, fixed size 20, sort `created_at DESC, id DESC` theo precedent #43.

**Cần xác nhận:** Page có bắt đầu từ 0 hay 1? Size cố định bao nhiêu? Thứ tự có ưu tiên `scheduled_at` không? Có cần total count?

## Q-92-03 — Campaign hay recipient-level notification

**Evidence:** AC-36 #93 tạo Notification và recipients. Legacy `notifications` là row có `user_id` recipient nullable; V1-PILOT notification gắn `learner_id`. Không có campaign/recipient aggregate được thống nhất.

**Cần xác nhận:** Admin list một notification campaign, từng recipient notification hay một row theo recipient/channel? Các row nào được gom thành một Notification response?

## Q-92-04 — Field projection và schema vật lý

**Evidence:** Logical `Notification` yêu cầu id/title/content/channels/status/read_at/scheduled_at/created_at. Legacy chỉ có id/title/content/type/is_read/created_at. Pilot dùng UUID/title/body/read_at/created_at và delivery relation riêng; không có scheduled_at.

**Đề xuất:** Không tạo query đầy đủ hoặc gộp legacy/pilot cho tới khi chọn model/schema.

**Cần xác nhận:** Schema nào là nguồn Admin notification? Có campaign table, recipient relation và physical scheduled/status fields nào?

## Q-92-05 — `NotificationChannel` và `NotificationStatus`

**Evidence:** Catalog nêu enum types nhưng không liệt kê value set. Pilot channel/status ở per-delivery rows; legacy `type` không phải channels và `is_read` không phải status.

**Cần xác nhận:** Các enum token là gì? Filter `channel` yêu cầu một phần tử trong delivery channels hay channel của campaign? Status là draft/scheduled hay delivery aggregate?

## Q-92-06 — `read_at` và `scheduled_at`

**Evidence:** `read_at` chỉ có trong pilot learner notification; không có legacy. `scheduled_at` không có trong hai DDL đã rà soát; pilot `expires_at` có nghĩa khác.

**Cần xác nhận:** Hai trường có áp dụng cho Admin-managed notification không? Nếu `read_at` theo recipient, list aggregate sẽ xử lý thế nào?

## Q-92-07 — Admin permission

**Evidence:** Catalog yêu cầu Admin; AC-36 yêu cầu notification-management permission. Current Study helper chưa có Admin guard/policy.

**Cần xác nhận:** Claim/permission code và scope (toàn hệ thống/tenant/sender) nào được dùng? 401/403 áp dụng thế nào?

## Q-92-08 — 503 dependency trigger và middleware wiring

**Evidence:** Catalog/diagram #92 liệt kê 503, nhưng node list chỉ nói “Query notifications”; không nêu external dependency. Path chưa có trong `DESIGN_CONTRACT_PATHS`.

**Cần xác nhận:** Dependency nào có thể làm GET list trả 503? Khi wire route, middleware map direct error codes ra sao?

## Q-92-09 — Empty result và validation errors

**Evidence:** Catalog không liệt kê 404/422. Singleton response và Page proposal có semantics khác nhau; query types không có range/enum values.

**Đề xuất DERIVED:** Nếu Page được duyệt, danh sách rỗng trả 200 với `items: []`; không trả 404 chỉ vì rỗng.

**Cần xác nhận:** Singleton direct contract xử lý không có notification thế nào? Parse/range/filter validation có business code nào trong contract?

## Q-92-10 — #93 create response và Operation tracker

**Evidence:** AC-36 index liệt kê operation polling riêng; catalog #93 row trả `ApiEnvelope<Notification>` ở 202, còn tracking summary nói Admin notification POST trả `Operation`. #63/#64 Mentor flow cũng chưa có ID bridge.

**Đề xuất:** Giữ #92 độc lập và không suy Operation result/notification ID.

**Cần xác nhận:** #93 trả Notification hay Operation? Operation ID và notification ID được nối ra sao để #92/#96 reload đúng resource?

## Ranh giới giữ nguyên

Cho tới khi các câu hỏi trên được chốt, không đổi catalog/schema/diagram, không map `type`/`is_read`/delivery status sang field khác, và không đánh dấu DD Approved/Final.

## AC-36 macro-review result

- Status: `VERIFIED_WITH_OPEN_QUESTIONS` at document level; this API remains `Draft — Needs Confirmation`.
- Group findings and owner decisions: [AC-36 macro-review #92–#96](../96_admin_notifications_status/AC-36_MACRO_REVIEW.md).
- No runtime, live-schema, deployment, or owner approval is implied.
