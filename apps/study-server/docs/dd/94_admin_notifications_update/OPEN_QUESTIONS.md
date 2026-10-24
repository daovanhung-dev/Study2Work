# Câu hỏi còn mở — Study API #94 Admin cập nhật notification

**Trạng thái DD:** Draft — Needs Confirmation. Giữ contract catalog trực tiếp; body/state và persistence proposal chưa được duyệt.

<a id="q-94-01-request-body"></a>
## Q-94-01 — Request body của PUT
**Evidence:** Catalog #94 chỉ khai báo path notification_id:int64!; AC-36 chỉ nói UPDATE Notification. DD #93 có recipients, segment, title, content, channels; Notification schema có optional scheduled_at.
**Đề xuất DERIVED:** Full replacement gồm đúng một audience selector, title, content, channels, scheduled_at.
**Cần xác nhận:** API #94 có nhận body không? Field nào được sửa? Có field nào partial/optional hay body phải full replacement?

<a id="q-94-02-audience-update"></a>
## Q-94-02 — Có cho thay audience không?
**Evidence:** #93 hỗ trợ explicit recipients hoặc segment; #94 diagram không nhắc recipient mutation. Legacy table chỉ có một user_id; campaign-recipient relation chưa được xác nhận.
**Đề xuất DERIVED:** Nếu body được duyệt, đúng một trong recipients hoặc segment thay thế audience hiện tại.
**Cần xác nhận:** Có cho đổi audience không? Empty/duplicate recipient xử lý thế nào? Segment gồm predicate/token nào? Điều gì xảy ra với deliveries đã tạo?

<a id="q-94-03-field-validation"></a>
## Q-94-03 — Validation của title/content/channels
**Evidence:** #93 required title/content/channels nhưng không nêu blank, length, enum tokens, empty hay duplicate rules. Legacy title VARCHAR(200) chỉ là candidate.
**Cần xác nhận:** Trim/nonblank/length limits; NotificationChannel tokens; min/max số channel và duplicate policy.

<a id="q-94-04-schedule-body"></a>
## Q-94-04 — scheduled_at và draft/scheduled state
**Evidence:** Catalog mô tả cập nhật draft/scheduled conditionally; reusable Notification có optional scheduled_at; #94 body, enum state và queue behavior chưa được định nghĩa.
**Đề xuất DERIVED:** scheduled_at:null nghĩa là Draft; future timestamp nghĩa là Scheduled; request là full replacement. Đây là logical proposal, không xác nhận enum hoặc scheduler action.
**Cần xác nhận:** Null/omit semantics, past timestamp, timezone, precision, transition table và liệu reschedule có update/cancel queue hay không?

<a id="q-94-05-editability"></a>
## Q-94-05 — Trạng thái nào được sửa?
**Evidence:** Catalog purpose gợi ý draft/scheduled; không có enum values, state transition hoặc diagram guard chi tiết.
**Đề xuất DERIVED:** Chỉ cho cập nhật conceptual Draft/Scheduled; dispatched/cancelled trả 422 bằng code hiện có.
**Cần xác nhận:** Các state/token chính thức nào editable? Có cho sửa sau dispatch hoặc khi delivery đang chạy không? Missing/deleted target dùng 404 hay state conflict?

<a id="q-94-06-persistence"></a>
## Q-94-06 — Admin schema, recipient relation và transaction
**Evidence:** Legacy BIGINT notifications thiếu channels/status/scheduled_at và campaign recipient relation. V1-PILOT dùng UUID learner/delivery model riêng.
**Cần xác nhận:** Model nào là baseline? Cột/bảng nào lưu audience/channels/status/schedule? Update Notification và recipients có cùng transaction không? Audit/updated_at/locking/rollback do layer nào sở hữu?

<a id="q-94-07-admin-permission"></a>
## Q-94-07 — Admin permission
**Evidence:** Catalog role Admin; AC-36 yêu cầu notification-management permission; Study Admin guard/policy chưa được xác minh.
**Cần xác nhận:** Claim/permission key, actor mapping, global/tenant scope và thứ tự 401/403/404?

<a id="q-94-08-response-projection"></a>
## Q-94-08 — Notification response projection
**Evidence:** Direct response ApiEnvelope<Notification>. Logical fields include channels/status/created_at and optional read_at/scheduled_at; compatible Admin persistence projection chưa được tìm thấy.
**Cần xác nhận:** Enum/status source, omit-vs-null rules, channel persistence/projection và updated schedule projection. Không đổi cardinality hoặc thêm Operation fields trong DD này.

<a id="q-94-09-error-behavior"></a>
## Q-94-09 — Error triggers
**Evidence:** Direct codes 401/403/404/422/500; field rules, target lookup, state guard và transaction failure mapping chưa được đặc tả.
**Cần xác nhận:** 404 lookup/authorization precedence; body/state 422 triggers; rollback và error envelope behavior. Không thêm 409/503 khi chưa có contract.

<a id="q-94-10-ac36-macro"></a>
## Q-94-10 — Macro-review AC-36 và #93 Operation ID
**Evidence:** #92–#96 form notification management flow. #93 catalog/diagram response Notification conflicts with Operation tracking summary; Notification ID int64 and Operation ID UUID/int64 mismatch.
**Cần xác nhận:** Owner cần chốt #93 response/ID bridge, request action/schedule handoff, #94 edit scope, #95 cancel/delete semantics and #96 status grain before closing group review.

## Ranh giới proposal
- DIRECT: method/path/auth role/path type/no direct body or query/response/status/errors; diagram UPDATE Notification and reload intent.
- DERIVED: body fields, full replacement, audience XOR, conceptual Draft/Scheduled guard and null/future schedule interpretation.
- SOURCE_REQUIRED: physical schema, enums, permission policy, scheduler, transaction/audit, response field mapping.
- DISCREPANCY: UPDATE intent without body; logical campaign model versus current candidate schemas.

## AC-36 macro-review result

- Status: `VERIFIED_WITH_OPEN_QUESTIONS` at document level; this API remains `Draft — Needs Confirmation`.
- Group findings and owner decisions: [AC-36 macro-review #92–#96](../96_admin_notifications_status/AC-36_MACRO_REVIEW.md).
- No runtime, live-schema, deployment, or owner approval is implied.
