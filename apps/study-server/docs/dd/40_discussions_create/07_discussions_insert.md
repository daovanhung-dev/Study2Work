---
title: "Định nghĩa discussions INSERT"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "40"
api_name: "Tạo topic/câu hỏi mới"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — discussions INSERT

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `discussions` |
| Logical table | Discussion topic/question |
| Operation | Candidate `INSERT`; design-only |
| Data Mapping step | 3 |
| Evidence | AC-19 create-topic branch; DB guide/ERD and checked-in DDL |

## Update mapping

**Áp dụng khi**

- N/A — API #40 creates a new topic; AC-19 routes replies to API #41.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| — | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No UPDATE is specified for API #40. |

## Insert mapping

**Áp dụng khi**

- AC-19 chooses the new-topic branch; the diagram labels the database action `INSERT Discussion`.
- Rows below are candidate mappings from design evidence, not approved SQL or verified live schema.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| 1 | `id` | Discussion ID | `BIGSERIAL` | N/A | N/A | Yes | ● | Database-generated candidate | DB DDL | 3 | Generated value; live schema not verified. |
| 2 | `course_id` | Course ID | `BIGINT` | N/A | N/A | Logical Yes; DDL nullable |  | Request `course_id` | Request body | 3 | Course access predicate unresolved; nullability conflict. |
| 3 | `user_id` | Author ID | `BIGINT` | N/A | N/A | Logical Yes; DDL nullable |  | Authenticated Student principal ID | Bearer JWT/current auth helper | 3 | No user ID is accepted in request body; nullability conflict. |
| 4 | `parent_id` | Parent discussion ID | `BIGINT` | N/A | N/A | No |  | `NULL` candidate for root topic | DB guide + AC-19 new-topic branch | 3 | Candidate root mapping; not runtime verified. |
| 5 | `content` | Discussion content | `TEXT` | N/A | N/A | Yes |  | `SOURCE_REQUIRED` | Request body `content:int64!` | 3 | No approved conversion from int64 to TEXT/logical string. |
| 6 | `status` | Discussion status | `VARCHAR(20)` | 20 | N/A | DDL default `ACTIVE` |  | `SOURCE_REQUIRED` | Checked-in DDL default | 3 | Default and status enum policy are design-only/unconfirmed. |
| 7 | `created_at` | Created time | `TIMESTAMP` | N/A | N/A | Yes |  | `SOURCE_REQUIRED` | No source defined | 3 | DDL has no default; timestamp source is unresolved. |
| 8 | `updated_at` | Updated time | `TIMESTAMP` | N/A | N/A | Yes |  | `SOURCE_REQUIRED` | No source defined | 3 | DDL has no default; timestamp source is unresolved. |

## Contract fields without physical mapping

| API field | Contract requirement | Physical mapping | Status |
|---|---|---|---|
| `title` | Required `string` in API #40 request and `Discussion` response | No `discussions.title` column in ERD or checked-in DDL | `SOURCE_REQUIRED / DISCREPANCY`; do not map from `content`. |

## Delete mapping

**Áp dụng khi**

- N/A — API #40 does not declare DELETE.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| — | N/A | N/A | N/A | N/A | No DELETE is specified. |

## Candidate mapping boundary

- DDL/ERD and DB guide are design evidence only; live database metadata was not inspected.
- `course_id` and `user_id` are nullable in checked-in DDL but required in the logical guide/ERD.
- `title` has no physical source; `content` type conversion, status policy, timestamp values and transaction behavior remain unresolved.

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
