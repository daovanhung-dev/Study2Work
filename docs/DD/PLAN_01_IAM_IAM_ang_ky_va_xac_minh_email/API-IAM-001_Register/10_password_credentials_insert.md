---
title: "password_credentials_insert"
order: 10
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
---

# Định nghĩa table

<a id="db-map"></a>

## Table metadata

| Thuộc tính | Giá trị |
| --- | --- |
| Physical table | `password_credentials` |
| Logical table | TBL-IAM-003 — Password credentials |
| Operation | `INSERT` |
| Data Mapping step | [05_Data_Mapping.md](./05_Data_Mapping.md#dm-3-5) |

## Update mapping

**Áp dụng khi**

- N/A — File này không mô tả UPDATE.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

## Insert mapping

**Áp dụng khi**

- New normalized email branch.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | ID | `uuid` | - | - | Y | ● | `credential_id` | Generated UUID v7 | [Data Mapping](./05_Data_Mapping.md#dm-3-5) |  |
| 2 | `created_at` | Created at | `timestamptz` | - | - | Y |  | `current_timestamp` | Generated | [Data Mapping](./05_Data_Mapping.md#dm-3-5) |  |
| 3 | `updated_at` | Updated at | `timestamptz` | - | - | Y |  | `current_timestamp` | Generated | [Data Mapping](./05_Data_Mapping.md#dm-3-5) |  |
| 4 | `row_version` | Row version | `bigint` | - | - | Y |  | `1` | DB default | [Data Mapping](./05_Data_Mapping.md#dm-3-5) |  |
| 5 | `user_id` | User ID | `uuid` | - | - | Y |  | `user_id` | Generated parent ID | [Data Mapping](./05_Data_Mapping.md#dm-3-5) |  |
| 6 | `password_hash` | Password hash | `varchar` | 512 | - | Y |  | `password_hash` | Argon2id output | [Data Mapping](./05_Data_Mapping.md#dm-3-5) |  |
| 7 | `algorithm` | Hash algorithm | `varchar` | 32 | - | Y |  | `ARGON2ID` | DB default | [Data Mapping](./05_Data_Mapping.md#dm-3-5) |  |
| 8 | `parameters` | Argon2 parameters | `jsonb` | - | - | Y |  | `argon2_parameters` | SOURCE_REQUIRED config | [Data Mapping](./05_Data_Mapping.md#dm-3-5) |  |
| 9 | `changed_at` | Password changed at | `timestamptz` | - | - | Y |  | `current_timestamp` | Generated | [Data Mapping](./05_Data_Mapping.md#dm-3-5) |  |
| 10 | `must_change` | Must change password | `boolean` | - | - | Y |  | `false` | DB default | [Data Mapping](./05_Data_Mapping.md#dm-3-5) |  |
| 11 | `failed_count` | Failed login count | `integer` | - | - | Y |  | `0` | DB default | [Data Mapping](./05_Data_Mapping.md#dm-3-5) |  |
| 12 | `locked_until` | Locked until | `timestamptz` | - | - | N |  | `NULL` | Not locked | [Data Mapping](./05_Data_Mapping.md#dm-3-5) |  |

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
