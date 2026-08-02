---
title: "idempotency_keys_insert"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
---

# Định nghĩa table

<a id="db-map"></a>

## Table metadata

| Thuộc tính | Giá trị |
| --- | --- |
| Physical table | `idempotency_keys` |
| Logical table | TBL-IAM-016 — Idempotency keys |
| Operation | `INSERT` |
| Data Mapping step | [05_Data_Mapping.md](./05_Data_Mapping.md#dm-3-2) |

## Update mapping

**Áp dụng khi**

- N/A — File này không mô tả UPDATE.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

## Insert mapping

**Áp dụng khi**

- Khi chưa có idempotency record cho actor anonymous + operation + key hash.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | ID | `uuid` | - | - | Y | ● | `UUID_V7()` | Generated | [Data Mapping](./05_Data_Mapping.md#dm-3-2) |  |
| 2 | `created_at` | Created at | `timestamptz` | - | - | Y |  | `current_timestamp` | Generated | [Data Mapping](./05_Data_Mapping.md#dm-3-2) |  |
| 3 | `updated_at` | Updated at | `timestamptz` | - | - | Y |  | `current_timestamp` | Generated | [Data Mapping](./05_Data_Mapping.md#dm-3-2) |  |
| 4 | `row_version` | Row version | `bigint` | - | - | Y |  | `1` | DB default | [Data Mapping](./05_Data_Mapping.md#dm-3-2) |  |
| 5 | `actor_id` | Actor ID | `uuid` | - | - | N |  | `NULL` | Anonymous actor | [Data Mapping](./05_Data_Mapping.md#dm-3-2) |  |
| 6 | `operation` | Operation | `varchar` | 120 | - | Y |  | `POST /api/v1/auth/register` | Fixed endpoint | [Data Mapping](./05_Data_Mapping.md#dm-3-2) |  |
| 7 | `key_hash` | Idempotency key hash | `char` | 64 | - | Y |  | `HASH(idempotency_key)` | Request header | [Data Mapping](./05_Data_Mapping.md#dm-3-2) |  |
| 8 | `request_hash` | Request hash | `char` | 64 | - | Y |  | `HASH(canonical_json(body))` | Request body | [Data Mapping](./05_Data_Mapping.md#dm-3-2) |  |
| 9 | `response_status` | Response HTTP status | `integer` | - | - | N |  | `NULL` | Pending | [Data Mapping](./05_Data_Mapping.md#dm-3-2) |  |
| 10 | `response_body` | Redacted response body | `jsonb` | - | - | N |  | `NULL` | Pending | [Data Mapping](./05_Data_Mapping.md#dm-3-2) |  |
| 11 | `locked_until` | Processing lock expiry | `timestamptz` | - | - | N |  | `current_timestamp + SOURCE_REQUIRED_LOCK_TTL` | SOURCE_REQUIRED | [Data Mapping](./05_Data_Mapping.md#dm-3-2) |  |
| 12 | `completed_at` | Completed at | `timestamptz` | - | - | N |  | `NULL` | Pending | [Data Mapping](./05_Data_Mapping.md#dm-3-2) |  |
| 13 | `expires_at` | Record expiry | `timestamptz` | - | - | Y |  | `current_timestamp + 7 days` | DB retention rule for register | [Data Mapping](./05_Data_Mapping.md#dm-3-2) |  |

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
