---
title: "outbox_events_insert"
order: 13
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
---

# Định nghĩa table

<a id="db-map"></a>

## Table metadata

| Thuộc tính | Giá trị |
| --- | --- |
| Physical table | `outbox_events` |
| Logical table | TBL-IAM-018 — Identity outbox events |
| Operation | `INSERT` |
| Data Mapping step | [05_Data_Mapping.md](./05_Data_Mapping.md#dm-3-7) |

## Update mapping

**Áp dụng khi**

- N/A — File này không mô tả UPDATE.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

## Insert mapping

**Áp dụng khi**

- Account activation succeeds.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | ID | `uuid` | - | - | Y | ● | `UUID_V7()` | Generated | [Data Mapping](./05_Data_Mapping.md#dm-3-7) |  |
| 2 | `created_at` | Created at | `timestamptz` | - | - | Y |  | `current_timestamp` | DB default | [Data Mapping](./05_Data_Mapping.md#dm-3-7) |  |
| 3 | `aggregate_type` | Aggregate type | `varchar` | 80 | - | Y |  | `USER` — DERIVED | SOURCE_REQUIRED convention | [Data Mapping](./05_Data_Mapping.md#dm-3-7) |  |
| 4 | `aggregate_id` | Aggregate ID | `uuid` | - | - | Y |  | `user_id` | Token subject | [Data Mapping](./05_Data_Mapping.md#dm-3-7) |  |
| 5 | `event_type` | Event type | `varchar` | 120 | - | Y |  | `identity.user.verified.v1` | EVT-IAM-001 | [Data Mapping](./05_Data_Mapping.md#dm-3-7) |  |
| 6 | `event_version` | Event version | `integer` | - | - | Y |  | `1` | Event catalog | [Data Mapping](./05_Data_Mapping.md#dm-3-7) |  |
| 7 | `payload` | Event payload | `jsonb` | - | - | Y |  | `{subject, sourceVersion, verifiedAt}` | EVT-IAM-001 minimum payload | [Data Mapping](./05_Data_Mapping.md#dm-3-7) |  |
| 8 | `available_at` | Available at | `timestamptz` | - | - | Y |  | `current_timestamp` | DB default | [Data Mapping](./05_Data_Mapping.md#dm-3-7) |  |
| 9 | `dedupe_key` | Dedupe key | `varchar` | 180 | - | Y |  | `identity.user.verified:{user_id}:{sourceVersion}` — DERIVED | SOURCE_REQUIRED convention | [Data Mapping](./05_Data_Mapping.md#dm-3-7) |  |
| 10 | `trace_id` | Trace ID | `varchar` | 64 | - | Y |  | `trace_id` | Request context | [Data Mapping](./05_Data_Mapping.md#dm-3-7) |  |

## Delete mapping

**Áp dụng khi**

- N/A — File này không mô tả DELETE.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
| ---: | --- | --- | --- | --- | --- |
| N/A | N/A | N/A | N/A | N/A | N/A |
---
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
