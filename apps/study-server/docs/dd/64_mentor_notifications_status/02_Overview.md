---
title: "Overview"
order: 2
dd_id: "64"
api_name: "Theo dõi trạng thái gửi"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---


# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #64 |
| Module | MENTOR / TEACHING & SUPPORT — AC-25 |
| Method | `GET` |
| Endpoint | `/api/v1/mentor/notifications/{notification_id}/status` |
| Purpose | Đọc trạng thái dispatch đã lưu của một notification để UI hiển thị sau API #63. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Role Mentor trực tiếp từ catalog; quyền theo notification được suy ra từ `notifications.sender_id` và giữ nhãn DERIVED. |
| Basis | Method/path/response/status/errors DIRECT từ catalog; đọc delivery state DIRECT từ AC-25; legacy outbox/owner/status mapping DERIVED từ implementation #63. |
| Status | `Draft — Needs Confirmation` |
| Current runtime state | Route/module/query/test của API #64 đã wired trong local source; fake-session HTTP tests pass. Live schema, migration 009 và worker/provider delivery chưa được xác minh. |
| Transaction | N/A — read-only; caller DB session không được commit. |
| Side effects | Không mutation hoặc provider call; chỉ đọc notification/outbox đã lưu. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — #18, #63–#64, `ApiEnvelope`, `Operation`, `NotificationDelivery`.
- [AC/API index, AC-25](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) và [AC-25 diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — #63 acceptance/outbox → Push/Email → #64 status read; #18 không có edge trong flow.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) và [migration 009](../../../../../infra/postgres/study-server/migrations/009_notification_delivery_outbox.sql) — local BIGINT notification/outbox source; chưa chứng minh live deployment.
- [API #63 source](../../../app/modules/mentor/api_63_mentor_notifications_create/query.py) — writes `operation_id`, `sender_id`, `created_at`, and `QUEUED` per-channel rows atomically.
- [API #63 DD](../63_mentor_notifications_create/02_Overview.md), [response](../63_mentor_notifications_create/04_Response.md), and [open questions](../63_mentor_notifications_create/OPEN_QUESTIONS.md) — `meta.notification_ids` is the current local handoff; Operation UUID remains separate.
- [API #18 Operation overview](../18_operations/02_Overview.md) — generic job tracking remains a separate contract with unresolved identity/lifecycle.
- [API #43 list](../43_users_me_notifications/02_Overview.md) and [API #45 read-all](../45_notifications_read_all/02_Overview.md) — read state is not delivery state.
- Current [Study router](../../../app/api/v1.py), [middleware](../../../app/core/middleware.py), [auth helper](../../../app/utils/auth.py), and [response helper](../../../app/core/responses.py) — runtime/auth/error boundaries.
- [Canonical DD Markdown templates](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/) — eight-sheet template fingerprints are recorded in [PLAN_RESULT](./PLAN_RESULT.md).

## Tables/entities đọc

- `notifications` — API #63's local BIGINT rows; key, Operation UUID, sending Mentor and submission timestamp.
- `notification_deliveries` — API #63's local per-notification/channel outbox rows and persisted delivery state.
- `Operation` — logical response type; reconstructed from the same API #63 rows because Study has no Operation table.

## Tables/entities ghi

N/A — READ-ONLY API. No notification, delivery or Operation row is changed.

## Mục chú ý

- Preserve direct contract: path `notification_id:int64!`, `ApiEnvelope<Operation>`, HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, and only 401/403/404/500 errors.
- AC-25 describes delivery status while the catalog returns Operation. Keep the direct response type; map its `status` from persisted per-channel states as a local DERIVED fallback.
- API #63 currently exposes notification IDs in `meta.notification_ids`; `data.id` remains its separate Operation UUID.
- Mentor access uses the same local `notifications.sender_id` written from JWT `sub` by API #63; another sender receives 403.
- For multiple channels, any queued row keeps aggregate status `QUEUED`; with no queued row, any failed row yields `FAILED`; otherwise all rows must be `SENT`.
- Partial success is summarized as `FAILED`; the direct Operation response has no delivery count fields, so counts are not added to `data` or `meta`.
- Do not use `notifications.is_read` or call Push/Email from this GET.

## Assumptions

- `Operation.id` is `notifications.operation_id`, generated and grouped by API #63.
- `Operation.kind` is `NOTIFICATION_DISPATCH`, matching API #63's accepted response.
- `Operation.owner_id` is `notifications.sender_id`.
- `Operation.submitted_at` is `notifications.created_at`.
- `Operation.updated_at` is the latest `notification_deliveries.updated_at` for this notification.
- `Operation.status` reuses local outbox values `QUEUED`, `SENT`, or `FAILED`; enum values remain DERIVED because catalog members are not listed.
- `completed_at` and optional Payment `result` are omitted because no Study persistence/semantics support them.
- A notification without `operation_id` or delivery rows has no API #63 dispatch status and returns 404; this is a local resource boundary.
- All assumptions remain `Draft — Needs Confirmation`; checked-in DDL and fake DB tests do not verify live database state.

## Conflicts

| Source A | Source B | Conflict | Local resolution/status |
|---|---|---|---|
| Catalog #64 | AC-25 delivery flow | Response type is Operation while the use case is delivery status. | Keep direct `ApiEnvelope<Operation>` and derive Operation.status from outbox; no new response field. |
| Catalog `Operation` | API #63 local source | Operation persistence/lifecycle is absent, but #63 stores UUID, sender and timestamps on notification rows. | Reconstruct Operation from API #63 rows; DERIVED local mapping. |
| Reusable OperationStatus | Migration 009 outbox | OperationStatus members are unspecified; delivery states are constrained to QUEUED/SENT/FAILED. | Reuse the three checked-in local states for Operation.status; DERIVED, not enum approval. |
| API #64 path | API #63 response | Operation UUID is not the notification int64 path key. | Consume API #63 `meta.notification_ids`; keep both IDs separate. |
| Legacy notifications | API #64 status lookup | Old notification rows may have no Operation/outbox. | Return 404 for no dispatch status resource; do not infer state from `is_read`. |
| Checked-in SQL | Live DB | DDL/migration do not prove deployment. | Local source/test only; live metadata remains unverified. |

## Security note

- Authenticate Bearer and require MENTOR before parsing or querying.
- Derive principal only from JWT; never accept sender ID from path/query.
- Compare the notification sender to the authenticated numeric subject before returning Operation data.
- Do not expose provider IDs/errors, SQL, stack traces or token claims.

## Reliability note

- Read only persisted status; no synchronous provider call, resending or mutation.
- API #63 commits the outbox before returning 202. With no worker wired in this Study source, local accepted rows remain `QUEUED` until an external actor changes them.
- Polling cadence, retry semantics, delivery SLA, enum approval and live migration state remain outside local verification.

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
