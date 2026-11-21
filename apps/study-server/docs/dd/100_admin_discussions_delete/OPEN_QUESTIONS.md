# OPEN_QUESTIONS — Study API #100

**Status:** Draft — Needs Confirmation
**Endpoint:** `DELETE /api/v1/admin/discussions/{discussion_id}`

## Q-100-01 — Soft-delete status marker

**Evidence:** AC-37 yêu cầu soft delete. Legacy `discussions.status` là nullable `VARCHAR(20)` default `ACTIVE`, nhưng không có enum/token `DELETED` được duyệt.

**Impact:** Không thể chọn physical state transition hoặc predicate loại bản ghi đã xóa.

**Decision needed:** Phê duyệt status token, trạng thái nguồn hợp lệ, chuyển trạng thái và cách xử lý request lặp. `DELETED` trong DD chỉ là DERIVED proposal.

## Q-100-02 — `deleted_at` source and persistence

**Evidence:** `DeleteResult` yêu cầu `deleted_at:date-time`; legacy `discussions` chỉ có `updated_at` và không có `deleted_at`.

**Impact:** Response bắt buộc không có nguồn persistence riêng; đọc lại thời điểm xóa không được định nghĩa.

**Decision needed:** Chọn schema/clock cho delete timestamp hoặc phê duyệt dùng chung `updated_at`. Dùng `updated_at` hiện chỉ là DERIVED.

## Q-100-03 — Audit trail meaning and storage

**Evidence:** Diagram ghi “preserve audit trail”; legacy Discussion DDL không có audit relation. Pilot `admin_adjustments.target_id`/`audit_events.resource_id` là UUID, không map được trực tiếp sang legacy BIGINT theo evidence hiện có.

**Impact:** Chưa biết lịch sử nào phải giữ, có append delete event mới không, actor/resource ID nào được ghi, retention và transaction/failure behavior.

**Decision needed:** Chỉ định audit source/table và key mapping; xác định append semantics, fields, retention, atomicity và behavior khi audit write lỗi.

## Q-100-04 — Already deleted and target eligibility

**Evidence:** Catalog có 404 cho resource not found; diagram không nói request lặp hoặc trạng thái target trước khi xóa.

**Impact:** Response 404, 200 idempotent hay conflict cho target đã xóa/chưa moderation đều chưa xác định.

**Decision needed:** Phê duyệt trạng thái được phép xóa, việc #99 có phải precondition, và semantics khi target đã xóa.

## Q-100-05 — Replies, reports and queue visibility

**Evidence:** `discussions.parent_id` hỗ trợ cây discussion; AC-37 #100 chỉ nêu soft delete target. #97 reloads queue nhưng không có deleted-item predicate/report history rule.

**Impact:** Chưa rõ xóa topic có ẩn reply không, xóa reply có ảnh hưởng topic không, report record được giữ/ẩn thế nào, và target còn xuất hiện ở #97/#98 không.

**Decision needed:** Quy định target root/reply, child visibility/cascade, report retention và queue/detail filter sau khi soft delete.

## Q-100-06 — Admin authorization and actor identity

**Evidence:** Catalog yêu cầu Admin Bearer JWT. Current Study helper chỉ có Student guard; chưa có Admin claims/policy.

**Impact:** Không thể kiểm tra role hoặc liên kết actor với audit trail bằng source hiện tại.

**Decision needed:** Xác định issuer/claim/role Admin, principal ID mapping, scope và audit actor reference.

## Q-100-07 — 422 and path parsing

**Evidence:** Catalog khai báo 422 `DESIGN_VALIDATION_ERROR` nhưng chỉ mô tả path `discussion_id:int64!`; không nêu parse/overflow rule.

**Impact:** Trigger, error detail và mapping path lỗi chưa ổn định.

**Decision needed:** Xác nhận invalid int64 behavior và giữ code theo catalog; không thêm error code.

## Q-100-08 — Transaction, concurrency and retry

**Evidence:** Diagram không quy định locking, transaction, retry hoặc idempotency. State update và audit trail có liên quan.

**Impact:** Race và audit partial failure có thể làm response/mutation khác nhau.

**Decision needed:** Chọn atomicity, locking/optimistic condition, retry/idempotency behavior và commit/rollback policy.

## Q-100-09 — Connected AC-37 contract gaps

**Evidence:** #97/#98 đọc reports nhưng `Discussion` response không có report fields; legacy DDL thiếu report relation/title; #99/#100 audit persistence và #100 queue visibility còn mở.

**Impact:** Group AC-37 chưa implementation-ready dù trình tự endpoint thống nhất.

**Decision needed:** Phê duyệt report data contract/persistence, Discussion projection, moderation state/audit mapping và deleted visibility across #97–#100. Xem macro-review trong [PLAN_RESULT.md](./PLAN_RESULT.md).
