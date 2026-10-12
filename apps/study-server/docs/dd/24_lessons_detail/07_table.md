---
title: "Định nghĩa table"
order: 7
dd_id: "24"
api_name: "Nạp nội dung bài học / Lấy nội dung chính"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `lessons` — candidate, DESIGN_ONLY |
| Logical table | Lesson |
| Operation | READ / GET; không có mutation mapping |
| Data Mapping step | 2–3 |

## Read mapping

| No | Item ID / Column | Item name | Type | Length | Required in checked-in DDL | Main key | Setting content / response mapping | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---|---|---|---|---:|---|
| 1 | id | Lesson ID | BIGSERIAL | N/A | Yes | Primary key | Candidate `data.id:int64` | `DB.sql` / catalog Lesson | 2–3 | Design-only; API #24 query chưa xác nhận. |
| 2 | course_id | Course ID | BIGINT | N/A | No — DDL không ghi `NOT NULL` | N/A | Candidate `data.course_id:int64` | `DB.sql` / catalog Lesson | 2–3 | DDL nullability differs from DB design documentation and required logical schema. |
| 3 | name | Lesson title | VARCHAR | 200 | Yes | N/A | `name` → candidate `data.title:string` | `DB.sql` / `DB_UNICA_TABLES.md` | 2–3 | Candidate logical mapping; query not confirmed. |
| 4 | content | Lesson content | TEXT | N/A | No — nullable | N/A | Candidate `data.content?:string` | `DB.sql` / catalog Lesson | 2–3 | Null/omitted serialization rule unspecified. |
| 5 | video_url | Video URL | TEXT | N/A | No — nullable | N/A | Candidate `data.video_url?:uri` | `DB.sql` / catalog Lesson | 2–3 | URI conversion and null/omit behavior unspecified. |
| 6 | sort_order | Lesson order | INT | N/A | No — DDL has default 0, no `NOT NULL` | N/A | `sort_order` → candidate `data.order:int32` | `DB.sql` / `DB_UNICA_TABLES.md` | 2–3 | Candidate mapping; DB design says logical order. |
| 7 | status | Lesson status | VARCHAR | 20 | No — DDL has default DRAFT, no `NOT NULL` | N/A | Candidate `data.status:LessonStatus` | `DB.sql` / catalog Lesson | 2–3 | Enum values and publish predicate unspecified. |

## Update mapping

**Áp dụng khi**

- N/A — API #24 là GET; catalog và diagrams không mô tả UPDATE.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---|---|---|---|---:|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Read-only API; không có update mapping. |

## Insert mapping

**Áp dụng khi**

- N/A — API #24 là GET; catalog và diagrams không mô tả INSERT.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---|---|---|---|---:|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Read-only API; không có insert mapping. |

## Delete mapping

**Áp dụng khi**

- N/A — API #24 là GET; catalog và diagrams không mô tả DELETE.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---|
| N/A | N/A | N/A | N/A | N/A | Read-only API; không có delete mapping. |

## Read source note

- Checked-in DDL định nghĩa `lessons.id`, `course_id`, `name`, `content`, `video_url`, `sort_order`, `status`, `created_at` và `updated_at`.
- Response schema `Lesson` không có `created_at` hoặc `updated_at`; DD không thêm hai field này vào payload.
- DDL checked-in không khai báo `lessons.course_id NOT NULL`, trong khi `DB_UNICA_TABLES.md` mô tả quan hệ bắt buộc và catalog yêu cầu `course_id:int64`.
- `DB.sql` và ERD là design evidence; không xác nhận live schema, API #24 runtime query hoặc projection.
- Candidate access sources `courses`/`enrollments` chưa được đưa vào mapping table như một query đã chốt; xem [05_Data_Mapping.md](./05_Data_Mapping.md) và [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

---
## Phụ lục đối chiếu template Markdown

- Template: [07_table.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/07_table.md).
- Sheet nguồn: table.
