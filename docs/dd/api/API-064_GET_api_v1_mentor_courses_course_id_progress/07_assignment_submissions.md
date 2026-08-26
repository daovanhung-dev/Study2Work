---
title: "DB Mapping — assignment_submissions"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
---

# DB Mapping — `assignment_submissions`

## 1. Table source

- Source: `docs/diagrams/DB_UNICA_ERD.drawio`
- Table: `assignment_submissions`
- API: `GET /api/v1/mentor/courses/{course_id}/progress`

## 2. ERD-defined columns

| Column | Type | Constraint/Relation |
|---|---|---|
| `id` | `BIGSERIAL` | PK |
| `assignment_id` | `BIGINT` | FK → assignments.id |
| `user_id` | `BIGINT` | FK → users.id |
| `content` | `TEXT` | NULL |
| `file_url` | `TEXT` | NULL |
| `submitted_at` | `TIMESTAMP` | NOT NULL |
| `score` | `NUMERIC(6,2)` | NULL |
| `feedback` | `TEXT` | NULL |
| `status` | `VARCHAR(20)` | DEFAULT SUBMITTED |

## 3. API usage

- Entity involvement is supported by the Activity/ERD mapping used by this DD.
- Exact columns read/written, predicates, join projection, transaction boundary, and mutation values are only fixed where `05_Data_Mapping.md` has explicit source evidence.
- Any remaining detail is `TBD`; **không suy diễn column usage chỉ vì column tồn tại trong ERD**.
