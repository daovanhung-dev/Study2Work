---
title: "email_verification_tokens_insert"
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
| Physical table | `email_verification_tokens` |
| Logical table | TBL-IAM-004 — Email verification tokens |
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

- New normalized email branch.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | ID | `uuid` | - | - | Y | ● | `verification_token_id` | Generated UUID v7 | [Data Mapping](./05_Data_Mapping.md#dm-3-7) |  |
| 2 | `created_at` | Created at | `timestamptz` | - | - | Y |  | `current_timestamp` | Generated | [Data Mapping](./05_Data_Mapping.md#dm-3-7) |  |
| 3 | `user_id` | User ID | `uuid` | - | - | Y |  | `user_id` | Generated parent ID | [Data Mapping](./05_Data_Mapping.md#dm-3-7) |  |
| 4 | `email_id` | Email ID | `uuid` | - | - | Y |  | `email_id` | Generated email ID | [Data Mapping](./05_Data_Mapping.md#dm-3-7) |  |
| 5 | `purpose` | Token purpose | `varchar` | 24 | - | Y |  | `REGISTER` | Canonical purpose | [Data Mapping](./05_Data_Mapping.md#dm-3-7) |  |
| 6 | `token_hash` | Token hash | `char` | 64 | - | Y |  | `verification_token_hash` | Hash of raw token | [Data Mapping](./05_Data_Mapping.md#dm-3-7) |  |
| 7 | `status` | Token status | `token_status` | - | - | Y |  | `ACTIVE` | DB default | [Data Mapping](./05_Data_Mapping.md#dm-3-7) |  |
| 8 | `expires_at` | Expires at | `timestamptz` | - | - | Y |  | `verification_expires_at` | SOURCE_REQUIRED TTL | [Data Mapping](./05_Data_Mapping.md#dm-3-7) |  |
| 9 | `consumed_at` | Consumed at | `timestamptz` | - | - | N |  | `NULL` | Unused | [Data Mapping](./05_Data_Mapping.md#dm-3-7) |  |
| 10 | `revoked_at` | Revoked at | `timestamptz` | - | - | N |  | `NULL` | Not revoked | [Data Mapping](./05_Data_Mapping.md#dm-3-7) |  |
| 11 | `request_ip_hash` | Request IP hash | `char` | 64 | - | N |  | `request_ip_hash` | Request context hash | [Data Mapping](./05_Data_Mapping.md#dm-3-7) |  |

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
