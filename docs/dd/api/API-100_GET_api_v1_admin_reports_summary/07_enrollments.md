---
title: "DB Mapping — enrollments"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
---

# DB Mapping — `enrollments`

## 1. Table source

- Source: `docs/diagrams/DB_UNICA_ERD.drawio`
- Table: `enrollments`
- API: `GET /api/v1/admin/reports/summary`

## 2. ERD-defined columns

| Column | Type | Constraint/Relation |
|---|---|---|
| `id` | `BIGSERIAL` | PK |
| `user_id` | `BIGINT` | FK → users.id |
| `course_id` | `BIGINT` | FK → courses.id |
| `status` | `VARCHAR(20)` | DEFAULT ACTIVE |
| `enrolled_at` | `TIMESTAMP` | NOT NULL |
| `completed_at` | `TIMESTAMP` | NULL |

## 3. API usage

- Entity involvement is supported by the Activity/ERD mapping used by this DD.
- Exact columns read/written, predicates, join projection, transaction boundary, and mutation values are only fixed where `05_Data_Mapping.md` has explicit source evidence.
- Any remaining detail is `TBD`; **không suy diễn column usage chỉ vì column tồn tại trong ERD**.
