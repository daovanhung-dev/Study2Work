# OPEN_QUESTIONS — Study API #96 Admin notification status

**Trạng thái DD:** `Draft — Needs Confirmation`. Direct contract được giữ nguyên. Source local có fallback cho query/projection; các lựa chọn vẫn chưa được owner duyệt.

<a id="q-96-01-aggregate-source"></a>
## Q-96-01 — Delivery aggregate đọc từ nguồn nào?

**Bằng chứng:** AC-36 có node “Đọc delivery aggregate”. Local #96 hiện dùng legacy BIGINT `notifications` và `notification_deliveries`, theo cùng candidate mà APIs #92–#95 sử dụng. V1-PILOT có UUID/learner scope khác contract int64.

**Cần xác nhận:** Owner có duyệt legacy BIGINT tables làm Admin source không, và migration 009 được áp dụng ở môi trường nào? V1-PILOT hiện không được #96 sử dụng.

<a id="q-96-02-grain-counts"></a>
## Q-96-02 — Aggregate có grain nào và count gì?

**Bằng chứng:** Reusable `NotificationDelivery` nêu `queued`, `sent`, `failed` nhưng không có recipient/channel/attempt grain hoặc cách xử lý retry/partial delivery.

**Cần xác nhận:** Count theo notification, recipient, channel hay attempt? Retry có thể tăng count nhiều lần không? Có snapshot/consistency requirement không?

<a id="q-96-03-response-projection"></a>
## Q-96-03 — Aggregate được biểu diễn trong response `Notification` ra sao?

**Bằng chứng:** Catalog #96 trả `ApiEnvelope<Notification>`; `Notification` không có queued/sent/failed hoặc result per channel. Local implementation hiện chiếu aggregate vào `channels/status` bằng precedence API #92.

**Fallback DERIVED hiện tại:** `channels` sắp xếp theo tên; `status` là `QUEUED` nếu có delivery queued, nếu không thì `FAILED` nếu có failed, nếu không thì `SENT` khi tất cả sent. Không thêm field vào response.

**Cần xác nhận:** Có duyệt các token, channel ordering, precedence và `Notification` projection hiện tại không? Aggregate cần phản ánh recipient hay attempt grain/retry? Có cần sửa catalog để trả `NotificationDelivery` không?

<a id="q-96-04-notification-schema"></a>
## Q-96-04 — Admin Notification physical model

**Bằng chứng:** Local fallback lấy `id/title/content/created_at` từ legacy row và channels/status từ delivery candidate. Legacy row thiếu `read_at/scheduled_at`; Pilot Notification có UUID/learner grain.

**Cần xác nhận:** Chọn bảng, ID domain, recipient relation, channel storage, lifecycle/read/schedule fields và retention. Local candidate không map `is_read` sang status/read_at.

<a id="q-96-05-enums"></a>
## Q-96-05 — Các enum và field optional

**Bằng chứng:** `NotificationChannel`, `NotificationStatus` và `OperationStatus` được tham chiếu nhưng member values/semantics chưa có trong catalog source.

**Cần xác nhận:** Token/casing, status transitions, channel-vs-notification status, optional `read_at`/`scheduled_at` serialization và mapping `NotificationDelivery.status`.

<a id="q-96-06-permission-errors"></a>
## Q-96-06 — Admin permission, 403/404 và error envelope

**Bằng chứng:** AC-36 yêu cầu notification-management permission; local source hiện gọi shared ADMIN guard, chưa có fine-grained permission. Catalog có 403/404/500; local helper trả error `data:null`.

**Cần xác nhận:** Permission key, global/tenant scope, principal mapping và chính thức hóa 403/404 precedence, missing/tombstoned behavior cùng malformed int64 mapping. Local fallback giữ error set chính xác và map invalid path/no-delivery thành 404.

<a id="q-96-07-operation-bridge"></a>
## Q-96-07 — API #93 Operation tracking và ID bridge

**Bằng chứng:** Catalog row/diagram #93 trả `Notification` với HTTP 202; Operation tracking prose nói notification POST trả `Operation`, có `operation_id:uuid` trong poll flow. #96 nhận `notification_id:int64`.

**Cần xác nhận:** #93 trả resource ID, Operation ID hay cả hai? Chốt bridge giữa operation lifecycle và notification delivery; không dùng int64 thay UUID.

<a id="q-96-08-macro-review"></a>
## Q-96-08 — AC-36 macro-review #92–#96

**Kết quả:** Tài liệu nhóm được macro-reviewed sau khi #96 wired; xem [AC-36_MACRO_REVIEW.md](./AC-36_MACRO_REVIEW.md). Local fallback không đóng các owner decisions về Admin schema, permission hay Operation bridge.

## Ranh giới giữ nguyên

- DIRECT: GET/path/Admin Bearer/Notification response/200 và exact 401/403/404/500.
- DIRECT from diagram: bước đọc delivery aggregate trước reload.
- DERIVED current source: legacy BIGINT row/outbox candidate, `Notification.channels/status` projection, status precedence, positive-ID parsing and invalid/no-delivery 404.
- SOURCE_REQUIRED: Admin physical model, aggregate grain/rules, enum approval, fine-grained permission, official empty/missing semantics and Operation bridge.
- DISCREPANCY: aggregate intent chưa có projection fields trong direct response; legacy/pilot schema không khớp Admin contract.
