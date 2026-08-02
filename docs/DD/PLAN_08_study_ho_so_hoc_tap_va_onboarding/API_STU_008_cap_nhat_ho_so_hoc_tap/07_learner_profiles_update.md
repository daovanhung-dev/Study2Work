---
title: "learner_profiles UPDATE"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "API-STU-008"
status: "STRUCTURE_CONFLICT — Draft"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `TBL-STU-002` |
| Logical table | `learner_profiles` |
| Operation | `UPDATE` |
| Data Mapping step | `05_Data_Mapping.md#3-insertupdate-thong-tin` |

## Update mapping

**Áp dụng khi**

- `If-Match; locale/timezone/skillIds have no canonical columns/relations.`

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| 1 | `full_name` | `full_name` | `varchar(160) NULL` | `N/A` | `N/A` | `N` | `` | `CONFLICT — request.displayName mapping not approved` | `CONFLICT — request.displayName mapping not approved` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `CONFLICT` |
| 2 | `bio` | `bio` | `varchar(2000) NULL` | `N/A` | `N/A` | `N` | `` | `request.bio with API max 1000` | `request.bio with API max 1000` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `CONFLICT` |
| 3 | `updated_at` | `updated_at` | `timestamptz NOT NULL DEFAULT now()` | `N/A` | `N/A` | `Y` | `` | `current_timestamp` | `current_timestamp` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `CONFLICT` |
| 4 | `row_version` | `row_version` | `bigint NOT NULL DEFAULT 1` | `N/A` | `N/A` | `Y` | `` | `row_version + 1` | `row_version + 1` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `CONFLICT` |

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
- Schema mismatch columns: `N/A`.

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
