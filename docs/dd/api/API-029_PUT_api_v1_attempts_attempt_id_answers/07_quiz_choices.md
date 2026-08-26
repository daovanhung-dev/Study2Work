---
title: "DB Mapping — quiz_choices"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
---

# DB Mapping — `quiz_choices`

## 1. Table source

- Source: `docs/diagrams/DB_UNICA_ERD.drawio`
- Table: `quiz_choices`
- API: `PUT /api/v1/attempts/{attempt_id}/answers`

## 2. ERD-defined columns

| Column | Type | Constraint/Relation |
|---|---|---|
| `id` | `BIGSERIAL` | PK |
| `question_id` | `BIGINT` | FK → quiz_questions.id |
| `choice_text` | `TEXT` | NOT NULL |
| `is_correct` | `BOOLEAN` | DEFAULT FALSE |

## 3. API usage

- Entity involvement is supported by the Activity/ERD mapping used by this DD.
- Exact columns read/written, predicates, join projection, transaction boundary, and mutation values are only fixed where `05_Data_Mapping.md` has explicit source evidence.
- Any remaining detail is `TBD`; **không suy diễn column usage chỉ vì column tồn tại trong ERD**.
