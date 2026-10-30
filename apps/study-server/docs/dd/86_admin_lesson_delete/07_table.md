---
title: "Định nghĩa table"
order: 7
dd_id: "86"
api_name: "Xóa lesson"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical mutation table | Legacy BIGINT `lessons` candidate |
| Logical table | Lesson |
| Operation | `UPDATE lessons.status/updated_at`; dependency `EXISTS` checks |
| Data Mapping step | [Step 3](./05_Data_Mapping.md#step-3-check-dependency-va-policy), [Step 4](./05_Data_Mapping.md#step-4-soft-delete-theo-policy) |
| Schema status | Legacy BIGINT DDL candidate; `DELETED` marker and timestamp alias are DERIVED; V1-PILOT UUID model is separate; live schema unknown. |

## Dependency read mapping — legacy candidates

| No | Relation/column | Type | Key/reference | Condition | Data Mapping step | Remarks |
|---:|---|---|---|---|---|---|
| 1 | resources.lesson_id | BIGINT candidate | FK candidate to lessons.id | lesson_id = :lesson_id | Q2a | Legacy DDL artifact; live FK/policy unknown. |
| 2 | lesson_progress.lesson_id | BIGINT candidate | FK candidate to lessons.id | lesson_id = :lesson_id | Q2b | Any progress status blocks; legacy DDL artifact. |
| 3 | lesson_uploads.lesson_id | BIGINT candidate | FK candidate to lessons.id | lesson_id = :lesson_id | Q2c | Any linked upload blocks; links/assets remain unchanged. |
| 4 | lessons.id | BIGSERIAL candidate | Primary key | id = :lesson_id | Q1 | Candidate target identity; no approved live-schema claim. |

## Soft-delete mutation mapping

No new column is introduced. The local fallback uses the legacy Lesson status and modification timestamp, following API #77.

| Logical field/effect | Physical source | Required mapping | Status |
|---|---|---|---|
| Lesson deleted state | lessons.status | Set literal `DELETED` | DERIVED from API #77 and checked-in DDL |
| deleted_at | lessons.updated_at | Set `CURRENT_TIMESTAMP`; return DB value | DERIVED mapping; live metadata unverified |
| DeleteResult.id | lessons.id | Return target ID from UPDATE RETURNING | Legacy BIGINT candidate |
| DeleteResult.status | Reusable DeleteResult | Literal deleted | DIRECT schema value |

## Insert mapping

**Áp dụng khi**

- N/A — API #86 không tạo lesson hoặc audit record.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No INSERT operation. |

## Delete mapping

**Áp dụng khi**

- N/A — no physical DELETE statement; operation is a status tombstone.

| No | Target relation/column | Operator | Value source | Data Mapping step | Remarks |
|---|---|---|---|---|---|
| 1 | lessons | UPDATE | `status='DELETED'`, `updated_at=CURRENT_TIMESTAMP` | M1 | Preserve row and all dependent/history rows. |

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
