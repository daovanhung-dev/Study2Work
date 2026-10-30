# Câu hỏi mở — Study API #93 Tạo/phát notification

**Trạng thái:** Draft — Needs Confirmation. Contract trực tiếp được giữ; runtime fallback đã triển khai nhưng chưa được owner duyệt.

<a id="q-93-01-notification-or-operation-response"></a>

## Q-93-01 — Response Notification hay Operation?

Catalog #93 row and AC-36 node n5 say ApiEnvelope<Notification> at 202. Operation tracking summary says data: Operation. Notification ID is int64; Operation ID schema is UUID. API #18 row says operation_id:int64 while diagram/schema use UUID.

**Runtime fallback:** `data` is the first per-recipient Notification; `meta.operation_id` is one shared UUID and `meta.notification_ids` lists all inserted int64 IDs.

**Ảnh hưởng:** Response metadata is not part of the direct row and does not resolve #18 Operation storage/polling or API #96 handoff.

**Cần xác nhận:** Response chính thức là Notification hay Operation? Nếu Operation, field nào nối notification_id:int64 với operation_id:uuid?

<a id="q-93-02-audience-selection"></a>

## Q-93-02 — Chọn recipients hay segment?

Both recipients?:int64[] and segment?:AudienceSegment are optional. AC-36 does not define XOR, empty array, duplicate rule, enum values, or audience predicate.

**Runtime fallback:** Require a non-empty explicit `recipients` list; require positive unique int64 IDs that exist in `users`; reject a supplied `segment` with 422. No recipient role/status/course rule is applied.

**Cần xác nhận:** Có duyệt fallback recipients-only không? Cung cấp AudienceSegment tokens, scope và eligibility predicate nếu cần hỗ trợ segment.

<a id="q-93-03-channel-values"></a>

## Q-93-03 — NotificationChannel values

`channels:NotificationChannel[]!` has no value set/minItems. Diagram names Push/Email; checked-in legacy delivery DDL uses `PUSH|EMAIL`. V1-PILOT permits IN_APP|EMAIL in a different delivery model.

**Runtime fallback:** Require non-empty unique uppercase `PUSH`/`EMAIL` and create one `QUEUED` outbox row per notification/channel. No provider mapping or delivery worker is wired.

**Cần xác nhận:** Channel token set có phải `PUSH`/`EMAIL` không? Empty/duplicate channels trả 422 hay được chuẩn hóa? Provider mapping nào được duyệt?

<a id="q-93-04-title-content-validation"></a>

## Q-93-04 — Title/content validation

Catalog only says required string. The selected checked-in legacy candidate has title `VARCHAR(200)` and content `TEXT`; that table is not an approved Admin target.

**Runtime fallback:** Reject whitespace-only title/content; preserve other input text; cap title at 200 using the selected local DDL candidate; no content maximum is added.

**Cần xác nhận:** Có duyệt các validation fallback này không? Độ dài/encoding limit chính thức nào áp dụng?

<a id="q-93-05-create-draft-or-send"></a>

## Q-93-05 — Tạo draft hay gửi ngay?

Purpose is Tạo/phát. Diagram branch CREATE/SEND writes Notification + recipients, then calls Push/Email if action is Send. Request has no action or scheduled_at. API #94 is described as updating draft/scheduled but does not define draft creation.

**Runtime fallback:** POST creates the notification rows and queues immediate asynchronous delivery intent. It returns 202 after local outbox commit. It does not call a provider; committed rows do not establish delivery success.

**Cần xác nhận:** POST luôn gửi ngay hay tạo draft? Nếu có action/schedule, API nào nhận các field đó?

<a id="q-93-06-persistence-and-recipient-grain"></a>

## Q-93-06 — Physical model, recipient grain and ID

AC-36 requires Notification + recipients. Runtime uses checked-in legacy BIGINT `notifications` rows with one `user_id` per recipient and `operation_id` UUID from migration 009, plus one `notification_deliveries` row per channel. The legacy candidate and migration are not proof of live schema or approved Admin storage. V1-PILOT UUID schema is separate.

**Runtime fallback:** One notification row per recipient; all rows share a UUID; delivery rows are keyed by notification ID and channel, in one DB transaction.

**Cần xác nhận:** Owner có duyệt legacy model này không, hay chọn Admin campaign schema riêng? Chốt campaign-vs-recipient grain, ID, recipient relation, channel/status storage and lifecycle.

<a id="q-93-07-acceptance-and-operation-lifecycle"></a>

## Q-93-07 — 202 acceptance and Operation lifecycle

Catalog returns 202; operation summary says Operation. No Study Operation store/queue producer was found. API Guidelines recommend Idempotency-Key for retryable mutations, but #93 does not declare it.

**Runtime fallback:** 202 is returned only after all Notification/outbox rows and response projection commit. `meta.operation_id` is grouping metadata only; no Operation record is created. DB OperationalError/invalidated connection maps to 503; other persistence/projection failures map to 500.

**Cần xác nhận:** Acceptance boundary, initial status, Operation storage, queue/retry policy and links to #18/#96? Có cần idempotency key không?

<a id="q-93-08-admin-permission"></a>

## Q-93-08 — Admin permission and caller identity

Catalog requires Admin; AC-36 requires notification-management permission. Runtime uses shared `ADMIN` role guard and the authenticated caller ID as `sender_id`; no fine-grained permission or tenant scope is checked.

**Cần xác nhận:** Permission key/claim, principal mapping, global/tenant scope and 401/403 precedence?

<a id="q-93-09-error-triggers"></a>

## Q-93-09 — 422, 503 and 500 triggers

Catalog lists codes but no field rules, queue dependency, transaction or rollback. Diagram does not define failure timing.

**Runtime fallback:** Request/audience/channel checks and unknown recipients map to 422. DB OperationalError or invalidated connection maps to 503; other SQL, projection, and commit failures map to 500. Insert-path failures attempt rollback.

**Cần xác nhận:** Approve validation and dependency triggers? Is DB unavailability the intended 503 condition, and what is the approved error-envelope detail?

<a id="q-93-10-notification-response-fields"></a>

## Q-93-10 — Status and optional Notification fields

Reusable Notification has channels/status/created_at and optional read_at/scheduled_at. Request has no status, read state or schedule; enum and storage are unknown.

**Runtime fallback:** `status` projects `QUEUED` from local outbox intent; `read_at` and `scheduled_at` are omitted; `created_at` comes from the first inserted notification row.

**Cần xác nhận:** Initial status, channel projection, and omit-vs-null rules?

## AC-36 boundary

AC-36 macro-review #92–#96 remains `VERIFIED_WITH_OPEN_QUESTIONS`. API #93 is wired and locally tested; current group status is #92–#95 wired and #96 unwired, as summarized in the macro-review. No catalog or diagram contract was changed.

## AC-36 macro-review result

- Status: `VERIFIED_WITH_OPEN_QUESTIONS` at document level; API #93 remains `Draft — Needs Confirmation`.
- Group findings and owner decisions: [AC-36 macro-review #92–#96](../96_admin_notifications_status/AC-36_MACRO_REVIEW.md).
- Local fake-DB tests do not prove live schema, deployment, provider delivery, or owner approval.
