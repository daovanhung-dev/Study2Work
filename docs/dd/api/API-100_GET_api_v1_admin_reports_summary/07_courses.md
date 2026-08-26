---
title: "DB Mapping — courses"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
---

# DB Mapping — `courses`

## 1. Table source

- Source: `docs/diagrams/DB_UNICA_ERD.drawio`
- Table: `courses`
- API: `GET /api/v1/admin/reports/summary`

## 2. ERD-defined columns

| Column | Type | Constraint/Relation |
|---|---|---|
| `id` | `BIGSERIAL` | PK |
| `mentor_id` | `BIGINT` | FK → users.id |
| `name` | `VARCHAR(200)` | NOT NULL |
| `description` | `TEXT` | NULL |
| `thumbnail_url` | `TEXT` | NULL |
| `price` | `NUMERIC(12,2)` | DEFAULT 0 |
| `status` | `VARCHAR(20)` | DEFAULT DRAFT |
| `created_at` | `TIMESTAMP` | NOT NULL |
| `updated_at` | `TIMESTAMP` | NOT NULL |

## 3. API usage

- Entity involvement is supported by the Activity/ERD mapping used by this DD.
- Exact columns read/written, predicates, join projection, transaction boundary, and mutation values are only fixed where `05_Data_Mapping.md` has explicit source evidence.
- Any remaining detail is `TBD`; **không suy diễn column usage chỉ vì column tồn tại trong ERD**.
