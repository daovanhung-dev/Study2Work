---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "02 Overview"
format: markdown
dd_id: "45"
api_name: "Đánh dấu tất cả đã đọc"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 45 |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | `PATCH` |
| Endpoint | `/api/v1/notifications/read-all` |
| Purpose | Đánh dấu các notification chưa đọc thuộc Student hiện tại là đã đọc. |
| Consumer/Actor | `Student` |
| Authentication | Bearer `JWT` |
| Authorization | Role `Student`; principal lấy từ token, không nhận user ID từ request. |
| Basis | API catalog và nhánh ALL AC-20; cách lưu `is_read` và response Page là `DERIVED`. |
| Status | Draft — Needs Confirmation |
| Current runtime state | `UNWIRED / NOT_FOUND` — không có route/module/query/test API #45 trong Study source. |
| Transaction | Một bulk update atomic trong transaction do caller/use-case sở hữu — `DERIVED`. |
| Side effects | Chuyển read state của các direct-recipient notification đang unread; không gọi email/push/provider. |

## Sources

- [API catalog](../../../../../docs/lists/list_api.md) — API #43–#45, `Page<T>`, `Notification`, status và error contract.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, precondition, postcondition và API của AC-20.
- [AC-20 activity diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — ALL branch gọi API #45, bulk update và UI synchronization.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) — notification entities và design-only operations.
- [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — legacy `notifications` fields và user recipient/sender relation.
- [Legacy Study Server DDL](../../../../../infra/postgres/study-server/DB.sql) — BIGINT `user_id` và boolean `is_read`; live schema chưa xác minh.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID `learner_id`, `read_at`, delivery table; mô hình khác với API catalog/current Study principal.
- [Database context](../../../../../.agents/server-study/database.md) — schema artifacts không chứng minh live database.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — envelope, trace, error body và idempotency guideline.
- Current [Study router](../../../app/api/v1.py), [Student auth helper](../../../app/utils/auth.py) và [response helper](../../../app/core/responses.py) — current boundary; API #45 chưa wired.
- [API #43 list DD](../43_users_me_notifications/02_Overview.md), [API #44 mark-one DD](../44_notifications_mark_read/02_Overview.md), và [API #42 Page response precedent](../42_discussions_detail/04_Response.md).
- [Canonical DD Markdown template](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/) — tám sheet; fingerprint tại [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).

## Tables read

- `notifications` — candidate target rows and `RETURNING` projection in the legacy schema proposal.
- `NotificationRecipient` — logical per-recipient object in AC-20; no matching table in the legacy ERD/DDL.
- `notification_deliveries` — exists only in the alternative V1-PILOT DDL; not joined in this candidate because its UUID identity model does not align with this API contract.

## Tables write

- `notifications` — candidate update of `is_read` for unread rows owned by the authenticated Student.
- No write to `notification_deliveries` in this proposal.

## Mục chú ý

- Preserve the exact API catalog contract: empty `body{}`, `ApiEnvelope<Page<Notification>>`, 200 `DESIGN_RESOURCE_UPDATED`, and errors 401/403/422/500 only.
- AC-20 says “BULK UPDATE unread notifications”; candidate predicates are `user_id = principal_id` and `is_read = FALSE`.
- A zero-row update is a successful no-op — `DERIVED`; API #45 has no resource ID and no 404 error.
- Candidate response contains only rows changed by this call, returned in one `Page`; page metadata and unbounded result size are open design choices.
- `NotificationRecipient.read_at`, `channels`, `status`, and `scheduled_at` cannot be safely mapped from one schema model without resolving the DDL conflict.
- No `Idempotency-Key` is added because it is absent from the API catalog; assigning `is_read=TRUE` is state-idempotent.

## Assumptions

- `body{}` is proposed as an empty JSON object with no fields.
- Only direct-recipient rows with `notifications.user_id = principal_id` are eligible; nullable/broadcast rows are excluded.
- Only rows with `is_read = FALSE` are updated; a repeated call changes no additional rows.
- `data.items` returns every row transitioned by the statement; this means the response can grow with the Student's unread count.
- For this candidate Page, `page=1`, `size=updated_count`, `total=updated_count`, and `total_pages` is 0 when empty or 1 otherwise.
- Every assumption remains subject to the questions in [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

## Conflicts

- AC-20 requires per-recipient `read_at`; legacy ERD/DDL use nullable `user_id` and boolean `is_read` without a recipient table or read timestamp.
- `infra/postgres/02_study_db.sql` has `read_at`, `learner_id UUID`, and `notifications.id UUID`; current Study auth and catalog use numeric user/notification IDs.
- Required `Notification.channels` and `Notification.status` have no single approved source across the schema alternatives.
- API catalog uses `Page<Notification>` for mark-all but does not define whether it returns all changed rows, a bounded page, or an empty result.
- Catalog specifies `body{}` and 422 but does not state body requiredness or validation details.
- Error guideline uses `data: null`; current `error_response()` fallback emits `{}` when data is omitted.

## Security note

- The principal comes only from the Student Bearer JWT helper; no user identifier is accepted from body, path or query.
- Every candidate update includes the authenticated principal predicate.
- Do not update nullable/broadcast rows because the legacy model cannot record per-Student read state for them.
- Never return raw SQL, stack traces, token claims or database details.

## Performance note

- `UPDATE ... RETURNING` avoids a separate pre-update read and returns only rows that transitioned from unread to read.
- This candidate returns all affected rows without a limit because the endpoint has no pagination input; large response size needs confirmation.
- No index or schema change is proposed in this DD; live query plans were not inspected.
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
