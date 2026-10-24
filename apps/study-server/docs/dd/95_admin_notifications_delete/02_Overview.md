---
title: "Overview"
order: 2
dd_id: "95"
api_name: "Admin xóa hoặc hủy notification"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #95 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-36 |
| Method | DELETE |
| Endpoint | /api/v1/admin/notifications/{notification_id} |
| Purpose | Xóa draft/cancel notification nếu policy cho phép; điều kiện cụ thể chưa được nguồn định nghĩa. |
| Consumer/Actor | Admin có notification-management permission |
| Authentication | Bearer JWT |
| Authorization | Catalog role Admin; AC-36 yêu cầu notification-management permission. Study Admin guard/policy chưa được xác minh. |
| Direct request | Path notification_id:int64!; không body/query. |
| Direct response | HTTP 200 DESIGN_RESOURCE_DELETED, ApiEnvelope<DeleteResult>. |
| DeleteResult | id:int64, status literal "deleted", deleted_at:date-time. |
| Direct errors | 401/403/404/422/500 đúng business codes trong catalog. |
| Current implementation | UNWIRED / NOT_FOUND: không có route/module/test API #95 trong scoped Study source scan. |
| Transaction | Không được catalog/diagram quy định. |
| Side effects | Diagram ghi DELETE/mark cancelled rồi reload management; physical write và scheduler effect chưa rõ. |
| DD status | Draft — Needs Confirmation |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — #92–#96, DeleteResult, Notification, NotificationChannel, NotificationStatus.
- [AC/API index, AC-36](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin permission, postcondition và các API notification.
- [AC-36 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — DELETE branch: API #95 → DELETE/mark cancelled → reload notification management.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) và [legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — BIGINT notification row; không có lifecycle tombstone/time column.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — UUID learner notification/delivery schema riêng.
- [DD #92](../92_admin_notifications_list/02_Overview.md), [DD #93](../93_admin_notifications_create/02_Overview.md), [DD #94](../94_admin_notifications_update/02_Overview.md) — shared schema, create/update lifecycle và outstanding Operation/schema gaps.
- [DELETE precedent #77](../77_admin_course_delete/02_Overview.md), [DELETE precedent #90](../90_admin_quizzes_delete/02_Overview.md) — giữ DeleteResult direct, tách policy-derived behavior khỏi physical schema.
- [Current Study router](../../../app/api/v1.py), [middleware](../../../app/core/middleware.py), [API Guidelines](../../../../../contracts/api-guidelines/README.md).

## Tables/entities read

| Relation/entity | Candidate fields | Basis/status |
|---|---|---|
| Legacy notifications | id, user_id, sender_id, title, content, type, is_read, created_at | BIGINT recipient-row candidate; không có status, scheduled_at, deleted_at hoặc campaign relation. |
| V1-PILOT notifications | UUID id, learner_id, category, title, body, read_at, expires_at, created_at | Learner-scoped model, không phải Admin campaign. |
| V1-PILOT notification_deliveries | UUID notification_id, channel, status, provider/retry fields | Delivery-level append-only rows; khác ID/grain của Admin API. |
| Logical Notification lifecycle | draft, scheduled, cancelled/deleted, delivery started | Catalog/diagram không định nghĩa enum hoặc transition table; trạng thái chưa được xác nhận. |

## Tables write

AC-36 diagram yêu cầu logical DELETE/mark cancelled. Không có physical Admin notification model hoặc tombstone fields được chốt. Proposal dưới đây không phát sinh SQL, table hay column.

## Mục chú ý

- Catalog purpose nêu “Xóa draft/cancel nếu policy cho phép”; diagram node nói “DELETE/mark cancelled”. Không có nhánh state/status cụ thể.
- Reusable DeleteResult bắt buộc literal status "deleted", kể cả khi logical action là cancellation. Giữ schema trực tiếp; meaning của literal trong nhánh cancel cần owner xác nhận.
- Legacy notifications không có deletion/cancellation timestamp hoặc state. V1-PILOT timestamps/status thuộc UUID learner/delivery model, không thể dùng thay cho Admin BIGINT contract.
- Notification delivery rows trong V1-PILOT được mô tả là append-only. Không dùng DDL đó để update/delete delivery history cho API #95.
- #96 direct response là Notification và không có delivery aggregate collection/field. Không dựa vào contract #96 để xác định đã dispatch hay chưa.
- #93 Operation response/ID bridge và request không có action field vẫn là group gaps. #95 không tự tạo Operation ID hoặc action.
- Scheduler/queue cancellation API chưa được tìm thấy; không claim provider đã huỷ gửi.

## Assumptions

- DERIVED proposal: Draft chưa dispatch được gỡ khỏi active management bằng logical removal, giữ recipient/delivery history.
- DERIVED proposal: Scheduled chỉ được mark cancelled khi chưa delivery nào bắt đầu; nếu dispatch đã bắt đầu thì từ chối bằng 422 hiện có.
- DERIVED proposal: repeated request cho cùng tombstone trả lại cùng DeleteResult 200 để DELETE retry an toàn; cần owner xác nhận.
- DeleteResult.deleted_at được hiểu là thời điểm logical removal/cancellation được commit. Nguồn clock/column chưa được chọn.
- Không coi các proposal là implementation contract đã duyệt.

## Conflicts

| Source A | Source B | Conflict | Impact |
|---|---|---|---|
| Catalog #95 purpose | AC-36 DELETE node | Delete draft/cancel conditionally vs generic DELETE/mark cancelled | Eligibility/state policy unresolved. |
| DeleteResult | Scheduled cancellation outcome | Response literal says deleted while lifecycle action may be cancelled | Preserve direct shape; clarify semantic meaning. |
| Notification schema | Legacy notifications | No status, schedule or deletion timestamp | Cannot implement exact lifecycle from legacy row alone. |
| Admin campaign | V1-PILOT notification/delivery schema | UUID learner/delivery model and append-only delivery history | Do not conflate or mutate pilot tables by analogy. |
| API #96 | Delivery-start eligibility | Its response is Notification, without delivery aggregate fields | No cross-API proof of cancellation eligibility. |
| #93 operation notes | AC-36 Operation tracker and #18 IDs | Response type/operation ID bridge unresolved | #95 cannot name or cancel an assumed Operation. |
| AC permission | Current Study auth source | No verified Admin notification guard | Permission implementation is SOURCE_REQUIRED. |

## Security note

- Authenticate Bearer JWT and authorize Admin plus notification-management permission before resource lookup or mutation.
- Do not expose notification existence to unauthorized callers; exact authorization/404 precedence needs the shared Admin policy.
- Do not log or return recipient PII, provider details, queue IDs or SQL errors.
- Do not accept an actor ID or permission from request input.

## Performance note

- Eligibility should use bounded existence/status reads rather than loading recipient/delivery history, if the owner approves a physical model.
- Delivery-start aggregate/index/query is not defined; no performance or transaction claim is made.
- Scheduler cancellation timeout/retry behavior remains unknown.

## Contract interpretation

- DIRECT: DELETE/path/auth role/path type/no body or query/DeleteResult/HTTP 200/exact 401/403/404/422/500 codes; AC-36 permission and DELETE/mark cancelled/reload intent.
- DERIVED: draft removal, scheduled pre-dispatch cancellation, preserve history, existing 422 for disallowed state and idempotent repeated delete.
- SOURCE_REQUIRED: schema/tombstone/timestamp, enum/state values, delivery-start signal, Admin permission and scheduler protocol.
- DISCREPANCY: cancel action represented by DeleteResult.status="deleted"; API #96 does not expose delivery aggregate needed by the proposed guard.

## Tình trạng nhóm AC-36

AC-36 macro-review #92–#96 is complete at document level with open questions. #93 send/action/Operation, #94 draft/schedule, #95 delete/cancel policy and #96 aggregate projection remain unresolved. See [AC-36 macro-review](../96_admin_notifications_status/AC-36_MACRO_REVIEW.md).

## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Overview`
- Dimension: `A1:BA10`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `4`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | 【Khái quát】 |  |
| 3 | `B3` | Get thông tin…. |  |
| 5 | `A5` | 【Mục chú ý】 |  |
| 7 | `B7` | Không có |  |

</details>
