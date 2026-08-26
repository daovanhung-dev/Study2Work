---
title: "DB Mapping — payments"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
---

# DB Mapping — `payments`

## 1. Table source

- Source: `docs/diagrams/DB_UNICA_ERD.drawio`
- Table: `payments`
- API: `GET /api/v1/admin/reports/community-impact`

## 2. ERD-defined columns

| Column | Type | Constraint/Relation |
|---|---|---|
| `id` | `BIGSERIAL` | PK |
| `user_id` | `BIGINT` | FK → users.id |
| `course_id` | `BIGINT` | FK → courses.id |
| `amount` | `NUMERIC(12,2)` | NOT NULL |
| `provider` | `VARCHAR(50)` | NOT NULL |
| `transaction_code` | `VARCHAR(100)` | UNIQUE |
| `status` | `VARCHAR(20)` | DEFAULT PENDING |
| `paid_at` | `TIMESTAMP` | NULL |
| `created_at` | `TIMESTAMP` | NOT NULL |

## 3. API usage

- Entity involvement is supported by the Activity/ERD mapping used by this DD.
- Exact columns read/written, predicates, join projection, transaction boundary, and mutation values are only fixed where `05_Data_Mapping.md` has explicit source evidence.
- Any remaining detail is `TBD`; **không suy diễn column usage chỉ vì column tồn tại trong ERD**.
