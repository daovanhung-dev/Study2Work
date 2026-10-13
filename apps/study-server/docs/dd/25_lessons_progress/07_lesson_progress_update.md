---
title: "Định nghĩa table"
order: 7
dd_id: "25"
api_name: "Lưu vị trí và trạng thái"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `lesson_progress` — candidate, DESIGN_ONLY |
| Logical table | Lesson progress record (design concept) |
| Operation | UPDATE/upsert intent per AC-14/DB design; exact mutation unresolved |
| Data Mapping step | 3 |

## Update mapping

**Áp dụng khi**

- AC-14 ghi cập nhật lesson progress; field-level mapping và row selection chưa được xác nhận.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---:|---|
| 1 | `id` | Progress row ID | BIGSERIAL | N/A | N/A | DDL primary key | Primary key | N/A — generated column; API update mapping not specified | Checked-in DDL | 3 | Schema design only; no row-selection key for API #25 is approved. |
| 2 | `user_id` | Student ID | BIGINT | N/A | N/A | ERD: Yes; DDL: nullable | No declared unique key | Authenticated identity candidate | JWT identity: SOURCE_REQUIRED | 3 | Candidate ownership column; token mapping unresolved. |
| 3 | `lesson_id` | Lesson ID | BIGINT | N/A | N/A | ERD: Yes; DDL: nullable | No declared unique key | Candidate path identity | `lesson_id` request | 3 | Candidate relationship; lookup/update predicate unresolved. |
| 4 | `status` | Lesson progress status | VARCHAR | 20 | N/A | DDL: nullable, default `NOT_STARTED` | No | `COMPLETED` or `IN_PROGRESS` branch in AC-14; persisted update behavior unresolved | AC-14 diagram | 3 | Allowed enum and behavior for existing states not canonicalized. |
| 5 | `progress_percent` | Progress percent | SMALLINT | N/A | N/A | DDL: nullable, default `0` | No | Candidate mapping from request `percent` | Request body candidate | 3 | Range, conversion and update semantics unresolved; DDL has no CHECK range. |
| 6 | `last_accessed_at` | Last access timestamp | TIMESTAMP | N/A | N/A | Nullable | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | Whether API #25 sets this field and timestamp source are unknown. |
| 7 | `completed_at` | Completion timestamp | TIMESTAMP | N/A | N/A | Nullable | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | Whether/how this field changes on completed true/false is unknown. |

> `id` is the checked-in DDL primary key but no API #25 generation/update mapping is specified. `position` is not a column in the ERD/DDL. Checked-in DDL and ERD are design evidence, not live schema proof.

## Insert mapping

**Áp dụng khi**

- AC-14 does not explicitly define whether API #25 inserts a missing progress row; upsert intent and insert semantics remain SOURCE_REQUIRED.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---:|---|
| 1 | `id` | Progress row ID | BIGSERIAL | N/A | N/A | DDL primary key | Primary key | DB-generated per checked-in DDL; runtime generation not verified | Checked-in DDL | 3 | API request does not provide this field. |
| 2 | `user_id` | Student ID | BIGINT | N/A | N/A | ERD: Yes; DDL: nullable | No declared unique key | SOURCE_REQUIRED | Authenticated identity candidate | 3 | Insert ownership binding not confirmed. |
| 3 | `lesson_id` | Lesson ID | BIGINT | N/A | N/A | ERD: Yes; DDL: nullable | No declared unique key | SOURCE_REQUIRED | `lesson_id` request candidate | 3 | Insert condition and conflict behavior not confirmed. |
| 4 | `status` | Lesson progress status | VARCHAR | 20 | N/A | DDL: nullable, default `NOT_STARTED` | No | SOURCE_REQUIRED | AC-14 state cues only | 3 | Initial status for API #25-created row is not specified. |
| 5 | `progress_percent` | Progress percent | SMALLINT | N/A | N/A | DDL: nullable, default `0` | No | SOURCE_REQUIRED | `percent` candidate | 3 | Range, conversion and default override behavior not specified. |
| 6 | `last_accessed_at` | Last access timestamp | TIMESTAMP | N/A | N/A | Nullable | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | Timestamp policy not specified. |
| 7 | `completed_at` | Completion timestamp | TIMESTAMP | N/A | N/A | Nullable | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | Timestamp policy not specified. |

## Delete mapping

**Áp dụng khi**

- N/A — API #25 and AC-14 do not describe deleting lesson progress.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---|
| N/A | N/A | N/A | N/A | N/A | No delete behavior is specified. |

## Schema and mapping notes

- Checked-in `DB.sql` declares `id BIGSERIAL PRIMARY KEY`, `user_id BIGINT`, `lesson_id BIGINT`, `status VARCHAR(20) DEFAULT 'NOT_STARTED'`, `progress_percent SMALLINT DEFAULT 0`, `last_accessed_at TIMESTAMP NULL` and `completed_at TIMESTAMP NULL`.
- `DB_UNICA_TABLES.md` describes `user_id` and `lesson_id` as required relationships; checked-in DDL omits `NOT NULL` for both columns.
- Neither the ERD field list nor checked-in DDL contains a position column.
- Checked-in DDL does not declare a unique `(user_id, lesson_id)` constraint; do not infer an UPSERT conflict target.
- No course aggregate target table/column is identified. See [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

---
## Phụ lục đối chiếu template Markdown

- Template: [07_table.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/07_table.md).
- Sheet nguồn: table.
