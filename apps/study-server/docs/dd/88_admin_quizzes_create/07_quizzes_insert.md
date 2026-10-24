---
title: "Định nghĩa table — quizzes INSERT"
order: 7
dd_id: "88"
api_name: "Tạo quiz mới"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — quizzes INSERT

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | quizzes |
| Logical table | Quiz |
| Operation | INSERT |
| Data Mapping step | [M1 — Step 3](./05_Data_Mapping.md#step-3-insert-quiz-parent) |
| Source | Legacy infra/postgres/study-server/DB.sql candidate |
| Live schema status | Chưa xác minh |

## Update mapping

**Áp dụng khi**

- N/A — API #88 tạo quiz; update thuộc API #89.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | API #88 không UPDATE bảng. |

## Insert mapping

**Áp dụng khi**

- Sau khi Admin được phép và config được parse theo proposal DERIVED.
- Course reference đã được kiểm tra theo candidate Q0.
- Cùng transaction với INSERT question và choice rows.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | id | Quiz ID | BIGSERIAL / int64 | N/A | N/A | Y | PK | Database generated | DB.sql candidate | 3 | Contract requires int64; live schema unverified. |
| 2 | course_id | Course ID | BIGINT / int64 | 8 bytes | N/A | Y by proposal | FK | config.course_id | Quiz schema + embedded config | 3 | DDL nullable; table guide says relation required. |
| 3 | name | Quiz title | VARCHAR | 200 | N/A | Y |  | config.title → name | Quiz.title + legacy DDL | 3 | Alias DERIVED; candidate physical max 200. |
| 4 | description | Description | TEXT | N/A | N/A | N |  | NULL / not provided | No Quiz/config field | 3 | Nullable candidate; do not invent input. |
| 5 | passing_score | Passing score | NUMERIC | 5 | 2 | Y |  | config.passing_score | Quiz schema + legacy DDL | 3 | Decimal range/scale policy open. |
| 6 | time_limit_minutes | Duration | INT | 4 | N/A | N |  | config.duration_minutes or NULL | Quiz.duration_minutes? + legacy DDL | 3 | Optional; null/omit response rule open. |
| 7 | status | Quiz status | VARCHAR | 20 | N/A | N |  | Use DDL default DRAFT | Legacy DB.sql | 3 | Not in request/Quiz response; lifecycle unresolved. |
| 8 | created_at | Created time | TIMESTAMP | N/A | N/A | Y |  | Current transaction time | Legacy DB.sql | 3 | DDL NOT NULL; no default. |
| 9 | updated_at | Updated time | TIMESTAMP | N/A | N/A | Y |  | Same value as created_at | Legacy DB.sql | 3 | DDL NOT NULL; no default. |

## Delete mapping

**Áp dụng khi**

- N/A — deletion thuộc API #90 và phụ thuộc attempts/policy.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | API #88 không DELETE. |
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
