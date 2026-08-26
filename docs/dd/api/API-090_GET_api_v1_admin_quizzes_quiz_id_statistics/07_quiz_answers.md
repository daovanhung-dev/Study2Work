---
title: "DB Mapping — quiz_answers"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
---

# DB Mapping — `quiz_answers`

## 1. Table source

- Source: `docs/diagrams/DB_UNICA_ERD.drawio`
- Table: `quiz_answers`
- API: `GET /api/v1/admin/quizzes/{quiz_id}/statistics`

## 2. ERD-defined columns

| Column | Type | Constraint/Relation |
|---|---|---|
| `id` | `BIGSERIAL` | PK |
| `attempt_id` | `BIGINT` | FK → quiz_attempts.id |
| `question_id` | `BIGINT` | FK → quiz_questions.id |
| `choice_id` | `BIGINT` | FK → quiz_choices.id |
| `is_correct` | `BOOLEAN` | NOT NULL |
| `score_received` | `NUMERIC(5,2)` | DEFAULT 0 |

## 3. API usage

- Entity involvement is supported by the Activity/ERD mapping used by this DD.
- Exact columns read/written, predicates, join projection, transaction boundary, and mutation values are only fixed where `05_Data_Mapping.md` has explicit source evidence.
- Any remaining detail is `TBD`; **không suy diễn column usage chỉ vì column tồn tại trong ERD**.
