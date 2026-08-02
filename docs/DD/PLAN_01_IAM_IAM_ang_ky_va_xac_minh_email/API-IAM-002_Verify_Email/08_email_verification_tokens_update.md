---
title: "email_verification_tokens_update"
order: 8
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
| Operation | `UPDATE` |
| Data Mapping step | [05_Data_Mapping.md](./05_Data_Mapping.md#dm-3-4) |

## Update mapping

**Áp dụng khi**

- Locked token is ACTIVE REGISTER token and not expired.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | ID | `uuid` | - | - | Y | ● | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 2 | `created_at` | Created at | `timestamptz` | - | - | Y |  | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 3 | `user_id` | User ID | `uuid` | - | - | Y |  | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 4 | `email_id` | Email ID | `uuid` | - | - | Y |  | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 5 | `purpose` | Token purpose | `varchar` | 24 | - | Y |  | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 6 | `token_hash` | Token hash | `char` | 64 | - | Y |  | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 7 | `status` | Token status | `token_status` | - | - | Y |  | `CONSUMED` | Canonical transition | [Data Mapping](./05_Data_Mapping.md#dm-3-4) | Transition phải qua security-definer procedure. |
| 8 | `expires_at` | Expires at | `timestamptz` | - | - | Y |  | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 9 | `consumed_at` | Consumed at | `timestamptz` | - | - | N |  | `current_timestamp` | Generated | [Data Mapping](./05_Data_Mapping.md#dm-3-4) | One-way update. |
| 10 | `revoked_at` | Revoked at | `timestamptz` | - | - | N |  | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 11 | `request_ip_hash` | Request IP hash | `char` | 64 | - | N |  | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |

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
