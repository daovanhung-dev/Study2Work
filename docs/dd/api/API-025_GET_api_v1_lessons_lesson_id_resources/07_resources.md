---
title: "DB Mapping — resources"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
---

# DB Mapping — `resources`

## 1. Table source

- Source: `docs/diagrams/DB_UNICA_ERD.drawio`
- Table: `resources`
- API: `GET /api/v1/lessons/{lesson_id}/resources`

## 2. ERD-defined columns

| Column | Type | Constraint/Relation |
|---|---|---|
| `id` | `BIGSERIAL` | PK |
| `lesson_id` | `BIGINT` | FK → lessons.id |
| `name` | `VARCHAR(200)` | NOT NULL |
| `resource_type` | `VARCHAR(20)` | NOT NULL |
| `url` | `TEXT` | NOT NULL |
| `created_at` | `TIMESTAMP` | NOT NULL |

## 3. API usage

- Entity involvement is supported by the Activity/ERD mapping used by this DD.
- Exact columns read/written, predicates, join projection, transaction boundary, and mutation values are only fixed where `05_Data_Mapping.md` has explicit source evidence.
- Any remaining detail is `TBD`; **không suy diễn column usage chỉ vì column tồn tại trong ERD**.
