---
title: "Overview"
order: 2
dd_id: "63"
api_name: "Tạo và phát thông báo"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #63 |
| Module | MENTOR / TEACHING & SUPPORT — AC-25 |
| Method | `POST` |
| Endpoint | `/api/v1/mentor/notifications` |
| Purpose | Tạo thông báo cho nhóm học viên Mentor đã chọn và chấp nhận yêu cầu phát bất đồng bộ. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Role Mentor; mọi recipient phải cùng thuộc ít nhất một roster ACTIVE trong course do Mentor trực tiếp sở hữu. Đây là `DERIVED` vì direct body không có `course_id`. |
| Basis | Method/path/body/response/status/errors lấy trực tiếp từ catalog; AC-25 yêu cầu lưu Notification/recipients rồi dispatch Push/Email. CSV encoding, common-course scope, legacy outbox và Operation projection là fallback `DERIVED`. |
| Status | `Draft — Needs Confirmation` |
| Current runtime state | API #63 hiện được wired trong local source và HTTP tests; delivery worker/provider chưa có. |
| Transaction | Tạo các notification per-recipient và QUEUED delivery outbox rows trong một DB transaction; chỉ commit trước khi trả 202. |
| Side effects | Lưu Notification và từng channel delivery vào outbox; 202 xác nhận đã ghi nhận bền vững, không chứng minh Push/Email đã được gửi. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — #18, #62–#64, #93, Notification, NotificationDelivery, Operation và Payment.
- [AC/API index, AC-25](../../diagrams/AC_UNICA/00_AC_API_INDEX.md).
- [AC-25 activity diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — node/edge #62 → chọn recipient → #63 → ghi Notification + recipients → Push/Email → #64; node #18 đứng riêng, không có edge.
- [API #62 overview](../62_mentor_course_students/02_Overview.md) và [Open Questions #62](../62_mentor_course_students/OPEN_QUESTIONS.md) — roster trả BIGINT Student IDs; #63 nhận CSV các ID này theo fallback `DERIVED`.
- [API #64 catalog row](../../../../../docs/lists/list_api.md) — trạng thái delivery theo `notification_id:int64`.
- [API #18 overview](../18_operations/02_Overview.md) và [Open Questions #18](../18_operations/OPEN_QUESTIONS.md) — Định danh Operation, persistence và kiểu result chưa chốt.
- [API #43 overview](../43_users_me_notifications/02_Overview.md), [API #45 overview](../45_notifications_read_all/02_Overview.md) — Notification schema/read-state không đồng nhất với delivery status.
- [API #50 logical mapping precedent](../50_mentor_content_create/07_table.md) — ghi logical operation khi physical persistence chưa có bằng chứng.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) và [legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — mô hình notification BIGINT candidate; không có recipient table riêng.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — mô hình UUID learner/notification/delivery thay thế; không coi là live schema.
- [Study router](../../../app/api/v1.py), [middleware](../../../app/core/middleware.py), [API Guidelines](../../../../../contracts/api-guidelines/README.md).
- [Canonical DD Markdown template](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/) — tám sheet; fingerprint trong [PLAN_RESULT](./PLAN_RESULT.md).

## Tables/entities đọc

- `notifications` — legacy BIGINT per-recipient rows; migration 009 adds nullable `operation_id` to group one accepted request.
- `notification_deliveries` — local BIGINT outbox rows, one per notification/channel, initially `QUEUED`; worker/provider is not implemented.
- `NotificationRecipient` — represented by one legacy notification row per Student, not a separate association table.
- `Operation` — projected from the shared UUID `operation_id`, Mentor `sender_id`, initial kind/status and DB-created timestamp; enum values are `DERIVED`.

## Tables/entities ghi

- One `notifications` row per selected Student and one `notification_deliveries` outbox row per requested channel — local legacy-BIGINT fallback.
- Operation grouping and delivery rows are committed atomically; external delivery is deferred to a future worker.

## Mục chú ý

- Giữ nguyên body trực tiếp theo catalog: `recipients:string!`, `title:string!`, `content:int64!`, `channels:string!`.
- Giữ nguyên direct body types: `recipients:string!`, `title:string!`, `content:int64!`, `channels:string!`.
- `recipients` là CSV ordered positive int64 Student IDs; server collapse duplicate IDs and verifies the full set is ACTIVE in one directly owned course. Course inference is `DERIVED`; the request cannot bind to the exact UI-selected course.
- `channels` is CSV `PUSH` and/or `EMAIL`, derived from the AC-25 labels. `content:int64` is stored as base-10 text to fit legacy `notifications.content`; free-form text remains a contract discrepancy.
- `Operation.id` is a UUID shared by the new notification rows; response metadata contains `notification_ids:int64[]` for API #64. Operation kind/status are `NOTIFICATION_DISPATCH`/`QUEUED`, both `DERIVED`.
- 202 means notification and channel delivery records were committed to the local outbox. No worker/provider currently consumes those rows, so the API does not claim delivery.

## Đề xuất DERIVED cần xác nhận

| Chủ đề | Đề xuất tối giản | Cơ sở | Trạng thái |
|---|---|---|---|
| Course scope | Không thêm body field; yêu cầu toàn bộ recipient IDs cùng thuộc ít nhất một course Mentor sở hữu trực tiếp với ACTIVE enrollment. | Giữ exact catalog body và kiểm tra server-side access; course ID cụ thể không thể suy ra. | DERIVED; không bảo đảm chính là course UI đã chọn. |
| Recipients | CSV Student `users.id` positive int64, duplicates collapsed in first-seen order. | API #62 returns numeric Student IDs; legacy enrollments are BIGINT/ACTIVE. | DERIVED local encoding. |
| Content | Giữ int64 và lưu decimal string vào `notifications.content`. | Preserves catalog type and fits legacy TEXT; API #47 uses the same scalar-to-decimal-text pattern. | DERIVED; free-form notification text remains unresolved. |
| Channels | CSV `PUSH` and/or `EMAIL`, duplicates collapsed in first-seen order. | AC-25 names Push/Email; legacy BIGINT has no channel field. | DERIVED local tokens. |
| Durable acceptance | Persist notification rows and QUEUED delivery records in one transaction; do not claim worker delivery. | Diagram requires Notification + recipients before asynchronous provider work. | DERIVED local outbox migration; live schema/worker unverified. |
| Tracking bridge | Return Operation UUID in `data.id` and created per-recipient BIGINT IDs in `meta.notification_ids`. | Direct Operation shape and #64 int64 path both remain usable. | DERIVED metadata extension; API #64 implementation remains separate. |

## Conflicts

| Nguồn A | Nguồn B | Xung đột | Ảnh hưởng |
|---|---|---|---|
| Catalog #63 | AC-25 diagram + Notification schema | Request `content:int64`; entered Notification content is text. | Local fallback stores decimal text; semantic mismatch remains open for contract owner. |
| #62 → #63 | API #63 body | #62 selects a roster by course; #63 does not receive course ID. | Local fallback requires one common directly owned ACTIVE roster but cannot prove the exact UI-selected course. |
| #63 response | #64 path | #63 returns Operation UUID; #64 accepts notification_id:int64. | `meta.notification_ids` exposes each created row ID; #64 can be called per row. |
| Operation schema | Notification job | `Operation.result?:Payment`; not a notification result. | Omit optional result; use metadata for notification IDs. |
| AC-25 diagram | AC/API index | Diagram có node API #18 nhưng không nối; index liệt kê #18 cùng #62–#64. | Chưa rõ generic operation polling là nhánh bắt buộc hay song song với #64. |
| Legacy schema | V1-PILOT schema | Legacy có `notifications.user_id` BIGINT cho từng người nhận nhưng không có bảng recipients; pilot dùng UUID theo learner và bảng delivery, với channel `IN_APP` hoặc `EMAIL`. | Không ghép model hoặc khẳng định schema live. |
| Catalog #93 | Operation tracking summary | Admin create trả `Notification` ở row nhưng phần tổng quan nói trả `Operation`. | Không dùng Admin row để tự sửa Mentor contract. |
| API Guidelines | Current response helper | Current `error_response` emits `data:null`; #63 uses the shared helper and design-path classification. | No current discrepancy after wiring. |

## Security note

- Chỉ lấy sender identity từ Bearer principal, không nhận sender ID từ body.
- Không chấp nhận recipient chỉ vì client gửi ID; server đối chiếu role, ACTIVE enrollment và direct Mentor ownership trên ít nhất một common course.
- API chỉ ghi QUEUED outbox rows; không gửi thông tin đến provider trong request transaction.
- Không trả token, raw provider error, SQL, stack trace hoặc thông tin cá nhân không cần thiết.

## Performance/reliability note

- Fan-out có thể tăng theo số recipients × channels; catalog không có giới hạn batch. Giới hạn phải được bổ sung vào contract trước khi chọn một con số.
- 202 chỉ trả sau khi Notification và toàn bộ QUEUED outbox rows đã commit. Migration là source artifact; live database, worker, retry và provider delivery chưa được xác minh.
- Không kết luận retry count, backoff, partial-success status hoặc timeout khi chưa có nguồn được duyệt.
---
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
