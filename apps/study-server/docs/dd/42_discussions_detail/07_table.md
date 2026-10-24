---
title: "Định nghĩa table"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "42"
api_name: "Tải lại thread thảo luận"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | discussions; users; enrollments |
| Logical table | Một Discussion root và các comment trực tiếp |
| Operation | SELECT candidate only; design-only |
| Data Mapping step | 0–5 |
| Evidence | AC-19 API #42; DB guide/ERD; checked-in DDL |

## Update mapping

**Áp dụng khi**

- N/A — READ-ONLY API; không có UPDATE.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---:|---|
| — | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No mutation. |

## Insert mapping

**Áp dụng khi**

- N/A — READ-ONLY API; API #41 owns reply insert.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| — | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No mutation. |

## Delete mapping

**Áp dụng khi**

- N/A — READ-ONLY API; không có DELETE.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---|
| — | N/A | N/A | N/A | N/A | No mutation. |

## Candidate read projection

> Các bảng dưới đây là design evidence; không khẳng định live schema hoặc SQL đã được duyệt.

| No | Table | Candidate column | Type in checked-in DB.sql | DDL constraint | Data Mapping use | Source status |
|---:|---|---|---|---|---|---|
| 1 | discussions AS root | id | BIGSERIAL | PRIMARY KEY | Root thread ID | ERD/DDL DESIGN_ONLY |
| 2 | discussions AS root | course_id | BIGINT | Nullable FK in DDL; required in DB guide/ERD | Course scope and response | DISCREPANCY |
| 3 | discussions AS root | user_id | BIGINT | Nullable FK in DDL; required in DB guide/ERD | Root author join | DISCREPANCY |
| 4 | discussions AS root | parent_id | BIGINT | Nullable self-FK | Require NULL for root topic | ERD/DDL DESIGN_ONLY |
| 5 | discussions AS root | content | TEXT | NOT NULL | Root content string | ERD/DDL DESIGN_ONLY |
| 6 | discussions AS root | status | VARCHAR(20) | DEFAULT ACTIVE | Candidate public topic gate | DERIVED; enum unresolved |
| 7 | discussions AS root | created_at | TIMESTAMP | NOT NULL | Available source, not in Discussion schema | ERD/DDL DESIGN_ONLY |
| 8 | discussions AS root | updated_at | TIMESTAMP | NOT NULL | Not in Discussion response schema | ERD/DDL DESIGN_ONLY |
| 9 | discussions AS child | id | BIGSERIAL | PRIMARY KEY | Comment ID | ERD/DDL DESIGN_ONLY |
| 10 | discussions AS child | parent_id | BIGINT | FK; nullable | Map to DiscussionComment.discussion_id | ERD/DDL DESIGN_ONLY |
| 11 | discussions AS child | user_id | BIGINT | Nullable FK in DDL | Comment author join | DISCREPANCY |
| 12 | discussions AS child | content | TEXT | NOT NULL | Comment content string | ERD/DDL DESIGN_ONLY |
| 13 | discussions AS child | status | VARCHAR(20) | DEFAULT ACTIVE | Candidate visible comment filter | DERIVED; enum unresolved |
| 14 | discussions AS child | created_at | TIMESTAMP | NOT NULL | Comment chronological order/output | ERD/DDL DESIGN_ONLY |
| 15 | users AS author | id | BIGSERIAL | PRIMARY KEY | UserSummary.id | ERD/DDL DESIGN_ONLY |
| 16 | users AS author | full_name | VARCHAR(150) | NOT NULL | UserSummary.full_name | ERD/DDL DESIGN_ONLY |
| 17 | users AS author | avatar_url | TEXT | NULL | Optional UserSummary.avatar_url | ERD/DDL DESIGN_ONLY |
| 18 | enrollments AS e | user_id | BIGINT | Nullable FK in DDL | Student principal match | DERIVED access gate |
| 19 | enrollments AS e | course_id | BIGINT | Nullable FK in DDL | Root course match | DERIVED access gate |
| 20 | enrollments AS e | status | VARCHAR(20) | DEFAULT ACTIVE | ACTIVE enrollment check | DERIVED; policy needs confirmation |
| — | discussions | title | N/A | No column in ERD/DDL | Required Discussion.title | SOURCE_REQUIRED / DISCREPANCY |
| — | discussions | counter | N/A | No field/table in ERD/DDL | No persistent counter output/write | SOURCE_REQUIRED if counter expected |

## Query boundary

- Q1 resolves one root row by ID, then checks topic/course access before returning content.
- Q2 reads direct child rows for that root where status is ACTIVE, joined to author summaries and ordered by created_at ASC, id ASC.
- Q3 checks an ACTIVE enrollment for the authenticated Student and the root course; predicate is DERIVED.
- Null author FK cannot fulfill required UserSummary; treat as data integrity failure rather than silently dropping data.
- No physical title or counter is invented; no INSERT/UPDATE/DELETE is part of API #42.
---
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


