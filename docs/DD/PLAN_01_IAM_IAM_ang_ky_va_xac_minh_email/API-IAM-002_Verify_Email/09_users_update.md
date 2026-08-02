---
title: "users_update"
order: 9
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
---

# Định nghĩa table

<a id="db-map"></a>

## Table metadata

| Thuộc tính | Giá trị |
| --- | --- |
| Physical table | `users` |
| Logical table | TBL-IAM-001 — Platform users |
| Operation | `UPDATE` |
| Data Mapping step | [05_Data_Mapping.md](./05_Data_Mapping.md#dm-3-4) |

## Update mapping

**Áp dụng khi**

- users.id = token.user_id.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | ID | `uuid` | - | - | Y | ● | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 2 | `created_at` | Created at | `timestamptz` | - | - | Y |  | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 3 | `updated_at` | Updated at | `timestamptz` | - | - | Y |  | `current_timestamp` | Generated | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 4 | `row_version` | Row version | `bigint` | - | - | Y |  | `row_version + 1` | ENTITY rule | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 5 | `status` | Account status | `account_status` | - | - | Y |  | `ACTIVE` | Verified account state | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 6 | `display_name` | Display name | `varchar` | 120 | - | N |  | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 7 | `locale` | Locale | `varchar` | 10 | - | Y |  | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 8 | `timezone` | Timezone | `varchar` | 64 | - | Y |  | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 9 | `email_verified_at` | Email verified at | `timestamptz` | - | - | N |  | `current_timestamp` | Generated | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 10 | `suspended_at` | Suspended at | `timestamptz` | - | - | N |  | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 11 | `suspension_reason` | Suspension reason | `varchar` | 500 | - | N |  | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 12 | `deletion_requested_at` | Deletion requested at | `timestamptz` | - | - | N |  | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 13 | `anonymized_at` | Anonymized at | `timestamptz` | - | - | N |  | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |
| 14 | `privileged_mfa_required` | Privileged MFA required | `boolean` | - | - | Y |  | Không đổi | N/A | [Data Mapping](./05_Data_Mapping.md#dm-3-4) |  |

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
