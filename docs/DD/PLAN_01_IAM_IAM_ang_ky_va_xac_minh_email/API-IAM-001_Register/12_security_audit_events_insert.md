---
title: "security_audit_events_insert"
order: 12
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
---

# Định nghĩa table

<a id="db-map"></a>

## Table metadata

| Thuộc tính | Giá trị |
| --- | --- |
| Physical table | `security_audit_events` |
| Logical table | TBL-IAM-017 — Security audit events |
| Operation | `INSERT` |
| Data Mapping step | [05_Data_Mapping.md](./05_Data_Mapping.md#dm-3-8) |

## Update mapping

**Áp dụng khi**

- N/A — File này không mô tả UPDATE.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

## Insert mapping

**Áp dụng khi**

- Registration success or duplicate attempt.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | ID | `uuid` | - | - | Y | ● | `audit_event_id` | Generated UUID v7 | [Data Mapping](./05_Data_Mapping.md#dm-3-8) |  |
| 2 | `occurred_at` | Occurred at | `timestamptz` | - | - | Y |  | `current_timestamp` | DB default | [Data Mapping](./05_Data_Mapping.md#dm-3-8) |  |
| 3 | `actor_id` | Actor ID | `uuid` | - | - | N |  | `NULL` | Anonymous | [Data Mapping](./05_Data_Mapping.md#dm-3-8) |  |
| 4 | `subject_id` | Subject ID | `uuid` | - | - | N |  | `user_id` for new; existing subject policy SOURCE_REQUIRED | Derived/context | [Data Mapping](./05_Data_Mapping.md#dm-3-8) |  |
| 5 | `action` | Action | `varchar` | 120 | - | Y |  | `identity.register` — DERIVED working action | SOURCE_REQUIRED audit catalog | [Data Mapping](./05_Data_Mapping.md#dm-3-8) |  |
| 6 | `outcome` | Audit outcome | `audit_outcome` | - | - | Y |  | `SUCCESS` or `DENIED` | Branch | [Data Mapping](./05_Data_Mapping.md#dm-3-8) |  |
| 7 | `reason_code` | Reason code | `varchar` | 80 | - | N |  | `NULL` or redacted duplicate reason | Branch | [Data Mapping](./05_Data_Mapping.md#dm-3-8) |  |
| 8 | `trace_id` | Trace ID | `varchar` | 64 | - | Y |  | `trace_id` | Request context | [Data Mapping](./05_Data_Mapping.md#dm-3-8) |  |
| 9 | `session_id` | Session ID | `uuid` | - | - | N |  | `NULL` | Anonymous | [Data Mapping](./05_Data_Mapping.md#dm-3-8) |  |
| 10 | `ip_hash` | IP hash | `char` | 64 | - | N |  | `request_ip_hash` | Request context | [Data Mapping](./05_Data_Mapping.md#dm-3-8) |  |
| 11 | `user_agent_hash` | User agent hash | `char` | 64 | - | N |  | `user_agent_hash` | Request context | [Data Mapping](./05_Data_Mapping.md#dm-3-8) |  |
| 12 | `metadata` | Redacted metadata | `jsonb` | - | - | Y |  | Redacted allowlisted JSON | Generated | [Data Mapping](./05_Data_Mapping.md#dm-3-8) |  |
| 13 | `prev_hash` | Previous event hash | `char` | 64 | - | N |  | Previous chain hash | SOURCE_REQUIRED procedure | [Data Mapping](./05_Data_Mapping.md#dm-3-8) |  |
| 14 | `event_hash` | Event hash | `char` | 64 | - | Y |  | Canonical event hash | SOURCE_REQUIRED procedure | [Data Mapping](./05_Data_Mapping.md#dm-3-8) |  |
| 15 | `legal_hold_until` | Legal hold until | `timestamptz` | - | - | N |  | `NULL` | Default unless legal hold | [Data Mapping](./05_Data_Mapping.md#dm-3-8) |  |

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
