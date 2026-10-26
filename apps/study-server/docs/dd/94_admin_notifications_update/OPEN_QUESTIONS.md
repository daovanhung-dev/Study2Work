# Câu hỏi còn mở — Study API #94 Admin cập nhật notification

**Trạng thái DD:** Draft — Needs Confirmation. Runtime có body và editability fallback DERIVED; catalog/diagram chưa khai báo body và owner chưa duyệt persistence/policy.

<a id="q-94-01-request-body"></a>
## Q-94-01 — Request body của PUT
**Evidence:** Catalog #94 chỉ khai báo path `notification_id:int64!`; AC-36 chỉ nói UPDATE Notification. Runtime hiện nhận strict `{title, content}` vì legacy candidate có đúng hai cột text có thể cập nhật.
**Cần xác nhận:** Có duyệt body này không? Cần partial update hay full replacement? Có field nào khác được phép sửa?

<a id="q-94-02-audience-update"></a>
## Q-94-02 — Có cho thay audience không?
**Evidence:** Legacy `notifications.user_id` lưu một recipient trên mỗi row; không có campaign-recipient relation. Runtime giữ nguyên recipient và từ chối `recipients`/`segment` như field ngoài schema.
**Cần xác nhận:** Có cần thay audience không? Nếu có, relation/predicate, empty/duplicate policy và ảnh hưởng đến delivery history là gì?

<a id="q-94-03-field-validation"></a>
## Q-94-03 — Validation của title/content/channels
**Evidence:** Runtime fallback yêu cầu title/content nonblank; title tối đa 200 theo legacy DDL candidate. Channels không nhận trong body và chỉ được đọc từ delivery rows.
**Cần xác nhận:** Duyệt giới hạn 200 và nonblank? Có yêu cầu trim? Có cần hỗ trợ đổi channels, token nào và quy tắc duplicate/empty ra sao?

<a id="q-94-04-schedule-body"></a>
## Q-94-04 — scheduled_at và draft/scheduled state
**Evidence:** Legacy BIGINT schema không có scheduled_at hoặc scheduler; runtime không đổi lịch và không dispatch/cancel queue.
**Cần xác nhận:** Có cần cập nhật lịch không? Nếu có, định nghĩa timezone, past timestamp, state transitions và coordination với scheduled jobs.

<a id="q-94-05-editability"></a>
## Q-94-05 — Trạng thái nào được sửa?
**Evidence:** Catalog prose gợi ý draft/scheduled nhưng không định nghĩa trạng thái. Runtime fallback chỉ sửa khi có ít nhất một outbox row và mọi row `QUEUED`; trạng thái này không được gọi là Draft/Scheduled.
**Cần xác nhận:** Duyệt điều kiện QUEUED này hay cung cấp lifecycle model/state transition chính thức? Xử lý row không có delivery, failed, canceled hoặc đang dispatch thế nào?

<a id="q-94-06-persistence"></a>
## Q-94-06 — Admin schema và transaction
**Evidence:** Runtime dùng checked-in legacy BIGINT candidate; V1-PILOT dùng UUID learner model khác. Fake-session tests không xác minh PostgreSQL/live schema.
**Cần xác nhận:** Legacy schema có phải Admin baseline không? Có cần migration/audit/updated_at hoặc campaign grain? Transaction/locking owner nào chịu trách nhiệm?

<a id="q-94-07-admin-permission"></a>
## Q-94-07 — Admin permission
**Evidence:** Catalog role Admin; AC-36 yêu cầu notification-management permission; runtime chỉ dùng shared ADMIN role guard.
**Cần xác nhận:** Claim/permission key, actor mapping, global/tenant scope và thứ tự 401/403/404?

<a id="q-94-08-response-projection"></a>
## Q-94-08 — Notification response projection
**Evidence:** Catalog yêu cầu `ApiEnvelope<Notification>`. Runtime tái dùng response #92; channels/status lấy từ outbox và read_at/scheduled_at bị omit do candidate schema không có mapping.
**Cần xác nhận:** Có duyệt projection recipient-level và QUEUED không? Cần `read_at`/`scheduled_at` hay campaign-level aggregate không? Không thêm Operation fields tự động.

<a id="q-94-09-error-behavior"></a>
## Q-94-09 — Error triggers
**Evidence:** Direct codes 401/403/404/422/500. Runtime dùng 422 cho validation và target không có/không còn QUEUED deliveries.
**Cần xác nhận:** Duyệt các trigger 422 và thứ tự lookup/authorization? Có tombstone/deleted behavior nào?

<a id="q-94-10-ac36-macro"></a>
## Q-94-10 — Macro-review AC-36 và #93 Operation ID
**Evidence:** #92–#96 tạo management flow; #93 Notification-vs-Operation response và ID bridge vẫn chưa được giải quyết. API #95 is now wired locally; #96 remains unwired. Xem macro-review để đọc trạng thái hiện tại.
**Cần xác nhận:** Owner chốt #93 response/ID bridge, #94 edit scope, #95 cancel/delete semantics, #96 status grain và shared Admin policy trước khi đóng review.

## Ranh giới proposal

- DIRECT: method/path/auth role/path type/response/status/errors; diagram UPDATE Notification/reload.
- WIRED DERIVED fallback: body `{title, content}`, validation local, target row grain, all-QUEUED eligibility, response projection từ outbox.
- PRESERVED: audience, channels, schedule, read state, delivery rows và `created_at`.
- SOURCE_REQUIRED: owner approval, live Admin schema, fine-grained permission, campaign/scheduler/lifecycle policy.

## AC-36 macro-review result

- Status: `VERIFIED_WITH_OPEN_QUESTIONS` at document level; this API remains `Draft — Needs Confirmation`.
- Group findings and owner decisions: [AC-36 macro-review #92–#96](../96_admin_notifications_status/AC-36_MACRO_REVIEW.md).
- Local tests do not imply live-schema, deployment, provider or owner approval.
