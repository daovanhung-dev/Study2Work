---
title: "path_recommendation_runs INSERT"
order: 8
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "API-STU-011"
status: "STRUCTURE_CONFLICT — Draft"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `TBL-STU-008` |
| Logical table | `path_recommendation_runs` |
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
| 4 | `onboarding_submission_id` | `onboarding_submission_id` | `uuid NOT NULL` | `N/A` | `N/A` | `Y` | `` | `Created completed submission ID` | `Created completed submission ID` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 5 | `algorithm_version` | `algorithm_version` | `varchar(40) NOT NULL` | `N/A` | `N/A` | `Y` | `` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 6 | `input_snapshot` | `input_snapshot` | `jsonb NOT NULL` | `N/A` | `N/A` | `Y` | `` | `Completed answer snapshot` | `Completed answer snapshot` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 7 | `ranked_path_version_ids` | `ranked_path_version_ids` | `uuid[] NOT NULL` | `N/A` | `N/A` | `Y` | `` | `Deterministic ranked UUID array` | `Deterministic ranked UUID array` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 8 | `reason_snapshot` | `reason_snapshot` | `jsonb NOT NULL` | `N/A` | `N/A` | `Y` | `` | `SOURCE_REQUIRED item-level schema — Q-10` | `SOURCE_REQUIRED item-level schema — Q-10` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 9 | `generated_at` | `generated_at` | `timestamptz NOT NULL` | `N/A` | `N/A` | `Y` | `` | `current_timestamp` | `current_timestamp` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 10 | `expires_at` | `expires_at` | `timestamptz NOT NULL` | `N/A` | `N/A` | `Y` | `` | `SOURCE_REQUIRED policy expiry` | `SOURCE_REQUIRED policy expiry` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |

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
