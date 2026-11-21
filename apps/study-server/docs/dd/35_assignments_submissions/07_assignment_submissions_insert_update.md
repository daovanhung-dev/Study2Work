---
title: "Định nghĩa table"
order: 7
dd_id: "35"
api_name: "Tạo/nộp submission"
source_sheet: "table — assignment_submissions insert/update"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | assignment_submissions |
| Logical table | Submission |
| Operation | INSERT / UPDATE candidate per AC-17; branch rule SOURCE_REQUIRED |
| Data Mapping step | 4 |

> Candidate mapping từ DB_UNICA_TABLES.md, ERD V1 và checked-in DB.sql; không xác nhận schema live hoặc runtime query. AC-17 nêu INSERT/UPDATE Submission = SUBMITTED nhưng không nêu key/branch rule.

## Read mapping

| No | Physical column | Logical field | Type | Nullable in DDL | Key/constraint | Data Mapping step | Remarks |
|---:|---|---|---|---:|---|---:|---|
| 1 | id | id | BIGSERIAL / int64 | No | PK | 4 | Candidate generated identity; generator/RETURNING behavior not verified. |
| 2 | assignment_id | assignment_id | BIGINT / int64 | Yes | FK to assignments.id | 2/4 | DB table notes call this required; checked-in DDL permits NULL. |
| 3 | user_id | user_id | BIGINT / int64 | Yes | FK to users.id | 0/4 | Candidate value from authenticated Student, never from request; DDL permits NULL. |
| 4 | content | content | TEXT / string | Yes | — | 1/4 | Candidate source for request text; required request versus nullable column is unresolved. |
| 5 | file_url | files | TEXT / uri candidate | Yes | — | 1/4 | One URL column cannot define the logical UploadAsset[] collection or file-ref format. |
| 6 | submitted_at | submitted_at | TIMESTAMP / date-time | No | — | 4 | DDL requires a value; time generator, timezone and serialization are unresolved. |
| 7 | score | score | NUMERIC(6,2) / decimal-string | Yes | — | 4 | No API #35 grading value is specified; do not invent an initial score. |
| 8 | feedback | feedback | TEXT / string | Yes | — | 4 | No API #35 feedback value is specified. |
| 9 | status | status | VARCHAR(20) / SubmissionStatus | Yes | DEFAULT SUBMITTED | 4 | AC-17 says initial SUBMITTED; full enum and lifecycle are undefined. |

## Update mapping

**Áp dụng khi**

- AC-17 describes an UPDATE branch, but the matching-row key, permitted current status, and resubmission policy are SOURCE_REQUIRED.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| 1 | assignment_id | Assignment ID | BIGINT | N/A | N/A | Candidate | Candidate predicate | Path assignment_id | API catalog / path | 4 | Whether it participates in a unique update key is unresolved. |
| 2 | user_id | Student ID | BIGINT | N/A | N/A | Candidate | Candidate predicate | Authenticated Student principal | API catalog / Bearer JWT | 0/4 | Must not come from request; no unique pair constraint is defined. |
| 3 | content | Submission text | TEXT | N/A | N/A | Candidate | — | Request text | API catalog | 1/4 | Whether an update replaces or preserves prior content is unresolved. |
| 4 | file_url | File reference | TEXT | N/A | N/A | Candidate | — | file refs only under an approved single-reference mapping | API catalog / API #34 | 1/4 | Cardinality, UploadAsset binding and replace/append behavior are unresolved. |
| 5 | submitted_at | Submission time | TIMESTAMP | N/A | N/A | Candidate | — | SOURCE_REQUIRED | DB design / time generator | 4 | Whether resubmission changes the timestamp is unresolved. |
| 6 | status | Submission status | VARCHAR(20) | N/A | N/A | Candidate | — | SUBMITTED per AC-17 | AC-17 | 4 | Allowed current states and transition rule are unresolved. |

- Do not update id, score or feedback from API #35 without a source rule.
- No transaction or optimistic-locking rule is specified.

## Insert mapping

**Áp dụng khi**

- AC-17 requires a Submission to be created; INSERT is named in the flow, but the condition selecting INSERT is SOURCE_REQUIRED.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---:|---|
| 1 | assignment_id | Assignment ID | BIGINT | N/A | N/A | Design: Yes; DDL: nullable |  | Path assignment_id | API catalog | 2/4 | Required logical FK; live constraint not verified. |
| 2 | user_id | Student ID | BIGINT | N/A | N/A | Design: Yes; DDL: nullable |  | Authenticated Student principal | API catalog / Bearer JWT | 0/4 | Must not be client-supplied. |
| 3 | content | Submission text | TEXT | N/A | N/A | Request: Yes; DDL: nullable |  | Request text | API catalog | 1/4 | Null/empty and storage requirement discrepancy unresolved. |
| 4 | file_url | File reference | TEXT | N/A | N/A | Request token: Yes; DDL: nullable |  | SOURCE_REQUIRED | API catalog / API #34 candidate | 1/4 | No confirmed one-to-one mapping from file refs to file_url. |
| 5 | submitted_at | Submission time | TIMESTAMP | N/A | N/A | DDL: NOT NULL |  | SOURCE_REQUIRED | Time generator | 4 | Do not assume application clock, DB clock or timezone. |
| 6 | status | Submission status | VARCHAR(20) | N/A | N/A | DDL: nullable with default |  | SUBMITTED | AC-17 | 4 | AC-17 supplies initial state; full enum not supplied. |

- id has a BIGSERIAL candidate default; the DD does not assert a live sequence or generation behavior.
- score and feedback are nullable candidate columns and are not assigned values by API #35 sources.

## Delete mapping

**Áp dụng khi**

- N/A — API #35 does not define deletion.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---|---|---|---|---:|---|
| N/A | N/A | N/A | N/A | N/A | API #35 does not define deletion. |
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
