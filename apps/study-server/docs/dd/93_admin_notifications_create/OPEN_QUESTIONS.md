# Câu hỏi mở — Study API #93 Tạo/phát notification

**Trạng thái:** Draft — Needs Confirmation. Contract trực tiếp được giữ; proposal DERIVED chưa được duyệt.

<a id="q-93-01-notification-or-operation-response"></a>

## Q-93-01 — Response Notification hay Operation?

Catalog #93 row and AC-36 node n5 say ApiEnvelope<Notification> at 202. Operation tracking summary says data: Operation. Notification ID is int64; Operation ID schema is UUID. API #18 row says operation_id:int64 while diagram/schema use UUID.

**Ảnh hưởng:** Client không biết response data và ID nào dùng cho #96 hoặc #18.

**Cần xác nhận:** Response chính thức là Notification hay Operation? Nếu Operation, field nào nối notification_id:int64 với operation_id:uuid?

<a id="q-93-02-audience-selection"></a>

## Q-93-02 — Chọn recipients hay segment?

Both recipients?:int64[] and segment?:AudienceSegment are optional. AC-36 does not define XOR, empty array, duplicate rule, enum values, or audience predicate.

**Đề xuất DERIVED:** Yêu cầu đúng một selector; recipients phải không rỗng và không trùng.

**Cần xác nhận:** Có duyệt đề xuất này không? Cung cấp AudienceSegment tokens, scope và eligibility predicate.

<a id="q-93-03-channel-values"></a>

## Q-93-03 — NotificationChannel values

channels:NotificationChannel[]! has no value set/minItems. Diagram names Push/Email. V1-PILOT permits IN_APP|EMAIL in a different delivery model.

**Đề xuất DERIVED:** Yêu cầu một channel trở lên và từ chối trùng; chốt provider mapping sau khi enum được duyệt.

**Cần xác nhận:** Channel token set là gì? Empty/duplicate channels trả 422 hay được chuẩn hóa?

<a id="q-93-04-title-content-validation"></a>

## Q-93-04 — Title/content validation

Catalog only says required string. Legacy title is VARCHAR(200) and content is TEXT, but that table is not an approved target.

**Đề xuất DERIVED:** Reject blank after trim; do not set max lengths before choosing schema.

**Cần xác nhận:** Có trim/nonblank rule không? Độ dài/encoding limit nào áp dụng?

<a id="q-93-05-create-draft-or-send"></a>

## Q-93-05 — Tạo draft hay gửi ngay?

Purpose is Tạo/phát. Diagram branch CREATE/SEND writes Notification + recipients, then calls Push/Email if action is Send. Request has no action or scheduled_at. API #94 is described as updating draft/scheduled but does not define draft creation.

**Đề xuất DERIVED:** POST creates and enqueues immediate send; delivery is asynchronous.

**Cần xác nhận:** POST luôn gửi ngay hay tạo draft? Nếu có action/schedule, API nào nhận các field đó?

<a id="q-93-06-persistence-and-recipient-grain"></a>

## Q-93-06 — Physical model, recipient grain and ID

AC-36 requires Notification + recipients. Legacy BIGINT notifications has one user_id plus sender/title/content/type/is_read/created_at; it lacks campaign relation/channels/status/scheduled_at. V1-PILOT UUID schema is learner-scoped.

**Cần xác nhận:** Chọn Admin schema; chốt campaign-vs-recipient grain, ID, recipient relation and channel/status storage.

<a id="q-93-07-acceptance-and-operation-lifecycle"></a>

## Q-93-07 — 202 acceptance and Operation lifecycle

Catalog returns 202; operation summary says Operation. No Study Operation store/queue producer was found. API Guidelines recommend Idempotency-Key for retryable mutations, but #93 does not declare it.

**Đề xuất DERIVED:** Return 202 after durable acceptance; keep operation_id separate from notification_id and add idempotency only through explicit contract.

**Cần xác nhận:** Acceptance boundary, initial status, Operation storage, queue/retry policy and links to #18/#96?

<a id="q-93-08-admin-permission"></a>

## Q-93-08 — Admin permission and caller identity

Catalog requires Admin; AC-36 requires notification-management permission; current Study source has no verified #93 guard.

**Cần xác nhận:** Permission key/claim, principal mapping, global/tenant scope and 401/403 precedence?

<a id="q-93-09-error-triggers"></a>

## Q-93-09 — 422, 503 and 500 triggers

Catalog lists codes but no field rules, queue dependency, transaction or rollback. Diagram does not define failure timing.

**Đề xuất DERIVED:** 503 before acceptance if queue/dependency rejects; post-202 provider failure belongs to delivery lifecycle.

**Cần xác nhận:** Validation mapping, acceptance boundary, rollback and error envelope?

<a id="q-93-10-notification-response-fields"></a>

## Q-93-10 — Status and optional Notification fields

Reusable Notification has channels/status/created_at and optional read_at/scheduled_at. Request has no status, read state or schedule; enum and storage are unknown.

**Cần xác nhận:** Initial status, channel projection and omit-vs-null rules?

## AC-36 boundary

AC-36 macro-review #92–#96 is complete at document level; the cross-API report records the remaining #93 response/action/Operation ID questions. No catalog or diagram contract was changed.

## AC-36 macro-review result

- Status: `VERIFIED_WITH_OPEN_QUESTIONS` at document level; this API remains `Draft — Needs Confirmation`.
- Group findings and owner decisions: [AC-36 macro-review #92–#96](../96_admin_notifications_status/AC-36_MACRO_REVIEW.md).
- No runtime, live-schema, deployment, or owner approval is implied.
