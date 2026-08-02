---
title: "refresh_tokens_insert"
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
| Physical table | `refresh_tokens` |
| Logical table | TBL-IAM-010 — Refresh tokens |
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

- After auth session generated.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | ID | `uuid` | - | - | Y | ● | `refresh_token_id` | Generated UUID v7 | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 2 | `created_at` | Created at | `timestamptz` | - | - | Y |  | `current_timestamp` | Generated | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 3 | `session_id` | Session ID | `uuid` | - | - | Y |  | `session_id` | Generated session | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 4 | `family_id` | Token family ID | `uuid` | - | - | Y |  | `refresh_family_id` | Generated UUID v7 | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 5 | `parent_token_id` | Parent token ID | `uuid` | - | - | N |  | `NULL` | Initial token | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 6 | `token_hash` | Refresh token hash | `char` | 64 | - | Y |  | `refresh_token_hash` | Hash raw refresh token | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 7 | `status` | Token status | `token_status` | - | - | Y |  | `ACTIVE` | DB default | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 8 | `issued_at` | Issued at | `timestamptz` | - | - | Y |  | `current_timestamp` | Generated | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 9 | `expires_at` | Expires at | `timestamptz` | - | - | Y |  | `refresh_expires_at` | Max 30 days; exact SOURCE_REQUIRED | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 10 | `rotated_to_id` | Rotated child ID | `uuid` | - | - | N |  | `NULL` | No child yet | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 11 | `consumed_at` | Consumed at | `timestamptz` | - | - | N |  | `NULL` | Unused | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |
| 12 | `reuse_detected_at` | Reuse detected at | `timestamptz` | - | - | N |  | `NULL` | No reuse | [Data Mapping](./05_Data_Mapping.md#dm-3-6) |  |

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
