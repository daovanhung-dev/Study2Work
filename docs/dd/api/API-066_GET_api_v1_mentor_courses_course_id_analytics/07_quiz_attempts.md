---
title: "DB Mapping — quiz_attempts"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
---

# DB Mapping — `quiz_attempts`

## 1. Table source

- Source: `docs/diagrams/DB_UNICA_ERD.drawio`
- Table: `quiz_attempts`
- API: `GET /api/v1/mentor/courses/{course_id}/analytics`

## 2. ERD-defined columns

| Column | Type | Constraint/Relation |
|---|---|---|
| `id` | `BIGSERIAL` | PK |
| `quiz_id` | `BIGINT` | FK → quizzes.id |
| `user_id` | `BIGINT` | FK → users.id |
| `started_at` | `TIMESTAMP` | NOT NULL |
| `submitted_at` | `TIMESTAMP` | NULL |
| `score` | `NUMERIC(6,2)` | NULL |
| `status` | `VARCHAR(20)` | DEFAULT IN_PROGRESS |

## 3. API usage

- Entity involvement is supported by the Activity/ERD mapping used by this DD.
- Exact columns read/written, predicates, join projection, transaction boundary, and mutation values are only fixed where `05_Data_Mapping.md` has explicit source evidence.
- Any remaining detail is `TBD`; **không suy diễn column usage chỉ vì column tồn tại trong ERD**.
