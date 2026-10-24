# Câu hỏi còn mở — Study API #95 Admin xóa hoặc hủy notification

**Trạng thái DD:** Draft — Needs Confirmation. Contract DeleteResult trực tiếp được giữ; policy proposal chưa được duyệt.

<a id="q-95-01-eligibility"></a>
## Q-95-01 — Khi nào được xóa hoặc hủy?

**Evidence:** Catalog purpose ghi xóa draft/cancel nếu policy cho phép; AC-36 diagram chỉ ghi DELETE/mark cancelled. Không có NotificationStatus tokens hoặc state transition.

**Đề xuất DERIVED:** Draft chưa dispatch được logical remove; Scheduled chưa bắt đầu delivery được mark cancelled; khi delivery đã bắt đầu thì trả 422.

**Cần xác nhận:** State names/tokens, policy cho từng state, partial/in-flight delivery và điều kiện nào dùng 422?

<a id="q-95-02-hard-or-soft-delete"></a>
## Q-95-02 — Hard delete hay tombstone?

**Evidence:** DeleteResult yêu cầu deleted_at; legacy notifications không có deletion marker/timestamp. AC-36 mô tả DELETE/mark cancelled nhưng không chỉ physical operation.

**Đề xuất DERIVED:** Giữ Notification và history bằng logical tombstone/cancel marker; không hard-delete recipients/delivery history.

**Cần xác nhận:** Có duyệt logical deletion không? Chọn physical state/timestamp nào? Có retention/anonymization rule không?

<a id="q-95-03-scheduled-work"></a>
## Q-95-03 — Scheduler/queue cancellation

**Evidence:** Không tìm thấy Admin scheduler, queue producer, job ID hoặc cancellation endpoint. Diagram không nêu scheduler call.

**Đề xuất DERIVED:** Với Scheduled chưa dispatch, mark notification cancelled để worker không gửi; nếu external job tồn tại, contract phải xác nhận cancellation.

**Cần xác nhận:** Scheduler nào xử lý schedule? Mark cancelled có đủ ngăn dispatch không? In-flight call/ack/retry xử lý thế nào? Có Operation ID không?

<a id="q-95-04-delete-result"></a>
## Q-95-04 — DeleteResult khi action là cancellation

**Evidence:** Catalog response là DeleteResult với literal status="deleted" và required deleted_at; AC-36 cho phép mark cancelled.

**Đề xuất DERIVED:** Giữ literal deleted như contract; deleted_at là thời điểm logical remove/cancel được commit. Notification lifecycle state riêng có thể là cancelled.

**Cần xác nhận:** Literal deleted có đúng cho cancellation không? deleted_at do database hay service clock cung cấp? Timestamp offset/precision nào áp dụng?

<a id="q-95-05-repeat-request"></a>
## Q-95-05 — DELETE lặp lại và target đã bị hủy

**Evidence:** Catalog có 404 và 422 nhưng không định nghĩa idempotency. API #95 là DELETE; tombstone persistence chưa biết.

**Đề xuất DERIVED:** Nếu tombstone còn tồn tại, repeated DELETE trả 200 cùng DeleteResult và timestamp; target không tồn tại trả 404.

**Cần xác nhận:** Có duyệt idempotent no-op không? Tombstone có giữ đủ để trả cùng result không? Notification đã cancelled nhưng vẫn còn history thì lần xóa sau trả gì?

<a id="q-95-06-delivery-aggregate"></a>
## Q-95-06 — Nguồn quyết định delivery đã bắt đầu

**Evidence:** API #96 response là Notification, không có delivery aggregate fields; V1-PILOT delivery model dùng UUID và learner scope, không phải Admin campaign schema.

**Cần xác nhận:** Aggregate/query nào cho sent/in-flight delivery? Đơn vị là notification, recipient, channel hay attempt? Khi chỉ một recipient đã nhận, policy hủy còn cho phép không?

<a id="q-95-07-admin-permission"></a>
## Q-95-07 — Admin permission và 404 precedence

**Evidence:** Catalog role Admin; AC-36 yêu cầu notification-management permission; Study Admin guard chưa được xác minh.

**Cần xác nhận:** Claim/permission key, actor ID, tenant/global scope và thứ tự auth → resource lookup?

<a id="q-95-08-physical-model"></a>
## Q-95-08 — Physical model, transaction và timestamp

**Evidence:** Legacy BIGINT notifications thiếu lifecycle/deleted_at; V1-PILOT UUID notifications/deliveries khác grain và delivery rows append-only.

**Cần xác nhận:** Admin campaign table/columns, tombstone, audit, transaction boundary, race với dispatcher, rollback và clock source nào được duyệt?

<a id="q-95-09-error-behavior"></a>
## Q-95-09 — Trigger 404/422/500

**Evidence:** Direct error codes 401/403/404/422/500; missing target, policy refusal, repeat delete và scheduler failure chưa có mapping.

**Cần xác nhận:** Missing/tombstone precedence, exact 422 conditions, scheduler failure mapping và error envelope data shape. Không thêm 409/410/503 nếu chưa cập nhật contract.

<a id="q-95-10-ac36-macro"></a>
## Q-95-10 — Macro-review AC-36 và Operation bridge

**Evidence:** #92–#96 là nhóm Admin notification. #93 Notification-vs-Operation/ID bridge còn mở; #94 body/schedule cũng là DERIVED; #96 status response không chứa delivery aggregate.

**Cần xác nhận:** Sau khi #96 DD hoàn tất, owner cần chốt audience/campaign grain, send action/schedule handoff, update/cancel policy, status projection, Operation ID bridge và schema model chung.

## Ranh giới giữ nguyên

- DIRECT: DELETE path-only contract, Admin Bearer, DeleteResult shape, HTTP 200 và đúng 401/403/404/422/500; diagram DELETE/mark cancelled/reload.
- DERIVED: logical tombstone, Draft removal, Scheduled pre-dispatch cancel, preserve history, repeat DELETE no-op và 422 for disallowed state.
- SOURCE_REQUIRED: Admin schema, state enum, delivery-start query, scheduler, Admin permission, timestamp and transaction.
- DISCREPANCY: cancellation represented by status="deleted"; no #96 delivery aggregate source.

## AC-36 macro-review result

- Status: `VERIFIED_WITH_OPEN_QUESTIONS` at document level; this API remains `Draft — Needs Confirmation`.
- Group findings and owner decisions: [AC-36 macro-review #92–#96](../96_admin_notifications_status/AC-36_MACRO_REVIEW.md).
- No runtime, live-schema, deployment, or owner approval is implied.
