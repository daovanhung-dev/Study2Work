---
title: "Data Mapping"
order: 5
dd_id: "95"
api_name: "Admin xóa hoặc hủy notification"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

1. Nhận raw path/header; shared ADMIN guard chạy trước parse path và DB.
2. Parse `notification_id` là ASCII digits, số dương trong miền signed-int64; sai trả 422.
3. Khóa một row `notifications` theo path ID; thiếu row trả 404.
4. Khóa các `notification_deliveries` theo `channel ASC`, kiểm tra đúng notification ID, channel/status hợp lệ và không trùng channel.
5. Nếu không có delivery hoặc bất kỳ status nào khác `QUEUED`, rollback và trả 422 theo fallback `DERIVED`.
6. Xóa đúng parent row và lấy `id/deleted_at` bằng `DELETE ... RETURNING`; checked-in FK cascade xóa outbox row cùng transaction.
7. Validate DeleteResult/envelope rồi commit; query/mapping/commit error rollback và trả 500.
8. API không gọi scheduler/provider và không xóa notification rows khác có cùng `operation_id`.

### Mục lục

- [Step 0 — Authentication and permission](#step-0-authentication-and-permission)
- [Step 1 — Read request](#step-1-read-request)
- [Step 2 — Lock target and deliveries](#step-2-lock-target-and-deliveries)
- [Step 3 — Delete eligible notification](#step-3-delete-eligible-notification)
- [Step 4 — Scheduler boundary](#step-4-scheduler-boundary)
- [Step 5 — Map DeleteResult](#step-5-map-deleteresult)
- [Step 6 — Return result or error](#step-6-return-result-or-error)

<a id="step-0-authentication-and-permission"></a>
## Step 0 — Authentication and permission

- Direct auth: Bearer JWT; catalog role Admin.
- AC-36 requires notification-management permission, while local implementation uses the shared ADMIN guard only.
- Missing/invalid credentials map to 401; denied role maps to 403 before path validation/resource lookup.
- Fine-grained permission, claim mapping, tenant/global scope and dedicated-policy enforcement are SOURCE_REQUIRED.

<a id="step-1-read-request"></a>
## Step 1 — Read request

| Input | Direct source | Use | Validation/source boundary |
|---|---|---|---|
| notification_id | Path int64! | Identify exactly one notification row | Positive ASCII integer through signed-int64 max; invalid input maps to 422 as DERIVED. |
| Body | None | No action/reason/policy flag is accepted | N/A |
| Query | None | No selector or filter | N/A |
| Operation ID | None | No batch/job selector | Do not infer grouping from shared `operation_id`. |

<a id="step-2-lock-target-and-deliveries"></a>
## Step 2 — Lock target and deliveries

1. Query `notifications.id` by the bound path ID with `FOR UPDATE`; if absent, rollback and return 404.
2. Query and lock `notification_deliveries` for that exact ID, ordered by channel. Reject malformed identity/channel/status/duplicate-channel projections as safe 500.
3. Require at least one delivery and every status to be `QUEUED`; otherwise rollback and return 422 `DESIGN_VALIDATION_ERROR`.
4. This is `DERIVED` from #93 creating one or more queued rows and #94's queued-only edit gate. Catalog/diagram do not define the trigger; current outbox status does not prove external provider state.
5. Lock order follows API #94's parent-before-delivery sequence. PostgreSQL concurrency and any worker order are not exercised by fake-DB tests.

### Query matrix

| Query ID | Purpose | Physical source/columns | Predicate | Status |
|---|---|---|---|---|
| Q1 | Lock parent | `notifications.id` | `id = :notification_id FOR UPDATE` | Current local legacy candidate; live schema unverified. |
| Q2 | Lock/read deliveries | `notification_deliveries.notification_id, channel, status` | Exact parent id; `ORDER BY channel ASC FOR UPDATE` | Migration 009 candidate; live schema/worker unverified. |
| Q3 | Delete parent and obtain response fields | `notifications.id` | Exact parent id; `RETURNING id, CURRENT_TIMESTAMP AS deleted_at` | Local SQL; relies on checked-in DDL candidate. |
| Q4 | Remove child outbox rows | FK cascade | Parent `notifications` row is deleted | Direct checked-in DDL behavior; not live-DB verified. |

<a id="step-3-delete-eligible-notification"></a>
## Step 3 — Delete eligible notification

### Local fallback — one recipient row and its queued outbox rows

- Delete exactly the `notifications` row selected by `notification_id`.
- Migration 009 and `DB.sql` define `notification_deliveries.notification_id` with `ON DELETE CASCADE`; candidate DB behavior removes that parent's delivery rows in the same transaction.
- The returned database `CURRENT_TIMESTAMP` maps to required `DeleteResult.deleted_at`. No tombstone or deletion column is written.
- `operation_id` can be shared across recipient rows. #95 does not fan out by that field and leaves siblings untouched.
- All effects and eligibility rules in this subsection are local `DERIVED` behavior over the current #93/#94 candidate model, not an approved retention policy.

### Mutation matrix

| ID | Operation | Condition | Fields/effect | Transaction/failure | Status |
|---|---|---|---|---|---|
| M1 | DELETE parent | At least one locked delivery, all QUEUED | Delete one `notifications` row; FK cascades its delivery rows; return id/time | Validate full response before commit; rollback on query/mapping/commit error | DERIVED local fallback |
| M2 | Reject eligibility | No delivery or any delivery status SENT/FAILED | No mutation | Rollback; return catalog 422 | DERIVED local fallback |
| M3 | Repeated request | Parent already deleted | No row to lock | Return catalog 404 | DERIVED consequence; no idempotency contract |

<a id="step-4-scheduler-boundary"></a>
## Step 4 — Scheduler boundary

- AC-36 requires a delete/cancel action but no queue, worker, provider or scheduler API is present in current Study source.
- The local transaction removes queued outbox rows under the checked-in FK candidate. It does not call an external scheduler/provider or prove an in-flight send was stopped.
- Worker polling/claim locking, dispatch race, scheduler acknowledgement, Operation ID and retry policy are SOURCE_REQUIRED. Do not report external cancellation as verified.
- See [08_notification_delivery_cancel.md](./08_notification_delivery_cancel.md).

<a id="step-5-map-deleteresult"></a>
## Step 5 — Map DeleteResult

| Response field | Logical source | Mapping rule | Status |
|---|---|---|---|
| id | DELETE RETURNING | Preserve the path-selected parent ID; validate positive signed-int64 | DIRECT type; local legacy mapping DERIVED |
| status | DeleteResult schema | Always literal `deleted` | DIRECT |
| deleted_at | DELETE RETURNING | Database `CURRENT_TIMESTAMP` from the delete statement | DIRECT field; local clock mapping DERIVED; not persisted |
| businessCode | Catalog | `DESIGN_RESOURCE_DELETED` | DIRECT |
| traceId | Request context | Propagate shared trace convention | Shared convention |

- Do not serialize NotificationStatus or an Operation ID in DeleteResult.
- If no tombstone exists after success, a repeated DELETE returns 404.

<a id="step-6-return-result-or-error"></a>
## Step 6 — Return result or error

- Direct success: HTTP 200 `DESIGN_RESOURCE_DELETED`, `ApiEnvelope<DeleteResult>`.
- Exact direct errors: 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`.
- Local 422 triggers are invalid path or no/started delivery; these are DERIVED, not catalog policy.
- Do not add 409, 410 or 503 for scheduler assumptions.
- Do not return recipient PII, provider errors, delivery IDs, SQL or stack traces.

## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `3. Data mapping`
- Dimension: `B1:BB61`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `63`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Flow xử lý data |  |
| 4 | `D4` | 0. |  |
| 4 | `E4` | Check quyền |  |
| 5 | `E5` | ・ |  |
| 5 | `F5` | Thực hiện check quyền |  |
| 6 | `E6` | ・ |  |
| 6 | `F6` | Get count khi get data từ … |  |
| 7 | `G7` | Table get |  |
| 7 | `K7` | : |  |
| 8 | `G8` | Conditions |  |
| 8 | `K8` | : |  |
| 10 | `E10` | ・ |  |
| 10 | `F10` | Trường hợp giá trị get được lớn hơn 0, thực hiện các xử lý tiếp theo |  |
| 11 | `E11` | ・ |  |
| 11 | `F11` | Trường hợp giá trị get được bằng 0, trả về status 2 |  |
| 13 | `D13` | 1. |  |
| 13 | `E13` | validate data input |  |
| 14 | `F14` | refer sheet [４．Error] |  |
| 16 | `D16` | 2. |  |
| 16 | `E16` | Get thông tin… |  |
| 18 | `F18` | Table get |  |
| 18 | `K18` | Column get |  |
| 18 | `P18` | Chú thích |  |
| 18 | `U18` | Remarks |  |
| 29 | `F29` | Target table / join condition |  |
| 30 | `F30` | Target table |  |
| 30 | `N30` | Join condition |  |
| 30 | `AL30` | 結合種類 |  |
| 31 | `F31` | txn_ams_t0320 AS a |  |
| 32 | `F32` | txn_amm_v0002 AS b |  |
| 32 | `N32` | ON a . chy_typ = b . kbn_typ AND b . dmin_cd = A AND b . kbnknr_cd = 001 |  |
| 32 | `AL32` | LEFT JOIN |  |
| 33 | `F33` | txn_amm_v0002 AS c |  |
| 33 | `N33` | ON a . chy_typ = c . kbn_typ AND c . dmin_cd = A AND c . kbnknr_cd = Z02 |  |
| 33 | `AL33` | LEFT JOIN |  |
| 35 | `F35` | ・ |  |
| 35 | `G35` | Điều kiện get data |  |
| 37 | `F37` | ・ |  |
| 37 | `G37` | Điều kiện sort |  |
| 41 | `D41` | 3. |  |
| 41 | `E41` | Insert/Update thông tin … |  |
| 42 | `E42` | Update table…. |  |
| 43 | `E43` | ・ |  |
| 43 | `F43` | Items update |  |
| 44 | `F44` | ・ |  |
| 44 | `G44` | Refer sheet [xxxx] |  |
| 45 | `E45` | ・ |  |
| 45 | `F45` | Điều kiện get data |  |
| 46 | `F46` | ・ |  |
| 46 | `G46` | auth_user. id = user hiện tại theo token |  |
| 48 | `D48` | 4. |  |
| 48 | `E48` | check kết quả execute query  |  |
| 49 | `E49` | 1. Thành công |  |
| 50 | `F50` | HTTPStatus = 200 |  |
| 51 | `F51` | Trả về kết quả status = 1 |  |
| 52 | `E52` | 2. Lỗi hệ thống phát sinh |  |
| 53 | `F53` | HTTPStatus = 500 |  |
| 54 | `F54` | Trả về kết quả status = 2 |  |
| 55 | `E55` | 3. Validate lỗi |  |
| 56 | `F56` | HTTPStatus = 400 |  |
| 57 | `F57` | Trả về kết quả status = 2 |  |
| 58 | `E58` | 4. Ngoài trường hợp trên |  |
| 59 | `F59` | Trả về kết quả status = 2 |  |

</details>
