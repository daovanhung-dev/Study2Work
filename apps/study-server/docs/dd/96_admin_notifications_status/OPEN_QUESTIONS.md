# OPEN_QUESTIONS — Study API #96 Admin notification status

**Trạng thái DD:** `Draft — Needs Confirmation`. Direct contract được giữ nguyên; các query/projection dưới đây chưa được owner duyệt.

<a id="q-96-01-aggregate-source"></a>
## Q-96-01 — Delivery aggregate đọc từ nguồn nào?

**Bằng chứng:** AC-36 có node “Đọc delivery aggregate”. Legacy Study DDL không có Admin delivery relation. V1-PILOT có `notification_deliveries` nhưng UUID/learner scope khác contract int64.

**Cần xác nhận:** Chọn physical relation và environment/schema áp dụng; xác nhận có thể dùng V1-PILOT hay cần Admin model riêng. Không có SQL nào được chốt trong DD này.

<a id="q-96-02-grain-counts"></a>
## Q-96-02 — Aggregate có grain nào và count gì?

**Bằng chứng:** Reusable `NotificationDelivery` nêu `queued`, `sent`, `failed` nhưng không có recipient/channel/attempt grain hoặc cách xử lý retry/partial delivery.

**Cần xác nhận:** Count theo notification, recipient, channel hay attempt? Retry có thể tăng count nhiều lần không? Có snapshot/consistency requirement không?

<a id="q-96-03-response-projection"></a>
## Q-96-03 — Aggregate được biểu diễn trong response `Notification` ra sao?

**Bằng chứng:** Catalog #96 trả `ApiEnvelope<Notification>`; `Notification` không có queued/sent/failed hoặc result per channel. Diagram chỉ yêu cầu đọc aggregate.

**Đề xuất DERIVED:** Nếu response không đổi, chỉ dùng `Notification.status` hiện có làm projection sau khi owner chốt quy tắc; không thêm field.

**Cần xác nhận:** Status aggregate có cần trả về client không? Nếu có, status tokens và quy tắc ưu tiên failure/in-flight/success là gì? Có cần sửa catalog để dùng `NotificationDelivery` không?

<a id="q-96-04-notification-schema"></a>
## Q-96-04 — Admin Notification physical model

**Bằng chứng:** Legacy row có `id/title/content/type/is_read/created_at`, thiếu channels/status/read_at/scheduled_at và delivery link. Pilot Notification có UUID/learner grain.

**Cần xác nhận:** Chọn bảng, ID domain, recipient relation, channel storage, lifecycle/read/schedule fields và retention. Không map `is_read` sang status/read_at.

<a id="q-96-05-enums"></a>
## Q-96-05 — Các enum và field optional

**Bằng chứng:** `NotificationChannel`, `NotificationStatus` và `OperationStatus` được tham chiếu nhưng member values/semantics chưa có trong catalog source.

**Cần xác nhận:** Token/casing, status transitions, channel-vs-notification status, optional `read_at`/`scheduled_at` serialization và mapping `NotificationDelivery.status`.

<a id="q-96-06-permission-errors"></a>
## Q-96-06 — Admin permission, 403/404 và error envelope

**Bằng chứng:** AC-36 yêu cầu notification-management permission; current Study Admin guard chưa được xác minh. Catalog có 403/404/500; API Guidelines và helper khác nhau ở error `data` shape.

**Cần xác nhận:** Permission key, global/tenant scope, principal mapping, 403/404 precedence, missing/tombstoned behavior, malformed int64 path mapping và error envelope convention. Không thêm lỗi ngoài direct set.

<a id="q-96-07-operation-bridge"></a>
## Q-96-07 — API #93 Operation tracking và ID bridge

**Bằng chứng:** Catalog row/diagram #93 trả `Notification` với HTTP 202; Operation tracking prose nói notification POST trả `Operation`, có `operation_id:uuid` trong poll flow. #96 nhận `notification_id:int64`.

**Cần xác nhận:** #93 trả resource ID, Operation ID hay cả hai? Chốt bridge giữa operation lifecycle và notification delivery; không dùng int64 thay UUID.

<a id="q-96-08-macro-review"></a>
## Q-96-08 — AC-36 macro-review #92–#96

**Kết quả:** Tài liệu nhóm đã được macro-review sau khi #96 hoàn tất; xem [AC-36_MACRO_REVIEW.md](./AC-36_MACRO_REVIEW.md). Kết quả review chỉ xác nhận nhất quán tài liệu và các discrepancy, không xác nhận runtime/schema/owner decision.

## Ranh giới giữ nguyên

- DIRECT: GET/path/Admin Bearer/Notification response/200 và exact 401/403/404/500.
- DIRECT from diagram: bước đọc delivery aggregate trước reload.
- DERIVED: projection vào `Notification.status` chỉ là phương án cần duyệt.
- SOURCE_REQUIRED: Admin physical model, aggregate grain/rules, enum values, permission, empty/missing semantics và Operation bridge.
- DISCREPANCY: aggregate intent chưa có projection fields trong direct response; legacy/pilot schema không khớp Admin contract.
