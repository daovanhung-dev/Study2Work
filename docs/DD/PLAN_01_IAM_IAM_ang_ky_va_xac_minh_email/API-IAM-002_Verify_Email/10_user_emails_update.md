---
title: "user_emails_update"
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
| Physical table | `user_emails` |
| Logical table | TBL-IAM-002 — User emails |
| Operation | `UPDATE` |
| Data Mapping step | [05_Data_Mapping.md](./05_Data_Mapping.md#dm-3-4) |

## Update mapping

**Áp dụng khi**

- user_emails.id = token.email_id AND user_id = token.user_id.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | ID | `uuid` | - | - | Y | ● | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 2 | `created_at` | Created at | `timestamptz` | - | - | Y |  | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 3 | `updated_at` | Updated at | `timestamptz` | - | - | Y |  | `current_timestamp` | Generated | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 4 | `row_version` | Row version | `bigint` | - | - | Y |  | `row_version + 1` | ENTITY rule | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 5 | `user_id` | User ID | `uuid` | - | - | Y |  | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 6 | `email_ciphertext` | Encrypted email | `bytea` | - | - | Y |  | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 7 | `email_normalized` | Normalized email | `varchar` | 320 | - | Y |  | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 8 | `is_primary` | Primary email flag | `boolean` | - | - | Y |  | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 9 | `verified_at` | Verified at | `timestamptz` | - | - | N |  | `current_timestamp` | Generated | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 10 | `replaced_at` | Replaced at | `timestamptz` | - | - | N |  | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |

## Insert mapping

**Áp dụng khi**

- N/A — File này không mô tả INSERT.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

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
