---
title: "DB Mapping — notifications"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
---

# DB Mapping — `notifications`

## 1. Table source

- Source: `docs/diagrams/DB_UNICA_ERD.drawio`
- Table: `notifications`
- API: `GET /api/v1/admin/reports/community-impact`

## 2. ERD-defined columns

| Column | Type | Constraint/Relation |
|---|---|---|
| `id` | `BIGSERIAL` | PK |
| `user_id` | `BIGINT` | FK → users.id, NULL |
| `sender_id` | `BIGINT` | FK → users.id, NULL |
| `title` | `VARCHAR(200)` | NOT NULL |
| `content` | `TEXT` | NOT NULL |
| `type` | `VARCHAR(30)` | NULL |
| `is_read` | `BOOLEAN` | DEFAULT FALSE |
| `created_at` | `TIMESTAMP` | NOT NULL |

## 3. API usage

- Entity involvement is supported by the Activity/ERD mapping used by this DD.
- Exact columns read/written, predicates, join projection, transaction boundary, and mutation values are only fixed where `05_Data_Mapping.md` has explicit source evidence.
- Any remaining detail is `TBD`; **không suy diễn column usage chỉ vì column tồn tại trong ERD**.
