---
title: "DB Mapping — quizzes"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
---

# DB Mapping — `quizzes`

## 1. Table source

- Source: `docs/diagrams/DB_UNICA_ERD.drawio`
- Table: `quizzes`
- API: `PUT /api/v1/admin/quizzes/{quiz_id}`

## 2. ERD-defined columns

| Column | Type | Constraint/Relation |
|---|---|---|
| `id` | `BIGSERIAL` | PK |
| `course_id` | `BIGINT` | FK → courses.id |
| `name` | `VARCHAR(200)` | NOT NULL |
| `description` | `TEXT` | NULL |
| `passing_score` | `NUMERIC(5,2)` | DEFAULT 0 |
| `time_limit_minutes` | `INT` | NULL |
| `status` | `VARCHAR(20)` | DEFAULT DRAFT |
| `created_at` | `TIMESTAMP` | NOT NULL |
| `updated_at` | `TIMESTAMP` | NOT NULL |

## 3. API usage

- Entity involvement is supported by the Activity/ERD mapping used by this DD.
- Exact columns read/written, predicates, join projection, transaction boundary, and mutation values are only fixed where `05_Data_Mapping.md` has explicit source evidence.
- Any remaining detail is `TBD`; **không suy diễn column usage chỉ vì column tồn tại trong ERD**.
