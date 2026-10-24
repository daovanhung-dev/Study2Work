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
| Logical operation | Cancel scheduled notification delivery |
| Trigger | AC-36 DELETE/mark cancelled; catalog policy is conditional |
| Candidate scheduler/queue | None found in current Study/Admin source |
| Physical delivery target | No approved Admin relation |
| Status | DERIVED logical intent; external/persistence contract SOURCE_REQUIRED |

## Eligibility and effect proposal

| Item | Proposed rule/effect | Basis/status |
|---|---|---|
| Scheduled target | Permit cancel only before any delivery starts | DERIVED; policy says cancel if allowed, no state model |
| Dispatch started | Reject using existing 422 code | DERIVED; trigger requires owner approval |
| Pending job | Mark target cancelled and prevent later dispatch | DERIVED intent; no worker/scheduler source |
| In-flight provider call | Do not claim cancellation succeeded | SOURCE_REQUIRED; provider semantics unknown |
| Delivery history | Preserve prior attempts and provider results | Conservative DERIVED proposal; no Admin table selected |
| Scheduler acknowledgement | Not represented in DeleteResult | SOURCE_REQUIRED; no operation/job ID contract |
| Repeat DELETE | Return stable original DeleteResult if tombstone remains | DERIVED idempotency proposal |

## Candidate evidence

| Source | Evidence | Why it is not a direct Admin mapping |
|---|---|---|
| AC-36 diagram | API #95 → DELETE/mark cancelled → reload management | Does not identify scheduler, job ID, delivery-start signal or transaction |
| Catalog API #96 | GET status returns ApiEnvelope<Notification> | Notification response has no delivery aggregate schema |
| V1-PILOT notification_deliveries | UUID notification_id, channel/status/retry fields; append-only | Learner/delivery grain differs from Admin BIGINT contract |
| Catalog Operation tracking | Operation schema/summary exists | #93 response and Operation ID mapping are inconsistent; #95 has no Operation input/output |

No physical table, queue API, Operation ID, SQL or provider call is inferred.

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
