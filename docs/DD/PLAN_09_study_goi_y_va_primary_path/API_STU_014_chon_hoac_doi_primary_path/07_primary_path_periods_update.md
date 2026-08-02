---
title: "primary_path_periods UPDATE"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "API-STU-014"
status: "NEEDS USER DECISION — Draft"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `TBL-STU-026` |
| Logical table | `primary_path_periods` |
| Operation | `UPDATE` |
| Data Mapping step | `05_Data_Mapping.md#3-insertupdate-thong-tin` |

## Update mapping

**Áp dụng khi**

- `Existing ACTIVE period; Q-12 and immutable transition semantics unresolved.`

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| 1 | `status` | `status` | `primary_path_status NOT NULL` | `N/A` | `N/A` | `Y` | `` | `SWITCHED_OUT` | `SWITCHED_OUT` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `CONFLICT` |
| 2 | `ended_at` | `ended_at` | `timestamptz NULL` | `N/A` | `N/A` | `N` | `` | `current_timestamp` | `current_timestamp` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `CONFLICT` |
| 3 | `end_reason` | `end_reason` | `varchar(80) NULL` | `N/A` | `N/A` | `N` | `` | `request.reason or SELF_SWITCH` | `request.reason or SELF_SWITCH` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `CONFLICT` |
| 4 | `updated_at` | `updated_at` | `SOURCE_REQUIRED` | `N/A` | `N/A` | `N` | `` | `SOURCE_REQUIRED — table uses IMMUTABLE set` | `SOURCE_REQUIRED — table uses IMMUTABLE set` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `CONFLICT` |
| 5 | `row_version` | `row_version` | `SOURCE_REQUIRED` | `N/A` | `N/A` | `N` | `` | `SOURCE_REQUIRED — table uses IMMUTABLE set` | `SOURCE_REQUIRED — table uses IMMUTABLE set` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `CONFLICT` |

## Insert mapping

**Áp dụng khi**

- `N/A — Operation không phải INSERT.`

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| 1 | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N` |  | `N/A` | `N/A` | `N/A` | Operation không áp dụng |

## Delete mapping

**Áp dụng khi**

- `N/A — Không có physical DELETE trong mapping này.`

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| 1 | `N/A` | `N/A` | `N/A` | `N/A` | Không hard-delete audit/history/token lifecycle nếu source không cho phép |

- Data Mapping: [05_Data_Mapping.md](./05_Data_Mapping.md#3-insertupdate-thong-tin).
- Schema mismatch columns: `updated_at; row_version`.

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
