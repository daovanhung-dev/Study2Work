# OPEN_QUESTIONS — Study API #63

Trạng thái DD: `Draft — Needs Confirmation`. Các quyết định local dưới đây là `DERIVED` theo quy tắc giải quyết conflict của task; chúng chưa phải policy được contract owner phê duyệt. Runtime source và test xác minh local behavior, không chứng minh live DB hay provider delivery.

<a id="q-63-01-course-scope"></a>

## Q-63-01 — Thiếu course_id trong request

**Bằng chứng:** AC-25 chọn một course rồi gọi API #62 để lấy roster; body #63 không có `course_id`.

**Fallback runtime:** Yêu cầu toàn bộ recipient IDs cùng là Student có ACTIVE enrollment trong ít nhất một course do Mentor trực tiếp sở hữu. Nếu không có common course, trả 403. Không thêm field ngoài direct catalog.

**Giới hạn còn lại:** Server không thể chứng minh đó chính là course đang chọn trên UI; một recipient set có thể cùng xuất hiện trong nhiều course Mentor sở hữu.

**Cần xác nhận:** Contract owner có muốn thêm `course_id:int64!` để bind chính xác vào course đã chọn không?

<a id="q-63-02-recipient-encoding"></a>

## Q-63-02 — Encoding và ID của recipients

**Bằng chứng:** Catalog khai báo string; API #62 hiện trả `UserSummary[]` với numeric BIGINT `users.id`; legacy enrollments dùng BIGINT.

**Fallback runtime:** CSV positive int64 User IDs, ví dụ `101,202`; trim từng item, reject item rỗng/sai range, collapse duplicate giữ lần đầu. Server kiểm tra lại role/enrollment/scope.

**Trạng thái:** `DERIVED`; không phải encoding được contract owner phê duyệt.

<a id="q-63-03-content-type"></a>

## Q-63-03 — Wire type của `content`

**Trạng thái 2026-11-21:** `RESOLVED_FOR_ME-14` theo quyết định người dùng: request `content` là `string`, khớp nội dung văn bản trong editor, reusable Notification và legacy TEXT column. Catalog, model, OpenAPI và tests đã được đồng bộ.

**Bằng chứng:** Trước reconcile, catalog dùng int64 trong khi AC-25, ME-14 editor, reusable Notification và legacy DDL dùng text. Current source đã nhận strict string và ghi text trực tiếp.

**Giới hạn còn lại:** API #63 không bổ sung business rule về trim/non-empty/content max length; current ME-14 UI validates its own composer input.

**Kết quả:** API #63 accepts text; no template ID interpretation is implemented.

<a id="q-63-04-channel-encoding"></a>

## Q-63-04 — Encoding và channel values

**Bằng chứng:** Diagram ghi Push/Email; body là string; V1-PILOT IN_APP/EMAIL thuộc một UUID schema riêng, không khớp Study legacy BIGINT.

**Fallback runtime:** CSV `PUSH` và/hoặc `EMAIL`, case-sensitive; token trùng được collapse, token khác trả 422. Mỗi notification/channel tạo một QUEUED outbox row.

**Trạng thái:** `DERIVED`; provider mapping và enum chuẩn vẫn cần xác nhận.

<a id="q-63-05-persistence"></a>

## Q-63-05 — Local notification/delivery schema

**Bằng chứng:** Legacy `notifications` có BIGINT ID và một `user_id` mỗi row nhưng thiếu group/delivery relation; V1-PILOT dùng UUID learner và channel delivery khác contract.

**Fallback runtime:** Migration 009 thêm nullable `notifications.operation_id UUID` và bảng legacy BIGINT `notification_deliveries`, một row mỗi channel. Một notification row được tạo cho từng recipient.

**Trạng thái:** `DERIVED_LOCAL_DDL`; migration chưa áp dụng và live schema chưa được probe.

<a id="q-63-06-async-lifecycle"></a>

## Q-63-06 — Outbox, worker, retry và 202

**Bằng chứng:** AC-25 đặt Push/Email sau bước lưu; 202 chỉ có thể xác nhận acceptance. Study không có queue, worker hoặc provider notification hiện hữu.

**Fallback runtime:** Ghi Notification rows và toàn bộ QUEUED delivery rows trong một transaction; chỉ trả 202 sau commit. Database table là durable outbox input.

**Giới hạn còn lại:** Không có worker/provider tiêu thụ hàng đợi; trạng thái không tự tiến khỏi QUEUED. Retry, idempotency key, partial failure và delivery guarantees chưa được triển khai.

<a id="q-63-07-operation-result"></a>

## Q-63-07 — Operation schema, values và persistence

**Bằng chứng:** Reusable Operation dùng UUID nhưng kind/status values và Study operations table chưa có source; `result` chỉ khai báo Payment.

**Fallback runtime:** Project Operation từ notification batch với `kind=NOTIFICATION_DISPATCH`, `status=QUEUED`, numeric Mentor owner và DB created timestamp; lưu UUID group key trên notification rows. Optional `result` được bỏ qua.

**Trạng thái:** Các enum/status values và projection là `DERIVED`; API #18 chưa được implement.

<a id="q-63-08-notification-id-handoff"></a>

## Q-63-08 — Cầu nối sang API #64

**Bằng chứng:** #63 `data.id` là Operation UUID, còn #64 path nhận notification int64.

**Fallback runtime:** Giữ response `ApiEnvelope<Operation>` và thêm `meta.notification_ids:int64[]`, chứa IDs theo thứ tự recipient. Client gọi #64 cho từng ID; Operation UUID không thay notification ID.

**Giới hạn còn lại:** #64 response/aggregate semantics vẫn là contract trực tiếp `Operation` dù use case là delivery status; API #64 runtime sẽ được xử lý ở session riêng.

<a id="q-63-09-api18"></a>

## Q-63-09 — API #18 notification tracking handoff

**Trạng thái 2026-11-21:** `RESOLVED_FOR_SH-07` for notification-only tracking. API #18 catalog and current source use UUID; lookup is owner-bound for Student/Mentor/Admin. The user approved ME-14/#63 as one SH-07 producer.

**Current behavior:** #63 returns an Operation UUID and `meta.notification_ids`; SH-07 consumes the UUID via API #18. The IDs in metadata remain available to API #64.

**Còn mở ngoài SH-07:** Generic payment/export results, status lifecycle, retention, polling and other producer mappings remain Draft.

<a id="q-63-10-error-envelope"></a>

## Q-63-10 — Error envelope khi wired

**Bằng chứng:** API #63 nằm trong middleware `DESIGN_CONTRACT_PATHS`; view dùng shared `error_response(...)`.

**Current behavior:** Error envelope có `data:null`, exact catalog status/business code và trace ID. Đây là source/runtime behavior được HTTP tests xác minh.

## Handoff AC-25

- #62 → #63: #62 trả numeric Student IDs; #63 parse CSV và xác minh lại ACTIVE roster.
- #63 → #64: `meta.notification_ids` đưa từng numeric ID cho endpoint status; local outbox rows là query candidate cho #64.
- #63 → #18 → SH-07: current UUID and owner-bound notification status flow is source-wired; generic non-notification tracking remains outside scope.
- Macro-review vẫn `VERIFIED_WITH_OPEN_QUESTIONS`; xem [API #64 report](../64_mentor_notifications_status/VERIFICATION_REPORT.md). Local implementation does not prove delivery worker, live schema or deployment.
