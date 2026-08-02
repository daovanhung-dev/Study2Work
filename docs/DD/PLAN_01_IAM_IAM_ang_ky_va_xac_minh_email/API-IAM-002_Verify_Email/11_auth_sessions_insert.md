---
title: "auth_sessions_insert"
order: 11
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
---

# Định nghĩa table

<a id="db-map"></a>

## Table metadata

| Thuộc tính | Giá trị |
| --- | --- |
| Physical table | `auth_sessions` |
| Logical table | TBL-IAM-009 — Authentication sessions |
| Operation | `INSERT` |
| Data Mapping step | [05_Data_Mapping.md](./05_Data_Mapping.md#dm-3-6) |

## Update mapping

**Áp dụng khi**

- N/A — File này không mô tả UPDATE.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

## Insert mapping

**Áp dụng khi**

- Valid verification token after account activation.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | ID | `uuid` | - | - | Y | ● | `session_id` | Generated UUID v7 | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 2 | `created_at` | Created at | `timestamptz` | - | - | Y |  | `current_timestamp` | Generated | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 3 | `updated_at` | Updated at | `timestamptz` | - | - | Y |  | `current_timestamp` | Generated | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 4 | `row_version` | Row version | `bigint` | - | - | Y |  | `1` | DB default | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 5 | `user_id` | User ID | `uuid` | - | - | Y |  | `user_id` | Token subject | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 6 | `status` | Session status | `session_status` | - | - | Y |  | `ACTIVE` | DB default | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 7 | `session_epoch` | Session epoch | `bigint` | - | - | Y |  | `SOURCE_REQUIRED` | Missing authVersion/session epoch source | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 8 | `device_id_hash` | Device ID hash | `char` | 64 | - | N |  | `NULL` | No request field | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 9 | `device_name` | Device name | `varchar` | 120 | - | N |  | `NULL` | No request field | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 10 | `ip_hash` | IP hash | `char` | 64 | - | N |  | `ip_hash` | Request context | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 11 | `user_agent_hash` | User agent hash | `char` | 64 | - | N |  | `user_agent_hash` | Request context | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 12 | `last_seen_at` | Last seen at | `timestamptz` | - | - | Y |  | `current_timestamp` | Generated | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 13 | `expires_at` | Expires at | `timestamptz` | - | - | Y |  | `session_expires_at` | SOURCE_REQUIRED policy | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 14 | `revoked_at` | Revoked at | `timestamptz` | - | - | N |  | `NULL` | Active | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 15 | `revoke_reason` | Revoke reason | `varchar` | 100 | - | N |  | `NULL` | Active | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |

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
