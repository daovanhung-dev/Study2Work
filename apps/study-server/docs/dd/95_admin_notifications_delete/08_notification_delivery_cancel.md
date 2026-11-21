---
title: "Delivery cancellation mapping"
order: 8
dd_id: "95"
api_name: "Admin xóa hoặc hủy notification"
source_sheet: "3. Data mapping — supplementary scheduler boundary"
status: "Draft — Needs Confirmation"
---

# Scheduled delivery cancellation — logical boundary

## Mapping metadata

| Thuộc tính | Giá trị |
|---|---|
| Logical operation | AC-36 says delete/mark cancelled; local API #95 deletes one legacy recipient row |
| Trigger | Catalog #95 says draft delete/cancel when policy allows |
| Candidate local outbox | `notification_deliveries` rows created by #93 |
| External scheduler/queue | None found in current Study/Admin source |
| Status | Local QUEUED-only gate and FK cascade are DERIVED; external cancellation SOURCE_REQUIRED |

## Eligibility and effect

| Item | Local behavior | Basis/status |
|---|---|---|
| Target grain | Delete only `notifications.id = notification_id` | Current #93 writes one row per recipient; DERIVED mapping |
| Delivery rows | Require at least one; lock them and require every status to be QUEUED | #93 creates per-channel QUEUED rows and #94 uses same gate; DERIVED policy |
| Parent/outbox effect | Delete parent; checked-in `ON DELETE CASCADE` removes its child delivery rows | DDL candidate, not live-verified |
| No delivery / SENT / FAILED | Return existing catalog 422; do not DELETE | DERIVED eligibility fallback |
| Pending external job | No scheduler call is made or inferred | SOURCE_REQUIRED; no worker contract found |
| In-flight provider call | Local success is not proof the call stopped | Provider semantics unknown |
| Batch siblings | Leave other recipient rows sharing `operation_id` untouched | Path identifies one row; no batch input contract |
| Repeat DELETE | Return 404 after parent removal | Physical row is absent; no tombstone/idempotency contract |
| Response timestamp | Return database `CURRENT_TIMESTAMP` from DELETE RETURNING | DeleteResult field direct; local mapping DERIVED |

## Candidate evidence

| Source | Evidence | Limit |
|---|---|---|
| AC-36 diagram | API #95 → `DELETE/mark cancelled` → reload management | Does not identify scheduler, job ID, delivery-start signal or transaction. |
| Catalog API #96 | GET status returns `ApiEnvelope<Notification>` | No delivery aggregate in direct response; #95 reads its local outbox candidate. |
| #93/#94 runtime | #93 writes `QUEUED` outbox rows; #94 locks parent then deliveries | Local behavior only; fake-DB tests do not establish live PostgreSQL/worker behavior. |
| Migration 009 | Delivery FK uses `ON DELETE CASCADE`, statuses include QUEUED/SENT/FAILED | Checked-in migration is not proof it is deployed. |
| V1-PILOT delivery model | Separate UUID learner delivery data | Not used by #95 and does not establish Admin scheduler behavior. |

API #95 does not call a provider, queue, scheduler or Operation endpoint. A successful 200 confirms only the local transaction result under the checked-in candidate model; it does not assert external delivery cancellation or retained audit history.

## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `table`
- Dimension: `A1:BA35`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `19`
- Số vùng merge: `5`

<details>
<summary>Danh sách vùng merge</summary>

- `W34:BA34`
- `W14:BA14`
- `W15:BA15`
- `W19:BA19`
- `W32:BA32`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `A2` | № |  |
| 2 | `B2` | Tên table |  |
| 3 | `B3` | SB |  |
| 3 | `S3` | Độ dài |  |
| 3 | `T3` | Dấu phẩy thập phân |  |
| 3 | `U3` | Bắt buộc |  |
| 3 | `V3` | Main key |  |
| 3 | `W3` | Nội dung setting |  |
| 4 | `B4` | № |  |
| 4 | `C4` | Item ID |  |
| 4 | `I4` | Item name |  |
| 4 | `O4` | Kiểu |  |
| 5 | `A5` | 1 |  |
| 5 | `B5` | table id |  |
| 5 | `I5` | table name |  |
| 6 | `B6` | Update |  |
| 6 | `I6` | Trường hợp số record get được từ xử lý 3. của sheet [３．Data mapping]  > 0 |  |
| 21 | `B21` | Insert |  |
| 21 | `I21` | Trường hợp số record get được từ xử lý 3. của sheet [３．Data mapping]  = 0 |  |

</details>
