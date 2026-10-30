# Câu hỏi còn mở — Study API #95 Admin xóa hoặc hủy notification

**Trạng thái DD:** Draft — Needs Confirmation. Direct contract and local fallback are documented separately. Implementation is locally wired and fake-DB tested; owner approval, live schema and external cancellation remain unverified.

<a id="q-95-01-eligibility"></a>
## Q-95-01 — Lifecycle policy và eligibility

**Evidence:** Catalog purpose ghi xóa draft/cancel nếu policy cho phép; AC-36 diagram chỉ ghi `DELETE/mark cancelled`. Legacy model không có Draft/Scheduled status.

**Local fallback DERIVED:** Chỉ cho phép khi có ít nhất một delivery row và tất cả row đang `QUEUED`; thiếu delivery hoặc có `SENT/FAILED` trả 422. Runtime không suy ra enum Draft/Scheduled.

**Cần xác nhận:** Quy tắc queued-only có phản ánh lifecycle được duyệt không? Trạng thái nào đại diện cho draft/scheduled/in-flight?

<a id="q-95-02-hard-or-soft-delete"></a>
## Q-95-02 — Hard delete hay tombstone/retention

**Evidence:** Checked-in legacy FK `notification_deliveries.notification_id` dùng `ON DELETE CASCADE`; notification không có deleted_at/status. API #93/#94 hiện dùng cùng candidate legacy rows.

**Local fallback DERIVED:** DELETE đúng parent row; FK cascade loại bỏ queued delivery rows của parent. Không xóa sibling recipients cùng `operation_id`.

**Cần xác nhận:** Có duyệt retention/cascade này cho Admin notification không? Cần tombstone hoặc audit trail nào?

<a id="q-95-03-scheduled-work"></a>
## Q-95-03 — Scheduler/queue cancellation

**Evidence:** Không tìm thấy Admin scheduler, worker, job ID hoặc cancellation endpoint. Diagram không nêu scheduler call.

**Local behavior:** Xóa parent và outbox candidate trong DB transaction; không gọi external system và không tuyên bố đã ngăn provider send.

**Cần xác nhận:** Scheduler nào xử lý queued work? Có cần cancellation API/ack, worker synchronization hoặc retry policy không?

<a id="q-95-04-delete-result"></a>
## Q-95-04 — DeleteResult khi diagram nói cancellation

**Evidence:** Catalog yêu cầu literal `status="deleted"` và `deleted_at`; AC-36 cho phép `mark cancelled`.

**Local fallback DERIVED:** Trả direct literal và map `deleted_at` từ DB `CURRENT_TIMESTAMP` trong DELETE RETURNING; đây không phải tombstone timestamp.

**Cần xác nhận:** DeleteResult có đúng khi nghiệp vụ gọi đây là cancel? Có cần persisted audit timestamp/offset precision khác không?

<a id="q-95-05-repeat-request"></a>
## Q-95-05 — DELETE lặp lại

**Evidence:** Catalog có 404 nhưng không khai báo idempotency/tombstone.

**Local fallback DERIVED:** Sau hard delete, request lặp không tìm thấy parent và trả 404.

**Cần xác nhận:** Có yêu cầu repeated DELETE trả success không? Nếu có, cần tombstone/idempotency record nào?

<a id="q-95-06-delivery aggregate và race với dispatcher"></a>
## Q-95-06 — Delivery source và race

**Evidence:** #96 response là Notification, không có delivery aggregate. Local #93 creates per-channel queued rows; #94 locks parent trước child. No worker protocol is source-backed.

**Local fallback DERIVED:** Lock parent then child rows and require all QUEUED; fake DB tests verify SQL ordering only.

**Cần xác nhận:** Worker claim/dispatch lock order, in-flight semantics, aggregate grain and race handling nào được duyệt?

<a id="q-95-07-admin-permission"></a>
## Q-95-07 — Fine-grained Admin permission

**Evidence:** Catalog role Admin; AC-36 yêu cầu notification-management permission; shared Study guard hiện kiểm tra ADMIN role.

**Local fallback:** Dùng shared ADMIN guard như #92–#94; không tuyên bố dedicated permission đã wire.

**Cần xác nhận:** Permission claim/key, principal mapping và tenant/global scope nào được duyệt?

<a id="q-95-08-live-schema-and-transaction"></a>
## Q-95-08 — Live schema và transaction

**Evidence:** DB.sql/migration 009 được kiểm tra trong repo; test API dùng fake DB; không có live DB/deployment verification.

**Local fallback:** Khóa parent/delivery, DELETE, build/validate response rồi commit; query/mapping/commit failure rollback.

**Cần xác nhận:** Migration/deployment/live FK cascade có đúng môi trường target không? Có yêu cầu audit/transaction khác không?

<a id="q-95-09-error-behavior"></a>
## Q-95-09 — Error triggers

**Evidence:** Catalog errors are exactly 401/403/404/422/500; it does not define parse or eligibility triggers.

**Local fallback DERIVED:** Invalid/non-positive/out-of-range path → 422; missing target → 404; no/started delivery → 422; unexpected SQL/projection/commit failure → 500.

**Cần xác nhận:** Các trigger này có cần đổi khi lifecycle contract được chốt? Không thêm 409/410/503 nếu catalog không đổi.

<a id="q-95-10-ac36-macro"></a>
## Q-95-10 — AC-36 macro-review và Operation bridge

**Evidence:** #92–#96 share Admin notification workflow. #93 Notification-vs-Operation/ID bridge remains open; #96 direct response lacks aggregate fields.

**Cần xác nhận:** Owner cần chốt audience/campaign grain, send/schedule handoff, update/cancel policy, status projection, Operation bridge và schema model chung.

## Ranh giới giữ nguyên

- DIRECT: DELETE path-only contract, Bearer/Admin role, DeleteResult shape, HTTP 200, exact 401/403/404/422/500 codes; diagram says DELETE/mark cancelled/reload.
- DERIVED: positive signed-int64 parsing, legacy recipient-row target, queued-only eligibility, physical delete/cascade, DB timestamp and repeated-delete 404.
- SOURCE_REQUIRED: lifecycle/retention approval, dedicated permission, live schema/deployment, worker/scheduler contract, in-flight race and Operation bridge.
- DISCREPANCY: diagram says cancellation while result literal says deleted; no external cancellation acknowledgement is represented.

## AC-36 macro-review result

- Status: `VERIFIED_WITH_OPEN_QUESTIONS` at document level; this API remains `Draft — Needs Confirmation`.
- Group findings and owner decisions: [AC-36 macro-review #92–#96](../96_admin_notifications_status/AC-36_MACRO_REVIEW.md).
- Local API tests do not imply runtime deployment, live schema, provider delivery or owner approval.
