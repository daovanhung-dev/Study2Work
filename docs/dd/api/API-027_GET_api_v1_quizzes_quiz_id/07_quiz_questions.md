---
title: "DB Mapping — quiz_questions"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
---

# DB Mapping — `quiz_questions`

## 1. Table source

- Source: `docs/diagrams/DB_UNICA_ERD.drawio`
- Table: `quiz_questions`
- API: `GET /api/v1/quizzes/{quiz_id}`

## 2. ERD-defined columns

| Column | Type | Constraint/Relation |
|---|---|---|
| `id` | `BIGSERIAL` | PK |
| `quiz_id` | `BIGINT` | FK → quizzes.id |
| `question_text` | `TEXT` | NOT NULL |
| `sort_order` | `INT` | DEFAULT 0 |
| `score` | `NUMERIC(5,2)` | DEFAULT 1 |

## 3. API usage

- Entity involvement is supported by the Activity/ERD mapping used by this DD.
- Exact columns read/written, predicates, join projection, transaction boundary, and mutation values are only fixed where `05_Data_Mapping.md` has explicit source evidence.
- Any remaining detail is `TBD`; **không suy diễn column usage chỉ vì column tồn tại trong ERD**.
