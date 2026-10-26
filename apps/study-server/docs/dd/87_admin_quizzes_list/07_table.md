---
title: "Định nghĩa table"
order: 7
dd_id: "87"
api_name: "Lấy danh sách quiz"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Phạm vi thao tác

N/A — READ-ONLY API. Runtime hiện chỉ đọc Quiz metadata và không truy vấn question/choice child tables. Không có INSERT/UPDATE/DELETE/UPSERT. Các mutation thuộc API #88–#90; aggregate thuộc #91.

## Candidate read source — legacy quizzes

| Thuộc tính | Giá trị |
|---|---|
| Physical table | quizzes |
| Logical table | Quiz |
| Operation | SELECT only |
| Data Mapping step | [Q1 — Step 2](./05_Data_Mapping.md#step-2-read-quiz-page) |
| Source evidence | infra/postgres/study-server/DB.sql legacy DDL artifact |
| Live schema status | Chưa xác minh |

| Physical column | Candidate response/filter mapping | Nullable in legacy DDL | Notes |
|---|---|---:|---|
| id | Quiz.id; sort tie-break | No | BIGSERIAL primary key. |
| course_id | Quiz.course_id; query course | Yes | Reusable Quiz requires int64; discrepancy. |
| name | Quiz.title | No | Alias name → title. |
| passing_score | Quiz.passing_score | Yes in DDL | NUMERIC(5,2); required decimal-string in contract. |
| time_limit_minutes | Quiz.duration_minutes | Yes | Alias candidate; output optional. |
| status | Query status only | Yes in DDL | Not a field in Quiz response; enum/casing unresolved. |
| description | No mapping | Yes | Not in reusable Quiz schema; do not return. |
| created_at | No mapping | No | Not in reusable Quiz schema; do not return. |
| updated_at | No mapping | No | Not in reusable Quiz schema; do not return. |

## Candidate read source — legacy quiz_questions

| Physical column | Candidate response mapping | Nullable in legacy DDL | Notes |
|---|---|---:|---|
| id | QuizQuestion.id | No | BIGSERIAL primary key. |
| quiz_id | Parent Quiz relation | Yes | Candidate relation; DDL nullable. |
| question_text | QuizQuestion.text | No | Alias candidate. |
| sort_order | Question order | Yes | Candidate ascending order; tie-break id ASC is DERIVED. |
| score | No mapping | Yes | Not present in reusable QuizQuestion. |
| type | No mapping | N/A | No type column in legacy table. |

## Candidate read source — legacy quiz_choices

| Physical column | Candidate response mapping | Nullable in legacy DDL | Notes |
|---|---|---:|---|
| id | QuizChoice candidate only | No | No reusable QuizChoice schema. |
| question_id | Parent question relation | Yes | Candidate relation; DDL nullable. |
| choice_text | QuizChoice candidate only | No | Logical property name not defined. |
| is_correct | No mapping | Yes | Not declared in QuizChoice contract; do not expose as response field without approval. |

## Non-selected V1-PILOT model

infra/postgres/02_study_db.sql defines UUID assessments, UUID quiz_questions linked by assessment_id, and UUID quiz_options. The catalog and legacy model use BIGINT quiz_id and quiz_choices. Do not treat the V1-PILOT tables as equivalent or as the current live schema.

## Write mapping

No write mapping applies. Do not create audit, statistics, attempt, or mutation mappings for this GET endpoint.
---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `table`
- Dimension: `A1:BA35`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `19`
- Số vùng merge: `5`

<details>
<summary>Danh sách vùng merge</summary>

- `W34:BA34`
- `W14:BA14`
- `W15:BA15`
- `W19:BA19`
- `W32:BA32`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `A2` | № |  |
| 2 | `B2` | Tên table |  |
| 3 | `B3` | SB |  |
| 3 | `S3` | Độ dài |  |
| 3 | `T3` | Dấu phẩy thập phân |  |
| 3 | `U3` | Bắt buộc |  |
| 3 | `V3` | Main key |  |
| 3 | `W3` | Nội dung setting |  |
| 4 | `B4` | № |  |
| 4 | `C4` | Item ID |  |
| 4 | `I4` | Item name |  |
| 4 | `O4` | Kiểu |  |
| 5 | `A5` | 1 |  |
| 5 | `B5` | table id |  |
| 5 | `I5` | table name |  |
| 6 | `B6` | Update |  |
| 6 | `I6` | Trường hợp số record get được từ xử lý 3. của sheet [３．Data mapping]  > 0 |  |
| 21 | `B21` | Insert |  |
| 21 | `I21` | Trường hợp số record get được từ xử lý 3. của sheet [３．Data mapping]  = 0 |  |

</details>
