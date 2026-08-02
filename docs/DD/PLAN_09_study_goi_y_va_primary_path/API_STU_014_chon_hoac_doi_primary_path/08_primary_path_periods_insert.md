---
title: "primary_path_periods INSERT"
order: 8
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
| Operation | `INSERT` |
| Data Mapping step | `05_Data_Mapping.md#3-insertupdate-thong-tin` |

## Update mapping

**Áp dụng khi**

- `N/A — Operation không phải UPDATE.`

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| 1 | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N` |  | `N/A` | `N/A` | `N/A` | Operation không áp dụng |

## Insert mapping

**Áp dụng khi**

- `Theo Data Mapping và owner/version predicate.`

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| 1 | `id` | `id` | `uuid NOT NULL` | `N/A` | `N/A` | `Y` | `●` | `Generated UUID v7` | `Generated UUID v7` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 2 | `created_at` | `created_at` | `timestamptz NOT NULL DEFAULT now()` | `N/A` | `N/A` | `Y` | `` | `current_timestamp` | `current_timestamp` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 3 | `learner_id` | `learner_id` | `uuid NOT NULL` | `N/A` | `N/A` | `Y` | `` | `Authenticated learner ID` | `Authenticated learner ID` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 4 | `path_version_id` | `path_version_id` | `uuid NOT NULL` | `N/A` | `N/A` | `Y` | `` | `request.pathVersionId` | `request.pathVersionId` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 5 | `status` | `status` | `primary_path_status NOT NULL` | `N/A` | `N/A` | `Y` | `` | `ACTIVE` | `ACTIVE` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 6 | `started_at` | `started_at` | `timestamptz NOT NULL` | `N/A` | `N/A` | `Y` | `` | `current_timestamp` | `current_timestamp` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 7 | `ended_at` | `ended_at` | `timestamptz NULL` | `N/A` | `N/A` | `N` | `` | `NULL` | `NULL` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 8 | `end_reason` | `end_reason` | `varchar(80) NULL` | `N/A` | `N/A` | `N` | `` | `NULL` | `NULL` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 9 | `supersedes_period_id` | `supersedes_period_id` | `uuid NULL` | `N/A` | `N/A` | `N` | `` | `Previous active period ID or NULL` | `Previous active period ID or NULL` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 10 | `switch_request_id` | `switch_request_id` | `uuid NULL` | `N/A` | `N/A` | `N` | `` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 11 | `selected_from_recommendation_id` | `selected_from_recommendation_id` | `uuid NULL` | `N/A` | `N/A` | `N` | `` | `SOURCE_REQUIRED or NULL` | `SOURCE_REQUIRED or NULL` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |

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
