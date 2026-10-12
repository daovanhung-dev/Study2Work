---
title: "Định nghĩa table"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "39"
api_name: "Lấy danh sách thread"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | discussions; users |
| Logical table | Discussion thread list and author projection |
| Operation | SELECT candidate only; design-only |
| Data Mapping step | 2–4 |

## Update mapping

**Áp dụng khi**

- N/A — READ-ONLY API; không có UPDATE.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| — | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No mutation. |

## Insert mapping

**Áp dụng khi**

- N/A — READ-ONLY API; không có INSERT.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| — | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No mutation. |

## Delete mapping

**Áp dụng khi**

- N/A — READ-ONLY API; không có DELETE.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| — | N/A | N/A | N/A | N/A | No mutation. |

## Candidate read projection

> Checked-in DB.sql and DB_UNICA_ERD are design evidence, not confirmation of live schema or an approved API #39 query. No SQL is asserted in this table.

| No | Table | Candidate column | Type in checked-in DB.sql | DDL constraint | Data Mapping use | Source status |
|---:|---|---|---|---|---|---|
| 1 | discussions | id | BIGSERIAL | PRIMARY KEY | Discussion ID | ERD/DDL DESIGN_ONLY |
| 2 | discussions | course_id | BIGINT | Nullable FK in DDL; required in DB guide/ERD | Course filter and response | DISCREPANCY |
| 3 | discussions | user_id | BIGINT | Nullable FK in DDL; required in DB guide/ERD | Author join | DISCREPANCY |
| 4 | discussions | parent_id | BIGINT | Nullable self-FK | Candidate root/reply distinction | ERD/DDL DESIGN_ONLY |
| 5 | discussions | content | TEXT | NOT NULL | Discussion content | ERD/DDL DESIGN_ONLY |
| 6 | discussions | status | VARCHAR(20) | DEFAULT ACTIVE | Status projection; visibility unresolved | ERD/DDL DESIGN_ONLY |
| 7 | discussions | created_at | TIMESTAMP | NOT NULL | Candidate thread/comment timestamp | ERD/DDL DESIGN_ONLY |
| 8 | discussions | updated_at | TIMESTAMP | NOT NULL | Not present in Discussion response schema | ERD/DDL DESIGN_ONLY |
| 9 | users | id | BIGSERIAL | PRIMARY KEY | Author ID | ERD/DDL DESIGN_ONLY |
| 10 | users | full_name | VARCHAR(150) | NOT NULL | UserSummary.full_name | ERD/DDL DESIGN_ONLY |
| 11 | users | avatar_url | TEXT | NULL | Optional UserSummary.avatar_url | ERD/DDL DESIGN_ONLY |

## Query and mutation boundary

- No discussion route, module, query method or API #39 test is present in the current Study Server source scan.
- discussions self-reference supports candidate child rows through parent_id; whether API #39 embeds them is unresolved.
- The catalog-required Discussion.title has no column in the checked-in DDL or DB ERD.
- DDL permits NULL for discussions.course_id and discussions.user_id; ERD/DB guide describe these relationships as required.
- INSERT mapping: N/A.
- UPDATE mapping: N/A.
- DELETE mapping: N/A.
- No table, column, migration or runtime behavior is added by this DD.
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

